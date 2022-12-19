# python
# ---------------------------------------
# Name:         SMO_QT_CreateAllColorIDFromMatGrpMask_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Create a ColorID on All Material Group Mask in the current Scene.
#               (Create a new Group Mask on top of the BaseShader with a Contant as Diffuse color (random values))
#
# Author:       Franck ELISABETH (with the help of Pavel Efimov)
# Website:      http://www.smoluck.com
#
# Created:      31/03/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.QT.CreateAllColorIDFromMatGrpMask"
# smo.QT.CreateAllColorIDFromMatGrpMask

class SMO_QT_CreateAllColorIDFromMatGrpMask_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO QT - Create All ColorID From Material Group Mask'

    def cmd_Desc(self):
        return 'Create a ColorID on All Material Group Mask in the current Scene. (Create a new Group Mask on top of the BaseShader with a Contant as Diffuse color (random values))'

    def cmd_Tooltip(self):
        return 'Create a ColorID on All Material Group Mask in the current Scene. (Create a new Group Mask on top of the BaseShader with a Contant as Diffuse color (random values))'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO QT - Create All ColorID From Material Group Mask'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        selMatGrp = (lx.evalN('query sceneservice selection ? mask'))
        lx.out('Selected Material Groups', selMatGrp)
        selMatGrpCount = len(selMatGrp)
        lx.out('Selected Material Group Masks Count', selMatGrpCount)
        lx.eval('smo.GC.DeselectAll')
        if selMatGrpCount >= 1:
            for m in selMatGrp:
                lx.eval('select.item {%s} set' % m)
                lx.eval('smo.QT.CreateColorIDFromMatGrpMask')


lx.bless(SMO_QT_CreateAllColorIDFromMatGrpMask_Cmd, Cmd_Name)
