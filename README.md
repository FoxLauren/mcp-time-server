# MCP Time Server

A lightweight, cross-platform MCP (Model Context Protocol) server that provides simple time and date utilities using only Python's standard library.

## Features

- **Get current time** in any timezone
- **Parse and validate** datetime strings
- **Compare times** and calculate differences
- **Add/subtract time** from dates
- **Convert Unix timestamps** to readable dates
- **List and query timezones**
- Cross-platform (Windows, macOS, Linux)
- Zero external dependencies (except FastMCP)
- Compilable to standalone executables

## Available Tools

### `get_current_time(tz: Optional[str])`
Get the current date and time, optionally in a specific timezone.

### `get_timezone_info(tz: str)`
Get detailed information about a timezone including current time and offset.

### `list_timezones(filter_text: Optional[str])`
List all available timezones, optionally filtered by text.

### `parse_datetime(date_string: str, format_string: str)`
Parse a datetime string and return detailed information.

### `compare_times(time1: str, time2: str, format_string: str)`
Compare two datetime strings and calculate the difference.

### `add_time_delta(base_time: str, days: int, hours: int, minutes: int, seconds: int, format_string: str)`
Add or subtract time from a given datetime.

### `is_valid_datetime(date_string: str, format_string: str)`
Validate whether a string matches a datetime format.

### `unix_to_datetime(timestamp: int, tz: Optional[str])`
Convert a Unix timestamp to a readable datetime.

## Installation

### Option 1: Download Pre-built Executables (Recommended)

Download the latest release for your platform from the [Releases](../../releases) page:

- **Windows**: `mcp-time-server.exe`
- **macOS**: `mcp-time-server-macos` (Apple Silicon)
- **Linux**: `mcp-time-server-linux` (x86_64)

On Unix systems (macOS/Linux), make the file executable:
```bash
chmod +x mcp-time-server-macos  # or mcp-time-server-linux
```

### Option 2: Run from Source

1. Clone or download this repository
2. Install dependencies:

```bash
pip install mcp
```

For development and building:

```bash
pip install mcp pyinstaller
```

### Running the Server

#### Standard Mode

```bash
python server.py
```

#### As MCP Server with Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "time": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

Or if using the compiled executable:

```json
{
  "mcpServers": {
    "time": {
      "command": "/absolute/path/to/mcp-time-server"
    }
  }
}
```

## Building Executables

### Prerequisites

```bash
pip install pyinstaller
```

### Build for Current Platform

Run the build script:

```bash
python build.py
```

This will create a standalone executable in the `dist/` directory.

### Cross-Platform Building

#### Automated Builds (GitHub Actions)

This repository includes a GitHub Actions workflow that automatically builds executables for all platforms:

- **Builds on every push** to main branch
- **Creates releases** when you push a version tag (e.g., `v1.0.0`)
- **Builds for**: Windows (x86_64), macOS (ARM64), Linux (x86_64)

To create a new release:
```bash
git tag v1.0.0
git push origin v1.0.0
```

The workflow will automatically build and attach executables to the GitHub release.

#### Manual Cross-Platform Building

PyInstaller creates executables for the platform you're building on:

1. **macOS executable**: Build on macOS
2. **Linux executable**: Build on Linux (or use Docker with a Linux image)
3. **Windows executable**: Build on Windows (or use a Windows VM)

## Usage Examples

### Get Current Time

```python
# Local time
get_current_time()

# Specific timezone
get_current_time(tz="America/New_York")
get_current_time(tz="Europe/London")
get_current_time(tz="Asia/Tokyo")
```

### Parse and Validate Dates

```python
# Parse a date
parse_datetime(
    date_string="2025-11-21 14:30:00",
    format_string="%Y-%m-%d %H:%M:%S"
)

# Validate a date
is_valid_datetime(
    date_string="2025-11-21",
    format_string="%Y-%m-%d"
)
```

### Compare Times

```python
compare_times(
    time1="2025-01-01 00:00:00",
    time2="2025-12-31 23:59:59",
    format_string="%Y-%m-%d %H:%M:%S"
)
```

### Add/Subtract Time

```python
# Add 5 days and 3 hours
add_time_delta(
    base_time="2025-11-21 10:00:00",
    days=5,
    hours=3,
    format_string="%Y-%m-%d %H:%M:%S"
)

# Subtract 2 days (use negative values)
add_time_delta(
    base_time="2025-11-21 10:00:00",
    days=-2,
    format_string="%Y-%m-%d %H:%M:%S"
)
```

### Working with Timezones

```python
# List all timezones
list_timezones()

# Filter timezones
list_timezones(filter_text="America")

# Get timezone info
get_timezone_info(tz="America/New_York")
```

### Unix Timestamps

```python
# Convert Unix timestamp to datetime
unix_to_datetime(timestamp=1732204800)

# With specific timezone
unix_to_datetime(timestamp=1732204800, tz="UTC")
```

## Common DateTime Format Strings

| Format | Example |
|--------|---------|
| `%Y-%m-%d %H:%M:%S` | 2025-11-21 14:30:00 |
| `%Y-%m-%d` | 2025-11-21 |
| `%m/%d/%Y` | 11/21/2025 |
| `%d/%m/%Y %H:%M` | 21/11/2025 14:30 |
| `%B %d, %Y` | November 21, 2025 |
| `%Y-%m-%dT%H:%M:%S` | 2025-11-21T14:30:00 (ISO format) |

## Technical Details

### Dependencies

- **Runtime**: Python 3.10+
- **MCP Framework**: `mcp` (FastMCP)
- **Build Tool**: PyInstaller 6.0+
- **Timezone Data**: `tzdata` (automatically included on Windows)

### Standard Library Modules Used

- `datetime` - Core date/time operations
- `zoneinfo` - Timezone support (Python 3.9+)
- `time` - Time utilities
- `typing` - Type hints

### Timezone Support

The server uses Python's `zoneinfo` module which:
- On Unix systems (macOS/Linux): Uses system timezone database
- On Windows: Requires `tzdata` package (automatically installed via dependencies)

## Platform-Specific Notes

### macOS
- Timezone data from system (`/usr/share/zoneinfo`)
- Executable will be for your Mac's architecture (Intel or Apple Silicon)

### Linux
- Timezone data from system (`/usr/share/zoneinfo`)
- Build on the architecture you want to target (x86_64, ARM, etc.)

### Windows
- Requires `tzdata` package (included in dependencies)
- May need to run build script as administrator
- Antivirus might flag PyInstaller executables (false positive)

## Troubleshooting

### "No timezone data found"

On Windows, ensure `tzdata` is installed:
```bash
pip install tzdata
```

### Executable is too large

The executable includes Python runtime and all dependencies. Typical sizes:
- macOS: 15-20 MB
- Linux: 10-15 MB
- Windows: 15-20 MB

To reduce size, you can disable UPX compression in the `.spec` file.

### "Permission denied" when running executable

On Unix systems:
```bash
chmod +x dist/mcp-time-server
```

## License

MIT

## Contributing

This is a simple, focused MCP server. If you need additional time utilities, feel free to fork and extend!
