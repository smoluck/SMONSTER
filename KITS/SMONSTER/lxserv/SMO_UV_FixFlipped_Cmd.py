#python
#---------------------------------------
# Name:         SMO_UV_FixFlipped_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Fix the Flipped UVs in the current UVMap.
# 
#
# Author:       Franck ELISABETH
# Website:      ttp://www.smoluck.com
#
# Created:      01/07/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

class SMO_UV_FixFlipped_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("UV Flip Axis Value", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO UV FixFlipped'
    
    def cmd_Desc (self):
        return 'Fix the Flipped UVs in the current UVMap.'
    
    def cmd_Tooltip (self):
        return 'Fix the Flipped UVs in the current UVMap.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO UV FixFlipped'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        mesh = scene.selectedByType('mesh')[0]
        # meshes = scene.selectedByType('mesh')       # to apply to all selected meshes
        
        # MODO version checks.
        # Modo 13.0 and up have UV Seam map.
        # Version below 13.0 haven't
        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        lx.out('Modo Version:',Modo_ver)
        
        
        
        Int_FlipAxes = self.dyna_Int (0)
        
        
        
        ############### 1 ARGUMENT ###############
        args = lx.args()
        lx.out(args)
        # Flip U = 0
        # Flip V = 1
        FlipAxes = Int_FlipAxes
        lx.out('Desired flip axes:',FlipAxes)
        ############### ARGUMENT ###############
        
        
        
        # ############### 1 ARGUMENT Test ###############
        # FlipAxes = 0
        # ############### ARGUMENT ###############
        
        
        
        ################################
        #<----[ DEFINE VARIABLES ]---->#
        ################################
        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
        
        # Selected UVmap Count
        lx.eval("user.defNew name:SMO_SafetyCheck_UVFixflipped_UVMapCount type:boolean life:momentary")
        ## Selected UVmap Name
        lx.eval("user.defNew name:UVFixflippedSoloV_UVMapName type:string life:momentary")
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####
        
        
        
        lx.eval('smo.GC.ClearSelectionVmap 2 1')
        lx.eval('smo.GC.ClearSelectionVmap 3 1')
        lx.eval('smo.GC.ClearSelectionVmap 4 1')
        lx.eval('smo.GC.ClearSelectionVmap 5 1')
        lx.eval('smo.GC.ClearSelectionVmap 6 1')
        lx.eval('smo.GC.ClearSelectionVmap 7 1')
        
        
        
        ###############################################
        ####### SAFETY CHECK 1 - UVMap Selected #######
        ###############################################
        lx.out('<------------- START -------------->')
        lx.out('<--- UV Map Safety Check --->')
        
        # Get info about the selected UVMap.
        lx.eval('smo.UV.GetUVMapCountName 0 1 1')
        SelectedMeshUVMapsCount = lx.eval('user.value SMO_UV_SelectedMeshUVmapCount ?')
        lx.out('Selected Mesh UV Maps Count:',SelectedMeshUVMapsCount)
        UVFixflipped_UVMapName = lx.eval('user.value SMO_UV_SelectedMeshUVmapName ?')
        lx.out('Selected Mesh UV Maps Name:',UVFixflipped_UVMapName)
        
        lx.eval('smo.GC.ClearSelectionVmap 1 1')
        lx.eval('select.vertexMap %s txuv replace' % UVFixflipped_UVMapName)
        
        if SelectedMeshUVMapsCount > 1 :
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV Fix flipped:}')
            lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
            lx.eval('dialog.open')
            sys.exit()
            SMO_SafetyCheck_UVFixflipped_UVMapCount = False
        
        if SelectedMeshUVMapsCount < 1 :
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV Fix flipped:}')
            lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
            lx.eval('dialog.open')
            sys.exit()
            SMO_SafetyCheck_UVFixflipped_UVMapCount = False
        
        if SelectedMeshUVMapsCount == 1 :
            SMO_SafetyCheck_UVFixflipped_UVMapCount = True
            
        # UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' %UVmap_Selected)
        # lx.out('USER UV Map Name:', UserUVMapName)
        lx.out('<- UV Map Safety Check ->')
        lx.out('<------------- END -------------->')
        ###############################################
        
        
        
        ################################################
        ####### SAFETY CHECK 2 -  Selection Mode #######
        ################################################
        
        #####--------------------  safety check 2: Component Selection Mode type --- START --------------------#####
        
        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""
        
        if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
            selType = "vertex"
            attrType = "vert"
            
            SMO_SafetyCheck_VertexModeEnabled = 1
            SMO_SafetyCheck_EdgeModeEnabled = 0
            SMO_SafetyCheck_PolygonModeEnabled = 0
            SMO_SafetyCheck_ItemModeEnabled = 0
            
            lx.out('script Running: Vertex Component Selection Mode')
            
            
        elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
            selType = "edge"
            attrType = "edge"
            
            SMO_SafetyCheck_VertexModeEnabled = 0
            SMO_SafetyCheck_EdgeModeEnabled = 1
            SMO_SafetyCheck_PolygonModeEnabled = 0
            SMO_SafetyCheck_ItemModeEnabled = 0
            
            lx.out('script Running: Edge Component Selection Mode')
            
        elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
            selType = "polygon"
            attrType = "poly"
            
            SMO_SafetyCheck_VertexModeEnabled = 0
            SMO_SafetyCheck_EdgeModeEnabled = 0
            SMO_SafetyCheck_PolygonModeEnabled = 1
            SMO_SafetyCheck_ItemModeEnabled = 0
            
            lx.out('script Running: Polygon Component Selection Mode')
        
        
        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            
            SMO_SafetyCheck_VertexModeEnabled = 0
            SMO_SafetyCheck_EdgeModeEnabled = 0
            SMO_SafetyCheck_PolygonModeEnabled = 0
            SMO_SafetyCheck_ItemModeEnabled = 1
            
            lx.out('script Running: Item Component Selection Mode')
        
        #####--------------------  safety check 2: Component Selection Mode type --- END --------------------#####
        
        
        
        if SMO_SafetyCheck_VertexModeEnabled == 1:
            lx.eval('select.type polygon')
            SMO_SafetyCheck_PolygonModeEnabled = 1
            
        if SMO_SafetyCheck_EdgeModeEnabled == 1:
            lx.eval('select.type polygon')
            SMO_SafetyCheck_PolygonModeEnabled = 1
            
        if SMO_SafetyCheck_ItemModeEnabled == 1:
            lx.eval('select.type polygon')
            SMO_SafetyCheck_PolygonModeEnabled = 1
            
        if SMO_SafetyCheck_PolygonModeEnabled == 1:
            lx.eval('select.type polygon')
            SMO_SafetyCheck_PolygonModeEnabled = 1
        
        
        lx.eval('select.uvOverlap {%s} false false true false false false' % UVFixflipped_UVMapName)
        
        # Test if the Polygon selection count
        CsPolys = len(mesh.geometry.polygons.selected)
        lx.out('Count Selected Poly',CsPolys)
        
        if CsPolys < 1 :
            SMO_SafetyCheck_min1PolygonSelected = 0
            lx.out('script running: No Flipped UV Island')
        
        elif CsPolys >= 1 :
            SMO_SafetyCheck_min1PolygonSelected = 1
            lx.out('script running: Flipped UV Island Detected')
        
        
        #####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
        #####
        TotalSafetyCheckTrueValue = 2
        lx.out('Desired Value',TotalSafetyCheckTrueValue)
        TotalSafetyCheck = (SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
        lx.out('Current Value',TotalSafetyCheck)
        #####
        #####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####
        
        
        ##############################
        ## <----( Main Macro )----> ##
        ##############################
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
        if SMO_SafetyCheck_UVFixflipped_UVMapCount == True :
            if TotalSafetyCheckTrueValue == TotalSafetyCheck :
                if CsPolys < 1:
                    SMO_SafetyCheck_min1PolygonSelected = 0
                    lx.out('No UV Island to Flip')
            
                if CsPolys >= 1:
                    SMO_SafetyCheck_min1PolygonSelected = 1
                    lx.out('script running: right amount of polygons in selection')
                    if FlipAxes == 0:
                        lx.eval('uv.flip false u')
                    if FlipAxes == 1:
                        lx.eval('uv.flip false v')
                    # lx.eval('select.drop polygon')
            
                if SMO_SafetyCheck_VertexModeEnabled == 1:
                    lx.eval('select.type vertex')
            
                if SMO_SafetyCheck_EdgeModeEnabled == 1:
                    lx.eval('select.type edge')
            
                if SMO_SafetyCheck_ItemModeEnabled == 1:
                    lx.eval('select.type item')
        
        elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
                lx.out('No UV Island to Flip')
            
        lx.out('End of SMO_UV_FixFlipped Script')
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END --------------------#####
lx.bless(SMO_UV_FixFlipped_Cmd, "smo.UV.FixFlipped")
# smo.UV.FixFlipped 1