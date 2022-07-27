#python
#---------------------------------------
# Name:         SMO_UV_UpdateUVSeamCutMap_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Update the UVseam Cut Map based on the current UVMap
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Cmd_Name ="smo.UV.UpdateUVSeamCutMap"
# smo.UV.UpdateUVSeamCutMap

class SMO_UV_UpdateUVSeamCutMap_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO UV - Update UVSeam CutMap'
    
    def cmd_Desc (self):
        return 'Update the UVseam Cut Map based on the current UVMap'
    
    def cmd_Tooltip (self):
        return 'Update the UVseam Cut Map based on the current UVMap'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO UV - Update UVSeam CutMap'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        mesh = scene.selectedByType('mesh')[0]
        # meshes = scene.selectedByType('mesh')       # to apply to all selected meshes
        meshseam = modo.Scene().selected[0]
        CsPolys = len(mesh.geometry.polygons.selected)
        CsEdges = len(mesh.geometry.edges.selected)
        CsVertex = len(mesh.geometry.vertices.selected)
        
        
        # MODO version checks.
        # Modo 13.0 and up have UV Seam map.
        # Version below 13.0 haven't
        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        lx.out('Modo Version:',Modo_ver)
        
        
        
        ################################
        #<----[ DEFINE VARIABLES ]---->#
        ################################
        
        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        
        ## Vertex
        lx.eval("user.defNew name:SMO_SafetyCheck_VertexModeEnabled type:integer life:momentary")
        
        lx.eval("user.defNew name:SMO_SafetyCheck_minVertexSelected type:integer life:momentary")
        
        ## Edges
        lx.eval("user.defNew name:SMO_SafetyCheck_EdgeModeEnabled type:integer life:momentary")
        
        lx.eval("user.defNew name:SMO_SafetyCheck_minEdgeSelected type:integer life:momentary")
        
        ## Polygon
        lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
        
        lx.eval("user.defNew name:SMO_SafetyCheck_minPolygonSelected type:integer life:momentary")
        
        ## Item
        lx.eval("user.defNew name:SMO_SafetyCheck_ItemModeEnabled type:integer life:momentary")
        
        ## Selected UVmap Count
        lx.eval("user.defNew name:SMO_SafetyCheck_UVUpdateUVSeam_UVMapCount type:boolean life:momentary")
        ## Selected UVmap Name
        lx.eval("user.defNew name:UVUpdateUVSeam_UVMapName type:string life:momentary")
        ## Selected UVmap Name
        lx.eval("user.defNew name:TargetUVSeammapPresent type:boolean life:momentary")
        
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####
        
        lx.eval('smo.GC.ClearSelectionVmap 2 1')
        lx.eval('smo.GC.ClearSelectionVmap 2 0')
        
        
        #####################################################
        ####### SAFETY CHECK 1 - One UVMap Selected ? #######
        #####################################################
        lx.out('<------------- START -------------->')
        lx.out('<--- UV Map Safety Check --->')
        # Get info about the selected UVMap.
        lx.eval('smo.UV.GetUVMapCountName 0 1 1')
        SelectedMeshUVMapsCount = lx.eval('user.value SMO_UV_SelectedMeshUVmapCount ?')
        lx.out('Selected Mesh UV Maps Count:',SelectedMeshUVMapsCount)
        UVUpdateUVSeam_UVMapName = lx.eval('user.value SMO_UV_SelectedMeshUVmapName ?')
        lx.out('Selected Mesh UV Maps Name:',UVUpdateUVSeam_UVMapName)
        
        lx.eval('smo.GC.ClearSelectionVmap 1 1')
        lx.eval('select.vertexMap %s txuv replace' % UVUpdateUVSeam_UVMapName)
        if SelectedMeshUVMapsCount > 1 :
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Planar:}')
            lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
            lx.eval('dialog.open')
            sys.exit()
            SMO_SafetyCheck_UVUpdateUVSeam_UVMapCount = False
        
        if SelectedMeshUVMapsCount < 1 :
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - UV - Unwrap Planar:}')
            lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
            lx.eval('dialog.open')
            sys.exit()
            SMO_SafetyCheck_UVUpdateUVSeam_UVMapCount = False
        
        if SelectedMeshUVMapsCount == 1 :
            SMO_SafetyCheck_UVUpdateUVSeam_UVMapCount = True
            
        # UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' % UVmap_Selected)
        # lx.out('USER UV Map Name:', UserUVMapName)
        lx.out('<- UV Map Safety Check ->')
        lx.out('<------------- END -------------->')
        ###############################################
        
        
        
        
        
        ######################################################
        ####### SAFETY CHECK 2 - UV Seam map Detection #######
        ######################################################
        lx.out('<------------- UV SEAM Map Detection -------------->')
        #Define the UV Seam vmap name Search case.
        lx.eval("user.defNew name:DesiredUVSEAMmapName type:string life:momentary")
        DesiredUVSEAMmapName = 'UVSeam_'
        
        lx.eval("user.defNew name:PrefixUVSEAMmapName type:string life:momentary")
        PrefixUVSEAMmapName = 'UVSeam'
        
        #Define the UV Seam vmap name Search case.
        lx.eval("user.defNew name:NoUVSeamMap type:string life:momentary")
        NoUVSeamMap = '_____n_o_n_e_____'
        
        UVSeamName = PrefixUVSEAMmapName + '_' + UVUpdateUVSeam_UVMapName
        lx.out('UV SEAM Map Expected Name:', UVSeamName)
        
        lx.eval('smo.GC.ClearSelectionVmap 2 0')
        # Get the number of UV Seam map available on mesh
        DetectedUVSEAMmapCount = len(lx.evalN('vertMap.list seam ?'))
        lx.out('UV SEAM Map Count:', DetectedUVSEAMmapCount)
        
        
        DetectedUVSEAMmapName = lx.eval('vertMap.list seam ?')
        lx.out('UV SEAM Map Name:', DetectedUVSEAMmapName)
        lx.eval('smo.GC.ClearSelectionVmap 2 1')
        
        UVSeamState = 3
        
        # No UV Seam Available. A New One will be created using UVMap name as Suffix
        if DetectedUVSEAMmapCount == 1 and DetectedUVSEAMmapName != UVSeamName and DetectedUVSEAMmapName == NoUVSeamMap :
            lx.out('No UV Seam Available. A New One will be created using UVMap name as Suffix')
            lx.out('No UV SEAM Map Detected:', DetectedUVSEAMmapName)
            UVSeamState = 0
            lx.out('UV SEAM State:', UVSeamState)
        
        
        # Detect if there is already the Targeted UV Seam map
        if DetectedUVSEAMmapCount >= 1 and UVSeamState != 0 and DetectedUVSEAMmapName != NoUVSeamMap :
            mesh = modo.Mesh()
            for map in mesh.geometry.vmaps:
                mapObj = lx.object.MeshMap(map)
                # print(mapObj.Name())
                # print(mapObj.Type())
                if mapObj.Type() == 1397047629: # int id for seam map
                    try :
                        lx.eval('!select.vertexMap {%s} seam add' % UVSeamName)
                        TargetUVSeammapPresent = True
                        lx.out('Target SEAM Present:', TargetUVSeammapPresent)
                        UVSeamState = 1
                        lx.out('UV SEAM State:', UVSeamState)
                    except :
                        TargetUVSeammapPresent = False
                        lx.out('Target SEAM Present:', TargetUVSeammapPresent)
        
        # UV Seam detected but a New One will be created and selected using UVMap name as Suffix
        if DetectedUVSEAMmapCount >= 1 and DetectedUVSEAMmapName != NoUVSeamMap and TargetUVSeammapPresent == False :
            lx.out('UV Seam detected but a New One will be created using UVMap name as Suffix')
            UVSeamState = 2
            lx.out('UV SEAM State:', UVSeamState)
        ##### UV SEAM Map Detection #####
        
        
        
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
        
        
        if Modo_ver >= 1300:
        ## UVSEAM Map Selection Check ##
            lx.out('<--- UVSEAM Map Safety Check --->')
            lx.out('<---------- START ---------->')
            if UVSeamState == 0 :
                # lx.eval('vertMap.list seam ?')
                # lx.eval('vertMap.list seam _____n_e_w_____')
                lx.eval('smo.GC.ClearSelectionVmap 2 1')
                lx.eval('vertMap.new %s seam true {0.78 0.78 0.78} 2.0' % UVSeamName)
                lx.eval('vertMap.list seam %s' % UVSeamName)
                lx.out('UV Map Selected and NEW UVSeam Map have been created')
            
            if UVSeamState == 1 :
                lx.eval('smo.GC.ClearSelectionVmap 2 1')
                lx.out('UV Map and corresponding UVSeam Map Selected')
                lx.eval('vertMap.list seam %s' % UVSeamName)
            
            if UVSeamState == 2 :
                lx.eval('smo.GC.ClearSelectionVmap 2 1')
                lx.eval('vertMap.new %s seam true {0.78 0.78 0.78} 2.0' % UVSeamName)
                lx.out('UV Map Selected and NEW corresponding UVSeam Map needs to be Created')
                lx.eval('vertMap.list seam %s' % UVSeamName)
                
            lx.out('<----------- END ----------->')
        ################################
        
        
        
        
        ##############################
        ## <----( Main Macro )----> ##
        ##############################
        
        #####--------------------  Compare SafetyCheck value and decide or not to continue the process  --- START --------------------#####
        if SMO_SafetyCheck_VertexModeEnabled == 1:
            lx.eval('select.type polygon')
            lx.eval('uv.selectBorder')
            lx.eval('seam.add')
            lx.eval('uv.selectBorder')
            lx.eval('select.invert')
            lx.eval('seam.clear')
            lx.eval('select.type vertex')
        
        if SMO_SafetyCheck_EdgeModeEnabled == 1:
            lx.eval('select.type polygon')
            lx.eval('uv.selectBorder')
            lx.eval('seam.add')
            lx.eval('uv.selectBorder')
            lx.eval('select.invert')
            lx.eval('seam.clear')
            lx.eval('select.type edge')
        
        if SMO_SafetyCheck_PolygonModeEnabled == 1:
            lx.eval('uv.selectBorder')
            lx.eval('seam.add')
            lx.eval('uv.selectBorder')
            lx.eval('select.invert')
            lx.eval('seam.clear')
            lx.eval('select.type polygon')
        
        if SMO_SafetyCheck_ItemModeEnabled == 1:
            lx.eval('select.type polygon')
            lx.eval('uv.selectBorder')
            lx.eval('seam.add')
            lx.eval('uv.selectBorder')
            lx.eval('select.invert')
            lx.eval('seam.clear')
            lx.eval('select.type item')
        
        lx.out('End of Update UVSeam Cut Map Script')
        #####--------------------  Compare SafetyCheck value and decide or not to continue the process  --- END --------------------#####
        
    
lx.bless(SMO_UV_UpdateUVSeamCutMap_Cmd, Cmd_Name)
