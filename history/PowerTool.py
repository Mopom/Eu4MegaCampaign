import PySimpleGUI as sg
import glob
import os
from pathlib import Path

superregions = []
regions = []
areas = []
folder = ''
modfolder = ''
provinceFiles = []

superregionsdict = {}
regionsdict = {}
areasdict = {}

finalIdList = []

filtre = ""
entry = ""
province = ""

layout = [
    [sg.Text("EU4 Base Game Folder", size=(17, 1)), sg.In(size=(36, 4), enable_events=True, key="-FOLDER-"), sg.FolderBrowse()],
    [sg.Text('Super Regions', size=(12, 1), justification='left'), sg.Combo(superregions, size=(20, 4), expand_x=True, readonly=True, enable_events=True, key='-SRLIST-')],
    [sg.Text('Regions', size=(12, 1), justification='left'), sg.Combo(regions, size=(20, 4), expand_x=True, readonly=True, enable_events=True, key='-RLIST-')],
    [sg.Text('Areas', size=(12, 1), justification='left'), sg.Combo(areas, size=(20, 4), expand_x=True, readonly=True, enable_events=True, key='-ALIST-')],
    [sg.Text('Currently selected Ids', justification='center')],
    [sg.Multiline(finalIdList, disabled=True, enable_events=True, key='-IDLIST-', expand_x=True, expand_y=True, justification='left')],
    [sg.Text('Adding or Removing Singles Provinces', justification='center')],
    [sg.Input(province, enable_events=True, key='-PROVINCE-', expand_x=True, justification='left')],
    [sg.Button("ADD PROVINCE TO LIST"), sg.Button("REMOVE PROVINCE FROM LIST")],
    [sg.Text('Additionnal Province Filter', justification='center')],
    [sg.Input(filtre, enable_events=True, key='-FILTER-', expand_x=True, justification='left')],
    [sg.Text('Entry to remove or add', justification='center')],
    [sg.Input(entry, enable_events=True, key='-ENTRY-', expand_x=True, justification='left')],
    [sg.Text("Mod Folder", size=(17, 1)), sg.In(size=(36, 4), enable_events=True, key="-MODFOLDER-"), sg.FolderBrowse()],
    [sg.Button("ADD"), sg.Button("REMOVE")],
    [sg.Button("EXIT")]
]

# Create the window
window = sg.Window("Mass Province Editor", layout, margins=(200, 200))

