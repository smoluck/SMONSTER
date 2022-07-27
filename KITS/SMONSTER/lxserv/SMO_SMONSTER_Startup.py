# python

import lx, modo, os, re, sys
python_majorver = sys.version_info.major
# print('the Highest version number 2 for 2.7 release / 3 for 3.7 release')
# print(python_majorver)

if python_majorver == 2 :
    # print("do something for 2.X code")
    from smodule.commander.SMO_Commander import SmoCommanderClass
elif python_majorver >= 3 :
    # print("do something for 3.X code")
    from smodule.commander.SMO_Commander import SmoCommanderClass


Cmd_Name = 'smo.SMONSTER.Startup'

class SMONSTER_BOOT_Cmd(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        if not lx.eval('query scriptsysservice userValue.isDefined ? SMO_SMONSTER_version'):
            lx.eval('user.defNew SMO_SMONSTER_version string')
            lx.eval('user.value SMO_SMONSTER_version {}')

        SMO_SMONSTER_version_from_config = lx.eval("user.value SMO_SMONSTER_version ?")

        kit_folder = lx.eval("query platformservice alias ? {kit_SMONSTER:}")
        index_file = os.path.join(kit_folder, "index.cfg")

        # xml.etree is not included in MODO install, so we need a hack
        # index_xml = xml.etree.ElementTree.parse(index_file).getroot()
        # SMO_SMONSTER_version_installed = index_xml.attrib["version"]

        # Regex is hardly ideal for this. But it works in the absence of an XML parser.
        with open(index_file, 'r') as index_file_data:
            xml_as_string = index_file_data.read().replace('\n', '')

        r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
        m = re.search(r, xml_as_string)
        SMO_SMONSTER_version_installed = m.group(1)

        if not SMO_SMONSTER_version_from_config:
            pass
            # lx.eval('smo.SMONSTER.MapDefaultHotkeys')
            lx.eval('attr.formPopover {SMONSTER_QUICK_KEYMAPS:sheet} pin:true')

        elif SMO_SMONSTER_version_from_config != SMO_SMONSTER_version_installed:
            modo.dialogs.alert(
                "New SMONSTER Version",
                "IMPORTANT: New version of SMONSTER detected.\n \nIt is Recommended to Reset MODO prefs using:\nSystem --> Reset Preferences"
                )

        lx.eval("user.value SMO_SMONSTER_version %s" % SMO_SMONSTER_version_installed)


lx.bless(SMONSTER_BOOT_Cmd, Cmd_Name)
