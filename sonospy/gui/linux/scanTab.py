###############################################################################
# Scan Tab for use with sonospyGUI.py
###############################################################################
# Copyright, blah, blah
###############################################################################
# TODO:
# - STDOUT to LogView.Value in realtime. Broken in WorkerThread?
# - Hangs on LARGE database read/writes.  Maybe I am trying to push too
#   much at once to the LogWindow?
# - Add guiFunctions.statusText() where appropriate.  Replace ERROR:?
###############################################################################

import wx
from wxPython.wx import *
import os
import sys
import subprocess
from threading import *
import guiFunctions
import time

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

    def stop(self):
        self.stop()

    def run(self):
        """Run Worker Thread."""
        proc = subprocess.Popen([scanCMD], shell=True,stdout=subprocess.PIPE)

# THIS WORKS, JUST DOESN'T UPDATE THE LOGVIEW PROPERLY
#        for line in proc.communicate()[0]:
#            wx.PostEvent(self._notify_window, ResultEvent(line))
# -----------------------------------------------------------------------------
# THIS IS PROBLEMATIC!
        #Set the filename and open the file

        # delay for 1 second while log gets created...
        time.sleep(2)
        filename = 'logs/scanlog.txt'
        file = open(filename,'r')

        where = file.tell()
        line = file.readline()
        size = os.path.getsize(filename)

        while where == 0:
            where = file.tell()

        while where <= size:
            size = os.path.getsize(filename)

            print str(where) + "/" + str(size)
            
            if not line:
                time.sleep(0.1)
                wx.PostEvent(self._notify_window, ResultEvent(file.seek(where)))
                line = file.readline()
            else:
                wx.PostEvent(self._notify_window, ResultEvent(line))
                line = file.readline()

            if where == size:
                print "trying to stop"
                wx.PostEvent(self._notify_window, ResultEvent(None))
                Thread.stop()
                
            where = file.tell()