# Create an event loop
while True:
    event, values = window.read()
    if event == "-FOLDER-":
        folder = values["-FOLDER-"] + "/map/"
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            print("Wrong folder somehow... Please try something different!")
            file_list = [] #TODO: complain here

        for file in file_list:
            extendDict = False
            tmpStorage = []
            if file == "superregion.txt":
                text = open(os.path.join(folder, file), "r")
                print("Looking at superregions")
                for line in text:
                    if "= {" in line:
                        superregions.append(line.split(" =")[0])
                        extendDict = True
                    elif "}" in line:
                        extendDict = False
                        superregionsdict[superregions[-1]] = tmpStorage
                        tmpStorage = []
                    elif extendDict:
                        tmpStorage.append(line.strip())
                text.close()
                window["-SRLIST-"].update(values=superregions, value='')
            elif file == "region.txt":
                text = open(os.path.join(folder, file), "r")
                print("Looking at regions")
                for line in text:
                    if "region = {" in line:
                        regions.append(line.split(" =")[0])
                        extendDict = True
                    elif "}" in line and extendDict:
                        regionsdict[regions[-1]] = tmpStorage
                        tmpStorage = []
                        extendDict = False
                    elif extendDict and "areas = {" not in line:
                        tmpStorage.append(line.strip())
                text.close()
                window["-RLIST-"].update(values=regions, value='')
            elif file == "area.txt":  # apacherian area not working for some god forsaken reason
                text = open(os.path.join(folder, file), "r")
                print("Looking at areas")
                for line in text:
                    if "{" in line and "color" not in line:
                        areas.append(line.split(" =")[0])
                        extendDict = True
                    elif "}" in line and "color" not in line:
                        extendDict = False
                        areasdict[areas[-1]] = tmpStorage
                        tmpStorage = []
                    elif extendDict and "color" not in line:
                        tmpStorage.extend(line.strip().split(' '))
                text.close()
                window["-ALIST-"].update(values=areas, value='')
    elif event == "-MODFOLDER-":
        modfolder = values["-MODFOLDER-"] + "/history/provinces/"
        try:
            # Get list of files in folder
            provinceFiles = os.listdir(modfolder)
        except:
            print("Wrong folder somehow... Please try something different!")
            provinceFiles = [] #TODO: complain here
    elif event == "-SRLIST-":
        print("Super region selection was changed.")
        finalIdList = []
        tmpRegionList = []
        tmpAreaList = []
        for region in superregionsdict[values["-SRLIST-"]]:
            if region != '' and '#' not in region and region in regionsdict:
                tmpRegionList.append(region)
                for area in regionsdict[region]:
                    if area != '' and '#' not in area and area in areasdict:
                        tmpAreaList.append(area)
                        for prov in areasdict[area]:
                            if prov != '' and '#' not in prov:
                                finalIdList.append(prov)
        window["-RLIST-"].update(values=tmpRegionList, value='')
        window["-ALIST-"].update(values=tmpAreaList, value='')
        window["-IDLIST-"].update(finalIdList)
    elif event == "-RLIST-":
        print("Region selection was changed.")
        finalIdList = []
        tmpAreaList = []
        for area in regionsdict[values["-RLIST-"]]:
            if area != '' and '#' not in area and area in areasdict:
                tmpAreaList.append(area)
                for prov in areasdict[area]:
                    if prov != '' and '#' not in prov:
                        finalIdList.append(prov)
        window["-ALIST-"].update(values=tmpAreaList, value='')
        window["-IDLIST-"].update(finalIdList)
    elif event == "-ALIST-":
        print("Area selection was changed.")
        finalIdList = []
        for prov in areasdict[values["-ALIST-"]]:
            if prov != '' and '#' not in prov:
                finalIdList.append(prov)
        window["-IDLIST-"].update(finalIdList)
    elif event == "-IDLIST-":
        print("Id List was changed.")
        finalIdList = values["-IDLIST-"]
        window["-IDLIST-"].update(values["-IDLIST-"])
    elif event == "-PROVINCE-":
        print("A province to add or remove to the list.")
        province = values["-PROVINCE-"]
        window["-PROVINCE-"].update(values["-PROVINCE-"])
    elif event == "ADD PROVINCE TO LIST":
        print("Province " + province + " will be added to the list.")
        finalIdList.append(province)
        window["-IDLIST-"].update(finalIdList)
    elif event == "REMOVE PROVINCE FROM LIST":
        print("Province " + province + " will be removed from the list.")
        try:
            finalIdList.remove(province)
        except:
            print("No province with that id in the list!!!!")
        window["-IDLIST-"].update(finalIdList)
    elif event == "-FILTER-":
        print("Will only modify provinces with that specific entry.")
        filtre = values["-FILTER-"]
        window["-FILTER-"].update(values["-FILTER-"])
    elif event == "-ENTRY-":
        print("Will modify provinces by adding or removing that specific entry.")
        entry = values["-ENTRY-"]
        window["-ENTRY-"].update(values["-ENTRY-"])
    elif event == "ADD":
        print("Adding entry to all selected provinces.")
        for file in provinceFiles:
            if file.split("-")[0].strip() in finalIdList:
                modify = False
                done = False
                replaced_content = ""
                text = open(os.path.join(modfolder, file), "r")
                print("Looking at province " + file)
                for line in text:
                    if ("base_manpower" in line or "discovered_by" in line) and not done:
                        replaced_content = replaced_content + line + entry + "\n"
                        done = True
                    else:
                        replaced_content = replaced_content + line

                    if filtre in line or filtre == "":
                        modify = True

                text.close()

                if modify:
                    write_file = open(os.path.join(modfolder, file), "w")
                    write_file.write(replaced_content)
                    write_file.close()
    elif event == "REMOVE":
        print("Removing entry from all selected provinces.")
        for file in provinceFiles:
            if file.split("-")[0].strip() in finalIdList:
                modify = False
                replaced_content = ""
                text = open(os.path.join(modfolder, file), "r")
                print("Looking at province " + file)
                for line in text:
                    if entry not in line:
                        replaced_content = replaced_content + line

                    if filtre in line or filtre == "":
                        modify = True

                text.close()

                if modify:
                    write_file = open(os.path.join(modfolder, file), "w")
                    write_file.write(replaced_content)
                    write_file.close()
    # End program if user closes window or presses the EXIT button
    elif event == "EXIT" or event == sg.WIN_CLOSED:
        print("Goodbye.")
        break

window.close()
