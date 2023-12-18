# python
"""
Name:         SMO_UV_UVNormalizePackApplyTD_Cmd.py

Purpose:      This script is designed to
              UVNormalize Pack and Apply Texel Density on the current UVMap

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      28/12/2018
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.UV.UVNormalizePackApplyTD"
# smo.UV.UVNormalizePackApplyTD


class SMO_UV_UVNormalizePackApplyTD_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO UV - Normalize Pack Apply Texel Density'
    
    def cmd_Desc (self):
        return 'UVNormalize Pack and Apply Texel Density on the current UVMap'
    
    def cmd_Tooltip (self):
        return 'UVNormalize Pack and Apply Texel Density on the current UVMap'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO UV - Normalize Pack Apply Texel Density'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        mesh = scene.selectedByType('mesh')[0]
        
        
        
        # ------------- UV SEAM Map Detection
        # MODO version checks.
        # Modo 13.0 and up have UV Seam map.
        # Version below 13.0 haven't
        Modo_ver = int(lx.eval ('query platformservice appversion ?'))
        lx.out('Modo Version:',Modo_ver)
        
        #Define the UV Seam vmap name Search case.
        lx.eval("user.defNew name:UVNormPack_DesiredUVSEAMmapName type:string life:momentary")
        UVNormPack_DesiredUVSEAMmapName = 'UV Seam'
        
        #Define the UV Seam vmap name Search case.
        lx.eval("user.defNew name:UVNormPack_NoUVSeamMap type:string life:momentary")
        UVNormPack_NoUVSeamMap = '_____n_o_n_e_____'
        
        
        # Get the number of UV Seam map available on mesh
        DetectedUVSEAMmapCount = len(lx.evalN('vertMap.list seam ?'))
        lx.out('UV SEAM Map Count:', DetectedUVSEAMmapCount)
        
        # Get the name of UV Seam map available on mesh
        DetectedUVSEAMmapName = lx.eval('vertMap.list seam ?')
        lx.out('UV SEAM Map Name:', DetectedUVSEAMmapName)
        # ------------- UV SEAM Map Detection
        
        
        
        
        if Modo_ver >= 1300:
        ## UVSEAM Map Selection Check ##
            lx.out('<--- UVSEAM Map Safety Check --->')
            lx.out('<---------- START ---------->')
            if DetectedUVSEAMmapName == UVNormPack_NoUVSeamMap:
                # lx.eval('vertMap.list seam ?')
                # lx.eval('vertMap.list seam _____n_e_w_____')
                lx.eval('vertMap.new "UV Seam" seam true {0.78 0.78 0.78} 2.0')
                lx.eval('vertMap.list seam "UV Seam"')
            
            elif DetectedUVSEAMmapName == UVNormPack_DesiredUVSEAMmapName:
                lx.out('UV Map and UVSEAM Map Selected')
                lx.eval('vertMap.list seam "UV Seam"')
            # UserUVSEAMmapName = lx.eval1('query layerservice vmap.name ? %s' %UVSEAM_Selected)
            # lx.out('USER UVSEAM Map Name:', UserUVSEAMmapName)
            
            lx.out('<----------- END ----------->')
        # ------------------------------ #
        
        # ------------------------ #
        # <----( Main Macro )----> #
        # ------------------------ #

        lx.out('Start of Update UVNormalizePackApplyTexelDensity Script')
        # ------------- Compare SafetyCheck value and decide or not to continue the process  --- START
        
        lx.eval('texeldensity.normalize')
        lx.eval('uv.pack pack:true stretch:false orient:false direction:auto gaps:"0.2" byPixel:false gapsByPixel:"10.24" bbox:false stack:false region:normalized udim:1001 regionX:"-1.0" regionY:"-1.0" regionW:"3.0" regionH:"3.0" tileU:1 tileV:1 polygonTag:material background:false writeNew:false')
        
        lx.eval('uv.fit sepa:entire gaps:"0.0"')
        lx.eval('texeldensity.set per:island mode:all')
        
        lx.out('End of Update UVNormalizePackApplyTexelDensity Script')
        #####--------------------  Compare SafetyCheck value and decide or not to continue the process  --- END
        
    
lx.bless(SMO_UV_UVNormalizePackApplyTD_Cmd, Cmd_Name)
