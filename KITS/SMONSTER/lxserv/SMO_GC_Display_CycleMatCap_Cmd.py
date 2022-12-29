# python
"""
Name:         SMO_GC_Display_CycleMatCap_Cmd.py

Purpose:      This script is designed to:
              Cycle Through Matcaps that are located in the Smonster GAME CONTENT MatCaps folder.
              SMONSTER\Kits\SMO_GAME_CONTENT\Matcaps

              Select in Item Mode or in Component Mode

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      14/02/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import os

Cmd_Name = "smo.GC.Display.CycleMatCap"

# Forward Mode
# smo.GC.Display.CycleMatCap 0

# Backward Mode
# smo.GC.Display.CycleMatCap 1


class SMO_GC_Display_CycleMatCap_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("ReverseDirection", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)				# here the (0) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact(self):
        pass
    
    def cmd_UserName(self):
        return 'SMO GC - Cycle MatCap'
    
    def cmd_Desc(self):
        return 'Cycle Through Matcaps that are located in the Smonster GAME CONTENT MatCaps folder.'
    
    def cmd_Tooltip(self):
        return 'Cycle Through Matcaps that are located in the Smonster GAME CONTENT MatCaps folder.'
    
    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName(self):
        return 'SMO GC - Cycle MatCap'
    
    def basic_Enable(self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        # ------------- ARGUMENTS ------------- #
        args = lx.args()
        #lx.out(args)
        # ReverseDirection = 0      # Forward Cycle
        # ReverseDirection = 1      # Backward Cycle
        ReverseDirection = self.dyna_Int(0)
        # lx.out('Cycle Direction Mode:',ReverseDirection)
        # ------------- ARGUMENTS ------------- #
        SMO_MatCapId = lx.eval('user.value SMO_MatCapId ?')
        # lx.out('MatCap Current Index:', SMO_MatCapId)

        MatCapKitPath = lx.eval("query platformservice alias ? {kit_SMO_GAME_CONTENT:Matcaps}")
        # lx.out('MatCap Path', MatCapKitPath)

        MatCapFilePath = []
        for MatCap in os.listdir(MatCapKitPath):
            if ".png" in MatCap:
                MatCapFilePath.append(os.path.join(MatCapKitPath + "\\" + MatCap))
            # print(MatCapFilePath)

        MaxId = len(MatCapFilePath)
        # print(MaxId)
        MinId = 0

        modo_ver = int(lx.eval('query platformservice appversion ?'))


        if ReverseDirection == 0:

            if SMO_MatCapId == (MaxId - 1):
                SMO_MatCapId = -1
                # lx.out('MatCap Current Index arrive at End:', SMO_MatCapId)



            if SMO_MatCapId == None:
                SMO_MatCapId = lx.eval('user.value SMO_MatCapId 0')
                # lx.out('MatCap Current Index:', SMO_MatCapId)

            if SMO_MatCapId != None:
                SMO_MatCapId = lx.eval('user.value SMO_MatCapId ?')
                # print(SMO_MatCapId)

                MatCapIndex = (SMO_MatCapId + 1)
                # print(MatCapIndex)

                lx.eval('smo.GC.LoadViewportPreset 1')
                # print(MatCapFilePath[0])
                # print(MatCapFilePath[1])

                MaxId = len(MatCapFilePath)
                # print(MaxId)

                # Get back to lowest Value if we are off the file count in the folder
                if MatCapIndex > (MaxId - 1):
                    MatCapIndex = 0

                # lx.out('MatCap Path List:', MatCapFilePath[MatCapIndex] )
                lx.eval('vpover.enable true')
                lx.eval('vpover.setOverride {%s} matcap' % MatCapFilePath[MatCapIndex])
                lx.eval('user.value SMO_MatCapId %i' % MatCapIndex)

                # Turn off wireframe
                if modo_ver <= 1610:
                    lx.eval('@av_smartWireToggle.pl')
                if modo_ver > 1610:
                    lx.eval('view3d.wireframeOverlay none active')

        if ReverseDirection == 1:
            if SMO_MatCapId == (MaxId - 1):
                SMO_MatCapId = (MaxId - 1)
                # lx.out('MatCap Current Index arrive at End:', SMO_MatCapId)



            if SMO_MatCapId == None:
                SMO_MatCapId = lx.eval('user.value SMO_MatCapId 0')
                # lx.out('MatCap Current Index:', SMO_MatCapId)

            if SMO_MatCapId != None:
                SMO_MatCapId = lx.eval('user.value SMO_MatCapId ?')
                # print(SMO_MatCapId)

                MatCapIndex = (SMO_MatCapId - 1)
                # print(MatCapIndex)

                lx.eval('smo.GC.LoadViewportPreset 1')
                # print(MatCapFilePath[0])
                # print(MatCapFilePath[1])

                MaxId = len(MatCapFilePath)
                # print(MaxId)

                # Get back to lowest Value if we are off the file count in the folder
                if MatCapIndex > (MaxId - 1):
                    MatCapIndex = 0

                # lx.out('MatCap Path List:', MatCapFilePath[MatCapIndex] )
                lx.eval('vpover.enable true')
                lx.eval('vpover.setOverride {%s} matcap' % MatCapFilePath[MatCapIndex])
                lx.eval('user.value SMO_MatCapId %i' % MatCapIndex)

                # Turn off wireframe
                if modo_ver <= 1610:
                    lx.eval('@av_smartWireToggle.pl')
                if modo_ver > 1610:
                    lx.eval('view3d.wireframeOverlay none active')

        # lx.eval('user value SMO_UseVal_VENOM_MatCapState 1')
        del MatCapFilePath[:]


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_Display_CycleMatCap_Cmd, Cmd_Name)
