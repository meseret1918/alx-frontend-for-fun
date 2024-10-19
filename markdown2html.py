#!/usr/bin/python3
import sys
import os

# Check if the number of arguments is less than 2
if len(sys.argv) < 3:
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)

# Extract filenames from arguments
markdown_file = sys.argv[1]
output_file = sys.argv[2]

# Check if the markdown file exists
if not os.path.isfile(markdown_file):
    print(f"Missing {markdown_file}", file=sys.stderr)
    sys.exit(1)

# If everything is okay, do nothing and exit with code 0
sys.exit(0)