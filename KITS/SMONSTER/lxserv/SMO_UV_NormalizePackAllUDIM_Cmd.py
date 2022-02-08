#python
#---------------------------------------
# Name:         SMO_UV_NormalizePackAllUDIM_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Normalize all the UV Islands and Pack
#               them on every UDIM Tiles from UDIM 1001 to 1100.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      28/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

class SMO_UV_NormalizePackAllUDIM_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Fix Flipped UV", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)                 # here the (0) define the argument index.
        self.dyna_Add("Orient Prepass Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO UV Normalize Pack All UDIM Tiles'
    
    def cmd_Desc (self):
        return 'Normalize all the UV Islands and Pack them on every UDIM Tiles from UDIM 1001 to 1100.'
    
    def cmd_Tooltip (self):
        return 'Normalize all the UV Islands and Pack them on every UDIM Tiles from UDIM 1001 to 1100.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO UV Normalize Pack All UDIM Tiles'
    
    def cmd_Flags (self):
        return lx.symbol.fCMD_UNDO
    
    def basic_Enable (self, msg):
        return True
        
    
    def basic_Execute(self, msg, flags):
        scene = modo.scene.current()
        mesh = scene.selectedByType('mesh')[0]
        # meshes = scene.selectedByType('mesh')       # to apply to all selected meshes
        
        
        Int_FixFlippedUV = self.dyna_Int (0)
        Int_Orient_Pass = self.dyna_Int (1)
        
        
        
        ############### 2 ARGUMENTS ###############
        args = lx.args()
        lx.out(args)
        # no Flipped = 0
        # Flipped U = 1
        # Flipped U = 2
        FixFlippedUV = Int_FixFlippedUV
        lx.out('Fix Flipped error UV Island:',FixFlippedUV)
        # Orient preprocess OFF = 0
        # Orient preprocess ON = 1
        Orient_Pass = Int_Orient_Pass
        lx.out('Orient preprocess state:',Orient_Pass)
        ############### ARGUMENTS ###############
        
        
        
        # ############### 2 ARGUMENT Test ###############
        # FixFlippedUV = 1
        # Orient_Pass = 0
        # ############### ARGUMENT ###############
        
        
        
        ################################
        #<----[ DEFINE VARIABLES ]---->#
        ################################
        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        
        ## Selected UVmap Count
        lx.eval("user.defNew name:SMO_SafetyCheckNPAllUDIM_UVMapCount type:boolean life:momentary")
        ## Selected UVmap Name
        lx.eval("user.defNew name:NPAllUDIM_UVMapName type:string life:momentary")
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####
        
        
        
        lx.eval('smo.GC.ClearSelectionVmap 2 1')
        lx.eval('smo.GC.ClearSelectionVmap 3 1')
        lx.eval('smo.GC.ClearSelectionVmap 4 1')
        lx.eval('smo.GC.ClearSelectionVmap 5 1')
        lx.eval('smo.GC.ClearSelectionVmap 6 1')
        lx.eval('smo.GC.ClearSelectionVmap 7 1')
        lx.eval('smo.GC.ClearSelectionVmap 8 1')
        
        
        
        ###############################################
        ####### SAFETY CHECK 1 - UVMap Selected #######
        ###############################################
        lx.out('<------------- START -------------->')
        lx.out('<--- UV Map Safety Check --->')
        
        # Get info about the selected UVMap.
        lx.eval('smo.UV.GetUVMapCountName 0 1 1')
        SelectedMeshUVMapsCount = lx.eval('user.value SMO_UV_SelectedMeshUVmapCount ?')
        lx.out('Selected Mesh UV Maps Count:',SelectedMeshUVMapsCount)
        NPAllUDIM_UVMapName = lx.eval('user.value SMO_UV_SelectedMeshUVmapName ?')
        lx.out('Selected Mesh UV Maps Name:',NPAllUDIM_UVMapName)
        
        lx.eval('smo.GC.ClearSelectionVmap 1 1')
        lx.eval('select.vertexMap %s txuv replace' % NPAllUDIM_UVMapName)
        
        if SelectedMeshUVMapsCount > 1 :
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - Normalize and Pack:}')
            lx.eval('dialog.msg {Please select Only One Vertex Map and run that script again.}')
            lx.eval('dialog.open')
            sys.exit()
            SMO_SafetyCheckNPAllUDIM_UVMapCount = False
        
        if SelectedMeshUVMapsCount < 1 :
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMONSTER - Normalize and Pack:}')
            lx.eval('dialog.msg {You must have a UV map selected to run this script.}')
            lx.eval('dialog.open')
            sys.exit()
            SMO_SafetyCheckNPAllUDIM_UVMapCount = False
        
        if SelectedMeshUVMapsCount == 1 :
            SMO_SafetyCheckNPAllUDIM_UVMapCount = True
            
        # UserUVMapName = lx.eval1('query layerservice vmap.name ? %s' %UVmap_Selected)
        # lx.out('USER UV Map Name:', UserUVMapName)
        lx.out('<- UV Map Safety Check ->')
        lx.out('<------------- END -------------->')
        ###############################################
        
        
        
        ################################
        ## <----( Main Macro : )----> ##
        ################################
        if SMO_SafetyCheckNPAllUDIM_UVMapCount == True :
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 0 0' % (FixFlippedUV, Orient_Pass) )  # 1001
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 1 0' % (FixFlippedUV, Orient_Pass) )  # 1002
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 2 0' % (FixFlippedUV, Orient_Pass) )  # 1003
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 3 0' % (FixFlippedUV, Orient_Pass) )  # 1004
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 4 0' % (FixFlippedUV, Orient_Pass) )  # 1005
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 5 0' % (FixFlippedUV, Orient_Pass) )  # 1006
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 6 0' % (FixFlippedUV, Orient_Pass) )  # 1007
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 7 0' % (FixFlippedUV, Orient_Pass) )  # 1008
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 8 0' % (FixFlippedUV, Orient_Pass) )  # 1009
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 9 0' % (FixFlippedUV, Orient_Pass) )  # 1010
            
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 0 1' % (FixFlippedUV, Orient_Pass) )  # 1011
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 1 1' % (FixFlippedUV, Orient_Pass) )  # 1012
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 2 1' % (FixFlippedUV, Orient_Pass) )  # 1013
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 3 1' % (FixFlippedUV, Orient_Pass) )  # 1014
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 4 1' % (FixFlippedUV, Orient_Pass) )  # 1015
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 5 1' % (FixFlippedUV, Orient_Pass) )  # 1016
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 6 1' % (FixFlippedUV, Orient_Pass) )  # 1017
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 7 1' % (FixFlippedUV, Orient_Pass) )  # 1018
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 8 1' % (FixFlippedUV, Orient_Pass) )  # 1019
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 9 1' % (FixFlippedUV, Orient_Pass) )  # 1020
            
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 0 2' % (FixFlippedUV, Orient_Pass) )  # 1021
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 1 2' % (FixFlippedUV, Orient_Pass) )  # 1022
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 2 2' % (FixFlippedUV, Orient_Pass) )  # 1023
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 3 2' % (FixFlippedUV, Orient_Pass) )  # 1024
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 4 2' % (FixFlippedUV, Orient_Pass) )  # 1025
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 5 2' % (FixFlippedUV, Orient_Pass) )  # 1026
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 6 2' % (FixFlippedUV, Orient_Pass) )  # 1027
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 7 2' % (FixFlippedUV, Orient_Pass) )  # 1028
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 8 2' % (FixFlippedUV, Orient_Pass) )  # 1029
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 9 2' % (FixFlippedUV, Orient_Pass) )  # 1030
            
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 0 3' % (FixFlippedUV, Orient_Pass) )  # 1031
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 1 3' % (FixFlippedUV, Orient_Pass) )  # 1032
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 2 3' % (FixFlippedUV, Orient_Pass) )  # 1033
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 3 3' % (FixFlippedUV, Orient_Pass) )  # 1034
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 4 3' % (FixFlippedUV, Orient_Pass) )  # 1035
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 5 3' % (FixFlippedUV, Orient_Pass) )  # 1036
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 6 3' % (FixFlippedUV, Orient_Pass) )  # 1037
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 7 3' % (FixFlippedUV, Orient_Pass) )  # 1038
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 8 3' % (FixFlippedUV, Orient_Pass) )  # 1039
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 9 3' % (FixFlippedUV, Orient_Pass) )  # 1040
            
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 0 4' % (FixFlippedUV, Orient_Pass) )  # 1041
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 1 4' % (FixFlippedUV, Orient_Pass) )  # 1042
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 2 4' % (FixFlippedUV, Orient_Pass) )  # 1043
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 3 4' % (FixFlippedUV, Orient_Pass) )  # 1044
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 4 4' % (FixFlippedUV, Orient_Pass) )  # 1045
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 5 4' % (FixFlippedUV, Orient_Pass) )  # 1046
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 6 4' % (FixFlippedUV, Orient_Pass) )  # 1047
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 7 4' % (FixFlippedUV, Orient_Pass) )  # 1048
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 8 4' % (FixFlippedUV, Orient_Pass) )  # 1049
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 9 4' % (FixFlippedUV, Orient_Pass) )  # 1050
            
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 0 5' % (FixFlippedUV, Orient_Pass) )  # 1051
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 1 5' % (FixFlippedUV, Orient_Pass) )  # 1052
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 2 5' % (FixFlippedUV, Orient_Pass) )  # 1053
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 3 5' % (FixFlippedUV, Orient_Pass) )  # 1054
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 4 5' % (FixFlippedUV, Orient_Pass) )  # 1055
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 5 5' % (FixFlippedUV, Orient_Pass) )  # 1056
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 6 5' % (FixFlippedUV, Orient_Pass) )  # 1057
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 7 5' % (FixFlippedUV, Orient_Pass) )  # 1058
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 8 5' % (FixFlippedUV, Orient_Pass) )  # 1059
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 9 5' % (FixFlippedUV, Orient_Pass) )  # 1060
            
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 0 6' % (FixFlippedUV, Orient_Pass) )  # 1061
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 1 6' % (FixFlippedUV, Orient_Pass) )  # 1062
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 2 6' % (FixFlippedUV, Orient_Pass) )  # 1063
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 3 6' % (FixFlippedUV, Orient_Pass) )  # 1064
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 4 6' % (FixFlippedUV, Orient_Pass) )  # 1065
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 5 6' % (FixFlippedUV, Orient_Pass) )  # 1066
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 6 6' % (FixFlippedUV, Orient_Pass) )  # 1067
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 7 6' % (FixFlippedUV, Orient_Pass) )  # 1068
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 8 6' % (FixFlippedUV, Orient_Pass) )  # 1069
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 9 6' % (FixFlippedUV, Orient_Pass) )  # 1070
            
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 0 7' % (FixFlippedUV, Orient_Pass) )  # 1071
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 1 7' % (FixFlippedUV, Orient_Pass) )  # 1072
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 2 7' % (FixFlippedUV, Orient_Pass) )  # 1073
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 3 7' % (FixFlippedUV, Orient_Pass) )  # 1074
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 4 7' % (FixFlippedUV, Orient_Pass) )  # 1075
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 5 7' % (FixFlippedUV, Orient_Pass) )  # 1076
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 6 7' % (FixFlippedUV, Orient_Pass) )  # 1077
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 7 7' % (FixFlippedUV, Orient_Pass) )  # 1078
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 8 7' % (FixFlippedUV, Orient_Pass) )  # 1079
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 9 7' % (FixFlippedUV, Orient_Pass) )  # 1080
            
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 0 8' % (FixFlippedUV, Orient_Pass) )  # 1081
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 1 8' % (FixFlippedUV, Orient_Pass) )  # 1082
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 2 8' % (FixFlippedUV, Orient_Pass) )  # 1083
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 3 8' % (FixFlippedUV, Orient_Pass) )  # 1084
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 4 8' % (FixFlippedUV, Orient_Pass) )  # 1085
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 5 8' % (FixFlippedUV, Orient_Pass) )  # 1086
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 6 8' % (FixFlippedUV, Orient_Pass) )  # 1087
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 7 8' % (FixFlippedUV, Orient_Pass) )  # 1088
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 8 8' % (FixFlippedUV, Orient_Pass) )  # 1089
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 9 8' % (FixFlippedUV, Orient_Pass) )  # 1090
            
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 0 9' % (FixFlippedUV, Orient_Pass) )  # 1091
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 1 9' % (FixFlippedUV, Orient_Pass) )  # 1092
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 2 9' % (FixFlippedUV, Orient_Pass) )  # 1093
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 3 9' % (FixFlippedUV, Orient_Pass) )  # 1094
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 4 9' % (FixFlippedUV, Orient_Pass) )  # 1095
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 5 9' % (FixFlippedUV, Orient_Pass) )  # 1096
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 6 9' % (FixFlippedUV, Orient_Pass) )  # 1097
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 7 9' % (FixFlippedUV, Orient_Pass) )  # 1098
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 8 9' % (FixFlippedUV, Orient_Pass) )  # 1099
            lx.eval('smo.UV.NormalizePackByUDIM %s %s 9 9' % (FixFlippedUV, Orient_Pass) )  # 1100
            
            lx.eval('select.drop polygon')
            
        
    
lx.bless(SMO_UV_NormalizePackAllUDIM_Cmd, "smo.UV.NormalizePackAllUDIM")