import copy
import json
import unittest
from pathlib import Path

from croll.contracts import (
    ContractError,
    validate_boundary_manifest,
    validate_dispatch_plan,
    validate_workset,
)


ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "examples"
SCHEMAS = ROOT / "schema"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class TestCrollContracts(unittest.TestCase):
    def test_all_schema_files_are_json_schema_2020_12(self):
        schemas = sorted(SCHEMAS.glob("*.schema.json"))
        self.assertEqual(
            [path.name for path in schemas],
            ["boundary.schema.json", "dispatch-plan.schema.json", "workset.schema.json"],
        )
        for path in schemas:
            with self.subTest(path=path.name):
                schema = load_json(path)
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(schema["type"], "object")
                self.assertTrue(schema["required"])

    def test_dispatch_schema_reference_exists(self):
        schema = load_json(SCHEMAS / "dispatch-plan.schema.json")
        reference = schema["properties"]["workset"]["$ref"]
        self.assertTrue((SCHEMAS / reference).is_file())

    def test_shipped_examples_satisfy_runtime_contracts(self):
        validate_boundary_manifest(load_json(EXAMPLES / "boundary.w3-internal.json"))
        validate_workset(load_json(EXAMPLES / "workset.rock.json"))
        validate_dispatch_plan(load_json(EXAMPLES / "dispatch-plan.jazz.json"))

    def test_boundary_requires_w3_scope_and_minimum_denies(self):
        manifest = load_json(EXAMPLES / "boundary.w3-internal.json")
        invalid_scope = copy.deepcopy(manifest)
        invalid_scope["network_scope"] = "public"
        with self.assertRaisesRegex(ContractError, "W3-scoped"):
            validate_boundary_manifest(invalid_scope)

        missing_deny = copy.deepcopy(manifest)
        missing_deny["boundary"]["deny"].remove("unreviewed_execution")
        with self.assertRaisesRegex(ContractError, "unreviewed_execution"):
            validate_boundary_manifest(missing_deny)

    def test_dispatch_plan_cannot_enable_execution_or_mutation(self):
        plan = load_json(EXAMPLES / "dispatch-plan.jazz.json")
        for field in ("execution_allowed", "mutated"):
            with self.subTest(field=field):
                unsafe = copy.deepcopy(plan)
                unsafe[field] = True
                with self.assertRaises(ContractError):
                    validate_dispatch_plan(unsafe)

    def test_nested_safety_permissions_must_remain_false(self):
        plan = load_json(EXAMPLES / "dispatch-plan.jazz.json")
        for field in (
            "modew_execution_allowed",
            "truth_mutation_allowed",
            "repo_write_allowed",
            "direct_merge_allowed",
        ):
            with self.subTest(field=field):
                unsafe = copy.deepcopy(plan)
                unsafe["safety"][field] = True
                with self.assertRaisesRegex(ContractError, field):
                    validate_dispatch_plan(unsafe)

    def test_contract_version_is_locked(self):
        workset = load_json(EXAMPLES / "workset.rock.json")
        workset["contract_version"] = "2.0"
        with self.assertRaisesRegex(ContractError, "contract_version"):
            validate_workset(workset)


if __name__ == "__main__":
    unittest.main()
