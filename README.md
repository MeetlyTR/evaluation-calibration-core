# evaluation-calibration-core (Evidence, Metrics, Reports)

This core generates evidence artifacts from `PacketV2` traces:
- metrics
- invariant checks
- calibration and drift summaries

Domain-agnostic; depends only on `decision-schema`.

## Responsibilities

- Read `PacketV2` traces from JSONL files
- Compute metrics (action distribution, guard trigger rates, latency percentiles)
- Verify invariants (contract closure, confidence clamp, fail-closed)
- Generate reports (JSON + Markdown)

## Integration

```python
from eval_calibration_core.io.packet_reader import PacketReader
from eval_calibration_core.metrics.compute import compute_metrics
from eval_calibration_core.report import build_report

# Read packets
reader = PacketReader("traces.jsonl")
packets = list(reader.read())

# Compute metrics
metrics = compute_metrics(packets)

# Generate report
report = build_report(packets)
report.save_json("report.json")
report.save_markdown("report.md")
```

## Documentation

- `docs/ARCHITECTURE.md`: System architecture
- `docs/FORMULAS.md`: Metric definitions and formulas
- `docs/INTEGRATION_GUIDE.md`: Integration examples

## Installation

```bash
pip install -e .
```

Or from git:
```bash
pip install git+https://github.com/MeetlyTR/evaluation-calibration-core.git
```

## Tests

```bash
pytest tests/
```

## License

[Add your license]
