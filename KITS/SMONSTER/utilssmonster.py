from pathlib import Path

# Get the root path to this repo
repo_dir = Path(__file__).parent
# Get the kit directory
kit_dir = repo_dir / "KITS"
target_kit = kit_dir / "SMONSTER_V3"

config_dir = target_kit / "Config"
scripts_dir = target_kit / "scripts"
smodule_dir = target_kit / "smodule"
lxserv_dir = target_kit / "lxserv"
training_dir = target_kit / "TRAINING_SCENES"

###### STANDARD KITS
kitsfolders_dir = target_kit / "Kits"

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


# def make_index(folder, files, message, restart="No"):
#     """ Method to generate the body of an index.xml for packaging example files.
#
#     Args:
#         folder (Path): The name of the folder.
#         files (list(Path)): List of files in the folder.
#         message (str): The message to display to the user after installing the lpk.
#         restart (bool): If the lpk should present the restart message to the user.
#
#     Returns:
#         xml (str): the generated index.xml template.
#     """
#     # Header
#     xml = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
#     # Modo 10+
#     xml += "\n<package version=\"1000\">"
#     # No need to restart
#     restart = "YES" if restart else "NO"
#     xml += f'\n\t<kit name="{folder}" restart="{restart}">'
#     # For each file add target
#     for file in files:  # type: Path
#         # Path including the kit directory
#         full_path = file.relative_to(folder.parent)
#         # Path without kit directory
#         rel_path = file.relative_to(folder)
#         xml += f'\n\t\t<source target="{full_path}">{rel_path}</source>'
#     xml += f'\n\t</kit>\n\t<message button="Help">{message}</message>\n</package>'
#     # Return Text
#     return xml

###### SMONSTER BASE STRUCTURE #########################################################
def midheader(name, restart="No"):
    # Header
    xml_header = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    # Modo 10+
    xml_header += "\n<package version=\"1500\">"
    # No need to restart
    restart = "YES" if restart else "NO"
    xml_header += f'\n\t<kit name="{name}" restart="{restart}">'
    return xml_header

def midroot(folder, files):
    # For each file add target
    xml_root = f''
    for file in files:  # type: Path
        # Path including the kit directory
        root_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        root_rel_path = file.relative_to(folder)
        xml_root += f'\n\t\t<source target="{root_full_path}">{root_rel_path}</source>'
    # print (xml_root)
    # Return Text
    return xml_root

def midconfig(folder, files):
    # For each file add target
    xml_config = f''
    for file in files:  # type: Path
        # Path including the kit directory
        config_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        config_rel_path = file.relative_to(folder)
        xml_config += f'\n\t\t<source target="{config_full_path}">{config_rel_path}</source>'
    # print (xml_config)
    return xml_config

def midscripts(folder, files):
    # For each file add target
    xml_scripts = f''
    for file in files:  # type: Path
        # Path including the kit directory
        scripts_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        scripts_rel_path = file.relative_to(folder)
        xml_scripts += f'\n\t\t<source target="{scripts_full_path}">{scripts_rel_path}</source>'
    # print (xml_scripts)
    return xml_scripts

def midlxserv(folder, files):
    # For each file add target
    xml_lxserv = f''
    for file in files:  # type: Path
        # Path including the kit directory
        lxserv_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        lxserv_rel_path = file.relative_to(folder)
        xml_lxserv += f'\n\t\t<source target="{lxserv_full_path}">{lxserv_rel_path}</source>'
    return xml_lxserv

def midsmodule(folder, files):
    # For each file add target
    xml_smodule = f''
    for file in files:  # type: Path
        # Path including the kit directory
        smodule_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        smodule_rel_path = file.relative_to(folder)
        xml_smodule += f'\n\t\t<source target="{smodule_full_path}">{smodule_rel_path}</source>'
    return xml_smodule

def midtraining(folder, files):
    # For each file add target
    xml_training = f''
    for file in files:  # type: Path
        # Path including the kit directory
        training_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        training_rel_path = file.relative_to(folder)
        xml_training += f'\n\t\t<source target="{training_full_path}">{training_rel_path}</source>'
    # print (xml_training)
    return xml_training



