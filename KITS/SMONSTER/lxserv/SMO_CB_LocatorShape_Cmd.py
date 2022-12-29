# python
"""
Name:         SMO_CB_LocatorShape_Cmd.py

Purpose:      This script is designed to:
              Define a new item Color and set the Draw Option
              to the corresponding color.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      18/02/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CB.LocatorShape"
# smo.CB.LocatorShape 2 1 1


class SMO_CB_LocatorShape_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Shape", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.
        self.dyna_Add("Solid", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Axis", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

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
        if len(self.current_Selection) >= 1:
            self.current_Selection = self.current_Selection
        else:
            self.current_Selection = None

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CB - Locator Shape'

    def cmd_Desc(self):
        return 'Define the itemList Color and Drawing option for the current selected Item.'

    def cmd_Tooltip(self):
        return 'Define the itemList Color and Drawing option for the current selected Item.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CB - Locator Shape'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        if self.current_Selection is not None:
            scene = modo.scene.current()
            # Be sure to deselect items that are not Locators
            selected_Items = lxu.select.ItemSelection().current()
            # print(selected_Items)
            for item in selected_Items:
                itemType = modo.Item(item).type
                item = lx.object.Item(item)
                item_name = item.UniqueName()
                if itemType != "locator":
                    scene.deselect(item_name)
            selected_locators = scene.selectedByType(lx.symbol.sITYPE_LOCATOR)


            # ------------- ARGUMENTS Test
            # LocShape = 2
            # LocSolid = 1
            # LocAxis = 0
            # ------------- ARGUMENTS ------------- #

            # ------------- ARGUMENTS ------------- #
            args = lx.args()
            lx.out(args)

            # BOX = 1
            # PYRAMID = 2
            # RHOMBUS = 3
            # CYLINDER = 4
            # CONE = 5
            # SPHERE = 6
            # PLANE = 7
            # POINT = 8
            # Circle = 9
            LocShape = self.dyna_Int (0)
            # lx.out('Desired Shape:',LocShape)

            # False = 0
            # True = 1
            LocSolid = self.dyna_Int (1)
            # lx.out('Desired Solid Mode:',LocSolid)

            # X = 0
            # Y = 1
            # Z = 2
            # View = 3
            # None = 4
            LocAxis = self.dyna_Int (2)
            # lx.out('Desired Axis:',LocAxis)
            # ------------- ARGUMENTS ------------- #



            # ------------------------------ #
            # <----( DEFINE VARIABLES )----> #
            # ------------------------------ #

            # ---------------- Define user value for all the different SafetyCheck --- START
            #####

            # Vertex
            lx.eval("user.defNew name:SMO_SafetyCheckLocShape_VertexModeEnabled type:integer life:momentary")

            # Edges
            lx.eval("user.defNew name:SMO_SafetyCheckLocShape_EdgeModeEnabled type:integer life:momentary")

            # Polygon
            lx.eval("user.defNew name:SMO_SafetyCheckLocShape_PolygonModeEnabled type:integer life:momentary")

            # Item
            lx.eval("user.defNew name:SMO_SafetyCheckLocShape_ItemModeEnabled type:integer life:momentary")

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

                SMO_SafetyCheckLocShape_VertexModeEnabled = 1
                SMO_SafetyCheckLocShape_EdgeModeEnabled = 0
                SMO_SafetyCheckLocShape_PolygonModeEnabled = 0
                SMO_SafetyCheckLocShape_ItemModeEnabled = 0

                # lx.out('script Running: Vertex Component Selection Mode')


            elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
                selType = "edge"
                attrType = "edge"

                SMO_SafetyCheckLocShape_VertexModeEnabled = 0
                SMO_SafetyCheckLocShape_EdgeModeEnabled = 1
                SMO_SafetyCheckLocShape_PolygonModeEnabled = 0
                SMO_SafetyCheckLocShape_ItemModeEnabled = 0

                # lx.out('script Running: Edge Component Selection Mode')

            elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
                selType = "polygon"
                attrType = "poly"

                SMO_SafetyCheckLocShape_VertexModeEnabled = 0
                SMO_SafetyCheckLocShape_EdgeModeEnabled = 0
                SMO_SafetyCheckLocShape_PolygonModeEnabled = 1
                SMO_SafetyCheckLocShape_ItemModeEnabled = 0

                # lx.out('script Running: Polygon Component Selection Mode')


            else:
                # This only fails if none of the three supported selection
                # modes have yet been used since the program started, or
                # if "item" or "ptag" (ie: materials) is the current
                # selection mode.

                SMO_SafetyCheckLocShape_VertexModeEnabled = 0
                SMO_SafetyCheckLocShape_EdgeModeEnabled = 0
                SMO_SafetyCheckLocShape_PolygonModeEnabled = 0
                SMO_SafetyCheckLocShape_ItemModeEnabled = 1

                # lx.out('script Running: Item Component Selection Mode')

            # Component Selection Mode type --- END


            # lx.out('Start of SMO_DIS_ItemColor Script')


            # ------------- Compare SafetyCheck value and decide or not to continue the process  --- START
            if SMO_SafetyCheckLocShape_VertexModeEnabled == 1:
                lx.eval('select.type item')

            if SMO_SafetyCheckLocShape_EdgeModeEnabled == 1:
                lx.eval('select.type item')

            if SMO_SafetyCheckLocShape_PolygonModeEnabled == 1:
                lx.eval('select.type item')

            if SMO_SafetyCheckLocShape_ItemModeEnabled == 1:
                lx.eval('select.type item')

            # -------------------------- #
            # <----( Main Macro )----> #
            # -------------------------- #

            ##################### For Locators ######################
            ################## Test Draw Pack #####################
            for item in selected_locators:
                lx.eval('item.channel locator$drawShape custom')
                if LocShape == 1:
                    lx.eval('item.channel locator$isShape box')
                if LocShape == 2:
                    lx.eval('item.channel locator$isShape pyramid')
                if LocShape == 3:
                    lx.eval('item.channel locator$isShape rhombus')
                if LocShape == 4:
                    lx.eval('item.channel locator$isShape cylinder')
                if LocShape == 5:
                    lx.eval('item.channel locator$isShape cone')
                if LocShape == 6:
                    lx.eval('item.channel locator$isShape sphere')
                if LocShape == 7:
                    lx.eval('item.channel locator$isShape plane')
                if LocShape == 8:
                    lx.eval('item.channel locator$isShape point')
                if LocShape == 9:
                    lx.eval('item.channel locator$isShape circle')

                if 0 <= LocAxis < 3 and LocShape > 0:
                    if LocShape == 4 or LocShape == 5:
                        lx.eval('item.channel locator$isRadius 0.1')

                    if LocShape == 6 or LocShape == 9:
                        lx.eval('item.channel locator$isRadius 0.5')

                    if LocAxis == 0:
                        lx.eval('item.channel locator$isAxis x')
                        if LocShape == 1 or LocShape == 2 or LocShape == 3 or LocShape == 4 or LocShape == 5 :
                            lx.eval('item.channel locator$isSize.X 1.0')
                        if LocShape == 1 or LocShape == 2 or LocShape == 3:
                            lx.eval('item.channel locator$isSize.Y 0.1')
                            lx.eval('item.channel locator$isSize.Z 0.1')

                        if LocShape == 7 :
                            lx.eval('item.channel locator$isSize.Y 1')
                            lx.eval('item.channel locator$isSize.Z 1')

                        if LocShape == 1 or LocShape == 2 or LocShape == 4 or LocShape == 5 :
                            lx.eval('item.channel locator$isOffset.X 0.5')
                            lx.eval('item.channel locator$isOffset.Y 0')
                            lx.eval('item.channel locator$isOffset.Z 0')

                        if LocShape == 3 or LocShape == 6 or LocShape == 7 or LocShape == 9 :
                            lx.eval('item.channel locator$isOffset.X 0')
                            lx.eval('item.channel locator$isOffset.Y 0')
                            lx.eval('item.channel locator$isOffset.Z 0')

                        lx.eval('smo.CB.ItemColor 2 2')
                        lx.eval('item.channel locator$isAlign false')

                    if LocAxis == 1 :
                        lx.eval('item.channel locator$isAxis y')

                        if LocShape == 1 or LocShape == 2 or LocShape == 3 or LocShape == 4 or LocShape == 5 :
                            lx.eval('item.channel locator$isSize.Y 1.0')
                        if LocShape == 1 or LocShape == 2 or LocShape == 3:
                            lx.eval('item.channel locator$isSize.X 0.1')
                            lx.eval('item.channel locator$isSize.Z 0.1')

                        if LocShape == 7 :
                            lx.eval('item.channel locator$isSize.X 1')
                            lx.eval('item.channel locator$isSize.Z 1')

                        if LocShape == 1 or LocShape == 2 or LocShape == 4 or LocShape == 5 :
                            lx.eval('item.channel locator$isOffset.X 0')
                            lx.eval('item.channel locator$isOffset.Y 0.5')
                            lx.eval('item.channel locator$isOffset.Z 0')

                        if LocShape == 3 or LocShape == 6 or LocShape == 7 or LocShape == 9 :
                            lx.eval('item.channel locator$isOffset.X 0')
                            lx.eval('item.channel locator$isOffset.Y 0')
                            lx.eval('item.channel locator$isOffset.Z 0')

                        lx.eval('smo.CB.ItemColor 8 2')
                        lx.eval('item.channel locator$isAlign false')

                    if LocAxis == 2 :
                        lx.eval('item.channel locator$isAxis z')

                        if LocShape == 1 or LocShape == 2 or LocShape == 3 or LocShape == 4 or LocShape == 5 :
                            lx.eval('item.channel locator$isSize.Z 1.0')
                        if LocShape == 1 or LocShape == 2 or LocShape == 3 :
                            lx.eval('item.channel locator$isSize.X 0.1')
                            lx.eval('item.channel locator$isSize.Y 0.1')

                        if LocShape == 7 :
                            lx.eval('item.channel locator$isSize.X 1')
                            lx.eval('item.channel locator$isSize.Y 1')

                        if LocShape == 1 or LocShape == 2 or LocShape == 4 or LocShape == 5 :
                            lx.eval('item.channel locator$isOffset.X 0')
                            lx.eval('item.channel locator$isOffset.Y 0')
                            lx.eval('item.channel locator$isOffset.Z 0.5')

                        if LocShape == 3 or LocShape == 6 or LocShape == 7 or LocShape == 9 :
                            lx.eval('item.channel locator$isOffset.X 0')
                            lx.eval('item.channel locator$isOffset.Y 0')
                            lx.eval('item.channel locator$isOffset.Z 0')

                        lx.eval('smo.CB.ItemColor 11 2')
                        lx.eval('item.channel locator$isAlign false')

                if LocAxis == 3 :
                    lx.eval('item.channel locator$isAxis z')
                    lx.eval('smo.CB.ItemColor 5 2')
                    lx.eval('item.channel locator$isAlign true')

                if 0 <= LocAxis <= 3 and LocShape > 0:
                    LocUniName = item.id
                    lx.out('current Locator Unique name is: ', LocUniName)
                    lx.eval('select.channel {%s:isRadius} add' % LocUniName)
                    lx.eval('tool.set channel.haul on')

                if LocSolid == 0 :
                    lx.eval('item.channel locator$isSolid false')
                if LocSolid == 1 :
                    lx.eval('item.channel locator$isSolid true')

                if LocShape == 0 :
                    lx.eval('item.channel locator$drawShape default')
            ###########################################################


            if SMO_SafetyCheckLocShape_VertexModeEnabled == 1:
                lx.eval('select.type vertex')

            if SMO_SafetyCheckLocShape_EdgeModeEnabled == 1:
                lx.eval('select.type edge')

            if SMO_SafetyCheckLocShape_PolygonModeEnabled == 1:
                lx.eval('select.type polygon')

            if SMO_SafetyCheckLocShape_ItemModeEnabled == 1:
                lx.eval('select.type item')
            # lx.out('End of SMO_DIS_ItemColor Script')
            del selected_Items[:]


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()
    
    
lx.bless(SMO_CB_LocatorShape_Cmd, Cmd_Name)
