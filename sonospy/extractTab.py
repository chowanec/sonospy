###############################################################################
# Extract Tab for use with sonospyGUI.py
###############################################################################
# Copyright, blah, blah
###############################################################################
# TODO:
#      - STDOUT to LogView.Value in realtime. Broken in WorkerThread?
#      - Tons and tons of error checking (check for int on relevant fields)
###############################################################################

import wx
from wxPython.wx import *
import os
import subprocess
from threading import *

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

class ExtractPanel(wx.Panel):
    """
    Extract Tab for creating subset databases.
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

        self.bt_MainDatabase = wx.Button(panel, label="Browse...")
        sizer.Add(self.bt_MainDatabase, pos=(0, 5), flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_VERTICAL, border=10)
        self.bt_MainDatabase.Bind(wx.EVT_BUTTON, self.bt_MainDatabaseClick, self.bt_MainDatabase)
    # --------------------------------------------------------------------------
    # [1] Target Database Label, Entry and Browse Button -----------------------

        # Create the label, text control and button
        label_TargetDatabase = wx.StaticText(panel, label="Target Database:")
        self.tc_TargetDatabase = wx.TextCtrl(panel)
        self.bt_TargetDatabase = wx.Button(panel, label="Browse...")

        # Add them to the sizer.
        sizer.Add(label_TargetDatabase, pos=(1, 0), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL|wx.TOP, border=10)
        sizer.Add(self.tc_TargetDatabase, pos=(1, 1), span=(1, 4), flag=wx.TOP|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(self.bt_TargetDatabase, pos=(1, 5), flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_VERTICAL, border=10)

        # Bind the button to a click event
        self.bt_TargetDatabase.Bind(wx.EVT_BUTTON, self.bt_TargetDatabaseClick,self.bt_TargetDatabase)
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
        self.combo_LogicalCreated = wx.ComboBox(panel, 1, "", (25, 25), (60, 25), logicList, wx.CB_DROPDOWN)
        self.combo_LogicalCreated.Select(1)
        self.tc_DaysAgoCreated = wx.TextCtrl(panel)
        label_DaysAgoCreated = wx.StaticText(panel, label="days ago")
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsCreated, pos=(sizerIndexX, 0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(self.combo_LogicalCreated, pos=(sizerIndexX,1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=1)
        OptionBoxSizer.Add(self.tc_DaysAgoCreated, pos=(sizerIndexX, 2), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)
        OptionBoxSizer.Add(label_DaysAgoCreated, pos=(sizerIndexX,3), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)

        # Inserted
        sizerIndexX += 1
        label_OptionsInserted = wx.StaticText(panel, label="Inserted:")
        self.combo_LogicalInserted = wx.ComboBox(panel, 1, "", (25, 25), (60, 25), logicList, wx.CB_DROPDOWN)
        self.combo_LogicalInserted.Select(1)
        self.tc_DaysAgoInserted = wx.TextCtrl(panel)
        label_DaysAgoInserted = wx.StaticText(panel, label="days ago")
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsInserted, pos=(sizerIndexX, 0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(self.combo_LogicalInserted, pos=(sizerIndexX,1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=1)
        OptionBoxSizer.Add(self.tc_DaysAgoInserted, pos=(sizerIndexX, 2), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)
        OptionBoxSizer.Add(label_DaysAgoInserted, pos=(sizerIndexX,3), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)

        # Modified
        sizerIndexX += 1
        label_OptionsModified = wx.StaticText(panel, label="Modified:")
        self.combo_LogicalModified = wx.ComboBox(panel, 1, "", (25, 25), (60, 25), logicList, wx.CB_DROPDOWN)
        self.combo_LogicalModified.Select(1)
        self.tc_DaysAgoModified = wx.TextCtrl(panel)
        label_DaysAgoModified = wx.StaticText(panel, label="days ago")
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsModified, pos=(sizerIndexX, 0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(self.combo_LogicalModified, pos=(sizerIndexX,1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=1)
        OptionBoxSizer.Add(self.tc_DaysAgoModified, pos=(sizerIndexX, 2), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)
        OptionBoxSizer.Add(label_DaysAgoModified, pos=(sizerIndexX,3), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)

        # Accessed
        sizerIndexX += 1
        label_OptionsAccessed = wx.StaticText(panel, label="Accessed:")
        self.combo_LogicalAccessed = wx.ComboBox(panel, 1, "", (25, 25), (60, 25), logicList, wx.CB_DROPDOWN)
        self.combo_LogicalAccessed.Select(1)
        self.tc_DaysAgoAccessed = wx.TextCtrl(panel)
        label_DaysAgoAccessed = wx.StaticText(panel, label="days ago")
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsAccessed, pos=(sizerIndexX, 0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(self.combo_LogicalAccessed, pos=(sizerIndexX,1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=1)
        OptionBoxSizer.Add(self.tc_DaysAgoAccessed, pos=(sizerIndexX, 2), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)
        OptionBoxSizer.Add(label_DaysAgoAccessed, pos=(sizerIndexX,3), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)

        # Year
        sizerIndexX += 1
        label_OptionsYear = wx.StaticText(panel, label="Year Recorded:")
        self.combo_LogicalYear = wx.ComboBox(panel, 1, "", (25, 25), (60, 25), logicList, wx.CB_DROPDOWN)
        self.combo_LogicalYear.Select(1)
        self.tc_Year = wx.TextCtrl(panel)
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsYear, pos=(sizerIndexX, 0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(self.combo_LogicalYear, pos=(sizerIndexX,1), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=1)
        OptionBoxSizer.Add(self.tc_Year, pos=(sizerIndexX, 2), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)

        # Genre
        sizerIndexX += 1
        label_OptionsGenre = wx.StaticText(panel, label="Genre:")
        self.tc_Genre = wx.TextCtrl(panel)
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsGenre, pos=(sizerIndexX, 0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(self.tc_Genre, pos=(sizerIndexX, 1), span=(1,2), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=0)

        # Artist
        sizerIndexX += 1
        label_OptionsArtist = wx.StaticText(panel, label="Artist:")
        self.tc_Artist = wx.TextCtrl(panel)
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsArtist, pos=(sizerIndexX, 0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(self.tc_Artist, pos=(sizerIndexX, 1), span=(1,2), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=0)

        # Composer
        sizerIndexX += 1
        label_OptionsComposer = wx.StaticText(panel, label="Composer:")
        self.tc_Composer = wx.TextCtrl(panel)
        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsComposer, pos=(sizerIndexX, 0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(self.tc_Composer, pos=(sizerIndexX, 1), span=(1,2), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=0)

        # Bit-rate
        sizerIndexX += 1
        label_OptionsBitrate = wx.StaticText(panel, label="Bitrate:")
        self.combo_LogicalBitrate = wx.ComboBox(panel, 1, "", (25, 25), (60, 25), logicList, wx.CB_DROPDOWN)
        self.combo_LogicalBitrate.Select(1)
        self.tc_Bitrate = wx.TextCtrl(panel)

        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_OptionsBitrate, pos=(sizerIndexX, 0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(self.combo_LogicalBitrate, pos=(sizerIndexX, 1), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)
        OptionBoxSizer.Add(self.tc_Bitrate, pos=(sizerIndexX, 2), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)

        # Last X Albums
        sizerIndexX += 1
        label_Last = wx.StaticText(panel, label="Last:")
        self.tc_Last = wx.TextCtrl(panel)
        label_Albums = wx.StaticText(panel, label="Albums")

        # Add them to the sizer (optionBoxSizer)
        OptionBoxSizer.Add(label_Last, pos=(sizerIndexX, 0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, border=0)
        OptionBoxSizer.Add(self.tc_Last, pos=(sizerIndexX, 1), span=(1,2), flag=wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)
        OptionBoxSizer.Add(label_Albums, pos=(sizerIndexX, 3), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, border=0)

        OptionBoxSizer.AddGrowableCol(4)
        sbs_ExtractOptions.Add(OptionBoxSizer, flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(sbs_ExtractOptions, pos=(2, 0), span=(1,6),flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=10)

    # --------------------------------------------------------------------------
    # [3] Add Scan Options and Scan Button -------------------------------------
        self.bt_Extract = wx.Button(panel, label="Extract")
        self.bt_Extract.Bind(wx.EVT_BUTTON, self.bt_ExtractClick, self.bt_Extract)
        self.ck_ExtractVerbose = wx.CheckBox(panel, label="Verbose")
        self.bt_SaveLog = wx.Button(panel, label="Save to Log")
        self.bt_SaveLog.Bind(wx.EVT_BUTTON, self.bt_SaveLogClick, self.bt_SaveLog)
        self.ck_OverwriteExisting = wx.CheckBox(panel, label="Overwrite")

        sizer.Add(self.bt_Extract, pos=(3,0), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(self.ck_ExtractVerbose, pos=(3,2), flag=wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(self.ck_OverwriteExisting, pos=(3,3), flag=wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(self.bt_SaveLog, pos=(3,1), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.RIGHT, border=10)

    # --------------------------------------------------------------------------
    # [4] Separator line ------------------------------------------------------
        hl_SepLine2 = wx.StaticLine(panel, 0, (250, 50), (300,1))
        sizer.Add(hl_SepLine2, pos=(4, 0), span=(1, 6), flag=wx.EXPAND, border=10)
    # --------------------------------------------------------------------------
    # [5] Output/Log Box -------------------------------------------------------
        self.LogWindow = wx.TextCtrl(panel, -1,"",size=(100, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.LogWindow.SetInsertionPoint(0)
        self.LogWindow.Disable()
        sizer.Add(self.LogWindow, pos=(5,0), span=(1,6), flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

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
            self.setButtons(True)
        else:
            # Process results here
            self.LogWindow.AppendText(event.data)
        # In either event, the worker is done
        self.worker = None

    def bt_MainDatabaseClick(self, event):
        # Create a list of filters
        filters = 'Text files (*.db)|*.db|All files (*.*)|*.*'
        dialog = wx.FileDialog ( None, message = 'Select Database File...', wildcard = filters, style = wxOPEN)

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

    def setButtons(self, state):
        """
        Toggle for the button states.
        """
        if state == True:
            self.bt_Extract.Enable()
            self.bt_MainDatabase.Enable()
            self.bt_SaveLog.Enable()
            self.bt_TargetDatabase.Enable()
            self.ck_ExtractVerbose.Enable()
            self.ck_OverwriteExisting.Enable()
            wx.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        else:
            self.bt_Extract.Disable()
            self.bt_MainDatabase.Disable()
            self.bt_SaveLog.Disable()
            self.bt_TargetDatabase.Disable()
            self.ck_ExtractVerbose.Disable()
            self.ck_OverwriteExisting.Disable()
            wx.SetCursor(wx.StockCursor(wx.CURSOR_WATCH))

    def bt_ExtractClick(self, event):
        global scanCMD
        global getOpts
        self.LogWindow.Enable()

# DEBUG ------------------------------------------------------------------------
#        self.tc_MainDatabase.Value = "test.db"
#        self.tc_TargetDatabase.Value = "test2.db"
# ------------------------------------------------------------------------------
        if self.tc_MainDatabase.Value == "":
            self.LogWindow.AppendText("ERROR:\tNo source database name selected!\n")
        elif self.tc_TargetDatabase.Value == "":
            self.LogWindow.AppendText("ERROR:\tNo target database name selected.\n")
        elif self.tc_MainDatabase.Value == self.tc_TargetDatabase.Value:
            self.LogWindow.AppendText("ERROR:\tSource database and target database cannot be the same database!\n")
        else:
            searchCMD = ""
            # Scrub the fields to see what our extract command should be.
            # Eventually stack these with some sort of AND query.

            if self.tc_DaysAgoCreated.Value != "":
                if searchCMD == "":
                    searchCMD = "where (julianday(datetime(\'now\')) - julianday(datetime(created, \'unixepoch\'))) " + self.combo_LogicalCreated.Value + " " + self.tc_DaysAgoCreated.Value
                else:
                    searchCMD += " AND where (julianday(datetime(\'now\')) - julianday(datetime(created, \'unixepoch\'))) " + self.combo_LogicalCreated.Value + " " + self.tc_DaysAgoCreated.Value

            if self.tc_DaysAgoInserted.Value != "":
                if searchCMD == "":
                    searchCMD = "where (julianday(datetime(\'now\')) - julianday(datetime(inserted, \'unixepoch\'))) " + self.combo_LogicalInserted.Value + " " + self.tc_DaysAgoInserted.Value
                else:
                    searchCMD += " AND where (julianday(datetime(\'now\')) - julianday(datetime(inserted, \'unixepoch\'))) " + self.combo_LogicalInserted.Value + " " + self.tc_DaysAgoInserted.Value

            if self.tc_DaysAgoModified.Value != "":
                if searchCMD == "":
                    searchCMD = "where (julianday(datetime(\'now\')) - julianday(datetime(lastmodified, \'unixepoch\'))) " + self.combo_LogicalModified.Value + " " + self.tc_DaysAgoModified.Value
                else:
                    searchCMD += " AND where (julianday(datetime(\'now\')) - julianday(datetime(lastmodified, \'unixepoch\'))) " + self.combo_LogicalModified.Value + " " + self.tc_DaysAgoModified.Value

            if self.tc_DaysAgoAccessed.Value != "":
                if searchCMD == "":
                    searchCMD = "where (julianday(datetime(\'now\')) - julianday(datetime(lastaccessed, \'unixepoch\'))) " + self.combo_LogicalAccessed.Value + " " + self.tc_DaysAgoAccessed.Value
                else:
                    searchCMD += " AND where (julianday(datetime(\'now\')) - julianday(datetime(lastaccessed, \'unixepoch\'))) " + self.combo_LogicalAccessed.Value + " " + self.tc_DaysAgoAccessed.Value

            if self.tc_Year.Value != "":
                if searchCMD == "":
                    searchCMD = "where year " + self.combo_LogicalYear.Value + " " + self.tc_Year.Value
                else:
                    searchCMD += " AND where year " + self.combo_LogicalYear.Value + " " + self.tc_Year.Value

            if self.tc_Genre.Value != "":
                if searchCMD == "":
                    searchCMD = "where genre=\'" + self.tc_Genre.Value + "\'"
                else:
                    searchCMD += " AND where genre=\'" + self.tc_Genre.Value + "\'"

            if self.tc_Artist.Value != "":
                if searchCMD == "":
                    searchCMD = "where artist=\'" + self.tc_Artist.Value + "\'"
                else:
                    searchCMD += " AND where artist=\'" + self.tc_Artist.Value + "\'"

            if self.tc_Composer.Value != "":
                if searchCMD == "":
                    searchCMD = " AND where composer=\'" + self.tc_Composer.Value + "\'"
                else:
                    searchCMD += " AND where composer=\'" + self.tc_Composer.Value + "\'"

            if self.tc_Bitrate.Value != "":
                if searchCMD == "":
                    searchCMD = "where bitrate " + self.combo_LogicalBitrate.Value + " " + self.tc_Bitrate.Value
                else:
                    searchCMD += "AND where bitrate " + self.combo_LogicalBitrate.Value + " " + self.tc_Bitrate.Value

            if self.tc_Last.Value != "":
                if searchCMD != "":
                    self.LogWindow.AppendText("You cannot combine Last " + self.tc_Last.Value + " albums with other search options...")
                else:
                    searchCMD = "AS t WHERE t.created >= (SELECT a.created FROM albums AS a WHERE a.albumartist != 'Various Artists' ORDER BY a.created DESC LIMIT " + str(int(self.tc_Last.Value) - 1) + ",1)"

            if searchCMD !="":
                searchCMD = "\"" + searchCMD + "\""

                if self.ck_OverwriteExisting.Value == True:
                    if os.path.exists(self.tc_TargetDatabase.Value) == True:
                        illegals = ["/", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "+","=",","]
                        for illegal in illegals:
                            if illegal in self.tc_TargetDatabase.Value:
                                self.LogWindow.AppendText("\nERROR:\tInvalid target database! You cannot use " + illegal + " in the database name.")
                                return(1)
                        delME = "rm -I " + self.tc_TargetDatabase.Value
                        proc = subprocess.Popen([delME],shell=True,stdout=subprocess.PIPE)

                getOpts = ""
                if self.ck_ExtractVerbose.Value == True:
                    getOpts = "-v "

                scanCMD = "./scan " + getOpts +"-d " + self.tc_MainDatabase.Value + " -x " + self.tc_TargetDatabase.Value + " -w " + searchCMD
                self.LogWindow.AppendText("\nExtracting from " + self.tc_MainDatabase.Value +" into " + self.tc_TargetDatabase.Value + "...\n\n")

# DEBUG ------------------------------------------------------------------------
#                self.LogWindow.AppendText(scanCMD)
# ------------------------------------------------------------------------------

# Multithreading is below this line.
                if not self.worker:
                    self.worker = WorkerThread(self)
                    self.setButtons(False)
# ------------------------------------------------------------------------------
            else:
                self.LogWindow.AppendText("\nERROR:\tYou have no extract options selected!")
                
    def bt_SaveLogClick(self, event):
        dialog = wx.FileDialog(self, message='Choose a file', style=wx.SAVE|wx.OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            savefile = dialog.GetFilename()
            saveMe = open(savefile, 'w')
            saveMe.write(self.LogWindow.Value)
            saveMe.close()
