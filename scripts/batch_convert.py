#!/usr/bin/env python3
"""
Batch convert conversation-ir JSON files to markdown.

This script processes all directories in the target directory that contain
ir/conversation-ir/*.json files and converts them to markdown files
in a md/ subdirectory using the cwprint CLI from source.
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Determine CLI path from this script's location
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
CLI_PATH = REPO_ROOT / "chatweave_printer" / "cli.py"


def main():
    parser = argparse.ArgumentParser(
        description='Batch convert conversation-ir JSON files to markdown'
    )
    parser.add_argument(
        '-d', '--directory',
        type=Path,
        default=Path.home() / "Downloads",
        help='Target directory to process (default: ~/Downloads/)'
    )
    args = parser.parse_args()

    target_dir = args.directory.expanduser().resolve()

    if not target_dir.exists():
        print(f"Error: {target_dir} does not exist")
        sys.exit(1)

    if not CLI_PATH.exists():
        print(f"Error: CLI not found at {CLI_PATH}")
        sys.exit(1)

    total_processed = 0
    total_success = 0
    total_failed = 0

    # Iterate through all directories in target directory
    for dir_path in target_dir.iterdir():
        if not dir_path.is_dir():
            continue

        # Check if ir/conversation-ir/ exists
        ir_dir = dir_path / "ir" / "conversation-ir"
        if not ir_dir.exists():
            continue

        # Create md/ directory
        md_dir = dir_path / "md"
        md_dir.mkdir(parents=True, exist_ok=True)

        # Process all JSON files
        json_files = list(ir_dir.glob("*.json"))
        if not json_files:
            continue

        print(f"\nProcessing: {dir_path.name}")
        print(f"  Found {len(json_files)} JSON file(s)")

        for json_file in json_files:
            total_processed += 1
            output_file = md_dir / f"{json_file.stem}.md"

            try:
                result = subprocess.run(
                    [sys.executable, str(CLI_PATH), str(json_file), "-o", str(output_file)],
                    capture_output=True,
                    text=True,
                    check=True
                )
                total_success += 1
                print(f"  ✓ {json_file.name} -> {output_file.name}")
            except subprocess.CalledProcessError as e:
                total_failed += 1
                error_msg = e.stderr.strip() if e.stderr else str(e)
                print(f"  ✗ {json_file.name}: {error_msg}")

    # Print summary
    print("\n" + "=" * 50)
    print(f"Total files processed: {total_processed}")
    print(f"Success: {total_success}")
    print(f"Failed: {total_failed}")
    print("=" * 50)


if __name__ == "__main__":
    main()
