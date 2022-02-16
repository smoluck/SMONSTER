# python
# ---------------------------------------
# Name:         SMO_DOC_VideoLink_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to:
#               Open the Tutorial Videos using a String Argument for Defined Kit and an integer as argument for Video ID.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      14/08/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.DOC.VideoLink"
# smo.DOC.VideoLink GAME 1

class SMO_DOC_VideoLink_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Kit ID", lx.symbol.sTYPE_STRING)
        self.dyna_Add("Page ID", lx.symbol.sTYPE_INTEGER)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'Open Documentation Video'

    def cmd_Desc(self):
        return 'Open the Tutorial Videos using a String Argument for Defined Kit and an integer as argument for Video ID.'

    def cmd_Tooltip(self):
        return 'Open the Tutorial Videos using a String Argument for Defined Kit and an integer as argument for Video ID.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'Open Documentation Video'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        args = lx.args()
        # lx.out(args)

        # BAKE - BATCH - CAD - CLEANUP - COLOR - GAME - MATH - MIFABOMA - QUICKTAG - RIZOMUV - MARMOSET - PIXAFLUX
        KIT_ID = self.dyna_String(0)
        PAGE_ID = self.dyna_Int(1)

        QUALITY = lx.eval('user.value SMO_UseVal_DOC_VideoQuality ?')
        # lx.out('YouTube Video Quality:', QUALITY)
        FULLSCREEN = lx.eval('user.value SMO_UseVal_DOC_FullScreen ?')
        # lx.out('Open YouTube Page in Fullscreen Mode:', FULLSCREEN)
        YouTube = "https://www.youtube.com/"
        TIME = "&t="
        TimeCount = 0
        
        if QUALITY == 1080 :
            VidQua = "&vq=hd1080"
        if QUALITY == 720 :
            VidQua = "&vq=hd720"
        if FULLSCREEN == True :
            FullS = "&fs=1"
            WatchMode = "watch?v="
            # WatchMode = "watch_popup?v=" # This PopUp mode doesn't allow to start the video at specific time
        if FULLSCREEN == False :
            FullS = "&fs=0"
            WatchMode = "watch?v="




        if KIT_ID == "BAKE":
            if PAGE_ID == 1:
                # BAKE: Preview Cage
                URL = "2Tq6XeEh9ug"
                TimeCount = 215
            if PAGE_ID == 2:
                # BAKE: Set Bake Pairs
                URL = "2Tq6XeEh9ug"
                TimeCount = 70

        if KIT_ID == "BATCH":
            if PAGE_ID == 1:
                # BATCH: Overview
                URL = "wTVcdREWOIg"
                TimeCount = 100

        if KIT_ID == "CAD":
            if PAGE_ID == 1:
                # CAD: Walkthrough Cleaning Process Tutorial
                URL = "zeK736RmjrE"
            if PAGE_ID == 2:
                # CAD: Cleanup NGons
                URL = "UYQ2ugdTC4c"
                TimeCount = 167
            if PAGE_ID == 3:
                # CAD: Main Menu integrated Help
                URL = "5fMt-NJPey8"
                TimeCount = 87
            if PAGE_ID == 4:
                # CAD: Cleanup To Ngon on XYZ Axes
                URL = "UYQ2ugdTC4c"
                TimeCount = 167
            if PAGE_ID == 5:
                # CAD: TriRing To Quad - FLAT
                URL = "5fMt-NJPey8"
                TimeCount = 50
            if PAGE_ID == 6:
                # CAD: TriRing To Quad - ROUND
                URL = "5fMt-NJPey8"
                TimeCount = 58
            if PAGE_ID == 7:
                # CAD: Rebuild with Cube
                URL = "5fMt-NJPey8"
                TimeCount = 161
            if PAGE_ID == 8:
                # CAD: Rebuild With Cylinder Closed
                URL = "5fMt-NJPey8"
                TimeCount = 87
            if PAGE_ID == 9:
                # CAD: Detriangulate
                URL = "UYQ2ugdTC4c"
                TimeCount = 213

        if KIT_ID == "CLEANUP":
            if PAGE_ID == 1:
                # CLEANUP: Batch Cleaning Command
                URL = "QWgUJvEAJBc"
                TimeCount = 126
            if PAGE_ID == 2:
                # CLEANUP: Batch Cleaning User Preferences
                URL = "QWgUJvEAJBc"

        if KIT_ID == "COLOR":
            if PAGE_ID == 1:
                # COLOR: COLOR Bar : Cycle
                URL = "YTLGi09ZttU"
                TimeCount = 176
            if PAGE_ID == 2:
                # COLOR: COLOR Bar : By Color
                URL = "YTLGi09ZttU"
            if PAGE_ID == 3:
                # COLOR: COLOR Bar : By Type
                URL = "YTLGi09ZttU"

        if KIT_ID == "GAME":
            if PAGE_ID == 1:
                # GAME:
                URL = ""
            if PAGE_ID == 2:
                # GAME:
                URL = ""
            if PAGE_ID == 3:
                # GAME:
                URL = ""

        if KIT_ID == "MATH":
            if PAGE_ID == 1:
                # MATH: Basic Nodes
                URL = "TU-AlDdY8sY"
                TimeCount = 108
            if PAGE_ID == 2:
                # MATH:
                URL = ""
            if PAGE_ID == 3:
                # MATH:
                URL = ""

        if KIT_ID == "MIFABOMA":
            if PAGE_ID == 1:
                # MIFABOMA: Boolean
                URL = "i5nF0G97Izk"
            if PAGE_ID == 2:
                # MIFABOMA: Mirror
                URL = "i5nF0G97Izk"
            if PAGE_ID == 3:
                # MIFABOMA: Match / Align
                URL = "fd3nlRKQPvY"
            if PAGE_ID == 4:
                # MIFABOMA: Flip On Axis
                URL = "lno53bLqFMo"
                TimeCount = 54
            if PAGE_ID == 5:
                # MIFABOMA: Slice
                URL = "lno53bLqFMo"
                TimeCount = 215

        if KIT_ID == "QUICKTAG":
            if PAGE_ID == 1:
                # QUICKTAG:
                URL = ""
            if PAGE_ID == 2:
                # QUICKTAG:
                URL = ""
            if PAGE_ID == 3:
                # QUICKTAG:
                URL = ""

        if KIT_ID == "UV":
            if PAGE_ID == 1:
                # UV: Preferences
                URL = "05b8SxzN2Bs"
            if PAGE_ID == 2:
                # UV: View Styles
                URL = "8ZWKLuUkvpo"
            if PAGE_ID == 3:
                # UV: Cheker Textures
                URL = "8ZWKLuUkvpo"
                TimeCount = 56
            if PAGE_ID == 4:
                # UV: Smart Projection Planar
                URL = "I_Wt0PMOkM8"
            if PAGE_ID == 5:
                # UV: Smart Projection Unwrap
                URL = "FCKcJemxS1Q"
            if PAGE_ID == 6:
                # UV: Smart Projection Cylindrical
                URL = "yfzGHzaXVGo"
            if PAGE_ID == 7:
                # UV: Relax
                URL = "j1HlKfJA5xA"
                TimeCount = "266"
            if PAGE_ID == 8:
                # UV: Walkthrough Tutorial
                URL = "sAClt96-bFQ"

        if KIT_ID == "VENOM":
            if PAGE_ID == 1:
                # VENOM: Commands
                URL = "yfdhhsm1UK4"

        if KIT_ID == "MARMOSET":
            if PAGE_ID == 1:
                # MARMOSET:
                URL = "2Tq6XeEh9ug"
                TimeCount = 390

        if KIT_ID == "RIZOMUV":
            if PAGE_ID == 1:
                # RIZOMUV:
                URL = "dttH0GtO-Zg"

        if KIT_ID == "PIXAFLUX":
            if PAGE_ID == 1:
                # PIXAFLUX:
                URL = "UVTfpYUHXtI"

        Output_URL = YouTube + WatchMode + URL + VidQua + FullS + TIME + str(TimeCount) + "s" # "s" for seconds

        # lx.out('*************************')
        # lx.out('YT URL', YouTube)
        # lx.out('WatchMode Tag', WatchMode)
        # lx.out('Video ID', URL)
        # lx.out('Video Quality', VidQua)
        # lx.out('Time Tag', TIME)
        # lx.out('Time Start', str(TimeCount))
        # lx.out('Open Video URL', Output_URL)
        # lx.out('*************************')

        lx.eval('openURL {%s}' % Output_URL)

lx.bless(SMO_DOC_VideoLink_Cmd, Command_Name)
