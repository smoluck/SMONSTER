# python
"""
Name:         SMO_GC_SplitInTwoMeshesByLocalAxisSides_Cmd.py

Purpose:      This script is designed to
              Unmerge selected mesh in 2 Meshes by Local Axis Side (positive or negative).

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      19/08/2022
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.SplitInTwoMeshesByLocalAxisSides"
# smo.GC.SplitInTwoMeshesByLocalAxisSides z true


class SMO_GC_SplitInTwoMeshesByLocalAxisSides_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Axis", lx.symbol.sTYPE_AXIS)
        self.dyna_Add("Direction", lx.symbol.sTYPE_BOOLEAN)
        self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item;ptag ?"))
        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item;ptag ?"))
        self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - SplitInTwoMeshesByLocalAxisSides'

    def cmd_Desc(self):
        return 'Unmerge selected mesh in 2 Meshes by Local Axis Side (positive or negative).'

    def cmd_Tooltip(self):
        return 'Unmerge selected mesh in 2 Meshes by Local Axis Side (positive or negative).'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - SplitInTwoMeshesByLocalAxisSides'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Axis = self.dyna_String(0)
        DirSource = self.dyna_Bool(1)
        DirClone = bool()
        if DirSource:
            DirClone = False
        if not DirSource:
            DirClone = True

        scene = modo.scene.current()
        input_mesh = modo.Mesh()

        SelItems = (lx.evalN('query sceneservice selection ? locator'))

        RefSystemActive = bool()
        CurrentRefSystemItem = lx.eval('item.refSystem ?')
        # print(CurrentRefSystemItem)
        if len(CurrentRefSystemItem) != 0:
            RefSystemActive = True
        else:
            RefSystemActive = False

        if not RefSystemActive:
            lx.eval('item.refSystem {%s}' % format(SelItems))

        lx.eval('select.type polygon')
        lx.eval('select.all')
        if Axis == "x":
            lx.eval('smo.MIFABOMA.SliceLocal 0 0 true')
        if Axis == "y":
            lx.eval('smo.MIFABOMA.SliceLocal 1 0 true')
        if Axis == "z":
            lx.eval('smo.MIFABOMA.SliceLocal 2 0 true')

        lx.eval('select.type item')
        Mesh_A = scene.selectedByType(lx.symbol.sITYPE_MESH)

        MeshList = []
        MeshList.append(input_mesh.Ident())

        lx.eval('item.duplicate all:false mods:false')
        cloned_mesh = modo.Mesh()
        MeshList.append(cloned_mesh.Ident())
        lx.eval('smo.GC.DeleteByLocalAxisSides %s %s' % (Axis, DirClone))
        Mesh_B = scene.selectedByType(lx.symbol.sITYPE_MESH)

        scene.select(input_mesh.Ident())
        lx.eval('smo.GC.DeleteByLocalAxisSides %s %s' % (Axis, DirSource))

        lx.eval('select.drop item')

        for item in MeshList:
            scene.select(item, True)

        # lx.eval('select.drop item')

        if not RefSystemActive:
            lx.eval('item.refSystem {}')
        if RefSystemActive:
            lx.eval('item.refSystem %s' % CurrentRefSystemItem)


lx.bless(SMO_GC_SplitInTwoMeshesByLocalAxisSides_Cmd, Cmd_Name)

