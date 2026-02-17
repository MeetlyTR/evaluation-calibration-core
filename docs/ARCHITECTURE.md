# Architecture — evaluation-calibration-core

## Role in the ecosystem

evaluation-calibration-core generates **evidence artifacts** from `PacketV2` traces.

## Data flow

```
PacketV2 traces -> read_packets() -> compute_metrics() -> build_report() -> Report
```

## Metrics computation

Metrics are computed from `PacketV2` traces:
- Action distribution
- Guard trigger rates
- Latency percentiles
- Invariant pass rates

## Invariant checks

Mathematical guarantee checks:
- Contract closure: Proposal.action and FinalDecision.action must be in Action enum
- Confidence clamp: Proposal.confidence must be within [0,1]
- Fail-closed: If mismatch contains deny flags => allowed must be False
- Packet version: PacketV2.schema_version must be present

## Contracts

- Input: `PacketV2` traces (from JSONL files)
- Output: Metrics dict, Report (JSON + Markdown)
- Uses `decision_schema.packet_v2.PacketV2` for trace reading

## Components

### 1. Packet Reader (`eval_calibration_core/io/packet_reader.py`)

**Class**: `PacketReader`

- Reads `PacketV2` from JSONL files
- Validates schema compatibility

### 2. Metrics Computation (`eval_calibration_core/metrics/compute.py`)

**Function**: `compute_metrics(packets: Iterable[PacketV2]) -> dict`

- Computes action distribution
- Computes guard trigger rates
- Computes latency percentiles
- Verifies invariants

### 3. Report Generation (`eval_calibration_core/report.py`)

**Function**: `build_report(packets: Iterable[PacketV2]) -> Report`

- Generates JSON report
- Generates Markdown report
- Includes metrics and invariant checks

## Safety invariants

- **Fail-closed**: On errors, return empty metrics or safe defaults
- **Deterministic**: Same inputs → same outputs
- **Schema validation**: Reject incompatible PacketV2 versions
