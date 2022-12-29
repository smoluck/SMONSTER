# python
"""
Name:         SMO_GC_FlipVertexNormalMap_Cmd.py

Purpose:      This script is designed to
              Flip the VertexNormalMap Data on selected Component.

Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
Website:      https://www.smoluck.com
Created:      07/06/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.FlipVertexNormalMap"
# smo.GC.FlipVertexNormalMap


class SMO_GC_FlipVertexNormalMap_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Flip Vertex Normal Map'

    def cmd_Desc(self):
        return 'Flip the VertexNormalMap Data on selected Component.'

    def cmd_Tooltip(self):
        return 'Flip the VertexNormalMap Data on selected Component.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Flip Vertex Normal Map'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        if self.SelModePoly:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        mesh = scene.selectedByType('mesh')[0]
        CsPolys = len(mesh.geometry.polygons.selected)


        ####
        # Select the VertexNormal Map if it exist in order to update it.
        VNMState = False
        lx.eval('smo.GC.ClearSelectionVmap 4 0')
        VMap_NameList = []
        VMap_TypeList = []
        for map in mesh.geometry.vmaps:
            mapObj = lx.object.MeshMap(map)
            VMap_Name = mapObj.Name()
            VMap_NameList.append(VMap_Name)
            VMap_Type = mapObj.Type()
            VMap_TypeList.append(VMap_Type)
        # print(VMap_NameList)
        # print(VMap_TypeList)
        for i in range(0, len(VMap_TypeList)):
            if (VMap_TypeList[i]) == 1313821261:  # int id for Vertex Normal map
                TargetVNMapName = VMap_NameList[i]
                VNMState = True
        # print(TargetVNMapName)
        ####

        ####
        # Correct and update the Vertex Normal Map accordingly to the PolyFlip.
        if VNMState:
            VNMapCmd = "NORM[3]:"
            MathCmd = VNMapCmd + TargetVNMapName
            print(MathCmd)
            lx.eval('vertMap.math {%s} {%s} -1.0 0.0 direct 0 (none) 1.0 0.0 direct 0' % (MathCmd, MathCmd))
        ####
        del VMap_NameList[:]
        del VMap_TypeList[:]


lx.bless(SMO_GC_FlipVertexNormalMap_Cmd, Cmd_Name)
