# mpcp/modew/base_modew.py

class BaseModew:
    """
    Base Modew (Pillar)
    Implements A–F execution flow aligned with MPCP + ROT
    """

    def __init__(self):
        self.context = {}
        self.trace = []
        self.memory = {
            "store": {},
            "history": [],
            "task_stats": {},
            "role_stats": {},
        }
        self.skills = {}
        self.capabilities = set()
        self.max_history = 50

    # =========================
    # CONTEXT
    # =========================
    def set_context(self, key, value):
        self.context[key] = value

    def set_role(self, role: str):
        self.set_context("ROLE", role)

    # =========================
    # MEMORY
    # =========================
    def remember(self, key, value):
        self.memory["store"][key] = value

    def recall(self, key, default=None):
        return self.memory["store"].get(key, default)

    # =========================
    # SKILLS / CAPABILITIES
    # =========================
    def register_skill(self, name, skill_fn):
        if not callable(skill_fn):
            raise TypeError("skill_fn must be callable")
        self.skills[name] = skill_fn

    def use_skill(self, name, *args, **kwargs):
        if name not in self.skills:
            raise ValueError(f"SKILL_NOT_FOUND:{name}")
        return self.skills[name](*args, **kwargs)

    def grant_capability(self, capability: str):
        if not isinstance(capability, str) or not capability.strip():
            raise ValueError("capability must be non-empty string")
        self.capabilities.add(capability.strip())

    def has_capability(self, capability: str):
        return capability in self.capabilities

    def require_capability(self, capability: str):
        if not self.has_capability(capability):
            raise PermissionError(f"CAPABILITY_REQUIRED:{capability}")
        return True

    # =========================
    # TRACE (ENV PRESERVE)
    # =========================
    def log(self, stage, data):
        self.trace.append({
            "stage": stage,
            "data": data,
            "env": dict(self.context)  # no reduction (ENV LAW)
        })

    # =========================
    # A–F PIPELINE
    # =========================
    def run(self):
        """
        Execute the A–F pillar pipeline.

        Prerequisites: call set_context("TASK", ...) before run() so that
        'cause' is captured correctly for CAUSE→ACTION→RESULT traceability.
        """
        cause = self.context.get("TASK")
        role = self.context.get("ROLE", "default")
        try:
            a = self.stage_A_input()
            self.log("A", a)

            b = self.stage_B_validate(a)
            self.log("B", b)

            c = self.stage_C_route(b)
            self.log("C", c)

            d = self.stage_D_process(c)
            self.log("D", d)

            e = self.stage_E_transition(d)
            self.log("E", e)

            f = self.stage_F_output(e)
            self.log("F", f)

            # CAUSE → ACTION → RESULT: include cause so trace is complete
            result = {
                "state": "SUCCESS",
                "cause": cause,
                "result": f,
                "trace": self.trace,
                "role": role,
            }
            self._remember_run(cause, role, result["state"])
            return result

        except Exception as e:
            result = {
                "state": "STOP",
                "cause": cause,
                "error": str(e),
                "trace": self.trace,
                "role": role,
            }
            self._remember_run(cause, role, result["state"], error=str(e))
            return result

    def _remember_run(self, cause, role, state, error=None):
        history = self.memory["history"]
        history.append({
            "cause": cause,
            "role": role,
            "state": state,
            "error": error,
        })
        if len(history) > self.max_history:
            history.pop(0)

        if cause:
            task_stats = self.memory["task_stats"]
            stat = task_stats.get(cause, {"runs": 0, "last_state": None})
            stat["runs"] += 1
            stat["last_state"] = state
            task_stats[cause] = stat

        role_stats = self.memory["role_stats"]
        role_stat = role_stats.get(role, {"runs": 0, "last_state": None})
        role_stat["runs"] += 1
        role_stat["last_state"] = state
        role_stats[role] = role_stat

        self.remember("last_state", state)
        self.remember("last_cause", cause)
        self.remember("last_role", role)
        if error:
            self.remember("last_error", error)

    # =========================
    # STAGES (OVERRIDE REQUIRED)
    # =========================
    def stage_A_input(self):
        return self.context

    def stage_B_validate(self, data):
        return data

    def stage_C_route(self, data):
        return data

    def stage_D_process(self, data):
        return data

    def stage_E_transition(self, data):
        return data

    def stage_F_output(self, data):
        return data
