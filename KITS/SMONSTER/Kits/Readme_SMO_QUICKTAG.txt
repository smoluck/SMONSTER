Hi. Everyone

----------------------
--- UPDATE LOG ---
----------------------
- 2.50 -
        • Introduced functions to process the color ID attribution Scene Wide and / or even By Mesh Islands (Polygon Continuity)
        • New Command -->	smo.QT.Batch.SetSelSetColorIDRandomConstant	(Set a random Diffuse Color override using Selection Set (polygons) and Constant item. It can runs over Selected Meshes or SceneWide, By Items or by Polygon Islands.)
        • New Command -->	smo.QT.SetSelSetColorIDByMeshIslands		(Set a Diffuse Color override using Selection Set (polygons) on the selected Mesh Layers by Polygons Continuity (Islands). Named the new Mat using "ColorID" as Prefix.)
        • Bugfix on the main command that where not processing the data correctly with specific user scene behavior.


- 2.00 -
        • Whole new commands added:
                • Set ColorID (by SelectionSet and Constant item override)	---> For ColorID Bakes from LowPoly.
							---> That system doesn't mess up the Material attribution and only add modification via Constant item override and Poly SelectionSet.
							---> Those resulting Meshes can be exported as FBX and Retain Color in Diffuse.
							---> ColorID tags are unique Scenewise and MeshWise, so now you can't have one polygon that share more than one ColorID. It prevent layout issue in Shader Tree.

                • Set ColorID (by Material Tags) 			---> For ColorID Bakes from HighPoly.
							---> Usually outside of Modo, like in Substance Painter or Marmoset Toolbag.
							---> Those resulting Meshes can be exported as FBX and Retain Color in Diffuse.

        • You can recall any existing Color ID you create to override existing one, via a Gang Menu of 17 Color ID Presets (from 0 to 16)
        • You can assign any existing Color ID by a User input value in a Pop window. 
        • Thanks to user feedback, i've set the first 0 to 16 ColorID with ItemColorCoding inside the ShaderTree, as well as fixed colors.
        • Passed ID #16, it will create random Color each time you create a new one.

- 1.50 -
        • Now ColorID are unique Meshwise, so now you can't have one polygon that share more than one ColorID Override. It prevent layout issue.
        • You can recall any Color ID you create to override existing one, via a Gang Menu of 17 Color ID (from 0 to 16)
        • Thanks to user feedback, i've set the first 0 to 16 ColorID with ColorCoding inside the ShaderTree, as well as fixed colors.
        • Passed ID 16, it will create random Color each time you create a new one.

- 1.30 -
        • Added Bugfix for SetColorID by Selection Set

- 1.20 -
        • Added the Quick Tag - Set ColorID command to polygons




------------------
----- VIDEOS -----
------------------

Overview of The Kit:
https://youtu.be/Am6Up0m3pxM

Overview of The Kit by William Vaughan:
https://youtu.be/-dPky3CjeFk



------------------
--- KEYMAPPING ---
------------------

--> QuickTag Pie-Menu available via
"Ctrl - Alt - T" (on PC)      OR     "Cmd - Alt - T" (on Mac)



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
https://community.foundry.com/discuss/topic/150217
and
https://www.pixelfondue.com/blog/2019/11/19/free-smo-math-tools-kit

Best regards, Franck.