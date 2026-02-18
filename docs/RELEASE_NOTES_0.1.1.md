<!--
Decision Ecosystem — evaluation-calibration-core
Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
SPDX-License-Identifier: MIT
-->
# Release Notes — evaluation-calibration-core 0.1.1

**Release Date:** 2026-02-17  
**Type:** Patch Release (backward-compatible)

---

## Summary

This patch release documents the percentile calculation method (nearest-rank) for clarity and deterministic behavior understanding.

---

## Changes

### ✅ F6 — Percentile Documentation

**Problem:** `latency_percentiles()` used nearest-rank method but wasn't documented, leading to potential confusion about behavior (especially for small datasets).

**Solution:** Added comprehensive documentation:
- Method explanation: nearest-rank (`idx = floor((k/100) * n)`)
- Small n behavior note: "For small n, p95 and p99 may equal max value (expected behavior)"
- Alternative methods mentioned (linear interpolation)

**Files Changed:**
- `eval_calibration_core/metrics/definitions.py`: Enhanced docstring for `latency_percentiles()`

**Clarity:** Users now understand:
- How percentiles are calculated (deterministic nearest-rank)
- Why small datasets may show p95=p99=max (expected behavior)
- That the method is deterministic and simple

---

## Backward Compatibility

✅ **Fully backward-compatible:**
- No code changes (documentation only)
- No API changes
- Existing behavior unchanged

---

## Migration Guide

**No migration needed.** This is a documentation-only change.

---

## Testing

- ✅ All existing tests pass (19/19)
- ✅ Percentile calculation behavior verified
- ✅ Deterministic behavior confirmed

---

## References

- **Issue:** F6 from static analysis report
- **Method:** Nearest-rank percentile calculation

---

**Upgrade Path:** `pip install "evaluation-calibration-core>=0.1.1,<0.2"`
