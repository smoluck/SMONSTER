# python
"""
Name:         SMO_UV_SelectUVArea_Cmd.py

Purpose:      This script is designed to:
              Select the Polygons in a defined UV Area (Via Arguments).

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      28/12/2018
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

Cmd_Name = "smo.UV.SelectUVArea"
# smo.UV.SelectUVArea -1 -1


class SMO_UV_SelectUVArea_Cmd(lxu.command.BasicCommand):
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
        return 'SMO UV - Select UV Area'
    
    def cmd_Desc (self):
        return 'Select the Polygons in a defined UV Area (Via Arguments).'
    
    def cmd_Tooltip (self):
        return 'Select the Polygons in a defined UV Area (Via Arguments).'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO UV - Select UV Area'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        mesh = scene.selectedByType('mesh')[0]
        # meshes = scene.selectedByType('mesh')       # to apply to all selected meshes
        
        
        Int_ZoneAreaU = self.dyna_Int (0)
        Int_ZoneAreaV = self.dyna_Int (1)
        
        # ------------- ARGUMENTS ------------- #
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
        # ------------- ARGUMENTS ------------- #
        
        
        
        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        # ---------------- Define user value for all the different SafetyCheck --- START
        #####
        ## UVmap Selected Count
        lx.eval("user.defNew name:SMO_SafetyCheckSelectUVArea_UVMapCount type:boolean life:momentary")
        #####
        # ---------------- Define user value for all the different SafetyCheck --- END
        
        
        
        # ----------------------------------------- #
        # <---( SAFETY CHECK 1 )---> UVMap Selected #
        # ----------------------------------------- #
        lx.out('<------------- START -------------->')
        lx.out('<--- UV Map Safety Check --->')
        
        # Get info about the selected UVMap.         UVMapsCount = len(item.geometry.vmaps.uvMaps)
        lx.eval('smo.UV.GetUVMapCountName 0 1 1')
        SelectedMeshUVMapsCount = lx.eval('user.value SMO_UV_SelectedMeshUVmapCount ?')
        lx.out('Selected Mesh UV Maps Count:',SelectedMeshUVMapsCount)
        SelectedMeshUVMapsName = lx.eval('user.value SMO_UV_SelectedMeshUVmapName ?')
        lx.out('Selected Mesh UV Maps Name:',SelectedMeshUVMapsName)
        
        if SelectedMeshUVMapsCount > 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - Normalize and Pack:}')
            lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
            lx.eval('dialog.open')
            SMO_SafetyCheckSelectUVArea_UVMapCount = False
            sys.exit()
        
        if SelectedMeshUVMapsCount < 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - Normalize and Pack:}')
            lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
            lx.eval('dialog.open')
            SMO_SafetyCheckSelectUVArea_UVMapCount = False
            sys.exit()
        
        if SelectedMeshUVMapsCount == 1:
            SMO_SafetyCheckSelectUVArea_UVMapCount = True
            
        # UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' % UVmap_Selected)
        # lx.out('USER UV Map Name:', UserUVMapName)
        lx.out('<- UV Map Safety Check ->')
        lx.out('<------------- END -------------->')
        ###############################################
        
        
        
        # -------------------------- #
        # <----( Main Macro : )----> #
        # -------------------------- #
        if SMO_SafetyCheckSelectUVArea_UVMapCount:
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            lx.eval('tool.set util.udim on')
            lx.eval('tool.noChange')
            #Command Block Begin:
            lx.eval('tool.attr util.udim manual true')
            lx.eval('tool.attr util.udim posU %s' %ZoneAreaU )
            lx.eval('tool.attr util.udim posV %s' %ZoneAreaV )
            lx.eval('tool.attr util.udim width 1.0')
            lx.eval('tool.attr util.udim height 1.0')
            #Command Block End:
            lx.eval('tool.doApply')
            lx.eval('udim.select')
            lx.eval('tool.set util.udim off')
        
    
lx.bless(SMO_UV_SelectUVArea_Cmd, Cmd_Name)
