# python
# ---------------------------------------
# Name:         SMO_MESHOP_Add_Cmd.py
# Version:      1.0
#
# Purpose:      Add a Meshop and add it to the Schematic.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      06/08/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo, sys

Cmd_Name = "smo.MESHOP.AddMeshop"
# smo.MESHOP.AddMeshop Stack

class SMO_MESHOP_Add_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Meshop Name", lx.symbol.sTYPE_STRING)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - MeshOp - Add Meshop'

    def cmd_Desc(self):
        return 'Add a Meshop and add it to the Schematic.'

    def cmd_Tooltip(self):
        return 'Add a Meshop and add it to the Schematic.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - MeshOp - Add Meshop'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):

        ################################
        # <----[ DEFINE ARGUMENTS ]---->#
        ################################
        Name = self.dyna_String(0)              # MeshOp Name
        ################################
        # <----[ DEFINE ARGUMENTS ]---->#
        ################################

        ########################################
        ## <----( Set Omnihaul Presets )----> ##
        Preset = "applyDefaultPreset:true"
        MeshOpState = False
        StackOp = False
        Added = False
        Type = "None"
        # MODO version checks. To Apply Default Presets in 15.1 +.
        modo_ver = int(lx.eval('query platformservice appversion ?'))

        Item_A = modo.Scene().selected
        # for item in ItemA:
        #    itemType = modo.Item(item).type
        #    item = lx.object.Item(item)
        #    ID_A = item.Ident()
        #    item_name_A = item.UniqueName()
        # print(item_name_A)
        # print(ID_A)

        for item in Item_A:
            SchemNode_A = lx.eval('schematic.node ?')
            # lx.out('Current Schematic is', SchemNode_A)
            # print(SchemNode_A)
            itemType_A = modo.Item(item).type
            print (itemType_A)
            if len(itemType_A) == 4 and itemType_A == "mesh":
                print ('Bad')
                print('Not Meshop')
                MeshOpState = False
                # print(Type)
            if len(itemType_A) > 4:
                if itemType_A == "prim.cone.item" or itemType_A == "prim.capsule.item" or itemType_A == "prim.sphere.item" or itemType_A == "prim.cube.item" or itemType_A == "prim.cylinder.item" or itemType_A == "prim.ellipsoid.item" or itemType_A == "prim.toroid.item" or itemType_A == "prim.text.item" or itemType_A == "pmodel.meshmerge" or itemType_A == "edge.bevel.item" or itemType_A == "vert.bevel.item" or itemType_A == "poly.bevel.item" or itemType_A == "edge.chamfer.item" or itemType_A == "chamfer.edit.item" or itemType_A == "poly.extrude.item" or itemType_A == "edge.extrude.item" or itemType_A == "vert.extrude.item" or itemType_A == "poly.thicken.item" or itemType_A == "edge.relax.item" or itemType_A == "mb.edgeFlow.item" or itemType_A == "edge.slide.item" or itemType_A == "pmodel.splitEdges.item" or itemType_A == "pmodel.edgeToCurve.item" or itemType_A == "pmodel.mergePolygons.item" or itemType_A == "vert.merge.item" or itemType_A == "pmodel.createVertex" or itemType_A == "vert.setpos.meshop.item" or itemType_A == "poly.smshift.item" or itemType_A == "smooth.meshop.item" or itemType_A == "subdivide.tool.item" or itemType_A == "poly.unsubdiv.item" or itemType_A == "poly.extrude.item" or itemType_A == "curve.extrude.item" or itemType_A == "pen.extrude.item":
                    print ('Good')
                    print('Meshop')
                    MeshOpState = True
                    if MeshOpState == True and itemType_A == "pmodel.meshmerge":
                        print('MergeMeshop')
            if modo_ver >= 1500:
                if itemType_A == "stackOperator":
                    StackOp = True
                if itemType_A != "stackOperator":
                    StackOp = False
            if modo_ver < 1500:
                StackOp = False
        print ('**************************')
        print ('Meshop State:', MeshOpState)
        print ('StackOp State:', StackOp)

        # sel_svc_A = lx.service.Selection()
        # chan_transpacket_A = lx.object.ChannelPacketTranslation(sel_svc_A.Allocate(lx.symbol.sSELTYP_CHANNEL))
        #
        # bDoChannels = True
        # if bDoChannels:
        #    chanType_A = lx.symbol.sSELTYP_CHANNEL
        #    pktID_A = sel_svc.LookupType(chanType_A)
        #    numChanns_A = sel_svc.Count(pktID_A)
        #    for chanId_A in range(0, numChanns_A):
        #        c_A = sel_svc_A.ByIndex(pktID_A, chanId_A)
        #        i_A = lx.object.Item(chan_transpacket_A.Item(c_A))
        #        chan_idx_A = chan_transpacket_A.Index(c_A)
        #        cName_A = item.ChannelName(chan_idx_A)
        #        lx.eval("schematic.addChannel chanIdx:{%s}" % cName_A)

        ##################################
        ## <----( Stack Operator )----> ##
        if modo_ver >= 1500:
            if Name == "Stack" and Added == False:
                try:
                    lx.eval('item.addDeformer stackOperator true')
                    Added = True
                except:
                    sys.exit

        ##################################
        ## <----( Merge Mesh Operator )----> ##
        if Name == "MergeMesh" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create pmodel.meshmerge {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create pmodel.meshmerge')
                    Added = True
            except:
                sys.exit

        ##################################
        ## <----( Primitive Type )----> ##
        if Name == "VertexCreate" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create pmodel.createVertex {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create pmodel.createVertex')
                    Added = True
            except:
                sys.exit

        if Name == "Cone" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create prim.cone.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create prim.cone.item')
                    Added = True
            except:
                sys.exit

        if Name == "Capsule" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create prim.capsule.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create prim.capsule.item')
                    Added = True
            except:
                sys.exit

        if Name == "Sphere" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create prim.sphere.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create prim.sphere.item')
                    Added = True
            except:
                sys.exit

        if Name == "Cube" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create prim.cube.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create prim.cube.item')
                    Added = True
            except:
                sys.exit

        if Name == "Cylinder" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create prim.cylinder.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create prim.cylinder.item')
                    Added = True
            except:
                sys.exit

        if Name == "Ellipsoid" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create prim.ellipsoid.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create prim.ellipsoid.item')
                    Added = True
            except:
                sys.exit

        if Name == "Torus" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create prim.toroid.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create prim.toroid.item')
                    Added = True
            except:
                sys.exit

        if Name == "Text" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create prim.text.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create prim.text.item')
                    Added = True
            except:
                sys.exit

        ##############################
        ## <----( Bevel Type )----> ##
        if Name == "BevelEdge" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create edge.bevel.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create edge.bevel.item')
                    Added = True
            except:
                sys.exit

        if Name == "BevelVertex" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create vert.bevel.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create vert.bevel.item')
                    Added = True
            except:
                sys.exit

        if Name == "BevelPoly" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create poly.bevel.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create poly.bevel.item')
                    Added = True
            except:
                sys.exit

        if Name == "Chamfer" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create edge.chamfer.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create edge.chamfer.item')
                    Added = True
            except:
                sys.exit

        if Name == "ChamferEdit" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create chamfer.edit.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create chamfer.edit.item')
                    Added = True
            except:
                sys.exit

        ################################
        ## <----( Extrude Type )----> ##
        if Name == "ExtrudePoly" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create poly.extrude.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create poly.extrude.item')
                    Added = True
            except:
                sys.exit

        if Name == "ExtrudeEdge" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create edge.extrude.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create edge.extrude.item')
                    Added = True
            except:
                sys.exit

        if Name == "VertexExtrude" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create vert.extrude.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create vert.extrude.item')
                    Added = True
            except:
                sys.exit

        if Name == "Thicken" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create poly.thicken.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create poly.thicken.item')
                    Added = True
            except:
                sys.exit

        if Name == "CurveExtrude" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create curve.extrude.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create curve.extrude.item')
                    Added = True
            except:
                sys.exit

        if Name == "PenExtrude" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create pen.extrude.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create pen.extrude.item')
                    Added = True
            except:
                sys.exit

        ################################
        ## <----( Polygon Type )----> ##
        if Name == "PolyExtrude" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create poly.extrude.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create poly.extrude.item')
                    Added = True
            except:
                sys.exit

        if Name == "PolyBevel" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create poly.bevel.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create poly.bevel.item')
                    Added = True
            except:
                sys.exit

        if Name == "PolyMerge" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create pmodel.mergePolygons.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create pmodel.mergePolygons.item')
                    Added = True
            except:
                sys.exit

        #############################
        ## <----( Edge Type )----> ##
        if Name == "EdgeBevel" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create edge.bevel.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create edge.bevel.item')
                    Added = True
            except:
                sys.exit

        if Name == "EdgeChamfer" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create edge.chamfer.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create edge.chamfer.item')
                    Added = True
            except:
                sys.exit

        if Name == "EdgeExtrude" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create edge.extrude.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create edge.extrude.item')
                    Added = True
            except:
                sys.exit

        if Name == "EdgeRelax" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create edge.relax.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create edge.relax.item')
                    Added = True
            except:
                sys.exit

        if Name == "EdgeFlow" and Added == False:
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create mb.edgeFlow.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create mb.edgeFlow.item')
                    Added = True
            except:
                sys.exit

        if Name == "EdgeSlide":
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create edge.slide.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create edge.slide.item')
                    Added = True
            except:
                sys.exit

        if Name == "EdgeSplit":
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create pmodel.splitEdges.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create pmodel.splitEdges.item')
                    Added = True
            except:
                sys.exit

        if Name == "EdgeToCurve":
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create pmodel.edgeToCurve.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create pmodel.edgeToCurve.item')
                    Added = True
            except:
                sys.exit

        ###############################
        ## <----( Vertex Type )----> ##
        if Name == "VertexMerge":
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create vert.merge.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create vert.merge.item')
                    Added = True
            except:
                sys.exit

        if Name == "VertexExtrude":
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create vert.extrude.item {%s}' % Preset)
                if modo_ver < 1510:
                    lx.eval('meshop.create vert.extrude.item')
            except:
                sys.exit

        if Name == "VertexBevel":
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create vert.bevel.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create vert.bevel.item')
                    Added = True
            except:
                sys.exit

        if Name == "VertexPosition":
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create vert.setpos.meshop.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create vert.setpos.meshop.item')
                    Added = True
            except:
                sys.exit

        ###############################
        ## <----( Smooth Type )----> ##
        if Name == "SmoothShift":
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create poly.smshift.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create poly.smshift.item')
                    Added = True
            except:
                sys.exit

        if Name == "Smooth":
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create smooth.meshop.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create smooth.meshop.item')
                    Added = True
            except:
                sys.exit

        if Name == "Subdivide":
            try:
                if modo_ver >= 1510:
                    lx.eval('meshop.create subdivide.tool.item {%s}' % Preset)
                    Added = True
                if modo_ver < 1510:
                    lx.eval('meshop.create subdivide.tool.item')
                    Added = True
            except:
                sys.exit
        if modo_ver >= 1500:
            if Name == "Unsubdivide":
                try:
                    if modo_ver >= 1510:
                        lx.eval('meshop.create poly.unsubdiv.item {%s}' % Preset)
                        Added = True
                    if modo_ver < 1510:
                        lx.eval('meshop.create poly.unsubdiv.item')
                        Added = True
                except:
                    sys.exit

        ###############################
        ## <----( Curve Type )----> ##
        # if Name == "CurveExtrude":
        #     try:
        #         if modo_ver >= 1510:
        #             lx.eval('meshop.create curve.extrude.item {%s}' % Preset)
        #         if modo_ver < 1510:
        #             lx.eval('meshop.create curve.extrude.item')
        #     except:
        #         sys.exit

        # if Name == "PenExtrude":
        #     try:
        #         if modo_ver >= 1510:
        #             lx.eval('meshop.create pen.extrude.item {%s}' % Preset)
        #         if modo_ver < 1510:
        #             lx.eval('meshop.create pen.extrude.item')
        #     except:
        #         sys.exit

        # if Name == "VertexBevel":
        #     try:
        #         if modo_ver >= 1510:
        #             lx.eval('meshop.create vert.bevel.item {%s}' % Preset)
        #         if modo_ver < 1510:
        #             lx.eval('meshop.create vert.bevel.item')
        #     except:
        #         sys.exit

        ###################################
        ## <----( Specific Action )----> ##
        ###################################

        sel_svc_B = lx.service.Selection()
        Item_B = modo.Scene().selected
        chan_transpacket_B = lx.object.ChannelPacketTranslation(sel_svc_B.Allocate(lx.symbol.sSELTYP_CHANNEL))

        bDoChannels = True

        for item in Item_B:
            lx.eval("schematic.addItem {%s}" % item.name)

        if bDoChannels:
            chanType_B = lx.symbol.sSELTYP_CHANNEL
            pktID_B = sel_svc_B.LookupType(chanType_B)
            numChanns_B = sel_svc_B.Count(pktID_B)
            for chanId_B in range(0, numChanns_B):
                c_B = sel_svc_B.ByIndex(pktID_B, chanId_B)
                i_B = lx.object.Item(chan_transpacket_B.Item(c_B))
                chan_idx_B = chan_transpacket_B.Index(c_B)
                cName_B = item.ChannelName(chan_idx_B)
                lx.eval("schematic.addChannel chanIdx:{%s}" % cName_B)

        for item in Item_B:
            SchemNode_B = lx.eval('schematic.node ?')
            # lx.out('Current Schematic is', SchemNode_B)
            # print(SchemNode_B)
            itemType_B = modo.Item(item).type
            # print (itemType_B)

        lx.eval("smo.GC.DeselectAll")
        lx.eval("select.node {%s} add" % SchemNode_A)
        lx.eval("select.node {%s} add" % SchemNode_B)

        if MeshOpState == False and StackOp == False:
            lx.eval("schematic.nodeSeparate top")
            lx.eval("schematic.nodeSeparate left")
            lx.eval("schematic.nodePosition {%s} 0.0 0.0 rel true" % SchemNode_B)  # abs or rel for Absolute or Relative Position
            # Select Back the next target
            lx.eval("smo.GC.DeselectAll")
            lx.eval("select.node {%s} toggle" % SchemNode_B)

        if MeshOpState == True and StackOp == False:
            lx.eval("schematic.nodeSeparate top")
            lx.eval("schematic.nodeSeparate left")
            lx.eval("schematic.nodePosition {%s} -20.0 0.0 rel true" % SchemNode_B)  # abs or rel for Absolute or Relative Position
            # Select Back the next target
            lx.eval("smo.GC.DeselectAll")
            lx.eval("select.node {%s} toggle" % SchemNode_B)

        if MeshOpState == False and StackOp == True:
            lx.eval("smo.GC.DeselectAll")
            lx.eval("select.node {%s} add" % SchemNode_B)
            lx.eval("select.node {%s} add" % SchemNode_A)
            lx.eval("schematic.nodeSeparate top")
            lx.eval("schematic.nodeSeparate left")
            lx.eval("smo.GC.DeselectAll")
            # Offset 2 Times the node to the Left Screen
            lx.eval("select.node {%s} add" % SchemNode_B)
            lx.eval("schematic.nodePosition {%s} -20.0 0.0 rel true" % SchemNode_B)  # abs or rel for Absolute or Relative Position
            lx.eval("smo.GC.DeselectAll")
            lx.eval("select.node {%s} add" % SchemNode_B)
            lx.eval("schematic.nodePosition {%s} -20.0 0.0 rel true" % SchemNode_B)  # abs or rel for Absolute or Relative Position
            # Select Back the next target
            lx.eval("smo.GC.DeselectAll")
            lx.eval("select.node {%s} toggle" % SchemNode_B)


lx.bless(SMO_MESHOP_Add_Cmd, Cmd_Name)
