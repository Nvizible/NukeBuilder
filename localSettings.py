
defaultNukeVersion = "6.2v4"
defaultArch = "64"

nukeLocation = {
                'darwin.i386'    : "/Applications/Nuke%(nuke_version)s-32/Nuke%(nuke_version)s.app/Contents/MacOS",
                'darwin.x86_64'  : "/Applications/Nuke%(nuke_version)s/Nuke%(nuke_version)s.app/Contents/MacOS",
                'linux.i386'     : "/usr/local/Nuke%(nuke_version)s",
                'linux.x86_64'   : "/usr/local/Nuke%(nuke_version)s",
                'windows.x86'    : "C:\\Program Files (x86)\\Nuke%(nuke_version)s",
                'windows.x86_64' : "C:\\Program Files\\Nuke%(nuke_version)s"
                }
