import os
from os import mkdir
from pathlib import Path
from shutil import rmtree
from zipfile import ZipFile, ZIP_DEFLATED

import utilssmonster

###### SMONSTER BASE STRUCTURE 
from utilssmonster import midheader
from utilssmonster import midroot
from utilssmonster import midconfig
from utilssmonster import midscripts
from utilssmonster import midlxserv
from utilssmonster import midsmodule
from utilssmonster import midtraining

###### STANDARD KITS
from utilssmonster import midkits
from utilssmonster import midkitai
from utilssmonster import midkitbake
from utilssmonster import midkitbatch
from utilssmonster import midkitcad
from utilssmonster import midkitcleanup
from utilssmonster import midkitcb
from utilssmonster import midkitdoc
from utilssmonster import midkitgc
from utilssmonster import midkitmaster
from utilssmonster import midkitmath
from utilssmonster import midkitmeshops
from utilssmonster import midkitmifaboma
from utilssmonster import midkitpcloud
from utilssmonster import midkitqtag
from utilssmonster import midkituv
from utilssmonster import midkitvenom

###### LIVELINK KITS 
from utilssmonster import midkitllmarmo
from utilssmonster import midkitllpixa
from utilssmonster import midkitllrizom

from utilssmonster import midmessage

# Get the root path to this repo
repo_dir = Path(__file__).parent

# Get the kit directory
kit_name = "SMONSTER_V3"
kit_dir = repo_dir
# target_kit = kit_dir / "SMONSTER"

kit_files = []
config_dir = kit_dir / "Config"
scripts_dir = kit_dir / "scripts"
smodule_dir = kit_dir / "smodule"
lxserv_dir = kit_dir / "lxserv"
training_dir = kit_dir / "TRAINING_SCENES"

###### STANDARD KITS 
kitsfolders_dir = kit_dir / "Kits"

kit_ai_dir = kitsfolders_dir / "SMO_AI_TOOLS"
kit_bake_dir = kitsfolders_dir / "SMO_BAKE"
kit_batch_dir = kitsfolders_dir / "SMO_BATCH"
kit_cad_dir = kitsfolders_dir / "SMO_CAD_TOOLS"
kit_cleanup_dir = kitsfolders_dir / "SMO_CLEANUP"
kit_cb_dir = kitsfolders_dir / "SMO_COLOR_BAR"
kit_doc_dir = kitsfolders_dir / "SMO_DOC"
kit_gc_dir = kitsfolders_dir / "SMO_GAME_CONTENT"
kit_master_dir = kitsfolders_dir / "SMO_MASTER"
kit_math_dir = kitsfolders_dir / "SMO_MATH_TOOLS"
kit_meshops_dir = kitsfolders_dir / "SMO_MESHOPS"
kit_mifaboma_dir = kitsfolders_dir / "SMO_MIFABOMA"
kit_pcloud_dir = kitsfolders_dir / "SMO_PCLOUD_XYZ"
kit_qt_dir = kitsfolders_dir / "SMO_QUICK_TAG"
kit_uv_dir = kitsfolders_dir / "SMO_UV"
kit_venom_dir = kitsfolders_dir / "SMO_VENOM"

###### LIVELINK KITS 
kit_marmo_dir = kitsfolders_dir / "SMO_MARMOSET_LIVELINK"
kit_pixa_dir = kitsfolders_dir / "SMO_PIXAFLUX_LIVELINK"
kit_rizom_dir = kitsfolders_dir / "SMO_RIZOMUV_LIVELINK"

# Get the build directory
build_dir = repo_dir / "build_StandardEdition"
# Get the license file
license_file = repo_dir / "LICENSE"


###### SMONSTER BASE STRUCTURE #########################################################
# root files are the txt files (README.txt ReadmeFirst_SMONSTER.txt UpdateLog.txt) and index.cfg
def root_fi():
    # Get Base files in folders "Config" "scripts" "TRAINING_SCENES" and make sure no pyc files come along
    root_files = []
    files = [f for f in os.listdir(kit_dir) if f.endswith((".cfg", ".txt", ".url", "LICENSE"))]
    for f in files:
        f = kit_dir / f
        root_files.append(f)
    print("Files in root folder:")
    print(root_files)
    print("--------------")
    return root_files
# root_fi()


