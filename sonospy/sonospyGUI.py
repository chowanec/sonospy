###############################################################################
# GUI for Mark Henkelis's awesome Sonospy Project.
###############################################################################
# Copyright, blah, blah
###############################################################################
# TODO lists are stored in individual files in the second import line below.
###############################################################################

import wx, sys
import scanTab, extractTab, launchTab
from wxPython.wx import *

########################################################################
class SonospyNotebook(wx.Notebook):
    """
    The core layout for the app -- notebook pages are slotted here
    """

    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)


        # Create the first tab and add it to the notebook
        tabOne = scanTab.ScanPanel(self)
        tabTwo = extractTab.ExtractPanel(self)
        tabThree = launchTab.LaunchPanel(self)

        # UNCOMMENT THIS TO GET BACK TO NORMAL!
        self.AddPage(tabOne, "Scan")
        self.AddPage(tabThree, "Launch")
        self.AddPage(tabTwo, "Extract")

########################################################################
class SonospyFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Sonospy", size=(520,610))
        panel = wx.Panel(self)

        notebook = SonospyNotebook(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()

        self.Show()
        self.Centre()
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = SonospyFrame()
    app.MainLoop()
