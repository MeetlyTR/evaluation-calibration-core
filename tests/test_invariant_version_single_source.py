# Decision Ecosystem — evaluation-calibration-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INV-V1: Version single-source — pyproject.toml [project] version must match package __version__."""

import tomllib
from pathlib import Path

import eval_calibration_core


def test_version_single_source() -> None:
    """pyproject.toml version must equal eval_calibration_core.__version__ (no drift)."""
    repo_root = Path(__file__).resolve().parent.parent
    with (repo_root / "pyproject.toml").open("rb") as f:
        data = tomllib.load(f)
    pyproject_version = data["project"]["version"]
    assert eval_calibration_core.__version__ == pyproject_version, (
        f"Version drift: pyproject.toml has {pyproject_version!r}, "
        f"eval_calibration_core.__version__ is {eval_calibration_core.__version__!r}"
    )
