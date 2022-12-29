# python
"""
Name:         SMO_GC_UDIMtoMaterial_Cmd.py

Purpose:      This script is designed to
              Create a New Material Tag, using MatName + UDIM ID on selected Mesh.
              It selects Poly via UDIM index, then create a material for those.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      18/01/2022
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.UDIMtoMaterial"
# smo.GC.UDIMtoMaterial {Boat} 1001 1013


class SMO_GC_UDIMtoMaterial_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        # self.dyna_Add("Fill Color", lx.symbol.sTYPE_COLOR)  # this define the color ID to be set on current mesh.
        self.dyna_Add("Material Name", lx.symbol.sTYPE_STRING)
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
        return 'SMO GC - UDIM to Material'

    def cmd_Desc(self):
        return 'Create a New Material Tag, using MatName + UDIM ID on selected Mesh. It select Poly via UDIM index, then create a material for those.'

    def cmd_Tooltip(self):
        return 'Create a New Material Tag, using MatName + UDIM ID on selected Mesh. It select Poly via UDIM index, then create a material for those.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - UDIM to Material'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        if self.dyna_String(0):
            MatName = self.dyna_String(0)
            print('Material Name is %s' % MatName)

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

        for i in range(0, Count):
            # print(i)
            UDIMIndex = int(UDIMStart + int(i))
            # print(UDIMIndex)
            MATNameList.append(MatName + "_" + str(UDIMIndex))
            UDIMIndexList.append(str(UDIMIndex))

        lx.out('------------------------------------')
        lx.out('---- SMO GC UDIM to Material Log ---')
        lx.out('UDIM Count is set from %s to %s . For a Total of %s Tile to be processed' % (UDIMStart, UDIMEnd, Count))
        lx.out('Mat Name List:')
        lx.out(MATNameList)
        lx.out('UDIM Index List:')
        lx.out(UDIMIndexList)
        lx.out('-------------')

        meshes = scene.selectedByType('mesh')
        # print(meshes)

        # Query UDIMIndicator tool settings of user current preferences
        lx.eval("tool.set util.udim on")
        CurrentUDIMIndicMode = bool(lx.eval('tool.attr util.udim manual ?'))
        print(CurrentUDIMIndicMode)
        if CurrentUDIMIndicMode:
            UDIMIndicModeChanged = True
            lx.eval('tool.setAttr util.udim manual false')
            lx.eval('tool.doApply')
        else:
            UDIMIndicModeChanged = False
        lx.eval("tool.set util.udim off")


        for i in meshes:
            # print('----- %s' % i)
            mesh = modo.Mesh(i)
            mesh.select(True)
            lx.eval("select.type polygon")



            for item in UDIMIndexList:
                # print('item in for loop: %s' % item)
                lx.eval("tool.set util.udim on")
                lx.eval('tool.setAttr util.udim manual false')
                lx.eval("tool.setAttr util.udim number %s" % item)
                lx.eval('tool.doApply')
                lx.eval("udim.select")
                CurrentMesh = scene.selectedByType('mesh')[0]
                CsPolys = len(CurrentMesh.geometry.polygons.selected)
                # print(CsPolys)
                if CsPolys > 0:
                    # lx.eval('select.editSet %s add' % item)
                    # lx.eval('poly.setMaterial %s {0.8 0.8 0.8} 0.8 0.04 true false' % (MatName + "_" + item))
                    lx.eval("smo.GC.SetNewMaterialSmartRename {%s} {1.0 1.0 1.0}" % (MatName + "_" + item))
                lx.eval("select.drop polygon")
                lx.eval("tool.set util.udim off")
                ### Not necessary as the group mask are deselected along the process
                # selMask = (lx.evalN('query sceneservice selection ? mask'))
                # print (selMask)
                # scene.deselect(selMask)
            lx.eval("select.type item")

        # Reset UDIMIndicator tool settings to user current preferences
        if UDIMIndicModeChanged:
            lx.eval("tool.set util.udim on")
            lx.eval('tool.setAttr util.udim manual %s' % CurrentUDIMIndicMode)
        lx.eval("tool.set util.udim off")

        scene.select(meshes)
        lx.out('Newly created and assigned: %s Material' % len(MATNameList))
        lx.out('-------------')


lx.bless(SMO_GC_UDIMtoMaterial_Cmd, Cmd_Name)
