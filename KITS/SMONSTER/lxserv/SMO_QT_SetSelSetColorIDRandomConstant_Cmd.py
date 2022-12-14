#python
#---------------------------------------
# Name:         SMO_QT_SetSelSetColorIDRandomConstant_Cmd.py
# Version:      1.00
#
# Purpose:      This script is designed to
#               Set a random Diffuse Color override
#               using Selection Set (polygons) and Constant item on the selected Mesh Layers
# 
# 
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      12/01/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import modo, lx, lxu, random

Cmd_Name = "smo.QT.SetSelSetColorIDRandomConstant"
# smo.QT.SetSelSetColorIDRandomConstant

def ListPSelSet():
    # scene service, reference of the scene and a channel read object
    scene_svc = lx.service.Scene()
    scene = lxu.select.SceneSelection().current()
    chan_read = scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, 0.0)

    # current selected items in scene
    selection = lxu.select.ItemSelection().current()

    # Get a int ID for the item type.
    # type_mesh = scene_svc.ItemTypeLookup(lx.symbol.sITYPE_MESH)
    type_mesh = lx.symbol.i_CIT_MESH

    # Find the first meshItem in the selection
    for item in selection:
        if item.TestType(type_mesh):
            meshItem = item
            break
        else:
            meshItem = None

    # Read the mesh channel from the item to get the mesh object
    mesh_obj = chan_read.ValueObj(meshItem, meshItem.ChannelLookup(lx.symbol.sICHAN_MESH_MESH))
    mesh = lx.object.Mesh(mesh_obj)  # mesh object

    # Get the selection sets from the mesh with PICK and save them into a list
    selSets = []
    num_polset = mesh.PTagCount(lx.symbol.i_PTAG_PICK)
    for i in xrange(0, num_polset):
        selSets.append(mesh.PTagByIndex(lx.symbol.i_PTAG_PICK, i))
    # lx.out('selSets:', selSets)
    return selSets


