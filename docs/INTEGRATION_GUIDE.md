# Evaluation & Calibration Core Integration Guide

## Installation

```bash
pip install evaluation-calibration-core
```

Or from source:
```bash
pip install -e .
```

## Basic Usage

### CLI: Run Evaluation Suite

```bash
# Use built-in fixture suite
python -m eval_calibration_core.cli run --suite smoke --out reports/smoke

# Use custom JSONL file
python -m eval_calibration_core.cli run --in traces.jsonl --out reports/custom
```

### Programmatic Usage

```python
from eval_calibration_core.io.packet_reader import PacketReader
from eval_calibration_core.metrics.compute import compute_metrics
from eval_calibration_core.suites.invariants import check_invariants
from eval_calibration_core.report.model import Report
from eval_calibration_core.report.writer import write_report
from eval_calibration_core.contracts import check_expected_minor_range, get_schema_version

# Read packets
reader = PacketReader("traces.jsonl")
packets = reader.read_all()

# Compute metrics
metrics = compute_metrics(packets)

# Check invariants
invariant_results = check_invariants(packets)

# Check contract compatibility
contract_ok, contract_details = check_expected_minor_range(expected_major=0, min_minor=1, max_minor=1)

# Create report
report = Report(
    schema_version=get_schema_version(),
    suite_name="custom",
    input_stats={"total_packets": len(packets)},
    metrics=metrics,
    invariant_results=invariant_results,
    contract_matrix_check=contract_details,
)

# Write report
write_report(report, "reports/custom")
```

### Using Fixture Suites

```python
from eval_calibration_core.io.fixtures import load_fixture_suite

# Load synthetic suite
packets = load_fixture_suite("smoke")  # or "determinism", "guard_pressure"
```

## Report Structure

### JSON Report (`report.json`)

```json
{
  "report_version": "0.1.0",
  "schema_version": "0.1.0",
  "suite_name": "smoke",
  "metrics": {
    "action_distribution": {"HOLD": 10, "ACT": 5},
    "guard_trigger_rate": {"staleness_exceeded": 0.1},
    "latency_percentiles": {"p50": 10.0, "p95": 20.0, "p99": 30.0}
  },
  "invariant_results": {
    "contract_closure": true,
    "confidence_clamp": true
  },
  "contract_matrix_check": {
    "schema_version": "0.1.0",
    "expected_major": 0,
    "min_minor": 1,
    "max_minor": 1,
    "compatible": true
  }
}
```

### Markdown Report (`report.md`)

Includes:
- Report metadata
- Input statistics
- Metrics (action distribution, guard triggers, latency)
- Contract matrix check (pass/fail)
- Invariant results

## Integration with Other Cores

### MDM Engine

MDM Engine writes PacketV2 traces:

```python
from ami_engine.trace.trace_logger import TraceLogger

logger = TraceLogger(run_id="run_123", output_dir="./traces")
logger.log_packet(packet_v2)
```

Evaluation core reads these traces:

```bash
python -m eval_calibration_core.cli run --in traces/traces.jsonl --out reports/eval
```

### Decision Modulation Core

DMC modulation results are captured in PacketV2 `final_action` and `mismatch` fields. Evaluation core computes guard trigger rates from these fields.

## Contract Compatibility

Evaluation core checks schema compatibility on startup:

```python
from eval_calibration_core.contracts import check_schema_compatibility

check_schema_compatibility(expected_minor=1)  # Raises RuntimeError if incompatible
```

See `ECOSYSTEM_CONTRACT_MATRIX.md` in decision-schema repo for version compatibility details.
