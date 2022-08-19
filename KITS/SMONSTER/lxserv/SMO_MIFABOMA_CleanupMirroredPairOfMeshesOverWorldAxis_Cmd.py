# python
# ---------------------------------------
# Name:         SMO_MIFABOMA_CleanupMirroredPairOfMeshesOverWorldAxis_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Cleanup selected Pairs of Meshes in order to align them over world axis
#               and recreate instances out of that mesh.
#               it use X Y Z axis as argument and Positive or Negative Direction
#               to define what is the Side part that we preserve.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      17/08/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.MIFABOMA.CleanupMirroredPairOfMeshesOverWorldAxis"
# smo.MIFABOMA.CleanupMirroredPairOfMeshesOverWorldAxis z true

class SMO_MIFABOMA_CleanupMirroredPairOfMeshesOverWorldAxis_Cmd(lxu.command.BasicCommand):
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
        return 'SMO MIFABOMA - CleanupMirroredPairOfMeshesOverWorldAxis'

    def cmd_Desc(self):
        return 'Cleanup selected Mirrored Mesh in order to align it over world axis and recreate instances out of that mesh. It use X Y Z axis as argument and Positive or Negative Direction to define what is the Side part that we preserve.'

    def cmd_Tooltip(self):
        return 'Cleanup selected Mirrored Mesh in order to align it over world axis and recreate instances out of that mesh. It use X Y Z axis as argument and Positive or Negative Direction to define what is the Side part that we preserve.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO MIFABOMA - CleanupMirroredPairOfMeshesOverWorldAxis'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):

        Axis = self.dyna_String(0)
        PositiveDir = self.dyna_Bool(1)

        scene = modo.scene.current()
        mesh = modo.Mesh()

        Mesh_A = scene.selectedByType('mesh')[0]
        lx.out('First Mesh:', Mesh_A)

        Mesh_B = scene.selectedByType('mesh')[1]
        lx.out('Second Mesh:', Mesh_B)

        selitems = len(lx.evalN('query sceneservice selection ? mesh'))
        lx.out('selitems', selitems)

        sel_items = list(scene.selectedByType("mesh"))
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('copy')
        lx.eval('select.drop polygon')
        lx.eval('select.type item')

        if selitems == 2:
            lx.eval('smo.GC.DeselectAll')
            lx.eval('layer.new')
            BBox = modo.Mesh()
            lx.eval('select.type polygon')
            lx.eval('paste')
            lx.eval('select.drop polygon')
            lx.eval('select.type item')
            lx.eval('smo.GC.Setup.MoveRotateCenterToSelection 1 0')
            WPX = lx.eval("transform.channel pos.X ?")
            WPY = lx.eval("transform.channel pos.Y ?")
            WPZ = lx.eval("transform.channel pos.Z ?")
            print(WPX)
            print(WPY)
            print(WPZ)

        if WPZ != 0.0:
            
            lx.eval("smo.GC.AlignToAxisWorldZero z")
            lx.eval('smo.GC.IsolateItemAndInstances')
            lx.eval('select.type vertex')
            lx.eval('select.drop vertex')
        lx.eval('smo.GC.SelectVertexByLocalAxis z true')

        if lx.eval("query layerservice vert.N ? selected") > 0:
            lx.eval('delete')

        # Select the First Item.
        lx.eval('select.subItem %s set mesh 0 0' % Mesh_B.name)


lx.bless(SMO_MIFABOMA_CleanupMirroredPairOfMeshesOverWorldAxis_Cmd, Cmd_Name)

