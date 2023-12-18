# python
"""
Name:         SMO_CB_CycleColor_Cmd.py

Purpose:      This script is designed to:
              Define a new item Color and set the
              Draw Option to the corresponding color.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      04/11/2019
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.CB.CycleColor"
# smo.CB.CycleColor 1


class SMO_CB_CycleColor_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("DrawOpt", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)				# here the (0) define the argument index.
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO CB - Cycle Color'
    
    def cmd_Desc (self):
        return 'Define the itemList Color and Drawing option for the current selected Item in a Cycle mode'
    
    def cmd_Tooltip (self):
        return 'Define the itemList Color and Drawing option for the current selected Item in a Cycle mode.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO CB - Cycle Color'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        DrawOpt = self.dyna_Int (0)
        scene = modo.scene.current()
        meshes = scene.selectedByType(lx.symbol.sITYPE_MESH)
        locators = scene.selectedByType(lx.symbol.sITYPE_LOCATOR)
        
        
        # ------------- ARGUMENTS Test
        # DrawOption = 1
        # ------------- ARGUMENTS ------------- #
        
        # ------------- ARGUMENTS ------------- #
        args = lx.args()
        lx.out(args)
        # Draw Option OFF = 0 
        # Draw Option ON Wireframe = 1
        # Draw Option ON Shaded = 2
        # Draw Option ON Shaded & Wireframe = 3
        DrawOption = DrawOpt
        lx.out('Desired Draw Option Mode:',DrawOption)
        # ------------- ARGUMENTS ------------- #
        
        
        
        
        DrawColorNone = 0
        DrawColorRed = 1
        DrawColorMagenta = 2
        DrawColorPink =  3
        DrawColorBrown =  4
        DrawColorOrange =  5
        DrawColorYellow =  6
        DrawColorGreen =  7
        DrawColorLightGreen =  8
        DrawColorCyan =  9
        DrawColorBlue =  10
        DrawColorLightBlue =  11
        DrawColorUltramarine =  12
        DrawColorPurple =  13
        DrawColorLightPurple =  14
        DrawColorDarkGrey =  15
        DrawColorGrey =  16
        DrawColorWhite =  17
        
        
        
        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        
        # ---------------- Define user value for all the different SafetyCheck --- START
        #####
        
        # Vertex
        lx.eval("user.defNew name:SMO_SafetyCheckIteCol_VertexModeEnabled type:integer life:momentary")
        
        # Edges
        lx.eval("user.defNew name:SMO_SafetyCheckIteCol_EdgeModeEnabled type:integer life:momentary")
        
        # Polygon
        lx.eval("user.defNew name:SMO_SafetyCheckIteCol_PolygonModeEnabled type:integer life:momentary")
        
        # Item
        lx.eval("user.defNew name:SMO_SafetyCheckIteCol_ItemModeEnabled type:integer life:momentary")
        
        ## Current Item List Color
        lx.eval("user.defNew name:CurrentItemListColor type:string life:momentary")
        
        # Item
        lx.eval("user.defNew name:ItemListColor type:integer life:momentary")
        ## Draw Pack
        lx.eval("user.defNew name:DrawPack type:integer life:momentary")
        
        #####
        # ---------------- Define user value for all the different SafetyCheck --- END
        
        
        
        # -------------------------- #
        # <---( SAFETY CHECK 2 )---> #
        # -------------------------- #
        
        # Component Selection Mode type --- START
        
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
        
        # Component Selection Mode type --- END
        # Component Selection Mode type --- END
        
        # lx.out('-------------------------------')
        # lx.out('Start of SMO_DIS_ItemColor Script')
        
        
        # ------------- Compare SafetyCheck value and decide or not to continue the process  --- START
        if SMO_SafetyCheckIteCol_VertexModeEnabled == 1:
            lx.eval('select.type item')
        
        if SMO_SafetyCheckIteCol_EdgeModeEnabled == 1:
            lx.eval('select.type item')
         
        if SMO_SafetyCheckIteCol_PolygonModeEnabled == 1:
            lx.eval('select.type item')
        
        if SMO_SafetyCheckIteCol_ItemModeEnabled == 1:
            lx.eval('select.type item')
        
        
        # ------------------------ #
        # <----( Main Macro )----> #
        # ------------------------ #

        CurrentItemListColor = lx.eval('item.editorColor ?')
        # lx.out('Current Item Color: ', CurrentItemListColor)
        
        
        if CurrentItemListColor == 'none':
            ItemListColor = 1
        if CurrentItemListColor == 'red':
            ItemListColor = 2
        if CurrentItemListColor == 'magenta':
            ItemListColor = 3
        if CurrentItemListColor == 'pink':
            ItemListColor = 4
        if CurrentItemListColor == 'brown':
            ItemListColor = 5
        if CurrentItemListColor == 'orange':
            ItemListColor = 6
        if CurrentItemListColor == 'yellow':
            ItemListColor = 7
        if CurrentItemListColor == 'green':
            ItemListColor = 8
        if CurrentItemListColor == 'lightgreen':
            ItemListColor = 9
        if CurrentItemListColor == 'cyan':
            ItemListColor = 10
        if CurrentItemListColor == 'blue':
            ItemListColor = 11
        if CurrentItemListColor == 'lightblue':
            ItemListColor = 12
        if CurrentItemListColor == 'ultramarine':
            ItemListColor = 13
        if CurrentItemListColor == 'purple':
            ItemListColor = 14
        if CurrentItemListColor == 'lightpurple':
            ItemListColor = 15
        if CurrentItemListColor == 'darkgrey':
            ItemListColor = 16
        if CurrentItemListColor == 'grey':
            ItemListColor = 17
        if CurrentItemListColor == 'white':
            ItemListColor = 0
        
        lx.out('expected Item Color:', ItemListColor)
        
        
        if ItemListColor == 0 :
            lx.eval('item.editorColor none')
        if ItemListColor == 1 :
            lx.eval('item.editorColor red')
        if ItemListColor == 2 :
            lx.eval('item.editorColor magenta')
        if ItemListColor == 3 :
            lx.eval('item.editorColor pink')
        if ItemListColor == 4 :
            lx.eval('item.editorColor brown')
        if ItemListColor == 5 :
            lx.eval('item.editorColor orange')
        if ItemListColor == 6 :
            lx.eval('item.editorColor yellow')
        if ItemListColor == 7 :
            lx.eval('item.editorColor green')
        if ItemListColor == 8 :
            lx.eval('item.editorColor lightgreen')
        if ItemListColor == 9 :
            lx.eval('item.editorColor cyan')
        if ItemListColor == 10 :
            lx.eval('item.editorColor blue')
        if ItemListColor == 11 :
            lx.eval('item.editorColor lightblue')
        if ItemListColor == 12 :
            lx.eval('item.editorColor ultramarine')
        if ItemListColor == 13 :
            lx.eval('item.editorColor purple')
        if ItemListColor == 14 :
            lx.eval('item.editorColor lightpurple')
        if ItemListColor == 15 :
            lx.eval('item.editorColor darkgrey')
        if ItemListColor == 16 :
            lx.eval('item.editorColor grey')
        if ItemListColor == 17 :
            lx.eval('item.editorColor white')
        
        # lx.out('Set Item Color to:', ItemListColor)
        
        
        
        if DrawOption >= 1 :
            ##################### Check Drawing Package State and add one if not present #####################
            DrawPack = lx.eval('smo.CB.GetDrawingPackageState ?')
            # lx.out('Drawing Package state is :',DrawPack)
            
            
            
            
            ##################### For Locators #####################
            ################### Test Draw Pack #####################
            for item in locators:
                if DrawOption >= 1 :
                    if DrawOption == 1 and ItemListColor != 0 :
                        # Set color to user
                        lx.eval('item.channel name:locator$wireOptions value:user item:%s' % item.id)
                        lx.eval('item.channel locator$wireOptions user')
                        lx.eval('item.channel locator$fillOptions default')
                        lx.eval('item.channel locator$style wire')
                        lx.eval('item.channel locator$isSolid false')
                    if DrawOption == 2 and ItemListColor != 0 :
                        lx.eval('item.channel name:locator$fillOptions value:user item:%s' % item.id)
                        lx.eval('item.channel locator$fillOptions user')
                        lx.eval('item.channel locator$wireOptions default')
                        lx.eval('item.channel locator$style shade')
                        lx.eval('item.channel locator$isSolid true')
                    if DrawOption == 3 and ItemListColor != 0 :
                        lx.eval('item.channel name:locator$wireOptions value:user item:%s' % item.id)
                        lx.eval('item.channel name:locator$fillOptions value:user item:%s' % item.id)
                        lx.eval('item.channel locator$fillOptions user')
                        lx.eval('item.channel locator$wireOptions user')
                        lx.eval('item.channel locator$style shade')
                        lx.eval('item.channel locator$isSolid true')
                        
                if DrawOption == 1 and ItemListColor != 0 :
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
                if DrawOption == 2 and ItemListColor != 0 :
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
                if DrawOption == 3 and ItemListColor != 0 :
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
            
            #####################  For Meshes #####################
            ################### Test Draw Pack #####################
            for item in meshes:
                if DrawOption >= 1 :
                    if DrawOption == 1 and ItemListColor != 0 :
                        # Set color to user
                        lx.eval('item.channel name:locator$wireOptions value:user item:%s' % item.id)
                        lx.eval('item.channel locator$wireOptions user')
                        lx.eval('item.channel locator$fillOptions default')
                        lx.eval('item.channel locator$style wire')
                    if DrawOption == 2 and ItemListColor != 0 :
                        lx.eval('item.channel name:locator$fillOptions value:user item:%s' % item.id)
                        lx.eval('item.channel locator$fillOptions user')
                        lx.eval('item.channel locator$wireOptions default')
                        lx.eval('item.channel locator$style shade')
                    if DrawOption == 3 and ItemListColor != 0 :
                        lx.eval('item.channel name:locator$wireOptions value:user item:%s' % item.id)
                        lx.eval('item.channel name:locator$fillOptions value:user item:%s' % item.id)
                        lx.eval('item.channel locator$fillOptions user')
                        lx.eval('item.channel locator$wireOptions user')
                        lx.eval('item.channel locator$style shade')
                        
                if DrawOption == 1 and ItemListColor != 0 :
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
                if DrawOption == 2 and ItemListColor != 0 :
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
                if DrawOption == 3 and ItemListColor != 0 :
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
        
        if ItemListColor == 0 :
            lx.eval('item.editorColor none')
            lx.eval('item.channel locator$fillOptions default')
            lx.eval('item.channel locator$wireOptions default')
            lx.eval('!item.draw rem locator')
        
        if SMO_SafetyCheckIteCol_VertexModeEnabled == 1:
            lx.eval('select.type vertex')
        
        if SMO_SafetyCheckIteCol_EdgeModeEnabled == 1:
            lx.eval('select.type edge')
         
        if SMO_SafetyCheckIteCol_PolygonModeEnabled == 1:
            lx.eval('select.type polygon')
        
        if SMO_SafetyCheckIteCol_ItemModeEnabled == 1:
            lx.eval('select.type item')
        
        # lx.out('End of SMO_DIS_ItemColor Script')
        # lx.out('-------------------------------')
        # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()
    
    
lx.bless(SMO_CB_CycleColor_Cmd, Cmd_Name)
