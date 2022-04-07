#python
#---------------------------------------
# Name:         SMO_UV_BuildingUnwrap_Cmd.py
# Version:      1.0
# 
# Purpose:      This script is designed to
#               Relax the UV's of the current Polygon Selection
# 
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
# 
# Created:      10/10/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

class SMO_UV_BuildingUnwrap_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO UV Building Unwrap'
    
    def cmd_Desc (self):
        return 'Relax the UVs of the current Polygon Selection.'
    
    def cmd_Tooltip (self):
        return 'Relax the UVs of the current Polygon Selection.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO UV Building Unwrap'
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        
        
        ##### UV SEAM Map Detection #####
        # MODO version checks.
        # Modo 13.0 and up have UV Seam map.
        # Version below 13.0 haven't
        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        lx.out('Modo Version:',Modo_ver)
        ##### UV SEAM Map Detection #####
        
        
        ################################
        #<----[ DEFINE VARIABLES ]---->#
        ################################
        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        lx.eval("user.defNew name:SMO_SafetyCheckUVBuildingUnwrap_UVConstraints type:string life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheckUVBuildingUnwrap_ReplaceUVSeamFailed type:integer life:momentary")
        ## Selected UVmap Count
        lx.eval("user.defNew name:SMO_SafetyCheckUVBuildingUnwrap_UVMapCount type:boolean life:momentary")
        ## Selected UVmap Name
        lx.eval("user.defNew name:UVRelaxBuildingUnwrap_UVMapName type:string life:momentary")
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####
        
        # lx.eval('smo.GC.ClearSelectionVmap 2 1')
        # lx.eval('smo.GC.ClearSelectionVmap 3 1')
        # lx.eval('smo.GC.ClearSelectionVmap 4 1')
        # lx.eval('smo.GC.ClearSelectionVmap 5 1')
        # lx.eval('smo.GC.ClearSelectionVmap 6 1')
        # lx.eval('smo.GC.ClearSelectionVmap 7 1')
        
        ###############################################
        ####### SAFETY CHECK 1 - UVMap Selected #######
        ###############################################
        lx.out('<------------- START -------------->')
        lx.out('<--- UV Map Safety Check --->')
        
        # Get info about the selected UVMap.
        lx.eval('smo.UV.GetUVMapCountName 0 1 1')
        SMO_SafetyCheckUVBuildingUnwrap_UVMapCount = lx.eval('user.value SMO_UV_SelectedMeshUVmapCount ?')
        lx.out('Selected Mesh UV Maps Count:',SMO_SafetyCheckUVBuildingUnwrap_UVMapCount)
        UVRelaxBuildingUnwrap_UVMapName = lx.eval('user.value SMO_UV_SelectedMeshUVmapName ?')
        lx.out('Selected Mesh UV Maps Name:',UVRelaxBuildingUnwrap_UVMapName)
        
        lx.eval('smo.GC.ClearSelectionVmap 1 1')
        lx.eval('select.vertexMap %s txuv replace' % UVRelaxBuildingUnwrap_UVMapName)
        
        if SMO_SafetyCheckUVBuildingUnwrap_UVMapCount > 1 :
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - Normalize and Pack:}')
            lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
            lx.eval('dialog.open')
            sys.exit()
            SMO_SafetyCheckUVRelax_UVMapCount = False
        
        if SMO_SafetyCheckUVBuildingUnwrap_UVMapCount < 1 :
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - Normalize and Pack:}')
            lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
            lx.eval('dialog.open')
            sys.exit()
            SMO_SafetyCheckUVRelax_UVMapCount = False
        
        if SMO_SafetyCheckUVBuildingUnwrap_UVMapCount == 1 :
            SMO_SafetyCheckUVRelax_UVMapCount = True
            
        # UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' %UVmap_Selected)
        # lx.out('USER UV Map Name:', UserUVMapName)
        lx.out('<- UV Map Safety Check ->')
        lx.out('<------------- END -------------->')
        ###############################################
        
        
        SMO_SafetyCheckUVBuildingUnwrap_ReplaceUVSeamFailed = 0
        SMO_SafetyCheckUVBuildingUnwrap_UVConstraints = 'UV Constraints'
        #### MAIN ACTION
        lx.eval('select.drop edge')
        lx.eval('select.edgeSharp 89.55 180.0')
        lx.eval('select.edge add bond equal (none)')
        lx.eval('smo.UV.UnwrapSmart 1 1 0 0')
        lx.eval('select.drop edge')
        ################
        
        
        # Get the number of UV Seam map available on mesh
        DetectedVMapPickCount = len(lx.evalN('vertMap.list pick ?'))
        lx.out('Vmap Pick Count:', DetectedVMapPickCount)
        # Get the name of UV Seam map available on mesh
        DetectedVMapPickName = lx.eval('vertMap.list pick ?')
        lx.out('Vmap Pick Name:', DetectedVMapPickName)
        ##### UV SEAM Map Detection #####
        ## UV Constraint Map Selection Check To bugfix the UV Constraint VMap creation ##
        lx.out('<--- UV Constraint Map Safety Check --->')
        lx.out('<---------- START ---------->')
        if Modo_ver <= 1399 :
            if DetectedVMapPickCount >= 1 and DetectedVMapPickName == SMO_SafetyCheckUVBuildingUnwrap_UVConstraints :
                lx.out('UV Constraints junk map detected')
                lx.eval('!vertMap.deleteByName pick "UV Constraints"')
                if Modo_ver >= 1300:
                    try:
                        lx.eval('!select.vertexMap "UV Seam" seam replace')
                    except:
                        SMO_SafetyCheckUVBuildingUnwrap_ReplaceUVSeamFailed = 1
                        # lx.out('UV Seam map NOT detected')
                    if SMO_SafetyCheckUVBuildingUnwrap_ReplaceUVSeamFailed == 1 :
                        lx.eval('smo.UV.UpdateUVSeamCutMap')
                        lx.eval('select.type polygon')
            elif DetectedVMapPickCount <= 0 and DetectedVMapPickName != SMO_SafetyCheckUVBuildingUnwrap_UVConstraints :
                lx.out('UV Constraints junk map NOT detected')
        
    
lx.bless(SMO_UV_BuildingUnwrap_Cmd, "smo.UV.BuildingUnwrap")