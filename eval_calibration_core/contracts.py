"""Contract compatibility checks."""

from decision_schema import __version__ as schema_version
from decision_schema.compat import is_compatible


def check_schema_compatibility(expected_minor: int = 1) -> None:
    """
    Check if decision-schema version is compatible.
    
    Args:
        expected_minor: Expected minor version (default: 1 for 0.1.x)
    
    Raises:
        RuntimeError: If schema version is incompatible
    """
    if not is_compatible(schema_version, expected_major=0, min_minor=expected_minor, max_minor=expected_minor):
        raise RuntimeError(
            f"decision-schema version {schema_version} is incompatible. "
            f"Expected 0.{expected_minor}.x"
        )


def get_schema_version() -> str:
    """Get current decision-schema version."""
    return schema_version


def check_expected_minor_range(expected_major: int = 0, min_minor: int = 1, max_minor: int = 1) -> tuple[bool, dict[str, any]]:
    """
    Check if schema version is within expected minor range.
    
    Args:
        expected_major: Expected major version (default: 0)
        min_minor: Minimum minor version (default: 1)
        max_minor: Maximum minor version (default: 1)
    
    Returns:
        Tuple of (ok: bool, details: dict)
    """
    ok = is_compatible(schema_version, expected_major=expected_major, min_minor=min_minor, max_minor=max_minor)
    details = {
        "schema_version": schema_version,
        "expected_major": expected_major,
        "min_minor": min_minor,
        "max_minor": max_minor,
        "compatible": ok,
    }
    return ok, details
