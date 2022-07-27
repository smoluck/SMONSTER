#python
#---------------------------------------
# Name:         SMO_UV_NormalizePackAllArea_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Normalize all the UV Islands and Pack
#               them on every Areas (Unwrap, Planar, Cylindrical).
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo, sys

Cmd_Name = "smo.UV.NormalizePackAllArea"
# smo.UV.NormalizePackAllArea 0 0

class SMO_UV_NormalizePackAllArea_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Fix Flipped UV", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)                 # here the (0) define the argument index.
        self.dyna_Add("Orient Prepass Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO UV - Normalize Pack All Areas'
    
    def cmd_Desc (self):
        return 'Normalize all the UV Islands and Pack them on every Areas (Unwrap, Planar, Cylindrical).'
    
    def cmd_Tooltip (self):
        return 'Normalize all the UV Islands and Pack them on every Areas (Unwrap, Planar, Cylindrical).'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO UV - Normalize Pack All Areas'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        mesh = scene.selectedByType('mesh')[0]
        # meshes = scene.selectedByType('mesh')       # to apply to all selected meshes
        
        
        Int_FixFlippedUV = self.dyna_Int (0)
        Int_Orient_Pass = self.dyna_Int (1)
        
        
        
        ############### 2 ARGUMENTS ###############
        args = lx.args()
        lx.out(args)
        # no Flipped = 0
        # Flipped U = 1
        # Flipped U = 2
        FixFlippedUV = Int_FixFlippedUV
        lx.out('Fix Flipped error UV Island:',FixFlippedUV)
        # Orient preprocess OFF = 0
        # Orient preprocess ON = 1
        Orient_Pass = Int_Orient_Pass
        lx.out('Orient preprocess state:',Orient_Pass)
        ############### ARGUMENTS ###############
        
        
        
        # ############### 2 ARGUMENT Test ###############
        # FixFlippedUV = 1
        # Orient_Pass = 0
        # ############### ARGUMENT ###############
        
        
        
        ################################
        #<----[ DEFINE VARIABLES ]---->#
        ################################
        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        
        ## UVmap Selected Count
        lx.eval("user.defNew name:SMO_SafetyCheckNPAllArea_UVMapCount type:boolean life:momentary")
        ## Selected UVmap Name
        lx.eval("user.defNew name:NPAllArea_UVMapName type:string life:momentary")
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####
        
        
        
        lx.eval('smo.GC.ClearSelectionVmap 2 1')
        lx.eval('smo.GC.ClearSelectionVmap 3 1')
        lx.eval('smo.GC.ClearSelectionVmap 4 1')
        lx.eval('smo.GC.ClearSelectionVmap 5 1')
        lx.eval('smo.GC.ClearSelectionVmap 6 1')
        lx.eval('smo.GC.ClearSelectionVmap 7 1')
        lx.eval('smo.GC.ClearSelectionVmap 8 1')
        
        
        
        
        ###############################################
        ####### SAFETY CHECK 1 - UVMap Selected #######
        ###############################################
        lx.out('<------------- START -------------->')
        lx.out('<--- UV Map Safety Check --->')
        
        # Get info about the selected UVMap.
        lx.eval('smo.UV.GetUVMapCountName 0 1 1')
        SelectedMeshUVMapsCount = lx.eval('user.value SMO_UV_SelectedMeshUVmapCount ?')
        lx.out('Selected Mesh UV Maps Count:',SelectedMeshUVMapsCount)
        NPAllArea_UVMapName = lx.eval('user.value SMO_UV_SelectedMeshUVmapName ?')
        lx.out('Selected Mesh UV Maps Name:',NPAllArea_UVMapName)
        
        lx.eval('smo.GC.ClearSelectionVmap 1 1')
        lx.eval('select.vertexMap %s txuv replace' % NPAllArea_UVMapName)
        
        if SelectedMeshUVMapsCount > 1 :
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - Normalize and Pack:}')
            lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
            lx.eval('dialog.open')
            SMO_SafetyCheckNPAllArea_UVMapCount = False
            sys.exit()
        
        if SelectedMeshUVMapsCount < 1 :
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - Normalize and Pack:}')
            lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
            lx.eval('dialog.open')
            SMO_SafetyCheckNPAllArea_UVMapCount = False
            sys.exit()
        
        if SelectedMeshUVMapsCount == 1 :
            SMO_SafetyCheckNPAllArea_UVMapCount = True
            
        # UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' %UVmap_Selected)
        # lx.out('USER UV Map Name:', UserUVMapName)
        lx.out('<- UV Map Safety Check ->')
        lx.out('<------------- END -------------->')
        ###############################################
        
        
        
        ################################
        ## <----( Main Macro : )----> ##
        ################################
        if SMO_SafetyCheckNPAllArea_UVMapCount == True :
            
            # Unwrap Areas
            lx.eval('smo.UV.NormalizePackByArea %s %s 0 -1' % (FixFlippedUV, Orient_Pass) )  # Unwrap Conform
            lx.eval('smo.UV.NormalizePackByArea %s %s 1 -1' % (FixFlippedUV, Orient_Pass) )  # Unwrap Angle Based
            lx.eval('smo.UV.NormalizePackByArea %s %s 0 -2' % (FixFlippedUV, Orient_Pass) )  # Unwrap Rectangle
            
            # Rectangle Oriented
            lx.eval('smo.UV.NormalizePackByArea %s %s 1 0' % (FixFlippedUV, Orient_Pass) )  # Rectangle Horizontal
            lx.eval('smo.UV.NormalizePackByArea %s %s 1 1' % (FixFlippedUV, Orient_Pass) )  # Rectangle Vertical
            
            # Planar Areas
            lx.eval('smo.UV.NormalizePackByArea %s %s -2 1' % (FixFlippedUV, Orient_Pass) )  # Planar Free
            lx.eval('smo.UV.NormalizePackByArea %s %s -2 0' % (FixFlippedUV, Orient_Pass) )  # Planar X
            lx.eval('smo.UV.NormalizePackByArea %s %s -1 0' % (FixFlippedUV, Orient_Pass) )  # Planar Y
            lx.eval('smo.UV.NormalizePackByArea %s %s -1 1' % (FixFlippedUV, Orient_Pass) )  # Planar Z
            
            # Cylindrical Areas
            lx.eval('smo.UV.NormalizePackByArea %s %s -2 -1' % (FixFlippedUV, Orient_Pass) )  # Cylindrical Free
            lx.eval('smo.UV.NormalizePackByArea %s %s -2 -2' % (FixFlippedUV, Orient_Pass) )  # Cylindrical X
            lx.eval('smo.UV.NormalizePackByArea %s %s -1 -2' % (FixFlippedUV, Orient_Pass) )  # Cylindrical Y
            lx.eval('smo.UV.NormalizePackByArea %s %s -1 -1' % (FixFlippedUV, Orient_Pass) )  # Cylindrical Z
            
            lx.eval('select.drop polygon')


lx.bless(SMO_UV_NormalizePackAllArea_Cmd, Cmd_Name)
