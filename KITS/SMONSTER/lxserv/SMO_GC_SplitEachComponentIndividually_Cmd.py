# python
"""
Name:         SMO_GC_SplitEachComponentIndividually_Cmd.py

Purpose:      This script is designed to
              Separate current Mesh by Edges (to create Polyline of 1 Edge).
              It Split each Polyline Edges into an individual item.

Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
Website:      https://www.linkedin.com/in/smoluck/
Created:      17/09/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.SplitEachComponentIndividually"
# smo.GC.SplitEachComponentIndividually 1 1 0


class SMO_GC_SplitEachComponentIndividually_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Component Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Separate Meshes", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Incremental Save Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact (self):
        pass

    def cmd_UserName (self):
        return 'SMO GC - Split each Component Individually'

    def cmd_Desc (self):
        return 'Separate current Mesh by Component. It Split each Vertex OR Polyline Edges OR Polygons into an individual piece. You can separate all Component by an individual mesh too.'

    def cmd_Tooltip (self):
        return 'Separate current Mesh by Component. It Split each Vertex OR Polyline Edges OR Polygons into an individual piece. You can separate all Component by an individual mesh too.'

    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName (self):
        return 'SMO GC - Split each Component Individually'

    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.Scene()

        # -------------- Index Style START Procedure  -------------- #
        # Bugfix for items that cant be detected when "Index Style" is not using underscore as separator.
        # Problem caused by item.UniqueName() at line 124
        IndexStyle = lx.eval("pref.value application.indexStyle ?")
        if IndexStyle is not "uscore":
            lx.eval("pref.value application.indexStyle uscore")
        # -------------------------------------------- #

        Component_Mode = self.dyna_Int(0)           # 0 = Vertex, 1 = Edges or 2 = Polygons
        Separate_Mode = self.dyna_Int(1)            # 0 = same mesh or 1 = Separate meshes
        Incremental_Save_Mode = self.dyna_Int(2)    # Incremental saving at each iteration. (sort of Safe Mode)

        lx.eval('select.type item')

        # Get the selected layer.
        TargetMesh = lx.eval('query layerservice layers ? selected')
        lx.out('Target Mesh Layer:', TargetMesh)

        ItemUniqueName = lx.eval('query layerservice layer.id ? main')      # store the Unique name of the current mesh layer
        # lx.out('Item Unique Name:', ItemUniqueName)

        if Component_Mode == 0:
            TotalVertex = lx.eval('query layerservice vert.N ? all')
            # lx.out('Count Selected Vertex',TotalVertex)

        if Component_Mode == 1:
            TotalEdge = lx.eval('query layerservice edge.N ? all')
            # lx.out('Count Selected Edge',TotalEdge)

        if Component_Mode == 2:
            TotalPoly = lx.eval('query layerservice poly.N ? all')
            # lx.out('Count Selected Poly',TotalPoly)

        if Component_Mode == 0:
            MeshIn = scene.selectedByType('mesh')[0]

            Target_Name = lx.eval('item.name ? xfrmcore')
            # lx.out('Item Name:', Target_Name)

            scene.select(MeshIn)

            lx.eval('select.type vertex')
            lx.eval('select.drop vertex')
            lx.eval('select.all')
            lx.eval('copy')
            lx.eval('select.all')
            lx.eval('!delete')
            lx.eval('paste')
            lx.eval('select.type item')
            lx.eval('select.drop item')
            scene.select(MeshIn)
            if Incremental_Save_Mode == 1:
                lx.eval('@incSaveEXP.py')

        if Component_Mode == 1:
            lx.eval('smo.GC.SplitEachEdgeIndividually %s' % Incremental_Save_Mode)

        if Component_Mode == 2:
            lx.eval('smo.GC.SplitEachPolyIndividually %s' % Incremental_Save_Mode)

        if Separate_Mode == 1:
            if Component_Mode == 0:
                scene.select(MeshIn)

                m = lx.Monitor()
                m.init(1)

                TotalVertexInMesh = lx.eval('query layerservice vert.N ? all')
                # lx.out('Count Selected Vertex',TotalVertexInMesh)

                index = 0
                MaxSteps = TotalVertexInMesh
                for steps in range(MaxSteps):
                    m.step(1)

                    # LeftVertex = lx.eval('query layerservice vert.N ? all')
                    # # lx.out('Count Selected Vertex',TotalVertexInMesh)

                    if TotalVertexInMesh > index:
                        lx.eval('select.type vertex')
                        lx.eval('select.drop vertex')
                        # Select the first vertex.
                        lx.eval('select.element layer:%s type:vertex mode:add index:%s' % (TargetMesh, index))
                        lx.eval('copy')
                        lx.eval('layer.new')
                        lx.eval('item.name {%s} xfrmcore' % Target_Name)
                        lx.eval('select.type vertex')
                        lx.eval('paste')
                        lx.eval('select.type item')
                        lx.eval('select.drop item')
                        scene.select(MeshIn)
                        if Incremental_Save_Mode == 1:
                            lx.eval('@incSaveEXP.py')
                    index += 1

                scene.select(MeshIn)
                lx.eval('!delete')

            if Component_Mode == 1 or Component_Mode == 2:
                lx.eval('layer.unmergeMeshes')

        # -------------- Index Style END Procedure  -------------- #
        if IndexStyle is not "uscore":
            lx.eval("pref.value application.indexStyle %s" % IndexStyle)
        # -------------------------------------------- #


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_SplitEachComponentIndividually_Cmd, Cmd_Name)
