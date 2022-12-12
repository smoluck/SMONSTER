#python
#---------------------------------------
# Name:         SMO_UV_AutoCreateUVMap_Cmd.py
# Version:      1.0
# 
# Purpose:      This script is designed to
#               Automatically Create a UV Map if missing using Default UVMap Name in Preferences.
# 
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
# 
# Created:      11/12/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo, sys

Cmd_Name = "smo.UV.AutoCreateUVMap"
# smo.UV.AutoCreateUVMap

class SMO_UV_AutoCreateUVMap_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO UV - Auto Create UVMap'
    
    def cmd_Desc (self):
        return 'Automatically Create a UV Map if missing using Default UVMap Name in Preferences.'
    
    def cmd_Tooltip (self):
        return 'Automatically Create a UV Map if missing using Default UVMap Name in Preferences.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO UV - Auto Create UVMap'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        # Create a UV Map automatically in case there is no UVMaps
        DefaultUVMapName = lx.eval('pref.value application.defaultTexture ?')
        # print(DefaultUVMapName)

        m = modo.Mesh()
        # print(m.name)
        maps = m.geometry.vmaps.getMapsByType([lx.symbol.i_VMAP_TEXTUREUV])  # same as m.geometry.vmaps.uvMaps
        # print(maps)
        # print(len(maps))

        if len(maps) == 0:
            lx.eval('vertMap.new {%s} txuv' % DefaultUVMapName)
            print('New UVMap created')
            print('UV map name is: %s' % DefaultUVMapName)

        if len(maps) == 1:
            lx.eval('select.vertexMap {%s} txuv replace' % maps[0].name)

        # if len(maps) > 1:
        #     # get the current select UV Map name
        #     print(lx.eval('vertMap.list type:txuv ?'))

        SelectedMeshUVMapsCount = len(maps)
        UVUnwrapPlanar_UVMapName = (lx.eval('vertMap.list type:txuv ?'))
        lx.out('Selected Mesh UV Maps Name:', UVUnwrapPlanar_UVMapName)

        lx.eval('smo.GC.ClearSelectionVmap 1 1')
        lx.eval("select.vertexMap {%s} txuv replace" % UVUnwrapPlanar_UVMapName)
        
    
lx.bless(SMO_UV_AutoCreateUVMap_Cmd, Cmd_Name)
