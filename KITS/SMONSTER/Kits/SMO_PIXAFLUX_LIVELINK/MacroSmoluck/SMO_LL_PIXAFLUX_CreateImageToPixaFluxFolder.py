# python
"""
Name:         SMO_PixaFlux_CreateImageToPixaFluxFolder.py

Purpose:      This Command is designed to:
              Create Image to PixaFlux Folder to Temp folder

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Modified:     09/07/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import os

############################ Export FBX Data #############################
# get modo's temp dir
temp_dir = lx.eval('query platformservice path.path ? temp')


############################ Create Image Data #############################
# name our temp file
image_file_name = "PixaFlux_NM.png"
# builds the complete path out of the temp dir and the temp file name
image_export_path = os.path.join(temp_dir, "SMO_PixaFluxLiveLink", image_file_name)


if not os.path.exists(os.path.dirname(image_export_path)):
    # try to create the directory. 
    try:
        os.makedirs(os.path.dirname(image_export_path))
    except:
        # if that fails for any reason print out the error
        print(traceback.format_exc())
else:
    if image_export_path == None:
        lx.out ('Didn\'t save Normal Map Image for PixaFlux.')
    else:
        image_export_path = os.path.splitext (image_export_path)[0] + '.png'
        image_file_name = os.path.splitext (os.path.basename (image_export_path))[0]


#lx.eval('clip.new')
lx.eval('clip.newStill "{}" x2048 RGBA false false format:PNG colorspace:(none)'.format(image_export_path))
lx.eval('clip.addStill "{}"'.format(image_export_path))
#lx.eval('select.subItem {PIXAFLUX_NM:videoStill001} set mediaClip')
lx.command("select.subItem", item=image_file_name, mode="set")
image_save_time = os.path.getmtime (image_export_path)