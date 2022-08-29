# python
# ---------------------------------------
# Name:         SMO_GC_Multi_SelectCoPlanarPoly_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to
#               (Replace the old Seneca Lazy Select by the Built in Select CoPlanar poly tool.)
#
#
# Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
# Website:      http://www.smoluck.com
#
# Created:      26/08/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.GC.Multi.SelectCoPlanarPoly"
# smo.GC.Multi.SelectCoPlanarPoly 0 20

class SMO_GC_Multi_SelectCoPlanarPoly_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Mode", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Angle", lx.symbol.sTYPE_INTEGER)
        self.dyna_Add("Range", lx.symbol.sTYPE_FLOAT)         # Set HardCoded to 10000 in order to not filter by distance when Mode is set to 2
        self.basic_SetFlags (2, lx.symbol.fCMDARG_OPTIONAL)

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))


    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - (Multi) Select CoPlanar Poly'

    def cmd_Desc(self):
        return 'MULTI - Replace the old Seneca Lazy Select by the Built in Select CoPlanar poly tool.'

    def cmd_Tooltip(self):
        return 'MULTI - Replace the old Seneca Lazy Select by the Built in Select CoPlanar poly tool.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - (Multi) Select CoPlanar Poly'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        #################################
        # <----[ DEFINE ARGUMENTS ]---->#
        #################################
        MODE = self.dyna_Int(0)         #  select = 0 (similarTouching)   ###   polygon(SimilarOnObject) = 1   ###   none = 2 (SimilarOnLayer)
        ANGLE = self.dyna_Int(1)  # in degree
        if self.dyna_IsSet(2) == False:
            RANGE = 10000.0
        else:
            RANGE = self.dyna_Float(2)  # in distance

        if self.dyna_Int(0) == 0:
            RANGE = 0.0

        # Expose the Result of the Arguments
        lx.out(MODE, ANGLE, RANGE)
        #################################
        # <----[ DEFINE ARGUMENTS ]---->#
        #################################

        scene = modo.scene.current()


        SelItem = lxu.select.ItemSelection().current()
        # print('lxu.object.Item : ', SelItem)

        mesh = scene.selectedByType('mesh')
        # print('modo.Mesh :', mesh)
        # print('modo.Mesh list length:', len(mesh))

        TargetIDList = []
        for item in mesh:
            itemType = modo.Item(item).type
            item = lx.object.Item(item)
            # print(item)
            if itemType == "mesh":
                ID = item.Ident()
                # print(ID)
                TargetIDList.append(ID)
        # print(TargetIDList)

        PolysTuple = []
        for item in mesh:
            # CsPolys = len(item.geometry.polygons.selected)
            # print('Total selected Polygons on this mesh layer', CsPolys)
            Polys = item.geometry.polygons.selected
            # print('modo.Mesh list ', Polys)
            PolysTuple.append(Polys)
        # print('Tuple (Poly ID and Mesh ID): ---)', PolysTuple)

        PolysList = list(PolysTuple)
        # print('List (Poly ID and Mesh ID): ---)', PolysList)
        # print(PolysList)
        # print('------------------')
        # print(PolysList[0])
        # print('------')
        # print(PolysList[1])
        # print('------')
        # print(PolysList[2])
        # print('------')
        # print(PolysList[3])
        # print('------')

        lx.eval('select.drop polygon')
        lx.eval('smo.GC.DeselectAll')
        lx.eval('select.type item')
        lx.eval('smo.GC.DeselectAll')

        CoplanarSelPolyTuple = []
        index = -1
        for m in TargetIDList:
            index = (index + 1)
            # print('id :', index)
            scene.select(m)
            selected_mesh = scene.selectedByType('mesh')[0]
            # print('current mesh indentity :', index, selected_mesh)
            lx.eval('select.type polygon')
            lx.eval('select.drop polygon')
            for item in (PolysList[index]):
                # print(item)
                selected_mesh.geometry.polygons.select(item)
                ############### PUT YOUR Command HERE to run over each item Polygons
                try:
                    lx.eval('smo.GC.SelectCoPlanarPoly %s %s %s' % (MODE, ANGLE, RANGE))
                except:
                    lx.out('Error on {%s}' % (lx.eval('item.name ? xfrmcore')))
                CoplanarPolys = selected_mesh.geometry.polygons.selected
                # print('modo.Mesh list ', Polys)
                CoplanarSelPolyTuple.append(CoplanarPolys)
            lx.eval('select.type item')
            lx.eval('select.drop item')
            # GOOOOOOOOOOOOD

        CoplanarSelPolyList = list(CoplanarSelPolyTuple)
        lx.eval('smo.GC.DeselectAll')
        scene.select(mesh)
        lx.eval('select.type polygon')

        # select back the Polygons
        lx.eval('smo.GC.DeselectAll')
        scene.select(mesh)
        lx.eval('select.type polygon')


        for item in (CoplanarSelPolyList):
            # print(item)
            selected_mesh.geometry.polygons.select(item)

        del index
        del TargetIDList
        del PolysList
        del PolysTuple
        del CoplanarSelPolyTuple
        del CoplanarSelPolyList
        lx.eval('select.type polygon')


lx.bless(SMO_GC_Multi_SelectCoPlanarPoly_Cmd, Cmd_Name)
