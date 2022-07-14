# python
import lx, modo, sys
python_majorver = sys.version_info.major
# print('the Highest version number 2 for 2.7 release / 3 for 3.7 release')
# print(python_majorver)

if python_majorver == 2 :
    # print("do something for 2.X code")
    from smodule.commander import SmoCommanderClass
elif python_majorver >= 3 :
    # print("do something for 3.X code")
    from smodule.commander.SMO_Commander import SmoCommanderClass


SMO_GC_EXTRA_HOTKEYS = [
    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "@kit_SMO_GAME_CONTENT:MacroSmoluck/Unbevel/SMO_UnbevelPolyLoops.py 1"]
        ],
        "key": "ctrl-shift-k",
        "command": "smo.GC.UnbevelLoops 1",
        "name": "GAME CONTENT: Unbevel Polyloops",
        "info": "Ctrl Shift K"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "@kit_SMO_GAME_CONTENT:MacroSmoluck/Unbevel/SMO_UnbevelPolyLoops.py 0"]
        ],
        "key": "ctrl-k",
        "command": "smo.GC.UnbevelLoops 0",
        "name": "GAME CONTENT: Unbevel Polyloops Corner mode",
        "info": "Ctrl K"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", ".componentMode", "smo.GC.Unbevel"]
        ],
        "key": "ctrl-u",
        "command": "smo.GC.Unbevel",
        "name": "GAME CONTENT: Unbevel Edges",
        "info": "Ctrl U  ---  ComponentMode"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", ".componentMode", "smo.GC.UnbevelRing"]
        ],
        "key": "ctrl-shift-u",
        "command": "smo.GC.UnbevelRing",
        "name": "GAME CONTENT: Unbevel Edges Ring",
        "info": "Ctrl Shift U  ---  ComponentMode"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMONSTER_SENECA_SUPERTAUT:sheet}"]
        ],
        "key": "ctrl-alt-l",
        "command": "attr.formPopover {SMONSTER_SENECA_SUPERTAUT:sheet}",
        "name": "GAME CONTENT: Seneca SuperTaut Pie Menu",
        "info": "Ctrl Alt L"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", ".componentMode", "@{kit_SMO_GAME_CONTENT:MacroSmoluck/Basic/SMO_BAS_JoinVertex.LXM}"]
        ],
        "key": "ctrl-alt-w",
        "command": "@{kit_SMO_GAME_CONTENT:MacroSmoluck/Basic/SMO_BAS_JoinVertex.LXM}",
        "name": "GAME CONTENT: JoinVertex (Weld)",
        "info": "Ctrl Alt W  ---  ComponentMode"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", ".componentMode", "@AddBoundary.py"]
        ],
        "key": "ctrl-alt-top2",
        "command": "@AddBoundary.py",
        "name": "GAME CONTENT: Select Boundary Edge of selected Polygon",
        "info": "Ctrl Alt 2  ---  ComponentMode"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "macro.replayRecorded 1"]
        ],
        "key": "ctrl-alt-r",
        "command": "macro.replayRecorded 1",
        "name": "GAME CONTENT: Replay last Macro",
        "info": "Ctrl Alt R"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "item.duplicate false all:true mods:false"]
        ],
        "key": "ctrl-alt-shift-d",
        "command": "item.duplicate false all:true mods:false",
        "name": "GAME CONTENT: Duplicate Item",
        "info": "Ctrl Alt Shift D"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "@{kit_SMO_GAME_CONTENT:MacroSmoluck/Basic/SMO_BAS_SetupColorScheme_ViewPortPref.LXM}"]
        ],
        "key": "ctrl-alt-top3",
        "command": "@{kit_SMO_GAME_CONTENT:MacroSmoluck/Basic/SMO_BAS_SetupColorScheme_ViewPortPref.LXM}",
        "name": "GAME CONTENT: Set SMO Viewport Preset",
        "info": "Ctrl Alt 3"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "edge.remove true"]
        ],
        "key": "ctrl-delete",
        "command": "edge.remove true",
        "name": "GAME CONTENT: Delete Edge but Keep Vertex",
        "info": "Ctrl Del"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "view3d.presetload AVP_Game"]
        ],
        "key": "numeric6",
        "command": "smo.GC.LoadViewportPreset 1",
        "name": "GAME CONTENT: Use AVP Game Shaded (instead of Reflection)",
        "info": "Numpad 6"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "smo.GC.Display.CycleMatCap 0"]
        ],
        "key": "ctrl-numeric6",
        "command": "smo.GC.Display.CycleMatCap 0",
        "name": "GAME CONTENT: Use AVP and Cycle Forward through SMONSTER Matcap Library",
        "info": "Ctrl Numpad 6"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "smo.GC.Display.CycleMatCap 1"]
        ],
        "key": "ctrl-alt-numeric6",
        "command": "smo.GC.Display.CycleMatCap 1",
        "name": "GAME CONTENT: Use AVP and Cycle Backward through SMONSTER Matcap Library",
        "info": "Ctrl Alt Numpad 6"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "tool.set xfrm.push on"]
        ],
        "key": "ctrl-alt-p",
        "command": "tool.set xfrm.push on",
        "name": "GAME CONTENT: Push Tool",
        "info": "Ctrl Alt P"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "poly.setPart"]
        ],
        "key": "alt-shift-p",
        "command": "poly.setPart",
        "name": "GAME CONTENT: Polygon Set Part",
        "info": "Alt Shift P"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "view3d.gameInputMode"]
        ],
        "key": "ctrl-alt-shift-g",
        "command": "view3d.gameInputMode",
        "name": "GAME CONTENT: Switch to Game Mode View",
        "info": "Ctrl Alt Shift G"
    },

    {
        "contexts": [
            ["view3DSelect", "(stateless)", "polygon", "(contextless)", "@{kit_SMO_GAME_CONTENT:MacroSmoluck/Modeling/SMO_MOD_PolyBoundaryEdgeWeight.LXM}"]
        ],
        "key": "ctrl-alt-e",
        "command": "@{kit_SMO_GAME_CONTENT:MacroSmoluck/Modeling/SMO_MOD_PolyBoundaryEdgeWeight.LXM}",
        "name": "GAME CONTENT: HardEdgeWeight from Poly",
        "info": "Ctrl Alt E  ---  PolygonMode in 3D Viewport"
    },

    {
        "contexts": [
            ["view3DSelect", "(stateless)", "edge", "(contextless)", "@{kit_SMO_GAME_CONTENT:MacroSmoluck/Modeling/SMO_MOD_EdgeWeight.LXM}"]
        ],
        "key": "ctrl-alt-e",
        "command": "@{kit_SMO_GAME_CONTENT:MacroSmoluck/Modeling/SMO_MOD_EdgeWeight.LXM}",
        "name": "GAME CONTENT: HardEdgeWeight from Edge",
        "info": "Ctrl Alt E  ---  EdgeMode in 3D Viewport"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", ".componentMode", "tool.set edge.bridge on"]
        ],
        "key": "ctrl-shift-b",
        "command": "tool.set edge.bridge on",
        "name": "GAME CONTENT: Bridge Edges",
        "info": "Ctrl Shift B  ---  ComponentMode"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "glocio.toggle true"]
        ],
        "key": "ctrl-alt-top1",
        "command": "glocio.toggle true",
        "name": "GAME CONTENT: Toggle the Color Correct in OpenGL Mode",
        "info": "Ctrl Alt 1"
    }

]

