"""Exercise the E-CS implementation itself, distinct from Cross-X event records."""
import pytest
from ecs.event_chain_system import EventChainSystem, EventFrame, Confidence, CrossState


@pytest.mark.parametrize('confidence,result,next_event,state', [
    (Confidence.CLEAR, 'CONTINUE', 'inspection_NEXT', CrossState.ACTIVE),
    (Confidence.AMBIGUOUS, 'UNCLEAR', 'REVIEW_OR_OBSERVE', CrossState.REVIEW),
    (Confidence.UNCLEAR, 'STOP', 'WAIT', CrossState.STANDBY),
])
def test_native_ecs_preserves_event_and_routes_confidence(confidence, result, next_event, state):
    event = EventFrame('inspection', 'inspection:test', 'test', 'bounded native check',
                       'inspection', ['Ev'], ['E-CS'], [], CrossState.ACTIVE, confidence)
    system = EventChainSystem()
    system.add_event(event)
    actual = system.process_event(system.chain[0]).to_dict()
    assert actual['event_id'] == 'inspection' and actual['source'] == 'inspection:test'
    assert actual['result'] == result and actual['next'] == next_event
    assert actual['cross_state'] == state.value and actual['mutated'] is False
