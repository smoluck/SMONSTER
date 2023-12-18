# python
"""
Name:         SMO_GC_ModollamaTriple_Cmd.py

Purpose:      This script is designed to:
              SMO Triple current Polygon selection using Modollama Kit using arguments as Iteration count.


Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      27/05/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu

Cmd_Name = "smo.GC.ModollamaTriple"
# smo.GC.ModollamaTriple 8


class SMO_GC_ModollamaTriple_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Iteration Count", lx.symbol.sTYPE_INTEGER)

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Modollama Triple'

    def cmd_Desc(self):
        return 'Triangulate current Polygon selection using Modollama Kit using arguments as Iteration count.'

    def cmd_Tooltip(self):
        return 'Triangulate current Polygon selection using Modollama Kit using arguments as Iteration count.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Modollama Triple'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Iteration = self.dyna_Int(0)

        if self.SelModePoly:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        KitsList = ['modollama']
        ModoLlama_Status = bool(lx.eval("kit.toggleEnable " + KitsList[0] + " ?"))
        if ModoLlama_Status:
            KeepUVBoundsState = bool(lx.eval('user.value llama_keepuvbounds ?'))
            KeepMatBoundsState = bool(lx.eval('user.value llama_keepmatbounds ?'))
            Origin_Iter = lx.eval('user.value llama_iterations ?')

        func = True
        if ModoLlama_Status:
            lx.eval('user.value llama_keepuvbounds true')
            lx.eval('user.value llama_keepmatbounds true')
            lx.eval('user.value llama_iterations %i' % Iteration)
            lx.eval('user.value llama_anglethreshold 0.005')

        if not ModoLlama_Status:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO GC Modollama Triple:}')
            lx.eval('dialog.msg {You must have ModoLllama kit enabled and loaded if you want to use that function}')
            lx.eval('+dialog.open')
            lx.out('You must have ModoLllama kit enabled and loaded if you want to use that function')
            func = False

        if ModoLlama_Status:
            if func:
                lx.eval('@SmartTriangulation.pl')

        if ModoLlama_Status:
            lx.eval('user.value llama_keepuvbounds %s' % KeepUVBoundsState)
            lx.eval('user.value llama_keepmatbounds %s' % KeepMatBoundsState)
            lx.eval('user.value llama_iterations %s' % Origin_Iter)


lx.bless(SMO_GC_ModollamaTriple_Cmd, Cmd_Name)
