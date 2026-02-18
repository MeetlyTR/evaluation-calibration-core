<!--
Decision Ecosystem — evaluation-calibration-core
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Formulas — evaluation-calibration-core

**Implemented metrics (this core):** action distribution, guard trigger rate, safety invariant pass rate, latency percentiles, confidence statistics. General outcome notation (R_T, R̄, σ, DD, MDD, SR) is defined in `decision-ecosystem-docs/FORMULAS.md` as optional/generic; this core does not compute outcome sums or means.

## Action Distribution

```
action_count(action) = count(packets where final_action.action == action)
action_rate(action) = action_count(action) / total_packets
```

## Guard Trigger Rate

```
trigger_rate(code) = triggers(code) / total_steps
```

Where `triggers(code)` is the count of packets where `mismatch.reason_codes` contains `code`.

## Safety Invariant Pass Rate

```
inv_pass = passed_checks / total_checks
```

Where `passed_checks` is the count of invariant checks that passed.

## Latency Percentiles

```
p50_latency = percentile(latency_samples, 50)
p95_latency = percentile(latency_samples, 95)
p99_latency = percentile(latency_samples, 99)
```

Where `latency_samples` are extracted from `PacketV2.latency_ms`.

## Confidence Statistics

```
mean_confidence = mean(proposal.confidence for all packets)
std_confidence = std(proposal.confidence for all packets)
min_confidence = min(proposal.confidence for all packets)
max_confidence = max(proposal.confidence for all packets)
```

## Invariant Formulas

### Contract Closure
```
pass = (proposal.action in Action enum) AND (final_action.action in Action enum)
```

### Confidence Clamp
```
pass = (0 <= proposal.confidence <= 1)
```

### Fail-Closed
```
pass = (mismatch.flags => final_action.allowed == False)
```

### Packet Version
```
pass = (packet.schema_version is present)
```

## Invariants

- **Fail-closed**: On errors, return empty metrics or safe defaults
- **Deterministic**: Same inputs → same outputs
- **Schema validation**: Reject incompatible PacketV2 versions
