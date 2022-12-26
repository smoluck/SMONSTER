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

SMO_CAD_TOOLS_HOTKEYS = [
    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_CAD_TOOLS_SH:sheet}"]
        ],
        "key": "ctrl-alt-h",
        "command": "attr.formPopover {SMO_CAD_TOOLS_SH:sheet}",
        "name": "CAD TOOLS: Pie Menu",
        "info": "Ctrl Alt H"
    }, {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "smo.CAD.StarTripleFlat"]
        ],
        "key": "alt-top5",
        "command": "smo.CAD.StarTripleFlat",
        "name": "CAD TOOLS: Star Triple Flat",
        "info": "Alt 5"
    }, {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "smo.CAD.RebuildRadialFlat"]
        ],
        "key": "alt-top6",
        "command": "smo.CAD.RebuildRadialFlat",
        "name": "CAD TOOLS: Rebuild Radial Flat",
        "info": "Alt 6"
    }, {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "smo.CAD.RebuildRadialTube"]
        ],
        "key": "alt-top7",
        "command": "smo.CAD.RebuildRadialTube",
        "name": "CAD TOOLS: Rebuild Radial Tube",
        "info": "Alt 7"
    }
]

# max = len(SMO_CAD_TOOLS_HOTKEYS)
# lx.out(max)


class SMO_CAD_KeymapCmdClass(SmoCommanderClass):
    def commander_arguments(self):
        args = []
        for n, hotkey in enumerate(SMO_CAD_TOOLS_HOTKEYS):
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

        for n, hotkey in enumerate(SMO_CAD_TOOLS_HOTKEYS):
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
        # modo.dialogs.alert("Mapped SMO CAD TOOLS Hotkeys", "Mapped %s SMO CAD TOOLS hotkeys. See Help > Smonster Hotkey Reference" % n)

lx.bless(SMO_CAD_KeymapCmdClass, "smo.CAD.MapDefaultHotkeys")


class RemoveSMO_CAD_KeymapCmdClass(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        for hotkey in SMO_CAD_TOOLS_HOTKEYS:
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

        modo.dialogs.alert("Reverted SMO CAD TOOLS Hotkeys", "Reverted %s SMO CAD TOOLS hotkeys to defaults." % len(SMO_CAD_TOOLS_HOTKEYS))

lx.bless(RemoveSMO_CAD_KeymapCmdClass, "smo.CAD.UnmapDefaultHotkeys")


class ClearSMO_CAD_KeymapCmdClass(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        for hotkey in SMO_CAD_TOOLS_HOTKEYS:
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

        modo.dialogs.alert("Cleared SMO CAD TOOLS Hotkeys", "Cleared %s SMO CAD TOOLS hotkeys attribution." % len(SMO_CAD_TOOLS_HOTKEYS))

lx.bless(ClearSMO_CAD_KeymapCmdClass, "smo.CAD.ClearHotkeys")