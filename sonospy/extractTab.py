###############################################################################
# Extract Tab for use with sonospyGUI.py
###############################################################################
# Copyright, blah, blah
###############################################################################
# TODO:
#      - Write extract function based on criteria
#      - Enable Verbose, overwrite and log
#      - Mulithread
###############################################################################

import wx
from wxPython.wx import *
import os
import subprocess

class ExtractPanel(wx.Panel):
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
        label_MainDatabase = wx.StaticText(panel, label="Source Database:")
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
    # [1] Target Database Label, Entry and Browse Button -----------------------

        # Create the label, text control and button
        label_TargetDatabase = wx.StaticText(panel, label="Target Database:")
        self.tc_TargetDatabase = wx.TextCtrl(panel)
        bt_TargetDatabase = wx.Button(panel, label="Browse...")

        # Add them to the sizer.
        sizer.Add(label_TargetDatabase, pos=(1, 0), flag=wx.LEFT|
            wx.ALIGN_CENTER_VERTICAL|wx.TOP, border=10)
        sizer.Add(self.tc_TargetDatabase, pos=(1, 1), span=(1, 4), flag=wx.TOP|
            wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(bt_TargetDatabase, pos=(1, 5), flag=wx.LEFT|wx.RIGHT|wx.TOP|
            wx.ALIGN_CENTER_VERTICAL, border=10)

        # Bind the button to a click event
        bt_TargetDatabase.Bind(wx.EVT_BUTTON, self.bt_TargetDatabaseClick,
            bt_TargetDatabase)
    # --------------------------------------------------------------------------
    # [2] Options Static Box ---------------------------------------------------

        # Create static box
        self.sb_ExtractOptions = wx.StaticBox(panel, label="Options for Extract", size=(100,100))
        sbs_ExtractOptions = wx.StaticBoxSizer(self.sb_ExtractOptions, wx.VERTICAL)
        OptionBoxSizer = wx.GridBagSizer(4, 9)
        
        # Create the options
        logicList = ['<', '<=', '=', '>', '>=']

        sizerIndexX = 0

        # Created
        label_OptionsCreated = wx.StaticText(panel, label="Created:")
        combo_LogicalCreated = wx.ComboBox(panel, 1, "", (25, 25), (60, 25), logicList, wx.CB_DROPDOWN)
        combo_LogicalCreated.Select(1)
        self.tc_DaysAgoCreated = wx.TextCtrl(panel)
        label_DaysAgoCreated = wx.StaticText(panel, label="days ago")
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsCreated, pos=(sizerIndexX, 0), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(combo_LogicalCreated, pos=(sizerIndexX,1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=1)
        OptionBoxSizer.Add(self.tc_DaysAgoCreated, pos=(sizerIndexX, 2), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)
        OptionBoxSizer.Add(label_DaysAgoCreated, pos=(sizerIndexX,3), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)

        # Inserted
        sizerIndexX += 1
        label_OptionsInserted = wx.StaticText(panel, label="Inserted:")
        combo_LogicalInserted = wx.ComboBox(panel, 1, "", (25, 25), (60, 25), logicList, wx.CB_DROPDOWN)
        combo_LogicalInserted.Select(1)
        self.tc_DaysAgoInserted = wx.TextCtrl(panel)
        label_DaysAgoInserted = wx.StaticText(panel, label="days ago")
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsInserted, pos=(sizerIndexX, 0), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(combo_LogicalInserted, pos=(sizerIndexX,1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=1)
        OptionBoxSizer.Add(self.tc_DaysAgoInserted, pos=(sizerIndexX, 2), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)
        OptionBoxSizer.Add(label_DaysAgoInserted, pos=(sizerIndexX,3), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)

        # Modified
        sizerIndexX += 1
        label_OptionsModified = wx.StaticText(panel, label="Modified:")
        combo_LogicalModified = wx.ComboBox(panel, 1, "", (25, 25), (60, 25), logicList, wx.CB_DROPDOWN)
        combo_LogicalModified.Select(1)
        self.tc_DaysAgoModified = wx.TextCtrl(panel)
        label_DaysAgoModified = wx.StaticText(panel, label="days ago")
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsModified, pos=(sizerIndexX, 0), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(combo_LogicalModified, pos=(sizerIndexX,1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=1)
        OptionBoxSizer.Add(self.tc_DaysAgoModified, pos=(sizerIndexX, 2), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)
        OptionBoxSizer.Add(label_DaysAgoModified, pos=(sizerIndexX,3), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)

        # Scanned
        sizerIndexX += 1
        label_OptionsScanned = wx.StaticText(panel, label="Scanned:")
        combo_LogicalScanned = wx.ComboBox(panel, 1, "", (25, 25), (60, 25), logicList, wx.CB_DROPDOWN)
        combo_LogicalScanned.Select(1)
        self.tc_DaysAgoScanned = wx.TextCtrl(panel)
        label_DaysAgoScanned = wx.StaticText(panel, label="days ago")
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsScanned, pos=(sizerIndexX, 0), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(combo_LogicalScanned, pos=(sizerIndexX,1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=1)
        OptionBoxSizer.Add(self.tc_DaysAgoScanned, pos=(sizerIndexX, 2), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)
        OptionBoxSizer.Add(label_DaysAgoScanned, pos=(sizerIndexX,3), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)

        # Year
        sizerIndexX += 1
        label_OptionsYear = wx.StaticText(panel, label="Year Recorded:")
        combo_LogicalYear = wx.ComboBox(panel, 1, "", (25, 25), (60, 25), logicList, wx.CB_DROPDOWN)
        combo_LogicalYear.Select(1)
        self.tc_Year = wx.TextCtrl(panel)
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsYear, pos=(sizerIndexX, 0), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(combo_LogicalYear, pos=(sizerIndexX,1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=1)
        OptionBoxSizer.Add(self.tc_Year, pos=(sizerIndexX, 2), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)

        # Genre
        sizerIndexX += 1
        label_OptionsGenre = wx.StaticText(panel, label="Genre:")
        self.tc_Genre = wx.TextCtrl(panel)
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsGenre, pos=(sizerIndexX, 0), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(self.tc_Genre, pos=(sizerIndexX, 1), span=(1,2), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=0)

        # Artist
        sizerIndexX += 1
        label_OptionsArtist = wx.StaticText(panel, label="Artist:")
        self.tc_Artist = wx.TextCtrl(panel)
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsArtist, pos=(sizerIndexX, 0), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(self.tc_Artist, pos=(sizerIndexX, 1), span=(1,2), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=0)

        # Composer
        sizerIndexX += 1
        label_OptionsComposer = wx.StaticText(panel, label="Composer:")
        self.tc_Composer = wx.TextCtrl(panel)
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsComposer, pos=(sizerIndexX, 0), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(self.tc_Composer, pos=(sizerIndexX, 1), span=(1,2), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=0)

        # Bit-rate
        sizerIndexX += 1
        label_OptionsBitrate = wx.StaticText(panel, label="Bitrate:")
        combo_LogicalBitrate = wx.ComboBox(panel, 1, "", (25, 25), (60, 25), logicList, wx.CB_DROPDOWN)
        combo_LogicalBitrate.Select(1)
        self.tc_Bitrate = wx.TextCtrl(panel)

        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsBitrate, pos=(sizerIndexX, 0), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(combo_LogicalBitrate, pos=(sizerIndexX,1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=1)
        OptionBoxSizer.Add(self.tc_Bitrate, pos=(sizerIndexX, 2), flag=wx.ALL|
            wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)

        OptionBoxSizer.AddGrowableCol(4)
        sbs_ExtractOptions.Add(OptionBoxSizer, flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(sbs_ExtractOptions, pos=(2, 0), span=(1,6),flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=10)

    # --------------------------------------------------------------------------
    # [3] Add Scan Options and Scan Button -------------------------------------
        bt_Extract = wx.Button(panel, label="Extract")
        bt_Extract.Bind(wx.EVT_BUTTON, self.bt_ExtractClick, bt_Extract)
        self.ck_ExtractVerbose = wx.CheckBox(panel, label="Verbose")
        self.ck_ExtractLog = wx.CheckBox(panel, label="Log")
        self.ck_OverwriteExisting = wx.CheckBox(panel, label="Overwrite")

        sizer.Add(bt_Extract, pos=(3,0), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(self.ck_ExtractVerbose, pos=(3,1), flag=wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(self.ck_OverwriteExisting, pos=(3,2), flag=wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(self.ck_ExtractLog, pos=(3,3), flag=wx.ALIGN_CENTER_VERTICAL, border=0)
    # --------------------------------------------------------------------------
    # [4] Separator line ------------------------------------------------------
        hl_SepLine2 = wx.StaticLine(panel, 0, (250, 50), (300,1))
        sizer.Add(hl_SepLine2, pos=(4, 0), span=(1, 6), flag=wx.EXPAND, border=10)
    # --------------------------------------------------------------------------
    # [5] Output/Log Box -------------------------------------------------------
        self.LogWindow = wx.TextCtrl(panel, -1,"",size=(100, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.LogWindow.SetInsertionPoint(0)
        sizer.Add(self.LogWindow, pos=(5,0), span=(1,6), flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

        sizer.AddGrowableCol(2)
        panel.SetSizer(sizer)

    def bt_ScanRepairClick(self, event):
        ## DEBUG
        self.tc_MainDatabase.Value = "test.db"

        if self.tc_MainDatabase.Value == "":
            self.LogWindow.Value += "ERROR:\tNo database name selected!\n"
        else:
            scanCMD = "./scan -d " + self.tc_MainDatabase.Value + " -r"
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

    def bt_TargetDatabaseClick(self, event):
        # Create a list of filters
        filters = 'Text files (*.db)|*.db|All files (*.*)|*.*'
        dialog = wx.FileDialog ( None, message = 'Select Database File...',
            wildcard = filters, style = wxOPEN )

        # Open Dialog Box and get Selection
        if dialog.ShowModal() == wxID_OK:
            selected = dialog.GetFilenames()
            for selection in selected:
                self.tc_TargetDatabase.Value = selection
        dialog.Destroy()

    
    def bt_ExtractClick(self, event):

        ## DEBUG
        self.tc_MainDatabase.Value = "test.db"

        if self.tc_MainDatabase.Value == "":
            self.LogWindow.Value += "ERROR:\tNo database name selected!\n"
        else:
            scanCMD = "./scan -d " + self.tc_MainDatabase.Value + " "

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
                #self.LogWindow.Value += scanCMD

                proc = subprocess.Popen([scanCMD],shell=True,stdout=subprocess.PIPE)
                for line in proc.communicate()[0]:
                    self.LogWindow.AppendText(line)
