from pathlib import Path
import shutil, os, sys
from generate_page import generate_pages_recursive

def recursive_call(path_to_files):
    basepath = ""
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    os.makedirs("docs", mode=0o777, exist_ok=True)

    for path in Path("docs" + "/" + path_to_files).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    
    source = 'static' + "/" + path_to_files
    destination = 'docs' + "/" + path_to_files
    files=os.listdir(source)
    for fname in files:
        if os.path.isfile(source + "/" + fname):
            shutil.copy(os.path.join(source,fname), destination)
        else:
            os.mkdir('docs' + "/" + path_to_files + "/" + fname)
            recursive_call(path_to_files + "/" + fname)

    generate_pages_recursive("content", "template.html", "docs", basepath)


def main():
    recursive_call("")

main()