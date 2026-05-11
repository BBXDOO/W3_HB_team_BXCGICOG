from .base import RuntimeAgent


class LRC2Agent(RuntimeAgent):
    module_name = "LRC2"
    action_label = "completed lifecycle review checkpoint"
    mpcp_role = "lifecycle_review"
    mpcp_concepts = ["lifecycle", "checkpoint", "review", "compliance"]
