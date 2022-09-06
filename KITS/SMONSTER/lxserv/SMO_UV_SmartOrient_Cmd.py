#python
#---------------------------------------
# Name:         SMO_UV_SmartOrient_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Orient the current UV Island (Horizontally or Vertically)
#               based on Poly or Edge Selection.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo, sys

Cmd_Name = "smo.UV.SmartOrient"
# smo.UV.SmartOrient 0

class SMO_UV_SmartOrient_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Orient Direction", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO UV - Smart Orient'
    
    def cmd_Desc (self):
        return 'Orient the current UV Island (Horizontally or Vertically) based on Poly or Edge Selection.'
    
    def cmd_Tooltip (self):
        return 'Orient the current UV Island (Horizontally or Vertically) based on Poly or Edge Selection.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO UV - Smart Orient'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        
        Int_OrientDir = self.dyna_Int (0)
        
        
        ############### 2 ARGUMENTS ###############
        args = lx.args()
        lx.out(args)
        # Orient U = 0
        # Orient V = 1
        OrientDir = Int_OrientDir
        lx.out('Orient Direction:',OrientDir)
        ############### ARGUMENTS ###############
        
        
        
        # Repack Off = 0
        # Repack On = 1
        RePack = lx.eval('user.value SMO_UseVal_UV_RepackAfterUnwrap ?')
        lx.out('RePack state:',RePack)
        
        # Relax UV Off = 0
        # Relax UV On = 1
        RelaxUV = lx.eval('user.value SMO_UseVal_UV_RelaxPostProcess ?')
        lx.out('RelaxUV state:',RelaxUV)
        
        UVRelaxIterCount = lx.eval('user.value SMO_UseVal_UV_RelaxIterCount ?')
        lx.out('RelaxUV iteration count:',UVRelaxIterCount)
        
        
        
        
        
        ################################
        #<----[ DEFINE VARIABLES ]---->#
        ################################
        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        lx.eval("user.defNew name:SMO_SafetyCheckUVOrient_PolygonModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheckUVOrient_min1PolygonSelected type:integer life:momentary")
        
        lx.eval("user.defNew name:SMO_SafetyCheckUVOrient_EdgeModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheckUVOrient_min1EdgeSelected type:integer life:momentary")
        
        lx.eval("user.defNew name:TotalSafetyCheckPolygon type:integer life:momentary")
        lx.eval("user.defNew name:TotalSafetyCheckEdge type:integer life:momentary")
        
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####
        
        
        
        ##############################
        ####### SAFETY CHECK 1 #######
        ##############################
        
        #####-------------------- safety check 1 : Only One Item Selected --- START --------------------#####
        try:
            # test if there is actually an item layer selected
            mesh = scene.selectedByType('mesh')[0]
            meshseam = modo.Scene().selected[0]
            # if this command return an error then i will select the corresponding mesh layer on the next step.
        except:
            ##############################
            ####### SAFETY CHECK 2 #######
            ##############################
        
            #####--------------------  safety check 2: Polygon or Edge Selection Mode enabled --- START --------------------#####
        
            selType = ""
            # Used to query layerservice for the list of polygons, edges or vertices.
            attrType = ""
        
            if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
                selType = "vertex"
                attrType = "vert"
                
                SMO_SafetyCheckUVOrient_PolygonModeEnabled = 0
                SMO_SafetyCheckUVOrient_EdgeModeEnabled = 0
                SMO_SafetyCheckUVOrient_VertexModeEnabled = 1
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {Unwrap_Smart:}')
                lx.eval('dialog.msg {You must be in Polygon or Edge Mode to run that script}')
                lx.eval('+dialog.open')
                lx.out('script Stopped: You must be in Polygon or Edge Mode to run that script')
                sys.exit
                #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
                
                
            elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
                selType = "edge"
                attrType = "edge"
                
                SMO_SafetyCheckUVOrient_VertexModeEnabled = 0
                SMO_SafetyCheckUVOrient_EdgeModeEnabled = 1
                SMO_SafetyCheckUVOrient_PolygonModeEnabled = 0
                SelectByLoop = 0
                lx.out('script Running: Edge Component Selection Mode')
                
            elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
                selType = "polygon"
                attrType = "poly"
                
                SMO_SafetyCheckUVOrient_VertexModeEnabled = 0
                SMO_SafetyCheckUVOrient_EdgeModeEnabled = 0
                SMO_SafetyCheckUVOrient_PolygonModeEnabled = 1
                lx.out('script Running: Polygon Component Selection Mode')
        
        
            else:
                # This only fails if none of the three supported selection
                # modes have yet been used since the program started, or
                # if "item" or "ptag" (ie: materials) is the current
                # selection mode.
                SMO_SafetyCheckUVOrient_VertexModeEnabled = 0
                SMO_SafetyCheckUVOrient_EdgeModeEnabled = 0
                SMO_SafetyCheckUVOrient_PolygonModeEnabled = 0
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {Unwrap_Smart:}')
                lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
                lx.eval('+dialog.open')
                lx.out('script Stopped: You must be in Polygon Mode to run that script')
                sys.exit
                #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
            #####--------------------  safety check 2: Polygon or Edge Selection Mode enabled --- END --------------------#####
            
            ItemLayerName = lx.eval('query layerservice layer.name ? 1')
            lx.out('Item Layer name is:', ItemLayerName)
            ItemLayerID = lx.eval('query layerservice layer.ID ?')
            lx.out('Item Layer ID is:', ItemLayerID)
            lx.eval('select.type item')
            lx.eval('select.item %s add' % ItemLayerID)
            if SMO_SafetyCheckUVOrient_EdgeModeEnabled == 1:
                lx.eval('select.type edge')
            elif SMO_SafetyCheckUVOrient_PolygonModeEnabled == 1 :
                lx.eval('select.type polygon')
            mesh = scene.selectedByType('mesh')[0]
            meshseam = modo.Scene().selected[0]
            
            
        ItemCount = lx.eval('query layerservice layer.N ? selected')
        lx.out('ItemCount', ItemCount)
        
        if ItemCount != 1:
            SMO_SafetyCheck_Only1MeshItemSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO Smart Unwrap:}')
            lx.eval('dialog.msg {You must select the Mesh Item layer you are working on, in Item List, to run that script}')
            lx.eval('+dialog.open')
            lx.out('Only One Item Selected result:', SMO_SafetyCheck_Only1MeshItemSelected)
            lx.out('script Stopped: Select only one Mesh Item')
            sys.exit
            
        elif ItemCount == 1:
            SMO_SafetyCheck_Only1MeshItemSelected = 1
            lx.out('Only One Item Selected:', SMO_SafetyCheck_Only1MeshItemSelected)
            lx.out('script running: right amount of Mesh Item selected')
        #####-------------------- safety check 1 : Only One Item Selected --- END --------------------#####
        
        
        
        CsPolys = len(mesh.geometry.polygons.selected)
        CsEdges = len(mesh.geometry.edges.selected)
        
        
        
        ##### UV SEAM Map Detection #####
        # MODO version checks.
        # Modo 13.0 and up have UV Seam map.
        # Version below 13.0 haven't
        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        lx.out('Modo Version:',Modo_ver)
        
        #Define the UV Seam vmap name Search case.
        lx.eval("user.defNew name:UVOrient_DesiredUVSEAMmapName type:string life:momentary")
        UVOrient_DesiredUVSEAMmapName = 'UV Seam'
        
        #Define the UV Seam vmap name Search case.
        lx.eval("user.defNew name:UVOrient_NoUVSeamMap type:string life:momentary")
        UVOrient_NoUVSeamMap = '_____n_o_n_e_____'
        
        
        # Get the number of UV Seam map available on mesh
        DetectedUVSEAMmapCount = len(lx.evalN('vertMap.list seam ?'))
        lx.out('UV SEAM Map Count:', DetectedUVSEAMmapCount)
        
        # Get the name of UV Seam map available on mesh
        DetectedUVSEAMmapName = lx.eval('vertMap.list seam ?')
        lx.out('UV SEAM Map Name:', DetectedUVSEAMmapName)
        ##### UV SEAM Map Detection #####
        
        
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####
            
        if Modo_ver >= 1300:
        ## UVSEAM Map Selection Check ##
            lx.out('<--- UVSEAM Map Safety Check --->')
            lx.out('<---------- START ---------->')
            if DetectedUVSEAMmapName == UVOrient_NoUVSeamMap:
                # lx.eval('vertMap.list seam ?')
                # lx.eval('vertMap.list seam _____n_e_w_____')
                lx.eval('vertMap.new "UV Seam" seam true {0.78 0.78 0.78} 2.0')
                lx.eval('vertMap.list seam "UV Seam"')
            
            elif DetectedUVSEAMmapName == UVOrient_DesiredUVSEAMmapName:
                lx.out('UV Map and UVSEAM Map Selected')
                lx.eval('vertMap.list seam "UV Seam"')
            # UserUVSEAMmapName = lx.eval1('query layerservice vmap.name ? %s' %UVSEAM_Selected)
            # lx.out('USER UVSEAM Map Name:', UserUVSEAMmapName)
            
            lx.out('<----------- END ----------->')
        ################################
        
        
        
        ##############################
        ####### SAFETY CHECK 2 #######
        ##############################
        
        #####--------------------  safety check 2: Polygon or Edge Selection Mode enabled --- START --------------------#####
        
        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""
        
        if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
            selType = "vertex"
            attrType = "vert"
            
            SMO_SafetyCheckUVOrient_PolygonModeEnabled = 0
            SMO_SafetyCheckUVOrient_EdgeModeEnabled = 0
            SMO_SafetyCheckUVOrient_VertexModeEnabled = 1
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {Unwrap_Smart:}')
            lx.eval('dialog.msg {You must be in Polygon or Edge Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon or Edge Mode to run that script')
            sys.exit
            #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
            
            
        elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
            selType = "edge"
            attrType = "edge"
            
            SMO_SafetyCheckUVOrient_VertexModeEnabled = 0
            SMO_SafetyCheckUVOrient_EdgeModeEnabled = 1
            SMO_SafetyCheckUVOrient_PolygonModeEnabled = 0
            SelectByLoop = 0
            lx.out('script Running: Edge Component Selection Mode')
            
        elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
            selType = "polygon"
            attrType = "poly"
            
            SMO_SafetyCheckUVOrient_VertexModeEnabled = 0
            SMO_SafetyCheckUVOrient_EdgeModeEnabled = 0
            SMO_SafetyCheckUVOrient_PolygonModeEnabled = 1
            lx.out('script Running: Polygon Component Selection Mode')
        
        
        
        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            SMO_SafetyCheckUVOrient_VertexModeEnabled = 0
            SMO_SafetyCheckUVOrient_EdgeModeEnabled = 0
            SMO_SafetyCheckUVOrient_PolygonModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {Unwrap_Smart:}')
            lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode to run that script')
            sys.exit
            #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        #####--------------------  safety check 2: Polygon or Edge Selection Mode enabled --- END --------------------#####
        
        
        
        ##############################
        ####### SAFETY CHECK 3 #######
        ##############################
        
        #####--------------------  safety check 3: at Least 1 Polygons is selected --- START --------------------#####
        if SMO_SafetyCheckUVOrient_PolygonModeEnabled == 1 and SMO_SafetyCheckUVOrient_EdgeModeEnabled == 0:
            lx.out('Count Selected Poly',CsPolys)
        
            if CsPolys < 1:
                SMO_SafetyCheckUVOrient_min1PolygonSelected = 0
                SMO_SafetyCheckUVOrient_min1EdgeSelected = 0
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {Unwrap_Smart:}')
                lx.eval('dialog.msg {You must select at least 1 Polygon or 3 Edges to run that script}')
                lx.eval('+dialog.open')
                lx.out('script Stopped: Add more Polygons to your selection')
                sys.exit
        
            elif CsPolys >= 1:
                SMO_SafetyCheckUVOrient_min1PolygonSelected = 1
                SMO_SafetyCheckUVOrient_min1EdgeSelected = 0
                lx.out('script running: right amount of polygons in selection')
        #####--------------------  safety check 3: at Least 1 Polygons is selected --- END --------------------#####
        
        
        
        #####--------------------  safety check 3: at Least 3 Edges are selected --- START --------------------#####
        if SMO_SafetyCheckUVOrient_EdgeModeEnabled == 1 and SMO_SafetyCheckUVOrient_PolygonModeEnabled == 0 :
            lx.out('Count Selected Edges',CsEdges)
        
            if CsEdges == 0 :
                SMO_SafetyCheckUVOrient_min1PolygonSelected = 0
                SMO_SafetyCheckUVOrient_min1EdgeSelected = 0
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {Unwrap_Smart:}')
                lx.eval('dialog.msg {You must select at least 1 Polygon or 3 Edges to run that script}')
                lx.eval('+dialog.open')
                lx.out('script Stopped: Add more Edges to your selection')
                sys.exit
        
            elif CsEdges >= 1 :
                SMO_SafetyCheckUVOrient_min1PolygonSelected = 0
                SMO_SafetyCheckUVOrient_min1EdgeSelected = 1
                lx.out('script running: right amount of Edges in selection')
        #####--------------------  safety check 3: at Least 3 Edges are selected --- END --------------------#####
        
        
        #####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
        #####
        TotalSafetyCheckTrueValuePoly = 3
        lx.out('Desired Value for Polygon Mode',TotalSafetyCheckTrueValuePoly)
        
        TotalSafetyCheckTrueValueEdge = 7
        lx.out('Desired Value for Edge Mode',TotalSafetyCheckTrueValueEdge)  
        
        TotalSafetyCheckPolygon = (SMO_SafetyCheck_Only1MeshItemSelected + SMO_SafetyCheckUVOrient_PolygonModeEnabled + SMO_SafetyCheckUVOrient_min1PolygonSelected)
        lx.out('Current Polygon Check Value',TotalSafetyCheckPolygon)
        
        TotalSafetyCheckEdge = (SMO_SafetyCheck_Only1MeshItemSelected + SMO_SafetyCheckUVOrient_EdgeModeEnabled + SMO_SafetyCheckUVOrient_min1EdgeSelected + 4)
        lx.out('Current Edge Check Value',TotalSafetyCheckEdge)
        
        
        
        #####
        #####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####
        
        
        
        ###############################################
        ## <----( Main Macro for Polygon Mode )----> ##
        ###############################################
        
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
        if TotalSafetyCheckPolygon == TotalSafetyCheckTrueValuePoly:
            lx.eval('select.type polygon')
            lx.eval('tool.viewType uv')
            if OrientDir == 0 :
                lx.eval('uv.orient horizontal')
            if OrientDir == 1 :
                lx.eval('uv.orient perpendicular')
            lx.eval('select.type polygon')
                
                
                
        ###############################################
        ## <----( Main Macro for Edge Mode )----> ##
        ###############################################
        
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
        if TotalSafetyCheckEdge == TotalSafetyCheckTrueValueEdge:
            lx.eval('select.type edge')
            lx.eval('tool.viewType uv')
            if OrientDir == 0 :
                lx.eval('uv.edgeAlign u')
            if OrientDir == 1 :
                lx.eval('uv.edgeAlign v')
            lx.eval('select.type edge')
        
        
        if SMO_SafetyCheckUVOrient_PolygonModeEnabled == 1 and SMO_SafetyCheckUVOrient_EdgeModeEnabled == 0:
            if TotalSafetyCheckPolygon != TotalSafetyCheckTrueValuePoly:
                lx.out('script Stopped: your mesh does not match the requirement for that script.')
                sys.exit
                
        if SMO_SafetyCheckUVOrient_PolygonModeEnabled == 0 and SMO_SafetyCheckUVOrient_EdgeModeEnabled == 1:
            if TotalSafetyCheckEdge != TotalSafetyCheckTrueValueEdge:
                lx.out('script Stopped: your mesh does not match the requirement for that script.')
                sys.exit

        lx.out('End of Unwrap_Smart Script')
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END --------------------#####


lx.bless(SMO_UV_SmartOrient_Cmd, Cmd_Name)
