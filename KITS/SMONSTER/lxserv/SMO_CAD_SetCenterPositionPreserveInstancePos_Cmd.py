# python
# ---------------------------------------
# Name:         SMO_CAD_SetCenterPositionPreserveInstancePos_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Set the Center of the current Mesh item to selected Polygons Center, but preserving the Instances Positions.
#
#
# Author:       Franck ELISABETH (with the help of Pavel Efimov)
# Website:      http://www.smoluck.com
#
# Created:      26/03/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.CAD.SetCenterPositionPreserveInstancePos"
# smo.CAD.SetCenterPositionPreserveInstancePos

class SMO_CAD_SetCenterPositionPreserveInstancePos_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CAD - Set Center Position but Preserve Instance Position'

    def cmd_Desc(self):
        return 'Set the Center of the current Mesh item to selected Polygons Center, but preserving the Instances Positions.'

    def cmd_Tooltip(self):
        return 'Set the Center of the current Mesh item to selected Polygons Center, but preserving the Instances Positions.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CAD - Set Center Position but Preserve Instance Position'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        #########################################################################################
        ### Solution try (Not working), by using the Transform Move Tool, to move locally the instances,
        ### by using the Float values of X Y Z Reposition Center.
        #########################################################################################
        # scene = modo.scene.current
        # Modo_Units = lx.eval('pref.value units.default ?')
        # Unit = str()
        # if Modo_Units == "millimeters":
        #     Unit = "mm"
        # if Modo_Units == "meters":
        #     Unit = "m"
        # print(Unit)
        #
        # lx.eval('select.type item')
        # Source = modo.Scene().selected[0]
        # lx.eval('select.itemInstances')
        # NewInstance = modo.Scene().selected[0]
        # InstancesList = []
        # InstancesList = lx.eval('query sceneservice selection ? locator')
        # lx.eval('smo.GC.DeselectAll')
        #
        # Source.select()
        # lx.eval('select.type polygon')
        # # replay name:"Set the Workplane to Polygon Selection"
        # lx.eval('workPlane.fitSelect')
        # lx.eval('workPlane.rotate 0 0.0')
        # lx.eval('workPlane.rotate 1 0.0')
        # lx.eval('workPlane.rotate 2 0.0')
        #
        # # replay name:"Convert selection to Item"
        # lx.eval('select.type item')
        # # replay name:"Convert selection to Center"
        # lx.eval('select.convert type:center')
        # # replay name:"Match Center to Workplane"
        # lx.eval('matchWorkplanePos')
        # # replay name:"Reset the Workplane"
        # lx.eval('workPlane.reset')
        # # replay name:"Item"
        # lx.eval('select.type polygon')
        # lx.eval('select.drop polygon')
        # lx.eval('select.type item')
        #
        # lx.eval('smo.GC.DeselectAll')
        # Source.select()
        # Source_PosX = float(lx.eval('transform.channel pos.X ?'))
        # Source_PosY = float(lx.eval('transform.channel pos.Y ?'))
        # Source_PosZ = float(lx.eval('transform.channel pos.Z ?'))
        # print(Source_PosX)
        # print(Source_PosY)
        # print(Source_PosZ)
        #
        # lx.eval('smo.GC.DeselectAll')
        # Source.select()
        # lx.eval('transform.channel pos.X 0.0')
        # lx.eval('transform.channel pos.Y 0.0')
        # lx.eval('transform.channel pos.Z 0.0')
        # lx.eval('smo.GC.DeselectAll')
        #
        # Source.select()
        # lx.eval('select.itemInstances')
        # # lx.eval('tool.set actr.local on')
        # # lx.eval('tool.set preset:TransformMove mode:on')
        # # lx.eval('tool.reset')
        # # lx.eval('tool.viewType type:xyz')
        # # lx.eval('tool.flag xfrm.transform auto 1')
        # # lx.eval('tool.noChange')
        #
        # # lx.eval('{@kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/TransformMove_Arg.LXM {%f} {%f} {%f}}' % (Source_PosX, Source_PosY, Source_PosZ))
        # # lx.eval('{@kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/TransformMove_Arg.py {%f} {%f} {%f}}' % (Source_PosX, Source_PosY, Source_PosZ))
        # # lx.eval('smo.GC.TransformMove {%f} {%f} {%f}' % (Source_PosX, Source_PosY, Source_PosZ))
        #
        # selitems = (lx.evalN('query sceneservice selection ? locator'))
        # lx.out('selitems', selitems)
        # lx.eval('select.drop item')
        # for m in selitems:
        #     lx.eval('select.item {%s} set' % m)
        #     lx.eval('{@kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/OffsetLocalByArg.py {%f} {%f} {%f}}' % (Source_PosX, Source_PosY, Source_PosZ))
        #
        # lx.eval('smo.GC.DeselectAll')




        #########################################################################################
        ### Solution found by creating a command that Create a temporary Locator at target item,
        ### reorder the Hierarchy in order to offset the item, then delete the locator.
        #########################################################################################
        scene = modo.scene.current
        Modo_Units = lx.eval('pref.value units.default ?')
        Unit = str()
        if Modo_Units == "millimeters":
            Unit = "mm"
        if Modo_Units == "meters":
            Unit = "m"
        print(Unit)

        lx.eval('select.type item')
        Source = modo.Scene().selected[0]
        lx.eval('select.itemInstances')
        NewInstance = modo.Scene().selected[0]
        InstancesList = []
        InstancesList = lx.eval('query sceneservice selection ? locator')
        lx.eval('smo.GC.DeselectAll')

        Source.select()
        lx.eval('select.type polygon')
        # replay name:"Set the Workplane to Polygon Selection"
        lx.eval('workPlane.fitSelect')
        lx.eval('workPlane.rotate 0 0.0')
        lx.eval('workPlane.rotate 1 0.0')
        lx.eval('workPlane.rotate 2 0.0')

        # replay name:"Convert selection to Item"
        lx.eval('select.type item')
        # replay name:"Convert selection to Center"
        lx.eval('select.convert type:center')
        # replay name:"Match Center to Workplane"
        lx.eval('matchWorkplanePos')
        # replay name:"Reset the Workplane"
        lx.eval('workPlane.reset')
        # replay name:"Item"
        lx.eval('select.type polygon')
        lx.eval('select.drop polygon')
        lx.eval('select.type item')

        lx.eval('smo.GC.DeselectAll')
        Source.select()
        Source_PosX = float(lx.eval('transform.channel pos.X ?'))
        Source_PosY = float(lx.eval('transform.channel pos.Y ?'))
        Source_PosZ = float(lx.eval('transform.channel pos.Z ?'))
        print(Source_PosX)
        print(Source_PosY)
        print(Source_PosZ)

        lx.eval('smo.GC.DeselectAll')
        Source.select()
        lx.eval('transform.channel pos.X 0.0')
        lx.eval('transform.channel pos.Y 0.0')
        lx.eval('transform.channel pos.Z 0.0')
        lx.eval('smo.GC.DeselectAll')

        Source.select()
        lx.eval('select.itemInstances')
        # lx.eval('tool.set actr.local on')
        # lx.eval('tool.set preset:TransformMove mode:on')
        # lx.eval('tool.reset')
        # lx.eval('tool.viewType type:xyz')
        # lx.eval('tool.flag xfrm.transform auto 1')
        # lx.eval('tool.noChange')

        # lx.eval('{@kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/TransformMove_Arg.LXM {%f} {%f} {%f}}' % (Source_PosX, Source_PosY, Source_PosZ))
        # lx.eval('{@kit_SMO_GAME_CONTENT:MacroSmoluck/Setup/TransformMove_Arg.py {%f} {%f} {%f}}' % (Source_PosX, Source_PosY, Source_PosZ))
        # lx.eval('smo.GC.TransformMove {%f} {%f} {%f}' % (Source_PosX, Source_PosY, Source_PosZ))

        selitems = (lx.evalN('query sceneservice selection ? locator'))
        lx.out('selitems', selitems)

        lx.eval('select.drop item')
        for m in selitems:
            lx.eval('select.item {%s} set' % m)
            lx.eval('smo.GC.OffsetLocalByArgs {%f} {%f} {%f}' % (Source_PosX, Source_PosY, Source_PosZ))

        lx.eval('smo.GC.DeselectAll')


lx.bless(SMO_CAD_SetCenterPositionPreserveInstancePos_Cmd, Cmd_Name)
