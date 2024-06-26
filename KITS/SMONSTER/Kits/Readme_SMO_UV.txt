----------------------
--- UPDATE LOG ---
----------------------
- 4.55 -
        • Rectangle command have been changed from "R" key to "Alt - R" to let user scale UV maps data in UVTexture editor.

- 4.50 -
        • smo.uv.Multi.UnwrapCylindrical - Bugfix on single item process.
        • Added Keymaps dialog in QuickKeymaps command for keys over UV Viewport:
        	• A - Align Tools
        	• P - Normalize and Pack
        	• R - Rectangle
        	• C - Cut/Split/UVSeam

- 4.40 -
        • smo.UV.Multi.AutoUnwrapSmartByAngle 88 180 - New command to Auto Unwrap the current Mesh item by using Sharp Edges defined by a Min and Max Angle as Seams.
        	• It use the SmartUnwrap base arguments (4 types):
        	• Unwrap Method (Conformal or Angle Based)
        	• Initial Projection (Planar or Group Normal)
        	• Min Ang
        	• Max Angle
        • Updated UI (Vertical Menu and Pie Menu) to expose Auto Smart Unwrap By Angle command.
        • smo.UV.SmartOrient - Bugfix to keep EdgeSelection from UVSpace (Edge selection relative to UVIslands).
        • smo.uv.Multi.UnwrapSmart - Bugfix to work as well in Edge Mode to define UVSeams.

- 4.20 -
        • Bugfix on Multi Meshes Unwrap when UVmaps where miss-matching in presence or not.
        	• smo.UV.Multi.UnwrapRectangleOrient / smo.UV.Multi.UnwrapPlanar / smo.UV.Multi.UnwrapSmart / smo.UV.Multi.UnwrapCylindrical
        • smo.UV.AutoCreateUVMap - Automatically Create a UV Map if missing using Default UVMap Name in Preferences.

- 4.10 -
        • Added UV popup menu to the Vertex Maps under Info / Statistics to give access to UV commands more simply. It also helps Users to keep in mind that they have to select the UVMap before running the command.

- 3.55 -
        • UV Tools Menu Reordering

- 3.50 -
        • Menu and Icons (Big UI refresh)
        • Bugfix (Get UVMap Count argument not correctly exposed. It adds also a 4th argument to deselect all maps except UV maps)

- 3.00 -
        • Bugfix on UnwrapCylindrical to disable Auto RelaxUV Island if the Unwrap Rectangle was True and AutoRelax was True, in order to keep Rectangle result in output.

- 2.80 -
        • UV Kit now support Micro Bevel Workflow by letting you use Auto Expand Option on SmartUnwrap and PlanarUnwrap
        • Added 2 Toggles to Main UV Pie menu to switch Auto Hide Unwrapped Poly and Auto Expand Poly

- 2.50 -
        • Added "Select Coplanar Touching 2 Deg + Expand" in Pie Menu Form (for Mid Poly UV Mapping) 
        • Adding "Select Coplanar on Object + Expand" in Pie Menu Form
        • Bugfix on Smart Unwrap , when Edge Mode was used, the script wasn't repositioning the UVs in 0-1 Space when "Auto Relocate" option was False
        • Bugfix on UnwrapCylindrical that now use Auto Relax and Auto Orient
        • Bugfix in forms (tooltips)

- 2.30 -
        • Load custom UV Checker texture was added to the Smart Projection PieMenu (Different resolution available: 512px, 1024, 2048, 4096).

- 2.20 -
        • Unwrap Smart / Planar / Cylindrical commands (Reference System Support)
        • Added the link to UV Preferences in Tail Menu
        • Bugfix on UV tools (Unwrap tools). (In case you wasn't selecting the Item first and worked directly in Polygon Mode.
          (Now he commands automatically select it for you at least if you have one Polygon Selected.)

- 2.00 -
        • Switched CAD Tools / UV / VeNom Kits from Lazy Select (Seneca Menard scripts) workflow to Built-in Select CoPlanar Polygons command Introduced in recent release of Modo.
            • Better Performance in mentioned Kits.
            • No More headache on Initialize CAD / UV / Venom kit procedure. (Runs smoothly right after the installation.)

- 1.80 -
        • Compatibility with Modo 15.X and minor bugfix.

- 1.70 -
        • All new Input Remapping Menu to manage your Hotkeys from all Smonster's kits.

- 1.60 -
        • Added a new command: Unwrap_By_SharpEdge to quickly unwrap buildings an other man made props.

- 1.50 -
        • Update UV Seam Cut Map toggle added to Preferences.
        • Support for multiple UVMaps on every Unwrap tools (Planar / Cylindrical / Unwrap)
        • Bug fix in UV Tools.

- 1.35 -
        • Bugfix on Modo Tail Menu

- 1.32 -
        • Bugfix at UV Smart Projection Planar SPP command in first Execution after installing the script.

- 1.30 -
        • Updated SMO UV Kit for new PieMenu and customizable workflow via Preferences.
        • Various bugfix.

- 1.15 -
        • Improvement of Code in many Scripts that where using selection commands.
        • Updated SMO UV Kit Icons



------------------
----- VIDEOS -----
------------------

PLAYLIST:
https://www.youtube.com/playlist?list=PLN8BUs-BSLgldE02O4JpR1OosCTvmUh_Z

PIXELFONDUE - S60 - S90 - Quick Videos
https://www.pixelfondue.com/blog/2020/7/18/smonster-summerdiscount

SMONSTER Kit & CLUB Membership - DevLog # 02
https://youtu.be/YEcUttWeQdY

SMONSTER Kit & CLUB Membership - DevLog # 01
https://youtu.be/2tU06E22zU0



------------------
--- KEYMAPPING ---
------------------

======> Main Keymapping are stored in this file in kit folder:
SMO_UV_Keymap.CFG in kit folder

--> when Mouse over UV View:
Shift + Q

--> when Mouse over 3D View:
Q



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
https://community.foundry.com/discuss/topic/152258

Best regards, Franck.