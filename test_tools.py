#!/usr/bin/env python3
"""
Simple test script to verify time tools work correctly
Run with: python test_tools.py
"""

from datetime import datetime
from server import (
    get_current_time,
    get_timezone_info,
    list_timezones,
    parse_datetime,
    compare_times,
    add_time_delta,
    is_valid_datetime,
    unix_to_datetime,
)


def test_get_current_time():
    print("Testing get_current_time...")
    result = get_current_time()
    assert "datetime" in result
    assert "timezone" in result
    print(f"  ✓ Local time: {result['formatted']}")

    result = get_current_time(tz="UTC")
    assert "datetime" in result
    assert result["timezone"] == "UTC"
    print(f"  ✓ UTC time: {result['formatted']}")
    print()


def test_timezone_info():
    print("Testing get_timezone_info...")
    result = get_timezone_info("America/New_York")
    assert "timezone" in result
    assert "offset" in result
    print(f"  ✓ NY timezone: {result['timezone']}, offset: {result['offset']}")
    print()


def test_list_timezones():
    print("Testing list_timezones...")
    result = list_timezones(filter_text="America")
    assert "timezones" in result
    assert result["count"] > 0
    print(f"  ✓ Found {result['count']} America/* timezones")
    print()


def test_parse_datetime():
    print("Testing parse_datetime...")
    result = parse_datetime("2025-11-21 14:30:00")
    assert result["date"] == "2025-11-21"
    assert result["time"] == "14:30:00"
    print(f"  ✓ Parsed: {result['day_of_week']}, {result['date']} {result['time']}")
    print()


def test_compare_times():
    print("Testing compare_times...")
    result = compare_times(
        "2025-01-01 00:00:00",
        "2025-12-31 23:59:59"
    )
    assert result["time1_is_before_time2"] is True
    assert result["difference_days"] == 364
    print(f"  ✓ Difference: {result['difference_days']} days")
    print()


def test_add_time_delta():
    print("Testing add_time_delta...")
    result = add_time_delta(
        "2025-01-01 00:00:00",
        days=10,
        hours=5
    )
    assert "result" in result
    print(f"  ✓ After adding 10 days + 5 hours: {result['formatted']}")
    print()


def test_is_valid_datetime():
    print("Testing is_valid_datetime...")
    result = is_valid_datetime("2025-11-21 14:30:00")
    assert result["valid"] is True
    print(f"  ✓ Valid datetime recognized")

    result = is_valid_datetime("not a date")
    assert result["valid"] is False
    print(f"  ✓ Invalid datetime rejected")
    print()


def test_unix_to_datetime():
    print("Testing unix_to_datetime...")
    result = unix_to_datetime(1732204800)
    assert "datetime" in result
    print(f"  ✓ Unix 1732204800 = {result['formatted']}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Testing MCP Time Server Tools")
    print("=" * 60)
    print()

    try:
        test_get_current_time()
        test_timezone_info()
        test_list_timezones()
        test_parse_datetime()
        test_compare_times()
        test_add_time_delta()
        test_is_valid_datetime()
        test_unix_to_datetime()

        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        exit(1)
