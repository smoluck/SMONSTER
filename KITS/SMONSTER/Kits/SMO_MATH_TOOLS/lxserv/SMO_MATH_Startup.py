# python

import lx, modo, os, re
from smodule.commander.SMO_Commander import SmoCommanderClass

CMD_NAME = 'smo.MATH.Startup'

class SMO_MATH_BOOT_Cmd(SmoCommanderClass):

    def commander_execute(self, msg, flags):
        if not lx.eval('query scriptsysservice userValue.isDefined ? SMO_MATH_TOOLS_version'):
            lx.eval('user.defNew SMO_MATH_TOOLS_version string')
            lx.eval('user.value SMO_MATH_TOOLS_version {}')

        SMO_MATH_TOOLS_version_from_config = lx.eval("user.value SMO_MATH_TOOLS_version ?")

        kit_folder = lx.eval("query platformservice alias ? {kit_SMO_MATH_TOOLS:}")
        index_file = os.path.join(kit_folder, "index.cfg")

        # xml.etree is not included in MODO install, so we need a hack
        # index_xml = xml.etree.ElementTree.parse(index_file).getroot()
        # SMO_MATH_TOOLS_version_installed = index_xml.attrib["version"]

        # Regex is hardly ideal for this. But it works in the absence of an XML parser.
        with open(index_file, 'r') as index_file_data:
            xml_as_string = index_file_data.read().replace('\n', '')

        r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
        m = re.search(r, xml_as_string)
        SMO_MATH_TOOLS_version_installed = m.group(1)

        if not SMO_MATH_TOOLS_version_from_config:
            pass
            # lx.eval('smo.MATH.MapDefaultHotkeys')

        elif SMO_MATH_TOOLS_version_from_config != SMO_MATH_TOOLS_version_installed:
            modo.dialogs.alert(
                "New SMO MATH TOOLS Version",
                "IMPORTANT: New version of SMO MATH TOOLS detected.\n \nIt is Recommended to Reset MODO prefs using:\nSystem --> Reset Preferences"
                )

        lx.eval("user.value SMO_MATH_TOOLS_version %s" % SMO_MATH_TOOLS_version_installed)

lx.bless(SMO_MATH_BOOT_Cmd, CMD_NAME)
