# engine/_util.py
# Owner: M2
# Purpose: tiny helpers shared by the M2 modules.
import math
from datetime import datetime, timezone
from typing import Any, Iterator, Optional


def get(obj: Any, key: str, default: Any = None) -> Any:
    """Read a field from a dict OR from an object (Pydantic model / dataclass).
    M1's ActionEvent is a Pydantic model, tests use plain dicts. This lets both work."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def parse_ts(value: Any) -> datetime:
    """ISO-8601 UTC string (or datetime) -> aware datetime. Raises ValueError if bad.
    A bad timestamp becomes an exception, and the enforcer's fail-closed wrapper turns it into BLOCK."""
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if not isinstance(value, str):
        raise ValueError(f"bad timestamp: {value!r}")
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def seconds_between(later: datetime, earlier: datetime) -> float:
    return (later - earlier).total_seconds()


def to_amount(value: Any) -> Optional[float]:
    """Turn an 'amount' argument into a safe number, or None if it is not a real finite number.
    LLM agents sometimes send '9000' as text; we accept that. NaN and infinity are rejected,
    because NaN > limit is False and would silently slip past a limit check."""
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def walk_strings(obj: Any) -> Iterator[str]:
    """Yield every string found anywhere inside nested dicts / lists / tuples
    (keys too, because a bait id could hide in a key)."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(k)
            yield from walk_strings(v)
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            yield from walk_strings(item)
    elif obj is not None and not isinstance(obj, (int, float, bool)):
        yield str(obj)


def history_in_window(history, now: datetime, window_seconds: float):
    """Yield (entry, timestamp) for history entries inside the last window_seconds."""
    for h in history or ():
        try:
            ts = parse_ts(get(h, "ts"))
        except ValueError:
            continue  # an unreadable old record should not crash the live decision
        age = seconds_between(now, ts)
        if -5 <= age <= window_seconds:   # small negative allowed for clock jitter
            yield h, ts
