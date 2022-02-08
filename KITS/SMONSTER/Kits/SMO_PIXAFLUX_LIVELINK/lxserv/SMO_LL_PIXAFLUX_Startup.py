# python

import lx, modo, os, re
from smodule.commander.SMO_Commander import SmoCommanderClass

CMD_NAME = 'smo.LL.PIXAFLUX.Startup'

class SMO_LL_PIXAFLUX_BOOT_Cmd(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        if not lx.eval('query scriptsysservice userValue.isDefined ? SMO_PIXAFLUX_LIVELINK_version'):
            lx.eval('user.defNew SMO_PIXAFLUX_LIVELINK_version string')
            lx.eval('user.value SMO_PIXAFLUX_LIVELINK_version {}')

        SMO_PIXAFLUX_LIVELINK_version_from_config = lx.eval("user.value SMO_PIXAFLUX_LIVELINK_version ?")

        kit_folder = lx.eval("query platformservice alias ? {kit_SMO_PIXAFLUX_LIVELINK:}")
        index_file = os.path.join(kit_folder, "index.cfg")

        # xml.etree is not included in MODO install, so we need a hack
        # index_xml = xml.etree.ElementTree.parse(index_file).getroot()
        # SMO_PIXAFLUX_LIVELINK_version_installed = index_xml.attrib["version"]

        # Regex is hardly ideal for this. But it works in the absence of an XML parser.
        with open(index_file, 'r') as index_file_data:
            xml_as_string = index_file_data.read().replace('\n', '')

        r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
        m = re.search(r, xml_as_string)
        SMO_PIXAFLUX_LIVELINK_version_installed = m.group(1)

        if not SMO_PIXAFLUX_LIVELINK_version_from_config:
            pass
            # lx.eval('smo.LL.PIXAFLUX.MapDefaultHotkeys')

        elif SMO_PIXAFLUX_LIVELINK_version_from_config != SMO_PIXAFLUX_LIVELINK_version_installed:
            modo.dialogs.alert(
                "New SMO MARMOSET LiveLink Version",
                "IMPORTANT: New version of SMO MARMOSET LiveLink detected.\n \nIt is Recommended to Reset MODO prefs using:\nSystem --> Reset Preferences"
                )

        lx.eval("user.value SMO_PIXAFLUX_LIVELINK_version %s" % SMO_PIXAFLUX_LIVELINK_version_installed)

lx.bless(SMO_LL_PIXAFLUX_BOOT_Cmd, CMD_NAME)
