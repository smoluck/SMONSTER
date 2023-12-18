# python
"""
Name:         SMO_RebuildStrokeRoundExtremity.py

Purpose:      This script is designed to:
              Rebuild the topology of the current selected Vertex set (Stroke Round Extremity)
              to a better Polygon topology.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      13/01/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import modo
import sys

# get selected items using TD SDK
scene = modo.Scene()
selectedItems = scene.selected
mesh = scene.selectedByType('mesh')[0]
CsVert = len(mesh.geometry.vertices.selected)
lx.out('Count Selected Vert:', CsVert)

# ------------- ARGUMENTS Test
# BuildMode = 2
# TriRadial_Mode = 1
# ------------- ARGUMENTS ------------- #

# ------------- 5 ARGUMENTS ------------- #
args = lx.args()
lx.out(args)

# 0 = Simple Ngon
# 1 = Radial Triple
BuildMode = int(args[0])
lx.out('Rebuild Mode:', BuildMode)

# 0 TriRadial by Polygon Bevel
# 1 TriRadial by EdgeExtend
TriRadial_Mode = int(args[1])
lx.out('TriRadial Mode: From EdgeExtend (0) or From Polygon Bevel (1) :', TriRadial_Mode)

User_Mode = int(args[2])
lx.out('User define Side Count:', User_Mode)

SideCount = int(args[3])
lx.out('Side Count Argument Value:', SideCount)
# ------------- ARGUMENTS ------------- #


# ------------------------------ #
# <----( DEFINE VARIABLES )----> #
# ------------------------------ #
# ---------------- Define user value for all the different SafetyCheck --- START
#####
# Only one Item Selected
lx.eval("user.defNew name:SMO_SC_Only1MeshItemSelected type:integer life:momentary")

# Vertex
lx.eval("user.defNew name:SMO_SC_VertexModeEnabled type:integer life:momentary")
# Edges
lx.eval("user.defNew name:SMO_SC_EdgeModeEnabled type:integer life:momentary")
# Polygon
lx.eval("user.defNew name:SMO_SC_PolygonModeEnabled type:integer life:momentary")
# Item
lx.eval("user.defNew name:SMO_SC_ItemModeEnabled type:integer life:momentary")

# Min Vertex count selected
lx.eval("user.defNew name:SMO_SC_min3VertexSelected type:integer life:momentary")
#####
# ---------------- Define user value for all the different SafetyCheck --- END


# ---------------- COPY/PASTE Check Procedure ---------------- #
lx.eval("user.defNew name:User_Pref_CopyDeselectChangedState type:boolean life:momentary")
lx.eval("user.defNew name:User_Pref_PasteSelectionChangedState type:boolean life:momentary")
lx.eval("user.defNew name:User_Pref_PasteDeselectChangedState type:boolean life:momentary")

lx.eval("user.defNew name:User_Pref_CopyDeselect type:boolean life:momentary")
lx.eval("user.defNew name:User_Pref_PasteSelection type:boolean life:momentary")
lx.eval("user.defNew name:User_Pref_PasteDeselect type:boolean life:momentary")

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
# -------------------------------------------- #


# -------------------------- #
# <---( SAFETY CHECK 1 )---> #
# -------------------------- #
# --------------------  safety check 1 : Only One Item Selected --- START
ItemCount = lx.eval('query layerservice layer.N ? selected')
lx.out('ItemCount', ItemCount)

if ItemCount != 1:
    SMO_SC_Only1MeshItemSelected = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO Quick Tag:}')
    lx.eval(
        'dialog.msg {You must only select the Mesh Item layer you are working on, in Item List, to run that script}')
    lx.eval('+dialog.open')
    lx.out('Only One Item Selected result:', SMO_SC_Only1MeshItemSelected)
    lx.out('script Stopped: Select only one Mesh Item')
    sys.exit

else:
    SMO_SC_Only1MeshItemSelected = 1
    lx.out('Only One Item Selected:', SMO_SC_Only1MeshItemSelected)
    lx.out('script running: right amount of Mesh Item selected')
# --------------------  safety check 1 : Only One Item Selected --- END


# -------------------------- #
# <---( SAFETY CHECK 2 )---> #
# -------------------------- #
# Component Selection Mode type --- START

selType = ""
# Used to query layerservice for the list of polygons, edges or vertices.
attrType = ""

if lx.eval1("select.typeFrom typelist:vertex;polygon;edge;item;ptag ?"):
    selType = "vertex"
    attrType = "vert"

    SMO_SC_VertexModeEnabled = 1
    SMO_SC_EdgeModeEnabled = 0
    SMO_SC_PolygonModeEnabled = 0
    SMO_SC_ItemModeEnabled = 0

    lx.out('script Running: Vertex Component Selection Mode')


elif lx.eval1("select.typeFrom typelist:edge;vertex;polygon;item ?"):
    selType = "edge"
    attrType = "edge"

    SMO_SC_VertexModeEnabled = 0
    SMO_SC_EdgeModeEnabled = 1
    SMO_SC_PolygonModeEnabled = 0
    SMO_SC_ItemModeEnabled = 0

    lx.out('script Running: Edge Component Selection Mode')

elif lx.eval1("select.typeFrom typelist:polygon;vertex;edge;item ?"):
    selType = "polygon"
    attrType = "poly"

    SMO_SC_VertexModeEnabled = 0
    SMO_SC_EdgeModeEnabled = 0
    SMO_SC_PolygonModeEnabled = 1
    SMO_SC_ItemModeEnabled = 0

    lx.out('script Running: Polygon Component Selection Mode')


else:
    # This only fails if none of the three supported selection
    # modes have yet been used since the program started, or
    # if "item" or "ptag" (ie: materials) is the current
    # selection mode.

    SMO_SC_VertexModeEnabled = 0
    SMO_SC_EdgeModeEnabled = 0
    SMO_SC_PolygonModeEnabled = 0
    SMO_SC_ItemModeEnabled = 1

    lx.out('script Running: Item Component Selection Mode')

# Component Selection Mode type --- END

# -------------------------- #
# <---( SAFETY CHECK 3 )---> #
# -------------------------- #
# at Least 1 Vertex are selected --- START
if CsVert < 3:
    SMO_SC_min3VertSelected = 0
    lx.eval('dialog.setup info')
    lx.eval('dialog.title {SMO Rebuild Stroke Round Extremity:}')
    lx.eval('dialog.msg {You must select at least 3 Vertex to run that script}')
    lx.eval('+dialog.open')
    lx.out('script Stopped: Add more Vertex to your selection')
    sys.exit

elif CsVert >= 3:
    SMO_SC_min3VertSelected = 1
    lx.out('script running: right amount of Vertex in selection')
# at Least 3 Vertex are selected --- END


if SMO_SC_VertexModeEnabled == 1 and SMO_SC_min3VertSelected == 1 and SMO_SC_Only1MeshItemSelected == 1:
    if BuildMode == 0:
        # lx.eval('select.type item')
        # lx.eval('hide.unsel')
        # lx.eval('select.type vertex')

        # Add current Vertex Selection to SelSet: SOURCE_Vertex
        lx.eval('select.editSet SOURCE_Vertex add')

        # Add current Vertex Selection to SelSet: Schrinked_Vertex
        lx.eval('select.contract')
        lx.eval('select.editSet Schrinked_Vertex add {}')

        lx.eval('select.useSet SOURCE_Vertex replace')
        lx.eval('poly.make auto')
        lx.eval('select.type polygon')
        lx.eval('cut')
        lx.eval('paste')
        lx.eval('hide.sel')
        lx.eval('select.type vertex')
        lx.eval('select.useSet Schrinked_Vertex select')

        # Recreate separate Piece of polygons
        lx.eval('!delete')
        lx.eval('unhide')

        # Merge Back the 2 Sets of Polygons
        lx.eval('select.all')
        lx.eval('script.run "macro.scriptservice:92663570022:macro"')
        lx.eval('select.convert vertex')
        lx.eval('!vert.merge fixed dist:0.000001 disco:false')
        lx.eval('select.type polygon')
        lx.eval('!poly.align')
        lx.eval('select.drop polygon')

        # Delete the Temp SelSet
        lx.eval('select.type vertex')
        lx.eval('!select.deleteSet Schrinked_Vertex')
        lx.eval('!select.deleteSet SOURCE_Vertex')
        lx.eval('select.drop vertex')

        # Switch back to Vertex Seletion state
        # lx.eval('select.type item')
        # lx.eval('unhide')
        lx.eval('select.type vertex')

        lx.out('End of SMO_RebuildCurve Script')
        lx.out('-------------------------------')

    if BuildMode == 1:
        # Tag the current mesh as the TreatenItem
        lx.eval('select.type item')
        lx.eval('select.editSet TreatenItem add')
        lx.eval('hide.unsel')
        lx.eval('select.type vertex')

        # create SelSet: SOURCE_Vertex and Schrinked_Vertex
        lx.eval('select.editSet SOURCE_Vertex add')
        lx.eval('select.contract')
        lx.eval('select.editSet Schrinked_Vertex add {}')

        # create SelSet: AXIS_Vertex
        lx.eval('select.useSet SOURCE_Vertex replace')
        lx.eval('select.useSet Schrinked_Vertex deselect')
        lx.eval('select.editSet AXIS_Vertex add {}')

        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('copy')
        lx.eval('paste')
        lx.eval('select.editSet SOURCE_PolygonIsland add')
        lx.eval('hide.sel')

        # create Temp Polygon from Axis to Fit Workplane to it's Center and then delete it
        lx.eval('select.type vertex')
        lx.eval('poly.make auto')
        lx.eval('select.type polygon')
        lx.eval('workPlane.fitSelect')
        lx.eval('!delete')

        # add an inbetween vertex and Recreate the polygon extremity.
        lx.eval('select.type vertex')

        # Convert SOURCE_Vertex selset to Edge and Extend Sale to Inbetween vertex to build the Radial structure.
        lx.eval('select.useSet SOURCE_Vertex replace')
        lx.eval('select.convert edge')
        lx.eval('tool.set edge.extend on')
        lx.eval('tool.setAttr edge.extend offX 0.0')
        lx.eval('tool.setAttr edge.extend offY 0.0')
        lx.eval('tool.setAttr edge.extend offZ 0.0')
        lx.eval('tool.doApply')
        lx.eval('select.nextMode')
        lx.eval('tool.set TransformScale on')
        lx.eval('tool.noChange')
        lx.eval('tool.set actr.origin on')
        lx.eval('tool.attr xfrm.transform SX 0.0')
        lx.eval('tool.setAttr xfrm.transform SY 0.0')
        lx.eval('tool.doApply')
        lx.eval('select.nextMode')
        lx.eval('select.expand')
        lx.eval('select.convert polygon')
        lx.eval('select.editSet New_ExtPolygon add {}')

        # Vertex Merge to fix continuity.
        lx.eval('select.convert vertex')
        lx.eval('!vert.merge fixed dist:0.000001 disco:false')
        lx.eval('select.type polygon')
        lx.eval('select.useSet New_ExtPolygon replace')

        # Isolate the built data and reset workplane
        lx.eval('copy')
        lx.eval('paste')
        lx.eval('select.editSet New_ExtPolygon add {}')
        lx.eval('workPlane.reset')
        lx.eval('cut')
        lx.eval('paste')
        lx.eval('hide.unsel')
        lx.eval('unhide')
        lx.eval('select.drop polygon')
        lx.eval('select.useSet New_ExtPolygon select')
        lx.eval('select.useSet SOURCE_PolygonIsland select')
        lx.eval('hide.sel')
        lx.eval('select.all')
        lx.eval('!delete')
        lx.eval('unhide')
        lx.eval('select.useSet New_ExtPolygon replace')
        lx.eval('hide.sel')

        # delete cleaned up (unnecesary) vertex
        lx.eval('select.type vertex')
        lx.eval('select.useSet Schrinked_Vertex select')
        lx.eval('!delete')
        lx.eval('select.type polygon')
        lx.eval('unhide')

        # Merge Back the 2 Sets of Polygons
        lx.eval('select.all')
        lx.eval('script.run "macro.scriptservice:92663570022:macro"')
        lx.eval('select.convert vertex')
        lx.eval('!vert.merge fixed dist:0.000001 disco:false')
        lx.eval('select.type polygon')
        lx.eval('!poly.align')
        lx.eval('select.drop polygon')

        # Delete the Temp SelSet
        lx.eval('select.type vertex')
        lx.eval('!select.deleteSet Schrinked_Vertex')
        lx.eval('!select.deleteSet SOURCE_Vertex')
        lx.eval('!select.deleteSet AXIS_Vertex')
        lx.eval('select.type polygon')
        lx.eval('!select.deleteSet New_ExtPolygon')
        lx.eval('!select.deleteSet SOURCE_PolygonIsland')
        lx.eval('select.type vertex')
        lx.eval('select.drop vertex')

        # Switch back to Vertex Selection state
        lx.eval('select.type item')
        lx.eval('unhide')
        lx.eval('select.type vertex')

        # ---------------------------------#
        # Create a Z positive Face Polygon #
        # ---------------------------------#
        lx.eval('item.create mesh')
        lx.eval('item.name PlaneZ xfrmcore')
        lx.eval('select.type polygon')
        lx.eval('script.run "macro.scriptservice:32235710027:macro"')
        # Get the selected layer.
        CubeNormalSelect = lx.eval('query layerservice layers ? selected')
        # Select the first vertex.
        lx.eval('select.element layer:%d type:polygon mode:add index:1' % CubeNormalSelect)
        lx.eval('select.invert')
        lx.eval('!delete')
        lx.eval('select.invert')
        lx.eval('select.createSet Polyflip')
        lx.eval('copy')
        lx.eval('select.type item')
        lx.eval('select.createSet PlaneZ')
        lx.eval('select.drop item')

        # Paste the PlaneZ Data to fix the flipped Polys to point in the Z direction at the end.
        lx.eval('select.useSet TreatenItem select')
        lx.eval('select.type polygon')
        lx.eval('paste')
        lx.eval('select.drop polygon')
        lx.eval('select.useSet Polyflip select')
        # lx.eval('select.pickWorkingSet Polyflip true')
        # lx.eval('@lazySelect.pl selectAll')
        lx.eval('smo.GC.SelectCoPlanarPoly 2 2 1000')
        lx.eval('poly.flip')
        lx.eval('select.drop polygon')
        lx.eval('select.useSet Polyflip select')
        # lx.eval('select.pickWorkingSet Polyflip true')
        lx.eval('!delete')

        # ------------------------#
        # Delete The Z Plane mesh #
        # ------------------------#
        lx.eval('select.type item')
        lx.eval('select.drop item')
        lx.eval('select.useSet PlaneZ select')
        lx.eval('!delete')

        # select back the Treaten Item and delete the Item selset Tag
        lx.eval('select.useSet TreatenItem select')
        lx.eval('!select.deleteSet TreatenItem')
        lx.eval('select.type vertex')

        lx.out('End of SMO_RebuildCurve Script')
        lx.out('-------------------------------')

    if BuildMode == 2:
        if User_Mode == 1:
            # ------------- Define User Value for Rebevel Count --- START
            #####
            # Create a user value that define the EdgeCount for the Rebevel.
            lx.eval("user.defNew name:RebuildEdgeCount type:integer life:momentary")
            # Set the title name for the dialog
            lx.eval('user.def RebuildEdgeCount dialogname "SMO_Rebevel Count"')
            # Set the input field name for the value that the users will see
            lx.eval("user.def RebuildEdgeCount username {Enter edge count here}")
            # The '?' before the user.value calls a popup to have the user set the value
            lx.eval("?user.value RebuildEdgeCount")
            # Now that the user set the value, we can query it
            user_inputReuildCount = lx.eval("user.value RebuildEdgeCount ?")
            lx.out('Edge Count:', user_inputReuildCount)
        #####
        # ------------- Define User Value for Rebevel Count --- END
        if User_Mode == 0:
            user_inputReuildCount = SideCount
            lx.out('Edge Count:', user_inputReuildCount)

        # Tag the current mesh as the TreatenItem
        lx.eval('select.type item')
        lx.eval('select.editSet TreatenItem add')
        lx.eval('select.type vertex')

        # create SelSet: SOURCE_Vertex and Schrinked_Vertex
        lx.eval('select.editSet SOURCE_Vertex add')

        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('select.createSet SrokeRoundLine_Poly')
        lx.eval('copy')

        lx.eval('item.create mesh')
        lx.eval('item.name SrokeRoundLine xfrmcore')

        lx.eval('select.type polygon')
        lx.eval('paste')
        lx.eval('select.type item')
        lx.eval('select.createSet SrokeRoundLine_DATA')
        lx.eval('select.type vertex')
        lx.eval('select.useSet SOURCE_Vertex replace')
        lx.eval('select.convert edge')
        lx.eval('select.editSet SrokeRoundLine_Edge add')
        lx.eval('select.type vertex')

        lx.eval('select.invert')
        lx.eval('!delete')
        lx.eval('select.type edge')
        lx.eval('select.invert')
        lx.eval('select.editSet SrokeRoundLine_AXISEdge add')

        # create Temp Polygon from Axis to Fit Workplane to it's Center and then delete it
        lx.eval('select.convert vertex')
        lx.eval('poly.make auto')
        lx.eval('select.type polygon')
        lx.eval('select.useSet SrokeRoundLine_Poly deselect')
        lx.eval('workPlane.fitSelect')
        lx.eval('select.type item')
        lx.eval('select.convert type:center')
        lx.eval('matchWorkplanePos')
        lx.eval('select.type item')
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('copy')
        lx.eval('workPlane.reset')

        #################
        ####################
        #######################
        ### Load the Mesh Data for the cleanup ###
        try:
            ### Load Rebevel Preset for the processing ###
            # example:
            # mypath = lx.eval("query platformservice alias ? {kit_eterea_swissknife:scripts/geometry}")
            # lx.eval("preset.do {%s/Bowl.lxl}" % mypath)
            # ------------- Define the Preset directory of the Custom CAD Presets to load the Rebevel Assembly --- START
            #####
            SMOAIPath = lx.eval("query platformservice alias ? {kit_SMO_AI_TOOLS:Presets}")
            lx.out('RebuildPresetPath:', SMOAIPath)
            #####
            # ------------- Define the Preset directory of the Custom CAD Presets to load the Rebevel Assembly --- START
            lx.eval('preset.do {%s/SMO_RebuildStrokeRoundExtremity.lxp}' % SMOAIPath)
            lx.eval('select.type item')
            lx.eval('select.drop item')

        except:
            sys.exit

        #### Part 2 : Define the Edgecount for the Rebuilded Curves using the Variable set by User
        lx.eval('select.useSet name:SMO_REBUILDStrokeRoundExtremity_LOC mode:select')
        lx.eval('item.channel Count %s' % user_inputReuildCount)
        lx.eval('select.drop item')
        lx.eval('select.useSet name:SMO_REBUILDStrokeRoundExtremity_INPUT mode:select')

        #### Part 3 : Paste the Curve into the Meshop Container to rebuild the Curve, then freeze the mesh and Bridge the 2 Edges Strips

        # replay name:"Paste Selection"
        lx.eval('paste')
        lx.eval('select.drop polygon')
        lx.eval('select.polygon add type line 8')
        lx.eval('workPlane.fitSelect')
        lx.eval('select.type item')
        lx.eval('select.convert type:center')
        lx.eval('matchWorkplanePos')
        lx.eval('select.type item')
        lx.eval('select.type polygon')
        lx.eval('select.drop polygon')
        lx.eval('workPlane.reset')

        lx.eval('select.type edge')

        lx.eval('select.useSet SrokeRoundLine_Edge replace')
        lx.eval('pmodel.edgeToCurveCMD spline')
        lx.eval('select.type polygon')
        lx.eval('select.polygon add type curve 2')

        lx.eval('select.invert')
        lx.eval('!delete')

        lx.eval('select.type item')
        lx.eval('select.drop item')
        lx.eval('select.useSet name:SMO_REBUILDStrokeRoundExtremity_OUTPUT mode:select')

        lx.eval('deformer.freeze duplicate:false')
        lx.eval('select.type edge')
        lx.eval('select.all')
        lx.eval('copy')
        #######################
        ####################
        #################

        lx.eval('select.type item')
        lx.eval('select.drop item')
        lx.eval('select.useSet TreatenItem replace')

        # ----------------------------------#
        # REBUILT_EDGES_StrokeExtremity #
        # ----------------------------------#
        lx.eval('item.create mesh')
        lx.eval('item.name REBUILT_EDGES_StrokeExtremity xfrmcore')
        lx.eval('select.type edge')
        lx.eval('select.drop edge')
        lx.eval('paste')
        lx.eval('select.editSet REBUILT_EDGES_StrokeExtremity_Edge add {}')
        lx.eval('select.drop edge')
        lx.eval('select.type item')
        lx.eval('select.createSet REBUILT_EDGES_StrokeExtremity')

        lx.eval('select.drop item')
        lx.eval('select.useSet TreatenItem replace')

        lx.eval('select.type vertex')
        lx.eval('select.useSet SOURCE_Vertex replace')
        lx.eval('select.contract')
        lx.eval('select.editSet Schrinked_Vertex add {}')

        # create SelSet: AXIS_Vertex
        lx.eval('select.useSet SOURCE_Vertex replace')
        lx.eval('select.useSet Schrinked_Vertex deselect')
        lx.eval('select.editSet AXIS_Vertex add {}')

        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('copy')
        lx.eval('paste')
        lx.eval('select.editSet SOURCE_PolygonIsland add')
        lx.eval('select.drop polygon')

        # create Temp Polygon from Axis to Fit Workplane to it's Center and then delete it
        lx.eval('select.type vertex')
        lx.eval('poly.make auto')
        lx.eval('select.type polygon')
        lx.eval('workPlane.fitSelect')
        lx.eval('!delete')

        # Paste back the Processed Edge Data from previous scene
        lx.eval('select.type item')
        lx.eval('select.drop item')
        lx.eval('select.useSet REBUILT_EDGES_StrokeExtremity replace')
        lx.eval('select.type edge')
        lx.eval('select.all')
        lx.eval('copy')
        lx.eval('select.type item')
        lx.eval('select.useSet TreatenItem replace')
        lx.eval('select.type edge')
        lx.eval('paste')

        ##################
        # SOLUTION:

        # 0 TriRadial by Polygon Bevel
        # 1 TriRadial by EdgeExtend

        # add an inbetween vertex and Recreate the polygon extremity.

        if TriRadial_Mode == 0:
            # Create the TriRadial Polygons
            lx.eval('poly.make auto')
            lx.eval('select.type polygon')
            lx.eval('tool.set *.bevel on')
            lx.eval('tool.noChange')
            lx.eval('tool.setAttr poly.bevel inset 0.0')
            lx.eval('tool.setAttr poly.bevel shift 0.0')
            lx.eval('tool.doApply')
            lx.eval('select.nextMode')
            lx.eval('tool.set TransformScale on')
            lx.eval('tool.noChange')
            lx.eval('tool.set actr.origin on')
            lx.eval('tool.attr xfrm.transform SX 0.0')
            lx.eval('tool.setAttr xfrm.transform SY 0.0')
            lx.eval('tool.doApply')
            lx.eval('select.nextMode')
            lx.eval('select.expand')

        if TriRadial_Mode == 1:
            # Convert SOURCE_Vertex selset to Edge and Extend Sale to Inbetween vertex to build the Radial structure.
            lx.eval('select.editSet TempEdgeRow add')
            lx.eval('copy')
            lx.eval('paste')
            lx.eval('tool.set TransformScale on')
            lx.eval('tool.noChange')
            lx.eval('tool.set actr.origin on')
            lx.eval('tool.attr xfrm.transform SX 0.0')
            lx.eval('tool.setAttr xfrm.transform SY 0.0')
            lx.eval('tool.doApply')
            lx.eval('select.nextMode')
            lx.eval('select.useSet TempEdgeRow select')
            lx.eval('tool.set edge.bridge on')
            lx.eval('tool.setAttr edge.bridge mode linear')
            lx.eval('tool.setAttr edge.bridge segments 0')
            lx.eval('tool.doApply')
            lx.eval('select.nextMode')
            lx.eval('select.convert vertex')
            lx.eval('select.convert polygon')

        lx.eval('select.editSet New_ExtPolygon add {}')

        # Vertex Merge to fix continuity.
        lx.eval('select.convert vertex')
        lx.eval('!vert.merge fixed dist:0.000001 disco:false')
        lx.eval('select.type polygon')
        lx.eval('select.useSet New_ExtPolygon replace')

        lx.eval('copy')
        lx.eval('item.create mesh')
        lx.eval('item.name OUTPUTMesh xfrmcore')
        lx.eval('select.type polygon')
        lx.eval('paste')
        lx.eval('select.drop polygon')
        lx.eval('select.type item')
        lx.eval('select.createSet OUTPUT_DATA')

        lx.eval('select.useSet TreatenItem replace')
        lx.eval('select.type polygon')
        lx.eval('select.useSet SOURCE_PolygonIsland select')
        lx.eval('select.invert')
        lx.eval('!delete')

        # delete cleaned up (unnecesary) vertex
        lx.eval('select.type vertex')
        lx.eval('select.useSet Schrinked_Vertex select')
        lx.eval('!delete')

        lx.eval('select.type item')
        lx.eval('select.useSet OUTPUT_DATA replace')
        lx.eval('select.type polygon')
        lx.eval('select.all')
        lx.eval('cut')
        lx.eval('select.type item')
        lx.eval('select.useSet TreatenItem replace')
        lx.eval('select.type polygon')
        lx.eval('paste')
        lx.eval('select.drop polygon')
        lx.eval('select.type vertex')
        lx.eval('select.all')
        lx.eval('!vert.merge fixed dist:0.000001 disco:false')
        lx.eval('select.type polygon')
        lx.eval('!poly.align')
        lx.eval('select.drop polygon')
        lx.eval('select.type vertex')
        lx.eval('select.drop vertex')

        # Delete the Temp Meshes
        lx.eval('select.type item')
        lx.eval('select.useSet REBUILT_EDGES_StrokeExtremity replace')
        lx.eval('select.useSet OUTPUT_DATA select')
        lx.eval('select.useSet SrokeRoundLine_DATA select')
        lx.eval('!delete')
        lx.eval('select.useSet TreatenItem replace')

        # ----------------------------------#
        # Create a Z positive Face Polygon #
        # ----------------------------------#
        lx.eval('item.create mesh')
        lx.eval('item.name PlaneZ xfrmcore')
        lx.eval('select.type polygon')
        lx.eval('script.run "macro.scriptservice:32235710027:macro"')
        # Get the selected layer.
        CubeNormalSelect = lx.eval('query layerservice layers ? selected')
        # Select the first vertex.
        lx.eval('select.element layer:%d type:polygon mode:add index:1' % CubeNormalSelect)
        lx.eval('select.invert')
        lx.eval('!delete')
        lx.eval('select.invert')
        lx.eval('select.createSet Polyflip')
        lx.eval('copy')
        lx.eval('select.type item')
        lx.eval('select.createSet PlaneZ')
        lx.eval('select.drop item')
        ####################################

        # Paste the PlaneZ Data to fix the flipped Polys to point in the Z direction at the end.
        lx.eval('select.useSet TreatenItem select')
        lx.eval('select.type polygon')
        lx.eval('paste')
        lx.eval('select.drop polygon')
        lx.eval('select.useSet Polyflip select')
        # lx.eval('select.pickWorkingSet Polyflip true')
        # lx.eval('@lazySelect.pl selectAll')
        lx.eval('smo.GC.SelectCoPlanarPoly 2 2 1000')
        lx.eval('poly.flip')
        lx.eval('select.drop polygon')
        lx.eval('select.useSet Polyflip select')
        # lx.eval('select.pickWorkingSet Polyflip true')
        lx.eval('!delete')

        # -------------------------#
        # Delete The Z Plane mesh #
        # -------------------------#
        lx.eval('select.type item')
        lx.eval('select.drop item')
        lx.eval('select.useSet PlaneZ select')
        lx.eval('!delete')
        lx.eval('select.useSet TreatenItem select')
        lx.eval('select.type polygon')

        # Delete the Temp SelSet Vertex
        lx.eval('select.type vertex')
        lx.eval('!select.deleteSet Schrinked_Vertex')
        lx.eval('!select.deleteSet SOURCE_Vertex')
        lx.eval('!select.deleteSet AXIS_Vertex')
        # Delete the Temp SelSet Edge
        lx.eval('select.type edge')
        lx.eval('!select.deleteSet TempEdgeRow')
        lx.eval('!select.deleteSet REBUILT_EDGES_StrokeExtremity_Edge')
        # Delete the Temp SelSet Polygon
        lx.eval('select.type polygon')
        lx.eval('!select.deleteSet New_ExtPolygon')
        lx.eval('!select.deleteSet SOURCE_PolygonIsland')
        lx.eval('!select.deleteSet SrokeRoundLine_Poly')

        lx.eval('select.type vertex')
        lx.eval('select.drop vertex')

        # Switch back to Vertex Seletion state
        lx.eval('select.type item')
        lx.eval('unhide')
        lx.eval('select.type vertex')

        # ----------------------------------#
        # Create a Z positive Face Polygon #
        # ----------------------------------#
        lx.eval('item.create mesh')
        lx.eval('item.name PlaneZ xfrmcore')
        lx.eval('select.type polygon')
        lx.eval('script.run "macro.scriptservice:32235710027:macro"')
        # Get the selected layer.
        CubeNormalSelect = lx.eval('query layerservice layers ? selected')
        # Select the first vertex.
        lx.eval('select.element layer:%d type:polygon mode:add index:1' % CubeNormalSelect)
        lx.eval('select.invert')
        lx.eval('!delete')
        lx.eval('select.invert')
        lx.eval('select.createSet Polyflip')
        lx.eval('copy')
        lx.eval('select.type item')
        lx.eval('select.createSet PlaneZ')
        lx.eval('select.drop item')
        ####################################

        # Paste the PlaneZ Data to fix the flipped Polys to point in the Z direction at the end.
        lx.eval('select.useSet TreatenItem select')
        lx.eval('select.type polygon')
        lx.eval('paste')
        lx.eval('select.drop polygon')
        lx.eval('select.useSet Polyflip select')
        # lx.eval('select.pickWorkingSet Polyflip true')
        # lx.eval('@lazySelect.pl selectAll')
        lx.eval('smo.GC.SelectCoPlanarPoly 2 2 1000')
        lx.eval('poly.flip')
        lx.eval('select.drop polygon')
        lx.eval('select.useSet Polyflip select')
        # lx.eval('select.pickWorkingSet Polyflip true')
        lx.eval('!delete')

        # -------------------------#
        # Delete The Z Plane mesh #
        # -------------------------#
        lx.eval('select.type item')
        lx.eval('select.drop item')
        lx.eval('select.useSet PlaneZ select')
        lx.eval('!delete')

        ### Part 8 Delete the Rebevel Assembly
        lx.eval('select.item SMO_RebuildStrokeRoundExtremity_ASS set')
        lx.eval('!delete')

        # select back the Treaten Item and delete the Item selset Tag
        lx.eval('select.useSet TreatenItem select')
        lx.eval('!select.deleteSet TreatenItem')
        lx.eval('select.type vertex')
        lx.eval('workPlane.reset')

        lx.out('End of SMO_RebuildCurve Script')
        lx.out('-------------------------------')

# -------------- COPY/PASTE END Procedure  -------------- #
# Restore user Preferences:
if User_Pref_CopyDeselectChangedState == 1:
    lx.eval('pref.value application.copyDeSelection false')
    lx.out('"Deselect Elements after Copying" have been Restored')
if User_Pref_PasteSelectionChangedState == 1:
    lx.eval('pref.value application.pasteSelection false')
    lx.out('"Select Pasted Elements" have been Restored')
if User_Pref_PasteDeselectChangedState == 1:
    lx.eval('pref.value application.pasteDeSelection false')
    lx.out('"Deselect Elements Before Pasting" have been Restored')
# -------------------------------------------- #
