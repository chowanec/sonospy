###############################################################################
# Launch Tab for use with sonospyGUI.py
###############################################################################
# Copyright, blah, blah
###############################################################################
# TODO:
# - Connect Show Duplicates
# - Add refresh button
# - Limit the max number of proxies based on what Mark is doing in his code.
# - Windowsify the command line commands.
###############################################################################

import wx
from wxPython.wx import *
import os
import subprocess
import guiFunctions

list_checkboxID = []
list_checkboxLabel = []
list_txtctrlID = []
list_txtctrlLabel = []
list_buttonID = []

class PrefsPanel(wx.Panel):
    """
    Launch Tab for finding and launching .db files
    """
    #----------------------------------------------------------------------


    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        panel = self
        sizer = wx.GridBagSizer(11, 3)
        
        xIndex = 0
        yIndex = 0

    # [0] Make Header Columns --------------------------
        label_ProxyName = wx.StaticText(panel, label="Display Name")
        self.ck_EnableAll = wxCheckBox(panel, label="Enable All ")
        help_EnableAll = "Click here to enable or disable all the databases below."
        self.ck_EnableAll.SetToolTip(wx.ToolTip(help_EnableAll))
        self.ck_EnableAll.Bind(wx.EVT_CHECKBOX, self.enableAllChecks, self.ck_EnableAll)
        sizer.Add(label_ProxyName, pos=(xIndex, 2), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL|wx.TOP, border=10)
        sizer.Add(self.ck_EnableAll, pos=(xIndex, 0), span=(1,2), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL|wx.TOP, border=10)

        xIndex +=1
    # --------------------------------------------------------------------------
    # [1] Separator line ------------------------------------------------------

        hl_SepLine1 = wx.StaticLine(panel, 0, (250, 50), (300,1))
        sizer.Add(hl_SepLine1, pos=(xIndex, 0), span=(1, 3), flag=wx.EXPAND)
        xIndex +=1

    # --------------------------------------------------------------------------
    # [2-9] Checkbox, database name and proxy name field, plus browse button
    #   [2]
        ck_DB1 = wx.CheckBox(self, -1, "<add .db file>")
        ck_DB1.SetToolTip(wx.ToolTip("Click here to enable/disable this database for launch."))
        tc_DB1 = wx.TextCtrl(panel)
        tc_DB1.SetToolTip(wx.ToolTip("Enter a name for display on your Sonos Controller."))
        bt_DB1 = wx.Button(self, label="Browse")

        sizer.Add(ck_DB1, pos=(xIndex,0), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(tc_DB1, pos=(xIndex,1), span=(1,2),flag=wx.EXPAND|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(bt_DB1, pos=(xIndex, 3), flag=wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

        #-------------------------------------------------------
        # Save references to the widgets created dynamically
        list_checkboxID.append(ck_DB1.GetId())
        list_checkboxLabel.append(ck_DB1.GetLabel())
        list_txtctrlID.append(tc_DB1.GetId())
        list_txtctrlLabel.append(tc_DB1.Value)
        list_buttonID.append(bt_DB1.GetId())

        ck_DB1.Bind(wx.EVT_CHECKBOX, self.OnCheck, ck_DB1)
        bt_DB1.Bind(wx.EVT_BUTTON, self.browseDB, bt_DB1)

        xIndex +=1

    #   [3]
        ck_DB2 = wx.CheckBox(self, -1, "<add .db file>")
        ck_DB2.SetToolTip(wx.ToolTip("Click here to enable/disable this database for launch."))
        tc_DB2 = wx.TextCtrl(panel)
        tc_DB2.SetToolTip(wx.ToolTip("Enter a name for display on your Sonos Controller."))
        bt_DB2 = wx.Button(self, label="Browse")

        sizer.Add(ck_DB2, pos=(xIndex,0), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(tc_DB2, pos=(xIndex,1), span=(1,2),flag=wx.EXPAND|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(bt_DB2, pos=(xIndex, 3), flag=wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

        #-------------------------------------------------------
        # Save references to the widgets created dynamically
        list_checkboxID.append(ck_DB2.GetId())
        list_checkboxLabel.append(ck_DB2.GetLabel())
        list_txtctrlID.append(tc_DB2.GetId())
        list_txtctrlLabel.append(tc_DB2.Value)
        list_buttonID.append(bt_DB2.GetId())

        ck_DB2.Bind(wx.EVT_CHECKBOX, self.OnCheck, ck_DB2)
#        bt_DB2.Bind(wx.EVT_BUTTON, self.browseDB(ck_DB2, tc_DB2), bt_DB2)

        xIndex +=1

    #   [4]
        ck_DB3 = wx.CheckBox(self, -1, "<add .db file>")
        ck_DB3.SetToolTip(wx.ToolTip("Click here to enable/disable this database for launch."))
        tc_DB3 = wx.TextCtrl(panel)
        tc_DB3.SetToolTip(wx.ToolTip("Enter a name for display on your Sonos Controller."))
        bt_DB3 = wx.Button(self, label="Browse")

        sizer.Add(ck_DB3, pos=(xIndex,0), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(tc_DB3, pos=(xIndex,1), span=(1,2),flag=wx.EXPAND|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(bt_DB3, pos=(xIndex, 3), flag=wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

        #-------------------------------------------------------
        # Save references to the widgets created dynamically
        list_checkboxID.append(ck_DB3.GetId())
        list_checkboxLabel.append(ck_DB3.GetLabel())
        list_txtctrlID.append(tc_DB3.GetId())
        list_txtctrlLabel.append(tc_DB3.Value)
        list_buttonID.append(bt_DB3.GetId())

        ck_DB3.Bind(wx.EVT_CHECKBOX, self.OnCheck, ck_DB3)
#        bt_DB3.Bind(wx.EVT_BUTTON, self.browseDB(ck_DB3, tc_DB3), bt_DB3)

        xIndex +=1

    #   [5]
        ck_DB4 = wx.CheckBox(self, -1, "<add .db file>")
        ck_DB4.SetToolTip(wx.ToolTip("Click here to enable/disable this database for launch."))
        tc_DB4 = wx.TextCtrl(panel)
        tc_DB4.SetToolTip(wx.ToolTip("Enter a name for display on your Sonos Controller."))
        bt_DB4 = wx.Button(self, label="Browse")

        sizer.Add(ck_DB4, pos=(xIndex,0), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(tc_DB4, pos=(xIndex,1), span=(1,2),flag=wx.EXPAND|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(bt_DB4, pos=(xIndex, 3), flag=wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

        #-------------------------------------------------------
        # Save references to the widgets created dynamically
        list_checkboxID.append(ck_DB4.GetId())
        list_checkboxLabel.append(ck_DB4.GetLabel())
        list_txtctrlID.append(tc_DB4.GetId())
        list_txtctrlLabel.append(tc_DB4.Value)
        list_buttonID.append(bt_DB4.GetId())

        ck_DB4.Bind(wx.EVT_CHECKBOX, self.OnCheck, ck_DB4)
#        bt_DB4.Bind(wx.EVT_BUTTON, self.browseDB(ck_DB4, tc_DB4), bt_DB4)

        xIndex +=1

    #   [6]
        ck_DB5 = wx.CheckBox(self, -1, "<add .db file>")
        ck_DB5.SetToolTip(wx.ToolTip("Click here to enable/disable this database for launch."))
        tc_DB5 = wx.TextCtrl(panel)
        tc_DB5.SetToolTip(wx.ToolTip("Enter a name for display on your Sonos Controller."))
        bt_DB5 = wx.Button(self, label="Browse")

        sizer.Add(ck_DB5, pos=(xIndex,0), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(tc_DB5, pos=(xIndex,1), span=(1,2),flag=wx.EXPAND|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(bt_DB5, pos=(xIndex, 3), flag=wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

        #-------------------------------------------------------
        # Save references to the widgets created dynamically
        list_checkboxID.append(ck_DB5.GetId())
        list_checkboxLabel.append(ck_DB5.GetLabel())
        list_txtctrlID.append(tc_DB5.GetId())
        list_txtctrlLabel.append(tc_DB5.Value)
        list_buttonID.append(bt_DB5.GetId())

        ck_DB5.Bind(wx.EVT_CHECKBOX, self.OnCheck, ck_DB5)
#        bt_DB5.Bind(wx.EVT_BUTTON, self.browseDB(ck_DB5, tc_DB5), bt_DB5)

        xIndex +=1

    #   [7]
        ck_DB6 = wx.CheckBox(self, -1, "<add .db file>")
        ck_DB6.SetToolTip(wx.ToolTip("Click here to enable/disable this database for launch."))
        tc_DB6 = wx.TextCtrl(panel)
        tc_DB6.SetToolTip(wx.ToolTip("Enter a name for display on your Sonos Controller."))
        bt_DB6 = wx.Button(self, label="Browse")

        sizer.Add(ck_DB6, pos=(xIndex,0), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(tc_DB6, pos=(xIndex,1), span=(1,2),flag=wx.EXPAND|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(bt_DB6, pos=(xIndex, 3), flag=wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

        #-------------------------------------------------------
        # Save references to the widgets created dynamically
        list_checkboxID.append(ck_DB6.GetId())
        list_checkboxLabel.append(ck_DB6.GetLabel())
        list_txtctrlID.append(tc_DB6.GetId())
        list_txtctrlLabel.append(tc_DB6.Value)
        list_buttonID.append(bt_DB6.GetId())

        ck_DB6.Bind(wx.EVT_CHECKBOX, self.OnCheck, ck_DB6)
#        bt_DB6.Bind(wx.EVT_BUTTON, self.browseDB(ck_DB6, tc_DB6), bt_DB6)

        xIndex +=1

    #   [8]
        ck_DB7 = wx.CheckBox(self, -1, "<add .db file>")
        ck_DB7.SetToolTip(wx.ToolTip("Click here to enable/disable this database for launch."))
        tc_DB7 = wx.TextCtrl(panel)
        tc_DB7.SetToolTip(wx.ToolTip("Enter a name for display on your Sonos Controller."))
        bt_DB7 = wx.Button(self, label="Browse")

        sizer.Add(ck_DB7, pos=(xIndex,0), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(tc_DB7, pos=(xIndex,1), span=(1,2),flag=wx.EXPAND|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(bt_DB7, pos=(xIndex, 3), flag=wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

        #-------------------------------------------------------
        # Save references to the widgets created dynamically
        list_checkboxID.append(ck_DB7.GetId())
        list_checkboxLabel.append(ck_DB7.GetLabel())
        list_txtctrlID.append(tc_DB7.GetId())
        list_txtctrlLabel.append(tc_DB7.Value)
        list_buttonID.append(bt_DB7.GetId())

        ck_DB7.Bind(wx.EVT_CHECKBOX, self.OnCheck, ck_DB7)
#        bt_DB7.Bind(wx.EVT_BUTTON, self.browseDB(ck_DB7, tc_DB7), bt_DB7)

        xIndex +=1

    #   [9]
        ck_DB8 = wx.CheckBox(self, -1, "<add .db file>")
        ck_DB8.SetToolTip(wx.ToolTip("Click here to enable/disable this database for launch."))
        tc_DB8 = wx.TextCtrl(panel)
        tc_DB8.SetToolTip(wx.ToolTip("Enter a name for display on your Sonos Controller."))
        bt_DB8 = wx.Button(self, label="Browse")

        sizer.Add(ck_DB8, pos=(xIndex,0), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(tc_DB8, pos=(xIndex,1), span=(1,2),flag=wx.EXPAND|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(bt_DB8, pos=(xIndex, 3), flag=wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)

        #-------------------------------------------------------
        # Save references to the widgets created dynamically
        list_checkboxID.append(ck_DB8.GetId())
        list_checkboxLabel.append(ck_DB8.GetLabel())
        list_txtctrlID.append(tc_DB8.GetId())
        list_txtctrlLabel.append(tc_DB8.Value)
        list_buttonID.append(bt_DB8.GetId())

        ck_DB8.Bind(wx.EVT_CHECKBOX, self.OnCheck, ck_DB8)
#        bt_DB8.Bind(wx.EVT_BUTTON, self.browseDB(ck_DB8, tc_DB8), bt_DB8)

        xIndex +=1

#   If you want to autogenerate DB list and increment sizer Index, uncomment
#   the below

#     Get a count of *.db from the filesystem
#        numDB = guiFunctions.scrubDB(os.getcwd())
#
#        # Checkbox (enable, disable for launch)
#        # textCtrl (for Proxy name in controller)
#        # database name (based on *.db)
#        for db in numDB:
#            if xIndex >= 12:
#                pass
#                xIndex += 1
#            else:
#                check = wx.CheckBox(self, -1, db)
#                check.SetToolTip(wx.ToolTip("Click here to enable/disable this database for launch."))
#                sizer.Add(check, pos=(xIndex,0), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=10)
#                label = wx.StaticText(panel, label="")
#                sizer.Add(label, pos=(xIndex,1), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=10)
#                name = wx.TextCtrl(panel)
#                name.SetToolTip(wx.ToolTip("Enter a name for display on your Sonos Controller."))
#                #Set Temp Name
#                if db.endswith('.db'):
#                    name.Value = db[:-3]
#                sizer.Add(name, pos=(xIndex,2), span=(1,3),flag=wx.EXPAND|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
#                xIndex +=1
#
#            #-------------------------------------------------------
#            # Save references to the widgets created dynamically
#                list_checkboxID.append(check.GetId())
#                list_checkboxLabel.append(check.GetLabel())
#                list_txtctrlID.append(name.GetId())
#                list_txtctrlLabel.append(name.Value)
#
#            # Bind to event for later (DEBUG)
#                check.Bind(wx.EVT_CHECKBOX, self.OnCheck, check)

    # --------------------------------------------------------------------------
    # [12] Separator line ------------------------------------------------------

        hl_SepLine1 = wx.StaticLine(panel, 0, (250, 50), (300,1))
        sizer.Add(hl_SepLine1, pos=(12, 0), span=(1, 3), flag=wx.EXPAND)

    # --------------------------------------------------------------------------
    # [13] Create and add a launch button and radios for Proxy vs. Web
    # Eventually add "Use Sorts" and "Remove Dupes"
        self.bt_Launch = wx.Button(panel, label="Launch")
        help_bt_Launch = "Click here to launch the Sonospy service."
        self.bt_Launch.SetToolTip(wx.ToolTip(help_bt_Launch))
        self.bt_Launch.Bind(wx.EVT_BUTTON, self.bt_LaunchClick, self.bt_Launch)
        self.rd_Proxy = wx.RadioButton(panel, label="Proxy")
        help_rd_Proxy = "Run only as a proxy service in the background."
        self.rd_Proxy.SetToolTip(wx.ToolTip(help_rd_Proxy))
        self.rd_Web = wx.RadioButton(panel, label="Web")
        help_rd_Web = "Run as the web interface to Sonospy."
        self.rd_Web.SetToolTip(wx.ToolTip(help_rd_Web))

        if guiFunctions.configMe("launch", "proxy", bool=True) == True:
            self.rd_Proxy.SetValue(True)
        else:
            self.rd_Web.SetValue(True)

        sizer.Add(self.bt_Launch, pos=(13,0), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(self.rd_Proxy, pos=(13,1), flag=wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(self.rd_Web, pos=(13,2), flag=wx.ALIGN_CENTER_VERTICAL, border=10)

        sizer.AddGrowableCol(2)
        panel.SetSizer(sizer)
        panel.Refresh()

    def browseDB(self, event):
        filters = 'Text files (*.db)|*.db|All files (*.*)|*.*'
        dialog = wx.FileDialog ( None, message = 'Select Database File...', wildcard = filters, style = wxOPEN)

        # Open Dialog Box and get Selection
        if dialog.ShowModal() == wxID_OK:
            selected = dialog.GetFilenames()
            for selection in selected:
                tc.Value = selection
                guiFunctions.statusText(self, "Database: " + selection + " selected...")
        dialog.Destroy()
    
    def OnCheck(self, event):

# DEBUG ------------------------------------------------------------------------
#        for item in range(len(list_checkboxID)):
#            print "Checkbox " + str(item) + ":\t\t\tID:" + str(list_checkboxID[item]) + "\tLABEL:" + list_checkboxLabel[item]
#            print "Text Control " + str(item) + ":\t\tID:" + str(list_txtctrlID[item]) + "\tLABEL:" + list_txtctrlLabel[item]
# ------------------------------------------------------------------------------

        pass

    def enableAllChecks(self, event):
        if self.ck_EnableAll.Value == True:
            self.ck_EnableAll.Label = "Disable All"
        else:
            self.ck_EnableAll.Label = "Enable All"

        for item in range(len(list_checkboxID)):
            wx.FindWindowById(list_checkboxID[item]).Value = self.ck_EnableAll.Value

    def bt_LaunchClick(self, event):
        # back up to the folder below our current one.  save cwd in variable
        owd = os.getcwd()
        os.chdir(os.pardir)

        launchCMD = "./sonospy_"

        # which version are we running?
        if self.rd_Proxy.Value == True:
            launchCMD += "proxy "
        else:
            launchCMD += "web "

        # rebuild text labels now, user may have changed them
        for item in range(len(list_checkboxID)):
            list_txtctrlLabel[item] = wxFindWindowById(list_txtctrlID[item]).Value

        # build out the command
        if self.bt_Launch.Label == "Stop":
            launchCMD = "./sonospy_stop"
        else:
            for item in range(len(list_checkboxID)):
                if wx.FindWindowById(list_checkboxID[item]).Value == True:
                    launchCMD += "-wSonospy=" + list_txtctrlLabel[item] + "," + list_checkboxLabel[item] + " "

# DEBUG ------------------------------------------------------------------------
#            print launchCMD
# ------------------------------------------------------------------------------

        proc = subprocess.Popen([launchCMD],shell=True)

        if self.bt_Launch.Label == "Stop":
            self.bt_Launch.Label = "Launch"
            self.bt_Launch.SetToolTip(wx.ToolTip("Click here to launch the Sonospy service."))
            guiFunctions.statusText(self, "Sonospy Service Stopped...")
        else:
            self.bt_Launch.Label = "Stop"
            self.bt_Launch.SetToolTip(wx.ToolTip("Click here to stop the Sonospy service."))
            guiFunctions.statusText(self, "Sonospy Service Started...")

        # set back to original working directory
        os.chdir(owd)

