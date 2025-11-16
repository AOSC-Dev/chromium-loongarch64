#!/usr/bin/env python3
"""
Format diff file to use a/b prefixes and standardized timestamps.

This script converts diff files from:
  diff ... -r original/path patched/path
  --- original/path timestamp
  +++ patched/path timestamp

To:
  diff '--color=auto' -p -X ../chromium-loongarch64/chromium/exclude -N -u -r a/path b/path
  --- a/path 2000-01-01 00:00:00.000000000 +0800
  +++ b/path 2000-01-01 00:00:00.000000000 +0800
"""

import re
import sys
import tempfile
import shutil


def format_diff(input_file, output_file):
    """Format a diff file with standardized paths and timestamps."""

    # Standard timestamp to use
    TIMESTAMP = "2000-01-01 00:00:00.000000000 +0800"

    # Pattern to match diff command line
    # Matches: diff ... -r some-prefix-original/path some-prefix-patched/path
    diff_pattern = re.compile(
        r"^diff\s+.*?\s+-r\s+\S*?([^\s]+)\s+\S*?([^\s]+)$"
    )

    # Pattern to match --- line
    # Matches: --- some-prefix-original/path timestamp
    old_file_pattern = re.compile(
        r"^---\s+(\S+?)(?:\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+\s+[+-]\d{4})?$"
    )

    # Pattern to match +++ line
    # Matches: +++ some-prefix-patched/path timestamp
    new_file_pattern = re.compile(
        r"^\+\+\+\s+(\S+?)(?:\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+\s+[+-]\d{4})?$"
    )

    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:

        for line in f_in:
            # Handle diff command line
            diff_match = diff_pattern.match(line)
            if diff_match:
                path = diff_match.group(1)
                # Extract just the relative path
                if '/' in path:
                    # Find the first real path component after the prefix
                    parts = path.split('/')
                    rel_path = '/'.join(parts[1:]) if len(parts) > 1 else path
                else:
                    rel_path = path

                # Write standardized diff command
                f_out.write(
                    f"diff '--color=auto' -p -X ../chromium-loongarch64/chromium/exclude "
                    f"-N -u -r a/{rel_path} b/{rel_path}\n"
                )
                continue

            # Handle --- line (old file)
            old_match = old_file_pattern.match(line)
            if old_match:
                path = old_match.group(1)
                # Extract relative path
                if '/' in path:
                    parts = path.split('/')
                    rel_path = '/'.join(parts[1:]) if len(parts) > 1 else path
                else:
                    rel_path = path

                f_out.write(f"--- a/{rel_path}\t{TIMESTAMP}\n")
                continue

            # Handle +++ line (new file)
            new_match = new_file_pattern.match(line)
            if new_match:
                path = new_match.group(1)
                # Extract relative path
                if '/' in path:
                    parts = path.split('/')
                    rel_path = '/'.join(parts[1:]) if len(parts) > 1 else path
                else:
                    rel_path = path

                f_out.write(f"+++ b/{rel_path}\t{TIMESTAMP}\n")
                continue

            # All other lines pass through unchanged
            f_out.write(line)


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} <diff_file> [output_file]")
        print(f"Example: {sys.argv[0]} input.diff           # in-place modification")
        print(f"         {sys.argv[0]} input.diff output.diff  # write to different file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else None

    try:
        if output_file is None:
            # In-place modification using temporary file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp_file:
                tmp_path = tmp_file.name

            format_diff(input_file, tmp_path)
            shutil.move(tmp_path, input_file)
            print(f"Successfully formatted diff file: {input_file}")
        else:
            # Write to different file
            format_diff(input_file, output_file)
            print(f"Successfully formatted diff file: {input_file} -> {output_file}")
    except Exception as e:
        print(f"Error formatting diff file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