class SMO_QT_SetSelSetColorIDRandomConstant_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        # print(self.SelModeVert)
        # print(self.SelModeEdge)
        # print(self.SelModePoly)
        # print(self.SelModeItem)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO QT - Set ColorID Random (by SelSet and Constant)'
    
    def cmd_Desc (self):
        return 'Set a random Diffuse Color override using Selection Set (polygons) and Constant item on the selected Mesh Layers.'
    
    def cmd_Tooltip (self):
        return 'Set a random Diffuse Color override using Selection Set (polygons) and Constant item on the selected Mesh Layers.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO QT - Set ColorID Random (by SelSet and Constant)'
    
    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        ColorID_Suffix = "ColorID"
        ByItemMode = bool()

        if self.SelModeItem == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
            lx.eval('select.type polygon')
            lx.eval('select.all')
            ByItemMode = True

        if self.SelModePoly == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
            ByItemMode = False

        # mesh = scene.selectedByType('mesh')[0]
        # CsPolys = len(mesh.geometry.polygons.selected)
        meshes = scene.selectedByType('mesh')
        # lx.eval('query layerservice layer.id ? main')# select main layer
        # ItemUniqueName = lx.eval('query layerservice layer.id ? main')# store the Unique name of the current mesh layer
        # lx.out('Item Unique Name:', ItemUniqueName)

        PrstColorIDRed = 0
        PrstColorIDMagenta = 1
        PrstColorIDPink = 2
        PrstColorIDBrown = 3
        PrstColorIDOrange = 4
        PrstColorIDYellow = 5
        PrstColorIDGreen = 6
        PrstColorIDLightGreen = 7
        PrstColorIDCyan = 8
        PrstColorIDBlue = 9
        PrstColorIDLightBlue = 10
        PrstColorIDUltramarine = 11
        PrstColorIDPurple = 12
        PrstColorIDLightPurple = 13
        PrstColorIDDarkGrey = 14
        PrstColorIDGrey = 15
        PrstColorIDWhite = 16

        ################################
        # <----[ DEFINE VARIABLES ]---->#
        ################################

        # #####--- Define user value for all the different SafetyCheck --- START ---#####
        # #####
        # lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
        # lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
        # #####
        # #####--- Define user value for all the different SafetyCheck --- END ---#####

        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        lx.eval("user.defNew name:SceneConstantID type:integer life:momentary")
        lx.eval("user.defNew name:ColorID_Suffix type:string life:momentary")
        lx.eval("user.defNew name:ColorIDSelSetName type:string life:momentary")
        lx.eval("user.defNew name:NewID type:string life:momentary")
        lx.eval("user.defNew name:Const_Suffix type:string life:momentary")
        lx.eval("user.defNew name:ColorIDConstantName type:string life:momentary")
        ###################

        # ##############################
        # ####### SAFETY CHECK 1 #######
        # ##############################
        #
        # #####--------------------  safety check 1: Polygon Selection Mode enabled --- START --------------------#####
        #
        # selType = ""
        # # Used to query layerservice for the list of polygons, edges or vertices.
        # attrType = ""
        #
        # if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
        #     selType = "vertex"
        #     attrType = "vert"
        #
        #     SMO_SafetyCheck_PolygonModeEnabled = 0
        #     lx.eval('dialog.setup info')
        #     lx.eval('dialog.title {SMO QT - Set ColorID:}')
        #     lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
        #     lx.eval('+dialog.open')
        #     lx.out('script Stopped: You must be in Polygon Mode to run that script')
        #     sys.exit
        #     #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        #
        #
        # elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
        #     selType = "edge"
        #     attrType = "edge"
        #
        #     SMO_SafetyCheck_PolygonModeEnabled = 0
        #     lx.eval('dialog.setup info')
        #     lx.eval('dialog.title {SMO QT - Set ColorID:}')
        #     lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
        #     lx.eval('+dialog.open')
        #     lx.out('script Stopped: You must be in Polygon Mode to run that script')
        #     sys.exit
        #     #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        #
        # elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
        #     selType = "polygon"
        #     attrType = "poly"
        #
        #     SMO_SafetyCheck_PolygonModeEnabled = 1
        #     lx.out('script Running: Correct Component Selection Mode')
        #
        #
        # else:
        #     # This only fails if none of the three supported selection
        #     # modes have yet been used since the program started, or
        #     # if "item" or "ptag" (ie: materials) is the current
        #     # selection mode.
        #     SMO_SafetyCheck_PolygonModeEnabled = 0
        #     lx.eval('dialog.setup info')
        #     lx.eval('dialog.title {SMO QT - Set ColorID:}')
        #     lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
        #     lx.eval('+dialog.open')
        #     lx.out('script Stopped: You must be in Polygon Mode to run that script')
        #     sys.exit
        #     #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        # #####--------------------  safety check 1: Polygon Selection Mode enabled --- END --------------------#####
        #
        #
        #
        #
        # ##############################
        # ####### SAFETY CHECK 2 #######
        # ##############################
        #
        # #####--------------------  safety check 2: at Least 1 Polygons is selected --- START --------------------#####
        # lx.out('Count Selected Poly',CsPolys)
        #
        # if CsPolys < 1:
        #     SMO_SafetyCheck_min1PolygonSelected = 0
        #     lx.eval('dialog.setup info')
        #     lx.eval('dialog.title {SMO QT - Set ColorID:}')
        #     lx.eval('dialog.msg {You must select at least 1 polygon to run that script}')
        #     lx.eval('+dialog.open')
        #     lx.out('script Stopped: Add more polygons to your selection')
        #     sys.exit
        #
        # elif CsPolys >= 1:
        #     SMO_SafetyCheck_min1PolygonSelected = 1
        #     lx.out('script running: right amount of polygons in selection')
        # #####--------------------  safety check 2: at Least 1 Polygons is selected --- END --------------------#####
        #
        #
        #
        # #####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
        # #####
        # TotalSafetyCheckTrueValue = 2
        # lx.out('Desired Value',TotalSafetyCheckTrueValue)
        # TotalSafetyCheck = (SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
        # lx.out('Current Value',TotalSafetyCheck)
        # #####
        # #####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####

        ##############################
        ## <----( Main Macro )----> ##
        ##############################

        # #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
        # Select the Base Shader to create and place ColorID group on top of current Material Groups

        ### Selection of ShaderItem have been dedicated to custom command below smo.QT.SelectBaseShader.
        # SceneShaderItemList = []
        # SceneShaderItemName = []
        # for item in scene.items(itype='defaultShader', superType=True):
        #     # lx.out('Default Base Shader found:',item)
        #     SceneShaderItemList.append(item)
        #     # print(item.id)
        #     SceneShaderItemName.append(item.id)
        # scene.select(SceneShaderItemList[0])
        # # print(SceneShaderItemName)

        lx.eval('smo.QT.SelectBaseShader')
        SceneShaderItemID = []
        for item in scene.items(itype='defaultShader', superType=True):
            if item.name == "Base Shader":
                SceneShaderItemID.append(item.id)
        # print('Base Shader item Id is:', SceneShaderItemID)


        def uNameItem():
            item = modo.item.Item()
            return item.UniqueName()

        def ItemIdent():
            item = modo.item.Item()
            return item.Ident()

        QTChannelExist = bool()
        NewID = int()

        try:
            lx.eval(
                '!channel.create SelSetColorIDConstantGlobalCount integer useMin:true default:(-1.0) username:SelSetColorIDConstantGlobalCount')
            SceneConstantID = (-1)
            QTChannelExist = False
        except RuntimeError:  # diffuse amount is zero.
            lx.eval('select.channel {%s:SelSetColorIDConstantGlobalCount@lmb=x} set' % SceneShaderItemID[0])
            QTChannelExist = True
            # lx.out('ColorID  Global Count channel already created')
            pass

        if QTChannelExist == True:
            SceneConstantID = lx.eval('!item.channel SelSetColorIDConstantGlobalCount ?')
            lx.out('Constant ID Max in scene', SceneConstantID)
        # print(QTChannelExist)

        # print(SceneConstantID)

        if SceneConstantID == (-1):
            NewID = 0
        if SceneConstantID >= 0:
            NewID = int(SceneConstantID) + 1
        # print(NewID)
        lx.eval('!item.channel SelSetColorIDConstantGlobalCount %i' % NewID)
        ColorIDSelSetName = ("%s_%s" % (ColorID_Suffix, NewID))
        # lx.out('Color ID Selection set name:', ColorIDSelSetName)

        lx.eval('select.editSet {%s} add' % ColorIDSelSetName)

        lx.eval('shader.create mask')
        GrpMask = scene.selected
        scene.select(GrpMask)

        if NewID <= 16:
            try:
                if NewID == PrstColorIDRed:
                    lx.eval('item.editorColor red')
                elif NewID == PrstColorIDMagenta:
                    lx.eval('item.editorColor magenta')
                elif NewID == PrstColorIDPink:
                    lx.eval('item.editorColor pink')
                elif NewID == PrstColorIDBrown:
                    lx.eval('item.editorColor brown')
                elif NewID == PrstColorIDOrange:
                    lx.eval('item.editorColor orange')
                elif NewID == PrstColorIDYellow:
                    lx.eval('item.editorColor yellow')
                elif NewID == PrstColorIDGreen:
                    lx.eval('item.editorColor green')
                elif NewID == PrstColorIDLightGreen:
                    lx.eval('item.editorColor lightgreen')
                elif NewID == PrstColorIDCyan:
                    lx.eval('item.editorColor cyan')
                elif NewID == PrstColorIDBlue:
                    lx.eval('item.editorColor blue')
                elif NewID == PrstColorIDLightBlue:
                    lx.eval('item.editorColor lightblue')
                elif NewID == PrstColorIDUltramarine:
                    lx.eval('item.editorColor ultramarine')
                elif NewID == PrstColorIDPurple:
                    lx.eval('item.editorColor purple')
                elif NewID == PrstColorIDLightPurple:
                    lx.eval('item.editorColor lightpurple')
                elif NewID == PrstColorIDDarkGrey:
                    lx.eval('item.editorColor darkgrey')
                elif NewID == PrstColorIDGrey:
                    lx.eval('item.editorColor grey')
                elif NewID == PrstColorIDWhite:
                    lx.eval('item.editorColor white')
            except RuntimeError:  # diffuse amount is zero.
                pass
        lx.eval('mask.setPTagType "Selection Set"')
        lx.eval('mask.setPTag {%s}' % ColorIDSelSetName)

        lx.eval('shader.create constant')
        if NewID <= 16:
            try:
                if NewID == PrstColorIDRed:
                    lx.eval('item.editorColor red')
                elif NewID == PrstColorIDMagenta:
                    lx.eval('item.editorColor magenta')
                elif NewID == PrstColorIDPink:
                    lx.eval('item.editorColor pink')
                elif NewID == PrstColorIDBrown:
                    lx.eval('item.editorColor brown')
                elif NewID == PrstColorIDOrange:
                    lx.eval('item.editorColor orange')
                elif NewID == PrstColorIDYellow:
                    lx.eval('item.editorColor yellow')
                elif NewID == PrstColorIDGreen:
                    lx.eval('item.editorColor green')
                elif NewID == PrstColorIDLightGreen:
                    lx.eval('item.editorColor lightgreen')
                elif NewID == PrstColorIDCyan:
                    lx.eval('item.editorColor cyan')
                elif NewID == PrstColorIDBlue:
                    lx.eval('item.editorColor blue')
                elif NewID == PrstColorIDLightBlue:
                    lx.eval('item.editorColor lightblue')
                elif NewID == PrstColorIDUltramarine:
                    lx.eval('item.editorColor ultramarine')
                elif NewID == PrstColorIDPurple:
                    lx.eval('item.editorColor purple')
                elif NewID == PrstColorIDLightPurple:
                    lx.eval('item.editorColor lightpurple')
                elif NewID == PrstColorIDDarkGrey:
                    lx.eval('item.editorColor darkgrey')
                elif NewID == PrstColorIDGrey:
                    lx.eval('item.editorColor grey')
                elif NewID == PrstColorIDWhite:
                    lx.eval('item.editorColor white')
            except RuntimeError:  # diffuse amount is zero.
                pass

        Const_Suffix = "Constant"
        ColorIDConstantName = ("%s_%s" % (Const_Suffix, ColorIDSelSetName))
        lx.eval('item.name %s constant' % ColorIDConstantName)
        # print(ColorIDSelSetName)

        Constant = lx.eval('query sceneservice selection ? textureLayer')
        # lx.out('Constant item name',Constant)

        if NewID <= 16:
            try:
                if NewID == PrstColorIDRed:
                    lx.eval('!item.channel constant$color {1.0 0.0844 0.0382} item:{%s}' % Constant)
                elif NewID == PrstColorIDMagenta:
                    lx.eval('!item.channel constant$color {0,8632 0,0802 0,3968} item:{%s}' % Constant)
                elif NewID == PrstColorIDPink:
                    lx.eval('!item.channel constant$color {0.807 0.1946 0.1946} item:{%s}' % Constant)
                elif NewID == PrstColorIDBrown:
                    lx.eval('!item.channel constant$color {0.402 0.2232 0.0704} item:{%s}' % Constant)
                elif NewID == PrstColorIDOrange:
                    lx.eval('!item.channel constant$color {1.0 0.4793 0.0497} item:{%s}' % Constant)
                elif NewID == PrstColorIDYellow:
                    lx.eval('!item.channel constant$color {1.0 0,8149 0,0452} item:{%s}' % Constant)
                elif NewID == PrstColorIDGreen:
                    lx.eval('!item.channel constant$color {0,0423 0,7682 0,0423} item:{%s}' % Constant)
                elif NewID == PrstColorIDLightGreen:
                    lx.eval('!item.channel constant$color {0.2832 0.9131 0.2832} item:{%s}' % Constant)
                elif NewID == PrstColorIDCyan:
                    lx.eval('!item.channel constant$color {0,0382 0,9911 0,7454} item:{%s}' % Constant)
                elif NewID == PrstColorIDBlue:
                    lx.eval('!item.channel constant$color {0,0529 0,5029 1.0} item:{%s}' % Constant)
                elif NewID == PrstColorIDLightBlue:
                    lx.eval('!item.channel constant$color {0,2232 0,624 1.0} item:{%s}' % Constant)
                elif NewID == PrstColorIDUltramarine:
                    lx.eval('!item.channel constant$color {0.1274 0.2502 1.0} item:{%s}' % Constant)
                elif NewID == PrstColorIDPurple:
                    lx.eval('!item.channel constant$color {0,3763 0,2423 0,8308} item:{%s}' % Constant)
                elif NewID == PrstColorIDLightPurple:
                    lx.eval('!item.channel constant$color {0.624 0.4179 1.0} item:{%s}' % Constant)
                elif NewID == PrstColorIDDarkGrey:
                    lx.eval('!item.channel constant$color {0,2423 0,2423 0,2423} item:{%s}' % Constant)
                elif NewID == PrstColorIDGrey:
                    lx.eval('!item.channel constant$color {0.4852 0.4852 0.4852} item:{%s}' % Constant)
                elif NewID == PrstColorIDWhite:
                    lx.eval('!item.channel constant$color {0.855 0.855 0.855} item:{%s}' % Constant)
            except RuntimeError:  # diffuse amount is zero.
                pass

        if NewID > 16:
            from random import randrange
            r, g, b = [randrange(0, 255, 10) / 255.0 for i in range(3)]
            try:
                lx.eval('!item.channel constant$color {%s %s %s} item:{%s}' % (r, g, b, Constant))
            except RuntimeError:  # diffuse amount is zero.
                pass

        ## Parent current ColorID Mask under BaseShader even if there is other Shader items in the scene
        lx.eval('smo.GC.DeselectAll')
        lx.eval('smo.QT.SelectBaseShader')
        baseShad = lx.eval('query sceneservice defaultShader.parent ? {Base Shader}')
        # print(baseShad)
        scene.select(GrpMask)
        TargetGrpMask = ItemIdent()
        # print(TargetGrpMask)
        lx.eval('texture.parent {%s} {%s} item:{%s}' % (baseShad, NewID, TargetGrpMask))

        # # Here we make sure the ColorID_0 is at the BottomMost in the hierarchy
        # if ColorIDSelSetName == "ColorID_0":
        # 	lx.eval('texture.parent {%s} 0 item:{%s}' % (baseShad, TargetGrpMask))  # '0' argument #2 is the relative position
        #
        # # Here we make sure that all other ColorID superior to 0 we be put on top of previously created Grp Mask
        # if ColorIDSelSetName == "ColorID_1":
        # 	lx.eval('texture.parent {%s} 1 item:{%s}' % (baseShad, TargetGrpMask)) # '0' argument #2 is the relative position

        lx.eval('smo.GC.DeselectAll')

        GrpPresence = False
        GrpTarget = []
        GrpColorIdent = []
        for item in scene.items(itype='mask', superType=True):
            # lx.out('Default Base Shader found:',item)
            if item.name == "Grp_ColorID":
                GrpPresence = True
                # print(item)
                GrpTarget.append(item.Ident())
                print(GrpTarget[0])

        # print(GrpPresence)
        if not GrpPresence:
            GrpColorID = scene.addItem('mask', name='Grp_ColorID')
            print(GrpColorID.Ident())
            GrpTarget.append(GrpColorID.Ident())
            GrpColorIdent = GrpColorID.Ident()
            lx.eval('texture.parent {%s} 99 item:{%s}' % (GrpColorIdent, TargetGrpMask))

        if GrpPresence:
            GrpColorIdent = GrpTarget[0]
            # scene.select(GrpTarget[0])
            lx.eval('texture.parent {%s} {%s} item:{%s}' % (GrpColorIdent, NewID, TargetGrpMask))

        renderItem = scene.renderItem
        AllMasks = []
        for mGrp in renderItem.childrenByType("mask", 1):
            AllMasks.append(mGrp.index)
        print(max(AllMasks))
        PosID = 0
        PosID = max(AllMasks)
        print(PosID)
        print(baseShad)
        print(GrpColorIdent)

        lx.eval('texture.parent {%s} {%s} item:{%s}' % (baseShad, PosID, GrpColorIdent))

        lx.eval('smo.GC.DeselectAll')
        scene.select(meshes)
        lx.eval('select.type polygon')
        lx.eval('select.drop polygon')

        # print('ColorID List in scene')
        # print(ListPSelSet())
        # print('latest ColorID created')
        # print(ColorIDSelSetName)
        if ByItemMode == False:
            # print(len(ListPSelSet()))
            if len(ListPSelSet()) > 1:
                for i in ListPSelSet():
                    # print(i)
                    if i != ColorIDSelSetName:
                        # lx.eval('select.pickWorkingSet %s' % i)
                        # Better to use select.useset cmd than select.pickWorkingSet as it's not deendant of a list ID as it's explicitly select by SelSet Name

                        lx.eval('!select.useSet {%s} select' % i)
                        lx.eval('!select.useSet {%s} deselect' % ColorIDSelSetName)
                        # lx.eval('!select.useSet ColorID_0 select')
                        # lx.eval('!select.useSet ColorID_1 deselect')
                        lx.eval('select.editSet {%s} remove' % ColorIDSelSetName)
                        lx.eval('select.drop polygon')
        lx.eval('select.useSet %s replace' % ColorIDSelSetName)

        if ByItemMode == True:
            lx.eval('select.type item')

        # elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
        #     lx.out('script Stopped: your mesh does not match the requirement for that script.')
        #     sys.exit
        
    
lx.bless(SMO_QT_SetSelSetColorIDRandomConstant_Cmd, Cmd_Name)
