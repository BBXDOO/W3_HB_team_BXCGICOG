from .base import RuntimeAgent


class REDRAgent(RuntimeAgent):
    module_name = "REDR"
    action_label = "read, tagged, and packaged the event before routing"
    mpcp_role = "reader_package_builder"
    mpcp_concepts = [
        "read",
        "reader",
        "tag",
        "package",
        "payload",
        "structure",
        "signal",
        "route",
        "memory",
        "trace",
        "non_mutation",
        "review",
    ]
