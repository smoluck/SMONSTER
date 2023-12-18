# python
"""
Name:         SMO_GC_Setup_MoveRotateCenterToSelectionWithNNrm_Cmd.py

Purpose:      This script is designed to:
              Select an Opened Mesh Move and Rotate
              the Center to Open boundary centroid and rotate it (use it in item mode).
              This build is for supporting VertexNormal Data

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      19/03/2022
Copyright:    (c) Franck Elisabeth 2017-2022
"""

from math import degrees

import lx
import lxu
import modo

Cmd_Name = "smo.GC.Setup.MoveRotateCenterToSelectionWithVNrm"
# smo.GC.Setup.MoveRotateCenterToSelectionWithVNrm 1 1


# Function for Radian to Degree
def rad(a):
    return [degrees(a)]


class SMO_GC_Setup_MoveRotateCenterToSelectionWithNNrm_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Setup - Move and Rotate Center to Selection (VNrm support)'

    def cmd_Desc(self):
        return 'Create New Mesh Layers, using target Mesh Name + PrefixName + UDIM ID from selected Mesh with VertexNormal Data update support.'

    def cmd_Tooltip(self):
        return 'Create New Mesh Layers, using target Mesh Name + PrefixName + UDIM ID from selected Mesh with VertexNormal Data update support.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Setup - Move and Rotate Center to Selection (VNrm support)'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;edge;polygon;item ?"))
        SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

        scene = modo.scene.current()
        if SelModePoly == True or SelModeEdge == True or SelModeVert == True :
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
        Target = scene.selectedByType('mesh')[0]


        VNMapName = lx.eval('pref.value application.defaultVertexNormals ?')
        #Result = ""
        m = modo.Mesh(Target)
        maps = m.geometry.vmaps.getMapsByType([lx.symbol.i_VMAP_NORMAL])
        VNormMap = bool()
        if len(maps) == 0:
            VNormMap = False
            print('No VNormMap')
        if len(maps) > 0:
            VNormMap = True
            print('VNorm detected: %s' % VNMapName)
        #    if maps[0].name == VNMapName:
        #        # Result = ("%s - GOOD" % (maps[0].name))
        #        return ""


        MoveCenter = 1
        RotateCenter = 1


        # BugFix to preserve the state of the RefSystem (item at origin in viewport)
        # This query only works when an item is selected.
        RefSystemActive = bool()
        CurrentRefSystemItem = lx.eval('item.refSystem ?')
        # print(CurrentRefSystemItem)
        if len(CurrentRefSystemItem) != 0:
            RefSystemActive = True
        else:
            RefSystemActive = False
        # print(RefSystemActive)



        if RefSystemActive:
            lx.eval('item.refSystem {}')


        if MoveCenter == 1:
            if SelModeVert:
                lx.eval('smo.MASTER.SelectModeDetector')
                CountVert = lx.eval1('user.value SMO_SelectModeDetector_CountVertSelected ?')
                # print(CountVert)
            if SelModeVert == True and CountVert >= 2:
                lx.eval('select.convert edge')
            lx.eval('workPlane.fitSelect')
            lx.eval('select.type item')
            lx.eval('select.convert type:center')
            lx.eval('matchWorkplanePos')
            lx.eval('workPlane.reset')

            if SelModePoly:
                lx.eval('select.type polygon')
            if SelModeEdge:
                lx.eval('select.type edge')
            if SelModeVert:
                lx.eval('select.type vertex')

        if RotateCenter == 1:
            if SelModeVert:
                lx.eval('smo.MASTER.SelectModeDetector')
                CountVert = lx.eval1('user.value SMO_SelectModeDetector_CountVertSelected ?')
                # print(CountVert)
            if SelModeVert == True and CountVert >= 2:
                lx.eval('select.convert edge')
            lx.eval('workPlane.fitSelect')

            if VNormMap:
                # ItemCenX = lx.eval('workplane.edit ? 0 0 0 0 0')
                # ItemCenY = lx.eval('workplane.edit 0 ? 0 0 0 0')
                # ItemCenZ = lx.eval('workplane.edit 0 0 ? 0 0 0')
                # lx.out('Workplane posX:', ItemCenX)
                # lx.out('Workplane posY:', ItemCenY)
                # lx.out('Workplane posZ:', ItemCenZ)
                # ItemRotXrad = lx.eval('workplane.edit 0 0 0 ? 0 0')
                # ItemRotYrad = lx.eval('workplane.edit 0 0 0 0 ? 0')
                # ItemRotZrad = lx.eval('workplane.edit 0 0 0 0 0 ?')
                # ItemRotX = math.degrees(ItemRotXrad)
                # ItemRotY = math.degrees(ItemRotYrad)
                # ItemRotZ = math.degrees(ItemRotZrad)
                # lx.eval('workPlane.state false')
                # lx.out('Workplane rot X:', ItemRotX)
                # lx.out('Workplane rot Y:', ItemRotY)
                # lx.out('Workplane rot Z:', ItemRotZ)

                lx.eval('select.type polygon')
                lx.eval('select.all')
                lx.eval('smo.CAD.CopyCutAsChildOfCurrentMesh 0 1 4 true')
                lx.eval('select.type item')
                TargetCopy = scene.selectedByType('mesh')[0]
                lx.eval('item.parent parent:{} inPlace:1')
                lx.eval('transform.freeze')
                scene.select(Target)


        lx.eval('select.type item')
        lx.eval('select.convert type:center')
        # lx.eval('workPlane.edit cenX:%f cenY:%f cenZ:%f rotX:%f rotY:%f rotZ:%f' % (ItemCenX, ItemCenY, ItemCenZ, ItemRotX, ItemRotY, ItemRotZ))
        lx.eval('matchWorkplaneRot')
        lx.eval('workPlane.reset')

        if VNormMap:
            lx.eval('select.type polygon')
            lx.eval('select.all')
            lx.eval('delete')
            scene.select(TargetCopy)
            lx.eval('select.type polygon')
            lx.eval('select.all')
            lx.eval('copy')
            lx.eval('select.type item')
            lx.eval('select.type polygon')
            scene.select(Target)
            lx.eval('select.type polygon')
            lx.eval('paste')
            lx.eval('select.type item')
            scene.select(TargetCopy)
            lx.eval('!delete')
            scene.select(Target)


lx.bless(SMO_GC_Setup_MoveRotateCenterToSelectionWithNNrm_Cmd, Cmd_Name)
