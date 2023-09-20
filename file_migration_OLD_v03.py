import os
from datetime import date, datetime
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

MOD_YEAR = "2023"
MOD_MONTH = "09"
MOD_DAY = "07"
MOD_TIME = f"{MOD_YEAR}-{MOD_MONTH}-{MOD_DAY}"
MONTH_SET_ONE = ['01', '03', '05', '07', '08', '10', '12']
MONTH_SET_TWO = ['04', '06', '09', '11']
TIME_PASSAGE = "future"
CURRENT_YEAR = datetime.today().year
OLDEST_YEAR = 2000


# PRE-CHECKS
def is_valid_dir(from_dir, to_dir):
    if not os.path.exists(from_dir) or not os.path.exists(to_dir):
        raise ValueError("Please check to make sure you have provided valid directories for migration.")
    return print("Directory is VALID")

def is_valid_mod_time(mod_time):
    overall_error_statement = "The set date is not valid."
    order_error_statement = "Please make sure the date is properly formatted with the proper order: YEAR-MONTH-DAY" # Will be omitted once UI is up and running
    day_error_statement = "Day is not a valid day. Please insert a day within the month."
    month_error_statement = "Month is not a valid month. Please insert a month within 01 and 12."
    year_error_statement = f"Year is not a valid year. Please insert a year within {OLDEST_YEAR} and {CURRENT_YEAR}."
    mod_parts = mod_time.split('-')
    if not len(mod_parts) == 3:
        raise TypeError(order_error_statement)
    
    if len(mod_parts[0]) != 4 or not (CURRENT_YEAR <= int(mod_parts[0]) <= OLDEST_YEAR):
        raise ValueError(f"{overall_error_statement} {year_error_statement}")
    
    if len(mod_parts[1]) != 2 and (12 <= int(mod_parts[1]) <= 1):
        raise ValueError(f"{overall_error_statement} {month_error_statement}")
    
    if int(mod_parts[1]) in MONTH_SET_ONE and not (31 <= int(mod_parts[2]) <= 1): 
        raise ValueError(f"{overall_error_statement} {day_error_statement}")
    
    if int(mod_parts[1]) in MONTH_SET_TWO and not (30 <= int(mod_parts[2]) <= 1):
        raise ValueError(f"{overall_error_statement} {day_error_statement}")
    
    if int(mod_parts[0]) % 4 == 0 and int(mod_parts[1]) == 2 and not (29 <= int(mod_parts[2]) <= 1):
        raise ValueError(f"{overall_error_statement} {day_error_statement}")
    
    if int(mod_parts[0]) % 4 == 0 and int(mod_parts[1]) == 2 and not (28 <= int(mod_parts[2]) <= 1):
        raise ValueError(f"{overall_error_statement} {day_error_statement}")
    
    return print("Mod time is VALID")
    
def is_valid_time_passage(time_passage):
    if (time_passage != "" or 
        time_passage != "past" or 
        time_passage != "present" or 
        time_passage != "future"):
        raise ValueError(f"{time_passage} is not a proper reference of time. Please input a proper time passage: \"past,\" \"present,\" or \"future.\"")
    return print("Time passage is VALID.")

# TOOLS
def file_migration(from_dir, to_dir, filetypes, move = False, mod_time = False, time_passage):
    # Calling pre-checks
    is_valid_dir()
    is_valid_mod_time()
    is_valid_time_passage()

    time_passage = time_passage.replace("-", "")
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
                if not sub_data.endswith(filetype):
                    return
                for sub_dir in sub_dirs:
                    if not os.path.isfile(f'{sub_dir}\{sub_data}'):
                        return
                    if MOD_TIME and time_passage == "past":

                    if move:     
                        print(f"MOVING \"{sub_dir}\{sub_data}\" NOW")
                        shutil.move(f'{sub_dir}\{sub_data}', TO_DIR)
                        print("MOVING COMPLETE")
                    else:
                        print(f"COPYING \"{sub_dir}\{sub_data}\" NOW")
                        shutil.copy(f'{sub_dir}\{sub_data}', TO_DIR)
                        print("COPYING COMPLETE")

if __name__ == "__main__":
    file_migration(FROM_DIR, TO_DIR, FILETYPES, mod_time = MOD_TIME, time_passage = TIME_PASSAGE)