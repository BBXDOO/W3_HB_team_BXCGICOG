from typing import Dict, Any

class ChainPointerOperator:
    @staticmethod
    def extract_paper_pack(event_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "PAPER_PACK_ID": event_data.get("PAPER_PACK_HINT"),
            "SOURCE_EVENT": event_data.get("EVENT_ID"),
            "TRACE_ID": event_data.get("TRACE_ID"),
            "TIMESTAMP": event_data.get("TIMESTAMP")
        }

    @staticmethod
    def build_cross_x_plan(event_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "PLAN_ID": f"PLAN_{event_data.get('EVENT_ID')}",
            "FIELD": event_data.get("CROSS_FIELD_HINT"),
            "ASSIST_MODULES": event_data.get("ALLOWED_ASSIST"),
            "RETURN_TO": event_data.get("RETURN_TO"),
            "TRACE_ID": event_data.get("TRACE_ID")
        }
