from .base import RuntimeAgent


class DTMLAgent(RuntimeAgent):
    module_name = "DTML"
    action_label = "completed decision trace mapping"
    mpcp_role = "decision_trace"
    mpcp_concepts = ["decision", "trace", "timeline", "memory"]
