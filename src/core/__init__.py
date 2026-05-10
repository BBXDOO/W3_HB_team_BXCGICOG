"""
W3 Core Module
--------------
Minimal, composable foundations aligned with MPCP / W3Lgu concepts.

Public surface:
  condien  — Condien: adaptive meaning/state/context layer
  blueprint — Blueprint: declarative setup/plan model
"""

from src.core.condien import Condien, CondienLayer, CONTINUITY_MODES, REBASE_MODES  # noqa: F401
from src.core.blueprint import Blueprint, parse_blueprint, BlueprintError  # noqa: F401
