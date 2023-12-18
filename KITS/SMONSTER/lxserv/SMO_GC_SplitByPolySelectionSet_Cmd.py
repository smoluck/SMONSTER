# python
"""
Name:         SMO_GC_SplitByPolySelectionSet_Cmd.py

Purpose:      This script is designed to:
              Split the current MeshLayer by reading the Polygon Selection Sets
              and using their names to split the mesh in multiple mesh Layers, with corresponding names.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      28/09/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.SplitByPolySelectionSet"
# smo.GC.SplitByPolySelectionSet


# Previous name of this command was "smo.GC.AffinitySVGRebuild" for cleaning up SVG data from Affinity Designer.
class SMO_GC_SplitByPolySelectionSet_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        try:
            self.current_Selection = lxu.select.ItemSelection().current()
        except:
            self.current_Selection = []

        # If we do have something selected, put it in self.current_Selection
        # Using [-1] will grab the newest item that was added to your selection.
        if len(self.current_Selection) > 0:
            self.current_Selection = self.current_Selection[-1]
        else:
            self.current_Selection = None

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Split by Poly Selection Set'

    def cmd_Desc(self):
        return 'Split the current MeshLayer by reading the Polygon Selection Sets and using their names to split the mesh in multiple mesh Layers, with corresponding names. Previous name of this command was "smo.GC.AffinitySVGRebuild" for cleaning up SVG data from Affinity Designer.'

    def cmd_Tooltip(self):
        return 'Split the current MeshLayer by reading the Polygon Selection Sets and using their names to split the mesh in multiple mesh Layers, with corresponding names. Previous name of this command was "smo.GC.AffinitySVGRebuild" for cleaning up SVG data from Affinity Designer.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Split by Poly Selection Set'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        if self.current_Selection is not None:
            scene = modo.scene.current()
            # Layer service
            layer_svc = lx.Service('layerservice')

            # MeshItem_List = scene.selected
            # MeshItem_List = scene.selectedByType(lx.symbol.sTYPE_MESH)
            # for mesh in MeshItem_List:
            #     mesh.select(True)

            TargetMesh = lx.eval('smo.GC.GetMeshUniqueName ?')
            lx.out('Current Mesh Unique name is ', TargetMesh)
            TargetName = lx.eval('item.name ? xfrmcore')
            lx.out('Current Mesh name is ', TargetName)

            # ---------------- COPY/PASTE Check Procedure ---------------- #
            ## create variables
            lx.eval("user.defNew name:User_Pref_CopyDeselectChangedState type:boolean life:momentary")
            lx.eval("user.defNew name:User_Pref_PasteSelectionChangedState type:boolean life:momentary")
            lx.eval("user.defNew name:User_Pref_PasteDeselectChangedState type:boolean life:momentary")

            lx.eval("user.defNew name:User_Pref_CopyDeselect type:boolean life:momentary")
            lx.eval("user.defNew name:User_Pref_PasteSelection type:boolean life:momentary")
            lx.eval("user.defNew name:User_Pref_PasteDeselect type:boolean life:momentary")
            ###################

            # Look at current Copy / Paste user Preferences:
            User_Pref_CopyDeselect = lx.eval('pref.value application.copyDeSelection ?')
            lx.out('User Pref: Deselect Elements after Copying', User_Pref_CopyDeselect)
            User_Pref_PasteSelection = lx.eval('pref.value application.pasteSelection ?')
            lx.out('User Pref: Select Pasted Elements', User_Pref_PasteSelection)
            User_Pref_PasteDeselect = lx.eval('pref.value application.pasteDeSelection ?')
            lx.out('User Pref: Deselect Elements Before Pasting', User_Pref_PasteDeselect)
            # Is Copy Deselect False ?
            if User_Pref_CopyDeselect == 0:
                lx.eval('pref.value application.copyDeSelection true')
                User_Pref_CopyDeselectChangedState = 1

            # Is Paste Selection False ?
            if User_Pref_PasteSelection == 0:
                lx.eval('pref.value application.pasteSelection true')
                User_Pref_PasteSelectionChangedState = 1

            # Is Paste Deselect False ?
            if User_Pref_PasteDeselect == 0:
                lx.eval('pref.value application.pasteDeSelection true')
                User_Pref_PasteDeselectChangedState = 1

            # Is Copy Deselect True ?
            if User_Pref_CopyDeselect == 1:
                User_Pref_CopyDeselectChangedState = 0

            # Is Paste Selection True ?
            if User_Pref_PasteSelection == 1:
                User_Pref_PasteSelectionChangedState = 0

            # Is Paste Deselect True ?
            if User_Pref_PasteDeselect == 1:
                User_Pref_PasteDeselectChangedState = 0
            # -------------------------------------------- #

            # Get the list of all Polygons Selection Sets using the SelSet ID count.
            selSets = []
            layer_svc.select('layer.id', 'main')
            PolySelSetCount = layer_svc.query('polset.N')
            lx.out('Range max: ', PolySelSetCount)
            for index in range(PolySelSetCount):
                layer_svc.select('polset.name', str(index))
                selSets.append(layer_svc.query('polset.name'))
            lx.out('selSet: ', selSets)

            # Delete the SVG data tag that is always present when files comes from Affinity Designer.
            if "Vectors" in selSets:
                lx.eval('select.type polygon')
                lx.eval('!select.deleteSet Vectors')
                lx.eval('select.type item')

            RangeClamp = PolySelSetCount - 1
            lx.out('Range clamp: ', RangeClamp)
            for i in range(PolySelSetCount):
                OutputLayerName = (TargetName + "_" + selSets[i])
                lx.out('Output Layer Name:', OutputLayerName)
                try:
                    scene.select(TargetMesh)
                    for mesh in scene.selectedByType("mesh")[:1]:
                        MeshPolyCount = len(mesh.geometry.vertices)
                        lx.out('In Selected items, Polygon count selected:', MeshPolyCount)
                    CurrentPolySelSetCount = layer_svc.query('polset.N')
                    lx.out('Polygon Selection Set Count:', CurrentPolySelSetCount)
                    lx.eval('select.drop polygon')
                    lx.eval('select.type item')
                    if MeshPolyCount >= 1:
                        lx.eval('select.drop item')
                        if MeshPolyCount >= 1 and CurrentPolySelSetCount >= 1:
                            lx.out('There is still polygons in Mesh source')
                            scene.select(TargetMesh)
                            lx.eval('select.type polygon')
                            # layer_svc.select('polset.name', str(index))
                            lx.eval('select.useSet {%s} select' % (selSets[i]))
                            lx.out('Target Selection Set name: ', (selSets[i]))
                            lx.eval('cut')
                            lx.eval('layer.new')
                            lx.eval('item.name {%s} xfrmcore' % OutputLayerName)
                            lx.eval('paste')
                            lx.eval('!select.deleteSet {%s}' % (selSets[i]))
                            lx.eval('select.type item')
                            lx.eval('select.drop item')
                        elif MeshPolyCount >= 1 or CurrentPolySelSetCount == 0:
                            lx.out('There is no more polygons in Mesh source')
                            scene.select(TargetMesh)
                            lx.eval('select.type polygon')
                            lx.eval('!!select.all')
                            lx.eval('select.editSet Target add')
                            lx.eval('select.drop polygon')
                            lx.eval('item.name Target xfrmcore')
                            lx.eval('select.drop item')
                    elif MeshPolyCount == 0 or CurrentPolySelSetCount == 0:
                        lx.out('There is no more polygons in Mesh source')
                        scene.select(TargetMesh)
                        lx.eval('item.name Target xfrmcore')
                        lx.eval('!delete')
                except:
                    pass
            del selSets[:]

            # -------------- COPY/PASTE END Procedure  -------------- #
            # Restore user Preferences:
            if User_Pref_CopyDeselectChangedState == 1:
                lx.eval('pref.value application.copyDeSelection false')
                lx.out('"Deselect Elements after Copying" have been Restored')
            if User_Pref_PasteSelectionChangedState == 1:
                lx.eval('pref.value application.pasteSelection false')
                lx.out('"Select Pasted Elements" have been Restored')
            if User_Pref_PasteDeselectChangedState == 1:
                lx.eval('pref.value application.pasteDeSelection false')
                lx.out('"Deselect Elements Before Pasting" have been Restored')
            # -------------------------------------------- #

            ''' Script with lx.Service
            # Layer service
            layer_svc = lx.Service('layerservice')

            selSets = []
            layer_svc.select('layer.id', 'main')
            num_polset = layer_svc.query('polset.N')
            for i in range(num_polset):
                layer_svc.select('polset.name', str(i))
                selSets.append(layer_svc.query('polset.name'))

            lx.out('selSet: ', selSets)
            '''

            ''' Script using API
            # scene service, reference of the scene and a channel read object
            scene_svc = lx.service.Scene()
            scene = lxu.select.SceneSelection().current()
            chan_read = scene.Channels(lx.symbol.s_ACTIONLAYER_EDIT, 0.0)

            # current selected items in scene
            selection = lxu.select.ItemSelection().current() 

            # Get a int ID for the item type.
            #type_mesh = scene_svc.ItemTypeLookup(lx.symbol.sITYPE_MESH) 
            type_mesh = lx.symbol.i_CIT_MESH 

            # Find the first meshItem in the selection
            for item in selection:
                if item.TestType(type_mesh):
                    meshItem = item
                    break
                else:
                    meshItem = None

            # Read the mesh channel from the item to get the mesh object
            mesh_obj = chan_read.ValueObj(meshItem ,meshItem.ChannelLookup(lx.symbol.sICHAN_MESH_MESH))
            mesh = lx.object.Mesh(mesh_obj) # mesh object

            # Get the selection sets from the mesh with PICK and save them into a list
            selSets = []
            num_polset = mesh.PTagCount(lx.symbol.i_PTAG_PICK)
            for i in range(num_polset):
                selSets.append(mesh.PTagByIndex(lx.symbol.i_PTAG_PICK, i))
            lx.out('selSets:', selSets)
            '''

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_SplitByPolySelectionSet_Cmd, Cmd_Name)

'''
class DetailSelSet:
    def __init__(self, Name, Count):
        self.Name = Name
        self.Count = Count


SelSetList = [DetailSelSet("Spine", 82),
              DetailSelSet("Belly", 68),
              DetailSelSet("Bones", 25)]


print(sum(i.Count >= 40 for i in SelSetList))

print(sum(i.Count < 30 for i in SelSetList))
'''