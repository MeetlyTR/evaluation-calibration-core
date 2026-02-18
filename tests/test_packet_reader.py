# Decision Ecosystem — evaluation-calibration-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Tests for PacketReader."""

import json
import tempfile
from pathlib import Path

import pytest

from decision_schema.packet_v2 import PacketV2
from eval_calibration_core.io.packet_reader import PacketReader


def test_packet_reader_reads_valid_jsonl() -> None:
    """Verify PacketReader reads valid JSONL."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        # Write valid packets
        for step in range(5):
            packet = PacketV2(
                run_id="test-run",
                step=step,
                input={"ts": 1000 + step},
                external={"mid": 0.5},
                mdm={"action": "HOLD"},
                final_action={"action": "HOLD"},
                latency_ms=2,
            )
            f.write(json.dumps(packet.to_dict()) + "\n")
        temp_path = Path(f.name)

    try:
        reader = PacketReader(temp_path)
        packets = reader.read_all()
        assert len(packets) == 5
        assert all(isinstance(p, PacketV2) for p in packets)
    finally:
        temp_path.unlink()


def test_packet_reader_handles_invalid_json() -> None:
    """Verify PacketReader handles invalid JSON."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write("invalid json\n")
        temp_path = Path(f.name)

    try:
        reader = PacketReader(temp_path)
        with pytest.raises(ValueError, match="Invalid packet"):
            list(reader.read())
    finally:
        temp_path.unlink()


def test_packet_reader_handles_missing_file() -> None:
    """Verify PacketReader handles missing file."""
    with pytest.raises(FileNotFoundError):
        PacketReader(Path("nonexistent.jsonl"))
