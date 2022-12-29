# python
"""
Name:               SMO_PixaFlux_CreateTSNMap_Cmd.py

Purpose:            This Script is designed to:
                    Create a new Texture file to save the PixaFlux Data.
                    Resolution defined by Argument in pixel.

Author:             Franck ELISABETH (with the help of Tom Dymond)
Website:            https://www.smoluck.com
Created:            12/08/2020
Copyright:          (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import os
import traceback

Cmd_Name = "smo.LL.PIXAFLUX.CreateTSNMap"


# smo.LL.PIXAFLUX.CreateTSNMap 2048

class SMO_PixaFlux_CreateTSNMap_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Map Size", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO LL PIXAFLUX - Create Tangent Space NormalMap'

    def cmd_Desc(self):
        return 'Create a new Texture file to save the PixaFlux Data. Resolution defined by Argument in pixel.'

    def cmd_Tooltip(self):
        return 'Create a new Texture file to save the PixaFlux Data. Resolution defined by Argument in pixel.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO LL PIXAFLUX - Create Tangent Space NormalMap'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):

        # ------------- ARGUMENTS ------------- #
        # MapSize = 512
        # MapSize = 1024
        # MapSize = 2048
        # MapSize = 4096
        MapSize = self.dyna_Int(0)
        # ------------------------------------- #

        scene = modo.scene.current()
        # -------------  Create Image Data
        # get modo's temp dir
        temp_dir = lx.eval('query platformservice path.path ? temp')
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
                lx.out('Didn\'t save Normal Map Image for PixaFlux.')
                return
            else:
                image_export_path = os.path.splitext(image_export_path)[0] + '.png'
                image_file_name = os.path.splitext(os.path.basename(image_export_path))[0]

        # lx.eval('clip.new')
        if MapSize == 512:
            lx.eval('clip.newStill "{}" x512 RGBA false false format:PNG colorspace:(none)'.format(image_export_path))
        if MapSize == 1024:
            lx.eval('clip.newStill "{}" x1024 RGBA false false format:PNG colorspace:(none)'.format(image_export_path))
        if MapSize == 2048:
            lx.eval('clip.newStill "{}" x2048 RGBA false false format:PNG colorspace:(none)'.format(image_export_path))
        if MapSize == 4096:
            lx.eval('clip.newStill "{}" x4096 RGBA false false format:PNG colorspace:(none)'.format(image_export_path))
        lx.eval('clip.addStill "{}"'.format(image_export_path))
        # lx.eval('select.subItem {PIXAFLUX_NM:videoStill001} set mediaClip')
        lx.command("select.subItem", item=image_file_name, mode="set")
        image_save_time = os.path.getmtime(image_export_path)


# -------------------------------------------- #

# ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END


lx.bless(SMO_PixaFlux_CreateTSNMap_Cmd, Cmd_Name)
