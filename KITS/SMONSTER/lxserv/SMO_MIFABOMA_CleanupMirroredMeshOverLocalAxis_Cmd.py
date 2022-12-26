# python
"""
# Name:         SMO_MIFABOMA_CleanupMirroredMeshOverLocalAxis_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Cleanup selected Mesh along a given axis Local (x, y, z)
#               in order to remove Mirrored Opposite Side Argument boolean
#               (Positive or Negative). Then recreate instances out of that mesh along that axis.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      17/08/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.MIFABOMA.CleanupMirroredMeshOverLocalAxis"
# smo.MIFABOMA.CleanupMirroredMeshOverLocalAxis z true


class SMO_MIFABOMA_CleanupMirroredMeshOverLocalAxis_Cmd(lxu.command.BasicCommand):
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
        return 'SMO MIFABOMA - CleanupMirroredMeshOverLocalAxis'

    def cmd_Desc(self):
        return 'Cleanup selected Mesh along a given axis Local (x, y, z) in order to remove Mirrored Opposite Side Argument boolean (Positive or Negative). Then recreate instances out of that mesh along that axis.'

    def cmd_Tooltip(self):
        return 'Cleanup selected Mesh along a given axis Local (x, y, z) in order to remove Mirrored Opposite Side Argument boolean (Positive or Negative). Then recreate instances out of that mesh along that axis.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO MIFABOMA - CleanupMirroredMeshOverLocalAxis'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        CleanupAxis = self.dyna_String(0)
        PositiveDir = self.dyna_Bool(1)

        scene = modo.scene.current()
        mesh = modo.Mesh()
        RefSystemActive = bool()
        CurrentRefSystemItem = lx.eval('item.refSystem ?')
        print(CurrentRefSystemItem)

        DeleteDir = bool()
        if PositiveDir:
            DeleteDir = False
        if not PositiveDir:
            DeleteDir = True


        Mesh_Target = scene.selectedByType('mesh')[0]
        lx.out('Target Mesh:', Mesh_Target)

        selitems = len(lx.evalN('query sceneservice selection ? mesh'))
        lx.out('selitems', selitems)

        sel_items = list(scene.selectedByType("mesh"))

        # lx.eval('smo.GC.IsolateItemAndInstances')
        if not RefSystemActive:
            lx.eval('item.refSystem %s' % (mesh.Ident()))


        lx.eval('smo.GC.SelectVertexByLocalAxis %s %s' % (CleanupAxis, DeleteDir))
        if lx.eval("query layerservice vert.N ? selected") > 0:
            lx.eval('delete')
        lx.eval('select.type item')
        # Select the First Item.
        lx.eval('select.subItem %s set mesh 0 0' % Mesh_Target.name)
        if CleanupAxis == "x":
            lx.eval('smo.MIFABOMA.Mirror_ViaUserPref 0 true false')
        if CleanupAxis == "y":
            lx.eval('smo.MIFABOMA.Mirror_ViaUserPref 1 true false')
        if CleanupAxis == "z":
            lx.eval('smo.MIFABOMA.Mirror_ViaUserPref 2 true false')

        lx.eval('select.subItem %s set mesh 0 0' % Mesh_Target.name)
        lx.eval('select.itemInstances')
        lx.eval('select.subItem %s add mesh 0 0' % Mesh_Target.name)

        # lx.eval('smo.GC.ReleaseFromIsolateMode')
        lx.eval('item.refSystem {}')


lx.bless(SMO_MIFABOMA_CleanupMirroredMeshOverLocalAxis_Cmd, Cmd_Name)

