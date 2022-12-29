# python
"""
Name:         SMO_GC_RebuildCurve_Cmd.py

Purpose:      This script is designed to
              Rebuild the current selected Mesh layer (curve Data) to Polylines.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      19/12/2019
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

Cmd_Name = "smo.GC.RebuildCurve"
# smo.GC.RebuildCurve


class SMO_GC_RebuildCurve_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("samplingPrecision", lx.symbol.sTYPE_DISTANCE)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)				# here the (0) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Rebuild Curve Data to Polyline'
    
    def cmd_Desc (self):
        return 'Rebuild the current selected Mesh layer (curve Data) to Polylines'
    
    def cmd_Tooltip (self):
        return 'Rebuild the current selected Mesh layer (curve Data) to Polylines'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Rebuild Curve Data to Polyline'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        # ------------- ARGUMENTS Test
        samplingPrecisionSize = 1
        # ------------- ARGUMENTS ------------- #
        
        # ------------- ARGUMENTS ------------- #
        # args = lx.args()
        # lx.out(args)
        # Draw Option OFF = 0 
        # Draw Option ON Wireframe = 1
        # Draw Option ON Shaded = 2
        # Draw Option ON Shaded & Wireframe = 3
        # samplingPrecisionSize = samplingPrecision
        # lx.out('Desired Resampling maximum size:', samplingPrecisionSize)
        # ------------- ARGUMENTS ------------- #
        
        
        # ---------------- COPY/PASTE Check Procedure ---------------- #
        ## create variables
        lx.eval("user.defNew name:User_Pref_CopyDeselectChangedState type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteSelectionChangedState type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteDeselectChangedState type:boolean life:momentary")
        
        lx.eval("user.defNew name:User_Pref_CopyDeselect type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteSelection type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteDeselect type:boolean life:momentary")
        ###################
        
        # Look at current Copy / Paste user Preferences:
        User_Pref_CopyDeselect = lx.eval('pref.value application.copyDeSelection ?')
        lx.out('User Pref: Deselect Elements after Copying', User_Pref_CopyDeselect)
        User_Pref_PasteSelection = lx.eval('pref.value application.pasteSelection ?')
        lx.out('User Pref: Select Pasted Elements', User_Pref_PasteSelection)
        User_Pref_PasteDeselect = lx.eval('pref.value application.pasteDeSelection ?')
        lx.out('User Pref: Deselect Elements Before Pasting', User_Pref_PasteDeselect)
        # Is Copy Deselect False ?
        if User_Pref_CopyDeselect == 0:
            lx.eval('pref.value application.copyDeSelection true')
            User_Pref_CopyDeselectChangedState = 1
            
        # Is Paste Selection False ?
        if User_Pref_PasteSelection == 0:
            lx.eval('pref.value application.pasteSelection true')
            User_Pref_PasteSelectionChangedState = 1
            
        # Is Paste Deselect False ?
        if User_Pref_PasteDeselect == 0:
            lx.eval('pref.value application.pasteDeSelection true')
            User_Pref_PasteDeselectChangedState = 1
            
        # Is Copy Deselect True ?
        if User_Pref_CopyDeselect == 1:
            User_Pref_CopyDeselectChangedState = 0
            
        # Is Paste Selection True ?
        if User_Pref_PasteSelection == 1:
            User_Pref_PasteSelectionChangedState = 0
            
        # Is Paste Deselect True ?
        if User_Pref_PasteDeselect == 1:
            User_Pref_PasteDeselectChangedState = 0
        # -------------------------------------------- #
        
        
        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        
        # ---------------- Define user value for all the different SafetyCheck --- START
        #####
        
        # Vertex
        lx.eval("user.defNew name:SMO_SafetyCheckIteCol_VertexModeEnabled type:integer life:momentary")
        
        # Edges
        lx.eval("user.defNew name:SMO_SafetyCheckIteCol_EdgeModeEnabled type:integer life:momentary")
        
        # Polygon
        lx.eval("user.defNew name:SMO_SafetyCheckIteCol_PolygonModeEnabled type:integer life:momentary")
        
        # Item
        lx.eval("user.defNew name:SMO_SafetyCheckIteCol_ItemModeEnabled type:integer life:momentary")
        
        #####
        # ---------------- Define user value for all the different SafetyCheck --- END
        
        
        
        # -------------------------- #
        # <---( SAFETY CHECK 1 )---> #
        # -------------------------- #
        
        # --------------------  safety check 1: Component Selection Mode type --- START
        
        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""
        
        if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
            selType = "vertex"
            attrType = "vert"
            
            SMO_SafetyCheckIteCol_VertexModeEnabled = 1
            SMO_SafetyCheckIteCol_EdgeModeEnabled = 0
            SMO_SafetyCheckIteCol_PolygonModeEnabled = 0
            SMO_SafetyCheckIteCol_ItemModeEnabled = 0
            
            lx.out('script Running: Vertex Component Selection Mode')
        
        elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
            selType = "edge"
            attrType = "edge"
            
            SMO_SafetyCheckIteCol_VertexModeEnabled = 0
            SMO_SafetyCheckIteCol_EdgeModeEnabled = 1
            SMO_SafetyCheckIteCol_PolygonModeEnabled = 0
            SMO_SafetyCheckIteCol_ItemModeEnabled = 0
            
            lx.out('script Running: Edge Component Selection Mode')
        
        elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
            selType = "polygon"
            attrType = "poly"
            
            SMO_SafetyCheckIteCol_VertexModeEnabled = 0
            SMO_SafetyCheckIteCol_EdgeModeEnabled = 0
            SMO_SafetyCheckIteCol_PolygonModeEnabled = 1
            SMO_SafetyCheckIteCol_ItemModeEnabled = 0
            
            lx.out('script Running: Polygon Component Selection Mode')
                
                
        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            
            SMO_SafetyCheckIteCol_VertexModeEnabled = 0
            SMO_SafetyCheckIteCol_EdgeModeEnabled = 0
            SMO_SafetyCheckIteCol_PolygonModeEnabled = 0
            SMO_SafetyCheckIteCol_ItemModeEnabled = 1
            
            lx.out('script Running: Item Component Selection Mode')
            
        # --------------------  safety check 1: Component Selection Mode type --- END
            
        
        lx.out('-------------------------------')
        lx.out('Start of SMO_RebuildCurve Script')
        
        
        lx.eval('select.itemType light super:true')
        lx.eval('!item.delete')
        
        lx.eval('select.itemType camera')
        lx.eval('!item.delete')
        
        
        # Delete all empty (no Poly) Mesh layer in the scene
        lx.eval('smo.CLEANUP.DelEmptyMeshItem')
        
        # Drop layer selection
        lx.eval('select.drop item')
        lx.eval('select.itemType mesh')
        
        lx.eval('item.parent parent:{} inPlace:1')
        lx.eval('select.createSet Curve_Meshes')
        lx.eval('select.drop item locator')
        lx.eval('select.itemType groupLocator')
        lx.eval('!item.delete')
        
        lx.eval('item.create mesh')
        
        lx.eval('item.componentMode polygon true')
        # Get the selected layer.
        CubeNormalSelect = lx.eval('query layerservice layers ? selected')
        # Select the first vertex.
        lx.eval('select.element layer:%d type:polygon mode:add index:1' % CubeNormalSelect)
        lx.eval('select.invert')
        lx.eval('!delete')
        lx.eval('select.invert')
        lx.eval('select.createSet Polyflip')
        lx.eval('copy')
        lx.eval('select.type item')
        lx.eval('!item.delete')
        
        lx.eval('select.type polygon')
        
        # Used with select.element to select polygons, edges or vertices.
        selType = ""
        
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""
        
        if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
            selType = "vertex"
            attrType = "vert"
            #lx.out( "- RandomSel.py - Vertex Selection Mode" )
        
        elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
            selType = "polygon"
            attrType = "poly"
            #lx.out( "- RandomSel.py - Polygon Selection Mode" )
        
        elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
            selType = "edge"
            attrType = "edge"
            #lx.out( "- RandomSel.py - Edge Selection Mode" )
        
        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            sys.exit( "LXe_FAILED:Must be in vertex, edge or polygon selection mode." )
        
        lx.eval('select.itemType mesh')
        
        scene = modo.scene.current()
        meshes = scene.selectedByType(lx.symbol.sITYPE_MESH)
        locators = scene.selectedByType(lx.symbol.sITYPE_LOCATOR)
        lx.eval('user.value llama_keepuvbounds false')
        lx.eval('user.value llama_keepmatbounds false')
        
        for item in meshes:
            # Freeze the curve to Polygons
            lx.eval('poly.freeze face false 2 true true true false 20.0 false Morph')
            lx.eval('select.type polygon')
            lx.eval('@SmartTriangulation.pl')
            lx.eval('select.drop polygon')
            lx.eval('paste')
            lx.eval('select.drop polygon')
            lx.eval('select.pickWorkingSet Polyflip true')
            # lx.eval('@lazySelect.pl selectAll')
            lx.eval('smo.GC.SelectCoPlanarPoly 2 2 1000')
            
            lx.eval("user.defNew name:polysFirstPasses type:integer life:momentary")
            polysFirstPasses = lx.eval('query layerservice poly.N ? selected')
            print(polysFirstPasses)
            if polysFirstPasses >= 1:
                lx.eval('select.invert')
                
            lx.eval("user.defNew name:polysSecondPasses type:integer life:momentary")
            polysSecondPasses = lx.eval('query layerservice poly.N ? selected')
            print(polysSecondPasses)
            if polysSecondPasses >= 1:
                lx.eval('poly.flip')
                
            lx.eval('select.drop polygon')
            lx.eval('select.pickWorkingSet Polyflip true')
            lx.eval('!delete')
            # lx.eval('%s' % item.id)
            
        # -------------- COPY/PASTE END Procedure  -------------- #
        # Restore user Preferences:
        if User_Pref_CopyDeselectChangedState == 1:
            lx.eval('pref.value application.copyDeSelection false')
            lx.out('"Deselect Elements after Copying" have been Restored')
        if User_Pref_PasteSelectionChangedState == 1:
            lx.eval('pref.value application.pasteSelection false')
            lx.out('"Select Pasted Elements" have been Restored')
        if User_Pref_PasteDeselectChangedState == 1:
            lx.eval('pref.value application.pasteDeSelection false')
            lx.out('"Deselect Elements Before Pasting" have been Restored')
        # -------------------------------------------- #
        
        
        lx.eval('select.drop item locator')
        lx.out('End of SMO_RebuildCurve Script')
        lx.out('-------------------------------')
        # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_RebuildCurve_Cmd, Cmd_Name)
