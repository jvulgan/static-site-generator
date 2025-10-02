import os
import shutil


def copy_files(src: str, dest: str):
    """
    Copy files from source directory to destination making sure destination is empty beforehand.
    """
    print(f"Copying from {src} to {dest}")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    for item in os.listdir(src):
        item_path = os.path.join(src, item)
        if os.path.isfile(item_path):
            print(f"Copying file {item_path}")
            shutil.copy(item_path, dest)
        else:
            copy_files(item_path, os.path.join(dest, item))
