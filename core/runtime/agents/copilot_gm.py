from .base import RuntimeAgent


class CopilotGmAgent(RuntimeAgent):
    module_name = "Copilot-Gm"
    action_label = "completed governance review"
    # W3 ecosystem role: governance / structural consistency (W3LGU_MPCP_ROLE_MAPPING.md §9)
    mpcp_role = "governance"
    mpcp_concepts = ["governance", "policy", "compliance", "structural consistency"]
