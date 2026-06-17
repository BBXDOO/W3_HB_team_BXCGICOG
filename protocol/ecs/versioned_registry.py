import uuid
from datetime import datetime
from typing import Dict, Any

class VersionedRegistry:
    def __init__(self):
        # เก็บข้อมูลเป็น {version_id: {event_chain}}
        self.versions: Dict[str, Dict[str, Any]] = {}
        self.current_version: str = None

    def create_version(self, chain: Dict[str, Any]) -> str:
        version_id = f"ver-{uuid.uuid4().hex[:8]}"
        timestamp = datetime.utcnow().isoformat()

        self.versions[version_id] = {
            "timestamp": timestamp,
            "chain": chain,
            "status": "ACTIVE"
        }
        self.current_version = version_id
        return version_id

    def rollback_to_version(self, version_id: str) -> Dict[str, Any]:
        if version_id in self.versions:
            self.current_version = version_id
            self.versions[version_id]["status"] = "ROLLED_BACK"
            return self.versions[version_id]["chain"]
        else:
            raise ValueError("Version not found")

    def get_current_chain(self) -> Dict[str, Any]:
        if self.current_version:
            return self.versions[self.current_version]["chain"]
        return {}

    def list_versions(self):
        return {vid: meta["timestamp"] for vid, meta in self.versions.items()}
