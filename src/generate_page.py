from collecting_to_html import markdown_to_html_node
#from htmlnode import ParentNode
import os

def extract_title(markdown):
    if markdown[0:2] != "# ":
        raise Exception("no header (# ) found")
    return markdown[2:].split("\n")[0].strip(" ")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    try:
        file_from_path = open(from_path)
        content_from_path = file_from_path.read()
        file_from_path.close()
    except OSError:
        print(f"file from {from_path} wasn't found")
        return
    
    try:
        file_template_path = open(template_path)
        content_template_path = file_template_path.read()
        file_template_path.close()
    except OSError:
        print(f"file from {template_path} wasn't found")
        return

    title = extract_title(content_from_path)
    html_string = markdown_to_html_node(content_from_path)
    html_string = html_string.to_html()
  
    template = content_template_path.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

    os.makedirs("/".join(dest_path.split("/")[:-1]), mode=0o777, exist_ok=True)
    

    with open(dest_path, "w+") as file_dest_path:
        file_dest_path.write(template)
    