# ------------------------------------------------------------------------------
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
        help_Database = "The 'Database' is the main collection of music you will create or update. Click BROWSE to select a previously created database, or enter a new name here."
        label_MainDatabase.SetToolTip(wx.ToolTip(help_Database))
        sizer.Add(label_MainDatabase, pos=(0, 0), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL|wx.TOP, border=10)

        self.tc_MainDatabase = wx.TextCtrl(panel)
        self.tc_MainDatabase.SetToolTip(wx.ToolTip(help_Database))
        self.tc_MainDatabase.Value = guiFunctions.configMe("scan", "database")
        sizer.Add(self.tc_MainDatabase, pos=(0, 1), span=(1, 4), flag=wx.TOP|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=10)

        self.bt_MainDatabase = wx.Button(panel, label="Browse...")
        self.bt_MainDatabase.SetToolTip(wx.ToolTip(help_Database))
        sizer.Add(self.bt_MainDatabase, pos=(0, 5), flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_VERTICAL, border=10)
        self.bt_MainDatabase.Bind(wx.EVT_BUTTON, self.bt_MainDatabaseClick,self.bt_MainDatabase)
    # --------------------------------------------------------------------------
    # [1] Paths to scan for new Music ------------------------------------------
        self.sb_FoldersToScan = wx.StaticBox(panel, label="Folders to Scan:", size=(200, 100))
        help_FoldersToScan = "Folders you will scan for music files are listed here.  Click ADD to browse for a *top-level* folder.  Scan will search all sub-folders for valid music."
        folderBoxSizer = wx.StaticBoxSizer(self.sb_FoldersToScan, wx.VERTICAL)
        self.multiText = wx.TextCtrl(panel, -1,"",size=(300, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.multiText.SetToolTip(wx.ToolTip(help_FoldersToScan))
        self.multiText.SetInsertionPoint(0)
        self.multiText.Value = guiFunctions.configMe("scan", "folder", parse=True)
        folderBoxSizer.Add(self.multiText, flag=wx.EXPAND)
        sizer.Add(folderBoxSizer, pos=(1, 0), span=(1, 6), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)

    # --------------------------------------------------------------------------
    # [2] Buttons to Add Folder, Clear Scan Area -------------------------------
        # ADD FOLDER
        self.bt_FoldersToScanAdd = wx.Button(panel, label="Add")
        help_FoldersToScanAdd = "Add a top-level folder to the 'Folders to Scan' field.  The scan will search any sub-folders beneath whatever folder you add."
        self.bt_FoldersToScanAdd.SetToolTip(wx.ToolTip(help_FoldersToScanAdd))
        self.bt_FoldersToScanAdd.Bind(wx.EVT_BUTTON, self.bt_FoldersToScanAddClick, self.bt_FoldersToScanAdd)
        sizer.Add(self.bt_FoldersToScanAdd, pos=(2,0), span=(1,2), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

        # CLEAR SCAN AREA
        self.bt_FoldersToScanClear = wx.Button(panel, label="Clear")
        help_FoldersToScanClear = "Clear the Folders to Scan field."
        self.bt_FoldersToScanClear.SetToolTip(wx.ToolTip(help_FoldersToScanClear))
        sizer.Add(self.bt_FoldersToScanClear, pos=(2,5), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        self.bt_FoldersToScanClear.Bind(wx.EVT_BUTTON, self.bt_FoldersToScanClearClick, self.bt_FoldersToScanClear)
    # --------------------------------------------------------------------------
    # [3] Separator line -------------------------------------------------------
        hl_SepLine1 = wx.StaticLine(panel, 0, (250, 50), (300,1))
        sizer.Add(hl_SepLine1, pos=(3, 0), span=(1, 6), flag=wx.EXPAND, border=10)
    # --------------------------------------------------------------------------
    # [4] Add Scan Options and Scan Button -------------------------------------
        # SCAN/UPDATE
        self.bt_ScanUpdate = wx.Button(panel, label="Scan/Update")
        help_ScanUpdate = "Click here to begin your scan of the folders listed above.  This will create a new database if one doesn't exist.  Otherwise it will update the database with any new music it finds."
        self.bt_ScanUpdate.SetToolTip(wx.ToolTip(help_ScanUpdate))
        self.bt_ScanUpdate.Bind(wx.EVT_BUTTON, self.bt_ScanUpdateClick, self.bt_ScanUpdate)
        sizer.Add(self.bt_ScanUpdate, pos=(4,0), span=(1,2), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

        # REPAIR
        self.bt_ScanRepair = wx.Button(panel, label="Repair")
        help_ScanRepair = "Click here to repair the 'Database' listed above."
        self.bt_ScanRepair.SetToolTip(wx.ToolTip(help_ScanRepair))
        self.bt_ScanRepair.Bind(wx.EVT_BUTTON, self.bt_ScanRepairClick, self.bt_ScanRepair)
        sizer.Add(self.bt_ScanRepair, pos=(4,5), span=(1,2), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

        # VERBOSE
        self.ck_ScanVerbose = wx.CheckBox(panel, label="Verbose")
        help_ScanVerbose = "Select this checkbox if you want to turn on the verbose settings during the scan."
        self.ck_ScanVerbose.SetToolTip(wx.ToolTip(help_ScanVerbose))
        self.ck_ScanVerbose.Value = guiFunctions.configMe("scan", "verbose", bool=True)
        sizer.Add(self.ck_ScanVerbose, pos=(4,2), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

        # SAVE LOG TO FILE
        self.bt_SaveLog = wx.Button(panel, label="Save Log to File")
        help_SaveLogToFile = "Save the log below to a file."
        self.bt_SaveLog.SetToolTip(wx.ToolTip(help_SaveLogToFile))
        self.bt_SaveLog.Bind(wx.EVT_BUTTON, self.bt_SaveLogClick, self.bt_SaveLog)
        sizer.Add(self.bt_SaveLog, pos=(4,4), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=5)
    # --------------------------------------------------------------------------
    # [5] Separator line ------------------------------------------------------
        hl_SepLine2 = wx.StaticLine(panel, 0, (250, 50), (300,1))
        sizer.Add(hl_SepLine2, pos=(5, 0), span=(1, 6), flag=wx.EXPAND, border=10)
    # --------------------------------------------------------------------------
    # [6] Output/Log Box -------------------------------------------------------
#        self.LogWindow = wx.PyShellOutput(panel, -1,"",size=(100, 300), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.LogWindow = wx.TextCtrl(panel, -1,"",size=(100, 300), style=wx.TE_MULTILINE|wx.TE_READONLY)
        help_LogWindow = "Results of a scan or repair will appear here."
        self.LogWindow.SetToolTip(wx.ToolTip(help_LogWindow))
        self.LogWindow.SetInsertionPoint(0)
        sizer.Add(self.LogWindow, pos=(6,0), span=(1,6), flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

# DEBUG ------------------------------------------------------------------------
#        self.multiText.Value = "~/Network/Music/Weezer\n"
#        self.multiText.Value += "~/Network/Music/Yuck"
# ------------------------------------------------------------------------------

        # Indicate we don't have a worker thread yet
        EVT_RESULT(self,self.onResult)
        self.worker = None

        sizer.AddGrowableCol(2)
        panel.SetSizer(sizer)

    def onResult(self, event):
        """Show Result status."""
        if event.data is None:
            # Thread aborted (using our convention of None return)
            self.LogWindow.AppendText("\n[Complete]\n\n")
            self.worker = None
            self.setButtons(True)
        else:
            # Process results here
            self.LogWindow.AppendText(event.data)
            if "[Complete]" in self.LogWindow.Value:
                event.data == None

        # In either event, the worker is done
        self.worker = None
        guiFunctions.statusText(self, "")

    def bt_ScanRepairClick(self, event):
# DEBUG ------------------------------------------------------------------------
#        self.tc_MainDatabase.Value = "test.db"
# ------------------------------------------------------------------------------
        global scanCMD
        getOpts = ""

        self.LogWindow.Enable()
        if self.tc_MainDatabase.Value == "":
            self.LogWindow.AppendText("ERROR:\tNo database name selected!\n")
        else:
            if self.ck_ScanVerbose.Value == True:
                getOpts = "-v "

            scanCMD = "python ../../scan.py " + getOpts +"-d " + "../../" + self.tc_MainDatabase.Value + " -r"

            self.LogWindow.AppendText("Running Repair on " + self.tc_MainDatabase.Value + "...\n\n")
            guiFunctions.statusText(self, "Running Repair...")

            if not self.worker:
                self.worker = WorkerThread(self)
                self.setButtons(False)
                wx.SetCursor(wx.StockCursor(wx.CURSOR_WATCH))
                
    def bt_MainDatabaseClick(self, event):
        filters = 'Text files (*.db)|*.db|All files (*.*)|*.*'
        dialog = wx.FileDialog ( None, message = 'Select Database File...', wildcard = filters, style = wxOPEN)

        # Open Dialog Box and get Selection
        if dialog.ShowModal() == wxID_OK:
            selected = dialog.GetFilenames()
            for selection in selected:
                self.tc_MainDatabase.Value = selection
                guiFunctions.statusText(self, "Database selected...")
        dialog.Destroy()
        

    def bt_FoldersToScanAddClick(self, event):
        dialog = wx.DirDialog(self, "Add a Directory...", style=wx.DD_DEFAULT_STYLE)

        if dialog.ShowModal() == wx.ID_OK:
            self.multiText.AppendText("%s" % dialog.GetPath() + "\n")
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
            wx.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        else:
            self.bt_FoldersToScanAdd.Disable()
            self.bt_FoldersToScanClear.Disable()
            self.bt_MainDatabase.Disable()
            self.bt_SaveLog.Disable()
            self.bt_ScanRepair.Disable()
            self.bt_ScanUpdate.Disable()
            self.ck_ScanVerbose.Disable()
            wx.SetCursor(wx.StockCursor(wx.CURSOR_WATCH))


    def bt_ScanUpdateClick(self, event):
        self.LogWindow.Enable()

# DEBUG ------------------------------------------------------------------------
#        self.tc_MainDatabase.Value = "test.db"
#-------------------------------------------------------------------------------
        if self.tc_MainDatabase.Value == "":
            self.LogWindow.AppendText("ERROR:\tNo database name selected!\n")
        else:
            getOpts = ""

            if self.ck_ScanVerbose.Value == True:
                getOpts = "-v "

            global scanCMD
            scanCMD = "python ../../scan.py " + getOpts +"-d " + "../../" + self.tc_MainDatabase.Value + " "

            numLines=0
            maxLines=(int(self.multiText.GetNumberOfLines()))

            if self.multiText.GetLineText(numLines) == "":
                self.LogWindow.AppendText("ERROR\tNo folder selected to scan!\n")
            else:
                self.LogWindow.AppendText("Running Scan...\n\n")
                guiFunctions.statusText(self, "Running Scan...")
                while (numLines < maxLines):
                    scanCMD += str(self.multiText.GetLineText(numLines)) + " "
                    numLines += 1

# Multithreading is below this line.
                if not self.worker:
                    self.worker = WorkerThread(self)
                    self.setButtons(False)

