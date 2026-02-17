"""Write reports to JSON and Markdown."""

import json
from pathlib import Path

from eval_calibration_core.report.model import Report


def write_report(report: Report, output_dir: Path | str) -> None:
    """
    Write report to JSON and Markdown files.
    
    Args:
        report: Report instance
        output_dir: Output directory path
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write JSON
    json_path = output_dir / "report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report.to_dict(), f, indent=2)

    # Write Markdown
    md_path = output_dir / "report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(_format_markdown(report))


def _format_markdown(report: Report) -> str:
    """Format report as Markdown."""
    lines = [
        "# Evaluation Report",
        "",
        f"**Report Version**: {report.report_version}",
        f"**Schema Version**: {report.schema_version}",
        f"**Suite**: {report.suite_name}",
        "",
        "## Input Statistics",
        "",
    ]

    for key, value in report.input_stats.items():
        lines.append(f"- **{key}**: {value}")

    lines.extend(["", "## Metrics", ""])

    # Action distribution
    if "action_distribution" in report.metrics:
        lines.append("### Action Distribution")
        lines.append("")
        for action, count in report.metrics["action_distribution"].items():
            lines.append(f"- {action}: {count}")
        lines.append("")

    # Guard trigger rate
    if "guard_trigger_rate" in report.metrics:
        lines.append("### Guard Trigger Rate")
        lines.append("")
        for code, rate in report.metrics["guard_trigger_rate"].items():
            lines.append(f"- {code}: {rate:.3f}")
        lines.append("")

    # Safety invariant
    if "safety_invariant_pass_rate" in report.metrics:
        pass_rate = report.metrics["safety_invariant_pass_rate"]
        lines.append(f"### Safety Invariant Pass Rate: {pass_rate:.3f}")
        lines.append("")

    # Latency
    if "latency_percentiles" in report.metrics:
        lat = report.metrics["latency_percentiles"]
        lines.append("### Latency Percentiles")
        lines.append(f"- p50: {lat.get('p50', 0):.1f}ms")
        lines.append(f"- p95: {lat.get('p95', 0):.1f}ms")
        lines.append(f"- p99: {lat.get('p99', 0):.1f}ms")
        lines.append("")

    # Contract Matrix Check
    if report.contract_matrix_check:
        check = report.contract_matrix_check
        ok = check.get("compatible", False)
        status = "✅ PASS" if ok else "❌ FAIL"
        lines.append("## Contract Matrix Check")
        lines.append("")
        lines.append(f"**Status**: {status}")
        lines.append(f"**Schema Version**: {check.get('schema_version', 'unknown')}")
        lines.append(f"**Expected Range**: {check.get('expected_major', 0)}.{check.get('min_minor', 1)}.{check.get('max_minor', 1)}")
        lines.append("")
        lines.append("> See `ECOSYSTEM_CONTRACT_MATRIX.md` in decision-schema repo for version compatibility details.")
        lines.append("")

    # Invariants
    if report.invariant_results:
        lines.append("## Invariant Results")
        lines.append("")
        for name, passed in report.invariant_results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            lines.append(f"- {name}: {status}")
        lines.append("")

    return "\n".join(lines)
