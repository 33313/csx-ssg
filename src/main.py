import re
import shutil
import os
import glob
from markdown_to_html import markdown_to_html_node


def main():
    path = "./public"
    shutil.rmtree(path)
    # Yes, I used copytree. Fight me 😼
    shutil.copytree("./static", "./public")
    generate_pages_recursive("./content", "template.html", "./public")


def extract_title(md):
    res = re.search(r"# .+\n\n", md)
    if res is None:
        raise Exception("All pages need at least one h1 header.")
    return res.group().strip("# ")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files = []
    for file in glob.glob(f"{dir_path_content}/**/*.md", recursive=True):
        files.append(file)
    template = None
    with open(template_path, "r") as f:
        template = f.read()
    for file in files:
        content = None
        with open(file, "r") as f:
            content = f.read()
        title = extract_title(content)
        tmp = template.replace("{{ Title }}", title)
        tmp = tmp.replace("{{ Content }}", markdown_to_html_node(content).to_html())
        new_file_path = f"{dest_dir_path}/{file.removeprefix(dir_path_content)[:-3]}.html"
        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
        with open(new_file_path, "w") as f:
            f.write(tmp)


main()
