#!/usr/bin/env python3
"""
Build script for MCP Time Server
Creates standalone executables for the current platform
"""

import subprocess
import sys
import platform
import shutil
from pathlib import Path


def main():
    print(f"Building MCP Time Server for {platform.system()} {platform.machine()}...")
    print()

    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("ERROR: PyInstaller not found!")
        print("Install it with: pip install pyinstaller")
        sys.exit(1)

    # Clean previous builds
    dist_dir = Path("dist")
    build_dir = Path("build")

    if dist_dir.exists():
        print("Cleaning previous dist directory...")
        shutil.rmtree(dist_dir)

    if build_dir.exists():
        print("Cleaning previous build directory...")
        shutil.rmtree(build_dir)

    print()

    # Run PyInstaller
    print("Running PyInstaller...")
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "mcp-time-server.spec"],
        capture_output=False
    )

    if result.returncode != 0:
        print("\nBuild failed!")
        sys.exit(1)

    print()
    print("=" * 60)
    print("Build successful!")
    print("=" * 60)
    print()

    # Find the executable
    if platform.system() == "Windows":
        exe_name = "mcp-time-server.exe"
    else:
        exe_name = "mcp-time-server"

    exe_path = dist_dir / exe_name

    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"Executable: {exe_path}")
        print(f"Size: {size_mb:.2f} MB")
        print()
        print("You can now distribute this executable to other machines")
        print(f"running {platform.system()} {platform.machine()}")
    else:
        print(f"Warning: Expected executable not found at {exe_path}")


if __name__ == "__main__":
    main()
