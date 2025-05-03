---
--- Created by Franck Elisabeth.
---

-- Show the Preferences Window
ZomSet({Path="Vars.UI.Display.DialogPreferencesShown", Value=true})

-- Set the UV Texture Cheker map path
-- Path Location is refering to our SMONSTER V2 Folder
ZomLoadGridTexture("C:/ONEDRIVE/GITHUB/SMONSTER/KITS/SMONSTER/Kits/SMO_UV/UVGrid/uvLayoutGrid_4096.png")
ZomSet({Path="Prefs.Viewport.GridTexturePath", Value="C:/ONEDRIVE/GITHUB/SMONSTER/KITS/SMONSTER/Kits/SMO_UV/UVGrid/uvLayoutGrid_4096.png"})

-- Define common settings
ZomSet({Path="Prefs.Viewport.NearPlane", Value=0.001})
ZomSet({Path="Prefs.Viewport.DisplayFPS", Value=true})
ZomSet({Path="Prefs.UI.Display.IslandProperties", Value=true})
ZomSet({Path="Prefs.UI.DisplayPx", Value=true})
-- ZomSet({Path="Prefs.UI.DefaultSceneUnit", Value="m"})

-- Set the Default IDE executable
--ZomSet({Path="Prefs.ExternalTextEditor.Path", Value="C:/Program Files/JetBrains/PyCharm 2020.3/bin/pycharm64.exe"})

-- Set the default FBX release used for Saving. Modo Rizom UV Livelink use FBX 2013 for Data exchange
-- and Disable the AutoSave function as we want to update the same File as the one exported from Modo
ZomSet({Path="Prefs.File.FBX.Version", Value="FBX201300"})
ZomSet({Path="Prefs.AutoSave.Enabled", Value=false})

-- Save the Preferences and Close the Prefs Window
ZomSavePreferences(none)
ZomSet({Path="Vars.UI.Display.DialogPreferencesShown", Value=false})

-- Show off the Packing Tab settings
ZomSet({Path="Prefs.UI.Display.IslandProperties", Value=true})

-- Display the custom Checker Texture on mesh
ZomSet({Path="Vars.Viewport.Viewport3D.Textured", Value=true})
ZomSet({Path="Vars.Viewport.TextureID", Value=1})
ZomSet({Path="Prefs.Script.Language", Value="Python"})


