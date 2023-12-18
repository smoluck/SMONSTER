# python
"""
Name:         SMO_UV_RelaxUV_Cmd.py

Purpose:      This script is designed to
              Relax the UV's of the current Polygon Selection

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      10/10/2019
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import sys

Cmd_Name = "smo.UV.Relax"
#smo.UV.Relax 256


class SMO_UV_RelaxUV_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Relax Iteration Count", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)				# here the (0) define the argument index.
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO UV - Relax'
    
    def cmd_Desc (self):
        return 'Relax the UVs of the current Polygon Selection.'
    
    def cmd_Tooltip (self):
        return 'Relax the UVs of the current Polygon Selection.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO UV - Relax'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        # Force to select the current Mesh Item if it is not selected in the Item List
        lx.eval('smo.MASTER.ForceSelectMeshItemOnly')
        
        IntRelaxCount = self.dyna_Int (0)
        
        
        # ------------- ARGUMENTS ------------- #
        args = lx.args()
        lx.out(args)
        
        # Conformal= 0
        # Angle Based = 1
        RelaxUV_Iter = IntRelaxCount
        lx.out('Relax UV iteration Count: %s' % RelaxUV_Iter)
        # ------------- ARGUMENTS ------------- #

        
        
        
        
        # ------------- UV SEAM Map Detection
        # MODO version checks.
        # Modo 13.0 and up have UV Seam map.
        # Version below 13.0 haven't
        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        lx.out('Modo Version:',Modo_ver)
        # ------------- UV SEAM Map Detection
        
        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        # ---------------- Define user value for all the different SafetyCheck --- START
        #####
        lx.eval("user.defNew name:UVConstraints type:string life:momentary")
        lx.eval("user.defNew name:ReplaceUVSeamFailed type:string life:momentary")
        ## Selected UVmap Count
        lx.eval("user.defNew name:SMO_SafetyCheckUVRelax_UVMapCount type:boolean life:momentary")
        ## Selected UVmap Name
        lx.eval("user.defNew name:UVRelax_UVMapName type:string life:momentary")
        #####
        # ---------------- Define user value for all the different SafetyCheck --- END

        
        
        lx.eval('smo.GC.ClearSelectionVmap 2 1')
        lx.eval('smo.GC.ClearSelectionVmap 3 1')
        lx.eval('smo.GC.ClearSelectionVmap 4 1')
        lx.eval('smo.GC.ClearSelectionVmap 5 1')
        lx.eval('smo.GC.ClearSelectionVmap 6 1')
        lx.eval('smo.GC.ClearSelectionVmap 7 1')
        lx.eval('smo.GC.ClearSelectionVmap 8 1')
        


        # ----------------------------------------- #
        # <---( SAFETY CHECK 1 )---> UVMap Selected #
        # ----------------------------------------- #
        lx.out('<------------- START -------------->')
        lx.out('<--- UV Map Safety Check --->')

        # Get info about the selected UVMap.
        lx.eval('smo.UV.GetUVMapCountName 0 1 1')
        SelectedMeshUVMapsCount = lx.eval('user.value SMO_UV_SelectedMeshUVmapCount ?')
        lx.out('Selected Mesh UV Maps Count:',SelectedMeshUVMapsCount)
        UVRelax_UVMapName = lx.eval('user.value SMO_UV_SelectedMeshUVmapName ?')
        lx.out('Selected Mesh UV Maps Name:',UVRelax_UVMapName)
        
        lx.eval('smo.GC.ClearSelectionVmap 1 1')
        lx.eval('select.vertexMap %s txuv replace' % UVRelax_UVMapName)
        
        if SelectedMeshUVMapsCount > 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - Relax UVs:}')
            lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
            lx.eval('dialog.open')
            SMO_SafetyCheckUVRelax_UVMapCount = False
            sys.exit()

        
        if SelectedMeshUVMapsCount < 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - Relax UVs:}')
            lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
            lx.eval('dialog.open')
            SMO_SafetyCheckUVRelax_UVMapCount = False
            sys.exit()

        
        if SelectedMeshUVMapsCount == 1:
            SMO_SafetyCheckUVRelax_UVMapCount = True
            
        # UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' %UVmap_Selected)
        # lx.out('USER UV Map Name:', UserUVMapName)
        lx.out('<- UV Map Safety Check ->')
        lx.out('<------------- END -------------->')
        ###############################################
        
        
        ReplaceUVSeamFailed = 0
        UVConstraints = 'UV Constraints'
        
        lx.eval('tool.set uv.relax on')
        lx.eval('tool.noChange')
        
        lx.eval('tool.attr uv.relax mode lscm')
        lx.eval('tool.attr uv.relax live false')
        # lx.eval('tool.attr uv.relax live true')
        lx.eval('tool.attr uv.relax iter %s' % RelaxUV_Iter)
        lx.eval('tool.attr uv.relax boundary smooth')
        
        lx.eval('tool.doApply')
        lx.eval('select.nextMode')
        # lx.eval('!vertMap.deleteByName pick "UV Constraints"')
        
        
        
        
        # Get the number of UV Seam map available on mesh
        DetectedVMapPickCount = len(lx.evalN('vertMap.list pick ?'))
        lx.out('Vmap Pick Count:', DetectedVMapPickCount)
        # Get the name of UV Seam map available on mesh
        DetectedVMapPickName = lx.eval('vertMap.list pick ?')
        lx.out('Vmap Pick Name:', DetectedVMapPickName)
        # ------------- UV SEAM Map Detection
        ## UV Constraint Map Selection Check To bugfix the UV Constraint VMap creation ##
        lx.out('<--- UV Constraint Map Safety Check --->')
        lx.out('<---------- START ---------->')
        if Modo_ver <= 1399:
            if DetectedVMapPickCount >= 1 and DetectedVMapPickName == UVConstraints:
                lx.out('UV Constraints junk map detected')
                lx.eval('!vertMap.deleteByName pick "UV Constraints"')
                if Modo_ver >= 1300:
                    try:
                        lx.eval('!select.vertexMap "UV Seam" seam replace')
                    except:
                        ReplaceUVSeamFailed = 1
                        # lx.out('UV Seam map NOT detected')
                    if ReplaceUVSeamFailed == 1:
                        lx.eval('smo.UV.UpdateUVSeamCutMap')
                        lx.eval('select.type polygon')
            elif DetectedVMapPickCount <= 0 and DetectedVMapPickName != UVConstraints:
                lx.out('UV Constraints junk map NOT detected')
        
    
lx.bless(SMO_UV_RelaxUV_Cmd, Cmd_Name)
