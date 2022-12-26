# python
"""
# Name:         SMO_GC_SplitMeshByUDIM_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Split the current Mesh into multiple one using UDIM IDs.
#               Create New Mesh Layers, using target
#               Mesh Name + PrefixName + UDIM ID from selected Mesh.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      23/02/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.SplitMeshByUDIM"
# smo.GC.SplitMeshByUDIM {Boat} 1001 1014


class SMO_GC_SplitMeshByUDIM_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Prefix Name", lx.symbol.sTYPE_STRING)
        # self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("UDIM Start ID", lx.symbol.sTYPE_INTEGER)
        # self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("UDIM End ID", lx.symbol.sTYPE_INTEGER)
        # self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - SplitMesh by UDIM'

    def cmd_Desc(self):
        return 'Create New Mesh Layers, using target Mesh Name + PrefixName + UDIM ID from selected Mesh.'

    def cmd_Tooltip(self):
        return 'Create New Mesh Layers, using target Mesh Name + PrefixName + UDIM ID from selected Mesh.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Split Mesh by UDIM'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        if self.dyna_String(0):
            PrefixName = self.dyna_String(0)
            print('Material Name is %s' % PrefixName)

        if self.dyna_Int(1):
            UDIMStart = self.dyna_Int(1)
            print('UDIM Start at %s' % UDIMStart)

        if self.dyna_Int(2):
            UDIMEnd = self.dyna_Int(2)
            print('UDIM End at %s' % UDIMEnd)

        scene = modo.scene.current()
        # mesh = scene.selectedByType('mesh')

        Iterate = int()
        Count = (UDIMEnd - UDIMStart) + 1

        MATNameList = []
        UDIMIndexList = []
        NewName = ""
        Mesh_Name = ""

        for i in range(0, Count):
            # print(i)
            UDIMIndex = int(UDIMStart + int(i))
            # print(UDIMIndex)
            MATNameList.append(PrefixName + "_" + str(UDIMIndex))
            UDIMIndexList.append(str(UDIMIndex))

        lx.out('------------------------------------')
        lx.out('---- SMO GC Split UDIM to Mesh Log ---')
        lx.out('UDIM Count is set from %s to %s . For a Total of %s Tile to be processed' % (UDIMStart, UDIMEnd, Count))
        lx.out('Mat Name List:')
        lx.out(MATNameList)
        lx.out('UDIM Index List:')
        lx.out(UDIMIndexList)
        lx.out('-------------')

        meshes = scene.selectedByType('mesh')
        # print(meshes)

        # Query UDIMIndicator tool settings of user current preferences
        lx.eval('tool.set util.udim on')
        CurrentUDIMIndicMode = bool(lx.eval('tool.attr util.udim manual ?'))
        print(CurrentUDIMIndicMode)
        if CurrentUDIMIndicMode:
            UDIMIndicModeChanged = True
            lx.eval('tool.setAttr util.udim manual false')
            lx.eval('tool.doApply')
        else:
            UDIMIndicModeChanged = False
        lx.eval('tool.set util.udim off')

        for i in meshes:
            print('----- %s' % i)
            mesh = modo.Mesh(i)
            mesh.select(True)
            Mesh_Name = lx.eval('item.name ? xfrmcore')
            print('Target mesh layer name is  ', Mesh_Name)

            for item in UDIMIndexList:
                lx.eval('select.type polygon')
                # print('item in for loop: %s' % item)
                lx.eval('tool.set util.udim on')
                lx.eval('tool.setAttr util.udim manual false')
                lx.eval('tool.setAttr util.udim number %s' % item)
                lx.eval('tool.doApply')
                lx.eval('udim.select')
                CurrentMesh = scene.selectedByType('mesh')[0]
                CsPolys = len(CurrentMesh.geometry.polygons.selected)
                print(CsPolys)
                if CsPolys > 0:
                    # lx.eval('select.editSet %s add' % item)
                    lx.eval('smo.CAD.CopyCutAsChildOfCurrentMesh 1 1 0 1')
                    lx.eval('select.type item')
                    NewName = (Mesh_Name + "_" + PrefixName + "_" + item)
                    # print (NewName)
                    lx.eval('item.name {%s} xfrmcore' % NewName)
                    lx.eval('item.parent parent:{} inPlace:1')
                    lx.eval('select.drop item')
                scene.select(CurrentMesh)
                lx.eval('select.type polygon')
                lx.eval('select.drop polygon')
                lx.eval('tool.set util.udim off')
                ### Not necessary as the group mask are deselected along the process
                # selMask = (lx.evalN('query sceneservice selection ? mask'))
                # print (selMask)
                # scene.deselect(selMask)
                lx.eval('select.type item')

        # Reset UDIMIndicator tool settings to user current preferences
        if UDIMIndicModeChanged:
            lx.eval('tool.set util.udim on')
            lx.eval('tool.setAttr util.udim manual %s' % CurrentUDIMIndicMode)
            lx.eval('tool.set util.udim off')

        scene.select(meshes)
        lx.eval('!delete')
        # lx.out('Newly created and assigned: %s Material' % len(MATNameList))
        lx.out('-------------')


lx.bless(SMO_GC_SplitMeshByUDIM_Cmd, Cmd_Name)
