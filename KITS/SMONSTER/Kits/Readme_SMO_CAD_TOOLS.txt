----------------------
--- UPDATE LOG ---
----------------------
- 3.90 -
	• smo.CAD.CopyCutAsChildOfCurrentMesh now rename the new mesh by the source name.

- 3.70 -
        • Added Option for Rebuild Polystrip to work on Circle (Closed Loop). (using 2nd argument to define if it's working for a closed Polystrip)

- 3.60 -
        • Bugfix to get the focus on Mesh Source if there is only one displayed in Isolate Mode (instead of fiting the viewport on both Instances and Source Meshes).
        • BugFix Missing Icons on Merge CoPlanarPoly Pie Menu.

- 3.50 -
        • Added CAD Fix Rotation Transform Order Cmd to convert all Rotation Transforms from "n" order to XYZ Order without loosing the item Position / Rotation in space.
        • MergeCoplanar Poly Forms in Context Menu.
        • Bugfix on CAD IsolateItemAndInstances. Now works in all conditions (From Selected (Meshes) or (Meshes + Instances) or (Instances)).

- 3.40 -
        • RebuildWithCylinder Side Count by User was added in the Pie Menus (via Axes Icons).
        • Rebevel now support Reference System.
        • Rebevel Bugfix when Meshes that got triangle Poly in the surrounding area around The processed selection.
        • Smart Rebuild With Cylinder Added for better shape handling (Regular Radius Support).  (RebuildWithCylinder command have been removed).
        • Copy / Cut to Child Mesh command Rework with Select Coplanar Modes and dedicated Pie Menu / Icons

- 3.20 -
        • Bugfix on Rebevel.
        • Rebevel / RebuildPolystrip now support Item Auto Selection in Component Mode (if you wasn't selecting the mesh before it will select it for you).

- 3.10 -
        • New Command: Rebuild Closed Polystrip.
        • New Command: CopySelectionAsChildOfCurrentMesh.
        • New Command: Merge CoPlanarPoly to replace old system on "Delete In... menu".
        • RebuildWithCube and RebuildWithCylinder Open / Closed / Hole script now support Reference System workflow.
        • RebuildWithCube and RebuildWithCylinder Open / Closed / Hole now support Item Auto Selection in Component Mode (if you wasn't selecting the mesh before it will select it for you).
        • Rebevel - RebuildWithCylinder / RebuildWithCube are now Wrapped Commands.
        • MergeCoplanarPoly Update on Forms.
        • Bugfix: Rebevel was lefting over an edge selection set, now it doesn't left over things (leading to better compatibility).
        • Bugfix: Delete Selection Set Item for RebuildPolyStrip / RebuildCylinder / Rebevel (Clear Tag).

- 2.90 -
        • New Command: Rebuild Closed Polystrip.
        • New Command: CopySelectionAsChildOfCurrentMesh.
        • New Command: Merge CoPlanarPoly to replace old system on "Delete In... menu".
        • RebuildWithCylinder Open / Closed / Hole script now support Reference System workflow.
        • RebuildWithCylinder Open / Closed / Hole now support Item Auto Selection in Component Mode (if you wasn't selecting the mesh before it will select it for you).
        • Rebevel - RebuildWithCylinder are now Wrapped Commands.
        • bugfix: Rebevel was lefting over an edge selection set, now it doesn't left over things (leading to better compatibility).

- 2.70 -
        • Bugfix when user was using their own Copy / Paste / Deselect mode in preferences.

- 2.60 -
        • Star Triple Flat (Reference System Support)
        • Rebuild Radial Flat (Reference System Support)
        • Rebuild Radial Tube (Reference System Support)

- 2.50 -
        • Switched CAD Tools / UV / VeNom Kits from Lazy Select (Seneca Menard scripts) workflow to Built-in Select CoPlanar Polygons command Introduced in recent release of Modo.
            • Better Performance in mentioned Kits.
            • No More headache on Initialize CAD / UV / Venom kit procedure. (Runs smoothly right after the installation.)

- 2.30 -
        • 3 New Mouse Over Commands
            • Star Triple Flat
            • Rebuild Radial Flat
            • Rebuild Radial Tube

- 2.10 -
        • added the Rebuild Polystrip Commands and Menus.
            • 2 Methods are available. (Select a Polygon Selection and 2 partial Edge loop to define the shape.)
                • Regular rebuild
                • Normalized Width

- 1.95 -
        • Updated Icons.

- 1.90 -
        • Compatibility with Modo 15.X and minor bugfix.

- 1.80 -
        • All new Input Remapping Menu to manage your Hotkeys from all Smonster's kits.

- 1.75 -
        • Compatibility Bugfix following 14.1 release.

- 1.70 -
        • Added various new scripts and bugfix.
        • More to come soon via videos and txt description.

- 1.57 -
        • Added the new Copy/Cut Script Pie Menu.
        • Cleaned up the Script folder structure.
        • Various bugfix and improvement.

- 1.52 -
        • Rebevel Now is fully Undoable.
        • Fixed an issue in the forms Files: Missing link in Pie Menu and Menu bar for Rebevel.

- 1.50 -
        • Solved a bug affecting Python Scripts that where using a different User preferences behavior on Copy/Paste settings.

- 1.47 -
        • Modo 13.2 Support.
        • Mode Tail Kit Button added.
        • Now with an option to define your own keymapping by Holding the Ctrl key on the Mode Tail Kit Button. 

- 1.30 -

        • Added the Help alternate command to most commands in the Main CAD Menu and other PieMenu.
        • To activate it, simply hold Shift key and click on any commands.
        • Except for pie menu, where this command is represented by a "?", the help is available that way.

        • Added the Audio Notification alternate command.
        • You'll access to it by holding the Ctrl (Cmd) key and cliking on the command in the Main CAD Menu. 
        • It plays a 5 sec music at the end of the script process.
        • I's helpful for high detailed CAD Models where the cleanup Process might take few minutes to complete.



--------------------
----- VIDEOS -----
--------------------

PLAYLIST:
https://www.youtube.com/playlist?list=PLN8BUs-BSLgkRDpgZqIuR5Acu6HEBA0Lx

Overview of the Kit:
https://youtu.be/UYQ2ugdTC4c

Installation:
https://youtu.be/AZueyjN5JQw

Rebevel tool in depth review:
https://youtu.be/L7sAAf9uL6g

CAD Tools Benchmark:
https://youtu.be/zeK736RmjrE



--------------------------Upgrade Instruction:--------------------------
If you already have the kit installed,
create a backup of the folder as Zip or any archive,
just in case you 'll have any issue with the new one.
The zip file will not be loaded at modo start.

Then delete the folder SMO_CAD_TOOLS
Open Modo and drag n drop the new LPK file in it.
Restart Modo.

--------------------------Installation Instruction:--------------------------
After downloading the Zip file, please follow those instructions:

1 ---> Open Modo and Drag and Drop the LPK file into Modo Window. then Close it, and reopen it.
2 ---> Now you can start using the kit.



----------------------
--- KEYMAPPING ---
----------------------

======> Main Keymapping are stored in this file in kit folder:
SMO_CAD_TOOLS_Keymap.cfg

It's a Pie menu , you'll access to it by pressing:

Ctr + Alt + H (on PC)
or
Cmd + Alt + H (on Mac)



---------------------
--- DISCLAIMER ---
---------------------

You need at least Modo 14.1 to run 100 % of the scripts included.
I try to keep compatibility tfrom 13.0 to 14.0.
As usual if you fiond a bug, please reach me out on SNS and i will do my best to help you and fix this.

----------------------------------------------------------------------------
As for every Product / Art piece / Assets that you do, like everyone of us,
please do not share those files, as you didn't want to see your work shared
on internet without your permission.
                 I'm sure you'll understand that point.
----------------------------------------------------------------------------



--------------------
---- CONTACT ----
--------------------

on Twitter:
https://twitter.com/sm0luck

on the Foundry Slack server:
foundry-modo.slack.com

on the Foundry Forums:
https://community.foundry.com/discuss/topic/143650/modo-i-cad-tools-kit
and
https://community.foundry.com/discuss/topic/152258

Best regards, Franck.