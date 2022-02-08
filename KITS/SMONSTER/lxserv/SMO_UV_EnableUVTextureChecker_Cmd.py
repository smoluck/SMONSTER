# python
# ---------------------------------------
# Name:         SMO_UV_EnableUVTextureChecker_Cmd.py
# Version:      1.0
#
# Purpose:      Select the Mesh in Item Mode
#               Enable the UV Texture Checker in the current Viewport using the UVGrid PNG files from the UV kit. (Argument define the file resolution)
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      14/04/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo, os

CMD_NAME = "smo.UV.EnableUVTextureChecker"


# smo.UV.EnableUVTextureChecker 1024

class SMO_UV_EnableUVTextureChecker_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Resolution", lx.symbol.sTYPE_INTEGER)

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO UV EnableUVTextureChecker'

    def cmd_Desc(self):
        return 'Enable the UV Texture Checker in the current Viewport using the UVGrid PNG files from the UV kit. (Argument define the file resolution)'

    def cmd_Tooltip(self):
        return 'Enable the UV Texture Checker in the current Viewport using the UVGrid PNG files from the UV kit. (Argument define the file resolution)'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO UV EnableUVTextureChecker'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        RES = self.dyna_Int(0)

        ### Load RemoveCoPlanar6Side Preset for the processing ###
        #####--- Define the Preset directory of the Custom CAD Presets to load the RemoveCoPlanar6Side Assembly --- START ---#####
        #####
        SMO_UVGrid_Path = lx.eval("query platformservice alias ? {kit_SMO_UV:UVGrid}")
        # lx.out('SMO UVGrid Path:', SMO_UVGrid_Path)

        SMO_UVGrid_File_512 = "uvLayoutGrid_512.png"
        SMO_UVGrid_File_1024 = "uvLayoutGrid_1024.png"
        SMO_UVGrid_File_2048 = "uvLayoutGrid_2048.png"
        SMO_UVGrid_File_4096 = "uvLayoutGrid_4096.png"

        UVGridFile = (os.path.join(SMO_UVGrid_Path + "\\" + SMO_UVGrid_File_512))
        if RES == 512:
            UVGridFile = (os.path.join(SMO_UVGrid_Path + "\\" + SMO_UVGrid_File_512))
        if RES == 1024:
            UVGridFile = (os.path.join(SMO_UVGrid_Path + "\\" + SMO_UVGrid_File_1024))
        if RES == 2048:
            UVGridFile = (os.path.join(SMO_UVGrid_Path + "\\" + SMO_UVGrid_File_2048))
        if RES == 4096:
            UVGridFile = (os.path.join(SMO_UVGrid_Path + "\\" + SMO_UVGrid_File_4096))
        # print(UVGridFile)
        #####
        #####--- Define the Preset directory of the Custom CAD Presets to load the RemoveCoPlanar6Side Assembly --- START ---#####

        try:
            lx.eval('layout.window UVsPBGlobal')
            lx.eval('select.preset {%s} UVsVPO set' % UVGridFile)
            lx.eval('preset.do')
            lx.eval('layout.window UVsPBGlobal')

        except:
            sys.exit
lx.bless(SMO_UV_EnableUVTextureChecker_Cmd, CMD_NAME)
