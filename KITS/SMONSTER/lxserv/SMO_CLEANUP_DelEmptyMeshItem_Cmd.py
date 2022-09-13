# python
# ---------------------------------------
# Name:         SMO_CLEANUP_DelEmptyMeshItem_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Delete Empty Mesh Layers (default Mesh Layer) in current scene.
#
#
# Author:       Franck ELISABETH (with the help of James O'Hare)
# Website:      http://www.smoluck.com
#
# Created:      17/02/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.CLEANUP.DelEmptyMeshItem"


class SMO_Cleanup_DelEmptyMeshItem_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CLEANUP - Delete Empty Mesh Item'

    def cmd_Desc(self):
        return 'Delete Empty Mesh Layers (default Mesh Layer) in current scene.'

    def cmd_Tooltip(self):
        return 'Delete Empty Mesh Layers (default Mesh Layer) in current scene.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CLEANUP - Delete Empty Mesh Item'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        # -----------------------------------------------#
        # Delete Empty Mesh Layers (default Mesh Layer) #
        # -----------------------------------------------#

        # # First we must select the scene and then all the mesh layers in our scene.
        lx.eval('select.drop item')
        lx.eval('select.itemType mesh')
        # lx.eval('select.layerTree all:1')
        ItemCount = lx.eval('query layerservice layer.N ? fg')
        # lx.out('Selected Item count:', ItemCount)

        DefaultMeshItemList = []
        if ItemCount == 0:
            pass

        if ItemCount == 1:
            numOfPoly = lx.eval('query layerservice poly.N ? all')
            # lx.out('Poly Count:', numOfPoly)
            # If there are no verts, we delete the mesh item layer.
            if numOfPoly == 0:
                lx.eval('!item.delete')

        elif ItemCount > 1:
            # Variables
            DefaultMeshItemList = lx.eval('query sceneservice selection ? mesh')  # mesh item layers
            # lx.out('Mesh list:', DefaultMeshItemList)
            # Create the monitor item
            m = lx.Monitor()
            m.init(len(DefaultMeshItemList))

            # For each mesh item layer, we check to see if there are any verts in the layer...
            for mesh in DefaultMeshItemList:
                # mesh.select(True)
                lx.eval('select.drop item')
                lx.eval('select.item %s' % mesh)
                lx.eval('query layerservice layer.index ? selected')  # scene
                numOfPoly = lx.eval('query layerservice poly.N ? all')
                # lx.out('Poly Count:', numOfPoly)

                # If there are no verts, we delete the mesh item layer.
                if numOfPoly == 0:
                    lx.eval('!item.delete')

                # Increare progress monitor
                m.step(1)
        lx.eval('select.drop item')

        del DefaultMeshItemList
        ###############################################


lx.bless(SMO_Cleanup_DelEmptyMeshItem_Cmd, Cmd_Name)
