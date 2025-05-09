# python

from smodule.commander.SMO_Commander import SmoCommanderClass

import lx
import modo
import os
import re

CMD_NAME = 'smo.BAKE.Startup'


class SMO_BAKE_BOOT_Cmd(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        if not lx.eval('query scriptsysservice userValue.isDefined ? SMO_BAKE_version'):
            lx.eval('user.defNew SMO_BAKE_version string')
            lx.eval('user.value SMO_BAKE_version {}')

        SMO_BAKE_version_from_config = lx.eval("user.value SMO_BAKE_version ?")

        kit_folder = lx.eval("query platformservice alias ? {kit_SMO_BAKE:}")
        index_file = os.path.join(kit_folder, "index.cfg")

        # xml.etree is not included in MODO install, so we need a hack
        # index_xml = xml.etree.ElementTree.parse(index_file).getroot()
        # SMO_BAKE_version_installed = index_xml.attrib["version"]

        # Regex is hardly ideal for this. But it works in the absence of an XML parser.
        with open(index_file, 'r') as index_file_data:
            xml_as_string = index_file_data.read().replace('\n', '')

        r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
        m = re.search(r, xml_as_string)
        SMO_BAKE_version_installed = m.group(1)

        if not SMO_BAKE_version_from_config:
            pass
        #     lx.eval('smo.BAKE.MapDefaultHotkeys')
        #
        # elif SMO_BAKE_version_from_config != SMO_BAKE_version_installed:
        elif SMO_BAKE_version_from_config != SMO_BAKE_version_installed:
            modo.dialogs.alert(
                "New SMO BAKE Version",
                "IMPORTANT: New version of SMO BAKE detected.\n \nIt is Recommended to Reset MODO prefs using:\nSystem --> Reset Preferences"
            )

        lx.eval("user.value SMO_BAKE_version %s" % SMO_BAKE_version_installed)


lx.bless(SMO_BAKE_BOOT_Cmd, CMD_NAME)
