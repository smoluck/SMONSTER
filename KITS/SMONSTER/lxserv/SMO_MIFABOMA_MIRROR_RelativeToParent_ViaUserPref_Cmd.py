# python
"""
Name:         SMO_MIFABOMA_MIRROR_RelativeToParent_ViaUserPref_Cmd.py

Purpose:      This Command is designed to
              Mirror current Polygon Selection (or all Poly
              if no selection) relative To Parent center.

Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
Website:      https://www.linkedin.com/in/smoluck/
Created:      16/09/2019
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.MIFABOMA.MirrorRelativeToParent_ViaUserPref"
#smo.MIFABOMA.MirrorRelativeToParent_ViaUserPref 1 0


class SMO_MIFABOMA_Mirror_RelativeToParent_ViaUserPref_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Mirror Axis", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("MergeMode", lx.symbol.sTYPE_BOOLEAN)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)             # here the (1) define the argument index.

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
        return 'SMO MIFABOMA - Mirror Relative To Parent via User Prefs'

    def cmd_Desc (self):
        return 'Mirror current Polygon Selection (or all Poly if no selection) relative To Parent center. It use the User Preferences to define wich clone type you do and if you clone also the hierarchy.'

    def cmd_Tooltip (self):
        return 'Mirror current Polygon Selection (or all Poly if no selection) relative To Parent center. It use the User Preferences to define wich clone type you do and if you clone also the hierarchy.'

    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName (self):
        return 'SMO MIFABOMA - Mirror Relative To Parent via User Prefs'

    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        # lx.out('Modo Version:',Modo_ver)

        VertMode = bool(self.SelModeVert)
        EdgeMode = bool(self.SelModeEdge)
        PolyMode = bool(self.SelModePoly)
        ItemMode = bool(self.SelModeItem)

        ##### Create a list of selected Targets items (meshes and instances)
        TargetMeshes = []
        SelectedInstances = list(scene.selectedByType("meshInst"))
        # print(SelectedInstances)
        for item in SelectedInstances:
            TargetMeshes.append(item)

        SelectedMeshes = list(scene.selectedByType("mesh"))
        # print(SelectedMeshes)
        for item in SelectedMeshes:
            TargetMeshes.append(item)
        # print(TargetMeshes)


        if self.SelModePoly:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        SelItems = (lx.evalN('query sceneservice selection ? locator'))
        lx.out('Selected items is:',SelItems)
        


        # BugFix to preserve the state of the RefSystem (item at origin in viewport)
        # This query only works when an item is selected.
        RefSystemActive = bool()
        CurrentRefSystemItem = lx.eval('item.refSystem ?')
        # print(CurrentRefSystemItem)
        if len(CurrentRefSystemItem) != 0:
            RefSystemActive = True
        else:
            RefSystemActive = False
        # print(RefSystemActive)



        
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #                    # smo.MIFABOMA.MirrorRelativeToParent_ViaUserPref 1 0
        # ------------------------------ #
        args = lx.args()
        lx.out(args)
        MIRROR_AXES = self.dyna_Int (0)                     # Axes selection:       X = 0 ### Y = 1 ### Z = 2
        MERGE_VERTEX = self.dyna_Bool (1)                   # Off = 0 ### On = 1
        
        # Expose the Result of the Arguments 
        lx.out(MIRROR_AXES,MERGE_VERTEX)
        # ------------------------------ #
        # <----( DEFINE ARGUMENTS )----> #
        # ------------------------------ #
        
        
        CloneType_Clone = lx.eval('user.value SMO_UseVal_MIFABOMA_CloneType_Clone ?')
        lx.out('Auto RePack state:',CloneType_Clone)
        
        CloneType_Instance = lx.eval('user.value SMO_UseVal_MIFABOMA_CloneType_Instance ?')
        lx.out('Auto Fix Flipped UVs state:',CloneType_Instance)
        
        CloneType_Replicas = lx.eval('user.value SMO_UseVal_MIFABOMA_CloneType_Replicas ?')
        lx.out('Auto Fix Flipped UVs state:',CloneType_Replicas)
        
        Clone_Hierarchy = lx.eval('user.value SMO_UseVal_MIFABOMA_CloneChilds ?')
        lx.out('Relocate In Area state:',Clone_Hierarchy)

        ChildPresent = bool()
        ParentPresent = bool()


        lx.eval('smo.GC.DeselectAll')


        # ---------------------------------- #
        # <----( Main Macro - POLYGON )----> #
        # ---------------------------------- #
        if ItemMode == 0 and VertMode == 0 and EdgeMode == 0 and PolyMode == 1:
            for item in SelectedMeshes:
                item.select(True)

                mesh = scene.selectedByType('mesh')[0]
                SelItems = (lx.evalN('query sceneservice selection ? locator'))
                lx.out('Selected items is:', SelItems)

                lx.eval('smo.MASTER.SelectModeDetector')

                MultiVert = lx.eval1('user.value SMO_SelectModeDetector_MultiVertSelected ?')
                MultiEdge = lx.eval1('user.value SMO_SelectModeDetector_MultiEdgeSelected ?')
                MultiPoly = lx.eval1('user.value SMO_SelectModeDetector_MultiPolySelected ?')
                MultiItem = lx.eval1('user.value SMO_SelectModeDetector_MultiItemSelected ?')

                CountVert = lx.eval1('user.value SMO_SelectModeDetector_CountVertSelected ?')
                CountEdge = lx.eval1('user.value SMO_SelectModeDetector_CountEdgeSelected ?')
                CountPoly = lx.eval1('user.value SMO_SelectModeDetector_CountPolySelected ?')
                CountItem = lx.eval1('user.value SMO_SelectModeDetector_CountItemSelected ?')

                lx.out('V---------- Selection Mode ----------V')
                lx.out('Vert Mode', VertMode)
                lx.out('Edge Mode', EdgeMode)
                lx.out('Poly Mode', PolyMode)
                lx.out('Item Mode', ItemMode)
                lx.out('V---------- At least one Element Selected ----------V')
                lx.out('Multi Vert Selected', MultiVert)
                lx.out('Multi Edge Selected', MultiEdge)
                lx.out('Multi Poly Selected', MultiPoly)
                lx.out('Multi Item Selected', MultiItem)
                lx.out('V---------- At least one Element Selected ----------V')
                lx.out('Vert Count Selected', CountVert)
                lx.out('Multi Count Selected', CountEdge)
                lx.out('Multi Count Selected', CountPoly)
                lx.out('Multi Count Selected', CountItem)



                # ------ PARENT  / CHILD Checkup ------ #
                # ------------------------------------- #
                if CountPoly > 0 :
                    lx.eval('hide.unsel')
                lx.eval('select.type item')
                # Tag TARGET
                lx.eval('select.editSet RadArr_ITEM_TARGET add')

                # Select item Hierarchy to test child presence
                lx.eval('select.itemHierarchy')
                ChildItems = len(lx.evalN('query sceneservice selection ? mesh'))
                lx.out('ChildItems',ChildItems)
                if ChildItems >= 2 :
                    ChildPresent = True
                    lx.out('This Target as Child elements')
                    lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
                    lx.eval('select.editSet RadArr_ITEM_CHILD add {}')
                    lx.eval('select.useSet RadArr_ITEM_TARGET select')
                    lx.eval('select.useSet RadArr_ITEM_CHILD deselect')
                elif ChildItems == 1 :
                    ChildPresent = False
                    lx.out('This Target doesn`t have Child elements')
                    lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
                    lx.eval('select.useSet RadArr_ITEM_TARGET replace')

                # Tag PARENT of TARGET
                item.parent.select()
                lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
                ParentItem = len(lx.evalN('query sceneservice selection ? locator'))
                lx.out('ParentItem',ParentItem)
                # Check if Parent exist on this target mesh
                if ParentItem == 1 :
                    ParentPresent = 1
                    lx.out('This Target as Parent')
                    lx.eval('select.editSet RadArr_ITEM_PARENT add')
                    lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                elif ParentItem == 0:
                    ParentPresent = 0
                    lx.out('This Target doesn`t have Parent')
                    lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
                    lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                    lx.eval('select.drop item')

                # Do actions wether Parent exist or Not
                if ParentPresent == 1:
                    lx.eval('select.drop item')
                    lx.eval('select.useSet RadArr_ITEM_PARENT replace')
                    SelItems = (lx.evalN('query sceneservice selection ? locator'))
                    lx.out('Selected items is:',SelItems)
                    lx.eval('item.refSystem %s' % SelItems)
                    lx.eval('select.drop item')
                    lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                # ------------------------------------- #

                lx.eval('select.drop item')
                lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                lx.eval('select.type polygon')
                # ------------------------------- #
                # ------ Mirror Tool Setup ------ #
                # ------------------------------- #
                lx.eval('tool.set *.mirror on')
                MirrorReplaceSourceState = lx.eval('tool.attr effector.clone replace ?')
                MirrorFlipPolyState = lx.eval('tool.attr effector.clone flip ?')
                if MirrorReplaceSourceState:
                    lx.eval('tool.setAttr effector.clone replace false')

                ## Modo Mirror Behavior have changed on Modo 15.2. (it automatically flip the polygons now)
                if Modo_ver < 1520:
                    if not MirrorFlipPolyState:
                        lx.eval('tool.setAttr effector.clone flip true')
                if Modo_ver >= 1520:
                    if MirrorFlipPolyState:
                        lx.eval('tool.setAttr effector.clone flip false')


                if MERGE_VERTEX == 0:
                    lx.eval('tool.setAttr effector.clone merge false')
                if MERGE_VERTEX == 1:
                    lx.eval('tool.setAttr effector.clone merge true')
                    # lx.eval('tool.setAttr effector.clone dist 0.0001')
                    lx.eval('tool.setAttr effector.clone dist [2um]')
                lx.eval('tool.setAttr gen.mirror cenX 0.0')
                lx.eval('tool.setAttr gen.mirror cenY 0.0')
                lx.eval('tool.setAttr gen.mirror cenZ 0.0')
                if MIRROR_AXES == 0:
                    lx.eval('tool.setAttr gen.mirror axis 0')
                    lx.eval('tool.setAttr gen.mirror leftX 0.0')
                    lx.eval('tool.setAttr gen.mirror leftY 1')
                    lx.eval('tool.setAttr gen.mirror leftZ 0.0')
                    lx.eval('tool.setAttr gen.mirror upX 0.0')
                    lx.eval('tool.setAttr gen.mirror upY 0.0')
                    lx.eval('tool.setAttr gen.mirror upZ 1')
                if MIRROR_AXES == 1:
                    lx.eval('tool.setAttr gen.mirror axis 1')
                    lx.eval('tool.setAttr gen.mirror leftX 0.0')
                    lx.eval('tool.setAttr gen.mirror leftY 0.0')
                    lx.eval('tool.setAttr gen.mirror leftZ 1')
                    lx.eval('tool.setAttr gen.mirror upX 1')
                    lx.eval('tool.setAttr gen.mirror upY 0.0')
                    lx.eval('tool.setAttr gen.mirror upZ 0.0')
                if MIRROR_AXES == 2:
                    lx.eval('tool.setAttr gen.mirror axis 2')
                    lx.eval('tool.setAttr gen.mirror leftX 1')
                    lx.eval('tool.setAttr gen.mirror leftY 0.0')
                    lx.eval('tool.setAttr gen.mirror leftZ 0.0')
                    lx.eval('tool.setAttr gen.mirror upX 0.0')
                    lx.eval('tool.setAttr gen.mirror upY 1')
                    lx.eval('tool.setAttr gen.mirror upZ 0.0')
                # -------------------------- #
                lx.eval('tool.doApply')
                lx.eval('select.nextMode')
                lx.eval('tool.set *.mirror off')
                lx.eval('select.drop polygon')

                # if MirrorReplaceSourceState == False or MirrorFlipPolyState == False:
                lx.eval('tool.set *.mirror on')
                lx.eval('tool.noChange')
                # if MirrorReplaceSourceState == False:
                lx.eval('tool.attr effector.clone replace {%s}' % MirrorReplaceSourceState)
                # if MirrorFlipPolyState == False:
                lx.eval('tool.attr effector.clone flip {%s}' % MirrorFlipPolyState)
                lx.eval('select.nextMode')
                lx.eval('tool.set *.mirror off')


                lx.eval('select.type polygon')

                lx.eval('item.refSystem {}')
                lx.eval('tool.set actr.auto on 0')
                if CountPoly > 0 :
                    lx.eval('unhide')

                if not RefSystemActive:
                    lx.eval('item.refSystem {}')
                else:
                    print('Ref System activated')
                    lx.eval('item.refSystem %s' % SelItems[0])


                # ------ PARENT  / CHILD Checkup ------ #
                # ------------------------------------- #
                lx.eval('select.type item')
                lx.eval('!select.deleteSet RadArr_ITEM_TARGET false')
                if ParentPresent == 1 :
                    lx.eval('!select.deleteSet RadArr_ITEM_PARENT false')
                if ChildPresent:
                    lx.eval('!select.deleteSet RadArr_ITEM_CHILD false')
                lx.eval('select.type polygon')

                # ------------------------------------- #
            
            
        # ------------------------------ #
        # <----( Main Macro - ITEM)----> #
        # ------------------------------ #
        if ItemMode == 1 and VertMode == 0 and EdgeMode == 0 and PolyMode == 0:
            for item in TargetMeshes:
                item.select(True)

                SelItems = (lx.evalN('query sceneservice selection ? locator'))
                lx.out('Selected items is:', SelItems)

                # ------ PARENT  / CHILD Checkup ------ #
                # ------------------------------------- #
                lx.eval('select.type item')
                # Tag TARGET
                lx.eval('select.editSet RadArr_ITEM_TARGET add')

                # Select item Hierarchy to test child presence
                lx.eval('select.itemHierarchy')
                ChildItems = len(lx.evalN('query sceneservice selection ? all'))
                lx.out('ChildItems',ChildItems)
                if ChildItems >= 2 :
                    ChildPresent = True
                    lx.out('This Target as Child elements')
                    lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
                    lx.eval('select.editSet RadArr_ITEM_CHILD add {}')
                    lx.eval('select.useSet RadArr_ITEM_TARGET select')
                    lx.eval('select.useSet RadArr_ITEM_CHILD deselect')
                elif ChildItems == 1 :
                    ChildPresent = False
                    lx.out('This Target doesn`t have Child elements')
                    lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
                    lx.eval('select.useSet RadArr_ITEM_TARGET replace')

                # Tag PARENT of TARGET
                item.parent.select()
                lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
                ParentItem = len(lx.evalN('query sceneservice selection ? locator'))
                lx.out('ParentItem',ParentItem)
                # Check if Parent exist on this target mesh
                if ParentItem == 1 :
                    ParentPresent = 1
                    lx.out('This Target as Parent')
                    lx.eval('select.editSet RadArr_ITEM_PARENT add')
                    lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                elif ParentItem == 0:
                    ParentPresent = 0
                    lx.out('This Target doesn`t have Parent')
                    lx.eval('select.useSet RadArr_ITEM_TARGET deselect')
                    lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                    lx.eval('select.drop item')

                # Do actions wether Parent exist or Not
                if ParentPresent == 1:
                    lx.eval('select.drop item')
                    lx.eval('select.useSet RadArr_ITEM_PARENT replace')
                    SelItems = (lx.evalN('query sceneservice selection ? locator'))
                    lx.out('Selected items is:',SelItems)
                    lx.eval('item.refSystem %s' % SelItems)
                    lx.eval('select.drop item')
                    lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                # ------------------------------------- #



                lx.eval('select.drop item')
                lx.eval('select.useSet RadArr_ITEM_TARGET replace')
                # ------------------------------- #
                # ------ Mirror Tool Setup ------ #
                # ------------------------------- #
                lx.eval('tool.set *.mirror on')
                if CloneType_Clone == 1 and CloneType_Instance == 0 and CloneType_Replicas == 0:
                    lx.eval('tool.setAttr effector.item instance false')
                if CloneType_Clone == 0 and CloneType_Instance == 1 and CloneType_Replicas == 0:
                    lx.eval('tool.setAttr effector.item instance true')
                if Clone_Hierarchy == 0 :
                    lx.eval('tool.setAttr effector.item hierarchy false')
                if Clone_Hierarchy == 1 :
                    lx.eval('tool.setAttr effector.item hierarchy true')
                lx.eval('tool.setAttr gen.mirror cenX 0.0')
                lx.eval('tool.setAttr gen.mirror cenY 0.0')
                lx.eval('tool.setAttr gen.mirror cenZ 0.0')
                if MIRROR_AXES == 0:
                    lx.eval('tool.setAttr gen.mirror axis 0')
                    lx.eval('tool.setAttr gen.mirror leftX 0.0')
                    lx.eval('tool.setAttr gen.mirror leftY 1')
                    lx.eval('tool.setAttr gen.mirror leftZ 0.0')
                    lx.eval('tool.setAttr gen.mirror upX 0.0')
                    lx.eval('tool.setAttr gen.mirror upY 0.0')
                    lx.eval('tool.setAttr gen.mirror upZ 1')
                if MIRROR_AXES == 1:
                    lx.eval('tool.setAttr gen.mirror axis 1')
                    lx.eval('tool.setAttr gen.mirror leftX 0.0')
                    lx.eval('tool.setAttr gen.mirror leftY 0.0')
                    lx.eval('tool.setAttr gen.mirror leftZ 1')
                    lx.eval('tool.setAttr gen.mirror upX 1')
                    lx.eval('tool.setAttr gen.mirror upY 0.0')
                    lx.eval('tool.setAttr gen.mirror upZ 0.0')
                if MIRROR_AXES == 2:
                    lx.eval('tool.setAttr gen.mirror axis 2')
                    lx.eval('tool.setAttr gen.mirror leftX 1')
                    lx.eval('tool.setAttr gen.mirror leftY 0.0')
                    lx.eval('tool.setAttr gen.mirror leftZ 0.0')
                    lx.eval('tool.setAttr gen.mirror upX 0.0')
                    lx.eval('tool.setAttr gen.mirror upY 1')
                    lx.eval('tool.setAttr gen.mirror upZ 0.0')
                # -------------------------- #
                lx.eval('tool.doApply')
                lx.eval('select.drop item')
                lx.eval('select.nextMode')
                lx.eval('item.refSystem {}')
                lx.eval('tool.set actr.auto on 0')


                # ------ PARENT  / CHILD Checkup ------ #
                # ------------------------------------- #
                lx.eval('select.type item')
                lx.eval('!select.deleteSet RadArr_ITEM_TARGET false')
                if ParentPresent == 1 :
                    lx.eval('!select.deleteSet RadArr_ITEM_PARENT false')
                if ChildPresent:
                    lx.eval('!select.deleteSet RadArr_ITEM_CHILD false')
                # ------------------------------------- #


                if not RefSystemActive:
                    lx.eval('item.refSystem {}')
                else:
                    print('Ref System activated')
                    lx.eval('item.refSystem %s' % SelItems[0])
        
        lx.out('End of SMO Mirror RelativeToParent Command')


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_MIFABOMA_Mirror_RelativeToParent_ViaUserPref_Cmd, Cmd_Name)
