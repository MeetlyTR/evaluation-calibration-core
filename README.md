<!--
Decision Ecosystem — evaluation-calibration-core
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
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
from pathlib import Path
from eval_calibration_core.io.packet_reader import PacketReader
from eval_calibration_core.metrics.compute import compute_metrics
from eval_calibration_core.report import build_report, write_report

# Read packets
reader = PacketReader("traces.jsonl")
packets = list(reader.read())

# Compute metrics
metrics = compute_metrics(packets)

# Build and write report
report = build_report(packets, suite_name="my_suite")
write_report(report, Path("output"))
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
pip install git+https://github.com/MchtMzffr/evaluation-calibration-core.git
```

## Tests

```bash
pytest tests/
```

## License

[Add your license]
