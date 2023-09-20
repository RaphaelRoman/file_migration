import os
import shutil

'''

Migration Tool v1.0.0

    Description:

    This is a tool that will allow you to migrate or copy files of a specific filetype to another directory.

'''
# PREP
def get_dir_files(path, list, print = False):
    for file in os.listdir(path):
        list.append(file)
    if print:
        print(list)

filetypes = ['pdf', 'gif', 'psd', 'avi', 'doc', 'mp4', 'jpg', 'tif', 'txt', 'mp3', 'wav', 'mov', 'png', 'exe', 'zip']
def make_filetype_dict(filetypes, dict, print = False):
    for filetype in filetypes:
        dict[filetype] = '.' + filetype
    if print:
        print(dict)

# MASTER CONSTANTS
MASTER_FROM_DIR = 'K:\\Zach Gray\\Intro to 3D\\_incoming\\'
MASTER_FROM_FOLDERS = []
get_dir_files(MASTER_FROM_DIR, MASTER_FROM_FOLDERS)

MASTER_TO_DIR = 'Z:\\intro_to_3d_grading\\'
MASTER_TO_FOLDERS = []
get_dir_files(MASTER_TO_DIR, MASTER_TO_FOLDERS)

MASTER_FILE_TYPES = {}
make_filetype_dict(filetypes, MASTER_FILE_TYPES)

# MIGRATION CONSTANTS
FILETYPES = [MASTER_FILE_TYPES['png']]
FROM_FOLDER = MASTER_FROM_FOLDERS[4] + '\\'
FROM_DIR = f'{MASTER_FROM_DIR}{FROM_FOLDER}'
TO_FOLDER = MASTER_TO_FOLDERS[2] + '\\'
TO_DIR = f'{MASTER_TO_DIR}{TO_FOLDER}'

def is_valid_dir(from_dir, to_dir):
    if not os.path.exists(from_dir) or not os.path.exists(to_dir):
        raise ValueError("Please check to make sure you have provided valid directories for migration.")
is_valid_dir(MASTER_FROM_DIR, MASTER_TO_DIR)

def file_migration(from_dir, to_dir, filetypes, move = False):
    upper_list = []
    sub_files = []
    sub_dirs = []

    for filetype in filetypes:
        upper_filetype = filetype.upper()
        upper_list.append(upper_filetype)
    
    for upper_filetype in upper_list:
        filetypes.append(upper_filetype)
    
    for file in os.walk(from_dir):
        if file[2]:
            sub_files.append(file[2])
        if file[0]:
            sub_dirs.append(file[0])

    for sub_file in sub_files:
        for sub_data in sub_file:
            for filetype in filetypes:
                if sub_data.endswith(filetype):
                    for sub_dir in sub_dirs:
                        if os.path.isfile(f'{sub_dir}\{sub_data}'):
                            if move:     
                                print(f"MOVING \"{sub_dir}\{sub_data}\" NOW")
                                shutil.move(f'{sub_dir}\{sub_data}', TO_DIR)
                                print("MOVING COMPLETE")
                            else:
                            print(f"COPYING \"{sub_dir}\{sub_data}\" NOW")
                            shutil.copy(f'{sub_dir}\{sub_data}', TO_DIR)
                            print("COPYING COMPLETE")

if __name__ == "__main__":
    file_migration(FROM_DIR, TO_DIR, FILETYPES)