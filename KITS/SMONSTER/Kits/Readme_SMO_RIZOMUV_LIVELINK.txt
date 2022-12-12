Hi. Everyone


Since 2.2 Release:
======> You ALWAYS need to have SMO_MASTER ans SMONSTER Kit up and running to use the commands in the kit <======


------------------
--- UPDATE LOG ---
------------------
- 2.82 -
        • Bugfix on compilation errors on some platforms (win 11)

- 2.8 -
        • MODO 16.0v3 Support and small bugfix in code
        • Added UV popup menu to the Vertex Maps under Info / Statistics to give access to commands more simply.
        • Bugfix on the smo.LL.RIZOMUV.Basic command that wasn't getting the right fbx settings. It should now export correctly to the user defined path without any issues.

- 2.7 -
        • MODO 16.0v1 Support

- 2.6 -
        • MODO 15.2v2  Support
        • RizomUV 2022.0 Support
        • Bugfix for those who also are using Vertex Normals maps in their workflow. In any case the kit won't update in Modo you could still open the Temp FBX File in order to get back all the data from Materials to VNrm to UV's of course..

- 2.55 -
        • Addition of Pixel Margin / Spacing Mode On in RizomUV Preferences Script.

- 2.5 -
        • MODO 15.1v1  Support
        • RizomUV 2021.0 Support
        • Added support for material at Livelink Export to let you use materials for fast polygon selection in RizomUV

- 2.4 -
        • Bugfix: in case you wasn't exporting Meshes fully triangulated, MODO 15.0vx wasn't getting proper UV data as it was exporting the mesh triangulated instead of preserving the Mesh Topology (Square and Ngons).

- 2.3 -
        • MODO 15.0v1  Support
        • RizomUV 2020.1 Support
        • New Key mapping System (No Hard-coded Keymap, Set Default Keymap by menu, Struggle-Free)
        • Access to SMONSTER Documentation from the Kit itself
        • Access to Rizom Lab Website
        • Various Bugfix

- 2.2 -
        • All new Input Remapping Menu to manage your Hotkeys from all Smonster's kits.

- 2.1 -
        • Fixed an issue where RizomUVLL was exporting the mesh triangulated if you was exporting Triangulated FBX previously using the RizomUV LL commands in the same scene.

- 2.0 -
        • Set path command to directly change the RizomUV Release you want to work with.
	(No need to to edit the Python script, and now you are able to choose the release to work with , without rebooting Modo.)
        • Kit Preferences Menu available in Modo Preferences Window

- 1.9.5 -
        • Bugfix on RizomUV LL to use only FBX 2013 for all Import / Exports from whatever Modo release to fix incompatibility.

- 1.9.0 -
        • MODO 14.0v2 Support and Up
        • RizomUV 2020.0.88 - last BETA Support (Development Build).

- 1.7.0 -
        • MODO 14.0v1 Support
        • RizomUV 2020.0 - BETA Support (Development Build).
        • It may be prompt to crash, as the Dev build is well in development.

- 1.6.0 -
        • RizomUV 2019.1 Support,
        • Fixed an issue related to an incompatibility with other Kits, causing a "RizomUVLL Failed" Error from time to time.

- 1.5.0 -
        • Livelink and Livelink (Save) are now available

	1-> LiveLink:
	You've asked for it a few month ago, but i found the time to manage to do it.
	This is the Real LiveLink.
	(No More PopUp for file destination)

	2-> Livelink (Save) - [Floppy disk icon]
	Here it's the same system as the previous build.
	You can define and store the FBX export in a specific location.

- 1.3.1 -
        • Modo 13.2 Support,
        • Tail Mode Button in the Kit (Top Right button)
        • Via the Tail Button, by Holding Ctrl and click you can now define your own Keymap to launch the livelink.

- 1.2.1 -
        • Modo 13.1 Support,
        • RizomUV 2019.0 Support,
        • New Price ^^

- 1.1.7 -
        • Updated the form structure,
        • Fixed some installation bug,
        • Added a Readme file,
        • Added an Icon to the Pie-menu

- 1.1.6 -
        • Fixing some link issue on few users.

- 1.1.5 -
        • Release as One Action command.


---------------------------
--- UPGRADE INSTRUCTION ---
---------------------------
If you already have the kit installed,
Delete the folder SMO_RizomUV_LiveLink under your Content/Kits folder
Open Modo and drag n drop the new LPK file in it.
Restart Modo.



--------------------------------
--- INSTALLATION INSTRUCTION ---
--------------------------------
After downloading the Zip file, please follow those instructions:

1 ---> Open Modo and Drag and Drop the LPK file into Modo Window. then Close it, and reopen it.

2 ---> Open the Demo scene: TestScene.lxo,
then select the items, then the UV Map in the Vertex Map List
Then run the hotkey: CTRL + ALT + Shift + R

if you run it the first time and have installed RizomUV in a specific Folder,
Modo will ask for the Exe file of RizomUV.
Point to the correct location on your system,
then run the Livelink again.



------------------
----- VIDEOS -----
------------------

https://youtu.be/dttH0GtO-Zg

PLAYLIST:
Overview of the Kit:
https://www.youtube.com/playlist?list=PLN8BUs-BSLgnkUVuJgDnfIexkuzYdsUXG


--- config ---

It's a Pie menu , you'll access to it by pressing:

CTRL + ALT + Shift + R (on PC)
or
CMD + ALT + Shift + R (on Mac)

if you want to change the Hotkey:
	You'll need to edit the hotkey via the Form editor or by editing directly this file:
	SMO_RizomUV_LiveLink\Configs\RizomUV_LiveLink_PieMenu.CFG
OR
	You can do that in Modo Via the Tail Button, by Holding Ctrl and click you can now define your own Keymap to launch the livelink.


------------------
--- DISCLAIMER ---
------------------

(you need at least Modo 13.0v1 to run this kit)

----------------------------------------------------------------------------
As for every Product / Art piece / Assets that you do, like every one of us,
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
