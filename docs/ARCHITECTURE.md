# Evaluation & Calibration Core Architecture

## Purpose

**Evaluation & Calibration Core** evaluates decision pipelines via PacketV2 traces. It provides metrics computation, invariant checks, report generation, and optional policy calibration.

## Data Flow

```
PacketV2 JSONL → PacketReader → Metrics Computation → Invariant Checks → Report (JSON + MD)
```

## Components

### 1. Packet Reader (`eval_calibration_core/io/packet_reader.py`)

**Function**: `PacketReader.read_all() -> list[PacketV2]`

- Reads PacketV2 objects from JSONL files
- Validates packet structure
- Handles missing/invalid packets gracefully

### 2. Fixture Suites (`eval_calibration_core/io/fixtures.py`)

**Function**: `load_fixture_suite(name: str) -> list[PacketV2]`

Provides synthetic test suites:
- `smoke`: Minimal valid packets
- `determinism`: Deterministic scenarios
- `guard_pressure`: Scenarios that trigger guards

### 3. Metrics Computation (`eval_calibration_core/metrics/`)

**Function**: `compute_metrics(packets: list[PacketV2]) -> dict`

Computes:
- **Action distribution**: Count and rates of actions
- **Guard trigger rate**: Rate at which guards trigger per reason code
- **Safety invariant pass rate**: Rate at which safety invariants pass
- **Latency percentiles**: p50, p95, p99 latency statistics

### 4. Invariant Checks (`eval_calibration_core/suites/invariants.py`)

**Function**: `check_invariants(packets: list[PacketV2]) -> dict[str, bool]`

Checks:
- **Contract closure**: `allowed=True` implies constraints met
- **Confidence clamp**: `confidence ∈ [0.0, 1.0]`
- **Fail-closed**: Guard failures result in safe actions
- **Packet version**: Packet structure matches expected version

### 5. Report Generation (`eval_calibration_core/report/`)

**Function**: `write_report(report: Report, output_dir: Path)`

- Generates JSON report (`report.json`)
- Generates Markdown report (`report.md`)
- Includes contract matrix compatibility check

### 6. Contract Compatibility (`eval_calibration_core/contracts.py`)

**Functions**:
- `check_schema_compatibility()`: Verify schema version compatibility
- `check_expected_minor_range()`: Check minor version range
- `get_schema_version()`: Get current schema version

## Integration Points

### Input: PacketV2 Traces

Evaluation core consumes PacketV2 traces (from `decision-schema`):
- Can read from JSONL files
- Can use synthetic fixture suites
- No domain-specific assumptions

### Output: Reports

Reports include:
- Metrics (action distribution, guard triggers, latency)
- Invariant results (pass/fail)
- Contract matrix check (schema compatibility)

### Optional Plugins

- **MDM plugin**: Replay MDM proposals (optional)
- **DMC plugin**: Replay DMC modulation (optional)

## Design Principles

1. **Contract-first**: Only depends on `decision-schema`
2. **Offline**: No network calls, all tests run offline
3. **Domain-agnostic**: No trading/exchange-specific terms
4. **Deterministic**: Same packets → same metrics
5. **Extensible**: Plugin system for MDM/DMC replay

## Non-Goals

- **Not a runtime system**: Does not execute decisions
- **Not domain-specific**: No trading/exchange logic
- **Not a test framework**: Focuses on metrics/invariants, not unit tests
