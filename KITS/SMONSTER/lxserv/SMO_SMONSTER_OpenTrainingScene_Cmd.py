#python
#---------------------------------------
# Name:         SMO_SMONSTER_OpenTrainingScene_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to:
#               Open the Training Scene using an ID integer as argument
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      14/08/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Command_Name = "smo.SMONSTER.OpenTrainingScene"
# smo.SMONSTER.OpenTrainingScene 1

class SMO_SMONSTER_OpenTrainingScene_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Scene ID", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)             # here the (1) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'Open Training Scene'
    
    def cmd_Desc (self):
        return 'Open the Training Scene using an ID integer as argument.'
    
    def cmd_Tooltip (self):
        return 'Open the Training Scene using an ID integer as argument.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'Open Training Scene'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
    
    
    def basic_Execute(self, msg, flags):
        args = lx.args()
        lx.out(args)
        SCENE_ID = self.dyna_Int (0)
        
        
        
        if SCENE_ID == 0 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_CAD_TOOLS/Rebevel_Demo_Startup.lxo}")
            
        if SCENE_ID == 1 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_CAD_TOOLS/TriangulatedRingToQuad.lxo}")

        if SCENE_ID == 2:
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_CAD_TOOLS/SMO_CAD_RebuildRadialFlat.lxo}")
            


        if SCENE_ID == 10 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_CLEANUP/CLEANUP_3DSMAX_FBX_Cleanup.lxo}")

        if SCENE_ID == 11:
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_CLEANUP/CLEANUP_UniformizeIndexStyle_Cleanup.lxo}")

        if SCENE_ID == 12:
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_CLEANUP/CLEANUP_RenameUVMapToDefaultSceneWise.lxo}")


            
        if SCENE_ID == 20 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_GAME_CONTENT/ExportAsFBXSequence_Metal_Beam.lxo}")
            
        if SCENE_ID == 21 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_GAME_CONTENT/ExportAsFBXSequence_QuadRemeshMeshFusion.lxo}")
            
        if SCENE_ID == 22 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_GAME_CONTENT/ExportAsFBXSequence_QuadRemeshMeshFusionResult.lxo}")
            
        if SCENE_ID == 23 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_GAME_CONTENT/ExportAsFBXSequencePY_MeshOpAnimatedMesh.lxo}")
            
        if SCENE_ID == 24 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_GAME_CONTENT/Modeling_HardEdgeWeight.lxo}")
            
        if SCENE_ID == 25 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_GAME_CONTENT/SMO_MES_MF_MatTag_and_SelSetPolyTag_byItemName.lxo}")

        if SCENE_ID == 26 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_GAME_CONTENT/SMO_GC_Setup_OffsetCenterPosPreserveInstancesPos.lxo}")

        if SCENE_ID == 27:
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_GAME_CONTENT/SMO_GC_SetSmartMaterial.lxo}")

        if SCENE_ID == 28 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_GAME_CONTENT/SMO_GC_EdgeBoundaryProjectNFuse.lxo}")

        if SCENE_ID == 29 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_GAME_CONTENT/SMO_GC_TransferVertexNormalFromPolygonUnderMouse.lxo}")

        if SCENE_ID == 30 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_MARMOSET_TOOLBAG_LIVELINK/SMO_MARMOSET_TOOLBAG_LIVELINK_Send.lxo}")
            
            
            
        if SCENE_ID == 40 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_MESHOPS/DemoScene_SMO_2D_PROFILE_TP_GEO.lxo}")
            
        if SCENE_ID == 41 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_MESHOPS/DemoScene_SMO_ARC.lxo}")
            
        if SCENE_ID == 42 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_MESHOPS/DemoScene_SMO_MERGEMESH_RESET.lxo}")
            
        if SCENE_ID == 43 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_MESHOPS/DemoScene_SMO_POLYFUSE_2D.lxo}")
            
            
            
        if SCENE_ID == 50 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_MIFABOMA/SMO_MIFABOMA__Bools.lxo}")
            
        if SCENE_ID == 51 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_MIFABOMA/SMO_MIFABOMA__FallOff.lxo}")
            
        if SCENE_ID == 52 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_MIFABOMA/SMO_MIFABOMA__Match.lxo}")
            
        if SCENE_ID == 53 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_MIFABOMA/SMO_MIFAMOBA__FlipOnAxis_Slice.lxo}")
            
        if SCENE_ID == 54 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_MIFABOMA/SMO_MIFAMOBA__Mirror.lxo}")
            
        if SCENE_ID == 55 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_MIFABOMA/SMO_MIFAMOBA__RadialArray.lxo}")
            
        if SCENE_ID == 56 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_MIFABOMA/SMO_MIFAMOBA__RadialSweep.lxo}")
            
            
            
        if SCENE_ID == 60 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_PIXAFLUX_LIVELINK/PixaFlux_LiveLink_Demo.lxo}")
            
            
            
        if SCENE_ID == 70 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_QUICK_TAG/ColorID.lxo}")
            
        if SCENE_ID == 71 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_QUICK_TAG/Demo.lxo}")

        if SCENE_ID == 72 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_QUICK_TAG/ColorID_Empty.lxo}")
            
            
            
        if SCENE_ID == 80 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_RIZOMUV_LIVELINK/TestScene.lxo}")
            
            
            
            
        if SCENE_ID == 90 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_UV/UV_Tools_AutoHide_Repack_Relax.lxo}")
            
        if SCENE_ID == 91 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_UV/UV_Tools_Cylindrical_AutoHide_Repack_Relax.lxo}")
            
        if SCENE_ID == 92 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_UV/UV_Tools_Done.lxo}")
            
        if SCENE_ID == 93 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_UV/UV_Tools_Empty.lxo}")
            
        if SCENE_ID == 94 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_UV/UV_Tools_PackAllArea.lxo}")
            
        if SCENE_ID == 95 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_UV/UV_Tools_PackAllUDIM.lxo}")
            
        if SCENE_ID == 96 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_UV/UV_Tools_PlanarY.lxo}")
            
        if SCENE_ID == 97 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_UV/UV_Tools_Result.lxo}")
            
        if SCENE_ID == 98 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_UV/UV_Tools_Unwraped.lxo}")

        if SCENE_ID == 99 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_UV/UV_Tools_AutoExpand_MicroBevelWorkflow.lxo}")
            
            
            
        if SCENE_ID == 110 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_COLOR_BAR/COLOR_BAR.lxo}")


            
        if SCENE_ID == 120 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_VENOM/VeNom_SampleScene.lxo}")


            
        if SCENE_ID == 130 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_GAME_CONTENT/GC_Unbevel_Startup.lxo}")

        if SCENE_ID == 131:
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_GAME_CONTENT/SMO_GC_UDIMtoMaterial.lxo}")

        if SCENE_ID == 132:
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_GAME_CONTENT/SMO_GC_SplitMeshByUDIM.lxo}")



            
        if SCENE_ID == 140 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_BAKE/SMO_BAKE_SetBakePairs.lxo}")

        if SCENE_ID == 141 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_BAKE/SMO_BAKE_CheckAndFixCAGEMorphMaps.lxo}")

        if SCENE_ID == 142 :
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_BAKE/SMO_BAKE_PreviewCageMeshData.lxo}")

        if SCENE_ID == 143:
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_BAKE/SMO_BAKE_FreezeSubdivAndPsubdivPolysOnHighpoly.lxo}")

        if SCENE_ID == 144:
            filePathToOpen = lx.eval("query platformservice alias ? {kit_SMONSTER:TRAINING_SCENES/SMO_BAKE/SMO_BAKE_QuickExport.lxo}")


            
            
        # Open scene file
        lx.eval('scene.open {%s}' % filePathToOpen)
        lx.eval('viewport.fit')
        
lx.bless(SMO_SMONSTER_OpenTrainingScene_Cmd, Command_Name)
