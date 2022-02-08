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


SMO_GC_MAIN_HOTKEYS = [
    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "(none)"]
        ],
        "key": "ctrl-w",
        "command": "(none)",
        "name": "GAME CONTENT: Clear -Close Scene- Modo Default Remapping",
        "info": "Ctrl W"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "(none)"]
        ],
        "key": "ctrl-q",
        "command": "(none)",
        "name": "GAME CONTENT: Clear -Quit Modo- Modo Default Remapping",
        "info": "Ctrl Q"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_GC_MASTER_Pie_SH:sheet}"]
        ],
        "key": "ctrl-q",
        "command": "attr.formPopover {SMO_GC_MASTER_Pie_SH:sheet}",
        "name": "GAME CONTENT: Pie Menu",
        "info": "Ctrl Q"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_GC_MASTER_VMENU_SH:sheet}"]
        ],
        "key": "ctrl-shift-q",
        "command": "attr.formPopover {SMO_GC_MASTER_VMENU_SH:sheet}",
        "name": "GAME CONTENT: Popover Menu",
        "info": "Ctrl Alt Shift Q"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_GC_NORMALS_Pie_SH:sheet}"]
        ],
        "key": "ctrl-alt-f1",
        "command": "attr.formPopover {SMO_GC_NORMALS_Pie_SH:sheet}",
        "name": "GAME CONTENT: Vertex Normals Pie Menu",
        "info": "Ctrl Alt F1"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_GC_SETUP_Pie_SH:sheet}"]
        ],
        "key": "ctrl-alt-f2",
        "command": "attr.formPopover {SMO_GC_SETUP_Pie_SH:sheet}",
        "name": "GAME CONTENT: Setup Pie Menu",
        "info": "Ctrl Alt F2"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_GC_EXPORT_Pie_SH:sheet}"]
        ],
        "key": "ctrl-alt-f3",
        "command": "attr.formPopover {SMO_GC_EXPORT_Pie_SH:sheet}",
        "name": "GAME CONTENT: Export Pie Menu",
        "info": "Ctrl Alt F3"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_GC_SELECT_Pie_SH:sheet}"]
        ],
        "key": "ctrl-alt-f4",
        "command": "attr.formPopover {SMO_GC_SELECT_Pie_SH:sheet}",
        "name": "GAME CONTENT: Select Pie Menu",
        "info": "Ctrl Alt F4"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_GC_MODELING_Pie_SH:sheet}"]
        ],
        "key": "ctrl-alt-f5",
        "command": "attr.formPopover {SMO_GC_MODELING_Pie_SH:sheet}",
        "name": "GAME CONTENT: Modeling Pie Menu",
        "info": "Ctrl Alt F5"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_GC_CLEANING_Pie_SH:sheet}"]
        ],
        "key": "ctrl-alt-f6",
        "command": "attr.formPopover {SMO_GC_CLEANING_Pie_SH:sheet}",
        "name": "GAME CONTENT: Cleaning Pie Menu",
        "info": "Ctrl Alt F6"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_GC_MESHOPS_Pie_SH:sheet}"]
        ],
        "key": "ctrl-alt-f7",
        "command": "attr.formPopover {SMO_GC_MESHOPS_Pie_SH:sheet}",
        "name": "GAME CONTENT: Meshops Pie Menu",
        "info": "Ctrl Alt F7"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_GC_DISPLAY_Pie_SH:sheet}"]
        ],
        "key": "ctrl-alt-f8",
        "command": "attr.formPopover {SMO_GC_DISPLAY_Pie_SH:sheet}",
        "name": "GAME CONTENT: Display Pie Menu",
        "info": "Ctrl Alt F8"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_GC_UV_Pie_SH:sheet}"]
        ],
        "key": "ctrl-alt-f9",
        "command": "attr.formPopover {SMO_GC_UV_Pie_SH:sheet}",
        "name": "GAME CONTENT: UV Pie Menu",
        "info": "Ctrl Alt F9"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_GC_UV_SEAM_Pie_SH:sheet}"]
        ],
        "key": "ctrl-alt-f10",
        "command": "attr.formPopover {SMO_GC_UV_SEAM_Pie_SH:sheet}",
        "name": "GAME CONTENT: UV Seam Pie Menu",
        "info": "Ctrl Alt F10"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_GC_PALETTES_Pie_SH:sheet}"]
        ],
        "key": "ctrl-alt-shift-x",
        "command": "attr.formPopover {SMO_GC_PALETTES_Pie_SH:sheet}",
        "name": "GAME CONTENT: Palettes",
        "info": "Ctrl Alt Shift X"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "item.name"]
        ],
        "key": "enter",
        "command": "item.name",
        "name": "GAME CONTENT: Rename an Item from anywhere",
        "info": "Enter"
    },

    {
        "contexts":[
            ["view3DSelect", "(stateless)", "item", "(contextless)", "attr.formPopover {itemprops:general}"],
            ["shaderTree", "(stateless)", ".anywhere", "(contextless)", None],
            ["deformerList", "(stateless)", ".anywhere", "(contextless)", None],
            ["schematic", "(stateless)", ".anywhere", "(contextless)", None],
            ["meshList", "(stateless)", "meshoperation", "(contextless)", None],
            ["meshList", "(stateless)", "deformName", "(contextless)", None],
            ["meshList", "(stateless)", "chanEffect", "(contextless)", None],
            ["meshList", "(stateless)", "chanModify", "(contextless)", None],
            ["meshList", "(stateless)", "itemModify", "(contextless)", None],
            ["meshList", "(stateless)", "itemRef", "(contextless)", None],
            ["meshList", "(stateless)", "cinemaRef", "(contextless)", None],
            ["meshList", "(stateless)", "cinemaName", "(contextless)", None],
            ["vpgroups", "(stateless)", ".anywhere", "(contextless)", None]
        ],
        "key":"mmb",
        "command":"attr.formPopover {itemprops:general}",
        "name":"GAME CONTENT: Middle Mouse show Item Properties",
        "info": "Middle Mouse Button"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "smo.GC.FullScreenToggle"]
        ],
        "key": "shift-escape",
        "command": "smo.GC.FullScreenToggle",
        "name": "GAME CONTENT: Toggle FullScreen Mode",
        "info": "Shift ESC"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_GC_PieSwitcherBorderToggle:sheet}"]
        ],
        "key": "ctrl-alt-space",
        "command": "attr.formPopover {SMO_GC_PieSwitcherBorderToggle:sheet}",
        "name": "GAME CONTENT: Viewport Border Toggles Pie Menu",
        "info": "Ctrl Alt Space"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", ".componentMode", "attr.formPopover {SMO_CAD_TOOLS_CopyOrCut_PM:sheet}"]
        ],
        "key": "ctrl-shift-c",
        "command": "attr.formPopover {SMO_CAD_TOOLS_CopyOrCut_PM:sheet}",
        "name": "GAME CONTENT: Copy/Paste Pie Menu",
        "info": "Ctrl Shift C  ---  ComponentMode"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "smo.GC.SetNewMaterialSmartRename"]
        ],
        "key": "m",
        "command": "smo.GC.SetNewMaterialSmartRename",
        "name": "GAME CONTENT: Set Smart Material",
        "info": "M"
    }


]

