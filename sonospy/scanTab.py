###############################################################################
# Scan Tab for use with sonospyGUI.py
###############################################################################
# Copyright, blah, blah
###############################################################################
# TODO:
#      - Get multithreading to work somehow, so I can process the STDOUT to
#        LogWindow in realtime.
#      - Cosmetic work -- grey out log until it is activated, etc.
###############################################################################

import wx
from wxPython.wx import *
import os
import subprocess

scanCMD = ""

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

        bt_MainDatabase = wx.Button(panel, label="Browse...")
        sizer.Add(bt_MainDatabase, pos=(0, 5), flag=wx.LEFT|wx.RIGHT|wx.TOP|
            wx.ALIGN_CENTER_VERTICAL, border=10)
        bt_MainDatabase.Bind(wx.EVT_BUTTON, self.bt_MainDatabaseClick,
            bt_MainDatabase)
    # --------------------------------------------------------------------------
    # [1] Paths to scan for new Music ------------------------------------------
        self.sb_FoldersToScan = wx.StaticBox(panel, label="Folders to Scan:", size=(200,100))
        folderBoxSizer = wx.StaticBoxSizer(self.sb_FoldersToScan, wx.VERTICAL)
        self.multiText = wx.TextCtrl(panel, -1,"",size=(300, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.multiText.SetInsertionPoint(0)
        folderBoxSizer.Add(self.multiText, flag=wx.EXPAND)
        sizer.Add(folderBoxSizer, pos=(1, 0), span=(1, 6), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)

    # --------------------------------------------------------------------------
    # [2] Buttons to Add Folder, Clear Scan Area -------------------------------
        bt_FoldersToScanAdd = wx.Button(panel, label="Add")
        bt_FoldersToScanClear = wx.Button(panel, label="Clear")
        sizer.Add(bt_FoldersToScanAdd, pos=(2,0), span=(1,2), flag=wx.LEFT|wx.RIGHT|
            wx.ALIGN_CENTER_VERTICAL, border=10)
        bt_FoldersToScanAdd.Bind(wx.EVT_BUTTON, self.bt_FoldersToScanAddClick, bt_FoldersToScanAdd)
        sizer.Add(bt_FoldersToScanClear, pos=(2,5), flag=wx.LEFT|wx.RIGHT|
            wx.ALIGN_CENTER_VERTICAL, border=10)
        bt_FoldersToScanClear.Bind(wx.EVT_BUTTON, self.bt_FoldersToScanClearClick, bt_FoldersToScanClear)
    # --------------------------------------------------------------------------
    # [3] Separator line -------------------------------------------------------
        hl_SepLine1 = wx.StaticLine(panel, 0, (250, 50), (300,1))
        sizer.Add(hl_SepLine1, pos=(3, 0), span=(1, 6), flag=wx.EXPAND, border=10)
    # --------------------------------------------------------------------------
    # [4] Add Scan Options and Scan Button -------------------------------------
        bt_ScanUpdate = wx.Button(panel, label="Scan/Update")
        bt_ScanUpdate.Bind(wx.EVT_BUTTON, self.bt_ScanUpdateClick, bt_ScanUpdate)
        bt_ScanRepair = wx.Button(panel, label="Repair")
        bt_ScanRepair.Bind(wx.EVT_BUTTON, self.bt_ScanRepairClick, bt_ScanRepair)
        self.ck_ScanVerbose = wx.CheckBox(panel, label="Verbose")
        bt_SaveLog = wx.Button(panel, label="Save to Log")
        bt_SaveLog.Bind(wx.EVT_BUTTON, self.bt_SaveLogClick, bt_SaveLog)
        sizer.Add(bt_ScanUpdate, pos=(4,0), span=(1,2), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(self.ck_ScanVerbose, pos=(4,2), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(bt_SaveLog, pos=(4,4), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=5)
        sizer.Add(bt_ScanRepair, pos=(4,5), span=(1,2), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
    # --------------------------------------------------------------------------
    # [5] Separator line ------------------------------------------------------
        hl_SepLine2 = wx.StaticLine(panel, 0, (250, 50), (300,1))
        sizer.Add(hl_SepLine2, pos=(5, 0), span=(1, 6), flag=wx.EXPAND, border=10)
    # --------------------------------------------------------------------------
    # [6] Output/Log Box -------------------------------------------------------
        self.LogWindow = wx.TextCtrl(panel, -1,"",size=(100, 300), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.LogWindow.SetInsertionPoint(0)
        sizer.Add(self.LogWindow, pos=(6,0), span=(1,6), flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

    # DEBUG
        self.multiText.Value = "~/Network/Music/Weezer\n"
        self.multiText.Value += "~/Network/Music/Yuck"

        sizer.AddGrowableCol(2)
        panel.SetSizer(sizer)

    def bt_ScanRepairClick(self, event):
        ## DEBUG
        self.tc_MainDatabase.Value = "test.db"

        if self.tc_MainDatabase.Value == "":
            self.LogWindow.Value += "ERROR:\tNo database name selected!\n"
        else:
            if self.ck_ScanVerbose.Value == True:
                getOpts = "-v "

            scanCMD = "./scan " + getOpts +"-d " + self.tc_MainDatabase.Value + " -r"

            self.LogWindow.Value += "Running Repair on " + self.tc_MainDatabase.Value + "...\n\n"
            proc = subprocess.Popen([scanCMD],shell=True,stdout=subprocess.PIPE)
            for line in proc.communicate()[0]:
                self.LogWindow.AppendText(line)

    def bt_MainDatabaseClick(self, event):
        # Create a list of filters
        filters = 'Text files (*.db)|*.db|All files (*.*)|*.*'
        dialog = wx.FileDialog ( None, message = 'Select Database File...',
            wildcard = filters, style = wxOPEN )

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
            saveMe = open(savefile, 'w')#open the file (self.filename) to store our saved data
            saveMe.write(self.LogWindow.Value)#get our text from the textctrl, and write it out to the file we just opened.
            saveMe.close()#and then close the file.

    def bt_ScanUpdateClick(self, event):

        ## DEBUG
        self.tc_MainDatabase.Value = "test.db"

        if self.tc_MainDatabase.Value == "":
            self.LogWindow.Value += "ERROR:\tNo database name selected!\n"
        else:
            getOpts = ""

            if self.ck_ScanVerbose.Value == True:
                getOpts = "-v "

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

                # DEBUG
                # self.LogWindow.Value += scanCMD

                proc = subprocess.Popen([scanCMD],shell=True,stdout=subprocess.PIPE)
                for line in proc.communicate()[0]:
                    self.LogWindow.AppendText(line)
