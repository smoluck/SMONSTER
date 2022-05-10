Hi. Everyone

----------------------
--- UPDATE LOG ---
----------------------
- 9.10 -
        • Fixed an issue with Error message populating the Event Log, while using the smo.GC.SetNewMaterialSmartRename command as well as the Quick Tag - Set Mat Color ID commands.
        • (Remap the SMO GAME CONTENT MainKeymaps as the smo.GC.SetNewMaterialSmartRename now need a Boolean Argument at the end. --> "smo.GC.SetNewMaterialSmartRename 1" to show Modo Color Picker at launch)


- 9.00 -
        • New Command -->	smo.GC.SplitByPart
        • New Command -->	smo.GC.SplitByMaterial
        • New Command -->	smo.GC.PlasticityPrepareMeshes				(Command to preprocess data from OBJ import from Plasticity. Cleanup Meshes data from Plasticity creating Polygons Parts, Unwraped UVMaps and Merging Solid items.)
        • Bugfix on smo.GC.EdgeSlideProjectToBG command that wasn't releasing the EdgeSlide tool at the end of his execution.
        • Bugfix Switching to AVP Shading Style (The view should now not be offset or reset in terms of Point of view).

- 8.00 -
        • New Command -->	EdgeBoundarySimpleFuse to fuse (without Projection) an Open Edge Boundary loop ( V Norm data is kept from BG Mesh of set Self if mouse over empty area in viewport).
        • New Command --> 	smo.GC.SplitMeshByUDIM to separate a mesh based on UDIM Polygons layout. It create New Mesh Layers, using target Mesh Name + PrefixName + UDIM ID from current selected Mesh.
        • Bugfixes on EdgeBoundaryProjectToBGnFuse to support Self Project onto same mesh. Also hiding other meshes for TransferVNData automatically
        • Transfer VNorm from BG Mesh now have an option to "Lock" edited component when the command is used. Toggle is set to off by default. It is located in the GC Options under Modo Preferences Window.
        • Layout change in right click Context Menus to add more options and commands.

- 7.50 -
        • New smo.GC.UDIMtoMaterial command to convert a Unique Material assignation to a set of Multiple Materials tag, for easy export of UDIM ready Meshes (created via Substance Painter for instance) to Unity Engine.
        • This command use this argument setup:
                • smo.GC.UDIMtoMaterial {Material Name} {UDIM Start ID} {UDIM END ID}
        • Polygon and Edge (right click) Context Menu now have a Chamfer by User Value command for custom size.

- 7.20 -
        • TransferVNrmFromPolyUnderMouse command added to Context Menus, in order to Transfer Vertex Normals from the Mesh under the mouse to the corresponding selected components (Vertex / Edges / Polygons)
          It works both on multiple meshes condition as well as self mesh transfer.

- 7.10 -
        • EdgeboundaryProjectNFuse Bugfix.

- 7.00 -
        • added more Chamfer presets to Polygon Context Menu
        • bugfix on MiniProperties Keymap assignment on Shift-Space (via the Menu SMONSTER / Quick Keymaps / GameContent - Modo15.1 Remapping Cmd). Now it should show up the popover as expected.

- 6.90 -
        • BugFix on StraightenEdgeBoundary on specific condition
        • Exposed the ability to Transfer Vertex Normal Data via Toggle in GC Preferences (while using the EdgeBoundaryProjectNFuse)

- 6.80 -
        • Added 3 new commands to Edge Context Menu
        • smo.GC.StraightenEdgeBoundary: It flatten the selected Edge Boundary to fix squeezed profile.
        • smo.GC.FixVertexWithNullVNormData. It fix missing VertexNormals on a given mesh.
        • smo.GC.EdgeBoundaryProjectToBGnFuse. It extend the current Opened Boundary Edge Loop to nearest BG Mesh using BG Constraint.
	      Then it inset out the resulting Polygon and Edge Bevel it + applying a VertexNormalTransfer to fuse the border with BG Mesh normals.
        • smo.GC.ChamferEdgeByUnit count is now exposed in the Preferences tab. it affect as wel the smo.GC.EdgeBoundaryProjectToBGnFuse accordingly.