###### STANDARD KITS #########################################################
def midkits(folder, files):
    # For each file add target
    xml_kits = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kits_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kits_rel_path = file.relative_to(folder)
        xml_kits += f'\n\t\t<source target="{kits_full_path}">{kits_rel_path}</source>'
    # print (xml_root)
    # Return Text
    return xml_kits

def midkitai(folder, files):
    # For each file add target
    xml_kitAI = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitAI_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitAI_rel_path = file.relative_to(folder)
        xml_kitAI += f'\n\t\t<source target="{kitAI_full_path}">{kitAI_rel_path}</source>'
    # print (xml_kitAI)
    # Return Text
    return xml_kitAI

def midkitbake(folder, files):
    # For each file add target
    xml_kitBAKE = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitBAKE_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitBAKE_rel_path = file.relative_to(folder)
        xml_kitBAKE += f'\n\t\t<source target="{kitBAKE_full_path}">{kitBAKE_rel_path}</source>'
    # print (xml_kitBAKE)
    # Return Text
    return xml_kitBAKE

def midkitbatch(folder, files):
    # For each file add target
    xml_kitBATCH = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitBATCH_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitBATCH_rel_path = file.relative_to(folder)
        xml_kitBATCH += f'\n\t\t<source target="{kitBATCH_full_path}">{kitBATCH_rel_path}</source>'
    # print (xml_kitBATCH)
    # Return Text
    return xml_kitBATCH

def midkitcad(folder, files):
    # For each file add target
    xml_kitCAD = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitCAD_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitCAD_rel_path = file.relative_to(folder)
        xml_kitCAD += f'\n\t\t<source target="{kitCAD_full_path}">{kitCAD_rel_path}</source>'
    # print (xml_kitCAD)
    # Return Text
    return xml_kitCAD

def midkitcleanup(folder, files):
    # For each file add target
    xml_kitCLEANUP = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitCLEANUP_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitCLEANUP_rel_path = file.relative_to(folder)
        xml_kitCLEANUP += f'\n\t\t<source target="{kitCLEANUP_full_path}">{kitCLEANUP_rel_path}</source>'
    # print (xml_kitCLEANUP)
    # Return Text
    return xml_kitCLEANUP

def midkitcb(folder, files):
    # For each file add target
    xml_kitCB = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitCB_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitCB_rel_path = file.relative_to(folder)
        xml_kitCB += f'\n\t\t<source target="{kitCB_full_path}">{kitCB_rel_path}</source>'
    # print (xml_kitCB)
    # Return Text
    return xml_kitCB

def midkitdoc(folder, files):
    # For each file add target
    xml_kitDOC = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitDOC_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitDOC_rel_path = file.relative_to(folder)
        xml_kitDOC += f'\n\t\t<source target="{kitDOC_full_path}">{kitDOC_rel_path}</source>'
    # print (xml_kitDOC)
    # Return Text
    return xml_kitDOC

def midkitgc(folder, files):
    # For each file add target
    xml_kitGC = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitGC_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitGC_rel_path = file.relative_to(folder)
        xml_kitGC += f'\n\t\t<source target="{kitGC_full_path}">{kitGC_rel_path}</source>'
    # print (xml_kitGC)
    # Return Text
    return xml_kitGC

def midkitmaster(folder, files):
    # For each file add target
    xml_kitMASTER = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitMASTER_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitMASTER_rel_path = file.relative_to(folder)
        xml_kitMASTER += f'\n\t\t<source target="{kitMASTER_full_path}">{kitMASTER_rel_path}</source>'
    # print (xml_kitMASTER)
    # Return Text
    return xml_kitMASTER

def midkitmath(folder, files):
    # For each file add target
    xml_kitMATH = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitMATH_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitMATH_rel_path = file.relative_to(folder)
        xml_kitMATH += f'\n\t\t<source target="{kitMATH_full_path}">{kitMATH_rel_path}</source>'
    # print (xml_kitMATH)
    # Return Text
    return xml_kitMATH

def midkitmeshops(folder, files):
    # For each file add target
    xml_kitMESHOPS = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitMESHOPS_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitMESHOPS_rel_path = file.relative_to(folder)
        xml_kitMESHOPS += f'\n\t\t<source target="{kitMESHOPS_full_path}">{kitMESHOPS_rel_path}</source>'
    # print (xml_kitMESHOPS)
    # Return Text
    return xml_kitMESHOPS

