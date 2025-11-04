#!/usr/bin/env python3
"""
cleaned_inventory_system.py
A safer, more testable inventory system with static-analysis friendly patterns.
"""

from __future__ import annotations
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Configure module logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
if not logger.handlers:
    logger.addHandler(handler)

# Use a single global inventory dictionary
_stock_data: Dict[str, int] = {}


def _now_str() -> str:
    return datetime.now().isoformat()


def add_item(item: str, qty: int, logs: Optional[List[str]] = None) -> None:
    """
    Add quantity for an item. Validate types and initialize logs safely.
    """
    if logs is None:
        logs = []

    if not isinstance(item, str) or not item:
        raise ValueError("item must be a non-empty string")

    if not isinstance(qty, int):
        raise ValueError("qty must be an integer")

    current = _stock_data.get(item, 0)
    new_qty = current + qty
    if new_qty <= 0:
        # If quantity zero or negative, remove item
        _stock_data.pop(item, None)
    else:
        _stock_data[item] = new_qty

    logs.append(f"{_now_str()}: Added {qty} of {item}")
    logger.info("Added %d of %s (new qty: %s)", qty, item, _stock_data.get(item))


def remove_item(item: str, qty: int) -> None:
    """
    Remove qty from item. Raises KeyError if item missing, ValueError on bad qty.
    """
    if not isinstance(item, str) or not item:
        raise ValueError("item must be a non-empty string")
    if not isinstance(qty, int) or qty <= 0:
        raise ValueError("qty to remove must be a positive integer")

    if item not in _stock_data:
        raise KeyError(f"Item '{item}' not found in inventory")

    if _stock_data[item] <= qty:
        # delete if resulting qty <= 0
        _stock_data.pop(item, None)
        logger.info("Removed %d of %s — item deleted", qty, item)
    else:
        _stock_data[item] -= qty
        logger.info("Removed %d of %s (remaining: %d)", qty, item, _stock_data[item])


def get_qty(item: str) -> int:
    """
    Return quantity (0 if missing). Validate input.
    """
    if not isinstance(item, str) or not item:
        raise ValueError("item must be a non-empty string")
    return _stock_data.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """
    Load inventory from JSON file. Gracefully handle missing or corrupted files.
    """
    try:
        with open(file, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError("inventory file must contain a JSON object")
        # Ensure keys are strings and values are ints
        cleaned: Dict[str, int] = {}
        for k, v in data.items():
            if not isinstance(k, str):
                logger.warning("Skipping non-string key in file: %s", k)
                continue
            try:
                vi = int(v)
            except (TypeError, ValueError):
                logger.warning("Skipping key with non-int value: %s -> %s", k, v)
                continue
            if vi > 0:
                cleaned[k] = vi
        global _stock_data
        _stock_data = cleaned
        logger.info("Loaded %d items from %s", len(_stock_data), file)
    except FileNotFoundError:
        logger.warning("%s not found; starting with empty inventory", file)
    except json.JSONDecodeError:
        logger.error("Failed to decode JSON from %s; starting with empty inventory", file)
    except Exception:
        logger.exception("Unexpected error loading data from %s", file)


def save_data(file: str = "inventory.json") -> None:
    """
    Save inventory to JSON file. Uses an atomic write pattern (write temporary then rename).
    """
    try:
        tmp_file = f"{file}.tmp"
        with open(tmp_file, "w", encoding="utf-8") as fh:
            json.dump(_stock_data, fh, indent=2)
        # Atomic replace
        import os
        os.replace(tmp_file, file)
        logger.info("Saved %d items to %s", len(_stock_data), file)
    except Exception:
        logger.exception("Failed to save inventory to %s", file)


def print_data() -> None:
    """
    Print a human-readable report of inventory.
    """
    print("Items Report")
    for name, qty in sorted(_stock_data.items()):
        print(f"{name} -> {qty}")


def check_low_items(threshold: int = 5) -> List[str]:
    if not isinstance(threshold, int) or threshold < 0:
        raise ValueError("threshold must be a non-negative integer")
    return [name for name, qty in _stock_data.items() if qty < threshold]


def main() -> None:
    """
    Example run: populates some items and demonstrates basic operations.
    """
    # configure root logger only if script executed directly
    if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO)
    try:
        # Seed some items (example)
        add_item("apple", 10)
        add_item("banana", 2)
        try:
            add_item("orange", -1)  # negative results in deletion / ignored
        except ValueError as exc:
            logger.warning("Bad add_item call: %s", exc)

        remove_item("apple", 3)

        print("Apple stock:", get_qty("apple"))
        print("Low items:", check_low_items())
        save_data()
        # Demonstrate load (safe)
        load_data()
        print_data()
    except Exception:
        logger.exception("Unexpected error in main()")


if __name__ == "__main__":
    main()
