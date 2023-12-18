# python
"""
Name:         SMO_GC_StarTriple_Cmd

Purpose:      This script is designed to:
              Star Triple area using touching polygons and same Facing Ratio.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      15/04/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.StarTriple"
# smo.GC.StarTriple


class SMO_GC_StarTriple_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Star Triple'

    def cmd_Desc(self):
        return 'Star Triple area using touching polygons and same Facing Ratio.'

    def cmd_Tooltip(self):
        return 'Star Triple area using touching polygons and same Facing Ratio.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Star Triple'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        VNMapName = lx.eval('pref.value application.defaultVertexNormals ?')
        # print(VNMapName)

        if self.SelModePoly:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        mesh = scene.selectedByType('mesh')[0]
        meshID = mesh.Ident()
        # print('selected mesh ID:', meshID)

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


        # #################################
        # ## Solution B
        # ## Local Scale Transform.
        # ACAuto = lx.test('tool.set actr.auto on')
        # ACSelection = lx.test('tool.set actr.select on')
        # ACSelBorder = lx.test('tool.set actr.border on')
        # ACElement = lx.test('tool.set actr.element on')
        # ACScreen = lx.test('tool.set actr.screen on')
        # ACOrigin = lx.test('tool.set actr.origin on')
        # ACParent = lx.test('tool.set actr.parent on')
        # ACLocal = lx.test('tool.set actr.local on')
        # ACPivot = lx.test('tool.set actr.pivot on')
        # print('Action Center Automatic:', ACAuto)
        # print('Action Center Selection:', ACSelection)
        # print('Action Center Border:', ACSelBorder)
        # print('Action Center Element:', ACElement)
        # print('Action Center Screen:', ACScreen)
        # print('Action Center Origin:', ACOrigin)
        # print('Action Center Parent:', ACParent)
        # print('Action Center Local:', ACLocal)
        # print('Action Center Pivot:', ACPivot)
        #
        # AAAuto = lx.test('tool.set axis.auto on')
        # AASelection = lx.test('tool.set axis.select on')
        # AASelBorder = lx.test('tool.set axis.border on')
        # AAElement = lx.test('tool.set axis.element on')
        # AAScreen = lx.test('tool.set axis.screen on')
        # AAOrigin = lx.test('tool.set axis.origin on')
        # AAParent = lx.test('tool.set axis.parent on')
        # AALocal = lx.test('tool.set axis.local on')
        # AAPivot = lx.test('tool.set axis.pivot on')
        # print('Action Axis Automatic:', AAAuto)
        # print('Action Axis Selection:', AASelection)
        # print('Action Axis Border:', AASelBorder)
        # print('Action Axis Element:', AAElement)
        # print('Action Axis Screen:', AAScreen)
        # print('Action Axis Origin:', AAOrigin)
        # print('Action Axis Parent:', AAParent)
        # print('Action Axis Local:', AALocal)
        # print('Action Axis Pivot:', AAPivot)
        #
        # ACNone = bool()
        # if ACAuto == False and ACSelection == False and ACSelBorder == False and ACElement == False and ACScreen == False and ACOrigin == False and ACParent == False and ACLocal == False and ACPivot == False and AAAuto == False and AASelection == False and AASelBorder == False and AAElement == False and AAScreen == False and AAOrigin == False and AAParent == False and AALocal == False and AAPivot == False:
        #     ACNone = True
        # print('Action Center set to NONE:', ACNone)
        # ## Solution B
        # #################################



        VertNrnMapList = []

        lx.eval('select.type polygon')
        # lx.eval('smo.GC.SelectCoPlanarPoly 0 2 0')

        lx.eval('!poly.merge')
        lx.eval('script.run "macro.scriptservice:92663570022:macro"')

        lx.eval('select.type polygon')
        lx.eval('tool.noChange')
        lx.eval('tool.set poly.bevel on')
        # Command Block Begin: ToolAdjustment
        lx.eval('tool.attr poly.bevel shift 0.0')
        lx.eval('tool.attr poly.bevel inset 0.00001')
        # Command Block End: ToolAdjustment
        lx.eval('tool.doApply')
        lx.eval('tool.drop')

        lx.eval('select.expand')
        lx.eval('select.convert vertex')
        lx.eval('select.editSet StarTriple_VertSelSet add')
        lx.eval('select.type polygon')
        lx.eval('script.run "macro.scriptservice:92663570022:macro"')

        lx.eval('select.type polygon')
        lx.eval('select.editSet StarTriple_PolySelSet add')

        # Schrink the Polygon to it's Local Center. Bug fix to offseted StarTriple
        lx.eval('select.contract')


        #################################
        ## Solution A
        ## Collapse Poly Solution
        lx.eval('poly.collapse')
        ## Collapse Poly Solution
        #################################


        # #################################
        # ## Solution B
        # ## Local Scale Transform.
        # if ACNone == True or ACLocal == False:
        #     # lx.eval('actionCenter.state enable:true')
        #     lx.eval('tool.set actr.local on')
        #     lx.eval('tool.set axis.local on')
        # ####### TOOL Action ######
        # lx.eval('tool.set TransformScale on')
        # lx.eval('tool.noChange')
        # lx.eval('tool.attr xfrm.transform SX 0.0')
        # lx.eval('tool.attr xfrm.transform SY 0.0')
        # lx.eval('tool.attr xfrm.transform SZ 0.0')
        # lx.eval('tool.doApply')
        # lx.eval('select.nextMode')
        # lx.eval('poly.collapse')
        # ## Local Scale Transform.
        # #################################


        lx.eval('select.nextMode') # to drop the tool
        lx.eval('select.type polygon')
        lx.eval('select.useSet StarTriple_PolySelSet replace')

        # Vertex Nornmal Map (From CAD) Detection on HighPoly.
        meshUpdateVNMap = modo.Mesh()
        VMaps = meshUpdateVNMap.geometry.vmaps
        # print(VMaps)
        VMapCount = len(meshUpdateVNMap.geometry.vmaps)
        # print(VMapCount)
        if VMapCount > 0:
            for map in VMaps:
                mapObj = lx.object.MeshMap(map)
                # print(mapObj.Name())
                # print(mapObj.Type())
                if mapObj.Type() == 1313821261:  # int id for Vertex Normal map
                    lx.eval("select.vertexMap {%s} norm mode:remove" % mapObj.Name())
                    lx.eval("select.vertexMap {%s} norm mode:add" % mapObj.Name())
                    CurrentVertexNormalMapName = mapObj.Name()
                    # print(CurrentVertexNormalMapName)
                    VertNrnMapList.append(CurrentVertexNormalMapName)

                    # Vertex Nornmal Map Detected. Delete it.
                    if CurrentVertexNormalMapName is not None:
                        if CurrentVertexNormalMapName != VNMapName:
                            try:
                                lx.eval('select.vertexMap "{%s}" norm replace' % CurrentVertexNormalMapName)
                                lx.eval('vertMap.name {%s} norm active' % VNMapName)
                                # lx.eval('!vertMap.delete norm')
                                # lx.eval('vertMap.new name:"Vertex Normal" type:norm init:false')
                            except:
                                pass
        # Create an empty VertexNormalMap if there is no Vertex Normals on Original HighPoly Mesh Source
        # if len(VertNrnMapList) == 0:
        #     lx.eval('vertMap.new name:{%s} type:norm init:false' % VNMapName)

        lx.eval('select.drop polygon')
        lx.eval('!select.deleteSet StarTriple_PolySelSet false')
        lx.eval('select.type edge')
        lx.eval('select.drop edge')
        lx.eval('select.type vertex')
        lx.eval('!select.deleteSet StarTriple_VertSelSet false')
        lx.eval('select.drop vertex')
        lx.eval('select.type polygon')

        if not RefSystemActive:
            lx.eval('item.refSystem {}')
        if RefSystemActive:
            lx.eval('item.refSystem %s' % CurrentRefSystemItem)

        # #################################
        # ## Solution B
        # if ACNone == True or ACLocal == False:
        #     lx.eval('tool.set actr.local off')
        #     lx.eval('tool.set axis.local off')
        #     # lx.eval('actionCenter.state enable:false')
        # ## Solution B
        # #################################


lx.bless(SMO_GC_StarTriple_Cmd, Cmd_Name)
