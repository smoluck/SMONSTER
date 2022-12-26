# python
"""
# Name:         SMO_GC_ItemListReParentToRootParent_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               ReParent selected item to the Root Parent of the current hierarchy.
#
#
# Author:       Franck ELISABETH ( Solution by Rouven Miller )
# Website:      https://www.smoluck.com
#
# Created:      18/08/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

if sys.version_info < (3, 0):
    xrange = range

Cmd_Name = "smo.GC.ItemListReParentToRootParent"
# smo.GC.ItemListReParentToRootParent


class SMO_GC_ItemListReParentToRootParent_Cmd(lxu.command.BasicCommand):
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
        return 'SMO GC - ItemListReParentToRootParent'

    def cmd_Desc(self):
        return 'ReParent selected item to the Root Parent of the current hierarchy.'

    def cmd_Tooltip(self):
        return 'ReParent selected item to the Root Parent of the current hierarchy.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - ItemListReParentToRootParent'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scn = modo.scene.current()

        item = modo.Item()
        # print(item)
        parent = item.parents
        # print(parent)
        if len(parent) > 1:
            scn.select(parent[len(parent) - 1])
            top_most_parent = modo.Item()
            scn.select(item)

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

        if len(parent) > 1:
            scn.select(top_most_parent, "add")
            lx.eval('item.parent inPlace:1')
            scn.select(item)


lx.bless(SMO_GC_ItemListReParentToRootParent_Cmd, Cmd_Name)

