import os
import sys
print(f'in __init__.py in ui directory')



# General __init__.py code in every directory
project_dir = "C:\\Users\\Admin\\Desktop\\Projects\\CRACK_THE_LOCK"

cur__file__:'str' = __file__

sys_path_set_version = set(sys.path)
while len(cur__file__) > len(project_dir):
    cur__file__ = os.path.split(cur__file__)[0]

    if cur__file__ not in sys_path_set_version:
        sys.path.append(cur__file__)
