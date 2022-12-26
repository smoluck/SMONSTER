# python
"""
# Name:         SMO_MESHOPS_ExportMeshOpRigToFBXSequence_Cmd
# Version:      1.00
#
# Purpose:      This script is designed to
#               Export MeshOps rig as a freezed Mesh, over time, as an FBX sequence.
#               Select the MeshOp item and run.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      08/06/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.MESHOP.ExportMeshOpRigToFBXSequence"
# smo.MESHOP.ExportMeshOpRigToFBXSequence


class SMO_MESHOP_ExportMeshOpRigToFBXSequence_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Meshop - Export MeshOp Rig to FBX Sequence'

    def cmd_Desc(self):
        return 'Add a Meshop and add it to the Schematic.'

    def cmd_Tooltip(self):
        return 'Add a Meshop and add it to the Schematic.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Meshop - Export MeshOp Rig to FBX Sequence'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        # lx.eval('!!log.masterClear')
        scn = modo.Scene()
        # Get the Default UV Map name of the user
        DefaultUVMapName = lx.eval('pref.value application.defaultTexture ?')
        # lx.out('Current Default UV Map name:', DefaultUVMapName)

        CheckEmptyList = []
        ZeroUVMap = bool()

        VMap_NameList = []
        VMap_CountList = []
        VMap_TypeList = []
        UVMapNameList = []
        UVMapCountList = []

        # for mesh in scn.items('mesh'):
        #    mesh.select(True)
        #    lx.eval('smo.GC.ClearSelectionVmap 1 0')
        #    DetectedVMapCount = len(lx.evalN('vertMap.list all ?'))
        #    lx.out('Vmap Count:', DetectedVMapCount)
        #    # Get the name of UV Seam map available on mesh
        #    DetectedVMapName = lx.eval('vertMap.list txuv ?')
        #    lx.out('UVmap Name:', DetectedVMapName)
        #    UVMapNameList.append(DetectedVMapName)
        #    UVMapCountList.append(DetectedVMapCount)
        #    lx.eval('smo.GC.ClearSelectionVmap 1 1')

        for mesh in scn.items('mesh'):
            mesh.select(True)
            lx.eval('smo.GC.ClearSelectionVmap 1 1')
            meshobj = modo.Mesh()
            for map in meshobj.geometry.vmaps:
                mapObj = lx.object.MeshMap(map)
                VMap_Name = mapObj.Name()
                VMap_Type = mapObj.Type()
                if mapObj.Type() == 1415075158:
                    # print ('UVmap Name is %s' % VMap_Name)
                    VMap_CountList.append("True")
                    VMap_NameList.append(VMap_Name)
                    UVMapNameList.append(VMap_Name)
            # print(VMap_NameList)
            if VMap_NameList == CheckEmptyList and VMap_CountList == CheckEmptyList:
                #        VMap_NameList.append("Empty")
                #        UVMapCountList.append("Empty")
                print('No UVMap')
                ZeroUVMap = True
            if VMap_NameList != CheckEmptyList and VMap_CountList != CheckEmptyList:
                UVMapCountList.append(len(VMap_CountList))
                ZeroUVMap = False
                print('Detected UV Map count %s:' % (len(VMap_NameList)))
                # print('UVmap Detected', VMap_CountList)

            if not ZeroUVMap:
                lx.eval('select.vertexMap {%s} txuv replace' % (VMap_NameList[0]))
                DetectedVMapName = lx.eval('vertMap.list txuv ?')
                if DetectedVMapName != DefaultUVMapName:
                    lx.eval('vertMap.rename {%s} {%s} txuv active' % ((VMap_NameList[0]), DefaultUVMapName))
                    lx.out('UVMap {%s} renamed to {%s}' % ((VMap_NameList[0]), DefaultUVMapName))
            lx.eval('smo.GC.ClearSelectionVmap 1 1')
            del VMap_NameList[:]
            del VMap_CountList[:]
            del VMap_TypeList[:]
            del UVMapNameList[:]
            del UVMapCountList[:]
            # print('---------')
            # print('---------')
            if ZeroUVMap:
                lx.out('UVMap Renaming skipped, because not Detected')
                lx.eval('vertMap.new {%s} txuv' % DefaultUVMapName)
        del CheckEmptyList[:]
        del ZeroUVMap
        lx.eval('smo.GC.DeselectAll')


lx.bless(SMO_MESHOP_ExportMeshOpRigToFBXSequence_Cmd, Cmd_Name)
