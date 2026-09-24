import json
from pathlib import Path

from core.modules_loader import router


def test_modules_loader_uses_canonical_registry():
    registry = json.loads(Path("modules/registry.json").read_text(encoding="utf-8"))

    assert router.REGISTRY_FILE == Path("modules/registry.json").resolve()
    assert router.load_registry() == registry["routing"]


def test_every_routed_module_has_separately_owned_manifest_and_identity():
    for module_name in set(router.load_registry().values()):
        assert Path(f"modules/{module_name}/module.json").is_file()
        assert Path(f"core/identity/profiles/{module_name}.idp.json").is_file()


def test_modules_loader_does_not_own_registry_or_identity_data():
    assert not (Path("core/modules_loader") / "identity").exists()
    assert not (Path("core/modules_loader") / "idp-schema.json").exists()


def test_legacy_loader_directories_are_retired():
    assert not Path("core/module-loader").exists()
    assert not (Path("core") / ("module" + "_loader")).exists()
