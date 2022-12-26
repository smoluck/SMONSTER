# python
"""
# Name:         SMO_QT_MoveColorIDGrpMaskToTopMostPos_Cmd.py
# Version:      1.00
#
# Purpose:      This script is designed to
#               Select BaseShader Item in current Scene (Assuming there is only one)
#
#
#
# Author:       Franck ELISABETH (with the help of Mateusz Losinski )
# Website:      https://www.smoluck.com
#
# Created:      13/12/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.QT.MoveColorIDGrpMaskToTopMostPos"
# smo.QT.MoveColorIDGrpMaskToTopMostPos


class SMO_QT_MoveColorIDGrpMaskToTopMostPosCmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO QT - MoveColorIDGrpMaskToTopMostPosition'

    def cmd_Desc(self):
        return 'Move the ColorID GrpMask from Quick Tag commands to top-most position in the Shader Tree.'

    def cmd_Tooltip(self):
        return 'Move the ColorID GrpMask from Quick Tag commands to top-most position in the Shader Tree.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO QT - MoveColorIDGrpMaskToTopMostPosition'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.Scene()
        renderItem = scene.renderItem

        GrpPresence = False
        GrpTarget = []
        GrpColorIdent = []
        AllMasks = []
        PosID = 0

        def ItemIdent():
            item = modo.item.Item()
            return item.Ident()

        for mGrp in renderItem.childrenByType("mask", 1):
            AllMasks.append(mGrp.index)
        # print(max(AllMasks))
        PosID = max(AllMasks)

        lx.eval('smo.QT.SelectBaseShader')
        baseShad = lx.eval('query sceneservice defaultShader.parent ? {Base Shader}')
        # print(baseShad)
        lx.eval('smo.GC.DeselectAll')

        for item in scene.items(itype='mask', superType=True):
            # lx.out('Default Base Shader found:',item)
            if item.name == "Grp_ColorID":
                GrpPresence = True
                # print(item)
                GrpTarget.append(item.Ident())
                # print(GrpTarget[0])
        # print(GrpPresence)
        scene.select(GrpTarget[0])
        GrpColorID = scene.selected

        TargetGrpColorID = ItemIdent()

        # if not GrpPresence:
        #     GrpColorID = scene.addItem('mask', name='Grp_ColorID')
        #     print(GrpColorID.Ident())
        #     GrpTarget.append(GrpColorID.Ident())
        #     GrpColorIdent = GrpColorID.Ident()
        #     lx.eval('texture.parent {%s} 99 item:{%s}' % (GrpColorIdent, TargetGrpColorID))

        if GrpPresence:
            lx.eval('texture.parent {%s} {%s} item:{%s}' % (baseShad, PosID, TargetGrpColorID))
        lx.eval('smo.GC.DeselectAll')

        del GrpPresence
        del GrpTarget
        del GrpColorIdent
        del TargetGrpColorID
        del AllMasks
        del PosID


lx.bless(SMO_QT_MoveColorIDGrpMaskToTopMostPosCmd, Cmd_Name)
