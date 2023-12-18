
# python
"""
Name:         SMO_UV_GetUVMapCountName_Cmd.py

Purpose:      This script is designed to
              Query UV Map count and name in all the scene and
              query UV Map count and name in selected meshes.

Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
Website:      https://www.linkedin.com/in/smoluck/
Created:      29/07/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.UV.GetUVMapCountName"
# smo.UV.GetUVMapCountName 0 1 1


class SMO_UV_GetUVMapCountName_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Check UV Map Scene Wise", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)                 # here the (0) define the argument index.
        self.dyna_Add("Check UV Map Only on Selected Mesh", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Set and Store Selected UV Map Name", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (2, lx.symbol.fCMDARG_OPTIONAL)
        self.dyna_Add("Clear Other Vmap Selection", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (3, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO UV - Get UVMap Count and Name'
    
    def cmd_Desc (self):
        return 'Query UV Map count and name in all the scene and query UV Map count and name in selected meshes.'
    
    def cmd_Tooltip (self):
        return 'Query UV Map count and name in all the scene and query UV Map count and name in selected meshes.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO UV - Get UVMap Count and Name'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        
        CheckUVMapSceneWise = self.dyna_Int (0)
        CheckUVMapOnlySelected = self.dyna_Int (1)
        SetSelectedUVMapName = self.dyna_Int (2)
        ClearOtherVmapSelection  = self.dyna_Int (3)
        
        if ClearOtherVmapSelection == 1:
            lx.eval('smo.GC.ClearSelectionVmap 2 1')
            lx.eval('smo.GC.ClearSelectionVmap 3 1')
            lx.eval('smo.GC.ClearSelectionVmap 4 1')
            lx.eval('smo.GC.ClearSelectionVmap 5 1')
            lx.eval('smo.GC.ClearSelectionVmap 6 1')
            lx.eval('smo.GC.ClearSelectionVmap 7 1')
        
        
        if CheckUVMapSceneWise == 1 :
            lx.out('----------------------------------')
            lx.out('UV Map Count and Name in all scene:')
            lx.out('----------------------------------')
            scnmeshitems = [item for item in scene.items() if item.type == 'mesh']
            for item in scnmeshitems:
                if item.geometry.vmaps.uvMaps:
                    UVMapsCount = len(item.geometry.vmaps.uvMaps)
                    lx.out('UV Map Count:', UVMapsCount)
                    for uvmap in item.geometry.vmaps.uvMaps:
                        lx.out('UV Map Name:', uvmap.name)
                    
        if CheckUVMapSceneWise == 1 and CheckUVMapOnlySelected == 1 :
            lx.out('-')
            lx.out('-')
            lx.out('-')
            
        if CheckUVMapOnlySelected == 1 :
            vmaps=set(lx.evalN('query layerservice vmaps ? selected'))
            texture=set(lx.evalN('query layerservice vmaps ? texture'))
            seltexture=list(vmaps.intersection(texture))
            if len(seltexture) == 0 :
                lx.out('NO UV Map Selected')
                lx.eval ('user.value SMO_UV_SelectedMeshUVmapCount 0')
            if len(seltexture) == 1 :
                lx.out('One UV Map Selected')
                lx.eval ('user.value SMO_UV_SelectedMeshUVmapCount 1')
            if len(seltexture) > 1 :
                lx.out('Multiple UV Map Selected')
                lx.eval ('user.value SMO_UV_SelectedMeshUVmapCount 2')
            
            
            lx.out('----------------------------------')
            lx.out('UV Map ID, Index, Total Count and Names in Selection:')
            lx.out('----------------------------------')
            selection = list(scene.selectedByType('mesh'))
            
            lx.out('UV Map ID:')
            UVmap_Selected = lx.evalN('query layerservice vmaps ? selected')
            lx.out('Selected UV Map ID:', UVmap_Selected)
            
            lx.out('-')
            lx.out('UV Map Index:')
            UVmap_SelectedN = len(lx.evalN('query layerservice vmaps ? selected'))
            lx.out('Selected UV Map Index:', UVmap_SelectedN)
            
            
            
            lx.out('-')
            lx.out('UV Map Count and Names:')
            for item in selection:
                if item.geometry.vmaps.uvMaps:
                    UVMapsTotalCount = len(item.geometry.vmaps.uvMaps)
                    lx.out('UV Map Total Count:', UVMapsTotalCount)
                    
                    for uvmap in item.geometry.vmaps.uvMaps:
                        lx.out('UV Map Names:', uvmap.name)
                        if UVMapsTotalCount == 1 :
                            lx.eval ('user.value SMO_UV_SelectedMeshUVmapName {%s}' % uvmap.name) 
            
            
            
            if len(seltexture) == 1 and SetSelectedUVMapName == 1 :
                lx.out('-')
                lx.out('Selected UV Map Name:')
                for item in selection:
                    if item.geometry.vmaps.uvMaps:
                        vmap_ids = lx.eval('query layerservice vmaps ? selected')
                        vmap_names = []
                        
                        for vmap_id in vmap_ids:
                            vmap_name = lx.eval('query layerservice vmap.name ? %s' % vmap_id)
                            vmap_names.append(vmap_name)
                            lx.out('Selected UV Map name:', vmap_name)
                            lx.eval ('user.value SMO_UV_SelectedMeshUVmapName {%s}' % vmap_name) 


lx.bless(SMO_UV_GetUVMapCountName_Cmd, Cmd_Name)
