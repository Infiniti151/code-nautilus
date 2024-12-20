# VSCode Nautilus Extension
#
# Place me in ~/.local/share/nautilus-python/extensions/,
# ensure you have python-nautilus package, restart Nautilus, and enjoy :)
#
# This script is released to the public domain.

from gi.repository import Nautilus, GObject
import os, subprocess

# path to vscode
VSCODE = 'code'

# what name do you want to see in the context menu?
VSCODENAME = 'Code'

class VSCodeExtension(GObject.GObject, Nautilus.MenuProvider):

    def launch_vscode(self, menu, files):
        safepaths = ''
        args = ''

        if os.environ.get('XDG_SESSION_TYPE') == "wayland": args = ' --ozone-platform-hint=auto'

        for file in files:
            filepath = file.get_location().get_path()
            safepaths += ' "' + filepath + '" '
            # If one of the files we are trying to open is a folder
            # create a new instance of vscode
            if os.path.isdir(filepath) and os.path.exists(filepath):
                args = ' --new-window' + args

        subprocess.run(VSCODE + args + safepaths + '&', shell=True)

    def get_file_items(self, *args):
        files = args[-1]
        item = Nautilus.MenuItem(
            name='VSCodeOpen',
            label='Open in ' + VSCODENAME,
            tip='Opens the selected files with VSCode'
        )
        item.connect('activate', self.launch_vscode, files)

        return [item]

    def get_background_items(self, *args):
        file_ = args[-1]
        item = Nautilus.MenuItem(
            name='VSCodeOpenBackground',
            label='Open in ' + VSCODENAME,
            tip='Opens the current directory in VSCode'
        )
        item.connect('activate', self.launch_vscode, [file_])

        return [item]
