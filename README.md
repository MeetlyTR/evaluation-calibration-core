# Evaluation & Calibration Core

**Evaluation & Calibration Core** evaluates decision pipelines via the shared `decision-schema` contract. It replays scenarios, computes metrics, produces reports, and optionally calibrates policy thresholds.

## Purpose

This core provides:
- **Scenario replay**: Replay PacketV2 traces or synthetic fixtures
- **Metrics computation**: Action distribution, guard trigger rates, safety invariants, latency percentiles
- **Report generation**: JSON + Markdown reports
- **Invariant checks**: Mathematical guarantee checks (contract closure, confidence clamp, fail-closed)
- **Optional calibration**: Safe grid-search over policy thresholds

## Installation

```bash
pip install evaluation-calibration-core
```

Or from source:
```bash
pip install -e .
```

## Quick Start

### Run Evaluation Suite

```bash
# Use built-in fixture suite
python -m eval_calibration_core.cli run --suite smoke --out reports/smoke

# Use custom JSONL file
python -m eval_calibration_core.cli run --in traces.jsonl --out reports/custom
```

### Generate Report

```bash
python -m eval_calibration_core.cli report --out reports/latest
```

## Dependencies

**Required**:
- `decision-schema>=0.1,<0.2` (contract dependency)

**Optional**:
- `[mdm]`: MDM engine plugin support
- `[dmc]`: DMC plugin support
- `[cli]`: Rich CLI formatting (`rich>=13.0`)

## Architecture

- **Contract-first**: Only depends on `decision-schema`
- **Plugin-based**: MDM/DMC are optional plugins
- **Offline**: No network calls, all tests run offline
- **Domain-agnostic**: No trading/exchange-specific terms

## Metrics

### Action Distribution
Count and rates of actions in final decisions.

### Guard Trigger Rate
Rate at which guards trigger per reason code:
```
trigger_rate(code) = triggers(code) / total_steps
```

### Safety Invariant Pass Rate
Rate at which safety invariants pass:
```
inv_pass = passed_checks / total_checks
```

### Latency Percentiles
p50, p95, p99 latency from PacketV2.latency_ms.

## Invariants

Mathematical guarantee checks:

1. **Contract Closure**: Proposal.action and FinalDecision.action must be in Action enum
2. **Confidence Clamp**: Proposal.confidence must be within [0,1]
3. **Fail-Closed**: If mismatch contains deny flags => allowed must be False
4. **Packet Version**: PacketV2.schema_version must be present

## Test Suites

- **smoke**: Minimal smoke test (10 packets)
- **determinism**: Determinism test (20 packets)
- **guard_pressure**: Guard trigger test (20 packets with guard triggers)

## Documentation

- `docs/ARCHITECTURE.md`: System architecture
- `docs/METRICS_AND_FORMULAS.md`: Metric definitions and formulas
- `docs/INVARIANTS.md`: Invariant specifications
- `docs/PUBLIC_RELEASE_GUIDE.md`: Public release checklist

## License

[Add your license]
