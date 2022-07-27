#python
#---------------------------------------
# Name:         SMO_UV_NormalizePackByArea_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Normalize all the UV Islands and Pack
#               them in defined UV Space by Arguments.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo, sys

Cmd_Name = "smo.UV.NormalizePackByArea"

class SMO_UV_NormalizePackByArea_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Fix Flipped UV", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)                 # here the (0) define the argument index.
        self.dyna_Add("Orient Prepass Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Area Value U", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (2, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Area Value V", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (3, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO UV - Normalize Pack by Area'
    
    def cmd_Desc (self):
        return 'Normalize all the UV Islands and Pack them in defined UV Space by Arguments.'
    
    def cmd_Tooltip (self):
        return 'Normalize all the UV Islands and Pack them in defined UV Space by Arguments.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO UV - Normalize Pack by Area'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        mesh = scene.selectedByType('mesh')[0]
        #meshes = scene.selectedByType('mesh')      # to apply to all selected meshes
        
        
        Int_FixFlippedUV = self.dyna_Int (0)
        Int_Orient_Pass = self.dyna_Int (1)
        Int_ZoneAreaU = self.dyna_Int (2)
        Int_ZoneAreaV = self.dyna_Int (3)
        
        
        
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
        # FixFlippedUV = 1
        # Orient_Pass = 0
        # ZoneAreaU = -1
        # ZoneAreaV = -2
        # ############### ARGUMENT ###############
        
        
        
        ################################
        #<----[ DEFINE VARIABLES ]---->#
        ################################
        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        
        ## Vertex
        lx.eval("user.defNew name:SMO_SafetyCheckNPbA_VertexModeEnabled type:integer life:momentary")
        
        ## Edges
        lx.eval("user.defNew name:SMO_SafetyCheckNPbA_EdgeModeEnabled type:integer life:momentary")
        
        ## Polygon
        lx.eval("user.defNew name:SMO_SafetyCheckNPbA_PolygonModeEnabled type:integer life:momentary")
        ## Polygon Count
        lx.eval("user.defNew name:SMO_SafetyCheckNPbA_minPolygonSelected type:integer life:momentary")
        
        ## Item
        lx.eval("user.defNew name:SMO_SafetyCheckNPbA_ItemModeEnabled type:integer life:momentary")
        
        ## Selected UVmap Count
        lx.eval("user.defNew name:SMO_SafetyCheckNPbA_UVMapCount type:boolean life:momentary")
        ## Selected UVmap Name
        lx.eval("user.defNew name:NPbA_UVMapName type:string life:momentary")
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
        NPbA_UVMapName = lx.eval('user.value SMO_UV_SelectedMeshUVmapName ?')
        lx.out('Selected Mesh UV Maps Name:',NPbA_UVMapName)
        
        lx.eval('smo.GC.ClearSelectionVmap 1 1')
        lx.eval('select.vertexMap %s txuv replace' % NPbA_UVMapName)
        
        if SelectedMeshUVMapsCount > 1 :
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - Normalize and Pack:}')
            lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
            lx.eval('dialog.open')
            SMO_SafetyCheckNPbA_UVMapCount = False
            sys.exit()
        
        if SelectedMeshUVMapsCount < 1 :
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - Normalize and Pack:}')
            lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
            lx.eval('dialog.open')
            SMO_SafetyCheckNPbA_UVMapCount = False
            sys.exit()
        
        if SelectedMeshUVMapsCount == 1 :
            SMO_SafetyCheckNPbA_UVMapCount = True
            
        # UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' % UVmap_Selected)
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
            
            SMO_SafetyCheckNPbA_VertexModeEnabled = 1
            SMO_SafetyCheckNPbA_EdgeModeEnabled = 0
            SMO_SafetyCheckNPbA_PolygonModeEnabled = 0
            SMO_SafetyCheckNPbA_ItemModeEnabled = 0
            
            lx.out('script Running: Vertex Component Selection Mode')
            
            
        elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
            selType = "edge"
            attrType = "edge"
            
            SMO_SafetyCheckNPbA_VertexModeEnabled = 0
            SMO_SafetyCheckNPbA_EdgeModeEnabled = 1
            SMO_SafetyCheckNPbA_PolygonModeEnabled = 0
            SMO_SafetyCheckNPbA_ItemModeEnabled = 0
            
            lx.out('script Running: Edge Component Selection Mode')
            
        elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
            selType = "polygon"
            attrType = "poly"
            
            SMO_SafetyCheckNPbA_VertexModeEnabled = 0
            SMO_SafetyCheckNPbA_EdgeModeEnabled = 0
            SMO_SafetyCheckNPbA_PolygonModeEnabled = 1
            SMO_SafetyCheckNPbA_ItemModeEnabled = 0
            
            lx.out('script Running: Polygon Component Selection Mode')
        
        
        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            
            SMO_SafetyCheckNPbA_VertexModeEnabled = 0
            SMO_SafetyCheckNPbA_EdgeModeEnabled = 0
            SMO_SafetyCheckNPbA_PolygonModeEnabled = 0
            SMO_SafetyCheckNPbA_ItemModeEnabled = 1
            
            lx.out('script Running: Item Component Selection Mode')
        #####--------------------  safety check 2: Component Selection Mode type --- END --------------------#####
        
        
        ################################
        ## <----( Main Macro : )----> ##
        ################################
        if SMO_SafetyCheckNPbA_UVMapCount == True :
            if SMO_SafetyCheckNPbA_VertexModeEnabled == 1:
                lx.eval('select.type polygon')
                
            if SMO_SafetyCheckNPbA_EdgeModeEnabled == 1:
                lx.eval('select.type polygon')
                
            if SMO_SafetyCheckNPbA_ItemModeEnabled == 1:
                lx.eval('select.type polygon')
                
            if SMO_SafetyCheckNPbA_PolygonModeEnabled == 1:
                lx.eval('select.type polygon')
            
            
            # Select Area
            lx.eval('smo.UV.SelectUVArea %s %s' % (ZoneAreaU, ZoneAreaV) )
            
            # test if there is a selection of Polygons
            CsPolysNPbA = len(mesh.geometry.polygons.selected)
            lx.out('Count Selected Poly',CsPolysNPbA)
            
            if CsPolysNPbA < 1:
                SMO_SafetyCheckNPbA_min1PolygonSelected = 0
                lx.out('Normalize and Pack by Area state: DISABLE for this Area')
            
            if CsPolysNPbA >= 1 :
                lx.eval('select.editSet name:UV_NormPackedByArea mode:add')
                lx.eval('hide.unsel')
                lx.eval('select.drop polygon')
                lx.eval('tool.viewType uv')
            
            if FixFlippedUV == 1 :
                lx.eval('smo.UV.FixFlipped 0')
                lx.eval('select.drop polygon')
            
            if CsPolysNPbA >= 1 :
                lx.eval('select.useSet UV_NormPackedByArea replace')
                lx.eval('!select.deleteSet UV_NormPackedByArea false')
            
            if CsPolysNPbA >= 1 :
                lx.out('NP by Area U', ZoneAreaU)
                lx.out('NP by Area V', ZoneAreaV)
                lx.eval('texeldensity.normalize')
                if Orient_Pass == 0:
                    lx.eval('uv.pack true false false gaps:0.2 byPixel:true gapsByPixel:8.0 region:normalized udim:1001 regionX:0.0 regionY:0.0 regionW:1.0 regionH:1.0')
                    # lx.eval('uv.pack true true true auto 0.2 true 8.0 region:manual regionX:0 regionY:0 regionW:1.0 regionH:1.0')
                if Orient_Pass == 1:
                    lx.eval('uv.pack true false {%i} gaps:0.2 byPixel:true gapsByPixel:8.0 region:normalized udim:1001 regionX:0.0 regionY:0.0 regionW:1.0 regionH:1.0' % Orient_Pass)
                if Orient_Pass == 2:
                    lx.eval('uv.orient auto')
                    # replay name:"Pack UVs"
                    lx.eval('uv.pack true false true gaps:0.2 byPixel:true gapsByPixel:8.0 region:normalized udim:1001 regionX:0.0 regionY:0.0 regionW:1.0 regionH:1.0')
                lx.eval('tool.viewType uv')
                lx.eval('smo.UV.MoveToUVArea %s %s' % (ZoneAreaU, ZoneAreaV) )
                lx.eval('select.drop polygon')
            
            
            # replay name:"Unhide"
            lx.eval('unhide')
            
            if SMO_SafetyCheckNPbA_VertexModeEnabled == 1:
                lx.eval('select.type vertex')
            
            if SMO_SafetyCheckNPbA_EdgeModeEnabled == 1:
                lx.eval('select.type edge')
            
            if SMO_SafetyCheckNPbA_ItemModeEnabled == 1:
                lx.eval('select.type item')
                
                
            lx.eval('smo.GC.ClearSelectionVmap 2 1')
            lx.eval('smo.GC.ClearSelectionVmap 3 1')
            lx.eval('smo.GC.ClearSelectionVmap 4 1')
            lx.eval('smo.GC.ClearSelectionVmap 5 1')
            lx.eval('smo.GC.ClearSelectionVmap 6 1')
            lx.eval('smo.GC.ClearSelectionVmap 7 1')
        
    
lx.bless(SMO_UV_NormalizePackByArea_Cmd, Cmd_Name)
