"""Read-only equipment: return the context already scoped by Paper/ENV."""
from copy import deepcopy

from .base_modew import BaseModew


class CondienViewModew(BaseModew):
    def stage_D_process(self, data):
        if not isinstance(data.get("CONDIEN"), dict):
            raise ValueError("CONDIEN_LIB:SCOPED_CONTEXT_REQUIRED")
        return {"context": deepcopy(data["CONDIEN"]), "context_ref": data.get("CONTEXT_REF")}
