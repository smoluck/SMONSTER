# python
"""
Name:         SMO_GC_TransferVNrmFromMouseSurface_Cmd.py

Purpose:      This script is designed to:
              VertexNormalTransfer on current Selected component
              from the Surface under mouse pointer (mouseOver).

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      31/12/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.TransferVNrmFromMouseOverSurface"
# smo.GC.TransferVNrmFromMouseOverSurface


class SMO_GC_TransferVNrmFromMouseOverSurface_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        # self.dyna_Add("Witdh Value", lx.symbol.sTYPE_DISTANCE)
        # scene = modo.scene.current()
        # self.Check = bool()
        # self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        # self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        # self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        # self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        # if self.SelModeVert == True or self.SelModeEdge == True or self.SelModePoly == True:
        #     try:
        #         lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
        #         self.TargetMeshList = lxu.select.ItemSelection().current()
        #     except:
        #         self.TargetMeshList = []
        #
        #     if self.SelModeVert == True:
        #         selected_mesh = scene.selected[0]
        #         self.CsVert = len(selected_mesh.geometry.vertices.selected)
        #         if self.CsVert >= 1:
        #             self.Check = True
        #         else:
        #             self.Check = False
        #
        #     if self.SelModeEdge == True:
        #         selected_mesh = scene.selected[0]
        #         self.CsEdges = len(selected_mesh.geometry.edges.selected)
        #         if self.CsEdges >= 1:
        #             self.Check = True
        #         else:
        #             self.Check = False
        #
        #     if self.SelModePoly == True:
        #         selected_mesh = scene.selected[0]
        #         self.CsVert = len(selected_mesh.geometry.polygons.selected)
        #         if self.CsVert >= 1:
        #             self.Check = True
        #         else:
        #             self.Check = False
        #     print(self.Check)
        #     if self.Check == True:
        #         lx.eval('select.editSet TransfVNrmFromMouseOverSurface add {}')
        #
        #     # If we do have something selected, put it in self.TargetMeshList
        #     if len(self.TargetMeshList) > 0:
        #         self.TargetMeshList = TargetMeshList
        #     else:
        #         self.TargetMeshList = None
        #     # print(self.TargetMeshList)
        #     # print(self.Check)
        #     for item in self.TargetMeshList:
        #         itemType = modo.Item(item).type
        #         item = lx.object.Item(item)
        #         item_name = item.UniqueName()
        #         if itemType != "mesh":
        #             scene.deselect(item_name)
        #         self.Target = scene.select(item)
        #     self.MeshTarget = modo.Scene().selected
        #
        # if self.Check == True:
        #     lx.eval('query view3dservice mouse ?')
        #     view_under_mouse = lx.eval('query view3dservice mouse.view ?')
        #     lx.eval('query view3dservice view.index ? %s' % view_under_mouse)
        #     lx.eval('query view3dservice mouse.pos ?')
        #     Item_under_mouse = lx.eval('query view3dservice element.over ? ITEM ')
        #     Poly_under_mouse = lx.eval('query view3dservice element.over ? POLY ')
        #     # edge_under_mouse = lx.eval('query view3dservice element.over ? EDGE ')
        #     hitpos = lx.eval('query view3dservice mouse.hitpos ?')
        #
        #     # lx.out('View under mouse:', view_under_mouse)
        #     # lx.out('Hit Position:', hitpos)
        #     # lx.out('Items under mouse:', Item_under_mouse)
        #     # lx.out('Polygon under mouse:', Poly_under_mouse)
        #
        #     # lx.eval('select.drop polygon')
        #     # lx.eval('materials.underMouse')
        #
        #     self.BGSuccess = bool()
        #     try:
        #         lx.eval('select.3DElementUnderMouse')
        #         self.BGSuccess = True
        #     except:
        #         self.BGSuccess = False
        #     self.BG = scene.select(Item_under_mouse)
        #     self.MeshBG = modo.Scene().selected
        #     lx.eval('smo.GC.DeselectAll')


    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Transfer Vertex Normal Data from Polygon under Mouse'

    def cmd_Desc(self):
        return 'Transfer Vertex Normal Data from Polygon under Mouse onto current selected elements.'

    def cmd_Tooltip(self):
        return 'Transfer Vertex Normal Data from Polygon under Mouse onto current selected elements.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Transfer Vertex Normal Data from Polygon under Mouse'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        Check = bool()
        SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        if SelModeVert == True or SelModeEdge == True or SelModePoly == True:
            try:
                lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
                TargetMeshList = lxu.select.ItemSelection().current()
            except:
                TargetMeshList = []

            if SelModeVert:
                selected_mesh = scene.selected[0]
                CsVert = len(selected_mesh.geometry.vertices.selected)
                if CsVert >= 1:
                    Check = True
                else:
                    Check = False

            if SelModeEdge:
                selected_mesh = scene.selected[0]
                CsEdges = len(selected_mesh.geometry.edges.selected)
                if CsEdges >= 1:
                    Check = True
                else:
                    Check = False

            if SelModePoly:
                selected_mesh = scene.selected[0]
                CsVert = len(selected_mesh.geometry.polygons.selected)
                if CsVert >= 1:
                    Check = True
                else:
                    Check = False
            # print(Check)
            if Check:
                lx.eval('select.editSet TransfVNrmFromMouseOverSurface add {}')

            # If we do have something selected, put it in self.TargetMeshList
            if len(TargetMeshList) > 0:
                TargetMeshList = TargetMeshList
            else:
                TargetMeshList = None
            # print(self.TargetMeshList)
            # print(self.Check)
            for item in TargetMeshList:
                itemType = modo.Item(item).type
                item = lx.object.Item(item)
                item_name = item.UniqueName()
                if itemType != "mesh":
                    scene.deselect(item_name)
                Target = scene.select(item)
            MeshTarget = modo.Scene().selected

        if Check:
            lx.eval('query view3dservice mouse ?')
            view_under_mouse = lx.eval('query view3dservice mouse.view ?')
            lx.eval('query view3dservice view.index ? %s' % view_under_mouse)
            lx.eval('query view3dservice mouse.pos ?')
            Item_under_mouse = lx.eval('query view3dservice element.over ? ITEM ')
            Poly_under_mouse = lx.eval('query view3dservice element.over ? POLY ')
            # edge_under_mouse = lx.eval('query view3dservice element.over ? EDGE ')
            hitpos = lx.eval('query view3dservice mouse.hitpos ?')

            # lx.out('View under mouse:', view_under_mouse)
            # lx.out('Hit Position:', hitpos)
            # lx.out('Items under mouse:', Item_under_mouse)
            # lx.out('Polygon under mouse:', Poly_under_mouse)

            # lx.eval('select.drop polygon')
            # lx.eval('materials.underMouse')

            BGSuccess = bool()
            try:
                lx.eval('select.3DElementUnderMouse')
                BGSuccess = True
            except:
                BGSuccess = False
            BG = scene.select(Item_under_mouse)
            LockElem = bool(lx.eval('user.value SMO_UseVal_GC_TransVNFromBG_LockElem ?'))
            MeshBG = modo.Scene().selected
            lx.eval('smo.GC.DeselectAll')


            # ------------------------ #
            # <----( Main Macro )----> #
            # ------------------------ #
        if Check == True and BGSuccess == True:
            if MeshTarget != MeshBG :
                lx.eval('select.type item')
                scene.select(MeshTarget)
                scene.select(MeshBG, "add")
                lx.eval('hide.unsel')
                lx.eval('smo.GC.DeselectAll')
                scene.select(MeshTarget)
                if SelModeVert:
                    lx.eval('select.type vertex')
                if SelModeEdge:
                    lx.eval('select.type edge')
                if SelModePoly:
                    lx.eval('select.type polygon')
                lx.eval('select.useSet TransfVNrmFromMouseOverSurface select')
                lx.eval('vertMap.transferNormals false')
                if LockElem:
                    lx.eval('lock.sel')
                lx.eval('select.type item')
                lx.eval('unhide')
                if SelModeVert:
                    lx.eval('select.drop vertex')
                if SelModeEdge:
                    lx.eval('select.drop edge')
                if SelModePoly:
                    lx.eval('select.drop polygon')
                lx.eval('select.deleteSet TransfVNrmFromMouseOverSurface')

            if MeshTarget == MeshBG :
                lx.eval('select.type item')
                scene.select(MeshTarget)
                lx.eval('select.type polygon')
                lx.eval('select.drop polygon')
                Poly_under_mouse = lx.eval('query view3dservice element.over ? POLY ')
                # print(Poly_under_mouse)
                Pol = bool()
                try:
                    lx.eval('select.3DElementUnderMouse')
                    Pol = True
                except:
                    Pol = False
                if Pol:
                    # lx.eval('smo.GC.SelectCoPlanarPoly 0 2')
                    lx.eval('select.connect')
                    lx.eval('smo.CAD.CopyCutAsChildOfCurrentMesh false true 1 true')
                    MeshBG = modo.Scene().selected
                    scene.select(MeshTarget)
                    scene.select(MeshBG, "add")
                    lx.eval('select.type item')
                    lx.eval('hide.unsel')
                    lx.eval('smo.GC.DeselectAll')
                scene.select(MeshTarget)
                if SelModeVert:
                    lx.eval('select.type vertex')
                if SelModeEdge:
                    lx.eval('select.type edge')
                if SelModePoly:
                    lx.eval('select.type polygon')
                lx.eval('select.useSet TransfVNrmFromMouseOverSurface select')
                lx.eval('vertMap.transferNormals false')
                if LockElem:
                    lx.eval('lock.sel')
                lx.eval('select.type item')
                lx.eval('unhide')
                if SelModeVert:
                    lx.eval('select.type vertex')
                    lx.eval('select.drop vertex')
                if SelModeEdge:
                    lx.eval('select.type edge')
                    lx.eval('select.drop edge')
                if SelModePoly:
                    lx.eval('select.type polygon')
                    lx.eval('select.drop polygon')
                lx.eval('select.deleteSet TransfVNrmFromMouseOverSurface')
                lx.eval('select.type item')
                scene.select(MeshBG)
                lx.eval('!delete')
                scene.select(MeshTarget)
                if SelModeVert:
                    lx.eval('select.type vertex')
                if SelModeEdge:
                    lx.eval('select.type edge')
                if SelModePoly:
                    lx.eval('select.type polygon')


lx.bless(SMO_GC_TransferVNrmFromMouseOverSurface_Cmd, Cmd_Name)
