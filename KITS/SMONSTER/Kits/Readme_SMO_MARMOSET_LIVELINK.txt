------------------
--- UPDATE LOG ---
------------------
- 2.70 -
        • Bugfix to Marmoset LL to support Material on export.
        • Reformatting SMO_Marmoset_LL_VarData.smo file to indented json for better debug.
        • Adding a time sleep to give some space for map initialize.
        • Used "with XX as f" technique for file writing/close for optimization

- 2.60 -
        • Bugfix on JSON module with Modo (if the Python version choosen was set to 3.9).
          The Exports of variable will now be exchanged and processed correctly in Marmoset.

- 2.50 -
        • Added option to Auto bake AOF (Floor) map (only available in Marmoset Toolbag 4.03)
        • Added option to define AO/Thickness RaySample count in preferences "Bake settings" --> (128 , 256, 512, 1024, 2048)
        • Added option to define PerPixelSampling count in preferences "Bake settings" --> (1X , 4X, 16X)
        • Maps list completely driven by Preferences in Modo to save out unwanted maps to be written in bake folder.

- 2.20 -
        • New Function to put automatically HighPoly Meshes layers in a dedicated Group (Groups Tab) via Set Bake Pairs Command. 

- 2.10 -
        • Compatibility with Modo 15.X and minor bugfix.
        • Now option to Create and Set automatically a Mikk Tangent Space map at export.
        • Added a Direct Link to their respective Website under the Tail Menus

- 2.00 -
        • Bugfix and Support now for HighPoly created via MehsFusion and/or Meshops setup. Smonster now Freeze the result for export, but preserve the scene state.

- 1.90 -
        • All new Input Remapping Menu to manage your Hotkeys from all Smonster's kits.

- 1.80 -
        • Automatic Bake at data load.
        • Automatically close Marmoset after Bake is finished
        • Automatically save a Marmoset Scene file as backup of the current Data processed
        • Bugfix on Bake File Output that was asking to user to create the file. 
        • Added Item Index Style Prefs to be sure the Marmoset and Bake Renaming will work by using Underscore system.
        • Now 4 Output File format type are supported ( PSD , JPG , TGA, PNG )
        • Now Posibility to define your own Baked File Name Prefix for the bakes.
        • Baked File Name Prefix Presets:
                3 Presets available and more to come. (SMOLUCK / Substance Painter Default / Vladimir Leleiva)
        • Now Ability to define your Normal Map workflow. OpenGL to DirectX or OpenGL to OpenGL

- 1.50 -
        • Now all necesarry Modo data and settings are sent to Marmoset.
        • New Folder organization. Subfolder in temp folder using Scene name as well as Subfolder in Scene path if choosen.
        • Added support for Material ID / Albedo from materials / UV Island ID.
        • Resolution of bakes can be set in Modo now

- 1.40 -
        • New Folder organization. Subfolder in temp folder using Scene name ads well as Subfolder in Scene path if choosen.

- 1.30 -
        • Rebuild the command from scratch to make it more flexible and robust.
        • Automatic export of Low / High / Cage meshes to setup bakes in Toolbag and get back the textures in Modo to check the result.
        • Automatic Freeze of the Higpoly Subdiv or Catmul-Clark Polys on export.

- 0.9 - Beta Release


------------------
----- VIDEOS -----
------------------

PLAYLIST:
Overview of the Kit:
https://youtu.be/2Tq6XeEh9ug


------------------
--- DISCLAIMER ---
------------------

You need at least Modo 13.0 to run 100 % of the scripts included.
As usual if you find a bug, please reach me out on SNS and i will do my best to help you and fix this.

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
https://community.foundry.com/discuss/topic/144251

Best regards, Franck.

