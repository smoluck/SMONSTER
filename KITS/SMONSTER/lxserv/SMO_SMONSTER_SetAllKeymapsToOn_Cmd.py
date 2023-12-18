# python
"""
Name:         SMO_SMONSTER_SetAllKeymapsToOn_Cmd.py

Purpose:      This script is designed to
              Set all the Smonster Keymaps Options to TRUE. Setting all Keymap in one Click.


Author:       Franck ELISABETH (with the help of Pavel Efimov)
Website:      https://www.linkedin.com/in/smoluck/
Created:      26/03/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.SMONSTER.SetAllKeymapsToOn"
# smo.SMONSTER.SetAllKeymapsToOn


class SMO_SMONSTER_SetAllKeymapsToOn_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO SMONSTER - Set All Keymaps to On'

    def cmd_Desc(self):
        return 'Set all the Smonster Keymaps Options to TRUE. Setting all Keymap in one Click.'

    def cmd_Tooltip(self):
        return 'Set all the Smonster Keymaps Options to TRUE. Setting all Keymap in one Click.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO SMONSTER - Set All Keymaps to On'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        # MODO version checks.
        # Modo 15.1 introduce change in SpaceBar Behavior
        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        # lx.out('Modo Version:',Modo_ver)

        lx.eval('smo.SMONSTER.MapDefaultHotkeys true true true true')
        # lx.eval('smo.AI.MapDefaultHotkeys true')
        lx.eval('smo.BAKE.MapDefaultHotkeys true')
        lx.eval('smo.BATCH.MapDefaultHotkeys true')
        lx.eval('smo.CAD.MapDefaultHotkeys true true true true')
        lx.eval('smo.CLEANUP.MapDefaultHotkeys true')
        lx.eval('smo.CB.MapDefaultHotkeys true true true true')
        lx.eval('smo.GC.MAIN.MapDefaultHotkeys true true true true true true true true true true true true true true true true true true true true true')
        lx.eval('smo.GC.EXTRA.MapDefaultHotkeys true true true true true true true true true true true true true true true true true true true true true')
        if Modo_ver >= 1510 :
            lx.eval('smo.GC.151.MapDefaultHotkeys true true true true true true')
        lx.eval('smo.MATH.MapDefaultHotkeys true')
        lx.eval('smo.MIFABOMA.MapDefaultHotkeys true')
        lx.eval('smo.QT.MapDefaultHotkeys true')
        lx.eval('smo.UV.MapDefaultHotkeys true true true true true true')
        lx.eval('smo.VENOM.MapDefaultHotkeys true true true true true true true true')
        lx.eval('smo.LL.MARMOSET.MapDefaultHotkeys true')
        lx.eval('smo.LL.PIXAFLUX.MapDefaultHotkeys true')
        lx.eval('smo.LL.RIZOMUV.MapDefaultHotkeys true')


lx.bless(SMO_SMONSTER_SetAllKeymapsToOn_Cmd, Cmd_Name)
