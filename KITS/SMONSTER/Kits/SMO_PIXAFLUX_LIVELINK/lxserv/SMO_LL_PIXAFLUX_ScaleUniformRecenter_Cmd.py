# python
"""
Name:               SMO_LL_PIXAFLUX_ScaleUniformRecenter_Cmd.py

Purpose:            This Script is designed to:
                    Boolean Subtract the last Polygon Selection
                    (Connected Polygons) from the current Layer.

Author:             Franck ELISABETH (with the help of Tom Dymond for debug)
Website:            https://www.smoluck.com
Created:            18/07/2020
Copyright:          (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.LL.PIXAFLUX.ScaleUniformRecenter"


class SMO_LL_PIXAFLUX_ScaleUniformRecenter_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO LL PIXAFLUX - Scale Uniform Recenter'

    def cmd_Desc(self):
        return 'Scale Uniformly to 1 m Unit and Recenter mesh to Origin.'

    def cmd_Tooltip(self):
        return 'Scale Uniformly to 1 m Unit and Recenter mesh to Origin.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO LL PIXAFLUX - Scale Uniform Recenter'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        mesh = scene.selectedByType('mesh')[0]
        CsPolys = len(mesh.geometry.polygons.selected)

        # select main layer
        lx.eval('query layerservice layer.id ? main')
        # store the Unique name of the current mesh layer
        ItemUniqueName = lx.eval('query layerservice layer.id ? main')
        lx.out('Item Unique Name:', ItemUniqueName)

        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('!@absolute.pl')
        lx.eval('user.value lux_absolute_size_Uniform 1.0')
        lx.eval('@absolute.pl scale')
        lx.eval('smo.GC.Setup.MoveRotateCenterToSelection 1 0')
        lx.eval('select.type item')
        lx.eval('transform.channel pos.X 0.0')
        lx.eval('transform.channel pos.Y 0.0')
        lx.eval('transform.channel pos.Z 0.0')
        lx.eval('transform.channel rot.X 0.0')
        lx.eval('transform.channel rot.Y 0.0')
        lx.eval('transform.channel rot.Z 0.0')


lx.bless(SMO_LL_PIXAFLUX_ScaleUniformRecenter_Cmd, Cmd_Name)
