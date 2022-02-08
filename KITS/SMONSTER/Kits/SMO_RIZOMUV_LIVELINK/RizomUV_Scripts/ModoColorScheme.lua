---
--- Created by Franck Elisabeth.
---
-- Show the Preferences Window
ZomSet({Path="Vars.UI.Display.DialogPreferencesShown", Value=true})

-- Define Color settings
ZomSet({Path="Prefs.Viewport.Colors.Background3DUp", Value={0.258824, 0.258824, 0.258824}})
ZomSet({Path="Prefs.Viewport.Colors.Background3DLow", Value={0.258824, 0.258824, 0.258824}})
ZomSet({Path="Prefs.Viewport.Colors.Selected", Value={0.956863, 0.611765, 0.109804}})
ZomSet({Path="Prefs.Viewport.Colors.MeshBorders", Value={1, 0.137255, 0.352941}})
ZomSet({Path="Prefs.UI.Color.Background", Value={0.258824, 0.258824, 0.258824}})
ZomSet({Path="Prefs.UI.Color.Foreground", Value={0.745098, 0.745098, 0.745098}})
ZomSet({Path="Prefs.Viewport.Colors.MeshWireOverPolys", Value={0, 0, 0}})

-- Save the Preferences and Close the Prefs Window
ZomSavePreferences(none)
ZomSet({Path="Vars.UI.Display.DialogPreferencesShown", Value=false})