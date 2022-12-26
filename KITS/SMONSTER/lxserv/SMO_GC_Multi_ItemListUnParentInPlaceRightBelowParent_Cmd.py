# python
"""
# Name:         SMO_GC_Multi_ItemListUnparentInPlaceRightBelowRootParent_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               (for Multiple items)
#               By default, when we unparent an item (inPlace), the item move at the end of the ItemList.
#               This command make sure the unparented item can appear right bellow
#               the Root Parent of it, in the ItemList.
#
# Author:       Franck ELISABETH ( Solution by Rouven Miller )
# Website:      https://www.smoluck.com
#
# Created:      24/08/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.Multi.ItemListUnparentInPlaceRightBelowRootParent"
# smo.GC.Multi.ItemListUnparentInPlaceRightBelowRootParent


class SMO_GC_Multi_ItemListUnparentInPlaceRightBelowRootParent_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - (Multi) ItemListUnparentInPlaceRightBelowRootParent'

    def cmd_Desc(self):
        return 'MULTI - By default, when we unparent an item (inPlace), the item move at the end of the ItemList. This command make sure the unparented item can appear right bellow the Root Parent of it, in the ItemList.'

    def cmd_Tooltip(self):
        return 'MULTI - By default, when we unparent an item (inPlace), the item move at the end of the ItemList. This command make sure the unparented item can appear right bellow the Root Parent of it, in the ItemList.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - (Multi) ItemListUnparentInPlaceRightBelowRootParent'
    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        # current Selection
        selitems_ksfs = scene.selected

        # selitems_ksfs = scene.selectedByType(lx.symbol.sITYPE_MESH)          # to select only Meshes              "in selection"
        # selitems_ksfs = scene.selectedByType(lx.symbol.sITYPE_GROUP)         # to select only Groups              ""
        # selitems_ksfs = scene.selectedByType(lx.symbol.sITYPE_GROUPLOCATOR)  # to select only GroupLocator        ""
        # selitems_ksfs = scene.selectedByType(lx.symbol.sITYPE_SCENE)         # to select only Scene Item          ""
        # selitems_ksfs = scene.selectedByType(lx.symbol.sITYPE_TRISURF)       # to select only StaticMeshes        ""
        # selitems_ksfs = scene.selectedByType(lx.symbol.sITYPE_VIDEOSTILL)    # to select only VideoStillImages    ""
        # selitems_ksfs = scene.selectedByType(lx.symbol.sITYPE_LOCATOR)       # to select only Locator             ""
        lx.eval('select.drop item')

        for mesh in selitems_ksfs:
            mesh.select(True)
            lx.eval('smo.GC.ItemListUnparentInPlaceRightBelowRootParent')
            lx.eval('select.drop item')

        scene.select(selitems_ksfs)

        del selitems_ksfs


lx.bless(SMO_GC_Multi_ItemListUnparentInPlaceRightBelowRootParent_Cmd, Cmd_Name)

