# BOX / Library-WX Knowledge Infrastructure

- **Version:** 1.0
- **Owner:** BBX19
- **Scope:** Planner-only
- **Runtime authority:** None
- **Mutation:** False
- **Relations:** W3 / Library-WX / Cross-L / MPCP / W3-API

BOX is a lightweight reference layer. It makes reusable templates and
blueprints discoverable without duplicating documents or turning knowledge into
a runtime/state system.

## Components

- `templates/`: single-source templates; copy before use.
- `blueprints/`: declaration-only structural references.
- `references/`: stable reference knowledge.
- `registry/`: machine-readable metadata source of truth.
- `index/`: human-readable navigation generated/maintained from registry intent.
- `engine_index.py`: read-only lookup and registry validation.
- `indexor.py`: Binder-style suggestions.
- `portdc.py`: read-only registered-content export; it never writes targets.
- `log_info/`: append-only audit files maintained by an explicitly authorized human/tool.

## Safety contract

BOX may read, locate, recommend, and export reference data. It may not execute,
copy to a workspace, edit source files, append logs automatically, call a
network, or approve a merge. Consumers must copy before editing and retain the
original `template_id` as provenance.

## Quick checks

```bash
python -m unittest discover -s wx -p "test_*.py" -v
python -m croll --compact plan "PX:[1,1]" --box-suggestion
```

The second command only adds a registered suggestion to a non-executing CROLL plan.
