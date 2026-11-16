"""Track electricity meter readings and calculate tiered bills."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TIER_RATES = [3.5, 5.0, 7.5]
SPIKE_LIMIT = 500
DEFAULT_DATA_FILE = Path("meters.json")

meters: dict[str, float] = {}
reading_history: list[dict[str, Any]] = []


def record_reading(meter_id: str, units: float) -> dict[str, Any]:
    """Record a nonnegative usage amount for a meter and return the entry."""
    if not meter_id.strip():
        raise ValueError("meter_id must not be empty")
    if isinstance(units, bool) or not isinstance(units, (int, float)):
        raise TypeError("units must be a number")
    if units < 0:
        raise ValueError("units must be nonnegative")

    entry = {
        "meter_id": meter_id,
        "units": float(units),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    reading_history.append(entry)
    meters[meter_id] = meters.get(meter_id, 0.0) + float(units)
    return entry


def compute_bill(
    meter_id: str, tier_rates: tuple[float, float, float] | None = None
) -> float:
    """Calculate progressive energy charges for a known meter."""
    rates = tier_rates or tuple(TIER_RATES)
    if len(rates) != 3 or any(rate < 0 for rate in rates):
        raise ValueError("exactly three nonnegative tier rates are required")
    units = meters[meter_id]
    if units <= 100:
        return units * rates[0]
    if units <= 300:
        return 100 * rates[0] + (units - 100) * rates[1]
    return 100 * rates[0] + 200 * rates[1] + (units - 300) * rates[2]


def raise_rates(percent: float) -> tuple[float, float, float]:
    """Raise all tariff tiers by a nonnegative percentage and return them."""
    if percent < 0:
        raise ValueError("percent must be nonnegative")
    multiplier = 1 + percent / 100
    for index, rate in enumerate(TIER_RATES):
        TIER_RATES[index] = rate * multiplier
    return tuple(TIER_RATES)


def flag_spikes() -> list[str]:
    """Return meter IDs whose accumulated use exceeds the spike limit."""
    return [
        meter_id for meter_id, units in meters.items()
        if units > SPIKE_LIMIT
    ]


def load_meter_data(file: str | Path = DEFAULT_DATA_FILE) -> None:
    """Load meter totals and optional history from a JSON data file."""
    path = Path(file)
    try:
        with path.open("r", encoding="utf-8") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        meters.clear()
        reading_history.clear()
        return
    except (json.JSONDecodeError, OSError) as error:
        message = f"Could not read meter data from {path}: {error}"
        raise ValueError(message) from error

    if isinstance(data, dict) and "meters" in data:
        loaded_meters = data["meters"]
        loaded_history = data.get("history", [])
    elif isinstance(data, dict):
        # Accept the original format of meter_id -> units.
        loaded_meters, loaded_history = data, []
    else:
        raise ValueError("meter data must be a JSON object")
    if not isinstance(loaded_meters, dict) or not isinstance(
        loaded_history, list
    ):
        raise ValueError("meter data has an invalid structure")
    meters.clear()
    meter_totals = {
        str(key): float(value) for key, value in loaded_meters.items()
    }
    meters.update(meter_totals)
    reading_history.clear()
    reading_history.extend(loaded_history)


def save_meter_data(file: str | Path = DEFAULT_DATA_FILE) -> None:
    """Persist meter totals and reading history as valid JSON."""
    path = Path(file)
    payload = {"meters": meters, "history": reading_history}
    try:
        with path.open("w", encoding="utf-8") as data_file:
            json.dump(payload, data_file, indent=2)
            data_file.write("\n")
    except OSError as error:
        message = f"Could not save meter data to {path}: {error}"
        raise ValueError(message) from error


def main() -> None:
    """Run a short interactive demonstration of the meter calculator."""
    load_meter_data()
    record_reading("M-01", 120)
    record_reading("M-02", 640)
    print(f"Readings stored this session: {len(reading_history)}")
    rates = tuple(TIER_RATES)
    for meter_id in ("M-01", "M-02"):
        print(f"Bill {meter_id}: {compute_bill(meter_id, rates):.2f}")
    print("Usage spikes:", flag_spikes())

    adjustment = input("Extra units for M-01 (Enter for 0): ").strip()
    if adjustment:
        try:
            record_reading("M-01", float(adjustment))
        except (TypeError, ValueError) as error:
            print(f"Invalid reading: {error}")
            return
    save_meter_data()
    print(f"Bill M-01 after save: {compute_bill('M-01', rates):.2f}")


if __name__ == "__main__":
    main()
