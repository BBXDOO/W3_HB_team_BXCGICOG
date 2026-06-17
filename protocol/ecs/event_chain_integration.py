from protocol.ecs.event_chain_system import EventFrame, EventChainSystem, Confidence, CrossState
from protocol.mpcp.cooperative_contract import CooperativeContract

def ecs_with_contract():
    ecs = EventChainSystem()

    # สร้าง EventFrame สำหรับ git conflict
    event = EventFrame(
        event_id="Event-GIT-001",
        source="LOCAL",
        type_data="source_control",
        intent="sync_repo",
        logic_chain="repo_conflict_recovery",
        rooms=["Ev", "Si", "Ap", "Ca", "Cu", "Re"],
        active_systems=["W3Lgu", "REDR", "DTML", "Git", "Hospitication"],
        standby_systems=["File.void", "Cross-L", "Codex"],
        cross_state=CrossState.REVIEW,
        confidence=Confidence.AMBIGUOUS
    )

    ecs.add_event(event)
    processed_event = ecs.process_event(event)

    # สร้าง CooperativeContract เชื่อมกับ EventFrame
    contract = CooperativeContract(
        responsible_module="MPCP",
        assist_modules=["Cross-X", "W3Lgu"],
        cross_field="RepoConflictField",
        reason="Conflict detected in source control sync",
        return_to="MPCP",
        event_id=processed_event.event_id,
        end_event=processed_event.next_event or "STOP",
        trigger="repo_conflict",
        expected_gain=["primary result", "risk signal", "trace explanation"],
        papers=["Paper-GIT-Conflict-Review"],
        trace=processed_event.to_dict(),
        rot_type="ROT-RECOVERY",
        paper_pack_id="PP-GIT-2026",
        field_selected="Cross-X",
        temp_agreement=True,
        risk_flags=["merge_conflict", "uncertain"],
        distribution_mode="parallel",
        max_assist_routes=2,
        rejoin_strategy="merge",
        quality_check=True,
        env_ref="Termux/git_pull",
        stack_ref="W3DB_APPEND",
        lrc_ref="LRC2"
    )

    print("[E-CS] Processed Event:", processed_event.to_dict())
    print("[MPCP] Cooperative Contract:", contract.to_dict())

if __name__ == "__main__":
    ecs_with_contract()
