"""Test suites."""

from eval_calibration_core.suites.determinism import DeterminismSuite
from eval_calibration_core.suites.guard_pressure import GuardPressureSuite
from eval_calibration_core.suites.smoke import SmokeSuite

__all__ = ["SmokeSuite", "DeterminismSuite", "GuardPressureSuite"]
