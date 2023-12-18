# python
"""
Name:			Unwrap_PlanarbyNormal.py

Purpose:		This script is designed to:
                Unwrap the current Polygon Selection
                using his normal as a guide.

Author:      	Franck ELISABETH
Website:      	https://www.linkedin.com/in/smoluck/
Created:      	28/12/2018
Copyright:    	(c) Franck Elisabeth 2017-2022
"""

import lx
import modo
import sys

scene = modo.scene.current()
mesh = scene.selectedByType('mesh')[0]
CsPolys = len(mesh.geometry.polygons.selected)

# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #
# ---------------- Define user value for all the different SafetyCheck --- START
lx.eval("user.defNew name:SMO_SafetyCheck_PolygonModeEnabled type:integer life:momentary")
lx.eval("user.defNew name:SMO_SafetyCheck_min1PolygonSelected type:integer life:momentary")
# ---------------- Define user value for all the different SafetyCheck --- END


# -------------------------- #
# <---( SAFETY CHECK 1 )---> #
# -------------------------- #

# --------------------  safety check 1: Polygon Selection Mode enabled --- START

selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
    selType = "vertex"
    attrType = "vert"

    SMO_SafetyCheck_PolygonModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {Unwrap_PlanarbyNormal:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
# sys.exit( "LXe_FAILED:Must be in polygon selection mode." )


elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
    selType = "edge"
    attrType = "edge"

    SMO_SafetyCheck_PolygonModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {Unwrap_PlanarbyNormal:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
# sys.exit( "LXe_FAILED:Must be in polygon selection mode." )

elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
    selType = "polygon"
    attrType = "poly"

    SMO_SafetyCheck_PolygonModeEnabled = 1
    lx.out('script Running: Correct Component Selection Mode')


else:
    # This only fails if none of the three supported selection
    # modes have yet been used since the program started, or
    # if "item" or "ptag" (ie: materials) is the current
    # selection mode.
    SMO_SafetyCheck_PolygonModeEnabled = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {Unwrap_PlanarbyNormal:}')
    lx.eval('dialog.msg {You must be in Polygon Mode to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: You must be in Polygon Mode to run that script')
    sys.exit
# sys.exit( "LXe_FAILED:Must be in polygon selection mode." )
# --------------------  safety check 1: Polygon Selection Mode enabled --- END


# -------------------------- #
# <---( SAFETY CHECK 2 )---> #
# -------------------------- #
# at Least 1 Polygons is selected --- START
lx.out('Count Selected Poly', CsPolys)

if CsPolys < 1:
    SMO_SafetyCheck_min1PolygonSelected = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {Unwrap_PlanarbyNormal:}')
    lx.eval('dialog.msg {You must select at least 1 polygon to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: Add more polygons to your selection')
    sys.exit

elif CsPolys >= 1:
    SMO_SafetyCheck_min1PolygonSelected = 1
    lx.out('script running: right amount of polygons in selection')
# at Least 1 Polygons is selected --- END


# ---------------- Define current value for the Prerequisite TotalSafetyCheck --- START
#####
TotalSafetyCheckTrueValue = 2
lx.out('Desired Value', TotalSafetyCheckTrueValue)
TotalSafetyCheck = (SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min1PolygonSelected)
lx.out('Current Value', TotalSafetyCheck)
#####
# ---------------- Define current value for the Prerequisite TotalSafetyCheck --- END


# ------------------------ #
# <----( Main Macro )----> #
# ------------------------ #
# ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- START
if TotalSafetyCheck == TotalSafetyCheckTrueValue:

    # Align Workplane to selection
    lx.eval('workPlane.fitSelect')

    lx.eval('smo.GC.SelectCoPlanarPoly 1 2')

    lx.eval('view3d.projection top')

    lx.eval('tool.set uv.viewProj on')
    lx.eval('view3d.projection top')
    lx.eval('tool.viewType xyz')
    lx.eval('tool.setAttr uv.viewProj ascal true')

    # lx.eval('tool.set preset:"uv.create" mode:on')
    # lx.eval('tool.setAttr tool:"uv.create" attr:mode value:manual')

    # ## Set Axis Y
    # try:
    # Command Block Begin:
    # lx.eval('tool.setAttr uv.create axis 1')
    # Command Block End:
    # except:
    # sys.exit

    # try:
    # Command Block Begin:
    # lx.eval('tool.setAttr tool:"uv.create" attr:sizX value:"0.1"')
    # lx.eval('tool.setAttr tool:"uv.create" attr:sizY value:"0.1"')
    # lx.eval('tool.setAttr tool:"uv.create" attr:sizZ value:"0.1"')
    # Command Block End:
    # except:
    # sys.exit

    # try:
    # Command Block Begin:
    # lx.eval('tool.setAttr tool:"uv.create" attr:cenX value:"0.0"')
    # lx.eval('tool.setAttr tool:"uv.create" attr:cenY value:"0.0"')
    # lx.eval('tool.setAttr tool:"uv.create" attr:cenZ value:"0.0"')
    # Command Block End:
    # except:
    # sys.exit

    lx.eval('tool.apply')

    lx.eval('view3d.projection psp')

    lx.eval('tool.viewType uv')

    # replay name:"Fit UVs"
    lx.eval('uv.fit entire true gapsByPixel:0.0 udim:1001')

    # ###########################
    # replay name:"Flip UV Island"
    # try:
    # Command Block Begin:
    # lx.eval('uv.flip false u')
    # Command Block End:
    # except:
    # sys.exit
    # ###########################

    # ###########################
    # Set specific Texel Density
    # replay name:"User Value"
    # lx.eval('user.value name:"texeldensity.size3D" value:"0.1"')
    # replay name:"User Value"
    # lx.eval('user.value name:"texeldensity.sizeUV" value:"512.0"')
    # ###########################

    # replay name:"Set Texel Density"
    # lx.eval('texeldensity.set per:island mode:all')

    # replay name:"Move"
    lx.eval('tool.set preset:TransformMove mode:on')

    try:
        # Command Block Begin:
        lx.eval('tool.setAttr tool:"xfrm.transform" attr:TX value:"-1.0"')
        lx.eval('tool.setAttr tool:"xfrm.transform" attr:TY value:"0.0"')
        lx.eval('tool.setAttr tool:"xfrm.transform" attr:TZ value:"0.0"')
        lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"-1.0"')
        lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"0.0"')
    # Command Block End:
    except:
        sys.exit

    # Launch the Move
    lx.eval('tool.doapply')
    lx.eval('tool.set preset:TransformMove mode:off')

    lx.eval('workPlane.reset')

elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
    lx.out('script Stopped: your mesh does not match the requirement for that script.')
    sys.exit

lx.out('End of Unwrap_PlanarbyNormal Script')
# ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END
