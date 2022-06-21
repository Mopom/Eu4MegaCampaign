import glob
import os
from pathlib import Path

ids_list = list(range(1, 4940, 1))
for ids in ids_list:
    replaced_content = ""
    filePath = 'provinces/' + str(ids) + ' -*.txt'
    fileName = glob.glob(filePath)
    if len(fileName) > 0:
        file = open(fileName[0], "r")
        print("Changing file: " + fileName[0])
        for line in file:
            line = line.strip()

            if "owner = Z03" in line:
                new_line = "controller = UBL"
            elif "add_core = Z03" in line:
                new_line = "add_core = UBL"
            else:
                new_line = line

            replaced_content = replaced_content + new_line + "\n"

        file.close()

        write_file = open(fileName[0], "w")
        write_file.write(replaced_content)
        write_file.close()
