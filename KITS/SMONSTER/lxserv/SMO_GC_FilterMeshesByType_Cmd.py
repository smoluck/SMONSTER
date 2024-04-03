# python
"""
Name:         SMO_GC_FilterMeshesByType_Cmd.py

Purpose:      This script is designed to:
              Select Regular Meshes or Procedural Meshes (Mesh Items that does or doesn't have Meshops attached to them, and that can be edited directly)

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      01/04/2024
Copyright:    (c) Franck Elisabeth 2017-2024
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.FilterMeshesByType"
# smo.GC.FilterMeshesByType 1 0 ------ > Select Regular Meshes (scenewise)
# smo.GC.FilterMeshesByType 1 1 ------ > Select Procedural Meshes (scenewise)


class SMO_GC_FilterMeshesByTpe_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Select SceneWise", lx.symbol.sTYPE_BOOLEAN)
        self.dyna_Add("Mesh Items Type", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(1, lx.symbol.fCMDARG_OPTIONAL)             # here the (0) define the argument index.
        
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return "SMO GC - Select Meshes by Type"
    
    def cmd_Desc (self):
        return "Select DirectModeling Meshes or Procedural Meshes (Mesh Items that does or doesn't have Meshops attached to them, and that can be edited directly)"
    
    def cmd_Tooltip (self):
        return "Select DirectModeling Meshes or Procedural Meshes (Mesh Items that does or doesn't have Meshops attached to them, and that can be edited directly)"
    
    def cmd_Help (self):
        return "https://twitter.com/sm0luck"
    
    def basic_ButtonName (self):
        return "SMO GC - Select Meshes by Type"
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.Scene()
        Mode = self.dyna_Bool(0)
        MIT = self.dyna_Int(1)

        def is_mesh_procedural(item):
            """
            # Alternative, check the supertype of the current modifier
            if conn.superType == 'meshoperation' or conn.superType == 'tooloperation':
                is_procedural == True
            """
            if item.type == "mesh":
                if len(item.itemGraphs) > 0:
                    if "deformers" in item.itemGraphNames:
                        graph = item.itemGraph("deformers")
                        # graph.connectedItems
                        for conn in graph.reverse():
                            if len(conn.channels("meshOpObj")) > 0:
                                # print "Found 'meshOpObj' channel for %s. This mesh is procedural." % conn.name
                                return True
            return False

        def select_by_type_in_scene(MeItType):
            lx.eval("select.type item")
            lx.eval("select.drop item")
            lx.eval("select.itemType mesh")
            source = scene.selectedByType('mesh', superType=False)
            list_targetmesh = []
            for item in source:
                if MeItType == 0:
                    if is_mesh_procedural(item):
                        list_targetmesh.append(item)
                if MeItType == 1:
                    if not is_mesh_procedural(item):
                        list_targetmesh.append(item)
            lx.eval("select.drop item")
            scene.select(list_targetmesh)
            del list_targetmesh

        def select_by_type_in_selection(MeItType):
            source = scene.selectedByType('mesh', superType=False)
            list_targetmesh = []
            for item in source:
                if MeItType == 0:
                    if is_mesh_procedural(item):
                        list_targetmesh.append(item)
                if MeItType == 1:
                    if not is_mesh_procedural(item):
                        list_targetmesh.append(item)
            lx.eval("select.drop item")
            scene.select(list_targetmesh)
            del list_targetmesh

        if Mode:
            select_by_type_in_scene(MIT)
        else:
            select_by_type_in_selection(MIT)

    
    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_FilterMeshesByTpe_Cmd, Cmd_Name)