# Files contained in the "Config" folder
def config_fi():
    # Get Base files in folders "Config" and make sure no pyc files come along
    config_files = [f for f in config_dir.glob("**/*") if f.is_file() and not f.name.endswith(".pyc")]
    print(config_files)
    return config_files
# config_fi()


# Files contained in the "scripts" folder
def scripts_fi():
    # Get Base files in folders "scripts"and make sure no pyc files come along
    scripts_files = [f for f in scripts_dir.glob("**/*") if f.is_file() and not f.name.endswith(".pyc")]
    print(scripts_files)
    return scripts_files
# scripts_fi()


# Files contained in the "smodule" folder
def smodule_fi():
    smodule_files = [f for f in smodule_dir.glob("**/*") if f.is_file() and not f.name.endswith(".pyc")]
    print(smodule_files)
    return smodule_files
# smodule_fi()


# Files contained in the "lxserv" folder
def lxserv_fi():
    lxserv_files = []
    for f in lxserv_dir.glob("**/*"):
        # Files that are compiled
        if f.is_file() and f.name.endswith(".pyc"):
            if not f.name.startswith(("SMO_SMONSTER_", "averageRGBA.pyc", "createBBOX.pyc", "islandCount.pyc", "randomRGBA.pyc", "renamePTag.pyc", "resetMeshTransform.pyc", "selectByColor.pyc", "SplitByMaterial.pyc")):
                lxserv_files.append(f)
        # Files that must be compiled on user Device because of OS dependency
        if f.is_file() and f.name.endswith(".py"):
            if f.name.startswith("SMO_SMONSTER_"):
                lxserv_files.append(f)
            # Files that are from 3rd party codes
            if f.name.endswith("averageRGBA.py") or f.name.endswith("createBBOX.py") or f.name.endswith(
                    "islandCount.py") or f.name.endswith("randomRGBA.py") or f.name.endswith(
                    "renamePTag.py") or f.name.endswith("resetMeshTransform.py") or f.name.endswith(
                    "selectByColor.py"):
                lxserv_files.append(f)
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


###### STANDARD KITS #########################################################
# root files are the txt files (README.txt ReadmeFirst_SMONSTER.txt UpdateLog.txt) and index.cfg
def kits_fi():
    # Get Base files in folders "Config" "scripts" "TRAINING_SCENES" and make sure no pyc files come along
    kits_files = []
    files = [f for f in os.listdir(kitsfolders_dir) if f.endswith(".txt")]
    for f in files:
        f = kitsfolders_dir / f
        kits_files.append(f)
    print("Files in Kits folder root:")
    print(kits_files)
    print("--------------")
    return kits_files
# kits_fi()

# Files contained in "Kits/SMO_AI" folder
def kit_ai_fi():
    kitAI_files = [f for f in kit_ai_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitAI_files)
    return kitAI_files
# kitAI_fi()

# Files contained in "Kits/SMO_BAKE" folder
def kit_bake_fi():
    kitBAKE_files = [f for f in kit_bake_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitBAKE_files)
    return kitBAKE_files
# kit_bake_fi()

# Files contained in "Kits/SMO_BATCH" folder
def kit_batch_fi():
    kitBATCH_files = [f for f in kit_batch_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitBATCH_files)
    return kitBATCH_files
# kit_batch_fi()

# Files contained in "Kits/SMO_CAD_TOOLS" folder
def kit_cad_fi():
    kitCAD_files = [f for f in kit_cad_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitCAD_files)
    return kitCAD_files
# kit_cad_fi()

# Files contained in "Kits/SMO_CLEANUP" folder
def kit_cleanup_fi():
    kitCLEANUP_files = [f for f in kit_cleanup_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitCLEANUP_files)
    return kitCLEANUP_files
# kit_cleanup_fi()

# Files contained in "Kits/SMO_COLOR_BAR" folder
def kit_colorbar_fi():
    kitCB_files = [f for f in kit_cb_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitCB_files)
    return kitCB_files
# kit_colorbar_fi()

# Files contained in "Kits/SMO_DOC" folder
def kit_doc_fi():
    kitDOC_files = [f for f in kit_doc_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitDOC_files)
    return kitDOC_files
# kit_doc_fi()

# Files contained in "Kits/SMO_GAME_CONTENT" folder
def kit_gamecontent_fi():
    kitGC_files = [f for f in kit_gc_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitGC_files)
    return kitGC_files
