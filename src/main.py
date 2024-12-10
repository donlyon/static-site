from textnode import TextNode, TextType
import os
import shutil
from textnode import markdown_to_html_node

def main():
    if  os.path.exists("public"):
        print("The public directory exists")
        shutil.rmtree("public")
    else:
        print("The public directory does not exist")
    os.mkdir("public")

    copy_files("static", "public")

    generate_pages_recursive("content", "template.html", "public")

def copy_files(from_dir, to_dir):
    if not os.path.exists(to_dir):
        os.mkdir(to_dir)
    dir_contents = os.listdir(from_dir)
    for item in dir_contents:
        if os.path.isfile(f"{from_dir}/{item}"):
            print(f"Copying {from_dir}/{item} to {to_dir}/{item}")
            shutil.copy(f"{from_dir}/{item}", f"{to_dir}/{item}")
        else:
            copy_files(f"{from_dir}/{item}", f"{to_dir}/{item}")

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.replace("#", "").strip()

    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Gernerating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
        filename = os.path.basename(from_path).replace(".md", "")
        f.close()
    with open(template_path, "r") as f:
        template = f.read()
        f.close()
    html_nodes = markdown_to_html_node(markdown)
    html = html_nodes.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    with open(f"{dest_path}/{filename}.html", "w") as f:
        f.write(template)
        f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_contents = os.listdir(dir_path_content)
    for item in dir_contents:
        if os.path.isfile(f"{dir_path_content}/{item}"):
            if item.endswith(".md"):
                generate_page(f"{dir_path_content}/{item}", template_path, dest_dir_path)
        else:
            generate_pages_recursive(f"{dir_path_content}/{item}", template_path, f"{dest_dir_path}/{item}")

main()
