from core.runtime.agents.psp2 import PSP2Agent


def test_psp2_direct_dispatch_unknown_route_requires_review():
    result = PSP2Agent().dispatch({"package_id": "PKG-1"}, ["NEW_SYSTEM"])

    assert result["status"] == "REVIEW_REQUIRED"
    assert result["status"] != "DISPATCHED"
    assert result["review"] is True
    assert result["details"]["unknown_routes"] == ["NEW_SYSTEM"]


def test_psp2_direct_dispatch_px_without_bridge_requires_review():
    result = PSP2Agent().dispatch({"package_id": "PKG-2"}, ["PX"])

    assert result["status"] == "REVIEW_REQUIRED"
    assert result["status"] != "DISPATCHED"
    assert result["details"]["cross_routes"] == ["PX"]