# kit_gamecontent_fi()

# Files contained in "Kits/SMO_MASTER" folder
def kit_master_fi():
    kitMASTER_files = [f for f in kit_master_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitMASTER_files)
    return kitMASTER_files
# kit_master_fi()

# Files contained in "Kits/SMO_MATH_TOOLS" folder
def kit_mathtools_fi():
    kitMATH_files = [f for f in kit_math_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitMATH_files)
    return kitMATH_files
# kit_mathtools_fi()

# Files contained in "Kits/SMO_MESHOPS" folder
def kit_meshops_fi():
    kitMESHOPS_files = [f for f in kit_meshops_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitMESHOPS_files)
    return kitMESHOPS_files
# kit_meshops_fi()

# Files contained in "Kits/SMO_MIFABOMA" folder
def kit_mifaboma_fi():
    kitMIFABOMA_files = [f for f in kit_mifaboma_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitMIFABOMA_files)
    return kitMIFABOMA_files
# kit_mifaboma_fi()

# Files contained in "Kits/SMO_PCLOUD_XYZ" folder
def kit_pcloud_fi():
    kitPCLOUD_files = [f for f in kit_pcloud_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitPCLOUD_files)
    return kitPCLOUD_files
# kitPCLOUD_fi()

# Files contained in "Kits/SMO_QUICK_TAG" folder
def kit_qtag_fi():
    kitQTAG_files = [f for f in kit_qt_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitQTAG_files)
    return kitQTAG_files
# kit_qtag_fi()

# Files contained in "Kits/SMO_UV" folder
def kit_uv_fi():
    kitUV_files = [f for f in kit_uv_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitUV_files)
    return kitUV_files
# kit_uv_fi()

