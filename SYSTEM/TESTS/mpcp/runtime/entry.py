from mpcp.runtime.executor import run, register, to_mpcp_output
from mpcp.modew.base_modew import BaseModew


class DesignModew(BaseModew):
    """
    Design Modew — example execution unit.

    Extends BaseModew to use the full A→F pillar pipeline
    defined in mpcp_pillar.md and base_modew.py.
    """

    # ---- Stage overrides ----

    def stage_B_validate(self, data):
        """Validate that a TASK key is present in context."""
        if "TASK" not in self.context:
            raise ValueError("DESIGN: missing TASK in context")
        return data

    def stage_D_process(self, data):
        """Core design processing."""
        return {"action": "design_done", "task": self.context.get("TASK")}

    def stage_F_output(self, data):
        """Produce final output value (BaseModew.run() wraps it in state dict)."""
        return data.get("action", "design_done")


# bind TASK → MODEW
register("design", DesignModew)


if __name__ == "__main__":
    result = run("TASK:design")
    # print internal dict for debugging
    print(result)
    # print external MPCP format string
    print(to_mpcp_output(result))
