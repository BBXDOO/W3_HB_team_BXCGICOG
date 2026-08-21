import unittest

from core.runtime.process_layer import run_w3lgu_packet_process_layer
from w3_api.adapters.w3lgu_adapter import build_cross_w3lgu_packet


class TestW3ApiMfcIntegration(unittest.TestCase):
    def test_api_packet_reaches_lrc2_checkpoint_without_persistence(self):
        packet = build_cross_w3lgu_packet(
            source="BBX19",
            intent="review memory route",
            target="W3DB",
            mode="cross",
            payload={"contract": "observe_only"},
        )

        result = run_w3lgu_packet_process_layer(
            packet,
            payload={"focus": "memory", "bridge_contract": "Cross-L"},
            process_id="PROC-API-MFC-1",
            timestamp="2026-08-21T00:00:00Z",
        )
        body = result.to_dict()

        self.assertEqual(
            [stage["stage"] for stage in body["stages"]],
            ["REDR", "PSP2", "DTML", "LRC2"],
        )
        self.assertEqual(list(body["agent_results"]), ["REDR", "PSP2", "DTML", "LRC2"])
        self.assertEqual(body["agent_results"]["LRC2"]["module"], "LRC2")
        self.assertEqual(
            body["agent_results"]["LRC2"]["decision"],
            "checkpoint_preview_ready",
        )
        self.assertEqual(
            body["agent_results"]["LRC2"]["details"]["identity"]["chain_id"],
            "PROC-API-MFC-1",
        )
        self.assertFalse(body["agent_results"]["LRC2"]["details"]["persistence"]["persisted"])
        self.assertFalse(body["mutated"])


if __name__ == "__main__":
    unittest.main()
