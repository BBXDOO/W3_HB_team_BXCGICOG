"""Cross-L ingress and MPCP egress contracts at the ENV boundary."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from ..config import MPCPConfig, load_config
from ..adapter.w3db import build_w3db_evidence_candidate
from ..kernel.contract import MPCPContract
from ..lib.registry import LibraryRegistry
from .models import EnvironmentSnapshot, MPCPWorkUnit
from .probe import probe_environment


class CrossLEnvironmentBoundary:
    """Validate Cross-L intent before MPCP conversion and execution."""

    def __init__(self, config: MPCPConfig | None = None) -> None:
        self.config = config or load_config()
        self.libraries = LibraryRegistry(self.config)

    @staticmethod
    def _mapping(value: Any, name: str) -> Mapping[str, Any]:
        if not isinstance(value, Mapping):
            raise ValueError(f"MPCP_ENV:{name}_MUST_BE_MAPPING")
        return value

    @staticmethod
    def _text(value: Any, name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"MPCP_ENV:{name}_REQUIRED")
        return value.strip()

    @staticmethod
    def _strings(value: Any, name: str) -> tuple[str, ...]:
        if value is None:
            return ()
        if isinstance(value, str):
            values = [item.strip() for item in value.split(",") if item.strip()]
        elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
            values = list(value)
        else:
            raise ValueError(f"MPCP_ENV:{name}_MUST_BE_STRING_LIST")
        if not all(isinstance(item, str) and item.strip() for item in values):
            raise ValueError(f"MPCP_ENV:{name}_MUST_BE_STRING_LIST")
        return tuple(item.strip() for item in values)

    def _select_language(self, workset: Mapping[str, Any], paper: Mapping[str, Any]) -> tuple[str, str]:
        explicit_tag = paper.get("LANGUAGE_TAG") or paper.get("language_tag")
        if explicit_tag:
            family, short = self.libraries.validate_tag(str(explicit_tag))
            allowed_families = {item.upper() for item in self._strings(workset.get("tag_group"), "TAG_GROUP")}
            if family not in allowed_families:
                raise ValueError(f"MPCP_ENV:TAG_FAMILY_OUTSIDE_WORKSET:{family}")
            short = self.libraries.short_name(short)
            binding = self.libraries.resolve_language(short)
            if not binding.available:
                raise ValueError(f"MPCP_ENV:RUNTIME_UNAVAILABLE:{short}")
            return f"{family}:{short}", short

        families = self._strings(workset.get("tag_group"), "TAG_GROUP")
        candidates = self._strings(workset.get("lang_candidate"), "LANG_CANDIDATE")
        if not families or not candidates:
            raise ValueError("MPCP_ENV:LANGUAGE_SELECTION_CONTEXT_REQUIRED")
        binding = self.libraries.select_available(candidates)
        if binding is None:
            raise ValueError("MPCP_ENV:NO_COMPATIBLE_LANGUAGE_RUNTIME")
        family = families[0].upper()
        validated_family, short = self.libraries.validate_tag(f"{family}:{binding.language}")
        return f"{validated_family}:{short}", short

    def ingress(
        self,
        envelope: Mapping[str, Any],
        *,
        payload: Mapping[str, Any],
        paper: Mapping[str, Any],
        env_hints: Mapping[str, Any] | None = None,
        environment: EnvironmentSnapshot | None = None,
        condien: Any | None = None,
    ) -> MPCPWorkUnit:
        """Accept Cross-L data, inspect ENV, then create an MPCP work unit."""

        source = self._mapping(envelope, "CROSS_L_ENVELOPE")
        body = dict(self._mapping(payload, "PAYLOAD"))
        paper_data = self._mapping(paper, "PAPER")
        if source.get("kind") != "cross-code-dispatch":
            raise ValueError("MPCP_ENV:CROSS_L_KIND_INVALID")
        plan = self._mapping(source.get("cross_l_plan"), "CROSS_L_PLAN")
        workset = self._mapping(plan.get("workset"), "WORKSET")
        expected_scope = self.config.data["environment"]["cross_l_scope"]
        if plan.get("scope") != expected_scope:
            raise ValueError("MPCP_ENV:CROSS_L_SCOPE_INVALID")

        chain_id = self._text(source.get("chain_id"), "CHAIN_ID")
        event_id = self._text(source.get("event_id"), "EVENT_ID")
        task = self._text(paper_data.get("TASK") or paper_data.get("TARGET"), "TASK")
        intent = self._text(paper_data.get("INTENT"), "INTENT")
        boundary = self._text(workset.get("boundary"), "BOUNDARY")
        modew = self._text(plan.get("modew"), "MODEW")
        language_tag, language = self._select_language(workset, paper_data)
        snapshot = environment or probe_environment(hints=env_hints, config=self.config)

        condien_read = self._strings(paper_data.get("READ"), "READ")
        paper_deny = self._strings(paper_data.get("DENY"), "PAPER_DENY")
        if condien is not None:
            body["CONDIEN"] = self.scope_condien(condien, condien_read, paper_deny)

        return MPCPWorkUnit(
            chain_id=chain_id,
            event_id=event_id,
            task=task,
            intent=intent,
            scope=expected_scope,
            boundary=boundary,
            modew=modew,
            language_tag=language_tag,
            language=language,
            payload=body,
            paper=paper_data,
            condien_read=condien_read,
            condien_deny=paper_deny,
            deny=self._strings(workset.get("deny"), "DENY"),
            return_contract=self._strings(workset.get("return_contract"), "RETURN_CONTRACT"),
            env=snapshot,
            review=bool(plan.get("review", True)),
        )

    @staticmethod
    def scope_condien(
        condien: Any,
        read_declarations: tuple[str, ...],
        deny_declarations: tuple[str, ...] = (),
    ) -> dict:
        """Read only declared Condien layers through Condien's own access law."""
        if not hasattr(condien, "get_layer") or not hasattr(condien, "to_dict"):
            raise TypeError("MPCP_ENV:CONDIEN_INTERFACE_INVALID")
        def layer_name(declaration: str) -> str | None:
            normalized = declaration.strip()
            if normalized.upper().startswith("CONDIEN."):
                layer = normalized.split(".", 1)[1]
            elif normalized.upper().startswith("LAYER"):
                layer = normalized
            else:
                return None
            if layer.upper().startswith("LAYER"):
                layer = layer[5:].lstrip("_:-")
            return layer or None

        requested = [layer for item in read_declarations if (layer := layer_name(item))]
        denied = {layer for item in deny_declarations if (layer := layer_name(item))}
        scoped = {}
        for layer_name in requested:
            if layer_name in denied:
                continue
            layer = condien.get_layer(layer_name)
            scoped[layer_name] = dict(layer.data)
        return {
            "identity": condien.to_dict(),
            "layers": scoped,
            "requested": requested,
            "denied": sorted(denied),
            "mutated": False,
        }

    def egress(self, work: MPCPWorkUnit, result: Mapping[str, Any]) -> dict:
        """Validate MPCP result and return only the Cross-L contract fields."""

        result_data = dict(self._mapping(result, "RESULT"))
        MPCPContract.validate_output(result_data)
        required = set(work.return_contract)
        base = {
            "state": result_data["state"],
            "reason": result_data.get("reason") or result_data.get("error") or "mpcp_result",
            "trace": result_data.get("trace", []),
            "mutated": bool(result_data.get("mutated", False)),
            "review": bool(result_data.get("review", work.review)),
            "source_truth_mutated": bool(result_data.get("source_truth_mutated", False)),
            "env_mutated": bool(result_data.get("env_mutated", False)),
            "event_container_mutated": bool(result_data.get("event_container_mutated", False)),
        }
        if base["source_truth_mutated"] and "truth_mutation" in work.deny:
            base.update({
                "state": "block",
                "reason": "boundary_denied_source_truth_mutation",
                "error": "BOUNDARY_DENIED:truth_mutation",
                "review": True,
            })
        modew_output = result_data.get("result")
        output_fields = modew_output if isinstance(modew_output, Mapping) else {}
        missing = sorted(
            field for field in required
            if field not in result_data and field not in base and field not in output_fields
        )
        if missing:
            base["state"] = "WAIT"
            base["reason"] = "return_contract_incomplete"
            base["review"] = True
            base["missing_return_fields"] = missing
        for field in required:
            if field in result_data:
                base[field] = result_data[field]
            elif field in output_fields:
                base[field] = output_fields[field]
        return {
            "schema": "mpcp.cross_l.return.1",
            "w3lgu_profile": "W3Lgu-Result",
            "chain_id": work.chain_id,
            "event_id": work.event_id,
            "language_tag": work.language_tag,
            "boundary": work.boundary,
            "result": base,
            "env": work.env.to_dict(),
            "w3db_evidence": build_w3db_evidence_candidate(
                chain_id=work.chain_id,
                event_id=work.event_id,
                result=base,
            ),
            "source_truth_mutated": base["source_truth_mutated"],
        }