def midkitmifaboma(folder, files):
    # For each file add target
    xml_kitMIFABOMA = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitMIFABOMA_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitMIFABOMA_rel_path = file.relative_to(folder)
        xml_kitMIFABOMA += f'\n\t\t<source target="{kitMIFABOMA_full_path}">{kitMIFABOMA_rel_path}</source>'
    # print (xml_kitMIFABOMA)
    # Return Text
    return xml_kitMIFABOMA

def midkitpcloud(folder, files):
    # For each file add target
    xml_kitPCLOUD = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitPCLOUD_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitPCLOUD_rel_path = file.relative_to(folder)
        xml_kitPCLOUD += f'\n\t\t<source target="{kitPCLOUD_full_path}">{kitPCLOUD_rel_path}</source>'
    # print (xml_kitPCLOUD)
    # Return Text
    return xml_kitPCLOUD

def midkitqtag(folder, files):
    # For each file add target
    xml_kitQTAG = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitQTAG_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitQTAG_rel_path = file.relative_to(folder)
        xml_kitQTAG += f'\n\t\t<source target="{kitQTAG_full_path}">{kitQTAG_rel_path}</source>'
    # print (xml_kitQTAG)
    # Return Text
    return xml_kitQTAG

def midkituv(folder, files):
    # For each file add target
    xml_kitUV = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitUV_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitUV_rel_path = file.relative_to(folder)
        xml_kitUV += f'\n\t\t<source target="{kitUV_full_path}">{kitUV_rel_path}</source>'
    # print (xml_kitUV)
    # Return Text
    return xml_kitUV

def midkitvenom(folder, files):
    # For each file add target
    xml_kitVENOM = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitVENOM_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitVENOM_rel_path = file.relative_to(folder)
        xml_kitVENOM += f'\n\t\t<source target="{kitVENOM_full_path}">{kitVENOM_rel_path}</source>'
    # print (xml_kitVENOM)
    # Return Text
    return xml_kitVENOM



###### LIVELINK KITS #########################################################
def midkitllmarmo(folder, files):
    # For each file add target
    xml_kitLL_MARMO = f''
    for file in files:  # type: Path
        # if file.is_file() and not f.name.endswith("_KeymapCommander.pyc") and not f.name.endswith("_Startup.pyc"):
        # Path including the kit directory
        kitLL_MARMO_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitLL_MARMO_rel_path = file.relative_to(folder)
        xml_kitLL_MARMO += f'\n\t\t<source target="{kitLL_MARMO_full_path}">{kitLL_MARMO_rel_path}</source>'
    # print (xml_kitLL_MARMO)
    # Return Text
    return xml_kitLL_MARMO

def midkitllpixa(folder, files):
    # For each file add target
    xml_kitLL_PIXA = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitLL_PIXA_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitLL_PIXA_rel_path = file.relative_to(folder)
        xml_kitLL_PIXA += f'\n\t\t<source target="{kitLL_PIXA_full_path}">{kitLL_PIXA_rel_path}</source>'
    # print (xml_kitLL_PIXA)
    # Return Text
    return xml_kitLL_PIXA

def midkitllrizom(folder, files):
    # For each file add target
    xml_kitLL_RIZOMUV = f''
    for file in files:  # type: Path
        # Path including the kit directory
        kitLL_RIZOMUV_full_path = file.relative_to(folder.parent)
        # Path without kit directory
        kitLL_RIZOMUV_rel_path = file.relative_to(folder)
        xml_kitLL_RIZOMUV += f'\n\t\t<source target="{kitLL_RIZOMUV_full_path}">{kitLL_RIZOMUV_rel_path}</source>'
    # print (xml_kitLL_RIZOMUV)
    # Return Text
    return xml_kitLL_RIZOMUV



def midmessage(info):
    xml_message = f'\n\t</kit>\n\t<message button="Help">{info}</message>\n</package>'
    return xml_message



def get_version():
    with repo_dir.joinpath("VERSION").open("r") as version_file:
        return version_file.read().strip()

