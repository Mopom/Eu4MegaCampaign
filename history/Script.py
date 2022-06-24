import glob
import os
from pathlib import Path

ids_list = [4711,71,4715,4718,79,66,67,4716,4717]
for ids in ids_list:
    replaced_content = ""
    filePath = 'provinces/' + str(ids) + ' -*.txt'
    fileName = glob.glob(filePath)
    if len(fileName) > 0:
        file = open(fileName[0], "r")
        print("Looking at file: " + fileName[0])
        for line in file:
            line = line.strip()

            if "owner = Z02" in line:
                new_line = "owner = FKN"
            elif "add_core = Z02" in line:
                new_line = "add_core = FKN"
            elif "controller = Z02" in line:
                new_line = "controller = FKN"
            else:
                new_line = line

            replaced_content = replaced_content + new_line + "\n"

        file.close()

        write_file = open(fileName[0], "w")
        write_file.write(replaced_content)
        write_file.close()