# max = len(SMO_GC_EXTRA_HOTKEYS)
# lx.out(max)


class SMO_GC_EXTRA_KeymapCmdClass(SmoCommanderClass):
    def commander_arguments(self):
        args = []
        for n, hotkey in enumerate(SMO_GC_EXTRA_HOTKEYS):
            args.append({
                'name':str(n),
                'label':"%s \x03(c:25132927)(%s)" % (hotkey['name'], hotkey['info']),
                'datatype':'boolean',
                'default':False
            })
        return args

    def commander_execute(self, msg, flags):
        m = len([i for i in self.commander_args().items() if i])

        # Old solution from Python 2.7 --> iteritems()
        # m = len([i for i in self.commander_args().iteritems() if i])

        dialog_serv = lx.service.StdDialog()
        monitor = dialog_serv.MonitorAllocate('Mapping Hotkeys...')
        monitor.Initialize(m)

        for n, hotkey in enumerate(SMO_GC_EXTRA_HOTKEYS):
            monitor.Increment(1)
            if not self.commander_arg_value(n):
                continue
            command = hotkey["command"]
            key = hotkey["key"]

            for context_list in hotkey["contexts"]:
                mapping = context_list[0]
                state = context_list[1]
                region = context_list[2]
                context = context_list[3]

                try:
                    lx.eval('!cmds.mapKey {%s} {%s} {%s} {%s} {%s} {%s}' % (key, command, mapping, state, region, context))
                except:
                    lx.out("Failed to set '%s' to '%s'." % (command, key))

        dialog_serv.MonitorRelease()
        # modo.dialogs.alert("Mapped Smonster Hotkeys", "Mapped %s Smonster hotkeys. See Help > Smonster Hotkey Reference" % n)

