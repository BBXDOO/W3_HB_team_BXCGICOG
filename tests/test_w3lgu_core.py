from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from protocol.w3lgu import (
    W3LguError,
    from_mpcp,
    from_text,
    normalize_line,
    parse_five_line_program,
    parse_line,
    run_five_line,
    run_line,
    signal_for_state,
    split_events,
    to_mpcp,
    validate_five_line,
    validate_packet,
)


def test_parse_line_repairs_line_c_spaces_to_canonical_packet():
    packet = parse_line("TASK:sync MODE:auto STATE:ready")

    assert packet.to_text() == "TASK:sync,MODE:auto,STATE:ready"
    assert packet.get("TASK") == "sync"
    assert validate_packet(packet).ok


def test_packet_contract_is_immutable():
    packet = parse_line("TASK:sync")

    with pytest.raises(FrozenInstanceError):
        packet.pairs = ()


def test_semicolon_splits_event_sequence():
    packets = split_events("TASK:scan,STATE:ready;TASK:commit,STATE:done.")

    assert len(packets) == 2
    assert packets[0].get("TASK") == "scan"
    assert packets[1].get("STATE") == "done"


def test_signal_mapping_preserves_half_confidence_as_warn():
    packet = signal_for_state("SUCCESS", confidence=0.5)

    assert packet.get("STATE") == "warn"
    assert packet.get("COLOR") == "yellow"
    assert packet.get("SYM") == "●"


def test_five_line_program_preserves_mem_patch_law_event_signal_boundaries():
    program = parse_five_line_program(
        """
        MEM:LAST_STATE:idle
        PATCH:CASE:room3
        LAW:RULE:divide_by_2
        EVENT:TASK:sync,STATE:ready
        SIGNAL:STATE:ready,COLOR:blue,SYM:◆
        """
    )

    assert program.memory.get("LAST_STATE") == "idle"
    assert program.patch.get("CASE") == "room3"
    assert program.law.get("RULE") == "divide_by_2"
    assert program.event.get("TASK") == "sync"
    assert validate_five_line(program).ok


def test_five_line_rejects_missing_line():
    with pytest.raises(W3LguError):
        parse_five_line_program(
            """
            MEM:LAST_STATE:idle
            PATCH:CASE:room3
            LAW:RULE:divide_by_2
            EVENT:TASK:sync,STATE:ready
            """
        )


def test_runtime_outputs_signal_and_memory_without_external_side_effects():
    result = run_line("TASK:sync,STATE:done,MODEW:queue")

    assert result.normalized_packet.get("MODEW") == "queue"
    assert result.signal_packet.get("STATE") == "done"
    assert result.signal_packet.get("COLOR") == "green"
    assert result.memory_packet is not None
    assert result.memory_packet.get("LAST_STATE") == "done"


def test_runtime_runs_five_line_event_only():
    program = parse_five_line_program(
        """
        MEM:LAST_STATE:idle
        PATCH:CASE:room3
        LAW:RULE:observe_only
        EVENT:TASK:route,STATE:ready
        SIGNAL:STATE:ready,COLOR:blue,SYM:◆
        """
    )

    result = run_five_line(program)

    assert result.input_packet.get("TASK") == "route"
    assert result.signal_packet.get("STATE") == "ready"


def test_adapters_bridge_text_and_mpcp_without_losing_w3lgu_view():
    packet = from_text("TASK:sync STATE:ready", env="mobile")
    mpcp = to_mpcp(packet)
    restored = from_mpcp(mpcp)

    assert packet.get("ENV") == "mobile"
    assert mpcp["w3lgu"].startswith("EVENT:input")
    assert restored.get("TASK") == "sync"
    assert restored.get("STATE") == "ready"


def test_normalize_line_is_deterministic():
    assert normalize_line("TASK:build MODE:fast STATE:ready") == "TASK:build,MODE:fast,STATE:ready"
