"""Report data model."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Report:
    """Evaluation report."""

    report_version: str = "0.1.0"
    schema_version: str = ""
    packet_versions: list[str] = field(default_factory=list)
    suite_name: str = ""
    seed: int | None = None
    input_stats: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, Any] = field(default_factory=dict)
    invariant_results: dict[str, bool] = field(default_factory=dict)
    calibration_summary: dict[str, Any] | None = None
    contract_matrix_check: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "report_version": self.report_version,
            "schema_version": self.schema_version,
            "packet_versions": self.packet_versions,
            "suite_name": self.suite_name,
            "seed": self.seed,
            "input_stats": self.input_stats,
            "metrics": self.metrics,
            "invariant_results": self.invariant_results,
            "calibration_summary": self.calibration_summary,
        }
        if self.contract_matrix_check is not None:
            result["contract_matrix_check"] = self.contract_matrix_check
        return result
