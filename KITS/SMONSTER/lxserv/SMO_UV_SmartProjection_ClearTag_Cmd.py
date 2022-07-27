#python
#---------------------------------------
# Name:         SMO_UV_SmartProjection_ClearTag_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Remove all Polygon Selection Set created 
#               with the UV - Smart Projection Scripts
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.UV.SmartProjectionClearTag"
# smo.UV.SmartProjectionClearTag

class SMO_UV_SmartProjection_ClearTag_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("UV Projection Axis", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
        self.dyna_Add("Negative Projection", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Rectangle Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (2, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Select by Loop Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (3, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Repack Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (4, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO UV - SmartProjection ClearTag'
    
    def cmd_Desc (self):
        return 'Remove all Polygon Selection Set created with the UV - Smart Projection Command.'
    
    def cmd_Tooltip (self):
        return 'Remove all Polygon Selection Set created with the UV - Smart Projection Command.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO UV - SmartProjection ClearTag'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        mesh = scene.selectedByType('mesh')[0]
        meshseam = modo.Scene().selected[0]
        CsPolys = len(mesh.geometry.polygons.selected)
        CsEdges = len(mesh.geometry.edges.selected)
        CsVertex = len(mesh.geometry.vertices.selected)
        
        
        ################################
        #<----[ DEFINE VARIABLES ]---->#
        ################################
        
        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        
        ## Vertex
        lx.eval("user.defNew name:SMO_SafetyCheck_VertexModeEnabled type:integer life:momentary")
        
        ## Edges
        lx.eval("user.defNew name:SMO_SafetyCheck_EdgeModeEnabled type:integer life:momentary")
        
        ## Polygon
        lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
        
        ## Item
        lx.eval("user.defNew name:SMO_SafetyCheck_ItemModeEnabled type:integer life:momentary")
        
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####
        
        
        ##############################
        ####### SAFETY CHECK 1 #######
        ##############################
        
        #####--------------------  safety check 1: Polygon Selection Mode enabled --- START --------------------#####
        
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
        
        #####--------------------  safety check 1: Polygon Selection Mode enabled --- END --------------------#####
        
        
        
        ##############################
        ## <----( Main Macro )----> ##
        ##############################
        
        #####--------------------  Compare SafetyCheck value and decide or not to continue the process  --- START --------------------#####
        if SMO_SafetyCheck_VertexModeEnabled == 1:
            lx.eval('select.type polygon')
            
        if SMO_SafetyCheck_EdgeModeEnabled == 1:
            lx.eval('select.type polygon')
            
        if SMO_SafetyCheck_ItemModeEnabled == 1:
            lx.eval('select.type polygon')
        
        try:
            lx.eval('!select.deleteSet UV_DONE false')
        except:
            pass
            
        try:  
            lx.eval('!select.deleteSet UV_DONE_X false')
        except:
            pass
            
        try:
            lx.eval('!select.deleteSet UV_DONE_Y false')
        except:
            pass
            
        try:
            lx.eval('!select.deleteSet UV_DONE_Z false')
        except:
            pass
            
        try:
            lx.eval('!select.deleteSet UV_DONE_FREE false')
        except:
            pass
            
            
        if SMO_SafetyCheck_VertexModeEnabled == 1:
            lx.eval('select.type vertex')
            
        if SMO_SafetyCheck_EdgeModeEnabled == 1:
            lx.eval('select.type edge')
            
        if SMO_SafetyCheck_ItemModeEnabled == 1:
            lx.eval('select.type item')
        
        lx.out('End of Smart Projection ClearTag Script')
        #####--------------------  Compare SafetyCheck value and decide or not to continue the process  --- END --------------------#####


lx.bless(SMO_UV_SmartProjection_ClearTag_Cmd, Cmd_Name)
