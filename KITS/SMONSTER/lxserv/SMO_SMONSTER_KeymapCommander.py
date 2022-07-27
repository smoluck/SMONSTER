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


SMONSTER_HOTKEYS = [
    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMONSTER_DOC_LIBRARY_POPOVER:sheet}"]
        ],
        "key": "alt-shift-l",
        "command": "attr.formPopover {SMONSTER_DOC_LIBRARY_POPOVER:sheet}",
        "name": "SMONSTER Library Documentation Menu",
        "info": "Alt Shift L"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMONSTER_LOAD_TRAINING_SCENES:sheet}"]
        ],
        "key": "alt-shift-t",
        "command": "attr.formPopover {SMONSTER_LOAD_TRAINING_SCENES:sheet}",
        "name": "SMONSTER Training Scene Menu",
        "info": "Alt Shift T"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMONSTER_TAIL_MENU:sheet}"]
        ],
        "key": "alt-shift-k",
        "command": "attr.formPopover {SMONSTER_TAIL_MENU:sheet}",
        "name": "SMONSTER Kits Menu",
        "info": "Alt Shift K"
    },

    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "@{kit_SMO_MASTER:Scripts/SMONSTER_OpenPrefs.py}"]
        ],
        "key": "alt-shift-o",
        "command": "@{kit_SMO_MASTER:Scripts/SMONSTER_OpenPrefs.py}",
        "name": "SMONSTER Options",
        "info": "Alt Shift O"
    }

]

# max = len(SMONSTER_HOTKEYS)
# lx.out(max)


class SMONSTER_KeymapCmdClass(SmoCommanderClass):
    def commander_arguments(self):
        args = []
        for n, hotkey in enumerate(SMONSTER_HOTKEYS):
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

        for n, hotkey in enumerate(SMONSTER_HOTKEYS):
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


lx.bless(SMONSTER_KeymapCmdClass, "smo.SMONSTER.MapDefaultHotkeys")


class RemoveSMONSTER_KeymapCmdClass(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        for hotkey in SMONSTER_HOTKEYS:
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

        modo.dialogs.alert("Reverted Smonster Hotkeys", "Reverted %s Smonster hotkeys to defaults." % len(SMONSTER_HOTKEYS))


lx.bless(RemoveSMONSTER_KeymapCmdClass, "smo.SMONSTER.unmapDefaultHotkeys")


class ClearSMONSTER_KeymapCmdClass(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        for hotkey in SMONSTER_HOTKEYS:
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

        modo.dialogs.alert("Cleared SMONSTER Hotkeys", "Cleared %s SMONSTER hotkeys attribution." % len(SMONSTER_HOTKEYS))


lx.bless(ClearSMONSTER_KeymapCmdClass, "smo.SMONSTER.ClearHotkeys")
