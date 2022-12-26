# python
"""
# Name:         SMO_GC_GetAngleBetweenThreeVert_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Select 3 vertex. 1st (Extremity A) / 2nd (Corner) / 3rd (Extremity B) to get Corner Angle via query.
#
#
#
# Author:       Franck ELISABETH
# GetRotFromThreeVector based on code from  Avatar "rockjail" on https://gist.github.com/rockjail/9e9379c4e52e72cb4cba
# Website:      https://www.smoluck.com
#
# Created:      03/12/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import lxu.vector
import math
import modo

Cmd_Name = "smo.GC.GetAngleBetweenThreeVert"
# smo.GC.GetAngleBetweenThreeVert ?

# ----------- USE CASE
# TestResult = lx.eval('smo.GC.GetAngleBetweenThreeVert ?')
# lx.out('Angle at Corner is: ',TestResult)
# --------------------

# create a function to get Rotation angle out of 3 Vectors ( created from 3 Vertex positions)
# if you'd like to know more about it have a look at this: http://www.soi.city.ac.uk/~sbbh653/publications/euler.pdf


def GetRotFromThreeVector(m):
    if m[0][0] == 1.0:
        x = math.atan2(m[0][2],m[2][3])
        y = 0
        z = 0
    elif m[0][0] == -1.0:
        x = math.atan2(m[0][2],m[2][3])
        y = 0
        z = 0
    else:
        x = math.atan2(-m[2][0],m[0][0])
        y = math.asin(m[1][0])
        z = math.atan2(-m[1][2],m[1][1])
    return math.degrees(z), math.degrees(x), math.degrees(y)


class SMO_GC_GetAngleBetweenThreeVert_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        
        # Store the currently selected item, or if nothing is selected, an empty list.
        # Wrap this is a try except, the initial launching of Modo will cause this function
        # to perform a shallow execution before the scene state is established.
        # The script will still continue to run, but it outputs a stack trace since it failed.
        # So to prevent console spew on launch when this plugin is loaded, we use the try/except.
        try:
            self.current_Selection = lxu.select.ItemSelection().current()
        except:
            self.current_Selection = []
        
        # If we do have something selected, put it in self.current_Selection
        # Using [-1] will grab the newest item that was added to your selection.
        if len(self.current_Selection) > 0:
            self.current_Selection = self.current_Selection[-1]
        else:
            self.current_Selection = None
        
        # Test the stored selection list, only if it it not empty, instantiate the variables.
        if self.current_Selection:
            self.dyna_Add("Angle", lx.symbol.sTYPE_FLOAT)
            self.basic_SetFlags (0, lx.symbol.fCMDARG_QUERY)
            
        
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO GC - Get Angle between 3 Vertex'
    
    def cmd_Desc (self):
        return 'Select 3 vertex. 1st (Extremity A) / 2nd (Corner) / 3rd (Extremity B) to get Corner Angle via query.'
    
    def cmd_Tooltip (self):
        return 'Select 3 vertex. 1st (Extremity A) / 2nd (Corner) / 3rd (Extremity B) to get Corner Angle via query.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO GC - Get Angle between 3 Vertex'
    
    def basic_Enable(self, msg):
        # Perform the checks for when the command is supposed to be enabled,
        # so users will be informed the command is unavailable by the button being
        # grayed out.
        # :param msg:
        # :type msg: lx.object.Message
        valid_selection = bool(modo.Scene().selectedByType('mesh'))
        return valid_selection
    

    def cmd_Query(self, index, vaQuery):
        # 'select' layer for layerservice
        mLayer = lx.eval('query layerservice layers ? main')
        
        # get selected verts
        lx.eval('select.type vertex')
        selVerts = lx.evalN('query layerservice verts ? selected')
        
        # check if there are 3 verts selected
        if len(selVerts) != 3:
            # replace with a dialog to make it more user friendly, I'm to lazy right now ;)
            lx.out('Please select exactly 3 vertices!')
        
        # get vert positions
        v0Pos = lx.eval('query layerservice vert.wPos ? %s'%selVerts[0])
        v1Pos = lx.eval('query layerservice vert.wPos ? %s'%selVerts[1])
        v2Pos = lx.eval('query layerservice vert.wPos ? %s'%selVerts[2])
        # lx.out(v0Pos)
        # lx.out(v1Pos)
        # lx.out(v2Pos)
        
        # !!! you should check at this point that the vectors are not collinear !!!
        # this means that they are not in a straight line, again I'm to lazy ;)
        
        # create rotation matrix
        # calculate vec0
        vec0 = lxu.vector.normalize(lxu.vector.sub(v1Pos,v0Pos))
        # calculate a temporary tvec1
        tVec1 = lxu.vector.sub(v2Pos,v0Pos)
        # cross product of vec0 and tvec1 will calc vec2 which is perpendicular to vec0 and tvec1 as well as vec1
        vec2 = lxu.vector.normalize(lxu.vector.cross(vec0,tVec1))
        # cross product of vec0 and vec2 will calc vec1
        vec1 = lxu.vector.normalize(lxu.vector.cross(vec0,vec2))
        # add them to a rotation matrix
        rotMat = (vec0,vec1,vec2)
        # lx.out(rotMat)
        
        Angle = GetRotFromThreeVector(rotMat)
        # lx.out(Angle[0])
        # lx.out(Angle[1])
        # lx.out(Angle[2])
        
        va = lx.object.ValueArray(vaQuery)
        va.AddFloat(Angle[0])
        return lx.result.OK


lx.bless(SMO_GC_GetAngleBetweenThreeVert_Cmd, Cmd_Name)
