# python
"""
Name:         SMO_GC_AttachScriptToPreset_Cmd.py

Purpose:      This script is designed to:
              Attach SMO_GC_onDrop_RotateTool.py script to the selected MeshPreset file via PB_View and smo.GC.AttachScriptToPreset command.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      03/02/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.GC.AttachScriptToPreset"


class SMO_GC_AttachScriptToPreset_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Attach Script to Preset'

    def cmd_Desc(self):
        return 'Attach SMO_GC_onDrop_RotateTool.py script to the selected MeshPreset file via PB_View and smo.GC.AttachScriptToPreset command.'

    def cmd_Tooltip(self):
        return 'Attach SMO_GC_onDrop_RotateTool.py script to the selected MeshPreset file via PB_View and smo.GC.AttachScriptToPreset command.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Attach Script to Preset'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        AttachScriptPath = lx.eval('query platformservice alias ? {kit_SMO_GAME_CONTENT:MacroSmoluck/Kitbash/SMO_GC_onDrop_RotateTool.py}')
        # lx.out(AttachScriptPath)
        try:
            SelPrstPBPath = lxu.select.PresetPathSelection().current()[-1][0]
        except:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title SMO KitBash')
            lx.eval('dialog.msg {You need to select a Polystein Preset in the Preset Browser}')
            lx.eval('dialog.open')
            sys.exit()
        # lx.out(SelPrstPBPath)
        
        lx.eval('preset.attachScript preset:{%s} script:{%s}' % (SelPrstPBPath, AttachScriptPath))


lx.bless(SMO_GC_AttachScriptToPreset_Cmd, Cmd_Name)
