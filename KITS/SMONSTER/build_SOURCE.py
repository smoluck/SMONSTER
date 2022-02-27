from os import mkdir
from pathlib import Path
from shutil import rmtree
from zipfile import ZipFile, ZIP_DEFLATED


import utilssmonster
from utilssmonster import make_index


# Get the root path to this repo
repo_dir = Path(__file__).parent

# Get the kit directory
kit_dir = repo_dir / "KITS"
target_kit = kit_dir / "SMONSTER"

lxserv_dir = target_kit / "lxserv"
kitsfolders_dir = target_kit / "Kits"

kit_ai = kitsfolders_dir / "SMO_AI_TOOLS"
kit_bake = kitsfolders_dir / "SMO_BAKE"
kit_batch = kitsfolders_dir / "SMO_BATCH"
kit_cad = kitsfolders_dir / "SMO_CAD_TOOLS"
kit_cleanup = kitsfolders_dir / "SMO_CLEANUP"
kit_cb = kitsfolders_dir / "SMO_COLOR_BAR"
kit_doc = kitsfolders_dir / "SMO_DOC"
kit_gc = kitsfolders_dir / "SMO_GAME_CONTENT"
kit_master = kitsfolders_dir / "SMO_MASTER"
kit_math = kitsfolders_dir / "SMO_MATH_TOOLS"
kit_meshops = kitsfolders_dir / "SMO_MESHOPS"
kit_mifaboma = kitsfolders_dir / "SMO_MIFABOMA"
kit_pcloud = kitsfolders_dir / "SMO_PCLOUD_XYZ"
kit_qt = kitsfolders_dir / "SMO_QUICK_TAG"
kit_uv = kitsfolders_dir / "SMO_UV"
kit_venom = kitsfolders_dir / "SMO_VENOM"

kit_marmo = kitsfolders_dir / "SMO_MARMOSET_LIVELINK"
kit_pix = kitsfolders_dir / "SMO_PIXAFLUX_LIVELINK"
kit_rizom = kitsfolders_dir / "SMO_RIZOMUV_LIVELINK"


# Get the build directory
build_dir = repo_dir / "build"
# Get the license file
license_file = repo_dir / "LICENSE"

# Get all files in the kit directory and make sure no pyc files come along
# kit_files = [f for f in kit_dir.glob("**/*") if f.is_file() and not f.name.endswith(".pyc")]

lxserv_file = [f for f in lxserv_dir.glob("**/*") if f.is_file() and not f.name.endswith(".pyc")]

# for f in lxserv_dir.glob("**/*"):
#     if f.is_file() and not f.name.endswith(".pyc"):
#         if not f.name.startswith("SMO_SMONSTER_"):
#             lxserv_file.append(f)
print(lxserv_file)
# del lxserv_file[:]

kit_files = lxserv_file

# Clear the build directory
if build_dir.exists():
    rmtree(build_dir)
# Remake the build directory
mkdir(build_dir)

# Format the lpk file name with the version number from the VERSION file
version = utils.get_version()
lpk_path = build_dir / f"SMONSTER_{version}.lpk"
# Message to display to the users
message = f"Successfully installed Modo Community Hub: v{version}"

# Build the LPK file.
with ZipFile(lpk_path, mode="w", compression=ZIP_DEFLATED) as lpk:
    # Add the license
    lpk.write(license_file, "license")
    # Generate the index.xml file data
    index_data = make_index(folder=kit_dir, files=kit_files, message=message)
    # Write the index.xml file
    lpk.writestr("index.xml", index_data)

    # Write all file into the lpk
    for file in kit_files:
        print(file.relative_to(kit_dir))
        lpk.write(file, file.relative_to(kit_dir))
