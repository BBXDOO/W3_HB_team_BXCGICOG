from .base import RuntimeAgent


class REDRAgent(RuntimeAgent):
    module_name = "REDR"
    action_label = "completed risk escalation decision"
    mpcp_role = "risk_escalation"
    mpcp_concepts = ["risk", "escalation", "decision", "review"]
