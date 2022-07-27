# python
# ---------------------------------------
# Name:         SMO_QT_CreateColorIDFromMaterialGroupMask_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Create a ColorID on the currently selected Material Group Mask.
#               (Create a new Group Mask on top of the BaseShader with a Contant as Diffuse color (random values))
#
# Author:       Franck ELISABETH (with the help of Pavel Efimov)
# Website:      http://www.smoluck.com
#
# Created:      31/03/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.QT.CreateColorIDFromMatGrpMask"
# smo.QT.CreateColorIDFromMatGrpMask

class SMO_QT_CreateColorIDFromMaterialGroupMask_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO QT - Create ColorID From Material Group Mask'

    def cmd_Desc(self):
        return 'Select the Source mesh of a given Instanced Mesh, instance it in place and move it back to Origin with zero transforms. (Create a new Group Mask on top of the BaseShader with a Contant as Diffuse color (random values))'

    def cmd_Tooltip(self):
        return 'Select the Source mesh of a given Instanced Mesh, instance it in place and move it back to Origin with zero transforms. (Create a new Group Mask on top of the BaseShader with a Contant as Diffuse color (random values))'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO QT - Create ColorID From Material Group Mask'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        sel = (lx.evalN('query sceneservice selection ? mask'))
        selCount = len(sel)
        lx.out('Selected Material Groups Count', selCount)
        if selCount >= 1:
            lx.eval('material.selectPolygons')
            lx.eval('smo.QT.SetColorID')
            lx.eval('smo.GC.DeselectAll')


lx.bless(SMO_QT_CreateColorIDFromMaterialGroupMask_Cmd, Cmd_Name)
