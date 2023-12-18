# python
"""
Name:         SMO_GC_CreateCAGEDataGroup_Cmd.py

Purpose:      This script is designed to:
              Select the Tagged LowPoly Meshes and create A new CAGE Data
              group out of their current Cage Morph map.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      30/11/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.CreateCloneCAGEData"
# smo.GC.CreateCloneCAGEData


class SMO_GC_CreateCAGEDataGroup_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Create CAGE Data Group.'
    
    def cmd_Desc (self):
        return 'Select the Tagged LowPoly Meshes and create A new CAGE Data group out of their current Cage Morph map.'
    
    def cmd_Tooltip (self):
        return 'Select the Tagged LowPoly Meshes and create A new CAGE Data group out of their current Cage Morph map.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Create CAGE Data Group.'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()

        # Create Selection sets based on Mesh MTyp Tags
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 1')
        # Select LowPoly meshes via Tags
        lx.eval('smo.GC.SelectMTypMesh 0')

        lx.eval('smo.GC.ClearSelectionVmap 0 1')

        # Create Cage meshes
        lx.eval('smo.GC.DuplicateToCageAndRename')

        # Clear items selection and select Cage back
        lx.eval('select.drop item')

        # CLear Selection Set based on Mesh MTyp Tags
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 0')
        # Create Selection Set based on Mesh MTyp Tags
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 1')

        # Select Cage meshes via Tags
        lx.eval('smo.GC.SelectMTypMesh 1')

        selitems = len(lx.evalN('query sceneservice selection ? mesh'))
        # lx.out('selitems',selitems)

        if selitems >= 1:
            ##### Morph Map Detection #####

            # Define the UV Seam vmap name Search case.
            lx.eval("user.defNew name:DesiredMorphmapName type:string life:momentary")
            DesiredMorphmapName = 'CAGE'

            # Define the UV Seam vmap name Search case.
            lx.eval("user.defNew name:NoMorphMap type:string life:momentary")
            NoMorphMap = '_____n_o_n_e_____'

            # Select Morph maps
            lx.eval('smo.GC.ClearSelectionVmap 3 0')
            # Get the number of Morph map available on mesh ////// DOESN'T WORK /////////
            # DetectedMorphmapCount = len(lx.evalN('vertMap.list morf ?'))
            # lx.out('Morph Map Count:', DetectedMorphmapCount)
            # Get the name of UV Seam map available on mesh
            # DetectedMorphmapName = lx.eval('vertMap.list all ?')
            # lx.out('Morph Map Name:', DetectedMorphmapName)
            # ##### Morph Map Detection #####

            selection = list(scene.selectedByType('mesh'))
            # meshitems = scene.selected
            # lx.out(items)

            for item in selection:
                if item.geometry.vmaps.morphMaps:
                    MorphmapCount = len(item.geometry.vmaps.morphMaps)
                    # lx.out('Morph Count:', MorphmapCount)
                    for morphMaps in item.geometry.vmaps.morphMaps:
                        # lx.out('Morph Count:', morphMaps.name)
                        pass
            ### Select CAGE Map if Detected
            if MorphmapCount >= 1 and morphMaps.name == "CAGE":
                lx.eval('smo.GC.ClearSelectionVmap 3 1')
                lx.eval('select.vertexMap CAGE morf replace')

        # CLear Selection Set based on Mesh MTyp Tags
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 0')
        # Create Selection Set based on Mesh MTyp Tags
        lx.eval('smo.GC.CreateDeleteSelSetFromMTypTag 1')

        # Select Cage meshes via Tags
        lx.eval('smo.GC.SelectMTypMesh 1')
        # Create Morph Influence
        lx.eval('item.addDeformer morphDeform true')
        ### Freeze CAGE Deformer
        lx.eval('deformer.freeze false')

        # Select Cage meshes via Tags and Ungroup them to Scene Root. Put them in a new Cage Grp
        lx.eval('smo.GC.SelectMTypMesh 1')
        CageItems = lx.evalN('query sceneservice selection ? mesh')
        CageItemsCount = len(lx.evalN('query sceneservice selection ? mesh'))
        print(CageItems)
        print(CageItemsCount)
        lx.eval('smo.GC.DeselectAll')
        # lx.out('selitems',selitems)
        # Unparent in Place And Group them back into the Cage Group locator / Rename it to CAGE / Turn it to Yellow Color. Lastly it will delete the Cage MorphMap Data in those Cage Mesh.
        for i in range(CageItemsCount):
            lx.eval('select.subItem %s add mesh 0 0' % CageItems[i])
        try:
            lx.eval('!item.parent parent:{} inPlace:1')
        except:
            pass
        lx.eval('smo.GC.DeselectAll')

        for i in range(CageItemsCount):
            lx.eval('select.subItem %s add mesh 0 0' % CageItems[i])
        lx.eval('layer.groupSelected')
        lx.eval('item.name cage xfrmcore')
        lx.eval('select.editSet MTyp_Cage add')
        lx.eval('smo.CB.ItemColor 7 0')
        lx.eval('select.itemHierarchy')
        lx.eval('smo.CB.ItemColor 7 1')
        lx.eval('select.drop item')
        lx.eval('smo.GC.SelectMTypMesh 1')
        lx.eval('!!vertMap.delete CAGE')
        lx.eval('select.drop item')


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_CreateCAGEDataGroup_Cmd, Cmd_Name)
