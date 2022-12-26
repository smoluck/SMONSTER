# python
"""
# Name:         SMO_SMONSTER_Club_SetAllKeymaps_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to :
#               Launch all the Popup Window dialog to set all the default keymaps for Smonster Kits.
#
# Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
# Website:      https://www.smoluck.com
#
# Created:      31/01/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

CMD_NAME = 'smo.SMONSTER.QuickSetAllKeymaps'


class SMONSTER_CLUB_SetAllKeymaps_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO SMONSTER - Quick Set All Default Keymaps'

    def cmd_Desc(self):
        return 'Launch all the Popup Window dialog to set all the default keymaps for Smonster Kits.'

    def cmd_Tooltip(self):
        return 'Launch all the Popup Window dialog to set all the default keymaps for Smonster Kits.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO SMONSTER - Quick Set All Default Keymaps'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        try:
            lx.eval('smo.SMONSTER.MapDefaultHotkeys')
        except:
            pass

        try:
            lx.eval('smo.AI.MapDefaultHotkeys')
        except:
            pass

        try:
            lx.eval('smo.BAKE.MapDefaultHotkeys')
        except:
            pass

        try:
            lx.eval('smo.BATCH.MapDefaultHotkeys')
        except:
            pass

        try:
            lx.eval('smo.CAD.MapDefaultHotkeys')
        except:
            pass

        try:
            lx.eval('smo.CLEANUP.MapDefaultHotkeys')
        except:
            pass

        try:
            lx.eval('smo.CB.MapDefaultHotkeys')
        except:
            pass

        try:
            lx.eval('smo.GC.MAIN.MapDefaultHotkeys')
        except:
            pass

        try:
            lx.eval('smo.GC.EXTRA.MapDefaultHotkeys')
        except:
            pass

        try:
            lx.eval('smo.GC.151.MapDefaultHotkeys')
        except:
            pass

        try:
            lx.eval('smo.MATH.MapDefaultHotkeys')
        except:
            pass

        try:
            lx.eval('smo.MIFABOMA.MapDefaultHotkeys')
        except:
            pass

        try:
            lx.eval('smo.QT.MapDefaultHotkeys')
        except:
            pass

        try:
            lx.eval('smo.UV.MapDefaultHotkeys')
        except:
            pass

        try:
            lx.eval('smo.VENOM.MapDefaultHotkeys')
        except:
            pass


lx.bless(SMONSTER_CLUB_SetAllKeymaps_Cmd, CMD_NAME)
