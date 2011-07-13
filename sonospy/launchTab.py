###############################################################################
# Launch Tab for use with sonospyGUI.py
###############################################################################
# Copyright, blah, blah
###############################################################################
# TODO:
#      - Layout
#      - Connect Web only
#      - Connect Proxy only
#      - Connect Sort ck
#      - Connect Show Duplicates
#      - Add refresh button
#
#      - Populate proxy based on *.db
###############################################################################

import wx
from wxPython.wx import *
import os
import subprocess
import re

class ExtractPanel(wx.Panel):
    """
    Scan Tab for running Sonospy Database Scans, Updates and Repairs
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        panel = self
        sizer = wx.GridBagSizer(1, 3)
        self.currentDirectory = os.getcwd()
        xIndex = 0
        yIndex = 0

	# [0] Make Header Columns  --------------------------
        label_ProxyName = wx.StaticText(panel, label="Display Name")
        self.ck_EnableAll = wxCheckBox(panel, label="Enable All")

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
		check = wx.CheckBox(self, -1, db)
		sizer.Add(check, pos=(xIndex,0), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=10)
	        label = wx.StaticText(panel, label="")
		sizer.Add(label, pos=(xIndex,1), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=10)
		name = wx.TextCtrl(panel)
		sizer.Add(name, pos=(xIndex,2), span=(1,3),flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.TOP, border=5)
		xIndex +=1
	#-------------------------------------------------------


        sizer.AddGrowableCol(2)
        panel.SetSizer(sizer)

def scrubDB(path):
    asps = []
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith('.db'):
                    asps.append(file)
    return asps

