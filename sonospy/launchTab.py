###############################################################################
# Launch Tab for use with sonospyGUI.py
###############################################################################
# Copyright, blah, blah
###############################################################################
# TODO:
#    - Layout
#    - Connect Web only
#    - Connect Proxy only
#    - Connect Sort ck
#    - Connect Show Duplicates
#    - Add refresh button
#    - Fix the core command to work on Windows and not be so janky (i.e. remove
#      the cd .. and cd -)
###############################################################################

import wx
from wxPython.wx import *
import os
import subprocess
import re

list_checkboxID = []
list_checkboxLabel = []
list_txtctrlID = []
list_txtctrlLabel = []

class LaunchPanel(wx.Panel):
    """
    Launch Tab for finding and launching .db files
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        panel = self
        sizer = wx.GridBagSizer(11, 3)
        self.currentDirectory = os.getcwd()
        xIndex = 0
        yIndex = 0

    # [0] Make Header Columns  --------------------------
        label_ProxyName = wx.StaticText(panel, label="Display Name")
        self.ck_EnableAll = wxCheckBox(panel, label="Enable All  ")
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
    # [2] Generate DB list and increment sizer Index

    # Get a count of *.db from the filesystem
        numDB = scrubDB(os.getcwd())

        # Checkbox (enable, disable for launch)
        # textCtrl (for Proxy name in controller)
        # database name (based on *.db)
        for db in numDB:
            if xIndex >= 12:
                pass
                xIndex += 1
            else:
                check = wx.CheckBox(self, -1, db)
                sizer.Add(check, pos=(xIndex,0), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=10)
                label = wx.StaticText(panel, label="")
                sizer.Add(label, pos=(xIndex,1), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=10)
                name = wx.TextCtrl(panel)
                #Set Temp Name
                if db.endswith('.db'):
                    name.Value = db[:-3]
                sizer.Add(name, pos=(xIndex,2), span=(1,3),flag=wx.EXPAND|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
                xIndex +=1

            #-------------------------------------------------------
            # Save references to the widgets created dynamically
                list_checkboxID.append(check.GetId())
                list_checkboxLabel.append(check.GetLabel())
                list_txtctrlID.append(name.GetId())
                list_txtctrlLabel.append(name.Value)

            # Bind to event for later (DEBUG)
                check.Bind(wx.EVT_CHECKBOX, self.OnCheck, check)

    # --------------------------------------------------------------------------
    # [12] Separator line ------------------------------------------------------

        hl_SepLine1 = wx.StaticLine(panel, 0, (250, 50), (300,1))
        sizer.Add(hl_SepLine1, pos=(12, 0), span=(1, 3), flag=wx.EXPAND)

    # --------------------------------------------------------------------------
    # [13] Create and add a launch button and radios for Proxy vs. Web
    # Eventually add "Use Sorts" and "Remove Dupes"
        self.bt_Launch = wx.Button(panel, label="Launch")
        self.bt_Launch.Bind(wx.EVT_BUTTON, self.bt_LaunchClick, self.bt_Launch)
        self.rd_Proxy = wx.RadioButton(panel, label="Proxy")
        self.rd_Web = wx.RadioButton(panel, label="Web")

        sizer.Add(self.bt_Launch, pos=(13,0), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(self.rd_Proxy, pos=(13,1), flag=wx.ALIGN_CENTER_VERTICAL, border=10)
        sizer.Add(self.rd_Web, pos=(13,2), flag=wx.ALIGN_CENTER_VERTICAL, border=10)

        sizer.AddGrowableCol(2)
        panel.SetSizer(sizer)

    def OnCheck(self, event):
# DEBUG
#        for item in range(len(list_checkboxID)):
#            print "Checkbox " + str(item) + ":\t\t\tID:" + str(list_checkboxID[item]) + "\tLABEL:" + list_checkboxLabel[item]
#            print "Text Control " + str(item) + ":\t\tID:" + str(list_txtctrlID[item]) + "\tLABEL:" + list_txtctrlLabel[item]
        pass

    def enableAllChecks(self, event):
        if self.ck_EnableAll.Value == True:
            self.ck_EnableAll.Label = "Disable All"
        else:
            self.ck_EnableAll.Label = "Enable All"

        for item in range(len(list_checkboxID)):
            wx.FindWindowById(list_checkboxID[item]).Value = self.ck_EnableAll.Value

    def bt_LaunchClick(self, event):
        # core command - fix this eventually
        launchCMD = "cd ..;./sonospy_"

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
            # Fix this later
            launchCMD = "cd ..;./sonospy_stop;cd -"
        else:
            for item in range(len(list_checkboxID)):
                if wx.FindWindowById(list_checkboxID[item]).Value == True:
                    launchCMD += "-wSonospy=" + list_txtctrlLabel[item] + "," + list_checkboxLabel[item] + " "
            # print it for debug
            print launchCMD
            # kludge to get me back to this directory
            launchCMD += ";cd -"

        proc = subprocess.Popen([launchCMD],shell=True)
        if self.bt_Launch.Label == "Stop":
            self.bt_Launch.Label = "Launch"
        else:
            self.bt_Launch.Label = "Stop"

def scrubDB(path):
    asps = []
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith('.db'):
                    asps.append(file)
    return asps


