###############################################################################
# Scan Tab for use with sonospyGUI.py
###############################################################################
# Copyright, blah, blah
###############################################################################
# TODO:
#      - STDOUT to LogView.Value in realtime. Broken in WorkerThread?
#      - Cosmetic work -- grey out log until it is activated, etc.
###############################################################################

import wx
from wxPython.wx import *
import os, sys
import subprocess
from threading import *

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data


# Worker thread for multi-threading
class WorkerThread(Thread):
    """Worker Thread Class."""
    def __init__(self, notify_window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.start()

    def run(self):
        """Run Worker Thread."""
        proc = subprocess.Popen([scanCMD], shell=True,stdout=subprocess.PIPE)
        for line in proc.communicate()[0]:
            wx.PostEvent(self._notify_window, ResultEvent(line))
        wx.PostEvent(self._notify_window, ResultEvent(None))
        return

class ScanPanel(wx.Panel):
    """
    Scan Tab for running Sonospy Database Scans, Updates and Repairs
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        panel = self
        sizer = wx.GridBagSizer(6, 5)
        self.currentDirectory = os.getcwd()

    # [0] Main Database Text, Entry and Browse Button --------------------------
        label_MainDatabase = wx.StaticText(panel, label="Database:")
        sizer.Add(label_MainDatabase, pos=(0, 0), flag=wx.LEFT|
            wx.ALIGN_CENTER_VERTICAL|wx.TOP, border=10)

        self.tc_MainDatabase = wx.TextCtrl(panel)
        sizer.Add(self.tc_MainDatabase, pos=(0, 1), span=(1, 4), flag=wx.TOP|
            wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=10)

        self.bt_MainDatabase = wx.Button(panel, label="Browse...")
        sizer.Add(self.bt_MainDatabase, pos=(0, 5), flag=wx.LEFT|wx.RIGHT|wx.TOP|
            wx.ALIGN_CENTER_VERTICAL, border=10)
        self.bt_MainDatabase.Bind(wx.EVT_BUTTON, self.bt_MainDatabaseClick,
            self.bt_MainDatabase)
    # --------------------------------------------------------------------------
    # [1] Paths to scan for new Music ------------------------------------------
        self.sb_FoldersToScan = wx.StaticBox(panel, label="Folders to Scan:", size=(200, 100))
        folderBoxSizer = wx.StaticBoxSizer(self.sb_FoldersToScan, wx.VERTICAL)
        self.multiText = wx.TextCtrl(panel, -1,"",size=(300, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.multiText.SetInsertionPoint(0)
        folderBoxSizer.Add(self.multiText, flag=wx.EXPAND)
        sizer.Add(folderBoxSizer, pos=(1, 0), span=(1, 6), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)

    # --------------------------------------------------------------------------
    # [2] Buttons to Add Folder, Clear Scan Area -------------------------------
        self.bt_FoldersToScanAdd = wx.Button(panel, label="Add")
        self.bt_FoldersToScanClear = wx.Button(panel, label="Clear")
        sizer.Add(self.bt_FoldersToScanAdd, pos=(2,0), span=(1,2), flag=wx.LEFT|wx.RIGHT|
            wx.ALIGN_CENTER_VERTICAL, border=10)
        self.bt_FoldersToScanAdd.Bind(wx.EVT_BUTTON, self.bt_FoldersToScanAddClick, self.bt_FoldersToScanAdd)
        sizer.Add(self.bt_FoldersToScanClear, pos=(2,5), flag=wx.LEFT|wx.RIGHT|
            wx.ALIGN_CENTER_VERTICAL, border=10)
        self.bt_FoldersToScanClear.Bind(wx.EVT_BUTTON, self.bt_FoldersToScanClearClick, self.bt_FoldersToScanClear)
    # --------------------------------------------------------------------------
    # [3] Separator line -------------------------------------------------------
        hl_SepLine1 = wx.StaticLine(panel, 0, (250, 50), (300,1))
        sizer.Add(hl_SepLine1, pos=(3, 0), span=(1, 6), flag=wx.EXPAND, border=10)
    # --------------------------------------------------------------------------
    # [4] Add Scan Options and Scan Button -------------------------------------
        self.bt_ScanUpdate = wx.Button(panel, label="Scan/Update")
        self.bt_ScanUpdate.Bind(wx.EVT_BUTTON, self.bt_ScanUpdateClick, self.bt_ScanUpdate)
        self.bt_ScanRepair = wx.Button(panel, label="Repair")
        self.bt_ScanRepair.Bind(wx.EVT_BUTTON, self.bt_ScanRepairClick, self.bt_ScanRepair)
        self.ck_ScanVerbose = wx.CheckBox(panel, label="Verbose")
        self.bt_SaveLog = wx.Button(panel, label="Save to Log")
        self.bt_SaveLog.Bind(wx.EVT_BUTTON, self.bt_SaveLogClick, self.bt_SaveLog)
        sizer.Add(self.bt_ScanUpdate, pos=(4,0), span=(1,2), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(self.ck_ScanVerbose, pos=(4,2), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(self.bt_SaveLog, pos=(4,4), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=5)
        sizer.Add(self.bt_ScanRepair, pos=(4,5), span=(1,2), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
    # --------------------------------------------------------------------------
    # [5] Separator line ------------------------------------------------------
        hl_SepLine2 = wx.StaticLine(panel, 0, (250, 50), (300,1))
        sizer.Add(hl_SepLine2, pos=(5, 0), span=(1, 6), flag=wx.EXPAND, border=10)
    # --------------------------------------------------------------------------
    # [6] Output/Log Box -------------------------------------------------------
        self.LogWindow = wx.TextCtrl(panel, -1,"",size=(100, 300), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.LogWindow.SetInsertionPoint(0)
        self.LogWindow.Disable()
        sizer.Add(self.LogWindow, pos=(6,0), span=(1,6), flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

# DEBUG ------------------------------------------------------------------------
        self.multiText.Value = "~/Network/Music/Weezer\n"
        self.multiText.Value += "~/Network/Music/Yuck"
#-------------------------------------------------------------------------------



        # Indicate we don't have a worker thread yet
        EVT_RESULT(self,self.OnResult)
        self.worker = None

        sizer.AddGrowableCol(2)
        panel.SetSizer(sizer)

    def OnResult(self, event):
        """Show Result status."""
        if event.data is None:
            # Thread aborted (using our convention of None return)
            self.LogWindow.Value += "\n[Complete]\n"
            self.setButtons(True)
            wx.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        else:
            # Process results here
            self.LogWindow.Value +=  event.data
        # In either event, the worker is done
        self.worker = None

    def bt_ScanRepairClick(self, event):
# DEBUG ------------------------------------------------------------------------
#        self.tc_MainDatabase.Value = "test.db"
# ------------------------------------------------------------------------------
        global scanCMD
        getOpts = ""

        self.LogWindow.Enable()
        if self.tc_MainDatabase.Value == "":
            self.LogWindow.Value += "ERROR:\tNo database name selected!\n"
        else:
            if self.ck_ScanVerbose.Value == True:
                getOpts = "-v "

            scanCMD = "./scan " + getOpts +"-d " + self.tc_MainDatabase.Value + " -r"

            self.LogWindow.Value += "Running Repair on " + self.tc_MainDatabase.Value + "...\n\n"
            if not self.worker:
                self.worker = WorkerThread(self)

    def bt_MainDatabaseClick(self, event):
        filters = 'Text files (*.db)|*.db|All files (*.*)|*.*'
        dialog = wx.FileDialog ( None, message = 'Select Database File...', wildcard = filters, style = wxOPEN)

        # Open Dialog Box and get Selection
        if dialog.ShowModal() == wxID_OK:
            selected = dialog.GetFilenames()
            for selection in selected:
                self.tc_MainDatabase.Value = selection
        dialog.Destroy()

    def bt_FoldersToScanAddClick(self, event):
        dialog = wx.DirDialog(self, "Add a Directory...", style=wx.DD_DEFAULT_STYLE)

        if dialog.ShowModal() == wx.ID_OK:
            self.multiText.Value += "%s" % dialog.GetPath() + "\n"
        dialog.Destroy()

    def bt_FoldersToScanClearClick(self, event):
        self.multiText.Value = ""

    def bt_SaveLogClick(self, event):
        dialog = wx.FileDialog(self, message='Choose a file', style=wx.SAVE|wx.OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            savefile = dialog.GetFilename()

            saveMe = open(savefile, 'w')
            saveMe.write(self.LogWindow.Value)
            saveMe.close()

    def setButtons(self, state):
        """
        Toggle for the button states.
        """
        
        if state == True:
            self.bt_FoldersToScanAdd.Enable()
            self.bt_FoldersToScanClear.Enable()
            self.bt_MainDatabase.Enable()
            self.bt_SaveLog.Enable()
            self.bt_ScanRepair.Enable()
            self.bt_ScanUpdate.Enable()
            self.ck_ScanVerbose.Enable()
        else:
            self.bt_FoldersToScanAdd.Disable()
            self.bt_FoldersToScanClear.Disable()
            self.bt_MainDatabase.Disable()
            self.bt_SaveLog.Disable()
            self.bt_ScanRepair.Disable()
            self.bt_ScanUpdate.Disable()
            self.ck_ScanVerbose.Disable()

    def bt_ScanUpdateClick(self, event):
        self.LogWindow.Enable()

# DEBUG ------------------------------------------------------------------------
        self.tc_MainDatabase.Value = "test.db"
#-------------------------------------------------------------------------------
        if self.tc_MainDatabase.Value == "":
            self.LogWindow.Value += "ERROR:\tNo database name selected!\n"
        else:
            getOpts = ""

            if self.ck_ScanVerbose.Value == True:
                getOpts = "-v "

            global scanCMD
            scanCMD = "./scan " + getOpts +"-d " + self.tc_MainDatabase.Value + " "

            numLines=0
            maxLines=(int(self.multiText.GetNumberOfLines()))

            if self.multiText.GetLineText(numLines) == "":
                self.LogWindow.Value += "ERROR\tNo folder selected to scan!\n"
            else:
                self.LogWindow.Value += "Running Scan...\n\n"
                while (numLines < maxLines):
                    scanCMD += str(self.multiText.GetLineText(numLines)) + " "
                    numLines += 1

# Multithreading is below this line.
                if not self.worker:
                    self.worker = WorkerThread(self)
                    self.setButtons(False)
                    wx.SetCursor(wx.StockCursor(wx.CURSOR_WATCH))

