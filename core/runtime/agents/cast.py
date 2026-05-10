from .base import RuntimeAgent


class CastAgent(RuntimeAgent):
    module_name = "Cast"
    action_label = "completed structural adaptation / reasoning / interpretation output"
    # W3 ecosystem role: continuity + context bridge (W3LGU_MPCP_ROLE_MAPPING.md §9)
    mpcp_role = "continuity_context"
    mpcp_concepts = ["continuity", "context", "reasoning", "adaptation"]
