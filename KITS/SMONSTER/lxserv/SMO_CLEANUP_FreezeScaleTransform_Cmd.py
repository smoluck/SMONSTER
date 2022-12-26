# python
"""
# Name:         SMO_CLEANUP_FreezeScaleTransform_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Freeze Scale transform of all meshes in scene but if there is instances,
#               it retain Instances scale to 100 percent or -100 percent as well.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      02/06/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CLEANUP.FreezeScaleTransform"


class SMO_CLEANUP_FreezeScaleTransform_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Merge Transform Rotation", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.
        self.dyna_Add("Freeze Rotation", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)  # here the (1) define the argument index.

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CLEANUP - Freeze Scale Transforms'

    def cmd_Desc(self):
        return 'Freeze Scale transform but retain Instances scale to 100 percent or -100 percent if that s the case.'

    def cmd_Tooltip(self):
        return 'Freeze Scale transform but retain Instances scale to 100 percent.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CLEANUP - Freeze Scale Transforms'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        InstState = bool()
        PositiveSclX = bool()
        PositiveSclY = bool()
        PositiveSclZ = bool()
        NegativeDetected = bool()

        InstPositiveSclX = bool()
        InstPositiveSclY = bool()
        InstPositiveSclZ = bool()
        InstNegativeDetected = bool()

        # lx.eval('select.drop item')
        # lx.eval('select.itemType mesh')

        mesh_list = scene.selectedByType(lx.symbol.sTYPE_MESH)
        print(mesh_list)
        print('-------------')
        for mesh in mesh_list:
            mesh.select(True)
            TargetItem = lx.eval1("query sceneservice selection ? locator")
            # print(TargetItem)
            chanSclX = lx.eval('transform.channel scl.X ?')
            chanSclY = lx.eval('transform.channel scl.Y ?')
            chanSclZ = lx.eval('transform.channel scl.Z ?')

            print('------ Mesh ------')
            print(chanSclX)
            print(chanSclY)
            print(chanSclZ)
            if chanSclX > 0:
                PositiveSclX = True
            if chanSclX < 0:
                PositiveSclX = False

            if chanSclY > 0:
                PositiveSclY = True
            if chanSclY < 0:
                PositiveSclY = False

            if chanSclZ > 0:
                PositiveSclZ = True
            if chanSclZ < 0:
                PositiveSclZ = False
            print(PositiveSclX)
            print(PositiveSclY)
            print(PositiveSclZ)

            if PositiveSclX == False or PositiveSclY == False or PositiveSclZ == False:
                NegativeDetected = True
            else:
                NegativeDetected = False
            print('------ Negative Scale Transform State ------')
            print(NegativeDetected)
            print('-------------')

            if chanSclX != 1.0 or chanSclY != 1.0 or chanSclZ != 1.0:
                lx.eval('transform.freeze scale')
                try:
                    lx.eval('!select.itemInstances')
                    InstState = True
                except:
                    InstState = False
                print(InstState)
                if InstState:
                    InstanceList = lxu.select.ItemSelection().current()
                    if InstanceList > 0:
                        for instance in InstanceList:
                            print('------ Instances ------')
                            InstchanSclX = lx.eval('transform.channel scl.X ?')
                            print(InstchanSclX)
                            InstchanSclY = lx.eval('transform.channel scl.Y ?')
                            print(InstchanSclY)
                            InstchanSclZ = lx.eval('transform.channel scl.Z ?')
                            print(InstchanSclZ)

                            if InstchanSclX > 0:
                                InstPositiveSclX = True
                            if InstchanSclX < 0:
                                InstPositiveSclX = False

                            if InstchanSclY > 0:
                                InstPositiveSclY = True
                            if InstchanSclY < 0:
                                InstPositiveSclY = False

                            if InstchanSclZ > 0:
                                InstPositiveSclZ = True
                            if InstchanSclZ < 0:
                                InstPositiveSclZ = False
                            print(InstPositiveSclX)
                            print(InstPositiveSclY)
                            print(InstPositiveSclZ)

                            if InstPositiveSclX == False or InstPositiveSclY == False or InstPositiveSclZ == False:
                                InstNegativeDetected = True
                            else:
                                InstNegativeDetected = False
                            print(InstNegativeDetected)
                            print('-------------')

                            print('------ Instances changed ------')
                            if InstchanSclX != 1.0 or InstchanSclX != -1.0:
                                if InstPositiveSclX:
                                    lx.eval('transform.channel scl.X 1.0')
                                else:
                                    lx.eval('transform.channel scl.X -1.0')

                            if InstchanSclY != 1.0 or InstchanSclY != -1.0:
                                if InstPositiveSclY:
                                    lx.eval('transform.channel scl.Y 1.0')
                                else:
                                    lx.eval('transform.channel scl.Y -1.0')

                            if InstchanSclZ != 1.0 or InstchanSclZ != -1.0:
                                if InstPositiveSclZ:
                                    lx.eval('transform.channel scl.Z 1.0')
                                else:
                                    lx.eval('transform.channel scl.Z -1.0')

                    del InstanceList[:]
                lx.eval('smo.GC.DeselectAll')
                mesh.select(True)


lx.bless(SMO_CLEANUP_FreezeScaleTransform_Cmd, Cmd_Name)