# max = len(SMO_GC_MAIN_HOTKEYS)
# lx.out(max)


class SMO_GC_MAIN_KeymapCmdClass(SmoCommanderClass):
    def commander_arguments(self):
        args = []
        for n, hotkey in enumerate(SMO_GC_MAIN_HOTKEYS):
            args.append({
                'name':str(n),
                'label':"%s \x03(c:25132927)(%s)" % (hotkey['name'], hotkey['info']),
                'datatype':'boolean',
                'default':True
            })
        return args

    def commander_execute(self, msg, flags):
        m = len([i for i in self.commander_args().items() if i])

        # Old solution from Python 2.7 --> iteritems()
        # m = len([i for i in self.commander_args().iteritems() if i])

        dialog_serv = lx.service.StdDialog()
        monitor = dialog_serv.MonitorAllocate('Mapping Hotkeys...')
        monitor.Initialize(m)

        for n, hotkey in enumerate(SMO_GC_MAIN_HOTKEYS):
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

lx.bless(SMO_GC_MAIN_KeymapCmdClass, "smo.GC.MAIN.MapDefaultHotkeys")


class RemoveSMO_GC_MAIN_KeymapCmdClass(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        for hotkey in SMO_GC_MAIN_HOTKEYS:
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

        modo.dialogs.alert("Reverted SMO GAME CONTENT: MAIN Hotkeys", "Reverted %s SMO GAME CONTENT: MAIN hotkeys to defaults." % len(SMO_GC_MAIN_HOTKEYS))

lx.bless(RemoveSMO_GC_MAIN_KeymapCmdClass, "smo.GC.MAIN.UnmapDefaultHotkeys")


class ClearSMO_GC_MAIN_KeymapCmdClass(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        for hotkey in SMO_GC_MAIN_HOTKEYS:
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

        modo.dialogs.alert("Cleared SMO GAME CONTENT: MAIN Hotkeys", "Cleared %s SMO GAME CONTENT: MAIN hotkeys attribution." % len(SMO_GC_MAIN_HOTKEYS))

lx.bless(ClearSMO_GC_MAIN_KeymapCmdClass, "smo.GC.MAIN.ClearHotkeys")
