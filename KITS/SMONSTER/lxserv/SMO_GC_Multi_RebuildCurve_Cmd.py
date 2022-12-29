# python
"""
Name:         SMO_GC_Multi_RebuildCurve_Cmd.py

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

Cmd_Name = "smo.GC.Multi.RebuildCurve"


class SMO_GC_Multi_RebuildCurve_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("samplingPrecision", lx.symbol.sTYPE_DISTANCE)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)				# here the (0) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - (Multi) Rebuild Curve Data to Polyline'
    
    def cmd_Desc (self):
        return 'MULTI - Rebuild the current selected Mesh layer (curve Data) to Polylines'
    
    def cmd_Tooltip (self):
        return 'MULTI - Rebuild the current selected Mesh layer (curve Data) to Polylines'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - (Multi) Rebuild Curve Data to Polyline'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        samplingPrecision = self.dyna_Float (0)
        
        
        # ------------- ARGUMENTS Test
        # samplingPrecisionSize = 1
        # ------------- ARGUMENTS ------------- #
        
        # ------------- ARGUMENTS ------------- #
        args = lx.args()
        lx.out(args)
        # Draw Option OFF = 0 
        # Draw Option ON Wireframe = 1
        # Draw Option ON Shaded = 2
        # Draw Option ON Shaded & Wireframe = 3
        samplingPrecisionSize = samplingPrecision
        lx.out('Desired Resampling maximum size:', samplingPrecisionSize)
        # ------------- ARGUMENTS ------------- #
        
        
        
        
        
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
        # <---( SAFETY CHECK 2 )---> #
        # -------------------------- #
        
        # Component Selection Mode type --- START
        
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
            
        # Component Selection Mode type --- END
        # Component Selection Mode type --- END
            
        lx.out('-------------------------------')
        lx.out('Start of SMO_RebuildCurve Script')
        
        ##################### For Meshes ######################
        modo.dialogs.customFile('fileOpen', 'Import AI file (v8 Compatible only)', ('ai',), ('ai',), ('*.ai',))
        
        lx.eval('select.itemType light super:true')
        lx.eval('!item.delete')
        
        lx.eval('select.itemType camera')
        lx.eval('!item.delete')
        
        # Delete all empty (no Poly) Mesh layer in the scene
        lx.eval('smo.CLEANUP.DelEmptyMeshItem')
        
        # #variables
        # meshItemList = []
        # numOfVerts = ''
        
        # First we must select the scene and then all the mesh layers in our scene.
        # lx.eval('select.drop item')
        # lx.eval('select.layerTree all:1')
        # meshItemList = lx.eval('query sceneservice selection ? mesh') # mesh item layers
        
        # Create the monitor item
        # m = lx.Monitor()
        # m.init(len(meshItemList))
        
        # For each mesh item layer, we check to see if there are any verts in the layer...
        # for meshItem in meshItemList:
            # lx.eval('select.drop item')
            # lx.eval('select.item %s' % meshItem)
            # lx.eval('query layerservice layer.index ? selected') # scene
            # numOfVerts = lx.eval('query layerservice vert.N ? all')
            
            # If there are no verts, we delete the mesh item layer.
            # if numOfVerts == 0:
                # lx.eval('!item.delete')
            
            # Increare progress monitor
            # m.step(1)
        
        # Drop layer selection
        lx.eval('select.drop item')
        lx.eval('select.itemType mesh')
        
        lx.eval('item.create mesh')
        # Get the list of foreground layers by querying the layerservice "layers" attribute
        fgLayers = lx.evalN('query layerservice layers ? fg')
        
        lx.eval('item.componentMode polygon true')
        
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
        
        lx.eval('script.run "macro.scriptservice:32235710027:macro"')
        for layer in fgLayers :
            # Add this element to the selection
            lx.command('select.element',  layer=layer, type=selType, mode='add', index=3 )
        
        
        
        
        lx.eval('item.parent parent:{} inPlace:1')
        lx.eval('select.createSet Curve_Meshes')
        lx.eval('select.drop item locator')
        lx.eval('select.itemType groupLocator')
        lx.eval('!item.delete')
        lx.eval('select.itemType mesh')
        
        scene = modo.scene.current()
        meshes = scene.selectedByType(lx.symbol.sITYPE_MESH)
        locators = scene.selectedByType(lx.symbol.sITYPE_LOCATOR)
        for item in meshes:
            # Freeze the curve to Polygons
            lx.eval('poly.freeze face false 2 true true true false 20.0 false Morph')
            # lx.eval('%s' % item.id)
        
        lx.eval('select.drop item locator')
        lx.out('End of SMO_RebuildCurve Script')
        lx.out('-------------------------------')
        # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()
    
    
lx.bless(SMO_GC_Multi_RebuildCurve_Cmd, Cmd_Name)
