#python
#---------------------------------------
# Name:         SMO_Unbevel.py
# Version: 1.0
# 
# Purpose:      This script is designed to:
#               Unbevel Edge Selection Selection, by using the MouseOver the Edge Ring
# 
# 
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
# 
# Created:      05/02/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Command_Name = "smo.GC.Unbevel"
# smo.GC.Unbevel

class SMO_GC_Unbevel_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        # self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        # self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        # self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        # print(self.SelModeVert)
        # print(self.SelModeEdge)
        # print(self.SelModePoly)
        # print(self.SelModeItem)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact (self):
        pass

    def cmd_UserName (self):
        return 'SMO GC Unbevel'

    def cmd_Desc (self):
        return 'Unbevel the Edge Selection, you must have 3 continuous Edges Selected at least.'

    def cmd_Tooltip (self):
        return 'Unbevel the Edge Selection, you must have 3 continuous Edges Selected at least.'

    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName (self):
        return 'SMO GC Unbevel'

    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.Scene()
        if self.SelModeEdge == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
        mesh = scene.selectedByType('mesh')[0]


        items = scene.selected
        # print(items)

        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        #lx.out('Modo Version:',Modo_ver)


        if self.SelModeEdge == True:
            ##############################
            ####### SAFETY CHECK 4 #######
            ##############################
            CsEdges = len(mesh.geometry.edges.selected)
            lx.out('Count Selected Edges', CsEdges)
            SMO_SC_UnbevelPolyLoop_1EdgeSelected = 0
            #####--------------------  safety check 4: at Least 1 Edge is selected --- START --------------------#####
            if CsEdges == 0 :
                SMO_SC_UnbevelPolyLoop_1EdgeSelected = 0
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {SMO GC Unbevel:}')
                lx.eval('dialog.msg {You must select at least 1 Edge and Mouse over an Edge to run that script}')
                lx.eval('+dialog.open')
                #lx.out('script Stopped: Mouse over an Edge to validate the script requirements')
                sys.exit

            elif CsEdges >= 1 :
                SMO_SC_UnbevelPolyLoop_1EdgeSelected = 1
                #lx.out('script running: right amount of Edges in selection')
            #####--------------------  safety check 4: at Least 1 edge is selected --- END --------------------#####


            if SMO_SC_UnbevelPolyLoop_1EdgeSelected == 1 and Modo_ver >= 1520 :
                lx.eval('tool.set edge.relax on')
                SMO_GC_UnbevelConvergence = lx.eval('tool.attr edge.relax convergence ?')
                #print (SMO_GC_UnbevelConvergence)
                SMO_GC_UnbevelPropagate = lx.eval('tool.attr edge.relax propagate ?')
                #print (SMO_GC_UnbevelPropagate)
                SMO_GC_UnbevelAddMode = lx.eval('tool.attr edge.relax addMode ?')
                #print (SMO_GC_UnbevelAddMode)
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

            if SMO_SC_UnbevelPolyLoop_1EdgeSelected == 1 and Modo_ver < 1520 :
                lx.eval('@unbevel.pl')
                    
        
    def cmd_Query(self, index, vaQuery):
        lx.notimpl()

lx.bless(SMO_GC_Unbevel_Cmd, Command_Name)