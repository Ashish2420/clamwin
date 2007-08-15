#!/usr/bin/python

#-----------------------------------------------------------------------------
# Name:        ClamWin.py
# Product:     ClamWin Free Antivirus
#
# Author:      alch [alch at users dot sourceforge dot net]
#
# Created:     2004/19/03
# Copyright:   Copyright alch (c) 2004
# Licence:
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import I18N
I18N.install()


#import SetUnicode
import sys
import os
#import locale
#import RedirectStd
import wx
import MainFrame
import Utils
import DialogUtils
import Config




modules ={'ClamTray': [0, '', 'ClamTray.py'],
 'CloseWindows': [0, '', 'CloseWindows.py'],
 'Config': [0, '', 'Config.py'],
 'EmailAlert': [0, '', 'EmailAlert.py'],
 'ExplorerShell': [0, '', 'ExplorerShell.py'],
 'MsgBox': [0, '', 'MsgBox.py'],
 'OlAddin': [0, '', 'OlAddin.py'],
 'Process': [0, '', 'Process.py'],
 'RedirectStd': [0, '', 'RedirectStd.py'],
 'Scheduler': [0, '', 'Scheduler.py'],
 'SplashScreen': [0, '', 'SplashScreen.py'],
 'Utils': [0, '', 'Utils.py'],
 'wxDialogAbout': [0, '', 'wxDialogAbout.py'],
 'wxDialogCheckUpdate': [0, '', 'wxDialogCheckUpdate.py'],
 'wxDialogLogViewer': [0, '', 'wxDialogLogViewer.py'],
 'wxDialogPreferences': [0, '', 'wxDialogPreferences.py'],
 'wxDialogScheduledScan': [0, '', 'wxDialogScheduledScan.py'],
 'wxDialogStatus': [0, '', 'wxDialogStatus.py'],
 'wxDialogUtils': [0, '', 'wxDialogUtils.py'],
 'wxFrameMain': [1, 'Main frame of Application', 'wxFrameMain.py']}

class ClamWin(wx.App):
    def __init__(self, params, config, mode='main', autoClose=False, path=''):
        self.config = config
        self.mode = mode
        self.path = path
        self.autoClose = autoClose
        self.exit_code = 0
        wx.App.__init__(self, params)

    def OnInit(self):
                
        if self.mode == 'scanner':
            self.exit_code = DialogUtils.Scan(parent=None, config=self.config, path=self.path, autoClose=self.autoClose)
        elif self.mode == 'update':
            self.exit_code = DialogUtils.UpdateVirDB(parent=None, config=self.config, autoClose=self.autoClose)
        elif self.mode == 'configure':
            DialogUtils.Configure(parent=None, config=self.config)
        elif self.mode == 'configure_schedule':
            DialogUtils.Configure(parent=None, config=self.config, switchToSchedule=True)
        elif self.mode == 'about':
            DialogUtils.About(parent=None, config=self.config)
        elif self.mode == 'viewlog':
            DialogUtils.ShowLog(parent=None, logfile=self.path.strip('"'))
        elif self.mode == 'checkversion':
            DialogUtils.CheckUpdate(parent=None, config=self.config)
        else: #  mode == 'main'
            self.main = MainFrame.MainFrame(None, self.config)
            self.main.Show()
            #workaround for running in wxProcess
            self.SetTopWindow(self.main)
        return True


def main(config=None, mode='main', autoClose=False, path='', config_file=None):
    currentDir = Utils.GetCurrentDir(True)
    os.chdir(currentDir)
    Utils.CreateProfile()
    if config is None:
        if(config_file is None):
            config_file = os.path.join(Utils.GetProfileDir(True),'ClamWin.conf')
        else:
            config_file = Utils.SafeExpandEnvironmentStrings(config_file)
        config = Config.Settings(config_file)
        b = config.Read()

    app = ClamWin(0, config, mode=mode, autoClose=autoClose, path=path)
    app.MainLoop()
    return app.exit_code



if __name__ == '__main__':
    import locale
    #import codecs
    #import encodings
    print "System Locale:", locale.getdefaultlocale()
    print "Default Encoding:", sys.getdefaultencoding()

    

    # set C locale, otherwise python and wxpython complain
    #why?
    #locale.setlocale(locale.LC_ALL, 'C')
    close = False
    mode = 'main'
    path = ''
    config_file = None
    for arg in sys.argv[1:]:
        if arg == '--close':
            close = True
        if arg.find('--mode=') == 0:
            mode = arg[len('--mode='):]
        if arg.find('--path=') == 0:
            path += '"' + arg[len('--path='):].replace('/', '\\') + '" '
        if arg.find('--config_file=') == 0:
            config_file = arg[len('--config_file='):]

    print "command line path: %s" % path.strip()
    exit_code = main(mode=mode, autoClose=close, path=path.strip(), config_file=config_file)
    sys.exit(exit_code)
