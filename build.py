import shutil
import os
import re
import sys

def process_includes(source, includes, built):
    shutil.copytree(source, built)

    pattern = re.compile(r"<!--\$\s*([a-zA-Z0-9-_]+\.[a-zA-Z0-9]+)\s*\$-->")
    print(f"Processing includes for HTML files in: {built}")
    
    for root, _, files in os.walk(built):
        for file in files:
            if file.endswith(".htm") or file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    html = f.read()
                
                matches = pattern.findall(html)
                dirty = False
                
                for match in matches:
                    include_file_path = os.path.join(includes, match)
                    
                    if not os.path.exists(include_file_path):
                        raise FileNotFoundError(f"{match} does not exist in includes.")
                    
                    with open(include_file_path, "r", encoding="utf-8") as f:
                        include_content = f.read()
                    
                    placeholder = f"<!--$ {match} $-->"
                    html = html.replace(placeholder, include_content)
                    print(f"Expanded {match} in {file_path}")
                    dirty = True
                
                if dirty:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(html)
                
                print(f"Processed {file_path}")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        source_dir = sys.argv[1]
        includes_dir = sys.argv[2]
        build_output_dir = sys.argv[3]
    else
        source_dir = "src"
        includes_dir = "includes"
        build_output_dir = "built"
    
    process_includes(source_dir, includes_dir, build_output_dir)
