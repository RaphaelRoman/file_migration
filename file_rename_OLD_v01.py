import os
import shutil

FILE_PATH  = "Z:\\intro_to_3d_grading\\04_build_kit\\submits\\"

def add_prefix(dir, prefix):
    for file in os.listdir(dir):
        if file.endswith('.png') or file.endswith('.PNG'):
            if not file.startswith(prefix):
                os.rename(f"{dir}{file}", f"{dir}{prefix}{file}")

if __name__ == '__main__':
    add_prefix(FILE_PATH, "04_")