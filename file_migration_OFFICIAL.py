import os
from datetime import date, datetime
import shutil

'''

Migration Tool v1.0.4

    Description:

    This is a tool that will allow you to migrate or copy files of a specific filetype to another directory.

'''
# PREP
def get_dir_files(path, list, print_out = False):
    for file in os.listdir(path):
        list.append(file)
    if print_out:
        print(list)

filetypes = ['pdf', 'gif', 'psd', 'avi', 'doc', 'mp4', 'jpg', 'tif', 'txt', 'mp3', 'wav', 'mov', 'png', 'exe', 'zip', 'obj', 'fbx']
def make_filetype_dict(filetypes, dict, print_out = False):
    for filetype in filetypes:
        dict[filetype] = '.' + filetype
    if print_out:
        print(dict)

# MASTER CONSTANTS
MASTER_FROM_DIR = 'K:\\Zach Gray\\Intro to 3D\\_incoming\\'
MASTER_FROM_FOLDERS = []
get_dir_files(MASTER_FROM_DIR, MASTER_FROM_FOLDERS)
MASTER_TO_DIR = 'K:\\Zach Gray\\Intro to 3D\\grading\\'
MASTER_TO_FOLDERS = []
get_dir_files(MASTER_TO_DIR, MASTER_TO_FOLDERS)

MASTER_FILE_TYPES = {}
make_filetype_dict(filetypes, MASTER_FILE_TYPES)

# MIGRATION CONSTANTS
FILETYPES = [MASTER_FILE_TYPES['mov'], MASTER_FILE_TYPES['avi']]
FROM_FOLDER = MASTER_FROM_FOLDERS[6] + '\\'
FROM_DIR = f'{MASTER_FROM_DIR}{FROM_FOLDER}'
TO_FOLDER = MASTER_TO_FOLDERS[5] + '\\submit\\'
TO_DIR = f'{MASTER_TO_DIR}{TO_FOLDER}'

MOD_YEAR = "2023"
MOD_MONTH = "09"
MOD_DAY = "07"
MOD_TIME = f"{MOD_YEAR}-{MOD_MONTH}-{MOD_DAY}"
MONTH_SET_ONE = ['01', '03', '05', '07', '08', '10', '12']
MONTH_SET_TWO = ['04', '06', '09', '11']
TIME_PASSAGE = "future"
CURRENT_YEAR = datetime.today().year
OLDEST_YEAR = CURRENT_YEAR - 25

# PRE-CHECKS
def is_valid_dir(from_dir, to_dir):
    if not os.path.exists(from_dir) or not os.path.exists(to_dir):
        raise ValueError("Please check to make sure you have provided valid directories for migration.")
    return print(f"DIRECTORIES [{from_dir}] AND [{to_dir}] ARE VALID")

def is_valid_mod_time(mod_time):
    overall_error_statement = "The set date is not valid."
    order_error_statement = "Please make sure the date is properly formatted with the proper order: YEAR-MONTH-DAY" # Will be omitted once UI is up and running
    day_error_statement = "Day is not a valid day. Please insert a day within the month."
    month_error_statement = "Month is not a valid month. Please insert a month within 01 and 12."
    year_error_statement = f"Year is not a valid year. Please insert a year within {OLDEST_YEAR} and {CURRENT_YEAR}."
    mod_parts = mod_time.split('-')

    # Checks
    if not len(mod_parts) == 3:
        raise TypeError(order_error_statement)
    
    if len(mod_parts[0]) != 4 or not (OLDEST_YEAR <= int(mod_parts[0]) <= CURRENT_YEAR):
        raise ValueError(f"{overall_error_statement} {year_error_statement}")
    
    if len(mod_parts[1]) != 2 and (12 <= int(mod_parts[1]) <= 1):
        raise ValueError(f"{overall_error_statement} {month_error_statement}")
    
    if int(mod_parts[1]) in MONTH_SET_ONE and not (31 <= int(mod_parts[2]) <= 1): 
        raise ValueError(f"{overall_error_statement} {day_error_statement}")
    
    if int(mod_parts[1]) in MONTH_SET_TWO and not (30 <= int(mod_parts[2]) <= 1):
        raise ValueError(f"{overall_error_statement} {day_error_statement}")
    
    if int(mod_parts[0]) % 4 == 0 and int(mod_parts[1]) == 2 and not (29 <= int(mod_parts[2]) <= 1):
        raise ValueError(f"{overall_error_statement} {day_error_statement}")
    
    if int(mod_parts[0]) % 4 != 0 and int(mod_parts[1]) == 2 and not (28 <= int(mod_parts[2]) <= 1):
        raise ValueError(f"{overall_error_statement} {day_error_statement}")
    
    return print(f"MOD TIME [{mod_time}] IS VALID")
    