- 6.30 -
        • Added Edge UnbevelRing command (default hotkey set to Ctrl-Shift-U)
        • Now there's also an option to use Original Modo Material command via a Toggle for SmartMaterial command.
        • Bugfix on SmartMaterial that was returning error in Modo 15.2 for Area Weighting method.
        • Bugfix on Render Thumbnail Scene (in case meshes Maximum Sizes was 1m / 0.1m / 0.01m / 0.001 )

- 6.10 -
        • Bugfix on Batch Mesh Preset to take care of the item center on thumbnail rendering.

- 6.00 -
        • Batch Export to LXL Mesh Preset command added to Smonster Top menu.
        • Batch convert all the Meshes in the scene to Mesh Preset with custom Thumbnail automatic render.
        • Convert selected Mesh to Mesh Preset with custom Thumbnail automatic render.
        • Subfolder function for this command Specific folder or SMO GC Kit folder.
        • Customizable Background Color for this command.
        • Command to Create / Remove Subfolder Tag in scene

- 5.50 -
        • PieSwitcher pie menu added for Viewport Borders management.
        • smo.Cleanup.RenameUVMapToDefaultSceneWise added (Check for all Meshes in the current scene and rename their First UVMap (by Index = 0) to Modo/Preferences/Defaults/Application name.)
        • Bugfix on OpenTrainingScene Command and Forms.
        • Bugfix Forms for Keymapping in GC Kit.
        • Bugfix on FullscreenMode command.

- 5.40 -
        • smo.GC.SetNewMaterialSmartRename
	   - Create a New Material Tag
	   - Rename the Material Layer in Shader Tree according to Group Material name with a Suffix (suffix defined in Prefs, as well as Separator based on Modo Index Style Prefs).
	   - Set the Shading Model via Preferences / SMO GC Options (Traditionnal, Energy Conserving, Physical Based, Principled, Unreal, Unity, glTF, AxF)
	   - Color Constant Override for Unreal, Unity, glTF, AxF to get correct color in Viewport (if needed via option)
	   - This command is assigned to "M" Key (via a oneclick form).
        • Meshops Popup form is now filtering available Meshops relative to your current Selection type (Vertex / Edge / Polygon / Item)
        • Finaly exposed that new Command: smo.GC.Setup.OffsetCenterPosPreserveInstancesPos that let you redifine Center Position on selected Mesh Item, but preserve the Instances Positions in Worldspace. (Useful for CAD)
        • Rewrite the Add Meshop Command to automatically arrange nodes when created.
        • Updated the AVP Game viewport Preset (Independent  Rotation, Position and Scale are now enabled).
        • Bugfix for QuickCreateCameraMatcherScene to not be Case Sensitive (both .jpg and .JPG are now supported).
        • AVP Game viewport Preset are now loaded according to yourModo Version. It will solve issue with post 15.0 Presets.
        • AVP Game viewport Preset is now set to Progressive Antialiasing by default via Numpad 6 Key. 

