# Evaluation & Calibration Core Formulas

## Metrics Formulas

### Action Distribution

```
count(action) = number of packets with final_action.action == action
rate(action) = count(action) / total_packets
```

### Guard Trigger Rate

```
triggers(code) = number of packets with mismatch.reason_codes containing code
trigger_rate(code) = triggers(code) / total_packets
```

### Safety Invariant Pass Rate

```
passed_checks = sum(1 for packet in packets if invariant_passes(packet))
pass_rate = passed_checks / total_packets
```

### Latency Percentiles

```
latencies = [packet.latency_ms for packet in packets]
p50 = percentile(latencies, 50)
p95 = percentile(latencies, 95)
p99 = percentile(latencies, 99)
```

## Invariant Formulas

### Contract Closure

```
invariant_passes = True if:
  - final_action.allowed == True implies constraints_met(context)
  - final_action.allowed == False implies constraints_not_met(context)
```

### Confidence Clamp

```
invariant_passes = True if:
  - proposal.confidence >= 0.0 AND proposal.confidence <= 1.0
```

### Fail-Closed

```
invariant_passes = True if:
  - mismatch.flags non-empty implies final_action.action is safe (HOLD/STOP)
```

### Packet Version

```
invariant_passes = True if:
  - packet.packet_version == "2"
  - packet.schema_version matches expected schema version
```

## Contract Matrix Check

### Schema Compatibility

```
ok = is_compatible(schema_version, expected_major=0, min_minor=1, max_minor=1)
```

Where:
- `schema_version`: Current decision-schema version (e.g., "0.1.0")
- `expected_major`: Expected major version (0 for 0.x)
- `min_minor`: Minimum minor version (inclusive)
- `max_minor`: Maximum minor version (inclusive)

**Compatibility rules**:
- For 0.x: compatible if major matches AND minor is within [min_minor, max_minor]
- For 1.x+: compatible if major matches (minor/patch are backward compatible)

## Calibration (Future)

### Grid Search Objective

```
objective = w1 * invariant_pass_rate + w2 * (1 - deny_rate) - w3 * latency_p95
```

Where:
- `invariant_pass_rate`: Rate at which invariants pass
- `deny_rate`: Rate at which actions are denied
- `latency_p95`: 95th percentile latency

Grid search optimizes policy thresholds to maximize objective while maintaining safety.
