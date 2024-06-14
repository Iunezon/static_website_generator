from textnode import *
from htmlnode import *
import os
import shutil

def main():
    generate_pages_recursive(
        "./content", 
        "./static/template.html", 
        "./static"
    )

    src = "./static"  # Source directory
    dst = "./public"  # Destination directory

    if os.path.exists(dst):
        shutil.rmtree(dst)
        print(f"Directory cleared: {dst}")

    copy_contents(src, dst)


def copy_contents(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
        print(f"Directory created: {dst}")
    
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"File copied: {src_path} to {dst_path}")
        elif os.path.isdir(src_path):
            copy_contents(src_path, dst_path)
        else:
            print(f"Skipping unknown item: {src_path}")

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.replace(u'\xa0', ' ').startswith("# "):
            return line.strip("#").replace(u'\xa0', ' ').strip()
    raise Exception("Markdown withouth title. Please add as first line the title preceded by '#' and a blank space")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as handle:
        md = handle.read()

    with open(template_path, "r") as handle:
        template = handle.read()
    
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    html = template.replace(r"{{ Title }}", title).replace(r"{{ Content }}", html)

    dst = os.path.dirname(dest_path)
    if not os.path.exists(dst):
        os.makedirs(dst)
        print(f"Directory created: {dst}")
    with open(dest_path, "w") as handle:
        handle.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)

    for content in contents:
        dir_path = os.path.join(dir_path_content, content)
        if os.path.isfile(dir_path):
            ext = content.split(".")[-1]
            file_name = ".".join(content.split(".")[:-1])
            if ext == "md":
                generate_page(
                    dir_path, 
                    template_path,
                    os.path.join(dest_dir_path, file_name+".html")
                )
        else:
            print(dir_path)
            generate_pages_recursive(
                dir_path, 
                template_path, 
                os.path.join(dest_dir_path, content)
            )

main()