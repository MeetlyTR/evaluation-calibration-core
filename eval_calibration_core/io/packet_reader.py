"""Read PacketV2 from JSONL files."""

from pathlib import Path
from typing import Iterator

from decision_schema.packet_v2 import PacketV2


class PacketReader:
    """Read PacketV2 packets from JSONL file."""

    def __init__(self, path: Path | str):
        """
        Initialize reader.
        
        Args:
            path: Path to JSONL file containing PacketV2 dicts
        """
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"Packet file not found: {self.path}")

    def read(self) -> Iterator[PacketV2]:
        """
        Read packets from JSONL file.
        
        Yields:
            PacketV2 instances
        
        Raises:
            ValueError: If packet format is invalid
        """
        import json

        with open(self.path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    packet = PacketV2.from_dict(data)
                    yield packet
                except (json.JSONDecodeError, ValueError, KeyError) as e:
                    raise ValueError(f"Invalid packet at line {line_num}: {e}") from e

    def read_all(self) -> list[PacketV2]:
        """
        Read all packets into a list.
        
        Returns:
            List of PacketV2 instances
        """
        return list(self.read())
