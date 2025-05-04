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
            return (rizomuv_exe_path is not None) and os.path.lexists(rizomuv_exe_path) and (os.path.splitext(rizomuv_exe_path)[1].lower() == '.exe')
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
    def get_ruv_path(self):
        """
        Returns the path to the most recent version
        of the RizomUV installation directory on the system using
        Windows registry (regedit) or MacOS (mdfind).

        Try versions from 2019.10 to 2029.10 included
        """
        system = platform.system()
        if system == "Windows":
            import winreg
            for i in range(9, 1, -1):
                for j in range(10, -1, -1):
                    if i == 2 and j < 2:
                        continue
                    # path = "SOFTWARE\\Rizom Lab\\RizomUV VS RS 202" + str(i) + "." + str(j)
                    path = f"SOFTWARE\\Rizom Lab\\RizomUV VS RS 202{i}.{j}"
                    try:
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                        exePath = winreg.QueryValue(key, "rizomuv.exe")
                        print("Windows - Detected Rizom UV path:", exePath)
                        return os.path.dirname(exePath)
                    except FileNotFoundError:
                        pass
        elif system == "Darwin":  # MacOS
            # for i in range(9, 1, -1):
            #     for j in range(10, -1, -1):
            #         if i == 2 and j < 2:
            #             continue
            #         app_path = f"/Applications/RizomUV.202{i}.{j}.app" + "/Contents/MacOS/rizomuv"
            #         if os.path.exists(app_path):
            #             return app_path
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

                # Check for valid installations
                for app_path in app_paths:
                    print("macOS - Detected Rizom UV path:", app_path)
                    if app_path and os.path.exists(app_path):
                        return os.path.join(app_path, "Contents/MacOS/rizomuv")

            except Exception as e:
                print(f"Error locating RizomUV: {e}")
        return None

    def basic_Execute(self, msg, flags):
        # print(self.get_ruv_path())
        self.setRizomUVPath(self.get_ruv_path())
        print(lx.eval ('user.value Smo_RizomUVPath ?'))

        # # Get RizomUV executable path from preferences.
        # Smo_RizomUVPath = None
        # print("Status", Smo_RizomUVPath)
        #
        # try:
        #     Smo_RizomUVPath = lx.eval1('!!user.value Smo_RizomUVPath ?')
        #     # print("Status 2", Smo_RizomUVPath)
        # except: # If failed Detect the RizomUV application path by checking automatically the installation of RizomUV by either looking at Windows Registry or via App indexing on macOS
        #     try:
        #         self.setRizomUVPath(self.get_ruv_path())
        #         Smo_RizomUVPath = lx.eval1('!!user.value Smo_RizomUVPath ?')
        #         print("Status 3", self.get_ruv_path())
        #         return
        #     except Exception as e:
        #         print(e)
        #         # if not self.get_ruv_path():
        #         #     try:
        #         #         Smo_RizomUVPath = lx.eval1('!!user.value Smo_RizomUVPath ?')
        #         #     except:  # If failed Set RizomUV executable path by asking the user to search for it in Explorer (Win) or Finder (macOS) to set it up.
        #         #         if not self.findRizomUVPath():
        #         #             return
        #         #     return
        #         return
        #
        # else:
        #     if not self.validRizomUVPath(Smo_RizomUVPath):
        #         if not self.findRizomUVPath():
        #             return
        #         else:
        #             Smo_RizomUVPath = lx.eval1('!!user.value Smo_RizomUVPath ?')
        #
        # if Smo_RizomUVPath is None:
        #     lx.out('Invalid RizomUV path.')
        #     return
        

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_LL_RIZOMUV_DetectExePath_Cmd, Cmd_Name)
