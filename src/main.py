import os
import shutil

from src.markdown_html import markdown_to_html_node


def copy_directory(source, destination):
    shutil.copytree(source, destination)


def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("##"):
            continue
        if line.startswith("#"):
            title = line[1:].strip()
            if title:
                return title
    raise Exception("No h1 header found")


def generate_page(from_path, template_path, dest_path):
    if os.path.isdir(from_path):
        for entry in os.listdir(from_path):
            entry_path = os.path.join(from_path, entry)
            if os.path.isdir(entry_path):
                generate_page(entry_path, template_path, os.path.join(dest_path, entry))
                continue
            if not entry.endswith(".md"):
                continue
            dest_file = os.path.join(dest_path, f"{os.path.splitext(entry)[0]}.html")
            generate_page(entry_path, template_path, dest_file)
        return

    if not from_path.endswith(".md"):
        return

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(page)


def main():
    src = "./static"
    dest = "./public"

    print("Deleting public directory...")
    if os.path.exists(dest):
        shutil.rmtree(dest)

    print("Copying static files to public directory...")
    copy_directory(src, dest)
    generate_page("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()
