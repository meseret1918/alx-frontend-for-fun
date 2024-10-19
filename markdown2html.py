#!/usr/bin/python3
import sys
import os

def parse_headings(line):
    level = line.count('#')
    if level > 0 and level <= 6:
        content = line[level:].strip()
        return f"<h{level}>{content}</h{level}>"
    return None

def parse_unordered_list(lines):
    output = "<ul>\n"
    for line in lines:
        if line.startswith('- '):
            item = line[2:].strip()
            output += f"<li>{item}</li>\n"
    output += "</ul>\n"
    return output

def parse_ordered_list(lines):
    output = "<ol>\n"
    for line in lines:
        if line.startswith('* '):
            item = line[2:].strip()
            output += f"<li>{item}</li>\n"
    output += "</ol>\n"
    return output

def parse_paragraphs(lines):
    output = ""
    paragraph = ""
    for line in lines:
        if line.strip() == "":
            if paragraph:
                output += f"<p>{paragraph.strip()}</p>\n"
                paragraph = ""
        else:
            paragraph += line + "\n"
    if paragraph:
        output += f"<p>{paragraph.strip()}</p>\n"
    return output

def parse_bold_and_emphasis(line):
    line = line.replace("**", "<b>").replace("__", "<em>")
    return line.replace("<b>", "<b>").replace("<em>", "</em>")

def convert_markdown_to_html(markdown_file, output_file):
    with open(markdown_file, 'r') as f:
        lines = f.readlines()

    html_output = ""
    
    for line in lines:
        # Parse headings
        heading = parse_headings(line)
        if heading:
            html_output += heading
            continue
        
        # Parse unordered lists
        unordered_list = parse_unordered_list(lines)
        if unordered_list:
            html_output += unordered_list
            continue

        # Parse ordered lists
        ordered_list = parse_ordered_list(lines)
        if ordered_list:
            html_output += ordered_list
            continue

        # Parse paragraphs
        paragraph = parse_paragraphs(lines)
        if paragraph:
            html_output += paragraph
            continue
        
        # Parse bold and emphasis text
        line = parse_bold_and_emphasis(line)
        if line.strip():
            html_output += line.strip() + "\n"

    # Write the output to the specified HTML file
    with open(output_file, 'w') as f:
        f.write(html_output)

def main():
    # Check the number of arguments
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    # Convert Markdown to HTML
    convert_markdown_to_html(markdown_file, output_file)

    # If all checks passed, exit normally
    sys.exit(0)

if __name__ == "__main__":
    main()