import os
from pathlib import Path

# 1. Išvardiname visus reikiamus katalogus
#    Sukursime tik šią struktūrą:
#    visualize/
#      components/
#      callbacks/
#    assets/
directories = [
    "visualize",
    "visualize/components",
    "visualize/callbacks",
    "assets"
]

# 2. Išvardiname visus reikiamus failus su jų keliais
#    Jei jie neegzistuoja, sukursime tuščius modulius/failus.
files = [
    "visualize/layout.py",
    "visualize/components/filters.py",
    "visualize/components/bar_topics.py",
    "visualize/components/pie_topics.py",
    "visualize/components/line_topics.py",
    "visualize/components/questions_table.py",
    "visualize/callbacks/filter_callbacks.py",
    "visualize/callbacks/crossfilter_callbacks.py",
    "assets/custom.css"
]

def ensure_directories_exist(dir_list):
    """
    Patikrina, ar katalogai egzistuoja. Jei ne – sukuria.
    """
    for dir_path in dir_list:
        path_obj = Path(dir_path)
        if not path_obj.exists():
            path_obj.mkdir(parents=True, exist_ok=True)
            print(f"Sukurta direktorija: {dir_path}")
        else:
            print(f"Direktorija jau egzistuoja: {dir_path}")

def ensure_files_exist(file_list):
    """
    Patikrina, ar failai egzistuoja. Jei ne – sukuria tuščius failus.
    """
    for file_path in file_list:
        path_obj = Path(file_path)
        parent_dir = path_obj.parent
        if not parent_dir.exists():
            parent_dir.mkdir(parents=True, exist_ok=True)
            print(f"Sukurta trūkstama direktorija: {parent_dir}")
        if not path_obj.exists():
            path_obj.touch()
            print(f"Sukurta failas: {file_path}")
        else:
            print(f"Failas jau egzistuoja: {file_path}")

if __name__ == "__main__":
    ensure_directories_exist(directories)
    ensure_files_exist(files)
