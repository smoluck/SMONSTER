----------------------
--- UPDATE LOG ---
----------------------
- 4.10 -
        • New Commands and Menu
            • smo.MIFABOMA.FlipSelectedPolys
            Flip the Polygon selection using the Local Axis but with a workplane
            offset to current Selected Polygons.(using Item Axis and Selected Poly Center)

- 3.50 -
        • Improvement and Bugfix on RADIAL ARRAY and MIRROR commands that now support:
                • both Meshes and MeshInstances (instead of only regular Meshes only).
                • Multiple Items selected at once. They will now process duplication over multiple selected items as intended.

- 3.00 -
        • Bugfix for Mirror Tool in Polygon Mode under Modo 15.1 and up. (Invert Polygons option have opposite behavior now)

- 2.90 -
        • Bugfix on forms Pie Menu. Mirror commands "Relative to Parent / Merge" and "Relative To Parent" was inverted. 
        • Bugfix on Mirror commands to Support ReferenceSystem as well as update on VertexNormalMap at once.
        • Bugfix on FlipOnAxis that now also support VertexNormalMap (they update correctly now) when you was using Reference System.

- 2.80 -
        • Bugfix on Radial Array with World Mode in Component Mode
        • FlipOnAxis now support VertexNormalMap and update it.
        • Bugfix on Mirror that wasn't saving user settings.

- 2.70 -
        • Boolean command is now preserving the current visible Items in the viewport when run.

- 2.60 -
        • RADIAL SWEEP (Local) - Process from High Poly Option added (to Rebuild topology from HighPolyMesh Data. Require Edges profile selection and Polygons area to be removed in the process).
        • Added the Preferences link on top of Tail Menu Pop Over.
        • Bugfix when user was using their own Copy / Paste / Deselect mode in preferences.
        • Bugfix on Booleans (that left unwanted Polygon Selection Sets after using the command).

- 2.40 -
        • Reference System Support (when it is defined on current Item in Local Mode and Component Mode)
          and Auto selection Support in Component Mode (if you wasn't selecting the mesh before it will select it for you).
                • Mirror
                • Slice
                • Radial Array
                • Booleans
                • Radial Sweep
                • Flip On Axis

- 2.30 -
        • Bugfix on Radial Sweep Local that wasn't working if the Reference System was already defined.

- 2.20 -
        • Compatibility with Modo 15.X and minor bugfix.
        • Bugfix on Vertical Menu (missing Commands and UserPref )

- 2.10 -
        • All new Input Remapping Menu to manage your Hotkeys from all Smonster's kits.

- 1.95 -
        • Compatibility Bugfix following 14.1 release.

- 1.90 -
        • Bugfix on Radial tools in Item Mode
        • Added  Radial Array by User Count
        • Added  Radial Sweep by User Count
        • Updated the Pie Menus
        • Added a Menu Bar to get access to Cloning preferences in item mode.

- 1.80 -
        • Bugfix on Mirror Pie Menu icons. New icon for "Relative to Parent"

- 1.77 -
        • Bugfix on Mirror pie menu using the new set of icons for Local/World/Relative to Parent.

- 1.75 -
        • Radial Array and Mirror Bugfix (to use the User Values (Clone type and Clone Hierarchy)) 

- 1.70 -
        • Radial Array and Radial Sweep Command Added. (Mode Local / World / Relative to Parent 

- 1.40 -
        • Flip On Axis and Slice Commands Added.

- 1.30 -
        • Added various new scripts and bugfix.
        • More to come soon via videos and txt description.

- 1.20 -
        • Solved a bug affecting Python Scripts that where using a different User preferences behavior on Copy/Paste settings.

- 1.15 -
        • Solved an install issue with the 1.14 lpk file. Missing link to the readme



------------------
----- VIDEOS -----
------------------

PLAYLIST:
https://www.youtube.com/playlist?list=PLN8BUs-BSLgkv_baslLC03YLeJkfgCmWM



------------------
--- KEYMAPPING ---
------------------

======> Main Keymapping are stored in this file in kit folder:
SMOLUCK_MIFABOMA_Keymap.CFG

--> MI-FA-BO-MA Pie-Menu: MIRROR -/- FALLOFF -/- BOOLS -/- MATCH -/- RADIAL SWEEP -/- RADIAL ARRAY -/- FLIP ON AXIS -/- SLICE ON AXIS
Ctr + ALT + M (on PC)      OR     Cmd + Alt + M (on Mac)



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
https://community.foundry.com/discuss/topic/149965/smo-mifaboma-kit-v1-11-for-modo-902-to-13-2-2019-11-10

Best regards, Franck.