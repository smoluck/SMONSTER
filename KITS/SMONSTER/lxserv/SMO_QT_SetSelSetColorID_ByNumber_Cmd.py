# python
# ---------------------------------------
# Name:         SMO_QT_SetSelSetColorID_ByNumber_Cmd.py
# Version:      1.00
#
# Purpose:      This script is designed to
#               Set a Diffuse Color override using Selection Set (polygons) on the selected Mesh Layers.
#               Named the new Mat using "ColorID" as Prefix. Color ID Number set by Argument.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      17/01/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import modo, lx, lxu, random

Command_Name = "smo.QT.SetSelSetColorIDByNumber"
# smo.QT.SetSelSetColorIDByNumber 1

# def ListPSelSet():
#     # scene service, reference of the scene and a channel read object
#     scene_svc = lx.service.Scene()
#     scene = lxu.select.SceneSelection().current()
#     chan_read = scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, 0.0)
#
#     # current selected items in scene
#     selection = lxu.select.ItemSelection().current()
#
#     # Get a int ID for the item type.
#     # type_mesh = scene_svc.ItemTypeLookup(lx.symbol.sITYPE_MESH)
#     type_mesh = lx.symbol.i_CIT_MESH
#
#     # Find the first meshItem in the selection
#     for item in selection:
#         if item.TestType(type_mesh):
#             meshItem = item
#             break
#         else:
#             meshItem = None
#
#     # Read the mesh channel from the item to get the mesh object
#     mesh_obj = chan_read.ValueObj(meshItem, meshItem.ChannelLookup(lx.symbol.sICHAN_MESH_MESH))
#     mesh = lx.object.Mesh(mesh_obj)  # mesh object
#
#     # Get the selection sets from the mesh with PICK and save them into a list
#     selSets = []
#     num_polset = mesh.PTagCount(lx.symbol.i_PTAG_PICK)
#     for i in xrange(num_polset):
#         selSets.append(mesh.PTagByIndex(lx.symbol.i_PTAG_PICK, i))
#     lx.out('selSets:', selSets)
#     return selSets


def SetColorIDByNumberCheckSceneMaxColorID():
    # Select the Base Shader to create and place ColorID group on top of current Material Groups
    scene = modo.scene.current()
    # lx.eval('smo.QT.SelectBaseShader')
    SceneShaderItemList = []
    SceneShaderItemName = []
    for item in scene.items(itype='defaultShader', superType=True):
        # lx.out('Default Base Shader found:',item)
        SceneShaderItemList.append(item)
        print(item.id)
        SceneShaderItemName.append(item.id)
    scene.select(SceneShaderItemList[0])
    print(SceneShaderItemName)

    QTChannelExist = bool()
    NewID = int()
    IDNum = int()

    # Test the Base Shader item and check if the needed Channel exist
    try:
        lx.eval(
            '!channel.create SelSetColorIDConstantGlobalCount integer useMin:true default:(-1.0) username:SelSetColorIDConstantGlobalCount')
        SceneConstantID = (-1)
        QTChannelExist = False
    except RuntimeError:  # diffuse amount is zero.
        lx.eval('select.channel {%s:SelSetColorIDConstantGlobalCount@lmb=x} set' % SceneShaderItemName[0])
        QTChannelExist = True
        print('ColorID  Global Count channel already created')
        pass

    # Now that we're sure we have a channel created, we select it
    try:
        lx.eval(
            '!channel.create SelSetColorIDConstantGlobalCount integer useMin:true default:(-1.0) username:SelSetColorIDConstantGlobalCount')
        SceneConstantID = (-1)
        QTChannelExist = False
    except RuntimeError:  # diffuse amount is zero.
        lx.eval('select.channel {%s:SelSetColorIDConstantGlobalCount@lmb=x} set' % SceneShaderItemName[0])
        QTChannelExist = True
        lx.out('ColorID  Global Count channel already created')
        pass
    if QTChannelExist == True:
        print('Quick Tag Channel is defined:', QTChannelExist)
        SceneConstantID = lx.eval('!item.channel SelSetColorIDConstantGlobalCount ?')
        if SceneConstantID < 0:
            SceneConstantID_Int = int(0)
        if SceneConstantID >= 0:
            SceneConstantID_Int = int(SceneConstantID)
        lx.out('Constant ID Max in scene', SceneConstantID_Int)
        print(QTChannelExist)
        print(SceneConstantID_Int)
    if QTChannelExist == False:
        SceneConstantID_Int == 0
        print('Quick Tag Channel is not set')
    return (SceneConstantID_Int)

# print(SetColorIDByNumberCheckSceneMaxColorID())


class SMO_QT_SetSelSetColorID_ByNumber_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("ID Number", lx.symbol.sTYPE_INTEGER)  # this define the color ID to be set on current mesh.
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.

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

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        ColorID_Suffix = "ColorID"

        if self.dyna_Int(0):
            IDNum = self.dyna_Int(0)

        if not self.dyna_Int(0):
            IDNum = 0

        if self.SelModePoly == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        lx.out('MODE PRESET ACTIVATED')
        PresetMaxID = int()

        # mesh = scene.selectedByType('mesh')[0]
        # CsPolys = len(meshes.geometry.polygons.selected)
        meshes = scene.selectedByType('mesh')
        # lx.eval('query layerservice layer.id ? main')  # select main layer
        # ItemUniqueName = lx.eval('query layerservice layer.id ? main')  # store the Unique name of the current mesh layer
        # lx.out('Item Unique Name:', ItemUniqueName)

        lx.eval('smo.QT.SelectBaseShader')
        # PresetMaxID = lx.eval('!item.channel SelSetColorIDConstantGlobalCount ?')

        PresetMaxID = SetColorIDByNumberCheckSceneMaxColorID()
        print(PresetMaxID)
        CheckSceneMaxColor = PresetMaxID + 1
        # PresetMaxID = int(PresetMaxID)
        lx.out('number of ColorID Tags: %s' % PresetMaxID)
        scene.select(meshes)
        lx.eval('select.type polygon')

        ColorIDSelSetName = ("%s_%s" % (ColorID_Suffix, IDNum))
        lx.out('Preset Assignment: Color ID Selection set name:', ColorIDSelSetName)
        lx.eval('select.editSet {%s} add' % ColorIDSelSetName)

        if CheckSceneMaxColor > 1:
            for i in xrange(0, CheckSceneMaxColor):
                # print(i)
                if i != IDNum:
                    # print("Good")
                    CleanupColorIDSelSetName = ("%s_%s" % (ColorID_Suffix, i))
                    lx.eval('!select.pickWorkingSet %s' % CleanupColorIDSelSetName)
                    lx.eval('!select.editSet %s remove' % CleanupColorIDSelSetName)
        lx.eval('select.useSet %s replace' % ColorIDSelSetName)

lx.bless(SMO_QT_SetSelSetColorID_ByNumber_Cmd, Command_Name)