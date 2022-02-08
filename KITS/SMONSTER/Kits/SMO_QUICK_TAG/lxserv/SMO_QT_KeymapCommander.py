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


SMO_QUICK_TAG_HOTKEYS = [
    {
        "contexts": [
            [".global", "(stateless)", ".anywhere", "(contextless)", "attr.formPopover {SMO_QT_PM:sheet}"]
        ],
        "key": "ctrl-alt-t",
        "command": "attr.formPopover {SMO_QT_PM:sheet}",
        "name": "QUICK TAG: Pie Menu",
        "info": "Ctrl Alt T"
    }

]

# max = len(SMO_QUICK_TAG_HOTKEYS)
# lx.out(max)


class SMO_QT_KeymapCmdClass(SmoCommanderClass):
    def commander_arguments(self):
        args = []
        for n, hotkey in enumerate(SMO_QUICK_TAG_HOTKEYS):
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

        for n, hotkey in enumerate(SMO_QUICK_TAG_HOTKEYS):
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

lx.bless(SMO_QT_KeymapCmdClass, "smo.QT.MapDefaultHotkeys")


class RemoveSMO_QT_KeymapCmdClass(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        for hotkey in SMO_QUICK_TAG_HOTKEYS:
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

        modo.dialogs.alert("Reverted SMO QUICK TAG Hotkeys", "Reverted %s SMO QUICK TAG hotkeys to defaults." % len(SMO_QUICK_TAG_HOTKEYS))

lx.bless(RemoveSMO_QT_KeymapCmdClass, "smo.QT.UnmapDefaultHotkeys")


class ClearSMO_QT_KeymapCmdClass(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        for hotkey in SMO_QUICK_TAG_HOTKEYS:
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

        modo.dialogs.alert("Cleared SMO QUICK TAG Hotkeys", "Cleared %s SMO QUICK TAG hotkeys attribution." % len(SMO_QUICK_TAG_HOTKEYS))

lx.bless(ClearSMO_QT_KeymapCmdClass, "smo.QT.ClearHotkeys")