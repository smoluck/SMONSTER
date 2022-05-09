# python
# ---------------------------------------
# Name:         SMO_CLEANUP_RenameVNrmMapToDefaultSceneWise_Cmd.py
# Version:      1.0
#
# Purpose:      Check for all Meshes in the current scene and rename their
#               first detected VertexNormal Map (by Index = 0) to Modo/Preferences/Defaults/Application name.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      21/10/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.Cleanup.RenameVNrmMapToDefaultSceneWise"
# smo.Cleanup.RenameVNrmMapToDefaultSceneWise

class SMO_CLEANUP_RenameVNrmMapToDefaultSceneWise_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CLEANUP RenameVNrmMapToDefaultSceneWise'

    def cmd_Desc(self):
        return 'Check for all Meshes in the current scene and rename their First VertexNormal Map (by Index = 0) to Modo/Preferences/Defaults/Application name.'

    def cmd_Tooltip(self):
        return 'Check for all Meshes in the current scene and rename their First VertexNormal Map (by Index = 0) to Modo/Preferences/Defaults/Application name.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CLEANUP RenameVNrmMapToDefaultSceneWise'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        #lx.eval('!!log.masterClear')
        scn = modo.Scene()
        # Get the Default UV Map name of the user
        DefaultVNrmMapName =  lx.eval('pref.value application.defaultVertexNormals ?')
        #lx.out('Current Default Vertex Normal Map name:', DefaultVNrmMapName)


        CheckEmptyList = []
        ZeroVNrmMap = bool()

        VMap_NameList = []
        VMap_CountList = []
        VMap_TypeList = []
        VNrmMapNameList = []
        VNrmMapCountList = []


        for mesh in scn.items('mesh'):
            mesh.select(True)
            lx.eval('smo.GC.ClearSelectionVmap 4 1')
            meshobj = modo.Mesh()
            for map in meshobj.geometry.vmaps:
                mapObj = lx.object.MeshMap(map)
                VMap_Name = mapObj.Name()
                VMap_Type = mapObj.Type()
                if mapObj.Type() == 1313821261 :
                    #print ('VertexNormalMap Name is %s' % VMap_Name)
                    VMap_CountList.append("True")
                    VMap_NameList.append(VMap_Name)
                    VNrmMapNameList.append(VMap_Name)
            # print(VMap_NameList)
            if VMap_NameList == CheckEmptyList and VMap_CountList == CheckEmptyList :
        #        VMap_NameList.append("Empty")
        #        VNrmMapCountList.append("Empty")
                 print('No VertexNormal Map')
                 ZeroVNrmMap = True
            if VMap_NameList != CheckEmptyList and VMap_CountList != CheckEmptyList :
                VNrmMapCountList.append(len(VMap_CountList))
                ZeroVNrmMap = False
                print('Detected Vertex Normal Map count %s:' % (len(VMap_NameList)))
                #print('VertexNormalMap Detected', VMap_CountList)

            if ZeroVNrmMap == False :
                lx.eval('select.vertexMap {%s} norm replace' % (VMap_NameList[0]))
                DetectedVMapName = lx.eval('vertMap.list norm ?')
                if DetectedVMapName != DefaultVNrmMapName :
                    lx.eval('vertMap.rename {%s} {%s} norm active' % ((VMap_NameList[0]), DefaultVNrmMapName))
                    lx.out('Vertex Normal Map {%s} renamed to {%s}'% ((VMap_NameList[0]), DefaultVNrmMapName))
            if ZeroVNrmMap == True :
                lx.out('Vertex Normal Map Renaming skipped, because not Detected')
            lx.eval('smo.GC.ClearSelectionVmap 4 1')
            del VMap_NameList[:]
            del VMap_CountList[:]
            del VMap_TypeList[:]
            del VNrmMapNameList[:]
            del VNrmMapCountList[:]
            # print('---------')
            # print('---------')
        del CheckEmptyList[:]
        del ZeroVNrmMap
        lx.eval('smo.GC.DeselectAll')

lx.bless(SMO_CLEANUP_RenameVNrmMapToDefaultSceneWise_Cmd, Command_Name)