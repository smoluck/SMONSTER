# python
"""
Name:         SMO_GC_Multi_SplitInTwoMeshesByLocalAxisSides_Cmd.py

Purpose:      This script is designed to
              (for Multiple items)
              unmerge selected mesh in 2 Meshes by Local Axis Side (positive or negative).

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      19/08/2022
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

# Cmd_Name = "smo.GC.Multi.SplitInTwoMeshesByLocalAxisSides"
# # smo.GC.Multi.SplitInTwoMeshesByLocalAxisSides z true
#
#
# class SMO_GC_Multi_SplitInTwoMeshesByLocalAxisSides_Cmd(lxu.command.BasicCommand):
#     def __init__(self):
#         lxu.command.BasicCommand.__init__(self)
#         self.dyna_Add("Axis", lx.symbol.sTYPE_AXIS)
#         self.dyna_Add("Direction", lx.symbol.sTYPE_BOOLEAN)
#
#         scenedata = modo.scene.current()
#         CheckGrpSelItems = lxu.select.ItemSelection().current()
#         for item in CheckGrpSelItems:
#             itemType = modo.Item(item).type
#             item = lx.object.Item(item)
#             item_name = item.UniqueName()
#             # print(item_name)
#             if itemType != "mesh":
#                 scenedata.deselect(item_name)
#
#     def cmd_Flags(self):
#         return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
#
#     def cmd_Interact(self):
#         pass
#
#     def cmd_UserName(self):
#         return 'SMO GC - (Multi) SplitInTwoMeshesByLocalAxisSides'
#
#     def cmd_Desc(self):
#         return 'Unmerge selected mesh in 2 Meshes by Local Axis Side (positive or negative).'
#
#     def cmd_Tooltip(self):
#         return 'Unmerge selected mesh in 2 Meshes by Local Axis Side (positive or negative).'
#
#     def cmd_Help(self):
#         return 'https://twitter.com/sm0luck'
#
#     def basic_ButtonName(self):
#         return 'SMO GC - (Multi) SplitInTwoMeshesByLocalAxisSides'
#
#     def basic_Enable(self, msg):
#         return True
#
#     def basic_Execute(self, msg, flags):
#         Axis = self.dyna_String(0)
#         DirSource = self.dyna_Bool(1)
#         scene = modo.scene.current()
#         items = modo.Scene().selected
#
#         selmeshessssa = scene.selectedByType(lx.symbol.sITYPE_MESH)
#         lx.eval('select.drop item')
#         MeshesList = []
#
#         for mesh in selmeshessssa:
#             mesh.select(True)
#             lx.eval('smo.GC.SplitInTwoMeshesByLocalAxisSides %s %s' % (Axis, DirSource))
#             # lx.eval('select.drop item')
#             MeshesList.append(scene.selectedByType(lx.symbol.sITYPE_MESH))
#
#         lx.eval('select.drop item')
#         for item in MeshesList:
#             scene.select(item, True)
#
#
# lx.bless(SMO_GC_Multi_SplitInTwoMeshesByLocalAxisSides_Cmd, Cmd_Name)
