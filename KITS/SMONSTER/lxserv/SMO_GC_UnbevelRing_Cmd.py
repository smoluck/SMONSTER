# python
"""
# Name:         SMO_GC_UnbevelRing_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Select current Edge Ring and Unbevel the selection.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      11/11/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.UnbevelRing"


class SMO_GC_UnbevelRing_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - UnBevel Ring'

    def cmd_Desc(self):
        return 'Select current Edge Ring and Unbevel the selection.'

    def cmd_Tooltip(self):
        return 'Select current Edge Ring and Unbevel the selection.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - UnBevel Ring'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.Scene()
        mesh = scene.selectedByType('mesh')[0]
        if self.SelModeEdge:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        #lx.out('Modo Version:',Modo_ver)

        if self.SelModeEdge:
            # -------------------------- #
            ####### SAFETY CHECK 4 #######
            # -------------------------- #
            CsEdges = len(mesh.geometry.edges.selected)
            lx.out('Count Selected Edges', CsEdges)
            SMO_SC_UnbevelPolyLoop_1EdgeSelected = 0
            # --------------------  safety check 4: at Least 3 Edges are selected --- START
            if CsEdges == 0:
                SMO_SC_UnbevelPolyLoop_1EdgeSelected = 0
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {SMO GC UnbevelRing:}')
                lx.eval('dialog.msg {You must select at least 3 Edges and Mouse over an Edge to run that script}')
                lx.eval('+dialog.open')
                #lx.out('script Stopped: Mouse over an Edge to validate the script requirements')
                sys.exit

            elif CsEdges >= 3:
                SMO_SC_UnbevelPolyLoop_1EdgeSelected = 1
                #lx.out('script running: right amount of Edges in selection')
            # --------------------  safety check 4: at Least 3 edges are selected --- END


            if SMO_SC_UnbevelPolyLoop_1EdgeSelected == 1 and Modo_ver >= 1520:
                lx.eval('select.ring')
                lx.eval('tool.set edge.relax on')
                SMO_GC_UnbevelConvergence = lx.eval('tool.attr edge.relax convergence ?')
                # print (SMO_GC_UnbevelConvergence)
                SMO_GC_UnbevelPropagate = lx.eval('tool.attr edge.relax propagate ?')
                # print (SMO_GC_UnbevelPropagate)
                SMO_GC_UnbevelAddMode = lx.eval('tool.attr edge.relax addMode ?')
                # print (SMO_GC_UnbevelAddMode)
                lx.eval('tool.attr edge.relax convergence true')
                lx.eval('tool.attr edge.relax propagate 0')
                lx.eval('tool.attr edge.relax addMode none')
                lx.eval('tool.noChange')
                lx.eval('tool.doApply')

                # set back the original settings of the tool.
                lx.eval('tool.attr edge.relax convergence {%s}' % SMO_GC_UnbevelConvergence)
                lx.eval('tool.attr edge.relax propagate {%s}' % SMO_GC_UnbevelPropagate)
                lx.eval('tool.attr edge.relax addMode {%s}' % SMO_GC_UnbevelAddMode)

                lx.eval('tool.set edge.relax off')
                lx.eval('select.drop edge')

            if SMO_SC_UnbevelPolyLoop_1EdgeSelected == 1 and Modo_ver < 1520:
                lx.eval('select.ring')
                lx.eval('@unbevel.pl')


lx.bless(SMO_GC_UnbevelRing_Cmd, Cmd_Name)
