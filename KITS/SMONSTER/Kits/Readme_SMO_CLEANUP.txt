----------------------
--- UPDATE LOG ---
----------------------
- 2.55 -
        • smo.cleanup.UpdateMaterial - Bugfix for material definition change between Mood 15.1 and 15.2

- 2.50 -
        • PopUp menu updated
        • New Command -->	smo.CLEANUP.ConvertAllSolidWorksShape
                    (Search for all Solidworks Shape Items in the scene and convert them to regular Meshes. Delete the empty meshes in the process as well.)
        • New Command -->	smo.CLEANUP.CleanupSolidWorksImport
                    (Cleanup SolidWorks Import (from McMaster Website Data) in order to save a new scene with only one Mesh item of the imported asset. It will also convert the VertexNormals Data to HardEdgeWorkflow if needed.)
        • New Command -->	smo.CLEANUP.DelEverythingExceptMeshes
                    • (Select everything in the current scene, except Meshes items and delete all other items / materials. It unparent in place the current Meshes to preserve their position in space in case they were part of a hierarchy.)
        • New Command -->	smo.CLEANUP.RemoveAllPartTags
                    (Check for all Meshes in the current scene remove any part tags in it.)
        • New Command -->	smo.CLEANUP.DelPreTransform
                    (Freeze Scale transform of all meshes in scene but if there is instances, it retain Instances scale to 100 percent or -100 percent as well.)
        • Bugfix smo.CLEANUP.RenameUVMapToDefaultSceneWise - (That command now create an empty UV map if one is missing using Default UVMap name from Preferences)

- 2.00 -
        • Added Rename Vertex Normal Map by Modo Default name for imported FBX files --> ( FBX_normals)
        • Changed the Popup menu UI layout for better functions discoverability

- 1.80 -
        • Added Rename All Instance by Source Mesh Name command.

- 1.70 -
        • Bugfix when user was using their own Copy / Paste / Deselect mode in preferences.

- 1.65 -
        • Added the dedicated Icon

- 1.60 -
        • Compatibility with Modo 15.X and minor bugfix.

- 1.50 -
        • All new Input Remapping Menu to manage your Hotkeys from all Smonster's kits.

- 1.40 -
        • Added cleanup function smo.CLEANUP.ConvertItemIndexStyleSceneWise and updated smo.CLEANUP.FullAutoCleanup to support it.

- 1.30 -
        • BugFix and Added User prefs string to search and replace UVMap Name from Source (string) to Target (string)

- 1.20 -
        • Changed all CLEANUP Commands to use User defined Preferences. (CLEANUP kit)
        • Added the FullAuto Cleanup Command to batch Cleanup based on User Prefs. (CLEANUP kit)

- 1.10 -
        • Added the Kit to the Preferences to let you define the Cleanup Batch Command.



------------------
----- VIDEOS -----
------------------

Overview of The Kit
https://youtu.be/QWgUJvEAJBc



------------------
--- KEYMAPPING ---
------------------

======> Main Keymapping are stored in this file in kit folder:
SMO_CLEANUP_Keymap.CFG

It's a PopOver Menu , you'll access to it by pressing:

Shift + F5
OR
access it via the Game Content Pie Menu under EXPORT tools section.



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