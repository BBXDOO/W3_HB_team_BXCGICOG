from .base import RuntimeAgent


class ChatGPTAgent(RuntimeAgent):
    module_name = "ChatGPT"
    action_label = "completed architecture flow"
    # W3 ecosystem role: flow architect / executor (module.json role)
    mpcp_role = "flow_architecture"
    mpcp_concepts = ["flow", "architecture", "execution", "executor"]
