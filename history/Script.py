import glob
import os
from pathlib import Path

ids_list = [4255,301,1778,1754,4254,1956,4147,4253,295,4251,296,4116,300,4252,307,4263]
for ids in ids_list:
    replaced_content = ""
    filePath = 'provinces/' + str(ids) + ' -*.txt'
    fileName = glob.glob(filePath)
    if len(fileName) > 0:
        file = open(fileName[0], "r")
        print("Looking at file: " + fileName[0])
        for line in file:
            line = line.strip()

            if "owner = RUS" in line:
                new_line = "owner = MOS"
            elif "add_core = MOS" in line:
                new_line = "add_core = MOS\nadd_core = RUS"
            elif "controller = RUS" in line:
                new_line = "controller = MOS"
            else:
                new_line = line

            replaced_content = replaced_content + new_line + "\n"

        file.close()

        write_file = open(fileName[0], "w")
        write_file.write(replaced_content)
        write_file.close()
