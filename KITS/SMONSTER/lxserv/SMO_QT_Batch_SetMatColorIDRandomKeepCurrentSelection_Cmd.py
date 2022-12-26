# python
"""
# Name:         SMO_QT_Batch_SetMatColorIDRandomKeepCurrentSelection_Cmd.py
# Version:      1.00
#
# Purpose:      This script is designed to
#               Set a random Diffuse Color using Material Tag (polygons) on the selected Mesh Layers.
#               Named the new Mat using "ColorID" as Prefix but Keep the polygon selection in order
#               to hide current Processed polygons
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      10/05/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.QT.Batch.SetMatColorIDRandomKeepCurrentSelection"
# smo.QT.Batch.SetMatColorIDRandomKeepCurrentSelection


class SMO_QT_Batch_SetMatColorIDRandomKeepCurrentSelection_Cmd(lxu.command.BasicCommand):
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
        return 'SMO QT - Set ColorID Random (by Material)'

    def cmd_Desc(self):
        return 'Set a random Diffuse Color using Material Tag (polygons) on the selected Mesh Layers. Named the new Mat using "ColorID" as Prefix.'

    def cmd_Tooltip(self):
        return 'Set a random Diffuse Color using Material Tag (polygons) on the selected Mesh Layers. Named the new Mat using "ColorID" as Prefix.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO QT - Set ColorID Random (by Material)'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        ColorID_Suffix = "ColorID"
        ByItemMode = bool()

        if self.SelModeItem:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
            lx.eval('select.type polygon')
            lx.eval('select.all')
            ByItemMode = True

        if self.SelModePoly:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
            ByItemMode = False

        # mesh = scene.selectedByType('mesh')[0]
        # CsPolys = len(mesh.geometry.polygons.selected)
        meshes = scene.selectedByType('mesh')
        lx.eval('query layerservice layer.id ? main')  # select main layer
        ItemUniqueName = lx.eval(
            'query layerservice layer.id ? main')  # store the Unique name of the current mesh layer
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

        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #

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
        lx.eval("user.defNew name:ColorIDMatName type:string life:momentary")
        lx.eval("user.defNew name:NewID type:string life:momentary")
        lx.eval("user.defNew name:Const_Suffix type:string life:momentary")
        lx.eval("user.defNew name:ColorIDConstantName type:string life:momentary")
        ###################

        # # -------------------------- #
        # # <---( SAFETY CHECK 1 )---> #
        # # -------------------------- #
        #
        # # --------------------  safety check 1: Polygon Selection Mode enabled --- START
        #
        # selType = ""
        # # Used to query layerservice for the list of polygons, edges or vertices.
        # attrType = ""
        #
        # if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
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
        #     # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        #
        #
        # elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
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
        #     # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        #
        # elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
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
        #     # sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
        # # --------------------  safety check 1: Polygon Selection Mode enabled --- END
        #
        # # -------------------------- #
        # # <---( SAFETY CHECK 2 )---> #
        # # -------------------------- #
        #
        # # at Least 1 Polygons is selected --- START
        # lx.out('Count Selected Poly', CsPolys)
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
        # # at Least 1 Polygons is selected --- END
        #
        # #####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
        # #####
        # TotalSafetyCheckTrueValue = 2
        # lx.out('Desired Value', TotalSafetyCheckTrueValue)
        # TotalSafetyCheck = (SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
        # lx.out('Current Value', TotalSafetyCheck)
        # #####
        # #####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####

        # ------------------------ #
        # <----( Main Macro )----> #
        # ------------------------ #

        # #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START
        # if TotalSafetyCheck == TotalSafetyCheckTrueValue:
        # Select the Base Shader to create and place ColorID group on top of current Material Groups
        # lx.eval('smo.QT.SelectBaseShader')
        SceneShaderItemList = []
        SceneShaderItemName = []
        for item in scene.items(itype='defaultShader', superType=True):
            # lx.out('Default Base Shader found:', item)
            SceneShaderItemList.append(item)
            # print(item.id)
            # print(item.name)
            SceneShaderItemName.append(item.name)
        scene.select(SceneShaderItemList[0])
        # print(SceneShaderItemName)

        QTChannelExist = bool()
        NewID = int()

        try:
            lx.eval(
                '!channel.create MatColorIDGlobalCount integer useMin:true default:(-1.0) username:MatColorIDGlobalCount')
            SceneConstantID = (-1)
            QTChannelExist = False
        except RuntimeError:  # diffuse amount is zero.
            lx.eval('select.channel {%s:MatColorIDGlobalCount@lmb=x} set' % SceneShaderItemName[0])
            QTChannelExist = True
            # lx.out('ColorID  Global Count channel already created')
            pass

        if QTChannelExist:
            SceneConstantID = lx.eval('!item.channel MatColorIDGlobalCount ?')
            # lx.out('Constant ID Max in scene', SceneConstantID)
        # print(QTChannelExist)

        # print(SceneConstantID)

        if SceneConstantID == (-1):
            NewID = 0
        if SceneConstantID >= 0:
            NewID = int(SceneConstantID) + 1
        # print(NewID)
        lx.eval('!item.channel MatColorIDGlobalCount %i' % NewID)
        ColorIDMatName = ("%s_%s" % (ColorID_Suffix, NewID))
        # lx.out('Color ID Selection set name:', ColorIDMatName)

        if NewID <= 16:
            try:
                if NewID == PrstColorIDRed:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {1.0 0.0844 0.0382}' % ColorIDMatName)
                    lx.eval('item.editorColor red')
                elif NewID == PrstColorIDMagenta:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {0,8632 0,0802 0,3968}' % ColorIDMatName)
                    lx.eval('item.editorColor magenta')
                elif NewID == PrstColorIDPink:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {0.807 0.1946 0.1946}' % ColorIDMatName)
                    lx.eval('item.editorColor pink')
                elif NewID == PrstColorIDBrown:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {0.402 0.2232 0.0704}' % ColorIDMatName)
                    lx.eval('item.editorColor brown')
                elif NewID == PrstColorIDOrange:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {1.0 0.4793 0.0497}' % ColorIDMatName)
                    lx.eval('item.editorColor orange')
                elif NewID == PrstColorIDYellow:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {1.0 0,8149 0,0452}' % ColorIDMatName)
                    lx.eval('item.editorColor yellow')
                elif NewID == PrstColorIDGreen:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {0,0423 0,7682 0,0423}' % ColorIDMatName)
                    lx.eval('item.editorColor green')
                elif NewID == PrstColorIDLightGreen:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {0.2832 0.9131 0.2832}' % ColorIDMatName)
                    lx.eval('item.editorColor lightgreen')
                elif NewID == PrstColorIDCyan:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {0,0382 0,9911 0,7454}' % ColorIDMatName)
                    lx.eval('item.editorColor cyan')
                elif NewID == PrstColorIDBlue:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {0,0529 0,5029 1.0}' % ColorIDMatName)
                    lx.eval('item.editorColor blue')
                elif NewID == PrstColorIDLightBlue:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {0,2232 0,624 1.0}' % ColorIDMatName)
                    lx.eval('item.editorColor lightblue')
                elif NewID == PrstColorIDUltramarine:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {0.1274 0.2502 1.0}' % ColorIDMatName)
                    lx.eval('item.editorColor ultramarine')
                elif NewID == PrstColorIDPurple:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {0,3763 0,2423 0,8308}' % ColorIDMatName)
                    lx.eval('item.editorColor purple')
                elif NewID == PrstColorIDLightPurple:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {0.624 0.4179 1.0}' % ColorIDMatName)
                    lx.eval('item.editorColor lightpurple')
                elif NewID == PrstColorIDDarkGrey:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {0,2423 0,2423 0,2423}' % ColorIDMatName)
                    lx.eval('item.editorColor darkgrey')
                elif NewID == PrstColorIDGrey:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {0.4852 0.4852 0.4852}' % ColorIDMatName)
                    lx.eval('item.editorColor grey')
                elif NewID == PrstColorIDWhite:
                    lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {0.855 0.855 0.855}' % ColorIDMatName)
                    lx.eval('item.editorColor white')
            except RuntimeError:  # diffuse amount is zero.
                pass

        if NewID > 16:
            from random import randrange
            r, g, b = [randrange(0, 255, 10) / 255.0 for i in range(3)]
            try:
                lx.eval('smo.GC.SetNewMaterialSmartRename 0 {%s} {%s %s %s}' % (ColorIDMatName, r, g, b))
            except RuntimeError:  # diffuse amount is zero.
                pass

        lx.eval('smo.GC.DeselectAll')
        # lx.eval('select.subItem %s set mesh;replicator;meshInst;camera;light;txtrLocator;backdrop;groupLocator;replicator;surfGen;locator;falloff;deform;locdeform;weightContainer;morphContainer;deformGroup;deformMDD2;ABCStreamingDeformer;morphDeform;itemInfluence;genInfluence;deform.push;deform.wrap;softLag;ABCCurvesDeform.sample;ABCdeform.sample;force.root;baseVolume;chanModify;itemModify;meshoperation;chanEffect;defaultShader;defaultShader 0 0' % ItemUniqueName)
        scene.select(meshes)
        lx.eval('select.type polygon')


lx.bless(SMO_QT_Batch_SetMatColorIDRandomKeepCurrentSelection_Cmd, Cmd_Name)
