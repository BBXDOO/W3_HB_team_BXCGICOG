from .base import RuntimeAgent


class GeminiAgent(RuntimeAgent):
    module_name = "Gemini"
    action_label = "completed verification"
    # W3 ecosystem role: validation / cross-check (W3LGU_MPCP_ROLE_MAPPING.md §9)
    mpcp_role = "validation"
    mpcp_concepts = ["validation", "verification", "cross-check", "cross check"]
