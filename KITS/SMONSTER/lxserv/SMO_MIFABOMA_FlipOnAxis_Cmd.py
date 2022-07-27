#python
#---------------------------------------
# Name:         SMO_MIFABOMA_FlipOnAxis_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Flip the Mesh or the Polygon selection or the whole item on using the  Item Center.
# 
#
# Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
# Website:      http://www.smoluck.com
#
# Created:      27/02/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo, sys

Cmd_Name = "smo.MIFABOMA.FlipOnAxis"
# smo.MIFABOMA.FlipOnAxis 0 1

class SMO_MIFABOMA_FlipOnAxis_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Axis", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)                 # here the (0) define the argument index.
        self.dyna_Add("Connected Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)

        self.SelModePoly = bool(lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"))

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO MIFABOMA - Flip Axes'
    
    def cmd_Desc (self):
        return 'Flip the Mesh or the Polygon selection using the  Item Center.'
    
    def cmd_Tooltip (self):
        return 'Flip the Mesh or the Polygon selection using the  Item Center.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO MIFABOMA - Flip Axes'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        mode = self.dyna_Int (0)
        scene = modo.scene.current()
        if self.SelModePoly == True:
            lx.eval('smo.MASTER.ForceSelectMeshItemOnly')

        mesh = scene.selectedByType('mesh')[0]
        CsPolys = len(mesh.geometry.polygons.selected)



        # BugFix to preserve the state of the RefSystem (item at origin in viewport)
        # This query only works when an item is selected.
        RefSystemActive = bool()
        CurrentRefSystemItem = lx.eval('item.refSystem ?')
        # print(CurrentRefSystemItem)
        if len(CurrentRefSystemItem) != 0:
            RefSystemActive = True
        else:
            RefSystemActive = False
        # print(RefSystemActive)
        
        
        
        Int_FlipAxis = self.dyna_Int (0)
        Int_Connected = self.dyna_Int (1)
        
        
        ############### 2 ARGUMENTS ###############
        args = lx.args()
        lx.out(args)
        # X Axis = 0
        # Y Axis = 1
        # Z Axis = 2
        FlipAxis = Int_FlipAxis
        lx.out('Flip on Axe value:',FlipAxis)
        # Selection only = 0
        # Connected = 1
        Connected = Int_Connected
        lx.out('Apply to Connected Mode:',Connected)
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
        lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
        lx.eval("user.defNew name:SMO_SafetyCheck_ItemModeEnabled type:integer life:momentary")
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####
        
        
        
        ###############COPY/PASTE Check Procedure#################
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
        ################################################
        
        
        
        
        ##############################
        ####### SAFETY CHECK 1 #######
        ##############################
        
        #####--------------------  safety check 1: Polygon Selection Mode enabled --- START --------------------#####
        
        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""
        
        if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
            selType = "vertex"
            attrType = "vert"
            
            SMO_SafetyCheck_PolygonModeEnabled = 0
            SMO_SafetyCheck_ItemModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO_Flip_Axes:}')
            lx.eval('dialog.msg {You must be in Polygon Mode or in Item Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode or in Item Mode to run that script')
            sys.exit
            #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
            
            
        elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
            selType = "edge"
            attrType = "edge"
            
            SMO_SafetyCheck_PolygonModeEnabled = 0
            SMO_SafetyCheck_ItemModeEnabled = 0
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO_Flip_Axes:}')
            lx.eval('dialog.msg {You must be in Polygon Mode or in Item Mode to run that script}')
            lx.eval('+dialog.open')
            lx.out('script Stopped: You must be in Polygon Mode or in Item Mode to run that script')
            sys.exit
            #sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
            
            
        elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
            selType = "polygon"
            attrType = "poly"
            
            SMO_SafetyCheck_PolygonModeEnabled = 1
            SMO_SafetyCheck_ItemModeEnabled = 0
            lx.out('script Running: Correct Polygon Selection Mode')
            
            
        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            SMO_SafetyCheck_PolygonModeEnabled = 0
            SMO_SafetyCheck_ItemModeEnabled = 1
            lx.out('script Running: Correct Item Selection Mode')
        #####--------------------  safety check 1: Polygon Selection Mode enabled --- END --------------------#####
        
        
        
        
        ##############################
        ####### SAFETY CHECK 2 #######
        ##############################
        if SMO_SafetyCheck_PolygonModeEnabled == 1 :
            #####--------------------  safety check 2: at Least 1 Polygons is selected --- START --------------------#####
            lx.out('Count Selected Poly',CsPolys)
            
            if CsPolys < 1:
                SMO_SafetyCheck_min1PolygonSelected = 0
                lx.eval('dialog.setup info')
                lx.eval('dialog.title {SMO_BoolSubtract:}')
                lx.eval('dialog.msg {You must select at least 1 polygon to run that script}')
                lx.eval('+dialog.open')
                lx.out('script Stopped: Add more polygons to your selection')
                sys.exit
            
            elif CsPolys >= 1:
                SMO_SafetyCheck_min1PolygonSelected = 1
                lx.out('script running: right amount of polygons in selection')
            #####--------------------  safety check 2: at Least 1 Polygons is selected --- END --------------------#####
        
        
        
        ### Test Safety Check in Polygon Mode ###
        #####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
        #####
        if SMO_SafetyCheck_PolygonModeEnabled == 1 and SMO_SafetyCheck_ItemModeEnabled == 0 :
            TotalSafetyCheckTrueValue = 2
            lx.out('Desired Value',TotalSafetyCheckTrueValue)
            TotalSafetyCheck = (SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
            lx.out('Current Value',TotalSafetyCheck)
        #####
        #####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####
        
        
        ### Test Safety Check in Item Mode ###
        #####--- Define current value for the Prerequisite TotalSafetyCheck --- START ---#####
        #####
        if SMO_SafetyCheck_PolygonModeEnabled == 0 and SMO_SafetyCheck_ItemModeEnabled == 1 :
            TotalSafetyCheckTrueValue = 1
            lx.out('Desired Value',TotalSafetyCheckTrueValue)
            TotalSafetyCheck = (SMO_SafetyCheck_ItemModeEnabled)
            lx.out('Current Value',TotalSafetyCheck)
        #####
        #####--- Define current value for the Prerequisite TotalSafetyCheck --- END ---#####
        
        
        
        ##############################
        ## <----( Main Macro )----> ##
        ##############################

        ####
        # Select the VertexNormal Map if it exist in order to update it.
        VNMState = False
        lx.eval('smo.GC.ClearSelectionVmap 4 0')
        VMap_NameList = []
        VMap_TypeList = []
        for map in mesh.geometry.vmaps:
            mapObj = lx.object.MeshMap(map)
            VMap_Name = mapObj.Name()
            VMap_NameList.append(VMap_Name)
            VMap_Type = mapObj.Type()
            VMap_TypeList.append(VMap_Type)
        # print(VMap_NameList)
        # print(VMap_TypeList)
        for i in range(0, len(VMap_TypeList)):
            if (VMap_TypeList[i]) == 1313821261:  # int id for Vertex Normal map
                TargetVNMapName = VMap_NameList[i]
                VNMState = True
        # print(TargetVNMapName)
        ####

        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- START --------------------#####
        if TotalSafetyCheck == TotalSafetyCheckTrueValue :

            ########################################
            ## <----( Main Macro - POLYGON )----> ##
            ########################################
            if SMO_SafetyCheck_PolygonModeEnabled == 1 :

                lx.eval('select.type item')
                if RefSystemActive == True:
                    lx.eval('item.refSystem {}')
                lx.eval('workPlane.reset')
                lx.eval('workPlane.fitSelect')
                lx.eval('select.type polygon')
                if CsPolys > 0:
                    lx.eval('hide.unsel')
                if Connected == 1 :
                    lx.eval('select.connect')
                lx.eval('tool.set actr.origin on')

                ####### TOOL Action ######
                lx.eval('tool.set TransformScale on')
                lx.eval('tool.noChange')
                OriginalNegScaleState = lx.eval('tool.attr xfrm.transform negScale ?')
                OriginalVNormalEditState = lx.eval('tool.attr xfrm.transform normal ?')
                if OriginalNegScaleState == False:
                    lx.eval('tool.attr xfrm.transform negScale true')
                if OriginalVNormalEditState != "update" and VNMState == True :
                    lx.eval('tool.attr xfrm.transform normal update')
                if FlipAxis == 0 :
                    lx.eval('tool.attr xfrm.transform SX -1.0')
                    lx.eval('tool.attr xfrm.transform SY 1.0')
                    lx.eval('tool.attr xfrm.transform SZ 1.0')
                if FlipAxis == 1 :
                    lx.eval('tool.attr xfrm.transform SX 1.0')
                    lx.eval('tool.attr xfrm.transform SY -1.0')
                    lx.eval('tool.attr xfrm.transform SZ 1.0')
                if FlipAxis == 2 :
                    lx.eval('tool.attr xfrm.transform SX 1.0')
                    lx.eval('tool.attr xfrm.transform SY 1.0')
                    lx.eval('tool.attr xfrm.transform SZ -1.0')
                lx.eval('tool.doApply')
                lx.eval('select.nextMode')
                lx.eval('tool.set TransformScale off')

                lx.eval('poly.flip')
                lx.eval('select.drop polygon')
                lx.eval('select.type polygon')
                lx.eval('select.all')


                ####
                # Correct and update the Vertex Normal Map accordingly to the PolyFlip.
                if VNMState == True :
                    lx.eval('smo.GC.FlipVertexNormalMap')
                    # VNMapCmd = "NORM[3]:"
                    # MathCmd = VNMapCmd + TargetVNMapName
                    # print(MathCmd)
                    # lx.eval('vertMap.math {%s} {%s} -1.0 0.0 direct 0 (none) 1.0 0.0 direct 0' % (MathCmd, MathCmd))
                    lx.eval('select.drop polygon')
                ####



                lx.eval('select.type item')
                lx.eval('workPlane.state false')

                if OriginalNegScaleState == False or OriginalVNormalEditState == False :
                    lx.eval('tool.set TransformScale on')
                    lx.eval('tool.noChange')
                    if OriginalNegScaleState == False :
                        lx.eval('tool.attr xfrm.transform negScale false')
                    if OriginalVNormalEditState == False :
                        lx.eval('tool.attr xfrm.transform normal %s' % OriginalVNormalEditState)
                    lx.eval('select.nextMode')
                    lx.eval('tool.set TransformScale off')

                if RefSystemActive == False:
                    lx.eval('item.refSystem {}')
                if RefSystemActive == True:
                    lx.eval('item.refSystem %s' % CurrentRefSystemItem)

                lx.eval('select.type polygon')
                lx.eval('select.drop polygon')
                lx.eval('unhide')


                ####### TOOL Action ######
                #########################
                #########################
                ######## Test With Mirror tool in Replace Mode ##########
                # lx.eval('tool.set *.mirror on')
                # MirrorReplaceSourceState = lx.eval('tool.attr effector.clone replace ?')
                # MirrorFlipPolyState = lx.eval('tool.attr effector.clone flip ?')
                #
                # if MirrorReplaceSourceState == False:
                #     lx.eval('tool.attr effector.clone replace true')
                # if MirrorFlipPolyState == False:
                #     lx.eval('tool.attr effector.clone flip true')
                # lx.eval('tool.attr gen.mirror angle 0.0')
                # lx.eval('tool.attr gen.mirror frot axis')
                # lx.eval('tool.attr gen.mirror cenX 0.0')
                # lx.eval('tool.attr gen.mirror cenY 0.0')
                # lx.eval('tool.attr gen.mirror cenZ 0.0')
                # if FlipAxis == 0:
                #     lx.eval('tool.attr gen.mirror axis 0')
                #     lx.eval('tool.attr gen.mirror upX 0.0')
                #     lx.eval('tool.attr gen.mirror upY 0.0')
                #     lx.eval('tool.attr gen.mirror upZ 1.0')
                #     lx.eval('tool.attr gen.mirror leftX 0.0')
                #     lx.eval('tool.attr gen.mirror leftY 1.0')
                #     lx.eval('tool.attr gen.mirror leftZ 0.0')
                # if FlipAxis == 1:
                #     lx.eval('tool.attr gen.mirror axis 1')
                #     lx.eval('tool.attr gen.mirror upX 1.0')
                #     lx.eval('tool.attr gen.mirror upY 0.0')
                #     lx.eval('tool.attr gen.mirror upZ 0.0')
                #     lx.eval('tool.attr gen.mirror leftX 0.0')
                #     lx.eval('tool.attr gen.mirror leftY 0.0')
                #     lx.eval('tool.attr gen.mirror leftZ 1.0')
                # if FlipAxis == 2:
                #     lx.eval('tool.attr gen.mirror axis 2')
                #     lx.eval('tool.attr gen.mirror upX 1.0')
                #     lx.eval('tool.attr gen.mirror upY 0.0')
                #     lx.eval('tool.attr gen.mirror upZ 0.0')
                #     lx.eval('tool.attr gen.mirror leftX 0.0')
                #     lx.eval('tool.attr gen.mirror leftY 1.0')
                #     lx.eval('tool.attr gen.mirror leftZ 0.0')
                # lx.eval('tool.doApply')
                # lx.eval('select.nextMode')
                # lx.eval('select.drop polygon')
                #
                # lx.eval('select.type item')
                # lx.eval('workPlane.state false')
                #
                # if MirrorReplaceSourceState == False or MirrorFlipPolyState == False:
                #     lx.eval('tool.set *.mirror on')
                #     lx.eval('tool.noChange')
                #     if MirrorReplaceSourceState == False:
                #         lx.eval('tool.attr effector.clone replace {%s}' % MirrorReplaceSourceState)
                #     if MirrorFlipPolyState == False:
                #         lx.eval('tool.attr effector.clone flip {%s}' % MirrorFlipPolyState)
                #     lx.eval('select.nextMode')
                # lx.eval('select.type polygon')
                #########################
                #########################


            
            
            
            #####################################
            ## <----( Main Macro - ITEM )----> ##
            #####################################
            if SMO_SafetyCheck_ItemModeEnabled == 1 :
                lx.eval('select.type item')
                lx.eval('workPlane.reset')
                lx.eval('workPlane.fitSelect')
                lx.eval('select.type polygon')
                lx.eval('select.all')
                lx.eval('tool.set actr.origin on')
                
                lx.eval('tool.set TransformScale on')
                lx.eval('tool.noChange')
                OriginalNegScaleState = lx.eval('tool.attr xfrm.transform negScale ?')
                OriginalVNormalEditState = lx.eval('tool.attr xfrm.transform normal ?')
                if OriginalNegScaleState == False:
                    lx.eval('tool.attr xfrm.transform negScale true')
                if OriginalVNormalEditState != "update":
                    lx.eval('tool.attr xfrm.transform normal update')
                if FlipAxis == 0 :
                    lx.eval('tool.attr xfrm.transform SX -1.0')
                    lx.eval('tool.attr xfrm.transform SY 1.0')
                    lx.eval('tool.attr xfrm.transform SZ 1.0')
                if FlipAxis == 1 :
                    lx.eval('tool.attr xfrm.transform SX 1.0')
                    lx.eval('tool.attr xfrm.transform SY -1.0')
                    lx.eval('tool.attr xfrm.transform SZ 1.0')
                if FlipAxis == 2 :
                    lx.eval('tool.attr xfrm.transform SX 1.0')
                    lx.eval('tool.attr xfrm.transform SY 1.0')
                    lx.eval('tool.attr xfrm.transform SZ -1.0')
                    
                lx.eval('tool.doApply')
                lx.eval('select.nextMode')
                
                lx.eval('poly.flip')
                lx.eval('select.drop polygon')
                lx.eval('select.type item')
                lx.eval('workPlane.state false')

                if OriginalNegScaleState == False:
                    lx.eval('tool.set TransformScale on')
                    lx.eval('tool.noChange')
                    lx.eval('tool.attr xfrm.transform negScale false')
                    lx.eval('select.nextMode')


                if RefSystemActive == False:
                    lx.eval('item.refSystem {}')
                if RefSystemActive == True:
                    lx.eval('item.refSystem %s' % CurrentRefSystemItem)
                    lx.eval('viewport.fitSelected')
        
        
        ###############COPY/PASTE END Procedure#################
        # Restore user Preferences:
        if User_Pref_CopyDeselectChangedState == 1 :
            lx.eval('pref.value application.copyDeSelection false')
            lx.out('"Deselect Elements after Copying" have been Restored')
        if User_Pref_PasteSelectionChangedState == 1 :
            lx.eval('pref.value application.pasteSelection false')
            lx.out('"Select Pasted Elements" have been Restored')
        if User_Pref_PasteDeselectChangedState == 1 :
            lx.eval('pref.value application.pasteDeSelection false')
            lx.out('"Deselect Elements Before Pasting" have been Restored')
        ########################################################
        
        
        elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
            lx.out('script Stopped: your mesh does not match the requirement for that script.')
            sys.exit

        lx.out('End of SMO_Bool_Subtract Script')
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END --------------------#####
        

lx.bless(SMO_MIFABOMA_FlipOnAxis_Cmd, Cmd_Name)
