# python
# ---------------------------------------
# Name:         SMO_CLEANUP_RenameUVMapToDefaultSceneWise_Cmd.py
# Version:      1.0
#
# Purpose:      Check for all Meshes in the current scene and rename their
#               first detected UVMap (by Index = 0) to Modo/Preferences/Defaults/Application name.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      21/10/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.Cleanup.RenameUVMapToDefaultSceneWise"
# smo.Cleanup.RenameUVMapToDefaultSceneWise

class SMO_CLEANUP_RenameUVMapToDefaultSceneWise_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CLEANUP RenameUVMapToDefaultSceneWise'

    def cmd_Desc(self):
        return 'Check for all Meshes in the current scene and rename their First UVMap (by Index = 0) to Modo/Preferences/Defaults/Application name.'

    def cmd_Tooltip(self):
        return 'Check for all Meshes in the current scene and rename their First UVMap (by Index = 0) to Modo/Preferences/Defaults/Application name.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CLEANUP RenameUVMapToDefaultSceneWise'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        #lx.eval('!!log.masterClear')
        scn = modo.Scene()
        # Get the Default UV Map name of the user
        DefaultUVMapName =  lx.eval('pref.value application.defaultTexture ?')
        #lx.out('Current Default UV Map name:', DefaultUVMapName)


        CheckEmptyList = []
        ZeroUVMap = bool()

        VMap_NameList = []
        VMap_CountList = []
        VMap_TypeList = []
        UVMapNameList = []
        UVMapCountList = []


        #for mesh in scn.items('mesh'):
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
                if mapObj.Type() == 1415075158 :
                    #print ('UVmap Name is %s' % VMap_Name)
                    VMap_CountList.append("True")
                    VMap_NameList.append(VMap_Name)
                    UVMapNameList.append(VMap_Name)
            # print(VMap_NameList)
            if VMap_NameList == CheckEmptyList and VMap_CountList == CheckEmptyList :
        #        VMap_NameList.append("Empty")
        #        UVMapCountList.append("Empty")
                 print('No UVMap')
                 ZeroUVMap = True
            if VMap_NameList != CheckEmptyList and VMap_CountList != CheckEmptyList :
                UVMapCountList.append(len(VMap_CountList))
                ZeroUVMap = False
                print('Detected UV Map count %s:' % (len(VMap_NameList)))
                #print('UVmap Detected', VMap_CountList)

            if ZeroUVMap == False :
                lx.eval('select.vertexMap {%s} txuv replace' % (VMap_NameList[0]))
                DetectedVMapName = lx.eval('vertMap.list txuv ?')
                if DetectedVMapName != DefaultUVMapName :
                    lx.eval('vertMap.rename {%s} {%s} txuv active' % ((VMap_NameList[0]), DefaultUVMapName))
                    lx.out('UVMap {%s} renamed to {%s}'% ((VMap_NameList[0]), DefaultUVMapName))
            if ZeroUVMap == True :
                lx.out('UVMap Renaming skipped, because not Detected')
            lx.eval('smo.GC.ClearSelectionVmap 1 1')
            del VMap_NameList[:]
            del VMap_CountList[:]
            del VMap_TypeList[:]
            del UVMapNameList[:]
            del UVMapCountList[:]
            # print('---------')
            # print('---------')
        del CheckEmptyList[:]
        del ZeroUVMap
        lx.eval('smo.GC.DeselectAll')

lx.bless(SMO_CLEANUP_RenameUVMapToDefaultSceneWise_Cmd, Command_Name)