lx.bless(SMO_GC_EXTRA_KeymapCmdClass, "smo.GC.EXTRA.MapDefaultHotkeys")


class RemoveSMO_GC_EXTRA_KeymapCmdClass(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        for hotkey in SMO_GC_EXTRA_HOTKEYS:
            key = hotkey["key"]

            for context_list in hotkey["contexts"]:
                mapping = context_list[0]
                state = context_list[1]
                region = context_list[2]
                context = context_list[3]
                default = context_list[4]

                if default is None:
                    try:
                        lx.eval('!cmds.clearKey {%s} {%s} {%s} {%s} {%s}' % (key, mapping, state, region, context))
                    except:
                        lx.out("Could not clear mapping for '%s'." % key)
                else:
                    try:
                        lx.eval('!cmds.mapKey {%s} {%s} {%s} {%s} {%s} {%s}' % (key, default, mapping, state, region, context))
                    except:
                        lx.out("Could not set '%s' to '%s'." % (default, key))

        modo.dialogs.alert("Reverted SMO GAME CONTENT: EXTRA Hotkeys", "Reverted %s SMO GAME CONTENT: EXTRA hotkeys to defaults." % len(SMO_GC_EXTRA_HOTKEYS))

lx.bless(RemoveSMO_GC_EXTRA_KeymapCmdClass, "smo.GC.EXTRA.UnmapDefaultHotkeys")


class ClearSMO_GC_EXTRA_KeymapCmdClass(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        for hotkey in SMO_GC_EXTRA_HOTKEYS:
            key = hotkey["key"]

            for context_list in hotkey["contexts"]:
                mapping = context_list[0]
                state = context_list[1]
                region = context_list[2]
                context = context_list[3]
                default = None

                # Setting the Default state to None in order to Clear all the Keymaps
                if default is None:
                    try:
                        lx.eval('!cmds.clearKey {%s} {%s} {%s} {%s} {%s}' % (key, mapping, state, region, context))
                    except:
                        lx.out("Could not clear mapping for '%s'." % key)

        modo.dialogs.alert("Cleared SMO GAME CONTENT: EXTRA Hotkeys", "Cleared %s SMO GAME CONTENT: EXTRA hotkeys attribution." % len(SMO_GC_EXTRA_HOTKEYS))

lx.bless(ClearSMO_GC_EXTRA_KeymapCmdClass, "smo.GC.EXTRA.ClearHotkeys")
