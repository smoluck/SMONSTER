#python
#---------------------------------------
# Name:         SMO_UV_MoveToUVArea_Cmd.py
# Version:      1.0
# 
# Purpose:      This script is designed to
#               Move selected Polygons to a defined  UV Area (Via Arguments).
# 
# 
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
# 
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo, sys

Cmd_Name = "smo.UV.MoveToUVArea"
# smo.UV.MoveToUVArea -1 -1

class SMO_UV_MoveToUVArea_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Area Value U", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)                 # here the (0) define the argument index.
        self.dyna_Add("Area Value V", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO UV - Move to UV Area'
    
    def cmd_Desc (self):
        return 'Move selected Polygons to a defined  UV Area (Via Arguments).'
    
    def cmd_Tooltip (self):
        return 'Move selected Polygons to a defined  UV Area (Via Arguments).'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO UV - Move to UV Area'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        mesh = scene.selectedByType('mesh')[0]
        
        
        Int_ZoneAreaU = self.dyna_Int (0)
        Int_ZoneAreaV = self.dyna_Int (1)
        
        ############### 2 ARGUMENTS ###############
        args = lx.args()
        lx.out(args)
        #
        #
        ZoneAreaU = Int_ZoneAreaU
        lx.out('Area Value U:',ZoneAreaU)
        # 
        # 
        ZoneAreaV = Int_ZoneAreaV
        lx.out('Area Value V:',ZoneAreaV)
        ############### ARGUMENTS ###############
        
        # ############### 2 ARGUMENT Test ###############
        # ZoneAreaU = -1
        # ZoneAreaV = -2
        # ############### ARGUMENT ###############
        
        
        
        
        
        ###############################################
        ####### SAFETY CHECK 1 - UVMap Selected #######
        ###############################################
        
        ##########################
        lx.out('<------------- START -------------->')
        lx.out('<--- UV Map Safety Check --->')
        
        # Get info about the selected UVMap.
        UVmap_Selected = lx.evalN('query layerservice vmaps ? selected')
        UVmap_SelectedN = len(lx.evalN('query layerservice vmaps ? selected'))
        lx.out('Selected UV Map Index:', UVmap_SelectedN)
        
        
        if UVmap_SelectedN <= 0:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - Normalize and Pack:}')
            lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
            lx.eval('dialog.open')
            sys.exit()
        
        if UVmap_SelectedN > 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - Normalize and Pack:}')
            lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
            lx.eval('dialog.open')
            sys.exit()
        
        
        UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' %UVmap_Selected)
        lx.out('USER UV Map Name:', UserUVMapName)	
        
        lx.out('<- UV Map Safety Check ->')
        lx.out('<------------- END -------------->')
        ##########################
        
        
        
        lx.eval('tool.set preset:TransformMove mode:on')
        lx.eval('tool.noChange')
        # Command Block Begin:
        lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:%s' %ZoneAreaU )
        lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:%s' %ZoneAreaV )
        # Command Block End:
        # Launch the Move Tool
        lx.eval('tool.doapply')
        lx.eval('tool.set preset:TransformMove mode:off')
        
    
lx.bless(SMO_UV_MoveToUVArea_Cmd, Cmd_Name)
