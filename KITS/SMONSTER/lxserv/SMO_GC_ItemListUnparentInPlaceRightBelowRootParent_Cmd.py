# python
# ---------------------------------------
# Name:         SMO_GC_ItemListUnparentInPlaceRightBelowRootParent_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               By default, when we unparent an item (inPlace), the item move at the end of the ItemList.
#               This command make sure the unparented item can appear right bellow
#               the Root Parent of it, in the ItemList.
#
# Author:       Franck ELISABETH ( Solution by Rouven Miller )
# Website:      http://www.smoluck.com
#
# Created:      18/08/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.GC.ItemListUnparentInPlaceRightBelowRootParent"
# smo.GC.ItemListUnparentInPlaceRightBelowRootParent


class SMO_GC_ItemListUnparentInPlaceRightBelowRootParent_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item;ptag ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item;ptag ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        # print(self.SelModeVert)
        # print(self.SelModeEdge)
        # print(self.SelModePoly)
        # print(self.SelModeItem)
        if self.SelModeEdge or self.SelModePoly or self.SelModeVert:
            lx.eval('select.type item')

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - ItemListUnparentInPlaceRightBelowRootParent'

    def cmd_Desc(self):
        return 'By default, when we unparent an item (inPlace), the item move at the end of the ItemList. This command make sure the unparented item can appear right bellow the Root Parent of it, in the ItemList.'

    def cmd_Tooltip(self):
        return 'By default, when we unparent an item (inPlace), the item move at the end of the ItemList. This command make sure the unparented item can appear right bellow the Root Parent of it, in the ItemList.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - ItemListUnparentInPlaceRightBelowRootParent'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        item = modo.Item()
        # print(item)
        parent = item.parents
        # print(parent)

        if len(parent) > 1:
            lx.eval('smo.GC.ItemListReParentToRootParent')

        parent = item.parents
        # print(parent)

        def rootItems():

            scene = lx.object.Scene(lxu.select.SceneSelection().current())
            parentSceneGraph = scene.GraphLookup(lx.symbol.sGRAPH_PARENT)
            # print(parentSceneGraph)
            # for x in xrange(parentSceneGraph.RootCount()):
            #     print(parentSceneGraph.RootByIndex(x))
            return [parentSceneGraph.RootByIndex(x) for x in xrange(parentSceneGraph.RootCount())]

        for count, value in enumerate(rootItems()):
            if modo.Item(parent[0]).id == modo.Item(value).id:
                print(count, modo.Item(value))
                break

        if len(parent) == 1:
            lx.eval('item.parent %s [] %s inPlace:1 duplicate:0' % (item.id, (count + 1)))


lx.bless(SMO_GC_ItemListUnparentInPlaceRightBelowRootParent_Cmd, Cmd_Name)

