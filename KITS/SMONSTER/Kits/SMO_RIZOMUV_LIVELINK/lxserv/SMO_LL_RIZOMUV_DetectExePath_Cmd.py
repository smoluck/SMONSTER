# python
"""
Name:         SMO_LL_RIZOMUV_SetExePath_Cmd.py

Purpose:      This Command is designed to
              Detect the RizomUV exe path to create the LiveLink.
              Set RizomUV path to the most recent version of the RizomUV installation directory
              on the system using Windows registry (regedit) or MacOS (mdfind) detection method

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Modified:     22/05/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu.command
import lxu.select
import os
import subprocess
import platform
import re
import sys

Cmd_Name = "smo.LL.RIZOMUV.DetectExePath"


class SMO_LL_RIZOMUV_DetectExePath_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO LL RIZOMUV - Detect Software Path'
    
    def cmd_Desc (self):
        return 'Set RizomUV path to the most recent version of the RizomUV installation directory on the system using Windows registry (regedit) or MacOS (mdfind) detection method.'
    
    def cmd_Tooltip (self):
        return 'Set RizomUV path to the most recent version of the RizomUV installation directory on the system using Windows registry (regedit) or MacOS (mdfind) detection method.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO LL RIZOMUV - Detect Software Path'
    
    def basic_Enable (self, msg):
        return True

    # Validate the path to RizomUV is good.
    def validRizomUVPath(self, rizomuv_exe_path):
        system = platform.system()
        if system == "Windows":
            print("Windows version of RIZOMUV is installed and have been detected")
            return rizomuv_exe_path is not None
        elif system == "Darwin":
            print("Mac version of RIZOMUV is installed and have been detected")
            return rizomuv_exe_path is not None
        return None

    # Set the path to RizomUV in a user variable un Modo's Preferences.
    def setRizomUVPath(self, rizomuv_exe_path):
        """
        Set the path in Modo's Preferences, under the 'Rizom UV Livelink Options', to be able to call the software.
        """
        if self.validRizomUVPath(rizomuv_exe_path):
            # try:
            # lx.eval ('!!user.defNew name:Smo_RizomUVPath type:string life:config')
            # except:
            # pass

            try:
                lx.eval('!!user.value Smo_RizomUVPath {%s}' % rizomuv_exe_path)
            except:
                pass

            return lx.eval1('user.value Smo_RizomUVPath ?') == rizomuv_exe_path
        return False

    # Checking installation of RizomUV by either looking at Windows Registry or via App indexing on macOS
    @property
    def get_ruv_path(self):
        """
        Returns the path to the most recent version
        of the RizomUV installation directory on the system using
        Windows registry (regedit) or MacOS (mdfind).

        Try versions from 2019.10 to 2029.10 included
        """
        system = platform.system()
        if system.lower == "windows":
            import winreg
            for i in range(9, 1, -1):
                for j in range(10, -1, -1):
                    if i == 2 and j < 2:
                        continue
                    path = "SOFTWARE\\Rizom Lab\\RizomUV VS RS 202" + str(i) + "." + str(j)
                    # path = f"SOFTWARE\\Rizom Lab\\RizomUV VS RS 202{i}.{j}"
                    try:
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                        exePath = winreg.QueryValue(key, "rizomuv.exe")
                        print("Windows - Detected Rizom UV path:", (os.path.dirname(exePath) + "\\rizomuv.exe"))
                        return (os.path.dirname(exePath) + "\\rizomuv.exe")
                    except FileNotFoundError:
                        pass

        elif system.lower == "darwin":  # MacOS
            try:
                # Adjust search strategy based on macOS version
                mac_version, _, _ = platform.mac_ver()
                major_version = int(mac_version.split(".")[0])  # Get major macOS version (e.g., "15")
                if major_version >= 15: # macOS Sequoia
                    # Use mdfind to dynamically locate RizomUV installations on MacOS Sequoia (v15.X.X)
                    result = subprocess.run(["mdfind", "kind:application RizomUV"], capture_output=True, text=True)
                else:  # macOS Sonoma and earlier release of macOS
                    result = subprocess.run(["mdfind", "RizomUV"], capture_output=True, text=True)
                app_paths = result.stdout.split("\n")

                pattern = re.compile(r"RizomUV\.(\d+)\.(\d+)")

                # # Extract versions and sort in Python 2.7
                # if (2, 7, 0) <= sys.version_info < (3, 7, 0):
                # rizuv_versions = []
                #     for path in app_paths:
                #         match = pattern.search(path)
                #         if match:
                #             rizuv_versions.append((int(match.group(1)), int(match.group(2)), path))
                #             rizuv_versions.sort(reverse=True)

                # elif sys.version_info >= (3, 8, 0):
                #     # Extract versions and sort in Python 3.8 and up (":=" run in Python 3.8 and up)
                #     rizuv_versions = sorted(
                #         [(int(match.group(1)), int(match.group(2)), path)
                #          for path in app_paths if (match := pattern.search(path))],
                #         reverse=True
                #     )

                # Extract versions and sort in Python 3.7
                rizuv_versions = sorted(
                    [
                        (int(match.group(1)), int(match.group(2)), path)
                        for path in app_paths
                        if pattern.search(path)
                    ],
                    key=lambda x: (x[0], x[1]),  # Sort by version numbers
                    reverse=True
                )
                latest_release = rizuv_versions[0][2] if rizuv_versions else None
                print("Detected base path", latest_release)

                if rizuv_versions:
                    latest_version = f"{rizuv_versions[0][0]}.{rizuv_versions[0][1]}"
                    latest_release = rizuv_versions[0][2]
                    updated_path = f"{latest_release}/Contents/MacOS/RizomUV.{latest_version}"
                else:
                    latest_release = None
                    updated_path = None

                return updated_path
            except Exception as e:
                print(f"Error locating RizomUV: {e}")
        return None

    def basic_Execute(self, msg, flags):
        # print(self.get_ruv_path())
        self.setRizomUVPath(self.get_ruv_path)
        print(lx.eval ('user.value Smo_RizomUVPath ?'))

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_LL_RIZOMUV_DetectExePath_Cmd, Cmd_Name)
