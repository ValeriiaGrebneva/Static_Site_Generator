from pathlib import Path
import shutil, os
from generate_page import generate_pages_recursive

def recursive_call(path_to_files):
    if path_to_files == "" and "public" not in os.listdir():
        os.mkdir('public')

    for path in Path("public" + "/" + path_to_files).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    
    source = 'static' + "/" + path_to_files
    destination = 'public' + "/" + path_to_files
    files=os.listdir(source)
    for fname in files:
        if os.path.isfile(source + "/" + fname):
            shutil.copy(os.path.join(source,fname), destination)
        else:
            os.mkdir('public' + "/" + path_to_files + "/" + fname)
            recursive_call(path_to_files + "/" + fname)

    generate_pages_recursive("content", "template.html", "public")


def main():
    recursive_call("")

main()