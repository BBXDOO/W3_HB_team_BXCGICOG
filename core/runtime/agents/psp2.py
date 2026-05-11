from .base import RuntimeAgent


class PSP2Agent(RuntimeAgent):
    module_name = "PSP2"
    action_label = "completed pointer-stamp routing"
    mpcp_role = "pr_flow_routing"
    mpcp_concepts = ["route", "stamp", "pr flow", "handoff"]
