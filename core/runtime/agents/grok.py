from .base import RuntimeAgent


class GrokAgent(RuntimeAgent):
    module_name = "Grok"
    action_label = "completed pattern scan"
    # W3 ecosystem role: pattern / signals / insight (module.json role)
    mpcp_role = "pattern_insight"
    mpcp_concepts = ["pattern", "signal", "signals", "insight", "knowledge"]