- 5.00 -
        • Modo 15.1 KeymapCommander added to set back Original Modo behavior, even if new features like Mini-Properties have been added.
              • Global and Item Mode -> C = Channel Haul
              • view3DOverlay3D and Component Mode -> C = Edge Knife
              • view3DOverlay3D and Component Mode -> Shift-C = Poly Knife
              • view3DOverlay3D and Component Mode -> Alt-C = Poly Loop Slice
              • Global and ContextLess -> SpaceBar = Original Modo Behavior
              • Global and ContextLess -> Shift-SpaceBar = Mini-Properties Popover
        • Set the Copy/Paste PieMenu remapping to Main Remapping (will appear only in ComponentMode via Ctrl + Shift + C)
        • smo.QuickCreateCameraMatchSetup command added. (to set up Camera Match from a set of JPG Images (found in defined Folder)

- 4.90 -
        • smo.GC.FlipVertexNormalData command added

- 4.80 -
        • smo.GC.Unbevel Command added.
        • smo.GC.Setup.MoveRotateCenterToSelection Command added with 3 Modes Supported.
        • smo.GC.MOD.MeshCleanup Command added.
        • smo.GC.MOD.MeshCleanup with Optional Merge/Triple (that Remove Colinear Vertex mode, useful on Text characters).
        • Added Select CoPlanar Menu to SMO GC PM (Pie Menu) and VM (vertical Menu) --> Select Section
        • CENTER related Scripts are now Wrapped commands and they support Reference System state.
        • Updated all the CENTERS Forms.
        • AVP_GAME Shading Preset (Reduced the Wireframe Opacity back to 50% as it was too contrasted at 100 / 70 %).

- 4.70 -
        • Added a "set VertexNormal" Command in Item / Viewport Context Menu.
        • Added Unbevel Ring by Convergence Script in Edge Context Menu.
        • Changed Color Scheme of Workplane color on SMO 3D ColorScheme preset.

- 4.60 -
        • MoveRotateCenter wrapped command added that wasn't supporting ReferenceSystem.
        • Fullscreen ToggleCommand added.

- 4.50 -
        • Hard Chamfer Presets to Edge Right Click Context Menu.
        • Added PrimGenCylinder Commands. (create a new mesh, and create a cylinder with defined arguments)
        • Disabled Split By Material from GC Pie Menu, to solve unwanted computation. now it's available from the Vertical Menu. (ctrl- shift- q)
        • Bugfix on forms (Vertical Menu Update).

- 4.30 -
        • UnbevelPolyLoop rewriten (ctrl-k and ctrl-shift-k commands)
        • Bugfix - Remapping.
        • Bugfix - StarTriple now works again on multiple selected islands, like it was expected to do.
        • Bugfix - SelectCoplanar Poly
        • Bugfix when user was using their own Copy / Paste / Deselect mode in preferences.

- 4.20 -
        • New command added via Right Click Item Context Menu:
                • SMO GC SoloInstanceInPlace (Now select back the original Item instead of the Instance)
                • New SMO GC ReleaseFromIsolate
        • Select Menu form updated to use the new Select CoPlanar Polys command

- 4.00 -
        • New command added via Right Click Item Context Menu:
            • SoloInstanceInPlace
            • Isolate Item and Instances

- 3.90 -
        • Compatibility with Modo 15.X and minor bugfix.

- 3.75 -
        • Bugfix on (Ctrl + numpad "6") Keymap and "Cycle Through MatCaps" Command.
		Ctrl + numapd "6" 	-- > Cycle to Next Matcap
		Ctrl + Alt + numapd "6" -- > Cycle to Previous Matcap
        • Added Hughsk Matcaps and Nidorx Matcap Library Links from Github.
		https://github.com/hughsk/matcap
		https://github.com/nidorx/matcaps

- 3.70 -
        • Currently in Developement but available via Beta Form in GAEM CONTENT.
        • New AttachScriptToPreset features to let you create optinized Mesh Presets library.
        • New Render Thumbnail for Mesh Preset with a Built-in scene with Dynamic Scaled Grid.

- 3.50 -
        • All new Input Remapping Menu to manage your Hotkeys from all Smonster's kits.

- 3.35 -
        • Get back the Senemodo Supertaut piemenu on Ctrl+Alt + L if you have this kit.

- 3.30 -
        • Extracted the UV Map name setting out of the Kit (now it will use your own preferences).
        • Extracted the Tool Handle Advanced Mode setting out of the Kit (now it will use your own preferences).

- 3.25 -
        • Added: Explode By Distance command

- 3.20 -
        • Added: Rotate Center to Selection
        • Added: Move and  Rotate center to Mesh open boundary center
        • Added: Replace Target by Instance

- 3.10 -
        • Updated the Preferences menus, and modified Main Pie Menu to add the MIFABOMA Menu Bar

- 3.00 -
        • Added various new scripts and bugfix.
        • More to come soon via videos and txt description.

- 2.70 -
        • Solved a bug affecting Python Scripts that where using a different User preferences behavior on Copy/Paste settings.

- 2.59 -
        • QuadRemesher Support for Export MeshOp Rig to FBX Sequence
        • Numerous Bugfix and improvements.



------------------
----- VIDEOS -----
------------------

PLAYLIST:
https://www.youtube.com/playlist?list=PLN8BUs-BSLgmFjQupfbI4K6NrY6dmcet1

Installation Part 1:
https://youtu.be/2vz_LKV1ePQ

Installation Part 2 (Config File):
https://youtu.be/jHjpSDeRzaY

Overview of the Boolean Pie Menu:
https://youtu.be/oRCOUVz_LIg

Bench test of the MeshOp to FBX Sequence with Sergey Tyapkin - SciFi Building.
https://youtu.be/0KqwgNggnM4

Bench test of the MeshOp to FBX Sequence with 180 variation of the same Meshop rig for Unity.
https://youtu.be/GSht0uVnxIk

VERTICAL POPOVER MENU:
https://youtu.be/psJ0NObQeyo

CLEANING SCRIPTS:
https://youtu.be/rGs6n_h4Isw

EXPORTS SCRIPTS:
https://youtu.be/6Ohg7he6930

UV SMART PROJECTION PLANAR:
https://youtu.be/NBMFwtqICZ4

UV SMART PROJECTION CYLINDRICAL:
https://youtu.be/Jgbsoe4qNBQ

UV SMART PROJECTION UNWRAP
https://youtu.be/JiAf7zxy4EY

If you want to know more about those Config File, take a look here!
Video on Gumroad product page:
      SMO_GAME_CONTENT_Preferences_in_CFG_Files.mp4


------------------
--- KEYMAPPING ---
------------------

======> Main Keymapping are stored in this file in kit folder:
SMO_GC_Keymap.CFG
SMO_GC_Tools_Command_Keymap.CFG and SMO_GC_Tools_Keymap.CFG are dedicated to Tools Keymap like Bevel that add Round Edge count to Up and Down key.


--> The Master Pie-Menu is reachable by pressing:
Ctr + Q (on PC)			OR		Cmd + Q (on Mac)

--> For Master Vertical Menu (1.99)
Ctr + Shift + Q (on PC)		OR		Cmd + Shift + Q (on Mac)

--> For Sub Pie Menu
Ctrl + Alt + F1 to F9		OR		Cmd + Alt + F1 to F9 (on Mac)

--> For Palette
Ctrl + Alt + X			OR		Cmd + Alt + X (on Mac)

--> For Vertex Normal Pie Menu
Ctrl + Alt + N			OR		Cmd + Alt + N (on Mac)

--> For Baking Pie Menu (1.99)
Ctrl + Alt + Shift + B		OR		Cmd + Alt + Shift + B (on Mac)



------------------
--- DISCLAIMER ---
------------------

You need at least Modo 14.1 to run 100 % of the scripts included.
I try to keep compatibility from 13.0 to 14.0.
As usual if you fiond a bug, please reach me out on SNS and i will do my best to help you and fix this.

======> You ALWAYS need to have SMO_MASTER ans SMOONSTER Kit up and running to use the command in the kit <======

----------------------------------------------------------------------------
As for every Product / Art piece / Assets that you do, like everyone of us,
please do not share those files, as you didn't want to see your work shared
on internet without your permission.
                 I'm sure you'll understand that point.
----------------------------------------------------------------------------



-----------------
---- CONTACT ----
-----------------

on Twitter:
https://twitter.com/sm0luck

on the Foundry Slack server:
foundry-modo.slack.com

on the Foundry Forums:
https://community.foundry.com/discuss/topic/146162
and
https://community.foundry.com/discuss/topic/152258


Best regards, Franck.