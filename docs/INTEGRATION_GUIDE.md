# Integration Guide — evaluation-calibration-core

## Dependency

Pin schema version:
```toml
dependencies = ["decision-schema>=0.1,<0.2"]
```

## Basic Usage

```python
from eval_calibration_core.io.packet_reader import PacketReader
from eval_calibration_core.metrics.compute import compute_metrics
from eval_calibration_core.report import build_report

# Read packets from JSONL file
reader = PacketReader("traces.jsonl")
packets = list(reader.read())

# Compute metrics
metrics = compute_metrics(packets)

print(f"Action distribution: {metrics['action_distribution']}")
print(f"Guard trigger rates: {metrics['guard_trigger_rates']}")
print(f"Latency percentiles: {metrics['latency_percentiles']}")
print(f"Invariant pass rate: {metrics['invariant_pass_rate']}")

# Generate report
report = build_report(packets)
report.save_json("report.json")
report.save_markdown("report.md")
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
inv_pass_rate = metrics["invariant_pass_rate"]
```

## Generating Reports

```python
from eval_calibration_core.report import build_report

report = build_report(packets)

# Save as JSON
report.save_json("report.json")

# Save as Markdown
report.save_markdown("report.md")

# Access report data
print(f"Total packets: {report.total_packets}")
print(f"Metrics: {report.metrics}")
print(f"Invariant checks: {report.invariant_checks}")
```

## Invariant Verification

```python
from eval_calibration_core.invariants import verify_invariants

results = verify_invariants(packets)

for invariant_name, passed in results.items():
    if not passed:
        print(f"Invariant failed: {invariant_name}")
```

## Fail-Closed Behavior

On any error:
- Returns empty metrics dict
- Logs error for debugging
- Does not raise exceptions (fail-closed)
