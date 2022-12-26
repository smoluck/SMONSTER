#python

from pathlib import Path

# Get the root path to this repo
repo_dir = Path(__file__).parent
# Get the kit directory
kit_dir = repo_dir / "KITS"
target_kit = kit_dir / "SMONSTER_TRAINING"

lxserv_dir = target_kit / "lxserv"
training_dir = target_kit / "TRAINING_SCENES"


# ----- SMONSTER BASE STRUCTURE ----- #
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


def midmessage(info):
    xml_message = f'\n\t</kit>\n\t<message button="Help">{info}</message>\n</package>'
    return xml_message


def get_version():
    with repo_dir.joinpath("VERSION").open("r") as version_file:
        return version_file.read().strip()
