# python
import lx
import modo
import sys

python_majorver = sys.version_info.major
# print('the Highest version number 2 for 2.7 release / 3 for 3.7 release')
# print(python_majorver)

if python_majorver == 2 :
    # print("do something for 2.X code")
    from smodule.commander import SmoCommanderClass
elif python_majorver >= 3 :
    # print("do something for 3.X code")
    from smodule.commander.SMO_Commander import SmoCommanderClass


SMO_GC_151_HOTKEYS = [
    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", ".itemMode", "tool.set channel.haul on"]
        ],
        "key": "c",
        "command": "tool.set channel.haul on",
        "name": "GAME CONTENT: Channel Haul",
        "info": "C  ---  ItemMode"
    },

    {
        "contexts": [
            ["view3DOverlay3D", "(stateless)", ".anywhere", ".componentMode", "tool.set edge.knife on"]
        ],
        "key": "c",
        "command": "tool.set edge.knife on",
        "name": "GAME CONTENT: Edge Knife",
        "info": "C  ---  ComponentMode"
    },

    {
        "contexts": [
            ["view3DOverlay3D", "(stateless)", ".anywhere", ".componentMode", "tool.set poly.knife on"]
        ],
        "key": "shift-c",
        "command": "tool.set poly.knife on",
        "name": "GAME CONTENT: Polygon Knife",
        "info": "Shift C  ---  ComponentMode"
    },

    {
        "contexts": [
            ["view3DOverlay3D", "(stateless)", ".anywhere", ".componentMode", "tool.set poly.loopSlice on"]
        ],
        "key": "alt-c",
        "command": "tool.set poly.loopSlice on",
        "name": "GAME CONTENT: Loop Slice",
        "info": "Alt C  ---  ComponentMode"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {MiniProps:sheet} mini lockProficiency:true"]
        ],
        "key": "shift-space",
        "command": "attr.formPopover {MiniProps:sheet} mini lockProficiency:true",
        "name": "GAME CONTENT: Mini-Properties Popover",
        "info": "Shift Spacebar"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "select.nextMode"]
        ],
        "key": "space",
        "command": "select.nextMode",
        "name": "GAME CONTENT: Original SpaceBar behaviour",
        "info": "Spacebar"
    }

]

# max = len(SMO_GC_151_HOTKEYS)
# lx.out(max)


class SMO_GC_151_KeymapCmdClass(SmoCommanderClass):
    def commander_arguments(self):
        args = []
        for n, hotkey in enumerate(SMO_GC_151_HOTKEYS):
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

        for n, hotkey in enumerate(SMO_GC_151_HOTKEYS):
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

lx.bless(SMO_GC_151_KeymapCmdClass, "smo.GC.151.MapDefaultHotkeys")


class RemoveSMO_GC_151_KeymapCmdClass(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        for hotkey in SMO_GC_151_HOTKEYS:
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

        modo.dialogs.alert("Reverted SMO GAME CONTENT: EXTRA Hotkeys", "Reverted %s SMO GAME CONTENT: EXTRA hotkeys to defaults." % len(SMO_GC_151_HOTKEYS))

lx.bless(RemoveSMO_GC_151_KeymapCmdClass, "smo.GC.151.UnmapDefaultHotkeys")


class ClearSMO_GC_151_KeymapCmdClass(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        for hotkey in SMO_GC_151_HOTKEYS:
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

        modo.dialogs.alert("Cleared SMO GAME CONTENT: EXTRA Hotkeys", "Cleared %s SMO GAME CONTENT: EXTRA hotkeys attribution." % len(SMO_GC_151_HOTKEYS))

lx.bless(ClearSMO_GC_151_KeymapCmdClass, "smo.GC.151.ClearHotkeys")
