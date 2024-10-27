<<<<<<< HEAD
#!/usr/bin/python3
"""
This is a script to convert a Markdown file to HTML.

Usage:
    ./markdown2html.py [input_file] [output_file]

Arguments:
    input_file: the name of the Markdown file to be converted
    output_file: the name of the output HTML file

Example:
    ./markdown2html.py README.md README.html
"""

import argparse
import pathlib
import re


def convert_md_to_html(input_file, output_file):
    '''
    Converts markdown file to HTML file
    '''
    # Read the contents of the input file
    with open(input_file, encoding='utf-8') as f:
        md_content = f.readlines()

    html_content = []
    for line in md_content:
        # Check if the line is a heading
        match = re.match(r'(#){1,6} (.*)', line)
        if match:
            # Get the level of the heading
            h_level = len(match.group(1))
            # Get the content of the heading
            h_content = match.group(2)
            # Append the HTML equivalent of the heading
            html_content.append(f'<h{h_level}>{h_content}</h{h_level}>\n')
        else:
            html_content.append(line)

    # Write the HTML content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(html_content)


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Convert markdown to HTML')
    parser.add_argument('input_file', help='path to input markdown file')
    parser.add_argument('output_file', help='path to output HTML file')
    args = parser.parse_args()

    # Check if the input file exists
    input_path = pathlib.Path(args.input_file)
    if not input_path.is_file():
        print(f'Missing {input_path}', file=sys.stderr)
        sys.exit(1)

    # Convert the markdown file to HTML
    convert_md_to_html(args.input_file, args.output_file)
=======
#!/usr/bin/python3
"""
Markdown to HTML converter.
"""

import sys
import os


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
    in_ul = in_paragraph = False

    for line in markdown_content:
        line = line.rstrip()

        # Handle headings
        if line.startswith("#"):
            if in_ul:
                html_content.append("</ul>\n")
                in_ul = False
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

        # Handle paragraphs and line breaks within paragraphs
        elif line:
            if in_ul:
                html_content.append("</ul>\n")
                in_ul = False

            if not in_paragraph:
                html_content.append("<p>\n")
                in_paragraph = True

            # Add line break if not the first line in the paragraph
            if html_content[-1].strip() != "<p>":
                html_content.append("<br/>\n")

            # Parse bold and italic markdown in text
            line = parse_bold_and_italic(line)

            html_content.append(f"{line}\n")

        # Handle empty lines (end of a paragraph)
        else:
            if in_paragraph:
                html_content.append("</p>\n")
                in_paragraph = False

    # Ensure any open tags are closed
    if in_ul:
        html_content.append("</ul>\n")
    if in_paragraph:
        html_content.append("</p>\n")

    with open(html_file, "w") as output_file:
        output_file.writelines(html_content)
>>>>>>> 4b11e8622845e06f88239728b09abb4618a2a719
