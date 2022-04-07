#python
#---------------------------------------
# Name:         SMO_GC_PrimGenCylinder_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Create a Cylinder or disk based on Arguments
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      21/08/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------
import lx, lxu, modo

Command_Name = "smo.GC.PrimGenCyl"
# smo.GC.PrimGenCyl x 32 [10cm] [56cm] 0 1 1

class SMO_GC_PrimGenCylinder_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Axis", lx.symbol.sTYPE_AXIS)  # 0
        self.dyna_Add("Side Count", lx.symbol.sTYPE_INTEGER)  # 1
        self.dyna_Add("Diameter", lx.symbol.sTYPE_DISTANCE)  # 2
        self.dyna_Add("Lenght", lx.symbol.sTYPE_DISTANCE)  # 3
        self.dyna_Add("Flat Mode", lx.symbol.sTYPE_INTEGER)  # 4
        self.dyna_Add("Cap Mode", lx.symbol.sTYPE_INTEGER)  # 5
        self.dyna_Add("Center at Base Mode", lx.symbol.sTYPE_INTEGER)  # 6
        self.dyna_Add("FTR_IDN (Pipeline Ref ID)", lx.symbol.sTYPE_INTEGER)  # 7
        self.basic_SetFlags(7, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO PrimGenCylinder'

    def cmd_Desc(self):
        return 'SMO Primitive Generator Cylinder: Create a Cylinder or disk based on Arguments'

    def cmd_Tooltip(self):
        return 'SMO Primitive Generator Cylinder: Create a Cylinder or disk based on Arguments'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO PrimGenCylinder'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Axis = self.dyna_String(0)
        Sides = self.dyna_Int(1)
        Diameter = (self.dyna_Float(2) / 2)  # to get the Radius
        DiameterStr = self.dyna_String(2)
        Lenght = (self.dyna_Float(3) / 2)  # to have the correct size
        LenghtStr = self.dyna_String(3)
        FlatMode = self.dyna_Int(4)
        CapMode = self.dyna_Int(5)  # 0 = None ### 1 = Single Poly ### 2 = Quad Grid ### 3 = Radial
        CenterAtBaseMode = self.dyna_Int(6)
        RefIDName = self.dyna_Int(7)
        string_RefIDName = str(RefIDName)

        User_UnitSystem = lx.eval("pref.value units.system ?")
        lx.out(User_UnitSystem)
        User_DefUnit = lx.eval("pref.value units.default ?")
        lx.out(User_DefUnit)

        # # ############### 2 ARGUMENTS Test ###############
        # Diameter = 75
        # # Diameter_mm = 75.0
        # # Diameter_mm = Diameter + 'mm'

        # Lenght_m = 177.59
        # lx.out('The Diameter size is:', Diameter)
        # lx.out('The Lenght is:', Lenght)

        lx.eval('select.type item')
        lx.eval('select.drop item')
        lx.eval('layer.new')

        lx.eval('tool.set prim.cylinder on')
        # Command Block Begin:  ToolActivation
        lx.eval('vertMap.new 00_Texture txuv')
        lx.eval('tool.setAttr prim.cylinder flip true')
        if CapMode == 0:
            lx.eval('tool.setAttr prim.cylinder capBottom none')
            lx.eval('tool.setAttr prim.cylinder capTop none')
        if CapMode == 1:
            lx.eval('tool.setAttr prim.cylinder capBottom single')
            lx.eval('tool.setAttr prim.cylinder capTop single')
        if CapMode == 2:
            lx.eval('tool.setAttr prim.cylinder capBottom quads')
            lx.eval('tool.setAttr prim.cylinder capTop quads')
        if CapMode == 3:
            lx.eval('tool.setAttr prim.cylinder capBottom radial')
            lx.eval('tool.setAttr prim.cylinder capTop radial')

        # Command Block Begin:  Ganged Edits
        lx.eval('tool.attr prim.cylinder cenX 0.0')
        lx.eval('tool.attr prim.cylinder cenY 0.0')
        lx.eval('tool.attr prim.cylinder cenZ 0.0')
        # Command Block End:  Ganged Edits

        lx.eval('tool.setAttr prim.cylinder axis %s' % Axis)
        if Axis == 'x':
            lx.eval('tool.attr prim.cylinder sizeY {%s}' % Diameter)
            lx.eval('tool.attr prim.cylinder sizeZ {%s}' % Diameter)
            if FlatMode == 0:
                lx.eval('tool.attr prim.cylinder sizeX %s' % Lenght)
            if FlatMode == 1:
                lx.eval('tool.attr prim.cylinder sizeX 0')
            if CenterAtBaseMode == 1:
                lx.eval('tool.attr prim.cylinder cenX %s' % Lenght)

        if Axis == 'y':
            lx.eval('tool.attr prim.cylinder sizeX {%s}' % Diameter)
            lx.eval('tool.attr prim.cylinder sizeZ {%s}' % Diameter)
            if FlatMode == 0:
                lx.eval('tool.attr prim.cylinder sizeY %s' % Lenght)
            if FlatMode == 1:
                lx.eval('tool.attr prim.cylinder sizeY 0')
            if CenterAtBaseMode == 1:
                lx.eval('tool.attr prim.cylinder cenY %s' % Lenght)

        if Axis == 'z':
            lx.eval('tool.attr prim.cylinder sizeX {%s}' % Diameter)
            lx.eval('tool.attr prim.cylinder sizeY {%s}' % Diameter)
            if FlatMode == 0:
                lx.eval('tool.attr prim.cylinder sizeZ {%s}' % Lenght)
            if FlatMode == 1:
                lx.eval('tool.attr prim.cylinder sizeZ 0')
            if CenterAtBaseMode == 1:
                lx.eval('tool.attr prim.cylinder cenZ %s' % Lenght )

        lx.eval('tool.attr prim.cylinder sides %s' % Sides)
        lx.eval('tool.attr prim.cylinder segments 1')
        lx.eval('tool.doApply')
        lx.eval('tool.set prim.cylinder off')

        ##########################################################
        # UNIT SYSTEM Check
        User_UnitSystem = lx.eval("pref.value units.system ?")
        # lx.out(User_UnitSystem)
        User_DefUnit = lx.eval("pref.value units.default ?")
        # lx.out(User_DefUnit)

        if User_UnitSystem == 'si':
            if User_DefUnit == 'micrometers':
                Unit = 'um'
            if User_DefUnit == 'millimeters':
                Unit = 'mm'
            if User_DefUnit == 'meters':
                Unit = 'm'
            if User_DefUnit == 'kilometers':
                Unit = 'km'

        if User_UnitSystem == 'metric':
            if User_DefUnit == 'micrometers':
                Unit = 'um'
            if User_DefUnit == 'millimeters':
                Unit = 'mm'
            if User_DefUnit == 'centimeters':
                Unit = 'cm'
            if User_DefUnit == 'meters':
                Unit = 'm'
            if User_DefUnit == 'kilometers':
                Unit = 'km'

        if User_UnitSystem == 'english':
            if User_DefUnit == 'mils':
                Unit = 'mils'
            if User_DefUnit == 'inches':
                Unit = 'inches'
            if User_DefUnit == 'feet':
                Unit = 'feet'
            if User_DefUnit == 'miles':
                Unit = 'miles'

        if User_UnitSystem == 'game':
            if User_DefUnit == 'units':
                Unit = 'gameunit'

        if User_UnitSystem == 'unitless':
            if User_DefUnit == 'meters':
                Unit = 'm'
        ##########################################################

        Mesh_Name = 'Pipeline' + '_' + Axis + '_' + string_RefIDName + '_' + DiameterStr + Unit + '_' + LenghtStr + Unit
        # lx.out('The Mesh Name is ', Mesh_Name)
        lx.eval('item.name {%s} xfrmcore' % Mesh_Name)

        lx.eval('select.drop item')


lx.bless(SMO_GC_PrimGenCylinder_Cmd, Command_Name)


