import os
import shutil

def copy_directory(source, destination):
   shutil.copytree(source, destination)

def main():
    src = "./static"
    dest = "./public"

    print("Deleting public directory...")
    if os.path.exists(dest):
        shutil.rmtree(dest)

    print("Copying static files to public directory...")
    copy_directory(src, dest)

if __name__ == "__main__":
    main()