# Files contained in "Kits/SMO_VENOM" folder
def kit_venom_fi():
    kitVENOM_files = [f for f in kit_venom_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc"))]
    print(kitVENOM_files)
    return kitVENOM_files
# kit_venom_fi()


###### LIVELINK KITS #########################################################
# Files contained in "Kits/SMO_MARMOSET_LIVELINK" folder
def kit_ll_marmosettoolbag_fi():
    # Files that doesn't include the source code py files, but only the one that remains to the KeymapCommander and Startup scripts.
    kitLLMARMO_files = [f for f in kit_marmo_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc", "SMO_LL_MARMOSET_AutoSegmentedExport_Cmd.py", "SMO_LL_MARMOSET_CreateMikkTangentBasisMap_Cmd.py", "SMO_LL_MARMOSET_ExportFBXBakes_Cmd.py", "SMO_LL_MARMOSET_SetExePath_Cmd.py"))]
    print("Files in Marmoset Toolbag LL kit folder:")
    print(kitLLMARMO_files)
    print("--------------")
    return kitLLMARMO_files
# kit_ll_marmosettoolbag_fi()

# Files contained in "Kits/SMO_PIXAFLUX_LIVELINK" folder
def kit_ll_pixaflux_fi():
    # Files that doesn't include the source code py files, but only the one that remains to the KeymapCommander and Startup scripts.
    kitLLPIXA_files = [f for f in kit_pixa_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc", "SMO_LL_PIXAFLUX_CreateTSNMap_Cmd.py", "SMO_LL_PIXAFLUX_DupAndExplodeByDist_Cmd.py", "SMO_LL_PIXAFLUX_ScaleUniformRecenter_Cmd.py", "SMO_LL_PIXAFLUX_SendDataAuto_Cmd.py", "SMO_LL_PIXAFLUX_SetExePath_Cmd.py"))]
    print("Files in Pixaflux LL kit folder:")
    print(kitLLPIXA_files)
    print("--------------")
    return kitLLPIXA_files
# kit_ll_pixaflux_fi()

# Files contained in "Kits/SMO_RIZOMUV_LIVELINK" folder
def kit_ll_rizomuv_fi():
    # Files that doesn't include the source code py files, but only the one that remains to the KeymapCommander and Startup scripts.
    kitLLRIZOM_files = [f for f in kit_rizom_dir.glob("**/*") if f.is_file() and not f.name.endswith(("_KeymapCommander.pyc", "_Startup.pyc", "SMO_LL_RIZOMUV_Basic_Cmd.py", "SMO_LL_RIZOMUV_SendDataAuto_Cmd.py", "SMO_LL_RIZOMUV_SetExePath_Cmd.py"))]
    print("Files in RizomUV LL kit folder:")
    print(kitLLRIZOM_files)
    print("--------------")
    return kitLLRIZOM_files
# kit_ll_rizomuv_fi()


# del config_files[:]
# del scripts_files[:]
# del scene_files[:]
# del smodule_files[:]
# del lxserv_files[:]


# Clear the build directory
if build_dir.exists():
    rmtree(build_dir)
# Remake the build directory
mkdir(build_dir)

# Format the lpk file name with the version number from the VERSION file
version = utilssmonster.get_version()
lpk_standard_path = build_dir / f"SMONSTER_v{version}_StandardEdition.lpk"
# Message to display to the users
message = f"You successfully installed SMONSTER (Standard Edition): v{version} &#10;Please refer to the README.url for more information. &#10;Remember to join our dedicated Slack server for support and updates.&#10; &#10;Best regards,&#10;Franck Elisabeth&#10; &#10;"

# Build the LPK file.
with ZipFile(lpk_standard_path, mode="w", compression=ZIP_DEFLATED) as lpk:
    index_data = []
    index_data_slash = []
    # Add the license
    lpk.write(license_file, "license")
    # Generate the index.xml file data
    indexheader = midheader(name=kit_name)

    ###### SMONSTER BASE STRUCTURE
    print("----- Copy Root Data -----")
    indexroot = midroot(folder=kit_dir, files=root_fi())

    print("----- Copy Root/config Folder Data -----")
    indexconfig = midconfig(folder=kit_dir, files=config_fi())

    print("----- Copy Root/scripts Folder Data -----")
    indexscripts = midscripts(folder=kit_dir, files=scripts_fi())

    print("----- Copy Root/lxserv Folder Data -----")
    indexlxserv = midlxserv(folder=kit_dir, files=lxserv_fi())

    print("----- Copy Root/smodule Folder Data -----")
    indexsmodule = midsmodule(folder=kit_dir, files=smodule_fi())

    print("----- Copy Root/TRAINING_SCENE Folder Data -----")
    indextraining = midtraining(folder=kit_dir, files=training_fi())

    ###### STANDARD KITS
    print("----- Copy Root/Kits Files Data -----")
    indexkits = midkits(folder=kit_dir, files=kits_fi())

    print("----- Copy Root/Kits/SMO_AI_TOOLS Folder Data -----")
    indexAI = midkitai(folder=kit_dir, files=kit_ai_fi())

    print("----- Copy Root/Kits/SMO_BAKE Folder Data -----")
    indexBAKE = midkitbake(folder=kit_dir, files=kit_bake_fi())

    print("----- Copy Root/Kits/SMO_BATCH Folder Data -----")
    indexBATCH = midkitbatch(folder=kit_dir, files=kit_batch_fi())

    print("----- Copy Root/Kits/SMO_CAD Folder Data -----")
    indexCAD = midkitcad(folder=kit_dir, files=kit_cad_fi())

    print("----- Copy Root/Kits/SMO_CLEANUP Folder Data -----")
    indexCLEANUP = midkitcleanup(folder=kit_dir, files=kit_cleanup_fi())

    print("----- Copy Root/Kits/SMO_COLOR_BAR Folder Data -----")
    indexCB = midkitcb(folder=kit_dir, files=kit_colorbar_fi())

    print("----- Copy Root/Kits/SMO_DOC Folder Data -----")
    indexDOC = midkitdoc(folder=kit_dir, files=kit_doc_fi())

    print("----- Copy Root/Kits/SMO_GAME_CONTENT Folder Data -----")
    indexGC = midkitgc(folder=kit_dir, files=kit_gamecontent_fi())

    print("----- Copy Root/Kits/SMO_MASTER Folder Data -----")
    indexMASTER = midkitmaster(folder=kit_dir, files=kit_master_fi())

    print("----- Copy Root/Kits/SMO_MATH_TOOLS Folder Data -----")
    indexMATH = midkitmath(folder=kit_dir, files=kit_mathtools_fi())

    print("----- Copy Root/Kits/SMO_MESHOPS Folder Data -----")
    indexMESHOPS = midkitmeshops(folder=kit_dir, files=kit_meshops_fi())

    print("----- Copy Root/Kits/SMO_MIFABOMA Folder Data -----")
    indexMIFABOMA = midkitmifaboma(folder=kit_dir, files=kit_mifaboma_fi())

    print("----- Copy Root/Kits/SMO_PCLOUD_XYZ Folder Data -----")
    indexPCLOUD = midkitpcloud(folder=kit_dir, files=kit_pcloud_fi())

    print("----- Copy Root/Kits/SMO_QUICK_TAG Folder Data -----")
    indexQTAG = midkitqtag(folder=kit_dir, files=kit_qtag_fi())

    print("----- Copy Root/Kits/SMO_UV Folder Data -----")
    indexUV = midkituv(folder=kit_dir, files=kit_uv_fi())

    print("----- Copy Root/Kits/SMO_VENOM Folder Data -----")
    indexVENOM = midkitvenom(folder=kit_dir, files=kit_venom_fi())

    ###### LIVELINK KITS
    print("----- Copy Root/Kits/SMO_MARMOSET_LIVELINK Folder Data -----")
    indexLLMARMO = midkitllmarmo(folder=kit_dir, files=kit_ll_marmosettoolbag_fi())

    print("----- Copy Root/Kits/SMO_PIXAFLUX_LIVELINK Folder Data -----")
    indexLLPIXA = midkitllpixa(folder=kit_dir, files=kit_ll_pixaflux_fi())

    print("----- Copy Root/Kits/SMO_RIZOMUV_LIVELINK Folder Data -----")
    indexLLRIZOM = midkitllrizom(folder=kit_dir, files=kit_ll_rizomuv_fi())

    ###### MESSAGE
    indexmessage = midmessage(info=message)

    index_data_base = (indexheader + indexroot + indexconfig + indexscripts + indexlxserv + indexsmodule + indextraining)
    index_data_kit = (indexkits + indexAI + indexBAKE + indexBATCH + indexCAD + indexCB + indexCLEANUP + indexDOC + indexGC + indexMASTER + indexMATH + indexMESHOPS + indexMIFABOMA + indexPCLOUD + indexQTAG + indexUV + indexVENOM)
    index_data_LLkit = (indexLLPIXA + indexLLMARMO + indexLLRIZOM)

    index_data = (index_data_base + index_data_kit + index_data_LLkit + indexmessage)

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

    print("----- Files in config folder -----")
    for file in config_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- scripts Folder files -----")
    for file in scripts_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- lxserv Folder files -----")
    for file in lxserv_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- smodule Folder files -----")
    for file in smodule_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- TRAINING_SCENE Folder files -----")
    for file in training_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    ###### STANDARD KITS ########
    print("----- Kits files -----")
    for file in kits_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    # print("----- SMO_AI_TOOLS Folder files -----")
    # for file in kitAI_fi():
    #     print(file.relative_to(kit_dir))
    #     lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_BAKE Folder files -----")
    for file in kit_bake_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_BATCH Folder files -----")
    for file in kit_batch_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_CAD_TOOLS Folder files -----")
    for file in kit_cad_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_CLEANUP Folder files -----")
    for file in kit_cleanup_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_COLOR_BAR Folder files -----")
    for file in kit_colorbar_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_DOC Folder files -----")
    for file in kit_doc_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_GAME_CONTENT Folder files -----")
    for file in kit_gamecontent_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_MASTER Folder files -----")
    for file in kit_master_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_MATH_TOOLS Folder files -----")
    for file in kit_mathtools_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_MESHOPS Folder files -----")
    for file in kit_meshops_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_MIFABOMA Folder files -----")
    for file in kit_mifaboma_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_QUICK_TAG Folder files -----")
    for file in kit_qtag_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_UV Folder files -----")
    for file in kit_uv_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_VENOM Folder files -----")
    for file in kit_venom_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    ###### LIVELINK KITS
    print("----- SMO_MARMOSET_LIVELINK Folder files -----")
    for file in kit_ll_marmosettoolbag_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_PIXAFLUX_LIVELINK Folder files -----")
    for file in kit_ll_pixaflux_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    print("----- SMO_RIZOMUV_LIVELINK Folder files -----")
    for file in kit_ll_rizomuv_fi():
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))

    lpk.close()