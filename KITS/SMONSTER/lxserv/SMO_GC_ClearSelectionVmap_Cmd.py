# python
"""
# Name:         SMO_GC_ClearSelectionVmap_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Select all or Deselect all Vmaps based
#               on specified type via arguments.
#
# Author:       Franck ELISABETH (with the help of Tom Dymond)
# Website:      https://www.smoluck.com
#
# Created:      12/08/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.ClearSelectionVmap"
# smo.GC.ClearSelectionVmap 1 1


class SMO_GC_ClearSelectionVmap_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("VMap Type", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
        self.dyna_Add("Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Clear Selection VertexMap'
    
    def cmd_Desc (self):
        return 'Select all or Deselect all Vmaps based on specified type via arguments.'
    
    def cmd_Tooltip (self):
        return 'Select all or Deselect all Vmaps based on specified type via arguments.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Clear Selection VertexMap'
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        mesh = modo.Mesh()
        
        # ------------- ARGUMENTS ------------- #
        
        # VMapType = 0 -> ALLLLLLL Maps
        # VMapType = 1 -> UV Map
        # VMapType = 2 -> Seam
        # VMapType = 3 -> Morph Map
        # VMapType = 4 -> Vertex Normal Map
        # VMapType = 5 -> B-Spline Weight map
        # VMapType = 6 -> Subdivision Weight map
        # VMapType = 7 -> Hard Edge Pick map
        # VMapType = 8 -> Weight map

        VMapType = self.dyna_Int (0)
        
        #ActionMode = 0 -> Select
        #ActionMode = 1 -> Deselect
        ActionMode = self.dyna_Int (1)
        # ------------------------------------- #

        VMap_NameList = []
        VMap_TypeList = []

        for map in mesh.geometry.vmaps:
            mapObj = lx.object.MeshMap(map)
            VMap_Name = mapObj.Name()
            VMap_NameList.append(VMap_Name)
            VMap_Type = mapObj.Type()
            VMap_TypeList.append(VMap_Type)
        #print(VMap_NameList)
        #print(VMap_TypeList)

        # Deselect all Weight Maps
        if VMapType == 0:
            mesh_list = scene.selectedByType(modo.constants.MESH_TYPE)
            for mesh in mesh_list:
                for i in range(0, len(VMap_TypeList)):
                    #  Weight
                    if (VMap_TypeList[i]) == 1464289364 and ActionMode == 0:  # int id for Weight map
                        lx.eval("select.vertexMap {%s} wght add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1464289364 and ActionMode == 1:  # int id for Weight map
                        lx.eval("select.vertexMap {%s} wght remove" % (VMap_NameList[i]))

                    #  UV map
                    if (VMap_TypeList[i]) == 1415075158 and ActionMode == 0:  # int id for UV map
                        lx.eval("select.vertexMap {%s} txuv add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1415075158 and ActionMode == 1:  # int id for UV map
                        lx.eval("select.vertexMap {%s} txuv remove" % (VMap_NameList[i]))

                    # Seam map
                    if (VMap_TypeList[i]) == 1397047629 and ActionMode == 0:  # int id for Seam map
                        lx.eval("select.vertexMap {%s} seam add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1397047629 and ActionMode == 1:  # int id for seam map
                        lx.eval("select.vertexMap {%s} seam remove" % (VMap_NameList[i]))

                    #  Morph map
                    if (VMap_TypeList[i]) == 1297044038 and ActionMode == 0:  # int id for Morph map
                        lx.eval("select.vertexMap {%s} morf add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1297044038 and ActionMode == 1:  # int id for Morph map
                        lx.eval("select.vertexMap {%s} morf remove" % (VMap_NameList[i]))

                    # Vertex Normal map
                    if (VMap_TypeList[i]) == 1313821261 and ActionMode == 0:  # int id for Vertex Normal map
                        lx.eval("select.vertexMap {%s} norm add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1313821261 and ActionMode == 1:  # int id for Vertex Normal map
                        lx.eval("select.vertexMap {%s} norm remove" % (VMap_NameList[i]))

                    # B-Spline Weight map
                    if (VMap_TypeList[i]) == 1112756300 and ActionMode == 0:  # int id for B-Spline Weight map
                        lx.eval("select.vertexMap {%s} bspl add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1112756300 and ActionMode == 1:  # int id for B-Spline Weight map
                        lx.eval("select.vertexMap {%s} bspl remove" % (VMap_NameList[i]))

                    # Subdivision Weight map
                    if (VMap_TypeList[i]) == 1398096470 and ActionMode == 0:  # int id for Subdivision Weight map
                        lx.eval("select.vertexMap {%s} subd add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1398096470 and ActionMode == 1:  # int id for Subdivision Weight map
                        lx.eval("select.vertexMap {%s} subd remove" % (VMap_NameList[i]))

                    # Hard Edge Pick map
                    if (VMap_TypeList[i]) == 1212240452 and ActionMode == 0:  # int id for Hard Edge Pick map
                        lx.eval("select.vertexMap {%s} hard add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1212240452 and ActionMode == 1:  # int id for Hard Edge Pick map
                        lx.eval("select.vertexMap {%s} hard remove" % (VMap_NameList[i]))

        # mesh_list = scene.selectedByType(modo.constants.MESH_TYPE)
        # print(mesh_list)
        # for mesh in mesh_list:

        if VMapType > 0:
            for i in range(0, len(VMap_TypeList)):
                #  UV map
                if VMapType == 1:
                    if (VMap_TypeList[i]) == 1415075158 and ActionMode == 0:  # int id for UV map
                        lx.eval("select.vertexMap {%s} txuv add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1415075158 and ActionMode == 1:  # int id for UV map
                        lx.eval("select.vertexMap {%s} txuv remove" % (VMap_NameList[i]))

                # Seam map
                if VMapType == 2:
                    if (VMap_TypeList[i]) == 1397047629 and ActionMode == 0:  # int id for Seam map
                        lx.eval("select.vertexMap {%s} seam add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1397047629 and ActionMode == 1:  # int id for seam map
                        lx.eval("select.vertexMap {%s} seam remove" % (VMap_NameList[i]))

                #  Morph map
                if VMapType == 3:
                    if (VMap_TypeList[i]) == 1297044038 and ActionMode == 0:  # int id for Morph map
                        lx.eval("select.vertexMap {%s} morf add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1297044038 and ActionMode == 1:  # int id for Morph map
                        lx.eval("select.vertexMap {%s} morf remove" % (VMap_NameList[i]))

                # Vertex Normal map
                if VMapType == 4:
                    if (VMap_TypeList[i]) == 1313821261 and ActionMode == 0:  # int id for Vertex Normal map
                        lx.eval("select.vertexMap {%s} norm add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1313821261 and ActionMode == 1:  # int id for Vertex Normal map
                        lx.eval("select.vertexMap {%s} norm remove" % (VMap_NameList[i]))

                # B-Spline Weight map
                if VMapType == 5:
                    if (VMap_TypeList[i]) == 1112756300 and ActionMode == 0:  # int id for B-Spline Weight map
                        lx.eval("select.vertexMap {%s} bspl add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1112756300 and ActionMode == 1:  # int id for B-Spline Weight map
                        lx.eval("select.vertexMap {%s} bspl remove" % (VMap_NameList[i]))

                # Subdivision Weight map
                if VMapType == 6:
                    if (VMap_TypeList[i]) == 1398096470 and ActionMode == 0:  # int id for Subdivision Weight map
                        lx.eval("select.vertexMap {%s} subd add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1398096470 and ActionMode == 1:  # int id for Subdivision Weight map
                        lx.eval("select.vertexMap {%s} subd remove" % (VMap_NameList[i]))

                # Hard Edge Pick map
                if VMapType == 7:
                    if (VMap_TypeList[i]) == 1212240452 and ActionMode == 0:  # int id for Hard Edge Pick map
                        lx.eval("select.vertexMap {%s} hard add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1212240452 and ActionMode == 1:  # int id for Hard Edge Pick map
                        lx.eval("select.vertexMap {%s} hard remove" % (VMap_NameList[i]))

                # Weight map
                if VMapType == 8:
                    if (VMap_TypeList[i]) == 1464289364 and ActionMode == 0:  # int id for Weight map
                        lx.eval("select.vertexMap {%s} wght add" % (VMap_NameList[i]))
                    if (VMap_TypeList[i]) == 1464289364 and ActionMode == 1:  # int id for Weight map
                        lx.eval("select.vertexMap {%s} wght remove" % (VMap_NameList[i]))

        del VMap_NameList[:]
        del VMap_TypeList[:]
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END


lx.bless(SMO_GC_ClearSelectionVmap_Cmd, Cmd_Name)
