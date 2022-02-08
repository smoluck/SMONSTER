#python
#---------------------------------------
# Name:         SMO_QT_ListAllColorIDSelSet_Cmd.py
# Version:      1.00
#
# Purpose:      This script is designed to
#               Set a random Diffuse Color override
#               using Selection Set (polygons) on the selected Mesh Layers
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      17/05/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import modo, lx, lxu

Command_Name = "smo.QT.ListAllColorIDSelSet"
# smo.QT.ListAllColorIDSelSet


tag = "ColorID_"
def GetColorIDSelSetList():
    listpolset = []
    lx.eval('select.itemType mesh')
    # lx.eval('query layerservice layer.id ? main')# select main layer
    num_polset = lx.eval('query layerservice polset.N ? all')# number of Poly SS
    for i in range(num_polset):
        polset_name = lx.eval('query layerservice polset.name ? %s' %i)
        if polset_name.startswith(tag):
            listpolset.append(polset_name)
        # lx.out(sorted(listpolset))
    lx.eval('smo.GC.DeselectAll')
    return listpolset
# print(GetColorIDSelSetList())

class SMO_QT_ListAllColorIDSelSet_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO QT - List current ColorID Selections Set Max Count'

    def cmd_Desc(self):
        return 'Set a random Diffuse Color override using Selection Set (polygons) on the selected Mesh Layers.'

    def cmd_Tooltip(self):
        return 'Set a random Diffuse Color override using Selection Set (polygons) on the selected Mesh Layers.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO QT - Set ColorID'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        items = scene.selected
        lx.out('current scene have %s ColorID PolySelSet.' % (GetColorIDSelSetList()))
        # print(GetColorIDSelSetList())
        scene.select(items)

lx.bless(SMO_QT_ListAllColorIDSelSet_Cmd, Command_Name)