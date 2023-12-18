# python
"""
Name:         SMO_GC_FreezeSubdivPolys_Cmd.py

Purpose:      This script is designed to
              Freeze the Subdiv or Catmull-Clark polygons in the given Mesh item.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      17/12/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.FreezeSubdivPoly"
# smo.GC.FreezeSubdivPoly


class SMO_GC_FreezeSubdivPolys_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Freeze Subdiv Polys'

    def cmd_Desc(self):
        return 'Freeze the Subdiv or Catmull-Clark polygons in the given Mesh item.'

    def cmd_Tooltip(self):
        return 'Freeze the Subdiv or Catmull-Clark polygons in the given Mesh item.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC -Freeze Subdiv Polys'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        meshes = scene.selectedByType(lx.symbol.sITYPE_MESH)

        for item in meshes:
            lx.eval('select.item %s' % item)

            lx.eval('select.type polygon')
            # select all subdiv polys
            lx.eval('select.polygon add type subdiv 1')
            # select all Psubdiv polys (Catmull-Clark)
            lx.eval('select.polygon add type psubdiv 7')

            SubdivState = lx.eval('query layerservice polys ? selected')
            # lx.out('state', SubdivState)
            if SubdivState is not None:
                lx.out("There are subdivs in this mesh.")
                lx.eval('mesh.patchSubdiv 3')
                lx.eval('mesh.psubSubdiv 3')
                lx.eval('poly.freeze face')

            lx.eval('!deformer.freeze false')
            lx.eval('select.drop polygon')
            lx.eval('select.type item')

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_FreezeSubdivPolys_Cmd, Cmd_Name)
