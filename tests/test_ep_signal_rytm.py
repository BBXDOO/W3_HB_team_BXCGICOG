from dataclasses import FrozenInstanceError

import pytest

from protocol.EP_SIGNAL.ep_signal_adapter import ep_signal_to_rytm, from_rytm_signal, to_ep_signal, to_rytm_signal
from protocol.EP_SIGNAL.rytm import build_rytm_preview, parse_rhythm, parse_rytm_signal, rytm_from_binary


def test_rytm_signal_round_trips_binary_and_keeps_meta_tokens():
    binary = "00000000001111111111000000"

    signal = to_rytm_signal(binary, meta=("cross_x", "ep_signal"))
    parsed = parse_rytm_signal(signal)

    assert signal == "0/AA6'CROSS_X'EP_SIGNAL'-10//BIN."
    assert parsed.to_binary() == binary
    assert parsed.meta == ("CROSS_X", "EP_SIGNAL")
    assert from_rytm_signal(signal) == binary


def test_ep_signal_can_be_exposed_as_immutable_rytm_packet():
    ep_signal = to_ep_signal("00110011")
    rytm = ep_signal_to_rytm(ep_signal, meta=("w3_api",))

    assert ep_signal == "0/2222-4'BIN"
    assert rytm.to_signal() == "0/2222'W3_API'-4//BIN."
    assert rytm.source_ep_signal == ep_signal
    assert rytm.to_binary() == "00110011"

    with pytest.raises(FrozenInstanceError):
        rytm.start = "1"  # type: ignore[misc]


def test_rytm_preview_is_non_mutating_and_reversible():
    preview = build_rytm_preview("111000", meta=("cross_x",))

    assert preview["mode"] == "preview_only"
    assert preview["mutated"] is False
    assert preview["rytm_signal"] == "1/33'CROSS_X'-3//BIN."
    assert parse_rytm_signal(str(preview["rytm_signal"])).to_binary() == "111000"
    assert "protocol/EP_SIGNAL/RYTM_SIGNAL.md" in preview["references"]


def test_rytm_rejects_invalid_or_non_reversible_packets():
    assert parse_rhythm("9AF*16*") == (9, 10, 15, 16)

    with pytest.raises(ValueError):
        rytm_from_binary("10x01")
    with pytest.raises(ValueError):
        parse_rytm_signal("0/33-99//BIN.")
    with pytest.raises(ValueError):
        parse_rhythm("0")
