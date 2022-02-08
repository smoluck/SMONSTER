#python
#---------------------------------------
# Name:         SMO_UnbevelLoops.py
# Version: 1.0
# 
# Purpose:      This script is designed to:
#               Unbevel the Polygon Selection, by using the MouseOver the Edge Ring
# 
# 
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
# 
# Created:      05/02/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Command_Name = "smo.GC.UnbevelLoops"
# smo.GC.UnbevelLoops 0

class SMO_GC_UnbevelLoops_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Corner Method", lx.symbol.sTYPE_INTEGER)

        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        # print(self.SelModeVert)
        # print(self.SelModeEdge)
        # print(self.SelModePoly)
        # print(self.SelModeItem)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact (self):
        pass

    def cmd_UserName (self):
        return 'SMO GC UnbevelPolyLoops'

    def cmd_Desc (self):
        return 'Unbevel the Polygon Selection, by using the MouseOver the Edge Ring.'

    def cmd_Tooltip (self):
        return 'Unbevel the Polygon Selection, by using the MouseOver the Edge Ring.'

    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName (self):
        return 'SMO GC UnbevelPolyLoops'

    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.Scene()
        if self.SelModePoly == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
        mesh = scene.selectedByType('mesh')[0]

        ################################
        # <----[ DEFINE VARIABLES ]---->#
        ################################
        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        lx.eval("user.defNew name:SMO_SC_UnbevelPolyLoop_min1PolygonSelected type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SC_UnbevelPolyLoop_1EdgeSelected type:integer life:momentary")
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####

        ##############################
        ####### SAFETY CHECK 3 #######
        ##############################
        CsPolys = len(mesh.geometry.polygons.selected)
        lx.out('Count Selected Poly', CsPolys)

        if CsPolys == 0:
            SMO_SC_UnbevelPolyLoop_min1PolygonSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO UnbevelPolyLoops:}')
            lx.eval('dialog.msg {You must select at least 1 Polygon and Mouse over an Edge to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: Add more Edges to your selection')
            sys.exit

        elif CsPolys >= 1:
            SMO_SC_UnbevelPolyLoop_min1PolygonSelected = 1
            lx.out('script running: right amount of Edges in selection')
        #####--------------------  safety check 3: at Least 1 Polygon is selected --- END --------------------#####



        items = scene.selected
        print(items)

        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        lx.out('Modo Version:',Modo_ver)


        ############### 5 ARGUMENTS ###############
        args = lx.args()
        lx.out(args)

        # Conformal= 0
        # Angle Based = 1
        CornerMethod = self.dyna_Int (0)
        lx.out('Corner solver method:',CornerMethod)
        ############### ARGUMENTS ###############


        # ############### 1 ARGUMENTS Test ###############
        # CornerMethod = 1
        # ############### ARGUMENTS ######################


        if self.SelModePoly == True:
            # Select the Edge via Mouse Over function
            lx.eval('select.type edge')

            lx.eval('query view3dservice mouse ?')
            view_under_mouse = lx.eval('query view3dservice mouse.view ?')
            lx.eval('query view3dservice view.index ? %s' % view_under_mouse)
            lx.eval('query view3dservice mouse.pos ?')
            # poly_under_mouse = lx.eval('query view3dservice element.over ? POLY ')
            edge_under_mouse = lx.eval('query view3dservice element.over ? EDGE ')
            hitpos = lx.eval('query view3dservice mouse.hitpos ?')

            lx.out(view_under_mouse)
            # lx.out(poly_under_mouse)
            lx.out(edge_under_mouse)
            lx.out(hitpos)
            lx.eval('select.drop edge')
            # lx.eval('materials.underMouse')
            success = True
            try:
                lx.eval('select.3DElementUnderMouse')
            except:
                success = False

        ##############################
        ####### SAFETY CHECK 4 #######
        ##############################
        CsEdges = len(mesh.geometry.edges.selected)
        lx.out('Count Selected Edges', CsEdges)
        #####--------------------  safety check 4: at Least 1 Edge is selected --- START --------------------#####
        if CsEdges == 0 :
            SMO_SC_UnbevelPolyLoop_1EdgeSelected = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO UnbevelPolyLoops:}')
            lx.eval('dialog.msg {You must select at least 1 Polygon and Mouse over an Edge to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: Mouse over an Edge to validate the script requirements')
            sys.exit

        elif CsEdges >= 1 :
            SMO_SC_UnbevelPolyLoop_1EdgeSelected = 1
            lx.out('script running: right amount of Edges in selection')
        #####--------------------  safety check 4: at Least 1 edge is selected --- END --------------------#####


        if SMO_SC_UnbevelPolyLoop_1EdgeSelected == 1:
            lx.eval('select.editSet UnbevelEdgeGuide add {}')
            lx.eval('select.type polygon')
            lx.eval('select.convert edge')
            lx.eval('select.invert')
            lx.eval('select.editSet UnbevelNoEdgeRing add {}')
            lx.eval('select.type polygon')
            lx.eval('hide.unsel')
            lx.eval('select.type edge')
            lx.eval('select.drop edge')
            lx.eval('select.useSet UnbevelEdgeGuide replace')
            lx.eval('select.edgeLoop base false m3d middle')
            lx.eval('select.ring')
            lx.eval('select.editSet UnbevelEdgeRing add {}')
            lx.eval('select.drop edge')
            lx.eval('select.type polygon')
            lx.eval('unhide')
            lx.eval('select.drop polygon')
            lx.eval('select.drop edge')
            lx.eval('select.useSet UnbevelEdgeRing replace')

            lx.eval('edge.unbevel convergence')
            # lx.eval('tool.set edge.relax on')
            # lx.eval('tool.attr edge.relax convergence true')
            # lx.eval('tool.attr edge.relax addMode none')
            # lx.eval('tool.noChange')
            # lx.eval('tool.doApply')
            # lx.eval('tool.set edge.relax off')

            lx.eval('!select.deleteSet UnbevelEdgeRing')
            lx.eval('!select.deleteSet UnbevelEdgeGuide')
            lx.eval('!select.deleteSet UnbevelNoEdgeRing')
            lx.eval('select.type polygon')
            if CornerMethod == 1 :
                lx.eval('script.run "macro.scriptservice:92663570022:macro"')
                CsEdges = len(mesh.geometry.edges.selected)
                if CsEdges >=3 :
                    lx.eval('poly.make auto')
                    lx.eval('select.type polygon')
                    lx.eval('poly.triple')
                    lx.eval('select.drop polygon')
                    lx.eval('select.type edge')
                    lx.eval('select.drop edge')
                    lx.eval('select.type polygon')
                if CsEdges <2 :
                    lx.eval('select.drop polygon')
                    lx.eval('select.type edge')
                    lx.eval('select.drop edge')
                    lx.eval('select.type polygon')
                    
        
    def cmd_Query(self, index, vaQuery):
        lx.notimpl()

lx.bless(SMO_GC_UnbevelLoops_Cmd, Command_Name)