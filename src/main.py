from pathlib import Path
import shutil, os
from generate_page import generate_page

def recursive_call(path_to_files):
    home = "/home/lera/projects/project_3/" #the path of the project
    if path_to_files == "" and "public" not in os.listdir(home):
        os.mkdir(home + 'public')

    for path in Path(home + "public" + "/" + path_to_files).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    
    source = home + 'static' + "/" + path_to_files
    destination = home + 'public' + "/" + path_to_files
    files=os.listdir(source)
    for fname in files:
        if os.path.isfile(source + "/" + fname):
            shutil.copy(os.path.join(source,fname), destination)
        else:
            os.mkdir(home + 'public' + "/" + path_to_files + "/" + fname)
            recursive_call(fname)
    
    generate_page(home + "content/index.md", home + "template.html", home + "public/index.html")


def main():
    recursive_call("")

main()