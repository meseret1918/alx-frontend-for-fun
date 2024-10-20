#!/usr/bin/python3
"""
Markdown to HTML converter.
"""

import sys
import os
import hashlib

def print_usage_and_exit():
    print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
    sys.exit(1)

def file_error_and_exit(filename):
    print(f"Missing {filename}", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage_and_exit()
    
    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        file_error_and_exit(markdown_file)

    with open(markdown_file, "r") as md_file:
        markdown_content = md_file.readlines()

    html_content = []
    in_ul = in_ol = False

    for line in markdown_content:
        line = line.strip()

        # Handle headings
        if line.startswith("#"):
            if in_ul:
                html_content.append("</ul>\n")
                in_ul = False
            if in_ol:
                html_content.append("</ol>\n")
                in_ol = False
            heading_level = len(line.split(' ')[0])
            heading_text = line[heading_level + 1:]
            html_content.append(f"<h{heading_level}>{heading_text}</h{heading_level}>\n")

        # Handle unordered list items
        elif line.startswith("-"):
            if not in_ul:
                html_content.append("<ul>\n")
                in_ul = True
            list_item = line[2:]
            html_content.append(f"<li>{list_item}</li>\n")

        # Handle ordered list items
        elif line.startswith("*"):
            if not in_ol:
                html_content.append("<ol>\n")
                in_ol = True
            list_item = line[2:]
            html_content.append(f"<li>{list_item}</li>\n")

        # Handle paragraphs and line breaks
        elif line:
            if not in_ul and not in_ol:
                html_content.append("<p>\n")
            line = line.replace("**", "<b>").replace("**", "</b>")
            line = line.replace("__", "<em>").replace("__", "</em>")

            while "[[" in line and "]]" in line:
                start = line.find("[[") + 2
                end = line.find("]]")
                to_convert = line[start:end]
                md5_hash = hashlib.md5(to_convert.encode()).hexdigest()
                line = line.replace(f"[[{to_convert}]]", md5_hash)

            while "((" in line and "))" in line:
                start = line.find("((") + 2
                end = line.find("))")
                to_modify = line[start:end]
                modified_text = to_modify.replace("c", "").replace("C", "")
                line = line.replace(f"(({to_modify}))", modified_text)

            html_content.append(f"{line}\n")
            html_content.append("</p>\n")

    with open(html_file, "w") as html_file:
        html_file.writelines(html_content)

