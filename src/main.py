import os, shutil, sys
from pathlib import Path
from block_markdown import markdown_to_html_node

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(basepath)
    dir_path_static = "./static"
    dir_path_docs = "./docs"
    dir_path_content = "./content"
    template_path = "./template.html"
    create_public()
    
    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)



def create_public():
    if os.path.exists("docs"):
        shutil.rmtree("docs")  # Clean out the old 'public' directory

    os.mkdir("docs")  # Recreate it fresh

    static_dir = "static"
    docs_dir = "docs"

    # First, copy the static files into the public directory
    create_public_recursive(static_dir, docs_dir)


def create_public_recursive(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)  # Ensure the destination exists before copying

    for item in os.listdir(source):
        item_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)

        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_path)
        elif os.path.isdir(item_path):
            os.mkdir(dest_path)  # Create subdirectory in destination
            create_public_recursive(item_path, dest_path)  # Recurse into subdirectory

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)

    if basepath.endswith('/') and basepath != '/':
        basepath = basepath[:-1]
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
        
    template = template.replace('href="/', f'href="{basepath}/')
    template = template.replace('src="/', f'src="{basepath}/')


    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")
        

if __name__ == "__main__":
    main()