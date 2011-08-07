#! /usr/bin/python
###############################################################################
# GUI for Mark Henkelis's awesome Sonospy Project.
###############################################################################
# Copyright, blah, blah
###############################################################################
# TODO: Kill sonsopy process on window close.
###############################################################################
import wx
from wxPython.wx import *
################################################################################
import scanTab
import extractTab
import launchTab
import nowPlayingTab

################################################################################
class SonospyNotebook(wx.Notebook):
    """
    The core layout for the app -- notebook pages are slotted here
    """

    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)

        # UNCOMMENT THIS TO GET BACK TO NORMAL!
        # Now Playing is SUPER EXPERIMENTAL, WILL PROBABLY BREAK!
        self.AddPage(launchTab.LaunchPanel(self), "Launch")
#        self.AddPage(nowPlayingTab.NowPlayingPanel(self), "Now Playing")
        self.AddPage(scanTab.ScanPanel(self), "Scan")
        self.AddPage(extractTab.ExtractPanel(self), "Extract")

########################################################################
class SonospyFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Sonospy", size=(580,645))
        panel = wx.Panel(self)

        notebook = SonospyNotebook(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        ib = wx.IconBundle()
        ib.AddIconFromFile("sonospy.png", wx.BITMAP_TYPE_ANY)
        self.SetIcons(ib)
        self.CreateStatusBar(style=0)
        self.SetStatusText("Welcome to Sonospy...")
        
        self.Layout()

        self.Show()
        self.Centre()

    def OnCloseWindow(self, event):
    # tell the window to kill itself and kill the running sonospy process
        owd = os.getcwd()
        os.chdir(os.pardir)

        if os.name == 'nt':
            cmdroot = 'python '
        else:
            cmdroot = './'
        
        launchCMD = cmdroot + "sonospy_stop"
        
        proc = subprocess.Popen([launchCMD],shell=True)
        os.chdir(owd)

        self.Destroy()

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = SonospyFrame()
    app.MainLoop()
