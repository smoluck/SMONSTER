# python
# ---------------------------------------
# Name:         SMO_QT_SetSelSetColorID_ByUser_Cmd.py
# Version:      1.00
#
# Purpose:      This script is designed to
#               Set a Diffuse Color override using Selection Set (polygons) on the selected Mesh Layers.
#               Named the new Mat using "ColorID" as Prefix. Color ID Number set by User value in Popup field.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      17/01/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import modo, lx, lxu, random

Command_Name = "smo.QT.SetSelSetColorIDByUser"
# smo.QT.SetSelSetColorIDByUser

ColorID_Suffix = "ColorID"

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
    lx.eval('smo.QT.SelectBaseShader')
    QTChannelExist = bool()
    NewID = int()
    IDNum = int()
    try:
        lx.eval('!channel.create SelSetColorIDConstantGlobalCount integer useMin:true default:(1) username:SelSetColorIDConstantGlobalCount')
        SceneConstantID = 1
        QTChannelExist = False
    except RuntimeError:  # diffuse amount is zero.
        lx.eval('select.channel {BaseShader:SelSetColorIDConstantGlobalCount@lmb=x} set')
        QTChannelExist = True
        lx.out('ColorID  Global Count channel already created')
        pass
    if QTChannelExist == True:
        SceneConstantID = lx.eval('!item.channel SelSetColorIDConstantGlobalCount ?')
        lx.out('Constant ID Max in scene', SceneConstantID)
        # print(QTChannelExist)
        # print(SceneConstantID)
        return (SceneConstantID)


class SMO_QT_SetSelSetColorID_ByUser_Cmd(lxu.command.BasicCommand):
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

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO QT - Set ColorID ByUser (by SelSet and Constant)'

    def cmd_Desc(self):
        return 'Set a Diffuse Color override using Selection Set (polygons) on the selected Mesh Layers. Named the new Mat using "ColorID" as Prefix. Color ID Number set by User value in Popup field.'

    def cmd_Tooltip(self):
        return 'Set a Diffuse Color override using Selection Set (polygons) on the selected Mesh Layers. Named the new Mat using "ColorID" as Prefix. Color ID Number set by User value in Popup field.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO QT - Set ColorID ByUser (by SelSet and Constant)'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        try:
            #####--- Define User Value for Count --- START ---#####
            #####
            #Create a user value that define the ID Number for the Command.
            lx.eval("user.defNew name:IDNumber type:integer life:momentary")
            #Set the title name for the dialog window
            lx.eval('user.def IDNumber dialogname "SMO QT - Color ID - IDNumber"')
            #Set the input field name for the value that the users will see
            lx.eval("user.def IDNumber username {Set the Color ID Number}")
            #The '?' before the user.value calls a popup to have the user set the value
            lx.eval("?user.value IDNumber")
            #Now that the user set the value, i can query it
            UserInput_IDNumber = lx.eval("user.value IDNumber ?")
            lx.out('User ID Number:',UserInput_IDNumber)
            IDNum = UserInput_IDNumber
        except:
            pass
            
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
        PresetMaxID = lx.eval('!item.channel SelSetColorIDConstantGlobalCount ?')
        
        
        # PresetMaxID = SetColorIDByNumberCheckSceneMaxColorID()
        CheckSceneMaxColor = int(PresetMaxID) + 1
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

lx.bless(SMO_QT_SetSelSetColorID_ByUser_Cmd, Command_Name)