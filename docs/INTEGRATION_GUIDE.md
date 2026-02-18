<!--
Decision Ecosystem — evaluation-calibration-core
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Integration Guide — evaluation-calibration-core

## Dependency

Pin schema version:
```toml
dependencies = ["decision-schema>=0.2,<0.3"]
```

## Basic Usage

```python
from pathlib import Path
from eval_calibration_core.io.packet_reader import PacketReader
from eval_calibration_core.metrics.compute import compute_metrics
from eval_calibration_core.report import build_report, write_report

# Read packets from JSONL file
reader = PacketReader("traces.jsonl")
packets = list(reader.read())

# Compute metrics
metrics = compute_metrics(packets)

print(f"Action distribution: {metrics['action_distribution']}")
print(f"Guard trigger rates: {metrics['guard_trigger_rates']}")
print(f"Latency percentiles: {metrics['latency_percentiles']}")
print(f"Safety invariant pass rate: {metrics['safety_invariant_pass_rate']}")

# Build and write report
report = build_report(packets, suite_name="my_suite")
write_report(report, Path("output"))
```

## Reading PacketV2 Traces

```python
from eval_calibration_core.io.packet_reader import PacketReader
from decision_schema.packet_v2 import PacketV2

reader = PacketReader("traces.jsonl")

for packet in reader.read():
    # packet is a PacketV2 instance
    print(f"Run ID: {packet.run_id}, Step: {packet.step}")
    print(f"Action: {packet.final_action.get('action')}")
    print(f"Latency: {packet.latency_ms}ms")
```

## Computing Metrics

```python
from eval_calibration_core.metrics.compute import compute_metrics

metrics = compute_metrics(packets)

# Access metrics
action_dist = metrics["action_distribution"]
guard_rates = metrics["guard_trigger_rates"]
latency_p50 = metrics["latency_percentiles"]["p50"]
safety_pass_rate = metrics["safety_invariant_pass_rate"]
```

## Generating Reports

```python
from pathlib import Path
from eval_calibration_core.report import build_report, write_report

report = build_report(packets, suite_name="my_suite")

# Write JSON and Markdown to directory
write_report(report, Path("output"))  # creates output/report.json, output/report.md

# Access report data
print(f"Metrics: {report.metrics}")
print(f"Invariant results: {report.invariant_results}")
print(f"Contract check: {report.contract_matrix_check}")
```

## Invariant Verification

```python
from eval_calibration_core.suites.invariants import check_invariants

results = check_invariants(packets)

for invariant_name, passed in results.items():
    if not passed:
        print(f"Invariant failed: {invariant_name}")
```

## Fail-Closed Behavior

On any error:
- Returns empty metrics dict
- Logs error for debugging
- Does not raise exceptions (fail-closed)
