# Python3

import sys
import shutil
from pathlib import Path


# Get the root path to this repo
repo_dir = Path(__file__).parent

# Get the os dependant kits path
if sys.platform == "win32":
    install_path = Path(r"~\AppData\Roaming\Luxology\Kits").expanduser()
elif sys.platform == "darwin":
    install_path = Path("~/Library/Application Support/Luxology/Kits").expanduser()


# Get the name of the kits directory
kit_name = "SMONSTER_KIT"
# Get the development kit.
kit_path = repo_dir / kit_name
# Get the modo install path for kit
modo_kit_path = install_path / kit_name


# If the Kit exists in the modo kit path, remove it before copying the new one.
if modo_kit_path.exists():
    shutil.rmtree(modo_kit_path)

# Copy the development kit to the modo kit path.
shutil.copytree(src=kit_path, dst=modo_kit_path)
