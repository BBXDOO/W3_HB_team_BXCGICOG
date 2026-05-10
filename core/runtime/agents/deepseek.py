from .base import RuntimeAgent


class DeepSeekAgent(RuntimeAgent):
    module_name = "DeepSeek"
    action_label = "completed structure planning"
    # W3 ecosystem role: scale / long-term planning (module.json role)
    mpcp_role = "planning"
    mpcp_concepts = ["scale", "planning", "long-term", "structure"]
