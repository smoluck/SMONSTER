# python
"""
Name:         SMO_BAKE_SetBakePairs_Cmd.py

Purpose:      This script is designed to:
              Set MTyp Tags and Name prefix according to selection
              order and user preferences. low --> high OR  high --> low.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      06/12/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.BAKE.SetBakePairs"


# smo.BAKE.SetBakePairs


class SMO_BAKE_SetBakePairs_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        # Store the currently selected item, or if nothing is selected, an empty list.
        # Wrap this is a try except, the initial launching of Modo will cause this function
        # to perform a shallow execution before the scene state is established.
        # The script will still continue to run, but it outputs a stack trace since it failed.
        # So to prevent console spew on launch when this plugin is loaded, we use the try/except.
        try:
            self.current_Selection = lxu.select.ItemSelection().current()
        except:
            self.current_Selection = []

        # If we do have something selected, put it in self.current_Selection
        if len(self.current_Selection) == 2:
            self.current_Selection = self.current_Selection
        else:
            self.current_Selection = None

        # Test the stored selection list, only if it it not empty, instantiate the variables.

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO BAKE - Set Bake Pairs'

    def cmd_Desc(self):
        return 'Set MTyp Tags and Name prefix according to selection order and user preferences. low --> high OR  high --> low.'

    def cmd_Tooltip(self):
        return 'Set MTyp Tags and Name prefix according to selection order and user preferences. low --> high OR  high --> low.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO BAKE - Set Bake Pairs.'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        if self.current_Selection is not None:
            # -------------- Index Style START Procedure  -------------- #
            # Bugfix for items that cant be detected when "Index Style" is not using underscore as separator.
            IndexStyle = lx.eval("pref.value application.indexStyle ?")
            if IndexStyle is not "uscore":
                lx.eval("pref.value application.indexStyle uscore")
            # -------------------------------------------- #

            scene = modo.scene.current()
            mesh = modo.Mesh()

            lx.out('--SMONSTER--')
            lx.out('smo.BAKE.SetBakePairs command launched')
            Mesh_A = scene.selectedByType('mesh')[0]
            lx.out('First Mesh:', Mesh_A.name)

            Mesh_B = scene.selectedByType('mesh')[1]
            lx.out('Second Mesh:', Mesh_B.name)

            selitems = len(lx.evalN('query sceneservice selection ? mesh'))
            lx.out('Selected items count', selitems)

            sel_items = list(scene.selectedByType("mesh"))

            AutoHide_Set_BakePairs = lx.eval('user.value SMO_UseVal_BAKE_AutoHideWhenSetBakePairs ?')
            lx.out('Autohide Bake Pairs state:', bool(AutoHide_Set_BakePairs))

            FirstMeshHighPoly = lx.eval('user.value SMO_UseVal_BAKE_WhenSetBakePairsSelectHighFirst ?')
            lx.out('Select HighPoly 1st when setting Bake Pairs state:', bool(FirstMeshHighPoly))

            CreatePosRotConstraints = lx.eval('user.value SMO_UseVal_BAKE_CreatePosRotConstraints ?')
            lx.out('Create Position/Rotation Constraints on High for Bake Pairs state:', bool(CreatePosRotConstraints))

            # Get the current selected item count
            selitecnt = lx.eval1('query sceneservice item.N ?')
            for i in range(selitecnt):
                itemtype = lx.eval('query sceneservice item.type ? %s' % i)
                # print(itemtype)
                if itemtype == "group":
                    # Get the item ID
                    SelItemGroups = scene.items(lx.symbol.sITYPE_GROUP)
                    lx.eval('select.item %s remove' % SelItemGroups)

            if selitems == 2:
                lx.eval('select.drop item')
                # print(Mesh_A.name)
                # print(Mesh_B.name)

            ############################################################################################################
            # Groups Support
            PutLowInGrpsSetBakePairs = lx.eval('user.value SMO_UseVal_BAKE_PutLowInGrpsSetBakePairs ?')
            lx.out('Put the LowPoly in a Group (LOW) state:', bool(PutLowInGrpsSetBakePairs))

            GrpLowName = lx.eval('user.value SMO_UseVal_BAKE_SetBakePairsGrpsString_low ?')
            lx.out('Group (LOW) name:', GrpLowName)

            PutHighInGrpsSetBakePairs = lx.eval('user.value SMO_UseVal_BAKE_PutHighInGrpsSetBakePairs ?')
            lx.out('Put the HighPoly in a Group (HIGH) state:', bool(PutHighInGrpsSetBakePairs))

            GrpHighName = lx.eval('user.value SMO_UseVal_BAKE_SetBakePairsGrpsString_high ?')
            lx.out('Group (HIGH) name:', GrpHighName)

            PutInGrpsSetBakePairsTopDownOrder = lx.eval('user.value SMO_UseVal_BAKE_PutInGrpsSetBakePairsTopDownOrder ?')
            lx.out('Add in Reverse order --> from TOP To BOTTOM (Last item added at Bottom)', bool(PutInGrpsSetBakePairsTopDownOrder))

            HP_GrpState = False
            LP_GrpState = False
            HP_Pos = int()
            LP_Pos = int()
            ############################################################################################################
            if PutHighInGrpsSetBakePairs:
                # Check if Groups HIGHPOLY_MESHES is present to create it if needed.
                # clear selection of any item in the scene.
                lx.eval('smo.GC.DeselectAll')

                # Get the item count
                n = lx.eval1('query sceneservice item.N ?')

                HPGrps = []
                HPGrpsIDList = []
                HPGrpsNameList = []

                # Loop through the items in the scene, looking for output items
                for i in range(n):
                    itemtype = lx.eval('query sceneservice item.type ? %s' % i)
                    # print(itemtype)
                    if itemtype == "group":
                        # Get the item ID
                        HPGrps = scene.items(lx.symbol.sITYPE_GROUP)

                for g in HPGrps:
                    # print g.name
                    ID = g.id
                    HPGrpsIDList.append(ID)
                    # print g.id
                    Name = g.name
                    HPGrpsNameList.append(Name)
                # print(HPGrpsIDList)
                # print(HPGrpsNameList)

                #####################################
                # Check HighPoly Grp Presence
                for p in HPGrpsNameList:
                    if p == GrpHighName:
                        print('Nice you have an LowPoly Group in Groups Tab !')
                        HP_GrpState = True

                if not HP_GrpState:
                    lx.eval('group.create %s mode:empty' % GrpHighName)
                    lx.eval('item.editorColor blue')
                    HP_GrpState = True
                lx.eval('smo.GC.DeselectAll')
                ######################################

            lx.eval('smo.GC.DeselectAll')

            ############################################################################################################
            if PutLowInGrpsSetBakePairs:
                # Check if Groups LOWPOLY_MESHES is present to create it if needed.
                # clear selection of any item in the scene.
                lx.eval('smo.GC.DeselectAll')

                # Get the item count
                n = lx.eval1('query sceneservice item.N ?')

                LPGrps = []
                LPGrpsIDList = []
                LPGrpsNameList = []

                # Loop through the items in the scene, looking for output items
                for i in range(n):
                    itemtype = lx.eval('query sceneservice item.type ? %s' % i)
                    # print(itemtype)
                    if itemtype == "group":
                        # Get the item ID
                        LPGrps = scene.items(lx.symbol.sITYPE_GROUP)

                for g in LPGrps:
                    # print g.name
                    ID = g.id
                    HPGrpsIDList.append(ID)
                    # print g.id
                    Name = g.name
                    LPGrpsNameList.append(Name)
                # print(LPGrpsIDList)
                # print(LPGrpsNameList)

                ######################################
                # Check LowPoly Grp Presence
                for p in LPGrpsNameList:
                    if p == GrpLowName:
                        print('Nice you have an LowPoly Group in Groups Tab !')
                        LP_GrpState = True

                if not LP_GrpState:
                    lx.eval('group.create %s mode:empty' % GrpLowName)
                    lx.eval('item.editorColor green')
                    LP_GrpState = True
                lx.eval('smo.GC.DeselectAll')
                ######################################
            ############################################################################################################

            lx.eval('smo.GC.DeselectAll')

            ######################################
            # Check Items count in groups
            if PutInGrpsSetBakePairsTopDownOrder:
                if HP_GrpState:
                    lx.eval('select.item {%s} set' % GrpHighName)
                    HPGrpID = scene.selectedByType(lx.symbol.sITYPE_GROUP)[0]
                    # print(HPGrpID)
                    try:
                        lx.eval('!group.scan sel item')
                        HP_ItemsInGrp = len(lx.evalN('query sceneservice selection ? all'))
                        lx.out('items in group count', HP_ItemsInGrp)
                    except:
                        HP_ItemsInGrp = int(0)
                    if HP_ItemsInGrp >= 1:
                        HP_Pos = (HP_ItemsInGrp + 1)
                    if HP_ItemsInGrp == 0:
                        HP_Pos = 0
                    # print(HP_Pos)
                    lx.eval('smo.GC.DeselectAll')

                if LP_GrpState:
                    lx.eval('select.item {%s} set' % GrpLowName)
                    LPGrpID = scene.selectedByType(lx.symbol.sITYPE_GROUP)[0]
                    # print(LPGrpID)
                    try:
                        lx.eval('!group.scan sel item')
                        LP_ItemsInGrp = len(lx.evalN('query sceneservice selection ? all'))
                        lx.out('items in group count', LP_ItemsInGrp)
                    except:
                        LP_ItemsInGrp = int(0)
                    if LP_ItemsInGrp >= 1:
                        LP_Pos = (LP_ItemsInGrp + 1)
                    if LP_ItemsInGrp == 0:
                        LP_Pos = 0
                    # print(LP_Pos)
                    lx.eval('smo.GC.DeselectAll')

            ######################################

            if selitems == 2:
                if not FirstMeshHighPoly:

                    ########################
                    # Select the First Item.
                    Mesh_A_Name = Mesh_A.name
                    lx.out('(LowPoly) Mesh A name is:', format(Mesh_A_Name))
                    lx.eval('select.subItem {%s} set mesh 0 0' % Mesh_A.Ident())

                    # Set item name to class "_low"
                    NewName_A = Mesh_A_Name + '_' + "low"
                    lx.eval('item.name {%s} xfrmcore' % NewName_A)

                    # Set/create MTyp Tag = "low"
                    lx.eval('smo.QT.TagBakeMeshType 1')

                    lx.eval('select.drop item')

                    ########################
                    # Select the 2nd Item.
                    Mesh_B_Name = Mesh_B.name
                    lx.out('(HighPoly) Mesh B name is: ', format(Mesh_B_Name))
                    lx.eval('select.subItem {%s} set mesh 0 0' % Mesh_B.Ident())

                    # Set item name to class "_low"
                    NewName_B = Mesh_A_Name + '_' + "high"
                    lx.eval('item.name {%s} xfrmcore' % NewName_B)

                    # Set/create MTyp Tag = "low"
                    lx.eval('smo.QT.TagBakeMeshType 3')

                    lx.eval('select.drop item')

                    ########################
                    if CreatePosRotConstraints:
                        lx.eval('select.subItem {%s} set mesh 0 0' % Mesh_A.Ident())
                        lx.eval('select.subItem {%s} add mesh 0 0' % Mesh_B.Ident())
                        lx.eval('smo.BAKE.PairsLinkConstraint')
                        lx.eval('smo.GC.DeselectAll')

                if FirstMeshHighPoly:

                    ########################
                    # Select the First Item.
                    Mesh_B_Name = Mesh_B.name
                    lx.out('(LowPoly) Mesh B name is: ', format(Mesh_B_Name))
                    lx.eval('select.subItem {%s} set mesh 0 0' % Mesh_B.Ident())

                    # Set item name to class "_low"
                    NewName_B = Mesh_B_Name + '_' + "low"
                    lx.eval('item.name {%s} xfrmcore' % NewName_B)

                    # Set/create MTyp Tag = "low"
                    lx.eval('smo.QT.TagBakeMeshType 1')

                    lx.eval('select.drop item')

                    ########################
                    # Select the 2nd Item.
                    Mesh_A_Name = Mesh_A.name
                    lx.out('(HighPoly) Mesh A name is: ', format(Mesh_A_Name))
                    lx.eval('select.subItem {%s} set mesh 0 0' % Mesh_A.Ident())

                    # Set item name to class "_low"
                    NewName_A = Mesh_B_Name + '_' + "high"
                    lx.eval('item.name {%s} xfrmcore' % NewName_A)

                    # Set/create MTyp Tag = "low"
                    lx.eval('smo.QT.TagBakeMeshType 3')

                    lx.eval('select.drop item')

                    ########################
                    if CreatePosRotConstraints:
                        lx.eval('select.subItem {%s} set mesh 0 0' % Mesh_A.Ident())
                        lx.eval('select.subItem {%s} add mesh 0 0' % Mesh_B.Ident())
                        lx.eval('smo.BAKE.PairsLinkConstraint')
                        lx.eval('smo.GC.DeselectAll')

                lx.eval('smo.GC.DeselectAll')

                # Put the HighPoly in a Group (HIGH).
                if PutHighInGrpsSetBakePairs:
                    lx.eval('select.item {%s} set' % format(GrpHighName))
                    GH = scene.selectedByType('group')[0].id
                    lx.eval('smo.GC.DeselectAll')
                    # print(GH)
                    if PutInGrpsSetBakePairsTopDownOrder:
                        if FirstMeshHighPoly:
                            lx.eval('group.itemPos {%s} %s %i' % (Mesh_A.Ident(), GH, HP_Pos))
                        if not FirstMeshHighPoly:
                            lx.eval('group.itemPos {%s} %s %i' % (Mesh_B.Ident(), GH, HP_Pos))
                    if not PutInGrpsSetBakePairsTopDownOrder:
                        if FirstMeshHighPoly:
                            lx.eval('group.itemPos {%s} %s 0' % (Mesh_A.Ident(), GH))
                        if not FirstMeshHighPoly:
                            lx.eval('group.itemPos {%s} %s 0' % (Mesh_B.Ident(), GH))
                lx.eval('smo.GC.DeselectAll')

                # Put the LowPoly in a Group (HIGH).
                if PutLowInGrpsSetBakePairs:
                    lx.eval('smo.GC.DeselectAll')
                    lx.eval('select.item {%s} set' % format(GrpLowName))
                    GL = scene.selectedByType('group')[0].id
                    lx.eval('smo.GC.DeselectAll')
                    # print(GH)
                    if PutInGrpsSetBakePairsTopDownOrder:
                        if FirstMeshHighPoly:
                            lx.eval('group.itemPos {%s} %s %i' % (Mesh_B.Ident(), GL, LP_Pos))
                        if not FirstMeshHighPoly:
                            lx.eval('group.itemPos {%s} %s %i' % (Mesh_A.Ident(), GL, LP_Pos))
                    if not PutInGrpsSetBakePairsTopDownOrder:
                        if FirstMeshHighPoly:
                            lx.eval('group.itemPos {%s} %s 0' % (Mesh_B.Ident(), GL))
                        if not FirstMeshHighPoly:
                            lx.eval('group.itemPos {%s} %s 0' % (Mesh_A.Ident(), GL))
                lx.eval('smo.GC.DeselectAll')

                # Autohide mode to declutter scene during Setup.
                if AutoHide_Set_BakePairs:
                    lx.eval('select.subItem {%s} set mesh 0 0' % Mesh_A.Ident())
                    lx.eval('select.subItem {%s} add mesh 0 0' % Mesh_B.Ident())
                    lx.eval('hide.sel')

            lx.eval('smo.GC.DeselectAll')

        # del HPGrps[:]
        # del HPGrpsIDList[:]
        # del HPGrpsNameList[:]
        # del LPGrps[:]
        # del LPGrpsIDList[:]
        # del LPGrpsNameList[:]

        # -------------- Index Style END Procedure  -------------- #
        if IndexStyle is not "uscore":
            lx.eval("pref.value application.indexStyle %s" % IndexStyle)
        # -------------------------------------------- #

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_BAKE_SetBakePairs_Cmd, Cmd_Name)
