# python
"""
Name:         SMO_QT_SetSelSetColorID_ByNumber_Cmd.py

Purpose:      This script is designed to
              Set a Diffuse Color override using Selection Set (polygons) on the selected Mesh Layers.
              Named the new Mat using "ColorID" as Prefix. Color ID Number set by Argument.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      17/01/2022
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

python_majorver = sys.version_info.major
if python_majorver >= 3:
    xrange = range

Cmd_Name = "smo.QT.SetSelSetColorIDByNumber"
# smo.QT.SetSelSetColorIDByNumber 1


def uNameItem():
    item = modo.item.Item()
    return item.UniqueName()


def ItemIdent():
    item = modo.item.Item()
    return item.Ident()


def getTargetGrpMaskName(IDNum):
    CID_Suffix = "ColorID"
    Separator = lx.eval('pref.value application.indexStyle ?')
    if Separator == "none":
        Sep = ""
        ColorIDMatName = CID_Suffix
    if Separator == "sp":
        Sep = " "
        ColorIDMatName = CID_Suffix + Sep + str(IDNum)
    if Separator == "uscore":
        Sep = "_"
        ColorIDMatName = CID_Suffix + Sep + str(IDNum)
    if Separator == "brak":
        SepA = "("
        SepB = ")"
        ColorIDMatName = CID_Suffix + SepA + str(IDNum) + SepB
    if Separator == "brak-sp":
        SepA = " ("
        SepB = ") "
        ColorIDMatName = CID_Suffix + SepA + str(IDNum) + SepB
    return ColorIDMatName


# print(getTargetGrpMaskName(IDNum))


def SetColorOnNode(IDNum):
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
    if IDNum == PrstColorIDRed:
        return lx.eval('item.editorColor red')
    elif IDNum == PrstColorIDMagenta:
        return lx.eval('item.editorColor magenta')
    elif IDNum == PrstColorIDPink:
        return lx.eval('item.editorColor pink')
    elif IDNum == PrstColorIDBrown:
        return lx.eval('item.editorColor brown')
    elif IDNum == PrstColorIDOrange:
        return lx.eval('item.editorColor orange')
    elif IDNum == PrstColorIDYellow:
        return lx.eval('item.editorColor yellow')
    elif IDNum == PrstColorIDGreen:
        return lx.eval('item.editorColor green')
    elif IDNum == PrstColorIDLightGreen:
        return lx.eval('item.editorColor lightgreen')
    elif IDNum == PrstColorIDCyan:
        return lx.eval('item.editorColor cyan')
    elif IDNum == PrstColorIDBlue:
        return lx.eval('item.editorColor blue')
    elif IDNum == PrstColorIDLightBlue:
        return lx.eval('item.editorColor lightblue')
    elif IDNum == PrstColorIDUltramarine:
        return lx.eval('item.editorColor ultramarine')
    elif IDNum == PrstColorIDPurple:
        return lx.eval('item.editorColor purple')
    elif IDNum == PrstColorIDLightPurple:
        return lx.eval('item.editorColor lightpurple')
    elif IDNum == PrstColorIDDarkGrey:
        return lx.eval('item.editorColor darkgrey')
    elif IDNum == PrstColorIDGrey:
        return lx.eval('item.editorColor grey')
    elif IDNum == PrstColorIDWhite:
        return lx.eval('item.editorColor white')
    else:
        return lx.eval('item.editorColor none')


# SetColorOnNode(IDNum)


def GetBaseShader():
    scn = modo.scene.current()
    # lx.eval('smo.QT.SelectBaseShader')
    RenderItemBaseShader = []
    SceneShaderItemName = []
    for item in scn.items(itype='defaultShader', superType=True):
        if item.name == "Base Shader":
            # lx.out('Default Base Shader found:',item)
            RenderItemBaseShader.append(item)
            # print(item.id)
            SceneShaderItemName.append(item.id)
    return SceneShaderItemName







# test if there is already MaxColorID in the "Base Shader" Render Item
# by checking the presence of the Channel "SelSetColorIDConstantGlobalCount"
def SetColorIDByNumberCheckSceneMaxColorID(IDNum):
    # Select the Base Shader to create and place ColorID group on top of current Material Groups
    scn = modo.scene.current()
    # lx.eval('smo.QT.SelectBaseShader')
    RenderItemBaseShader = []
    SceneShaderItemName = []
    for item in scn.items(itype='defaultShader', superType=True):
        if item.name == "Base Shader":
            # lx.out('Default Base Shader found:',item)
            RenderItemBaseShader.append(item)
            # print(item.id)
            SceneShaderItemName.append(item.id)
    scn.select(RenderItemBaseShader[0])
    # print(SceneShaderItemName)

    QTChannelExist = bool()
    IDNum = int()
    SceneConstantID_Int = 0

    # Test the Base Shader item and check if the needed Channel exist
    try:
        lx.eval(
            '!channel.create SelSetColorIDConstantGlobalCount integer useMin:true default:(-1) username:SelSetColorIDConstantGlobalCount')
        SceneConstantID = (-1)
        QTChannelExist = False
    except RuntimeError:  # diffuse amount is zero.
        lx.eval('select.channel {%s:SelSetColorIDConstantGlobalCount@lmb=x} set' % SceneShaderItemName[0])
        QTChannelExist = True
        # print('ColorID  Global Count channel already created')
        pass

    # Now that we're sure we have a channel created, we select it
    try:
        lx.eval(
            '!channel.create SelSetColorIDConstantGlobalCount integer useMin:true default:(-1) username:SelSetColorIDConstantGlobalCount')
        SceneConstantID = (-1)
        QTChannelExist = False
    except RuntimeError:  # diffuse amount is zero.
        lx.eval('select.channel {%s:SelSetColorIDConstantGlobalCount@lmb=x} set' % SceneShaderItemName[0])
        QTChannelExist = True
        print('ColorID  Global Count channel already created')
        pass
    if QTChannelExist:
        # print('Quick Tag Channel is defined:', QTChannelExist)
        SceneConstantID = int(lx.eval('!item.channel SelSetColorIDConstantGlobalCount ?'))
        if SceneConstantID < 0:
            SceneConstantID_Int = 0
        if SceneConstantID >= 0:
            SceneConstantID_Int = int(SceneConstantID)
        print('Constant ID Max in scene', SceneConstantID_Int)

    if not QTChannelExist:
        lx.eval(
            '!channel.create SelSetColorIDConstantGlobalCount integer useMin:true default:(-1) username:SelSetColorIDConstantGlobalCount')
        lx.eval('!item.channel SelSetColorIDConstantGlobalCount %i' % SceneConstantID_Int)

    # Set the Max ColorID to at least the maximum between IDNum and what was set.
    if QTChannelExist:
        if SceneConstantID_Int < IDNum:
            lx.eval('!item.channel SelSetColorIDConstantGlobalCount %i' % IDNum)
        if SceneConstantID_Int > IDNum:
            lx.eval('!item.channel SelSetColorIDConstantGlobalCount %i' % SceneConstantID_Int)
        # print('Quick Tag Channel is not set')
    # print(QTChannelExist)
    # print(SceneConstantID_Int)
    scn.deselect(RenderItemBaseShader[0])
    return QTChannelExist, SceneConstantID_Int, RenderItemBaseShader[0]


# print(SetColorIDByNumberCheckSceneMaxColorID(IDNum))
# print('ColorIDCount Channel already exist: %s' % SetColorIDByNumberCheckSceneMaxColorID(IDNum)[0])
# print('ColorIDCount Channel Value is: %s' % SetColorIDByNumberCheckSceneMaxColorID(IDNum)[1])
# print('Base Shader RenderItem call is: %s' % SetColorIDByNumberCheckSceneMaxColorID(IDNum)[2])
# scn.select(SetColorIDByNumberCheckSceneMaxColorID(IDNum)[2])


def ListGrpMaskColorIDSelSet(IDNum):
    scn = modo.scene.current()
    GrpMaskPresence = False
    ListGrpMaskColorID = []
    for item in scn.items(itype='mask', superType=True):
        if item.name.startswith('ColorID_'):
            GrpMaskPresence = True
            ListGrpMaskColorID.append(item.Ident())
    return ListGrpMaskColorID


# print(ListGrpMaskColorIDSelSet(IDNum))


# test if there is already a Grp Mask for that specific desired Color ID
def IsThereTargetGrpMaskColorIDSelSet(ListGrpMaskColorID, IDNum):
    scn = modo.scene.current()
    GrpMaskAlreadyThere = False
    ListTargetGrpMaskState = []
    print(getTargetGrpMaskName(IDNum))
    IsThereTargetGrpMaskColorIDSelSet = False
    for item in ListGrpMaskColorID:
        scn.select(item)
        for mask in scn.selectedByType('mask'):
            print(mask.name)
            if mask.name == (getTargetGrpMaskName(IDNum) + " " + "(Set)"):
                IsThereTargetGrpMaskColorIDSelSet = True
                ListTargetGrpMaskState.append(IsThereTargetGrpMaskColorIDSelSet)
        lx.eval('smo.GC.DeselectAll')
    for item in ListTargetGrpMaskState:
        if item:
            GrpMaskAlreadyThere = True
            print('ColorID_%s Group Mask is already is the Shader Tree' % str(IDNum))
    if not GrpMaskAlreadyThere:
        print('No Group Mask called: %s' % ('ColorID_' + str(IDNum)))
        print('We need to create a new one')
    return GrpMaskAlreadyThere, IDNum


# print(IsThereTargetGrpMaskColorIDSelSet(ListGrpMaskColorIDSelSet(IDNum), IDNum))


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
    for i in xrange(num_polset):
        selSets.append(mesh.PTagByIndex(lx.symbol.i_PTAG_PICK, i))
    lx.out('selSets:', selSets)
    return selSets


# print(ListPSelSet())




# test if there is already MaxColorID in the "Base Shader" Render Item by
# checking the presence of the Channel "SelSetColorIDConstantGlobalCount"
def ProcessGrp_ColorID(TargetGrpMask, IDNum, baseShad):
    scn = modo.scene.current()
    GrpPresence = False
    GrpTarget = []
    for item in scn.items(itype='mask', superType=True):
        # lx.out('Default Base Shader found:',item)
        if item.name == "Grp_ColorID":
            GrpPresence = True
            # print(item)
            GrpTarget.append(item.Ident())
            print(GrpTarget[0])
    GrpColorIdent = []
    # print(GrpPresence)
    if not GrpPresence:
        GrpColorID = scn.addItem('mask', name='Grp_ColorID')
        print(GrpColorID.Ident())
        GrpTarget.append(GrpColorID.Ident())
        GrpColorIdent = GrpColorID.Ident()
        lx.eval('texture.parent {%s} 99 item:{%s}' % (GrpColorIdent, TargetGrpMask))
    if GrpPresence:
        GrpColorIdent = GrpTarget[0]
        # scene.select(GrpTarget[0])
        lx.eval('texture.parent {%s} {%s} item:{%s}' % (GrpColorIdent, IDNum, TargetGrpMask))
    renderItem = scn.renderItem
    AllMasks = []
    for mGrp in renderItem.childrenByType("mask", 1):
        AllMasks.append(mGrp.index)
    print(max(AllMasks))
    PosID = 0
    PosID = max(AllMasks)
    print(PosID)
    # if not GrpPresence:
    #     lx.eval('texture.parent {%s} {%s} item:{%s}' % (baseShad, PosID, GrpColorIdent))
    scn.deselect(TargetGrpMask)
    return GrpColorIdent



class SMO_QT_SetSelSetColorID_ByNumber_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("ID Number", lx.symbol.sTYPE_INTEGER)     # this define the color ID to be set on current mesh.
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)      # here the (0) define the argument index.

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

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO QT - Set ColorID ByNumber (by SelSet and Constant)'

    def cmd_Desc(self):
        return 'Set a Diffuse Color override using Selection Set (polygons) on the selected Mesh Layers. Color ID Number set by Argument.'

    def cmd_Tooltip(self):
        return 'Set a Diffuse Color override using Selection Set (polygons) on the selected Mesh Layers. Color ID Number set by Argument.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO QT - Set ColorID ByNumber (by SelSet and Constant)'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scn = modo.scene.current()
        baseShad = GetBaseShader()
        # print(baseShad)

        if self.dyna_Int(0):
            IDNum = self.dyna_Int(0)

        if not self.dyna_Int(0):
            IDNum = 0

        ByItemMode = bool()

        if self.SelModeItem:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
            lx.eval('select.type polygon')
            lx.eval('select.all')
            ByItemMode = True

        if self.SelModePoly:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
            ByItemMode = False
        meshes = scn.selectedByType('mesh')

        lx.out('MODE PRESET ACTIVATED')

        print(getTargetGrpMaskName(IDNum))

        print('---')
        print(ListGrpMaskColorIDSelSet(IDNum))

        print('---')
        print(IsThereTargetGrpMaskColorIDSelSet(ListGrpMaskColorIDSelSet(IDNum), IDNum))

        scn.select(meshes)

        print(SetColorIDByNumberCheckSceneMaxColorID(IDNum))
        print('ColorIDCount Channel already exist: %s' % SetColorIDByNumberCheckSceneMaxColorID(IDNum)[0])
        print('ColorIDCount Channel Value is: %s' % SetColorIDByNumberCheckSceneMaxColorID(IDNum)[1])
        print('Base Shader RenderItem call is: %s' % SetColorIDByNumberCheckSceneMaxColorID(IDNum)[2])
        # scn.select(SetColorIDByNumberCheckSceneMaxColorID(IDNum)[2])

        print('---')
        GrpMaskExist = IsThereTargetGrpMaskColorIDSelSet(ListGrpMaskColorIDSelSet(IDNum), IDNum)[0]
        print(GrpMaskExist)

        # Assign PolySelSet to current polygon selection according to ColorID_VALUE  (IDNum)
        lx.eval('select.editSet {%s} add' % getTargetGrpMaskName(IDNum))

        def SetColorID_Constant_RGB(IDNum, Constant):
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
            if IDNum <= 16:
                try:
                    if IDNum == PrstColorIDRed:
                        lx.eval('!item.channel constant$color {1.0 0.0844 0.0382} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDMagenta:
                        lx.eval('!item.channel constant$color {0,8632 0,0802 0,3968} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDPink:
                        lx.eval('!item.channel constant$color {0.807 0.1946 0.1946} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDBrown:
                        lx.eval('!item.channel constant$color {0.402 0.2232 0.0704} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDOrange:
                        lx.eval('!item.channel constant$color {1.0 0.4793 0.0497} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDYellow:
                        lx.eval('!item.channel constant$color {1.0 0,8149 0,0452} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDGreen:
                        lx.eval('!item.channel constant$color {0,0423 0,7682 0,0423} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDLightGreen:
                        lx.eval('!item.channel constant$color {0.2832 0.9131 0.2832} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDCyan:
                        lx.eval('!item.channel constant$color {0,0382 0,9911 0,7454} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDBlue:
                        lx.eval('!item.channel constant$color {0,0529 0,5029 1.0} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDLightBlue:
                        lx.eval('!item.channel constant$color {0,2232 0,624 1.0} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDUltramarine:
                        lx.eval('!item.channel constant$color {0.1274 0.2502 1.0} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDPurple:
                        lx.eval('!item.channel constant$color {0,3763 0,2423 0,8308} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDLightPurple:
                        lx.eval('!item.channel constant$color {0.624 0.4179 1.0} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDDarkGrey:
                        lx.eval('!item.channel constant$color {0,2423 0,2423 0,2423} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDGrey:
                        lx.eval('!item.channel constant$color {0.4852 0.4852 0.4852} item:{%s}' % Constant)
                    elif IDNum == PrstColorIDWhite:
                        lx.eval('!item.channel constant$color {0.855 0.855 0.855} item:{%s}' % Constant)
                except RuntimeError:  # diffuse amount is zero.
                    pass
            if IDNum > 16:
                from random import randrange
                r, g, b = [randrange(0, 255, 10) / 255.0 for i in range(3)]
                try:
                    lx.eval('!item.channel constant$color {%s %s %s} item:{%s}' % (r, g, b, Constant))
                except RuntimeError:  # diffuse amount is zero.
                    pass

        if not GrpMaskExist:
            Const_Suffix = "Constant"
            lx.eval('shader.create mask')
            GrpMask = scn.selected
            scn.select(GrpMask)
            TargetGrpMask = ItemIdent()
            SetColorOnNode(IDNum)
            print(TargetGrpMask)
            lx.eval('mask.setPTagType "Selection Set"')
            lx.eval('mask.setPTag {%s}' % getTargetGrpMaskName(IDNum))
            lx.eval('shader.create constant')
            SetColorOnNode(IDNum)
            ColorIDConstantName = ("%s_%s" % (Const_Suffix, getTargetGrpMaskName(IDNum)))
            lx.eval('item.name %s constant' % ColorIDConstantName)
            # print(ColorIDSelSetName)
            Constant = lx.eval('query sceneservice selection ? textureLayer')
            # print('Constant item name',Constant)
            SetColorID_Constant_RGB(IDNum, Constant)
            scn.select(GrpMask)
            print('Group Folder Grp_ColorID name:')
            print(TargetGrpMask)
            print('Base Shader name:')
            print(baseShad)
            ProcessGrp_ColorID(TargetGrpMask, IDNum, baseShad)

        # if GrpMaskExist:
        # SetColorOnNode(IDNum)

        if self.SelModePoly:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        print(ListPSelSet())
        AllColorIDSelSets = ListPSelSet()
        for item in AllColorIDSelSets:
            if item != getTargetGrpMaskName(IDNum):
                lx.eval('select.editSet %s remove' % item)

        if ByItemMode:
            lx.eval('select.type item')


lx.bless(SMO_QT_SetSelSetColorID_ByNumber_Cmd, Cmd_Name)