def is_valid_time_passage(time_passage):
    if  not (time_passage == "" or 
        time_passage == "past" or 
        time_passage == "present" or 
        time_passage == "future"):
        raise ValueError(f"{time_passage} is not a proper reference of time. Please input a proper time passage: \"past,\" \"present,\" or \"future.\"")
    return print(f"TIME PASSAGE [{time_passage}] IS VALID")

# TOOLS
def file_migration(from_dir, to_dir, filetypes, move = False, mod_time = '', time_passage = ''):
    # Calling pre-checks
    is_valid_dir(from_dir = from_dir, to_dir = to_dir)
    if mod_time:
        is_valid_mod_time(mod_time)
    if time_passage:
        is_valid_time_passage(time_passage)

    def move_or_copy_files(files = [], move = False):
        if not files:
            print("No files to move or copy. No changes made.")
        if move:
            for file in files:
                print(f"MOVING {file}")
                shutil.move(file, to_dir)
                print("MOVE COMPLETE\n")
            print("MOVING PROCESS COMPLETE")
            return
        else:
            for file in files:
                print(f"COPYING {file}")
                shutil.copy(file, to_dir)
                print("COPY COMPLETE\n")
            print("n\COPYING PROCESS COMPLETE")
            return

    def time_relative_migration(files, mod_time, time_passage, move = False):
        file_and_mod_time = []
        mod_time = int(mod_time.replace('-', ''))
        file_time_values = []
        for file in files:
            raw_mod_time = os.path.getmtime(file) 
            new_mod_time = (int(str(datetime.fromtimestamp(raw_mod_time))[:10].replace('-', '')))
            file_and_mod_time.append([file, new_mod_time])

        for pair in file_and_mod_time:
            if time_passage == 'past':
                if pair[1] <= mod_time:
                    if move:
                        move_or_copy_files(pair[0], move = True)
                    else:
                        move_or_copy_files(pair[0])
            if time_passage == 'present':
                if pair[1] == mod_time:
                    if move:
                        move_or_copy_files(pair[0], move = True)
                    else:
                        move_or_copy_files(pair[0])
            if time_passage == 'future':
                if pair[1] >= mod_time:
                    if move:
                        move_or_copy_files(pair[0], move = True)
                    else:
                        move_or_copy_files(pair[0])
        return

    def size_relative_migration(files, file_min_max = [], move = False):
        # based on minmax list, move or copy files
        return

    time_passage = time_passage.replace("-", "")
    upper_list = []
    sub_files = []

    for filetype in filetypes:
        upper_filetype = filetype.upper()
        upper_list.append(filetype.upper())
    
    for upper_filetype in upper_list:
        filetypes.append(upper_filetype)

    for item in os.walk(from_dir):
        for file in item[2]:
            for filetype in filetypes:
                if file.endswith(filetype):
                    sub_files.append(f'{item[0]}\\{file}')

    if mod_time: # add choice to move or copy
        time_relative_migration(sub_files, mod_time, time_passage, move)
        return

    else:
        if move:
            move_or_copy_files(sub_files, move)
            return
        move_or_copy_files(sub_files)
        return
    

if __name__ == "__main__":
    file_migration(FROM_DIR, TO_DIR, FILETYPES)

# MAJOR FLAW - If user wants to have multiple parameters, multiple functions would be called.
# Try to find a work around. Probably going to need to reroute code structure and move away from individual
# funcs per parm

# ADD this functionality - need to check if file already exists in TO_DIR. If so, maybe just skip over the file?
# Should probably inform the user and maybe pause the code somehow to let the user rebuttal

# MAJOR FLAW II - if two files have the same name, whichever is first moved/copied is the only one
# to do so. The other is ignored.