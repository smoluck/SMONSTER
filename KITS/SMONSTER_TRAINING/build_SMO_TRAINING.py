import os
from os import mkdir
from pathlib import Path
from shutil import rmtree
from zipfile import ZipFile, ZIP_DEFLATED

import utilssmotraining

###### SMONSTER BASE STRUCTURE
from utilssmotraining import midheader
from utilssmotraining import midroot
from utilssmotraining import midlxserv
from utilssmotraining import midtraining

from utilssmotraining import midmessage

# Get the root path to this repo
repo_dir = Path(__file__).parent

# Get the kit directory
kit_name = "SMONSTER_TRAINING"
kit_dir = repo_dir
# target_kit = kit_dir / "SMONSTER"

kit_files = []
lxserv_dir = kit_dir / "lxserv"
training_dir = kit_dir / "TRAINING_SCENES"

# Get the build directory
build_dir = repo_dir / "build"
# Get the license file
license_file = repo_dir / "LICENSE"


###### SMONSTER BASE STRUCTURE #########################################################
# root files are the txt files (README.txt ReadmeFirst_SMONSTER.txt UpdateLog.txt) and index.cfg
def root_fi():
    # Get Base files in folders "Config" "scripts" "TRAINING_SCENES" and make sure no pyc files come along
    root_files = []
    files = [f for f in os.listdir(kit_dir) if f.endswith((".cfg", ".txt", "LICENSE"))]
    for f in files:
        f = kit_dir / f
        root_files.append(f)
    print("Files in root folder:")
    print(root_files)
    print("--------------")
    return root_files
# root_fi()


# Files contained in the "lxserv" folder
def lxserv_fi():
    lxserv_files = [f for f in lxserv_dir.glob("**/*") if f.is_file() and not f.name.endswith(".pyc")]
    print("Files in lxserv folder:")
    print(lxserv_files)
    print("--------------")
    # for f in lxserv_files:
    #     kit_files.append(lxserv_files)
    return lxserv_files
# lxserv_fi()


# Files contained in the "TRAINING_SCENES" folder
def training_fi():
    # Get Base files in folders "Config" "scripts" "TRAINING_SCENES" and make sure no pyc files come along
    training_files = [f for f in training_dir.glob("**/*") if f.is_file() and not f.name.endswith(".pyc")]
    print(training_files)
    # clean_training_files = []
    # blacklistedstring = "SMO_AI_TOOLS"
    # for f in training_files:
    #     if training_files.find(blacklistedstring) == False:
    #         clean_training_files.append(f)
    return training_files
# training_fi()


# del lxserv_files[:]



# Clear the build directory
if build_dir.exists():
    rmtree(build_dir)
# Remake the build directory
mkdir(build_dir)

# Format the lpk file name with the version number from the VERSION file
version = utilssmotraining.get_version()
lpk_source_path = build_dir / f"SMONSTER_TRAINING_v{version}.lpk"
# Message to display to the users
message = f"You successfully installed SMONSTER TRAINING Kit: v{version} &#10;Please refer to the README.url for more information. &#10;Remember to join our dedicated Slack server for support and updates.&#10; &#10;Best regards,&#10;Franck Elisabeth&#10; &#10;"

# Build the LPK file.
with ZipFile(lpk_source_path, mode="w", compression=ZIP_DEFLATED) as lpk:
    index_data = []
    index_data_slash = []
    # Add the license
    # lpk.write(license_file, "license")
    # Generate the index.xml file data
    indexheader = midheader(name=kit_name)

    ###### SMONSTER BASE STRUCTURE
    print("----- Copy Root Data -----")
    indexroot = midroot(folder=kit_dir, files=root_fi())

    print("----- Copy Root/lxserv Folder Data -----")
    indexlxserv = midlxserv(folder=kit_dir, files=lxserv_fi())

    print("----- Copy Root/TRAINING_SCENE Folder Data -----")
    indextraining = midtraining(folder=kit_dir, files=training_fi())

    ###### MESSAGE
    indexmessage = midmessage(info=message)

    index_data_base = (indexheader + indexroot + indexlxserv + indextraining)

    index_data = (index_data_base + indexmessage)

    # print("--")
    # print("----------------")
    # print("-------------------------------")
    # print("----- Resulting INDEX.XML -----")
    # print(index_data)
    # print("-------------------------------")
    # print("----------------")
    # print("--")

    print("--")
    print("----------------")
    print("-------------------------------")
    print("----- Resulting INDEX.XML (with Forward Slash) -----")
    # Convert String path to Absolute Path using OS formatting
    index_data_slash = index_data.replace('\\', '/')
    print(index_data_slash)
    print("-------------------------------")
    print("----------------")
    print("--")

    # Write the index.xml file
    # lpk.writestr("index.xml", index_data)
    lpk.writestr("index.xml", index_data_slash)

    # Write all file into the lpk
    print("----- Root files -----")
    for file in root_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- lxserv Folder files -----")
    for file in lxserv_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- TRAINING_SCENE Folder files -----")
    for file in training_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    lpk.close()

