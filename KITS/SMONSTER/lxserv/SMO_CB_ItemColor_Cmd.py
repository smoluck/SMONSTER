#python
#---------------------------------------
# Name:         SMO_CB_ItemColor_Cmd.py
# Version:      1.0
#
# Purpose: This script is designed to
# Define a new item Color and set the Draw Option
# to the corresponding color.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      04/11/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.CB.ItemColor"
# smo.CB.ItemColor 2 1


class SMO_CB_ItemColor_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("ITColor", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)				# here the (0) define the argument index.
        self.dyna_Add("DrawOpt", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (1, lx.symbol.fCMDARG_OPTIONAL)				# here the (1) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO CB - ItemColor'
    
    def cmd_Desc (self):
        return 'Define the itemList Color and Drawing option for the current selected Item.'
    
    def cmd_Tooltip (self):
        return 'Define the itemList Color and Drawing option for the current selected Item.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO CB - ItemColor'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        ITColor = self.dyna_Int (0)
        DrawOpt = self.dyna_Int (1)
        scene = modo.scene.current()
        selected_meshes = scene.selectedByType(lx.symbol.sITYPE_MESH)
        selected_locators = scene.selectedByType(lx.symbol.sITYPE_LOCATOR)
        
        
        # # ############### 2 ARGUMENTS Test ###############
        # ItemListColor = 2
        # DrawOption = 0
        # # ############### ARGUMENTS ###############
        
        # ############### 2 ARGUMENTS ###############
        args = lx.args()
        lx.out(args)
        # item Color NONE = 0 
        # item Color Cycle through = 1
        # item Color >= red|magenta|pink|brown|orange|yellow|green|lightgreen|cyan|blue|lightblue|ultramarine|purple|lightpurple|darkgrey|grey|white
        ItemListColor = ITColor
        # lx.out('Desired item Color:',ItemListColor)
        # Draw Option OFF = 0 
        # Draw Option ON Wireframe = 1
        # Draw Option ON Shaded = 2
        # Draw Option ON Shaded & Wireframe = 3
        DrawOption = DrawOpt
        # lx.out('Desired Draw Option Mode:',DrawOption)
        # ############### ARGUMENTS ###############
        
        
        
        
        DrawColorRed = 2
        DrawColorMagenta = 3
        DrawColorPink =  4
        DrawColorBrown =  5
        DrawColorOrange =  6
        DrawColorYellow =  7
        DrawColorGreen =  8
        DrawColorLightGreen =  9
        DrawColorCyan =  10
        DrawColorBlue =  11
        DrawColorLightBlue =  12
        DrawColorUltramarine =  13
        DrawColorPurple =  14
        DrawColorLightPurple =  15
        DrawColorDarkGrey =  16
        DrawColorGrey =  17
        DrawColorWhite =  18
        
        
        
        ################################
        #<----[ DEFINE VARIABLES ]---->#
        ################################
        
        #####--- Define user value for all the different SafetyCheck --- START ---#####
        #####
        
        ## Vertex
        lx.eval("user.defNew name:SMO_SafetyCheckIteCol_VertexModeEnabled type:integer life:momentary")
        
        ## Edges
        lx.eval("user.defNew name:SMO_SafetyCheckIteCol_EdgeModeEnabled type:integer life:momentary")
        
        ## Polygon
        lx.eval("user.defNew name:SMO_SafetyCheckIteCol_PolygonModeEnabled type:integer life:momentary")
        
        ## Item
        lx.eval("user.defNew name:SMO_SafetyCheckIteCol_ItemModeEnabled type:integer life:momentary")
        
        # Current Item List Color
        lx.eval("user.defNew name:CurrentItemListColor type:integer life:momentary")
        
        #####
        #####--- Define user value for all the different SafetyCheck --- END ---#####
        
        
        
        ##############################
        ####### SAFETY CHECK 2 #######
        ##############################
        
        #####--------------------  safety check 2: Component Selection Mode type --- START --------------------#####
        
        selType = ""
        # Used to query layerservice for the list of polygons, edges or vertices.
        attrType = ""
        
        if lx.eval1( "select.typeFrom typelist:vertex;polygon;edge;item;ptag ?" ):
            selType = "vertex"
            attrType = "vert"
            
            SMO_SafetyCheckIteCol_VertexModeEnabled = 1
            SMO_SafetyCheckIteCol_EdgeModeEnabled = 0
            SMO_SafetyCheckIteCol_PolygonModeEnabled = 0
            SMO_SafetyCheckIteCol_ItemModeEnabled = 0
            
            # lx.out('script Running: Vertex Component Selection Mode')
            
            
        elif lx.eval1( "select.typeFrom typelist:edge;vertex;polygon;item ?" ):
            selType = "edge"
            attrType = "edge"
            
            SMO_SafetyCheckIteCol_VertexModeEnabled = 0
            SMO_SafetyCheckIteCol_EdgeModeEnabled = 1
            SMO_SafetyCheckIteCol_PolygonModeEnabled = 0
            SMO_SafetyCheckIteCol_ItemModeEnabled = 0
            
            # lx.out('script Running: Edge Component Selection Mode')
            
        elif lx.eval1( "select.typeFrom typelist:polygon;vertex;edge;item ?" ):
            selType = "polygon"
            attrType = "poly"
            
            SMO_SafetyCheckIteCol_VertexModeEnabled = 0
            SMO_SafetyCheckIteCol_EdgeModeEnabled = 0
            SMO_SafetyCheckIteCol_PolygonModeEnabled = 1
            SMO_SafetyCheckIteCol_ItemModeEnabled = 0
            
            # lx.out('script Running: Polygon Component Selection Mode')
        
        
        else:
            # This only fails if none of the three supported selection
            # modes have yet been used since the program started, or
            # if "item" or "ptag" (ie: materials) is the current
            # selection mode.
            
            SMO_SafetyCheckIteCol_VertexModeEnabled = 0
            SMO_SafetyCheckIteCol_EdgeModeEnabled = 0
            SMO_SafetyCheckIteCol_PolygonModeEnabled = 0
            SMO_SafetyCheckIteCol_ItemModeEnabled = 1
            
            # lx.out('script Running: Item Component Selection Mode')
        
        #####--------------------  safety check 2: Component Selection Mode type --- END --------------------#####
        
        
        # lx.out('Start of SMO_DIS_ItemColor Script')
        
        
        #####--------------------  Compare SafetyCheck value and decide or not to continue the process  --- START --------------------#####
        if SMO_SafetyCheckIteCol_VertexModeEnabled == 1:
            lx.eval('select.type item')
            
        if SMO_SafetyCheckIteCol_EdgeModeEnabled == 1:
            lx.eval('select.type item')
             
        if SMO_SafetyCheckIteCol_PolygonModeEnabled == 1:
            lx.eval('select.type item')
            
        if SMO_SafetyCheckIteCol_ItemModeEnabled == 1:
            lx.eval('select.type item')
        
        
        ##############################
        ## <----( Main Macro )----> ##
        ##############################
        
        CurrentItemListColor = lx.eval('item.editorColor ?')
        # lx.out('Current Item Color: ', CurrentItemListColor)
        
        if ItemListColor == 0 :
            lx.eval('item.editorColor none')
        
        if ItemListColor == 2 :
            lx.eval('item.editorColor red')
        if ItemListColor == 3 :
            lx.eval('item.editorColor magenta')
        if ItemListColor == 4 :
            lx.eval('item.editorColor pink')
        if ItemListColor == 5 :
            lx.eval('item.editorColor brown')
        if ItemListColor == 6 :
            lx.eval('item.editorColor orange')
        if ItemListColor == 7 :
            lx.eval('item.editorColor yellow')
        if ItemListColor == 8 :
            lx.eval('item.editorColor green')
        if ItemListColor == 9 :
            lx.eval('item.editorColor lightgreen')
        if ItemListColor == 10 :
            lx.eval('item.editorColor cyan')
        if ItemListColor == 11 :
            lx.eval('item.editorColor blue')
        if ItemListColor == 12 :
            lx.eval('item.editorColor lightblue')
        if ItemListColor == 13 :
            lx.eval('item.editorColor ultramarine')
        if ItemListColor == 14 :
            lx.eval('item.editorColor purple')
        if ItemListColor == 15 :
            lx.eval('item.editorColor lightpurple')
        if ItemListColor == 16 :
            lx.eval('item.editorColor darkgrey')
        if ItemListColor == 17 :
            lx.eval('item.editorColor grey')
        if ItemListColor == 18 :
            lx.eval('item.editorColor white')
            
        
        # CYCLE THROUGH MODE
        if ItemListColor == 1 :
            if CurrentItemListColor == 'none' :
                lx.eval('item.editorColor red')
                ItemListColor = 2
            if CurrentItemListColor == 'red' :
                lx.eval('item.editorColor magenta')
                ItemListColor = 3
            if CurrentItemListColor == 'magenta' :
                lx.eval('item.editorColor pink')
                ItemListColor = 4
            if CurrentItemListColor == 'pink' :
                lx.eval('item.editorColor brown')
                ItemListColor = 5
            if CurrentItemListColor == 'brown' :
                lx.eval('item.editorColor orange')
                ItemListColor = 6
            if CurrentItemListColor == 'orange' :
                lx.eval('item.editorColor yellow')
                ItemListColor = 7
            if CurrentItemListColor == 'yellow' :
                lx.eval('item.editorColor green')
                ItemListColor = 8
            if CurrentItemListColor == 'green' :
                lx.eval('item.editorColor lightgreen')
                ItemListColor = 9
            if CurrentItemListColor == 'lightgreen' :
                lx.eval('item.editorColor cyan')
                ItemListColor = 10
            if CurrentItemListColor == 'cyan' :
                lx.eval('item.editorColor blue')
                ItemListColor = 11
            if CurrentItemListColor == 'blue' :
                lx.eval('item.editorColor lightblue')
                ItemListColor = 12
            if CurrentItemListColor == 'lightblue' :
                lx.eval('item.editorColor ultramarine')
                ItemListColor = 13
            if CurrentItemListColor == 'ultramarine' :
                lx.eval('item.editorColor purple')
                ItemListColor = 14
            if CurrentItemListColor == 'purple' :
                lx.eval('item.editorColor lightpurple')
                ItemListColor = 15
            if CurrentItemListColor == 'lightpurple' :
                lx.eval('item.editorColor darkgrey')
                ItemListColor = 16
            if CurrentItemListColor == 'darkgrey' :
                lx.eval('item.editorColor grey')
                ItemListColor = 17
            if CurrentItemListColor == 'grey' :
                lx.eval('item.editorColor white')
                ItemListColor = 18
            if CurrentItemListColor == 'white' :
                lx.eval('item.editorColor none')
                ItemListColor = 0
        
        
        
        if DrawOption >= 1 :
            ##################### Check Drawing Package State and add one if not present #####################
            DrawPack = lx.eval('smo.CB.GetDrawingPackageState ?')
            # lx.out('Drawing Package state is :',DrawPack)
            
            
            
            
            if DrawPack == 1 and DrawOption == 0 :
                lx.eval('item.channel locator$fillOptions default')
                lx.eval('item.channel locator$wireOptions default')
                lx.eval('!item.draw rem locator')
            
            
            ##################### For Meshes ######################
            ################## Test Draw Pack #####################
            for item in selected_meshes:
                if DrawOption >= 1 :
                    if DrawOption == 1 :
                        # Set color to user
                        lx.eval('item.channel name:locator$wireOptions value:user item:%s' % item.id)
                        lx.eval('item.channel locator$wireOptions user')
                        lx.eval('item.channel locator$fillOptions default')
                        lx.eval('item.channel locator$style wire')
                    if DrawOption == 2 :
                        lx.eval('item.channel name:locator$fillOptions value:user item:%s' % item.id)
                        lx.eval('item.channel locator$fillOptions user')
                        lx.eval('item.channel locator$wireOptions default')
                        lx.eval('item.channel locator$style shade')
                    if DrawOption == 3 :
                        lx.eval('item.channel name:locator$wireOptions value:user item:%s' % item.id)
                        lx.eval('item.channel name:locator$fillOptions value:user item:%s' % item.id)
                        lx.eval('item.channel locator$fillOptions user')
                        lx.eval('item.channel locator$wireOptions user')
                        lx.eval('item.channel locator$style shade')
                    
                    if DrawOption == 1 :
                        # lx.eval('select.color "item.channel locator$wireColor ?"')
                        if ItemListColor == DrawColorRed :
                            lx.eval('item.channel locator$wireColor {1.0 0.0844 0.0382}')
                        elif ItemListColor == DrawColorMagenta :
                            lx.eval('item.channel locator$wireColor {0,8632 0,0802 0,3968}')
                        elif ItemListColor == DrawColorPink :
                            lx.eval('item.channel locator$wireColor {0.807 0.1946 0.1946}')
                        elif ItemListColor == DrawColorBrown :
                            lx.eval('item.channel locator$wireColor {0.402 0.2232 0.0704}')
                        elif ItemListColor == DrawColorOrange :
                            lx.eval('item.channel locator$wireColor {1.0 0.4793 0.0497}')
                        elif ItemListColor == DrawColorYellow :
                            lx.eval('item.channel locator$wireColor {1.0 0,8149 0,0452}')
                        elif ItemListColor == DrawColorGreen :
                            lx.eval('item.channel locator$wireColor {0,0423 0,7682 0,0423}')
                        elif ItemListColor == DrawColorLightGreen :
                            lx.eval('item.channel locator$wireColor {0.2832 0.9131 0.2832}')
                        elif ItemListColor == DrawColorCyan :
                            lx.eval('item.channel locator$wireColor {0,0382 0,9911 0,7454}')
                        elif ItemListColor == DrawColorBlue :
                            lx.eval('item.channel locator$wireColor {0,0529 0,5029 1.0}')
                        elif ItemListColor == DrawColorLightBlue :
                            lx.eval('item.channel locator$wireColor {0,2232 0,624 1.0}')
                        elif ItemListColor == DrawColorUltramarine :
                            lx.eval('item.channel locator$wireColor {0.1274 0.2502 1.0}')
                        elif ItemListColor == DrawColorPurple :
                            lx.eval('item.channel locator$wireColor {0,3763 0,2423 0,8308}')
                        elif ItemListColor == DrawColorLightPurple :
                            lx.eval('item.channel locator$wireColor {0.624 0.4179 1.0}')
                        elif ItemListColor == DrawColorDarkGrey :
                            lx.eval('item.channel locator$wireColor {0,2423 0,2423 0,2423}')
                        elif ItemListColor == DrawColorGrey :
                            lx.eval('item.channel locator$wireColor {0.4852 0.4852 0.4852}')
                        elif ItemListColor == DrawColorWhite :
                            lx.eval('item.channel locator$wireColor {0.855 0.855 0.855}')
                    
                    if DrawOption == 2 :
                        # lx.eval('select.color "item.channel locator$fillColor ?"')
                        if ItemListColor == DrawColorRed :
                            lx.eval('item.channel locator$fillColor {1.0 0.0844 0.0382}')
                        elif ItemListColor == DrawColorMagenta :
                            lx.eval('item.channel locator$fillColor {0,8632 0,0802 0,3968}')
                        elif ItemListColor == DrawColorPink :
                            lx.eval('item.channel locator$fillColor {0.807 0.1946 0.1946}')
                        elif ItemListColor == DrawColorBrown :
                            lx.eval('item.channel locator$fillColor {0.402 0.2232 0.0704}')
                        elif ItemListColor == DrawColorOrange :
                            lx.eval('item.channel locator$fillColor {1.0 0.4793 0.0497}')
                        elif ItemListColor == DrawColorYellow :
                            lx.eval('item.channel locator$fillColor {1.0 0,8149 0,0452}')
                        elif ItemListColor == DrawColorGreen :
                            lx.eval('item.channel locator$fillColor {0,0423 0,7682 0,0423}')
                        elif ItemListColor == DrawColorLightGreen :
                            lx.eval('item.channel locator$fillColor {0.2832 0.9131 0.2832}')
                        elif ItemListColor == DrawColorCyan :
                            lx.eval('item.channel locator$fillColor {0,0382 0,9911 0,7454}')
                        elif ItemListColor == DrawColorBlue :
                            lx.eval('item.channel locator$fillColor {0,0529 0,5029 1.0}')
                        elif ItemListColor == DrawColorLightBlue :
                            lx.eval('item.channel locator$fillColor {0,2232 0,624 1.0}')
                        elif ItemListColor == DrawColorUltramarine :
                            lx.eval('item.channel locator$fillColor {0.1274 0.2502 1.0}')
                        elif ItemListColor == DrawColorPurple :
                            lx.eval('item.channel locator$fillColor {0,3763 0,2423 0,8308}')
                        elif ItemListColor == DrawColorLightPurple :
                            lx.eval('item.channel locator$fillColor {0.624 0.4179 1.0}')
                        elif ItemListColor == DrawColorDarkGrey :
                            lx.eval('item.channel locator$fillColor {0,2423 0,2423 0,2423}')
                        elif ItemListColor == DrawColorGrey :
                            lx.eval('item.channel locator$fillColor {0.4852 0.4852 0.4852}')
                        elif ItemListColor == DrawColorWhite :
                            lx.eval('item.channel locator$fillColor {0.855 0.855 0.855}')
                    
                    if DrawOption == 3 :
                        # lx.eval('select.color "item.channel locator$fillColor ?"')
                        if ItemListColor == DrawColorRed :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {1.0 0.0844 0.0382}')
                        elif ItemListColor == DrawColorMagenta :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0,8632 0,0802 0,3968}')
                        elif ItemListColor == DrawColorPink :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0.807 0.1946 0.1946}')
                        elif ItemListColor == DrawColorBrown :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0.402 0.2232 0.0704}')
                        elif ItemListColor == DrawColorOrange :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {1.0 0.4793 0.0497}')
                        elif ItemListColor == DrawColorYellow :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {1.0 0,8149 0,0452}')
                        elif ItemListColor == DrawColorGreen :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0,0423 0,7682 0,0423}')
                        elif ItemListColor == DrawColorLightGreen :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0.2832 0.9131 0.2832}')
                        elif ItemListColor == DrawColorCyan :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0,0382 0,9911 0,7454}')
                        elif ItemListColor == DrawColorBlue :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0,0529 0,5029 1.0}')
                        elif ItemListColor == DrawColorLightBlue :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0,2232 0,624 1.0}')
                        elif ItemListColor == DrawColorUltramarine :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0.1274 0.2502 1.0}')
                        elif ItemListColor == DrawColorPurple :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0,3759 0,2421 0,83}')
                        elif ItemListColor == DrawColorLightPurple :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0.624 0.4179 1.0}')
                        elif ItemListColor == DrawColorDarkGrey :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0,2423 0,2423 0,2423}')
                        elif ItemListColor == DrawColorGrey :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0.4852 0.4852 0.4852}')
                        elif ItemListColor == DrawColorWhite :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0.855 0.855 0.855}')
            ###########################################################
            
            
            ##################### For Locators ######################
            ################## Test Draw Pack #####################
            for item in selected_locators:
                if DrawOption >= 1 :
                    if DrawOption == 1 :
                        # Set color to user
                        lx.eval('item.channel locator$isSolid false')
                        lx.eval('item.channel name:locator$wireOptions value:user item:%s' % item.id)
                        lx.eval('item.channel locator$wireOptions user')
                        lx.eval('item.channel locator$fillOptions default')
                        lx.eval('item.channel locator$style wire')
                        
                        lx.eval('item.channel locator$isSolid false')
                        
                    if DrawOption >= 2 :
                        lx.eval('item.channel locator$isSolid true')
                        
                    if DrawOption == 2 :
                        lx.eval('item.channel name:locator$fillOptions value:user item:%s' % item.id)
                        lx.eval('item.channel locator$fillOptions user')
                        lx.eval('item.channel locator$wireOptions default')
                        lx.eval('item.channel locator$style shade')
                    if DrawOption == 3 :
                        lx.eval('item.channel name:locator$wireOptions value:user item:%s' % item.id)
                        lx.eval('item.channel name:locator$fillOptions value:user item:%s' % item.id)
                        lx.eval('item.channel locator$fillOptions user')
                        lx.eval('item.channel locator$wireOptions user')
                        lx.eval('item.channel locator$style shade')
                    
                    if DrawOption == 1 :
                        # lx.eval('select.color "item.channel locator$wireColor ?"')
                        if ItemListColor == DrawColorRed :
                            lx.eval('item.channel locator$wireColor {1.0 0.0844 0.0382}')
                        elif ItemListColor == DrawColorMagenta :
                            lx.eval('item.channel locator$wireColor {0,8632 0,0802 0,3968}')
                        elif ItemListColor == DrawColorPink :
                            lx.eval('item.channel locator$wireColor {0.807 0.1946 0.1946}')
                        elif ItemListColor == DrawColorBrown :
                            lx.eval('item.channel locator$wireColor {0.402 0.2232 0.0704}')
                        elif ItemListColor == DrawColorOrange :
                            lx.eval('item.channel locator$wireColor {1.0 0.4793 0.0497}')
                        elif ItemListColor == DrawColorYellow :
                            lx.eval('item.channel locator$wireColor {1.0 0,8149 0,0452}')
                        elif ItemListColor == DrawColorGreen :
                            lx.eval('item.channel locator$wireColor {0,0423 0,7682 0,0423}')
                        elif ItemListColor == DrawColorLightGreen :
                            lx.eval('item.channel locator$wireColor {0.2832 0.9131 0.2832}')
                        elif ItemListColor == DrawColorCyan :
                            lx.eval('item.channel locator$wireColor {0,0382 0,9911 0,7454}')
                        elif ItemListColor == DrawColorBlue :
                            lx.eval('item.channel locator$wireColor {0,0529 0,5029 1.0}')
                        elif ItemListColor == DrawColorLightBlue :
                            lx.eval('item.channel locator$wireColor {0,2232 0,624 1.0}')
                        elif ItemListColor == DrawColorUltramarine :
                            lx.eval('item.channel locator$wireColor {0.1274 0.2502 1.0}')
                        elif ItemListColor == DrawColorPurple :
                            lx.eval('item.channel locator$wireColor {0,3763 0,2423 0,8308}')
                        elif ItemListColor == DrawColorLightPurple :
                            lx.eval('item.channel locator$wireColor {0.624 0.4179 1.0}')
                        elif ItemListColor == DrawColorDarkGrey :
                            lx.eval('item.channel locator$wireColor {0,2423 0,2423 0,2423}')
                        elif ItemListColor == DrawColorGrey :
                            lx.eval('item.channel locator$wireColor {0.4852 0.4852 0.4852}')
                        elif ItemListColor == DrawColorWhite :
                            lx.eval('item.channel locator$wireColor {0.855 0.855 0.855}')
                    
                    if DrawOption == 2 :
                        # lx.eval('select.color "item.channel locator$fillColor ?"')
                        if ItemListColor == DrawColorRed :
                            lx.eval('item.channel locator$fillColor {1.0 0.0844 0.0382}')
                        elif ItemListColor == DrawColorMagenta :
                            lx.eval('item.channel locator$fillColor {0,8632 0,0802 0,3968}')
                        elif ItemListColor == DrawColorPink :
                            lx.eval('item.channel locator$fillColor {0.807 0.1946 0.1946}')
                        elif ItemListColor == DrawColorBrown :
                            lx.eval('item.channel locator$fillColor {0.402 0.2232 0.0704}')
                        elif ItemListColor == DrawColorOrange :
                            lx.eval('item.channel locator$fillColor {1.0 0.4793 0.0497}')
                        elif ItemListColor == DrawColorYellow :
                            lx.eval('item.channel locator$fillColor {1.0 0,8149 0,0452}')
                        elif ItemListColor == DrawColorGreen :
                            lx.eval('item.channel locator$fillColor {0,0423 0,7682 0,0423}')
                        elif ItemListColor == DrawColorLightGreen :
                            lx.eval('item.channel locator$fillColor {0.2832 0.9131 0.2832}')
                        elif ItemListColor == DrawColorCyan :
                            lx.eval('item.channel locator$fillColor {0,0382 0,9911 0,7454}')
                        elif ItemListColor == DrawColorBlue :
                            lx.eval('item.channel locator$fillColor {0,0529 0,5029 1.0}')
                        elif ItemListColor == DrawColorLightBlue :
                            lx.eval('item.channel locator$fillColor {0,2232 0,624 1.0}')
                        elif ItemListColor == DrawColorUltramarine :
                            lx.eval('item.channel locator$fillColor {0.1274 0.2502 1.0}')
                        elif ItemListColor == DrawColorPurple :
                            lx.eval('item.channel locator$fillColor {0,3763 0,2423 0,8308}')
                        elif ItemListColor == DrawColorLightPurple :
                            lx.eval('item.channel locator$fillColor {0.624 0.4179 1.0}')
                        elif ItemListColor == DrawColorDarkGrey :
                            lx.eval('item.channel locator$fillColor {0,2423 0,2423 0,2423}')
                        elif ItemListColor == DrawColorGrey :
                            lx.eval('item.channel locator$fillColor {0.4852 0.4852 0.4852}')
                        elif ItemListColor == DrawColorWhite :
                            lx.eval('item.channel locator$fillColor {0.855 0.855 0.855}')
                    
                    if DrawOption == 3 :
                        # lx.eval('select.color "item.channel locator$fillColor ?"')
                        if ItemListColor == DrawColorRed :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {1.0 0.0844 0.0382}')
                        elif ItemListColor == DrawColorMagenta :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0,8632 0,0802 0,3968}')
                        elif ItemListColor == DrawColorPink :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0.807 0.1946 0.1946}')
                        elif ItemListColor == DrawColorBrown :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0.402 0.2232 0.0704}')
                        elif ItemListColor == DrawColorOrange :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {1.0 0.4793 0.0497}')
                        elif ItemListColor == DrawColorYellow :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {1.0 0,8149 0,0452}')
                        elif ItemListColor == DrawColorGreen :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0,0423 0,7682 0,0423}')
                        elif ItemListColor == DrawColorLightGreen :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0.2832 0.9131 0.2832}')
                        elif ItemListColor == DrawColorCyan :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0,0382 0,9911 0,7454}')
                        elif ItemListColor == DrawColorBlue :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0,0529 0,5029 1.0}')
                        elif ItemListColor == DrawColorLightBlue :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0,2232 0,624 1.0}')
                        elif ItemListColor == DrawColorUltramarine :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0.1274 0.2502 1.0}')
                        elif ItemListColor == DrawColorPurple :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0,3759 0,2421 0,83}')
                        elif ItemListColor == DrawColorLightPurple :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0.624 0.4179 1.0}')
                        elif ItemListColor == DrawColorDarkGrey :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0,2423 0,2423 0,2423}')
                        elif ItemListColor == DrawColorGrey :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0.4852 0.4852 0.4852}')
                        elif ItemListColor == DrawColorWhite :
                            lx.eval('item.channel locator$wireColor {1.0 1.0 1.0}')
                            lx.eval('item.channel locator$fillColor {0.855 0.855 0.855}')
            ###########################################################
        
        if ItemListColor == 0 :
            lx.eval('item.editorColor none')
            lx.eval('item.channel locator$fillOptions default')
            lx.eval('item.channel locator$wireOptions default')
            lx.eval('item.draw rem locator')
        
        if SMO_SafetyCheckIteCol_VertexModeEnabled == 1:
            lx.eval('select.type vertex')
            
        if SMO_SafetyCheckIteCol_EdgeModeEnabled == 1:
            lx.eval('select.type edge')
            
        if SMO_SafetyCheckIteCol_PolygonModeEnabled == 1:
            lx.eval('select.type polygon')
            
        if SMO_SafetyCheckIteCol_ItemModeEnabled == 1:
            lx.eval('select.type item')
        # lx.out('End of SMO_DIS_ItemColor Script')
        #####--------------------  Compare TotalSafetyCheck value and decide or not to continue the process  --- END --------------------#####


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()
    
    
lx.bless(SMO_CB_ItemColor_Cmd, Cmd_Name)
