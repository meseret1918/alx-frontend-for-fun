#!/usr/bin/python3
import sys
import os
import hashlib

def markdown_to_html(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            content = f.readlines()
    except FileNotFoundError:
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    html_lines = []
    in_list = False
    list_type = None

    for line in content:
        line = line.rstrip()

        # Headings
        if line.startswith('#'):
            heading_level = len(line.split(' ')[0])
            heading_text = line[heading_level+1:].strip()
            html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")

        # Unordered list
        elif line.startswith('- '):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
                list_type = 'ul'
            html_lines.append(f"<li>{line[2:]}</li>")

        # Ordered list
        elif line.startswith('* '):
            if not in_list:
                html_lines.append("<ol>")
                in_list = True
                list_type = 'ol'
            html_lines.append(f"<li>{line[2:]}</li>")

        # End of list
        elif in_list and not line.startswith(('-', '*')):
            if list_type == 'ul':
                html_lines.append("</ul>")
            elif list_type == 'ol':
                html_lines.append("</ol>")
            in_list = False

        # Paragraphs
        elif line != "":
            # Handling bold and emphasis
            line = line.replace("**", "<b>").replace("__", "<em>")
            line = line.replace("<b>", "</b>", 1).replace("<em>", "</em>", 1)

            # Custom transformations: MD5 and letter removal
            if "[[" in line:
                start = line.find("[[")
                end = line.find("]]", start)
                if start != -1 and end != -1:
                    text = line[start + 2:end]
                    md5_hash = hashlib.md5(text.encode()).hexdigest()
                    line = line[:start] + md5_hash + line[end + 2:]
            
            if "((" in line:
                start = line.find("((")
                end = line.find("))", start)
                if start != -1 and end != -1:
                    text = line[start + 2:end]
                    transformed_text = text.replace("c", "").replace("C", "")
                    line = line[:start] + transformed_text + line[end + 2:]
            
            html_lines.append(f"<p>{line}</p>")

    # Close any unclosed lists
    if in_list:
        if list_type == 'ul':
            html_lines.append("</ul>")
        elif list_type == 'ol':
            html_lines.append("</ol>")

    with open(output_file, 'w') as f:
        for html_line in html_lines:
            f.write(html_line + '\n')


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    markdown_to_html(input_file, output_file)
    sys.exit(0)