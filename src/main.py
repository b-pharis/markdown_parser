import os, shutil

def main():
    create_public()


def create_public():
    if os.path.exists("public"):
        shutil.rmtree("public")

    if not os.path.exists("public"):
        os.mkdir("public")

    static_dir = "/home/brand/workspace/markdown_parser/static"
    public_dir = "/home/brand/workspace/markdown_parser/public"

    create_public_recursive(static_dir, public_dir)

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
        

main()