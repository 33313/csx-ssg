import re
import shutil
import os
from markdown_to_html import markdown_to_html_node


def main():
    path = './public'
    shutil.rmtree(path)
    shutil.copytree('./static', './public')
    generate_page('./content/index.md', 'template.html', './public/index.html')


def extract_title(md):
    res = re.search(r"# .+\n\n", md)
    if res is None:
        raise Exception("All pages need at least one h1 header.")
    return res.group().strip("# ")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_in = None
    template = None
    with open(from_path, "r") as f:
        md_in = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    content = markdown_to_html_node(md_in).to_html()
    title = extract_title(md_in)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)


main()
