#!/usr/bin/env python3
"""
MCP Time Server - Provides simple time and date utilities via MCP protocol.
Uses only standard library for cross-platform compatibility.
"""

from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo, available_timezones
from typing import Optional
import time

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("time-server")


@mcp.tool()
def get_current_time(tz: Optional[str] = None) -> dict:
    """
    Get the current date and time.

    Args:
        tz: Optional timezone name (e.g., 'America/New_York', 'UTC').
            If not provided, returns local time.

    Returns:
        Dictionary containing formatted time information
    """
    try:
        if tz:
            # Validate timezone
            if tz not in available_timezones():
                return {
                    "error": f"Invalid timezone: {tz}",
                    "available_timezones_sample": sorted(list(available_timezones()))[:10]
                }

            now = datetime.now(ZoneInfo(tz))
            tz_info = tz
        else:
            now = datetime.now()
            tz_info = "local"

        return {
            "datetime": now.isoformat(),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "time_12h": now.strftime("%I:%M:%S %p"),
            "timezone": tz_info,
            "timezone_offset": now.strftime("%z"),
            "day_of_week": now.strftime("%A"),
            "unix_timestamp": int(now.timestamp()),
            "formatted": now.strftime("%A, %B %d, %Y at %I:%M:%S %p")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_timezone_info(tz: str) -> dict:
    """
    Get information about a specific timezone.

    Args:
        tz: Timezone name (e.g., 'America/New_York', 'Europe/London')

    Returns:
        Dictionary containing timezone information
    """
    try:
        if tz not in available_timezones():
            return {
                "error": f"Invalid timezone: {tz}",
                "hint": "Use list_timezones to see available options"
            }

        zone = ZoneInfo(tz)
        now = datetime.now(zone)

        return {
            "timezone": tz,
            "current_time": now.isoformat(),
            "offset": now.strftime("%z"),
            "offset_hours": now.utcoffset().total_seconds() / 3600 if now.utcoffset() else 0,
            "abbreviation": now.strftime("%Z")
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def list_timezones(filter_text: Optional[str] = None) -> dict:
    """
    List available timezones, optionally filtered by text.

    Args:
        filter_text: Optional text to filter timezone names (case-insensitive)

    Returns:
        Dictionary containing list of timezone names
    """
    try:
        zones = sorted(list(available_timezones()))

        if filter_text:
            filter_lower = filter_text.lower()
            zones = [z for z in zones if filter_lower in z.lower()]

        return {
            "count": len(zones),
            "timezones": zones
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def parse_datetime(
    date_string: str,
    format_string: str = "%Y-%m-%d %H:%M:%S"
) -> dict:
    """
    Parse a date/time string and return detailed information.

    Args:
        date_string: The date/time string to parse
        format_string: The format of the input string (default: "%Y-%m-%d %H:%M:%S")
                      Common formats:
                      - "%Y-%m-%d %H:%M:%S" : 2025-01-21 14:30:00
                      - "%Y-%m-%d" : 2025-01-21
                      - "%m/%d/%Y" : 01/21/2025
                      - "%d/%m/%Y %H:%M" : 21/01/2025 14:30

    Returns:
        Dictionary containing parsed datetime information
    """
    try:
        dt = datetime.strptime(date_string, format_string)

        return {
            "original": date_string,
            "parsed": dt.isoformat(),
            "date": dt.strftime("%Y-%m-%d"),
            "time": dt.strftime("%H:%M:%S"),
            "day_of_week": dt.strftime("%A"),
            "unix_timestamp": int(dt.timestamp()),
            "is_past": dt < datetime.now(),
            "is_future": dt > datetime.now()
        }
    except ValueError as e:
        return {
            "error": f"Failed to parse date: {str(e)}",
            "hint": "Check that your date_string matches the format_string"
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def compare_times(
    time1: str,
    time2: str,
    format_string: str = "%Y-%m-%d %H:%M:%S"
) -> dict:
    """
    Compare two datetime strings and return the difference.

    Args:
        time1: First datetime string
        time2: Second datetime string
        format_string: The format both strings use (default: "%Y-%m-%d %H:%M:%S")

    Returns:
        Dictionary containing comparison information
    """
    try:
        dt1 = datetime.strptime(time1, format_string)
        dt2 = datetime.strptime(time2, format_string)

        diff = dt2 - dt1
        abs_diff = abs(diff)

        days = abs_diff.days
        hours, remainder = divmod(abs_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return {
            "time1": dt1.isoformat(),
            "time2": dt2.isoformat(),
            "difference_seconds": diff.total_seconds(),
            "difference_days": diff.days,
            "difference_formatted": {
                "days": days,
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds
            },
            "time1_is_before_time2": dt1 < dt2,
            "time1_is_after_time2": dt1 > dt2,
            "times_are_equal": dt1 == dt2
        }
    except ValueError as e:
        return {
            "error": f"Failed to parse dates: {str(e)}",
            "hint": "Check that both time strings match the format_string"
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def add_time_delta(
    base_time: str,
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
    format_string: str = "%Y-%m-%d %H:%M:%S"
) -> dict:
    """
    Add or subtract time from a given datetime.
    Use negative values to subtract time.

    Args:
        base_time: The starting datetime string
        days: Number of days to add (can be negative)
        hours: Number of hours to add (can be negative)
        minutes: Number of minutes to add (can be negative)
        seconds: Number of seconds to add (can be negative)
        format_string: The format of the base_time string

    Returns:
        Dictionary containing the new datetime
    """
    try:
        dt = datetime.strptime(base_time, format_string)
        delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        new_dt = dt + delta

        return {
            "original": dt.isoformat(),
            "delta_applied": {
                "days": days,
                "hours": hours,
                "minutes": minutes,
                "seconds": seconds
            },
            "result": new_dt.isoformat(),
            "formatted": new_dt.strftime("%A, %B %d, %Y at %I:%M:%S %p"),
            "unix_timestamp": int(new_dt.timestamp())
        }
    except ValueError as e:
        return {
            "error": f"Failed to parse date: {str(e)}",
            "hint": "Check that your base_time matches the format_string"
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def is_valid_datetime(
    date_string: str,
    format_string: str = "%Y-%m-%d %H:%M:%S"
) -> dict:
    """
    Check if a string is a valid datetime in the specified format.

    Args:
        date_string: The date/time string to validate
        format_string: The expected format

    Returns:
        Dictionary indicating whether the datetime is valid
    """
    try:
        dt = datetime.strptime(date_string, format_string)
        return {
            "valid": True,
            "parsed": dt.isoformat(),
            "message": "Successfully parsed datetime"
        }
    except ValueError as e:
        return {
            "valid": False,
            "error": str(e),
            "message": "Failed to parse datetime with given format"
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }


@mcp.tool()
def unix_to_datetime(
    timestamp: int,
    tz: Optional[str] = None
) -> dict:
    """
    Convert a Unix timestamp to a datetime.

    Args:
        timestamp: Unix timestamp (seconds since epoch)
        tz: Optional timezone name for the output

    Returns:
        Dictionary containing formatted datetime information
    """
    try:
        if tz:
            if tz not in available_timezones():
                return {
                    "error": f"Invalid timezone: {tz}",
                    "hint": "Use list_timezones to see available options"
                }
            dt = datetime.fromtimestamp(timestamp, ZoneInfo(tz))
        else:
            dt = datetime.fromtimestamp(timestamp)

        return {
            "unix_timestamp": timestamp,
            "datetime": dt.isoformat(),
            "date": dt.strftime("%Y-%m-%d"),
            "time": dt.strftime("%H:%M:%S"),
            "formatted": dt.strftime("%A, %B %d, %Y at %I:%M:%S %p"),
            "timezone": tz if tz else "local"
        }
    except (ValueError, OSError) as e:
        return {
            "error": f"Invalid timestamp: {str(e)}",
            "hint": "Timestamp should be a valid Unix timestamp in seconds"
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Run the server
    mcp.run()
