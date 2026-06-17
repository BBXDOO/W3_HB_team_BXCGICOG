from protocol.ecs.event_template import ECSEventTemplate
from protocol.ecs.cooperative_contract import ECSCooperativeContract
from protocol.ecs.chain_pointer_operator import ChainPointerOperator

def ecs_event_flow_example():
    template = ECSEventTemplate(
        template_id="EVT-ECS-DEMO",
        event_type="ECS_LIB_BLUEPRINT",
        scope="ECS_LIB_BUILD",
        required_fields=["code_set", "intent", "scope"],
        allowed_assist=["Cross-X", "W3Lgu"],
        paper_pack_hint="Papers-Pack-ECS",
        cross_field_hint="Cross-X",
        return_to="MPCP"
    )

    payload = {"code_set": "demo", "intent": "build_lib_blueprint", "scope": "ECS_LIB_BUILD"}
    template.validate_payload(payload)

    contract = ECSCooperativeContract(
        event_id="EVENT-ECS-01",
        responsible_module="ECS",
        assist_modules=["Cross-X", "W3Lgu"],
        cross_field="Cross-X",
        reason="Blueprint build request",
        expected_gain=["primary result", "trace explanation"],
        return_to="MPCP",
        trigger="build_request",
        trace=template.to_dict()
    )

    paper_pack = ChainPointerOperator.extract_paper_pack(template.to_dict())
    cross_plan = ChainPointerOperator.build_cross_x_plan(template.to_dict())

    print("[ECS] Contract:", contract.to_dict())
    print("[ECS] Paper Pack:", paper_pack)
    print("[ECS] Cross-X Plan:", cross_plan)

if __name__ == "__main__":
    ecs_event_flow_example()
