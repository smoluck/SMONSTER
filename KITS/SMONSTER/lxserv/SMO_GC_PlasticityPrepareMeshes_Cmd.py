# python
# ---------------------------------------
# Name:         SMO_GC_PlasticityPrepareMeshes_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Cleanup Meshes data from Plasticity creating Polygons Parts, Unwraped UVMaps and Merging Solid items.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      04/12/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo
from math import degrees

Cmd_Name = "smo.GC.PlasticityPrepareMeshes"
# smo.GC.PlasticityPrepareMeshes 0 1 1 1 0

class SMO_GC_PlasticityPrepareMeshes_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Convert Scale", lx.symbol.sTYPE_BOOLEAN)
        # self.basic_SetFlags(0, lx.symbol.fCMDARG_OPTIONAL)  # here the (0) define the argument index.
        self.dyna_Add("Create Part Tags", lx.symbol.sTYPE_BOOLEAN)
        # self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Create UV Maps and Unwrap", lx.symbol.sTYPE_BOOLEAN)
        # self.basic_SetFlags(2, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Output Airtight Meshes", lx.symbol.sTYPE_BOOLEAN)
        # self.basic_SetFlags(3, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Repack All Meshes together", lx.symbol.sTYPE_BOOLEAN)
        # self.basic_SetFlags(4, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Unparent in place", lx.symbol.sTYPE_BOOLEAN)
        # self.basic_SetFlags(5, lx.symbol.fCMDARG_OPTIONAL)

        # self.SelModeVert = bool(lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"))
        # self.SelModeEdge = bool(lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"))
        # self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))
        # self.SelModeItem = bool(lx.eval1("select.typeFrom typelist:item;pivot;center;edge;polygon;vertex;ptag ?"))
        # print(self.SelModeVert)
        # print(self.SelModeEdge)
        # print(self.SelModePoly)
        # print(self.SelModeItem)
        # if self.SelModePoly == True or self.SelModeItem == True:
            # try:
                # self.TargetMeshList = lxu.select.ItemSelection().current()
            # except:
                # self.TargetMeshList = []

            # # If we do have something selected, put it in self.TargetMeshList
            # if len(self.TargetMeshList) > 0:
                # self.TargetMeshList = self.TargetMeshList
            # else:
                # self.TargetMeshList = None
            # # print(self.TargetMeshList)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Plasticity Prepare Meshes'

    def cmd_Desc(self):
        return 'Cleanup Meshes data from Plasticity creating Polygons Parts, Unwraped UVMaps and Merging Solid items.'

    def cmd_Tooltip(self):
        return 'Cleanup Meshes data from Plasticity creating Polygons Parts, Unwraped UVMaps and Merging Solid items.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Plasticity Prepare Meshes'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        treated_meshes_list = []
        NewNameList = []
        GrpNewNameList = []

        ConvertScale = self.dyna_Bool (0)
        CreatePartTags = self.dyna_Bool (1)
        UVUnwrap = self.dyna_Bool (2)
        Airtight = self.dyna_Bool (3)
        RepackAll = self.dyna_Bool (4)
        UnparentInPlace = self.dyna_Bool (5)

        ### Part toggle
        PolygonTagTypeMode = lx.eval('select.ptagType ?')
        # print(PolygonTagTypeMode)

        if PolygonTagTypeMode != "part":
            lx.eval('select.ptagType part')
            PTTMdiff = True

        if PolygonTagTypeMode != "material":
            PTTMdiff = False
        ###


        ### Delete  Empty Meshes maybe not needed in SMO Batch context
        lx.eval('smo.CLEANUP.DelEmptyMeshItem')
        lx.eval('select.itemType mesh')
        meshes_list = scene.selectedByType(lx.symbol.sITYPE_MESH)
        # print(meshes_list)

        if ConvertScale == True:
            u_def = lx.eval("pref.value units.default ?")
            # print(u_def)
            if u_def == "meters":
                ### Scale down from meter to centimeter
                lx.eval('transform.channel scl.X 0.001')
                lx.eval('transform.channel scl.Y 0.001')
                lx.eval('transform.channel scl.Z 0.001')
                lx.eval('transform.freeze scale')

            if u_def == "millimeters":
                ### Scale down from centimeter to millimeters
                lx.eval('transform.channel scl.X 10')
                lx.eval('transform.channel scl.Y 10')
                lx.eval('transform.channel scl.Z 10')
                lx.eval('transform.freeze scale')


        #secondmeshes_list = scene.selected
        #meshes_list.append(secondmeshes_list)

        ### Grouping and Separate meshes parts
        for mesh in meshes_list:
            mesh.select(True)
            TargetItem = lx.eval1("query sceneservice selection ? locator")
            Mesh_Target = scene.selectedByType('mesh')[0]
            TargetNamePrefix = Mesh_Target.name
            # print(TargetNamePrefix)
            NewName = TargetNamePrefix + '_' + "part"
            GrpNewName = "Grp"+ '_' + TargetNamePrefix
            GrpNewNameList.append(GrpNewName)

            if UnparentInPlace == True:
                lx.eval('item.parent parent:{} inPlace:1')
            lx.eval('layer.groupSelected')
            lx.eval('item.name %s xfrmcore' % GrpNewName)
            lx.eval('select.editSet %s add' % GrpNewName)
            lx.eval('select.itemHierarchy')
            lx.eval('smo.GC.DeselectAll')

            scene.select(Mesh_Target)
            lx.eval('layer.unmergeMeshes')
            lx.eval('smo.GC.DeselectAll')
            lx.eval('select.useSet %s select' % GrpNewName)
            lx.eval('select.itemHierarchy')
            lx.eval('select.useSet %s deselect' % GrpNewName)
            if CreatePartTags == True:
                lx.eval('item.name %s xfrmcore' % NewName)
                lx.eval('select.editSet %s add' % NewName)
                NewNameList.append(NewName)
            if CreatePartTags == False:
                lx.eval('item.name %s xfrmcore' % TargetNamePrefix)
                lx.eval('select.editSet %s add' % TargetNamePrefix)
                NewNameList.append(TargetNamePrefix)
            lx.eval('smo.GC.DeselectAll')


        ### Rename Items 
        print(NewNameList)
        print(GrpNewNameList)

        if CreatePartTags == True:
            ### Set Parts to each Meshes using their name
            for item in GrpNewNameList:
                PartTargetsList = []
                lx.eval('select.useSet %s select' % item)
                lx.eval('select.itemHierarchy')
                lx.eval('select.useSet %s deselect' % item)
                PartTargetsList = scene.selected
                for mesh in PartTargetsList:
                    mesh.select(True)
                    PartMesh = scene.selectedByType('mesh')[0]
                    PartName = PartMesh.name
                    lx.eval('poly.setPart %s' % PartName)
                del PartTargetsList[:]
                lx.eval('smo.GC.DeselectAll')


        ### MergeBack the meshes
        for item in GrpNewNameList:
            lx.eval('select.useSet %s select' % item)
            lx.eval('select.itemHierarchy')
            lx.eval('select.useSet %s deselect' % item)
            lx.eval('layer.mergeMeshes false')
            lx.eval('smo.GC.DeselectAll')


        ### Delete the Groups locator and update the Lists
        lx.eval('select.itemType mesh')
        resultingmesh_list = scene.selectedByType(lx.symbol.sITYPE_MESH)
        lx.eval('item.parent parent:{} inPlace:1')
        lx.eval('smo.GC.DeselectAll')

        for item in GrpNewNameList:
            lx.eval('select.useSet %s select' % item)
            lx.eval('!delete')
            lx.eval('smo.GC.DeselectAll')

        # remove Selection Sets
        lx.eval('select.deleteSet %s true' % GrpNewNameList[0] )

            

        if PTTMdiff == True:
            lx.eval('select.ptagType %s' % PolygonTagTypeMode)


        ### Generate UV maps and Create Airtight Mesh by merging Vertex Boundary
        UVMapName = lx.eval('pref.value application.defaultTexture ?')
        scene.select(resultingmesh_list)
        lx.eval('vertMap.new {%s} txuv' % UVMapName)
        for mesh in resultingmesh_list:
            mesh.select(True)

            if UVUnwrap == True:
                # Unwrap and Pack UV Islands
                lx.eval('select.type polygon')
                lx.eval('select.all')
                lx.eval('smo.UV.Multi.UnwrapSmart 0 1 0 0')
                lx.eval('smo.UV.SmartProjectionClearTag')

            if Airtight == True:
                # Merge Vertex Boundary
                lx.eval('@AddBoundary.py')
                lx.eval('item.componentMode vertex true')
                lx.eval('!vert.merge fixed false 0.00001 false false')
            lx.eval('select.type item')
            lx.eval('smo.GC.DeselectAll')

        if RepackAll == True and UVUnwrap == True:
            scene.select(resultingmesh_list)
            lx.eval('smo.UV.NormalizePack 0 0')

        # Mesh Cleanup passes
        scene.select(resultingmesh_list)
        lx.eval('!mesh.cleanup true mergeVertex:false')

        # lx.eval('smo.UV.EnableUVTextureChecker 4096')


lx.bless(SMO_GC_PlasticityPrepareMeshes_Cmd, Cmd_Name)
