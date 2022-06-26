import glob
import os
from pathlib import Path

ids_list = [4375,244,245,4368,4367,4785]
for ids in ids_list:
    replaced_content = ""
    filePath = 'provinces/' + str(ids) + ' -*.txt'
    fileName = glob.glob(filePath)
    if len(fileName) > 0:
        file = open(fileName[0], "r")
        print("Looking at file: " + fileName[0])
        for line in file:
            line = line.strip()

            if "owner = ENG" in line:
                new_line = "owner = NOL"
            elif "add_core = ENG" in line:
                new_line = "add_core = NOL"
            elif "controller = ENG" in line:
                new_line = "controller = NOL"
            else:
                new_line = line

            replaced_content = replaced_content + new_line + "\n"

        file.close()

        write_file = open(fileName[0], "w")
        write_file.write(replaced_content)
        write_file.close()
