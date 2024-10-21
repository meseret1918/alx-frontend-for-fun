#!/usr/bin/python3
"""
Markdown to HTML converter.
"""

import sys
import os
import hashlib


def print_usage_and_exit():
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)


def file_error_and_exit(filename):
    print(f"Missing {filename}", file=sys.stderr)
    sys.exit(1)


def parse_bold_and_italic(line):
    """
    Replace Markdown bold (**) and italic (__) syntax with the corresponding
    HTML tags.
    """
    # Replace bold syntax (**bold text**) with <b>bold text</b>
    while '**' in line:
        line = line.replace('**', '<b>', 1)
        line = line.replace('**', '</b>', 1)

    # Replace italic syntax (__italic text__) with <em>italic text</em>
    while '__' in line:
        line = line.replace('__', '<em>', 1)
        line = line.replace('__', '</em>', 1)

    return line


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
    in_ul = in_ol = in_paragraph = False

    for line in markdown_content:
        line = line.rstrip()

        # Handle headings
        if line.startswith("#"):
            if in_ul:
                html_content.append("</ul>\n")
                in_ul = False
            if in_ol:
                html_content.append("</ol>\n")
                in_ol = False
            if in_paragraph:
                html_content.append("</p>\n")
                in_paragraph = False

            heading_level = len(line.split(' ')[0])
            heading_text = line[heading_level + 1:]
            html_content.append(
                f"<h{heading_level}>{heading_text}</h{heading_level}>\n"
            )

        # Handle unordered list items
        elif line.startswith("-"):
            if in_paragraph:
                html_content.append("</p>\n")
                in_paragraph = False
            if not in_ul:
                html_content.append("<ul>\n")
                in_ul = True
            list_item = line[2:]
            list_item = parse_bold_and_italic(list_item)  # Parse bold/italic
            html_content.append(f"<li>{list_item}</li>\n")

        # Handle ordered list items
        elif line.startswith("*"):
            if in_paragraph:
                html_content.append("</p>\n")
                in_paragraph = False
            if not in_ol:
                html_content.append("<ol>\n")
                in_ol = True
            list_item = line[2:]
            list_item = parse_bold_and_italic(list_item)  # Parse bold/italic
            html_content.append(f"<li>{list_item}</li>\n")

        # Handle paragraphs and line breaks within paragraphs
        elif line:
            if in_ul:
                html_content.append("</ul>\n")
                in_ul = False
            if in_ol:
                html_content.append("</ol>\n")
                in_ol = False

            if not in_paragraph:
                html_content.append("<p>\n")
                in_paragraph = True

            # Add line break if not the first line in the paragraph
            if (line != markdown_content[0] and in_paragraph and
                    html_content[-1].strip() != "<p>"):
                html_content.append("<br/>\n")

            # Parse bold and italic markdown in text
            line = parse_bold_and_italic(line)

            # Handle custom [[ ]] with MD5 hash
            while "[[" in line and "]]" in line:
                start = line.find("[[") + 2
                end = line.find("]]")
                to_convert = line[start:end]
                md5_hash = hashlib.md5(to_convert.encode()).hexdigest()
                line = line.replace(f"[[{to_convert}]]", md5_hash)

            # Handle custom (( )) with text modification
            while "((" in line and "))" in line:
                start = line.find("((") + 2
                end = line.find("))")
                to_modify = line[start:end]
                modified_text = to_modify.replace("c", "").replace("C", "")
                line = line.replace(f"(({to_modify}))", modified_text)

            html_content.append(f"{line}\n")

        # Handle empty lines (end of a paragraph)
        else:
            if in_paragraph:
                html_content.append("</p>\n")
                in_paragraph = False

    # Ensure any open tags are closed
    if in_ul:
        html_content.append("</ul>\n")
    if in_ol:
        html_content.append("</ol>\n")
    if in_paragraph:
        html_content.append("</p>\n")

    with open(html_file, "w") as output_file:
        output_file.writelines(html_content)
