###############################################################################
# guiFunctions - shared functions across the Sonospy GUI project.
###############################################################################
# Copyright, blah, blah
###############################################################################
# TODO:
# - Write out the config file
###############################################################################
from wxPython.wx import *

#-------------------------------------------------------------------------------
# configMe
#
# For reading and parsing the config file.
#-------------------------------------------------------------------------------
# TODO:
# - Handle deleted config entries in ini file?
# - Handle multi-line text box in config file?
#-------------------------------------------------------------------------------
import ConfigParser

def configMe(tab, term, integer=False, bool=False, parse=False):
    config = ConfigParser.ConfigParser()
    config.read("GUIpref.ini")

    if integer == True:
        fetchMe = config.getint(tab, term)
    elif bool == True:
        fetchMe = config.getboolean(tab, term)
    else:
        fetchMe = config.get(tab, term)

    if parse == True:
        fetchMe = fetchMe.replace(", ", ",")
        fetchMe = fetchMe.replace(",", "\n")
        fetchMe = str(fetchMe + "\n")

    if fetchMe == NULL:
        return 1;
    else:
        return(fetchMe)

#    # dump entire config file
#    for section in config.sections():
#        print section
#        for option in config.options(section):
#            print " ", option, "=", config.get(section, option)

#-------------------------------------------------------------------------------
# scrubDB
#
# Scours the provided path for *.db files to return back to the app so that we
# can dynamically create widgets for the launch tab
#-------------------------------------------------------------------------------
import os

def scrubDB(path):
    asps = []
    # replace "(path)" with os.path.abspath(os.path.join(path, os.path.pardir, os.path.pardir))
    # when this goes in gui/linux
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.db'):
                    asps.append(file)
    return asps

#-------------------------------------------------------------------------------
# statusText
#
# Simple function to set the status text in any of the other notebook tabs.
#-------------------------------------------------------------------------------
def statusText(object, line):
    object.GetParent().GetParent().GetParent().SetStatusText(line)
