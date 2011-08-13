#!/usr/bin/env python

# utest_scan
#
# scan, movetags, gettags copyright (c) 2010-2011 Mark Henkelis
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Barry Mossman <sonospy-devel@googlegroups.com.>

import unittest
import shlex
import scan
import sys
import os
import sqlite3
import re
import shutil
from gettags import getfilestat


# Acknowledgment: This program built and tested using Wing IDE from http://wingware.com/ .... great product.

'''
Is most convenient and illuminating way to run the unit tests from the Wing IDE. 

Otherwise running unit tests manually from the python command line (from http://docs.python.org/library/unittest.html#command-line-options):
<<<<<<<
The unittest module can be used from the command line to run tests from modules, classes or even individual test methods:

python -m unittest test_module1 test_module2
python -m unittest test_module.TestClass
python -m unittest test_module.TestClass.test_method

You can pass in a list with any combination of module names, and fully qualified class or method names.

You can run tests with more detail (higher verbosity) by passing in the -v flag.
>>>>>>>>
'''

#Define some global containing paths to test files and locations.
"""
Expected test file structure is:
+ "unit test files"            # (1) inside Sonosospy (ie. at the same level as "errors" & "logs
    + "music tracks"           # (2) 
        + "copy target location during update scan test"     # (3) empty directory
        + "tracks for main tests"            # (4) the tracks which will be read by the Initial Scan tests
        + "tracks for update scan art test"  # (5)  
        + "tracks for update scan test"      
            + "before update"        # (7)  containing tracks which will updated in Update Scan tests
            + "after update"         # (8) same tracks, but tag update as part of same Update Scan tests

It is important not to manually change the music tracks, as some of the the unit tests compare the data built 
in the database against expected values, and therefore these tests need to work with known input.
"""
g_test_db_name = 'unitTest.db'   #name of db that we will build. Will reside in the sonospy work directory. 
g_test_root_directory_name = 'unit_test_files'   #our test directory root
_music_tracks_root_container_name = "music_tracks"
_scan_update_test_directory_name = 'tracks_for_update_scan_test'
_scan_update_test_copy_target_name = 'copy_target_location_during_update_scan_test'
_scan_update_test_art_file_directory_name = 'tracks_for_update_scan_art_test'   
_scan_update_test_art_directory_name = 'tracks for_update_scan_test'  
g_test_root_directory_path = os.path.join(os.getcwd(), g_test_root_directory_name)  #(1) ... see diagram above
_initial_scan_tracks_path = os.path.join(g_test_root_directory_path, _music_tracks_root_container_name)   #(2)
assert os.path.exists(g_test_root_directory_path),'Cannot locate unit test file directory ({0}'.format(g_test_root_directory_name)
assert os.path.exists(_initial_scan_tracks_path),'Cannot locate unit test music track directory ({0}'.format(_initial_scan_tracks_path)
_music_track_path = os.path.join(_initial_scan_tracks_path, 'tracks_for_main_tests')    #(4)
assert os.path.exists(_music_track_path),'Cannot locate unit test music tracks directory ({0}'.format(_music_track_path)
g_update_scan_copy_target_path = os.path.join(_initial_scan_tracks_path, _scan_update_test_copy_target_name)   #(3)
g_update_scan_copy_source_BEFORE_path = os.path.join(_initial_scan_tracks_path, _scan_update_test_directory_name, 'before_update')  #(7)
g_update_scan_copy_source_AFTER_path = os.path.join(_initial_scan_tracks_path, _scan_update_test_directory_name, 'after_update')  #(8)
g_update_scan_art_test_path = os.path.join(_initial_scan_tracks_path, _scan_update_test_art_file_directory_name)  #(5)
g_update_scan_art_file_name = 'folder.jpg'
        
'''
 Setup string pointing to test file directory
 ... John!!! =====================================================================
Linux may not need all of this, althought it probably doesn't do any damage. The windows path separator is a backslash. 
In python a backslash is an escape character. To get a backslash accepted you need to supply two, as the first will be 
gobbled up doing its escape character duties. 
Mark's Scan processes the path, and gobbles half the backslashes. I snagged some code from Scan, so that goobles up half again. ... 
For this reason i need 2*2*2 = 8 backslashes just to get two arrive where it they are needed ... were they will get stripped down to 1, 
if you follow me..  The second .replace puts four back slashes ahead of any blank in the path; in the same way 2 are stripped 
off by the code which I snagged from Scan, then 1 (half the remaining 2) are stripped of by scan itself, that leaves one to 
provide an escape character to handle the imbedded blank in the path. 
    
 .. The windows path string passed to scan needs to have a lots of backslashes.
 .. ie. C:\Documents and settings\Foo would need  to be passed as
 ..     C:\\\\\\\\Documents\\\\and\\\\Settings\\\\\\\\Foo
 '''

_scan_path_with_slashes = _music_track_path.replace('\\','\\\\\\\\').replace(' ','\\\\ ')

_update_scan_track_path = os.path.join(_initial_scan_tracks_path, _scan_update_test_copy_target_name)
_update_scan_track_path_2 = os.path.join(_initial_scan_tracks_path, 'tracks_for_update_scan_art_test')
_update_scan_path_with_slashes = _update_scan_track_path.replace('\\','\\\\\\\\').replace(' ','\\\\ ')
_update_scan_path_2_with_slashes = _update_scan_track_path_2.replace('\\','\\\\\\\\').replace(' ','\\\\ ')

if sys.platform.startswith("win"):
    g_command_line_scan = '-d {0} {1}'.format(g_test_db_name, _scan_path_with_slashes)
    g_command_line_repair = '-d {0} -r'.format(g_test_db_name)
    g_command_line_update_scan = '-d {0} {1} {2}'.format(g_test_db_name, _update_scan_path_with_slashes, _update_scan_path_2_with_slashes )
elif sys.platform:.startswith("linux"):
    g_command_line_scan = '-d {0} {1}'.format(g_test_db_name, _scan_path_with_slashes)
    g_command_line_repair = '-d {0} -r'.format(g_test_db_name)
    g_command_line_update_scan = '-d {0} {1} {2}'.format(g_test_db_name, _update_scan_path_with_slashes, _update_scan_path_2_with_slashes )
else:
    g_command_line_scan = 'some other crap'
    g_command_line_repair = 'some other crap'
    g_command_line_update_scan = 'some other crap'
    raise Exception, '# REMOVE EXCEPTION when set up for MAC'

#
#General purpose functions
#  
    
"""
Define structure for parameter passed to the perform_and_assert_comparison method defined below.
"""
class prepare_row_comparison_parms(object):
    def __init__(self, tableName=None):
        self.tableName = tableName 
        
    tableName = csvFileName = queryString = whichRowStart = None
    ignoredRows = integerRows = realRows = None
    fixNumericNulls = fieldsContainingPaths = None
    dbRow = None  # True if passed row if from the database, False if it is from the CSV file 
    howManyRows = 1
    
    _default_params = {}
    
    # Albums table
    _work_params = {'ignored' : ('lastmodified','inserted','playcount','artid','created'),
                    'integer' : ('id','year','duplicate','artid','albumtype'),
                    'real'    : ('created','lastplayed'),
                    'nullnums': (),
                    'pathflds': ('cover',) }
    _default_params['albums'] = _work_params
    # Tracks table
    _work_params = {'ignored' : ('lastmodified','inserted','playcount','lastscanned','id','created'),
                    'integer' : ('duplicate','tracknumber','year','length','size','discnumber','bitrate','samplerate','bitspersample','channels','folderartid','trackartid','playcount'),
                    'real'    : ('created','lastplayed','lastplayed','lastscanned'),
                    'nullnums': ('tracknumber',),
                    'pathflds': ('path','folderart','trackart') }
    _default_params['tracks'] = _work_params
    
    
    def setDefault(self, table):
        try:
            self.ignoredRows = self._default_params[table]['ignored']
            self.integerRows = self._default_params[table]['integer']
            self.realRows = self._default_params[table]['real']
            self.fixNumericNulls = self._default_params[table]['nullnums']
            self.fieldsContainingPaths = self._default_params[table]['pathflds']            
        except (KeyError):
            print 'Invalid, or uncatered for, table type of "{0}"'.format(table)
            raise
    
    
"""
This service function obtains data from the database using a, test-specific query string, and then 
compares the obtained data against expected values which are stored in a test-specific CSV file.  
An assertion exception is raised if the database data fails the comparison.
"""
def perform_and_assert_comparison(self, param):
    isinstance(param, prepare_row_comparison_parms)   #provide assistnace to Wing IDE code completion
    """ -----------------------
    This nested function reads a CSV file containing the database values expected following 
    a Scan run over the known set of music tracks.
    
    For each row, that the unit test is interested in, it creates a dictionary. It then returns all 
    dictionaries in a list.
    
    The parameter which is passed is defined by the prepare_row_comparison_parms class above.
    
    Here is an extract from one for the Albums table. The field separator is a tab control character.
    The string quoting character is expected to be as shown.
    ---
    'id'	'parentID'	'album'	'artist'	'year'	
    300000001	'300000000'	'Pearl'	'Janis Joplin'	719559	
    300000002	'300000000'	'Between My Head and the Sky'	'Yoko Ono Plastic Ono Band'	733671
    ---
    
    The CSV files can be built by SQLite Data Wizard rom http://www.sqlmaestro.com/products/sqlite/datawizard/
    (using the data Export facility, and the templates, .extx files, found in the "unit test files" directory.
    Alternatively SQLite Meastro from the same vendor can used used, but there is no template, and tables have to
    handled individually.
    """
    def ObtainRowComparisonDataFromCSVFile(pathWork): 
        
        # globals
        #quoted_string_test = re.compile('"[^"]*"')
        quoted_string_test = re.compile("'[^']*'")    #The CSV file needs to use single quotes for strings.
        return_data = []      #The list of dictionaries which are returned, one dictionary per database row.
        row_names = []        #The field name for each row. Obtained from the CSV file.
        
        """
        This nested (two levels deep) function handles a single row of data from the test comparison file.
        It breaks the row down into its separate database columns, creates a dictionary object for the row, and
        then adds that row dictionary onto the list of rows which will be returned to the caller.
        """
        def Handle_RowData(line):
            row_values_list = line.split('\t')
            i = 0
            row_of_comparison_data = {}
            for col in row_names:
                #Column names in the CSV are quoted. The columm names which come in via the sql query
                #will not be quoted. Make them the same.
                col = col[1:-1]
                #Data from text table fields will be quoted in the CSV. Everything read from the CSV
                #file will be a string, so will all be encased in quotes when added into the dictionary.
                #Strip off the CSV quotes from the text fields, to avoid them becoming double quoted.
                # ... So far I have not seen any data of type unicode come in here.
                # ... Any unicode data which comes in from the database is converted to str before the 
                # ... comparison.
                if re.match(quoted_string_test,row_values_list[i]) == None:
                    row_of_comparison_data[col] = str(row_values_list[i])
                else:
                    row_of_comparison_data[col] = str(row_values_list[i][1:-1])
                    
                i += 1
            return_data.append(row_of_comparison_data)
            #---------- end of nested function (inner most level) --- we are still within a nested function --- .            
        
        #Read expected data values from a saved CSV file.
        linework = None
        rows_completed = 0
        rows_read = 0
        full_row = ''
        first_thru = True
        with open(pathWork) as f:
            for line in f:  
                #Things would have been tidier if one CSV row == 1 database row. However multi-entry tags have been implemented
                #with an imbedded newline control character separator. This means that where a database row contains multi-value
                #tags, there will be several CSV lines for the one db record. We need to detect this situation, and join the 
                #parts back into a whole.
                if not first_thru:
                    linework = line.rstrip()                     #strip off newline control character.
                    test_row = linework.split('\t')                                               
                    if len(test_row) >= row_count: 
                        full_row = linework                      # No multi-entry tgas. This single line si the whole db record.
                    else:
                        full_row = full_row + line               # This here is just part of the record, so get more pieces
                        test_row = full_row.split('\t')          # and join them together.
                        if len(test_row) < row_count:
                            continue
                    assert len(test_row) == row_count, 'Test row data has unexpected column count, {0} headings, {1} data rows'.format(row_count, len(full_row))
                    
                #First load field names into list from CSV heading line
                if first_thru:
                    first_thru = False                    
                    linework = line.rstrip()   #strip off newline control character.                    
                    row_names = linework.split('\t')
                    row_count = len(row_names) 
                #Then load field values for requested row(s) into a dictionary by field name.
                else:                    
                    rows_read += 1
                    full_row = full_row.rstrip()   #strip off newline control character.
                    if userDefinedStartPosition:
                        if rows_read < param.whichRowStart: 
                            full_row = ''
                            continue
                    if not startLastRow:
                        Handle_RowData(full_row)
                        rows_completed += 1
                        full_row = ''
                        if not allRows and rows_completed >= param.howManyRows: break
                        
        if full_row == None:
            print 'No test data found in {0} file'.format(pathWork)
            raise AssertionError
        if startLastRow:
            Handle_RowData(full_row)
        
        return return_data
    
    #----------- end of nested functions, back to the outer level of  def perform_and_assert_comparison -------
           
    pathWork = os.path.join(g_test_root_directory_name, param.csvFileName)
    self.assertTrue(os.path.exists(pathWork),'Cannot locate {0} test comparison file '.format(param.csvFileName))    
    
    # evaluate start position request 
    if isinstance(param.whichRowStart,int):
        userDefinedStartPosition = True
        startFirstRow = startLastRow = allRows = False
    else:
        valid_which_rows = ['first','last','all']        
        param.whichRowStart = param.whichRowStart.lower()
        if param.whichRowStart not in valid_which_rows:
            print "which_row_values parameter must be either {0}".format(valid_which_rows)
            raise AssertionError
        startFirstRow = param.whichRowStart == valid_which_rows[0]
        startLastRow = param.whichRowStart == valid_which_rows[1]
        allRows = param.whichRowStart == valid_which_rows[2]
        userDefinedStartPosition = False
        
    if  not (startFirstRow | startLastRow | allRows | userDefinedStartPosition):
        raise RuntimeError(self,"failed belt and braces logic test")
    
    #Obtain comparison data for all tests; a list of dictionaries, one dictionery per row to be tested
    row_test_values = ObtainRowComparisonDataFromCSVFile(pathWork)        
    
    #Obtain data to be tested from the database
    db = sqlite3.connect(g_test_db_name)
    db.row_factory = sqlite3.Row
    db_cursor = db.cursor()
    
    db_cursor.execute(param.queryString)
    
    #Process data obtained from the database. Loop through, processing records were were asked to process.
    number_of_rows_compared = 0
    number_of_rows_read = 0
    while True:
        if startLastRow:
            list_of_rows = db_cursor.fetchall()
            if list_of_rows == []:
                print "No data obtained for comparion?"
                raise AssertionError
            row = list_of_rows[len(list_of_rows)-1]
            list_of_rows = []  #release memory
        
        else:
            row = db_cursor.fetchone()
            if row == None:
                if number_of_rows_compared == 0:
                    print "No data obtained for comparion?"
                    raise AssertionError                    
                break
            number_of_rows_read += 1
            if userDefinedStartPosition:
                if number_of_rows_read < param.whichRowStart:
                    continue
            
            if not allRows and number_of_rows_compared >= param.howManyRows: break
            
        ##TODO: count rows in csv file, and make sure that this equals rows in the db    
        #self.assertEqual(len(row), param.expectedRowCount, '{0} table contains unexpected row count during row comparison; {1} expected, but found {2}'.format(param.tableName, param.expectedRowCount, len(row)))
                         
        row_file_values = {}        
        for key in row.keys():
            #All of the comparison values come in from the CSV file as strings, so is best that we
            #convert to strings also, to avoid any false mismatches. Numeric fields will be 
            #reconverted to numeric in unision with the test compasision data.
            # ... sqllite returns datatype of unicode for non-ascii data (not UTF8-encoded data?) 
            # ... otherwise TEXT. Not sure why. Manual reads as if unicode is default for a TEXT data. 
            try:
                row_file_values[key] = str(row[key])
            except UnicodeEncodeError:
                if type(row[key]) == unicode:
                    #TODO: a stab in the dark here, this seems to work. Don't know it it covers all cases.
                    try:
                        row_file_values[key] = row[key].encode('latin-1')
                    except:
                        row_file_values[key] = row[key].encode('utf-8')                            
                else:
                    raise
                
        
        #Remove columns which shouldn't be compared, and also convert any numeric fields to the appropriate
        #format to avoid false mismatches such as 10 != 10.0
        param.dbRow = True
        PrepareForComparison(row_file_values, param)
        param.dbRow = False
        PrepareForComparison(row_test_values[number_of_rows_compared], param)
        
        self.maxDiff = None
        self.longMessage = True     #required python v2.7.2, but not backport of unittest2 into python v2.6
        self.assertEqual(row_file_values, row_test_values[number_of_rows_compared], 'Unexpected value in {0} table'.format(param.tableName)) 
        #self.assertDictEqual(row_file_values, row_test_values[number_of_rows_compared], 'Unexpected value in {0} table'.format(param.tableName))  
        
        number_of_rows_compared += 1
        
        if startLastRow: break
        
    print '{0} row(s) processed'.format(number_of_rows_compared)
                         

"""
Database row values are checked against expected values, which are obtained from a CSV file.
The comparison is made by comparing a dictionary of file values against a dictionary loaded from the 
CSV file data. 
This function prepares each of the dictionaries for comparison.
Not all columns should be compared, eg. lastmodified in the new record will differ from the value
obtained from the CSV file. ... These columns are removed from the dictionaries prior to comparison.
Also all values coming in from the CSV files are in string format. Numeric data obtained from the new 
database have also been converted to strings. ... This function converts numeric fields to their correct 
format prior to comparison.
The function corrects any database field containing a null in a numeric field. The CSV file will pass
these to us as '0'. We set the numeric nulls to '0' before comparison.
The function also prepares any field which contain a data path for compariosn. The CSV compararison data
may have been built upon a PC with a different file location than the PC running the unit test. The path
data is made relative to the test file directory, ignoring the different in locatiosn for that directory.
"""
def PrepareForComparison (data_to_be_compared, param):
    isinstance(param, prepare_row_comparison_parms)   #provide assistnace to Wing IDE code completion
    
    for col in param.integerRows:
        #try:
        if data_to_be_compared[col]:
            data_to_be_compared[col] = int(data_to_be_compared[col])
        #except KeyError:
            #print 'KeyError for {0} having expected integer value'.format(col)
        #except ValueError:
            #print 'ValueError for {0} with integer value of {1}'.format(col, data_to_be_compared[col])
            
    for col in param.realRows:
        #try:
        if data_to_be_compared[col]:
            data_to_be_compared[col] = float(data_to_be_compared[col])
        #except KeyError:
            #print 'KeyError for {0} having expected "real" value'.format(col)
        #except ValueError:
            #print 'ValueError for {0} with "real" value of {1}'.format(col, data_to_be_compared[col])
        if data_to_be_compared[col] == 0:
            data_to_be_compared[col] = '' 
            

    for col in param.ignoredRows:
        #try:
        data_to_be_compared.pop(col)
        #except KeyError:
            #print 'KeyError for {0} when trying to ignore column'.format(col)
      
    '''
    Paths may give a false alert if the testing machine has a different file structure to the machine
    which setup the comparison data. Cause the comparison to only look at path data relative to the 
    folder containing the test data.
    Further compicated since in the case of the "trackart" field the path can be embedded with the field.   
    ie.  EMBEDDED_423,16807_c:\ etc
    '''
    if param.fieldsContainingPaths:
        for col in param.fieldsContainingPaths:
            try:        
                if data_to_be_compared[col] != '':
                    path_work = data_to_be_compared[col]
                    embedded_field = path_work.startswith('EMBEDDED_')
                    if embedded_field:
                        coverparts = path_work.split('_')
                        coveroffsets = coverparts[1]
                        # path may contain '_'
                        specstart = len('EMBEDDED_') + len(coveroffsets) + 1
                        save_prefix = path_work[:specstart]
                        path_work = path_work[specstart:]
                    try:
                        # CSV files prepared on a Windows machine. If tests being run under linux, any path data 
                        # stored in the CSV file needs to be translated across to Linux.
                        s=""
                        if param.dbRow and sys.platform.startswith("linux"):
                            s = s.replace('\\','/')
                            
                        s = os.path.split(os.path.normpath(path_work))[1]
                        if embedded_field:
                            data_to_be_compared[col] = '{0}{1}'.format(save_prefix,s)
                        else:
                            data_to_be_compared[col] = s
                    except:
                        raise
            except KeyError:
                print 'KeyError for {0} when trying to fix fields with paths'.format(col)
                
                #string.replace(str, old, new[, maxreplace]) 

            
    '''
    Currently the db has numeric fields which can contain nulls. Hopefully this situation will go away.
    It is an issue becuase the CSV file gets 0, and the db returns ''.
    As a workaround we force any '' to 0 for fields at risk.
    '''
    if param.fixNumericNulls:
        for col in param.fixNumericNulls:
            try:        
                if data_to_be_compared[col] == '': data_to_be_compared[col] = 0
            except KeyError:
                print 'KeyError for {0} when trying to fix numeric nulls'.format(col)
            
"""
 This class contains tests which examine the Scan process as a black box, and verify that it runs
 without error, and that it produces a database which contains at least some data.
 Each test within this class needs to build its own database, as the Setup method clears the slate.
"""
class TestInitalScanCompletesOK(unittest.TestCase):

    def setUp(self):        
        if os.path.isfile(g_test_db_name):
            os.remove(g_test_db_name)
        if os.path.isfile(g_test_db_name):
            raise RuntimeError,'failed to delete testbase({0}) during unit test set up.'.format(g_test_db_name)  
        
    #def tearDown(self):
        #if os.path.isfile('unitTest.db'):
            #os.remove('unitTest.db')
    

    def test_whole_scan(self):
        """ Test complete Scan against a known test database
        
        1) Test Scan completed with expected return code
        2) Verify that a database was created successfully
        3) Verify that the record count in various tables is as expected.
        4) Delete some tracks from various tables, verify record counts confirm deletion
        5) Run a scan repair (-r), verify expected return code
        6) Verify that the record count of various tables is as expected after repair.
        
        """
        expected_tags_record_count = 18
        expected_albums_record_count = 14
        expected_tracks_record_count = 18
        
        args = shlex.split(g_command_line_scan)
        i = scan.main(args)
        self.assertEqual(i,0,'Simple call to Scan failed: return code = ' + str(i))
        
        self.assertTrue(os.path.isfile(g_test_db_name), 'Scan failed to create database')
        
        db = sqlite3.connect(g_test_db_name)
        db_cursor = db.cursor()
        db_cursor.execute('SELECT count(id) FROM tags')
        i = db_cursor.fetchone()[0]
        self.assertEqual(i,expected_tags_record_count, 'Unexpected record count in Tags table, found {0}, expected {1}'.format(i,expected_tags_record_count))
        db_cursor.execute('SELECT count(id) FROM albums')
        i = db_cursor.fetchone()[0]
        self.assertEqual(i,expected_albums_record_count, 'Unexpected record count in Albums table; found {0}, found {1}'.format(i,expected_albums_record_count))
        db_cursor.execute('SELECT count(id) FROM tracks')
        i = db_cursor.fetchone()[0]
        self.assertEqual(i,expected_tracks_record_count, 'Unexpected record count in Tracks table; found {0}, expected {1}'.format(i,expected_tracks_record_count))
        
        
        db_cursor.execute('drop table albums')
        db.commit()
        with self.assertRaises(sqlite3.OperationalError):
            db_cursor.execute('SELECT * FROM albums')
        #self.assertRaises(sqlite3.OperationalError,db_cursor.execute('SELECT * FROM albums'))
        db_cursor.execute('drop table tracks')
        db.commit()
        with self.assertRaises(sqlite3.OperationalError):
            db_cursor.execute('SELECT * FROM tracks')
        
        args = shlex.split(g_command_line_repair)
        i = scan.main(args)
        self.assertEqual(i,0,'Simple call to Scan repair failed: return code = ' + str(i))
        
        db_cursor.execute('SELECT count(id) FROM albums')
        i = db_cursor.fetchone()[0]
        self.assertEqual(i, expected_albums_record_count,'Unexpected record count in Albums table after repair; expected {0}, found {1}'.format(i,expected_albums_record_count))
        db_cursor.execute('SELECT count(id) FROM tracks')
        i = db_cursor.fetchone()[0]
        self.assertEqual(i,expected_tracks_record_count, 'Unexpected record count in Tracks table after repair; expected {0}, found {1}'.format(i, expected_tracks_record_count))
        
"""
This class contains tests which examine the data produced by an initial scan, and compare that data against expected values.
The database is created by the class' setup method, and none of the tests within this class should alter that database.

Warning: If you are using the param.whichRowStart = 'all' option, please be aware that the whole result set for you query
will be loaded into memory, so be sure only to use this option with appropriately sized result sets.
"""                
class TestRowContentsFromInitialScan(unittest.TestCase):    
        
    @classmethod
    def setUpClass(cls): 
        cls.Error = None
        
        if os.path.isfile(g_test_db_name):
            os.remove(g_test_db_name)
            if os.path.isfile(g_test_db_name):
                cls.Error = 'failed to delete testbase({0}) during unit test set up.'.format(g_test_db_name) 
                return
        
        args = shlex.split(g_command_line_scan)
        i = scan.main(args)
        if i != 0:
            cls.Error = 'Simple call to Scan failed: return code = ' + str(i)
            return
        
        if not os.path.isfile(g_test_db_name):
            cls.Error = 'Scan failed to create database'
            return
    
    def setUp(self):        
        # Don't allow the test suite to start of there was a set up problem.
        self.assertIsNone(TestRowContentsFromInitialScan.Error, 'Test set up error: {0}'.format(TestRowContentsFromInitialScan.Error))
               
    """
    These tests compare database values to expected values. Assertion exceptions are raised if the data comparison fails.
    """
    def test_album_row_contents(self):        
               
        param = prepare_row_comparison_parms('Albums')
        param.csvFileName = 'albums.csv'
        param.queryString = 'select * from albums'
        param.setDefault('albums')
        param.whichRowStart = 'all' # valid options are 'first', 'last' or 'all, or an integer causing start at row n (relative to 1)'
                                                   # NB. that final option expects an integer, not a string containing an integer       
        param.howManyRows = 2       # defaults to 1, ignored for whichRowStart = 'all'            
        perform_and_assert_comparison(self,param)  
        
    def test_track_row_contents(self):        
               
        param = prepare_row_comparison_parms('Tracks')
        param.csvFileName = 'tracks.csv'
        param.queryString = 'select * from tracks'        
        param.setDefault('tracks')
        param.whichRowStart = 'all' # valid options are 'first', 'last' or 'all, or an integer causing start at row n (relative to 1)'
                                                   # NB. that final option expects an integer, not a string containing an integer       
        #param.howManyRows = 1       # defaults to 1, ignored for whichRowStart = 'all'        
        perform_and_assert_comparison(self,param) 
       
"""
This class contains tests which examine the data produced by an update scan, ie. a subsequent scan which finds updates 
for an already existing database. It compares updated data to expected values.

The database is created by the setup class method, and none of the tests within this class should alter that database.

Warning: If you are using the param.whichRowStart = 'all' option, please be aware that the whole result set for you query
will be loaded into memory, so be sure only to use this option with appropriately sized result sets.
"""                  
class TestUpdateScans(unittest.TestCase):
    
    '''
    This methods runs once for the whole test suite.
    It uses Scan to create a database using a set of music tracks. It then provides updated values of some of the tracks.
    It then runs scan to update the database. The tests within this class verify that the database is as it should be.
    '''
    @classmethod
    def setUpClass(cls):        
        expected_tags_record_count = 6
        expected_tags_record_count_after_update = 7
        
        cls.Error = None
                 
        copy_source_before = g_update_scan_copy_source_BEFORE_path
        if not os.path.isdir(copy_source_before):
            cls.Error = 'Cannot find Copy From path: {0}'.format(copy_source_before)
            return
        
        copy_source_after = g_update_scan_copy_source_AFTER_path
        if not os.path.isdir(copy_source_after):
            cls.Error = 'Cannot find Copy From path: {0}'.format(copy_source_after)
            return
        copy_target_root = g_update_scan_copy_target_path
        
        if os.path.isdir(copy_target_root):
            shutil.rmtree(copy_target_root)
            if os.path.isdir(copy_target_root):
                cls.Error = 'failed to delete directory BEFORE test'
                return
            
        art_file_source = os.path.join(g_test_root_directory_path, g_update_scan_art_file_name)
        if not os.path.isfile(art_file_source):
            cls.Error = 'Cannot find test file; {0}'.format(art_file_source)
            return
        
        art_file_target = os.path.join(g_update_scan_art_test_path,g_update_scan_art_file_name)
        if os.path.isfile(art_file_target):
            try:
                os.remove(art_file_target)
                if os.path.isfile(art_file_target):
                    cls.Error = 'Unable to delete file before running test: {0}'.format(art_file_target)
                    return                    
            except WindowsError as x:     #don't know what error would be raised in linux.
                cls.Error = 'Error clearing slate for a new test.\n{0}: {1}'.format(x.args, x.filename)
                return
            
        def _logpath(path, names):
            print 'Cloning {0}: {1}'.format(path, names)   # only shows in debug mode
            return []
            
        print 'Cloning BEFORE data to: {0}'.format(copy_target_root)
        shutil.copytree(copy_source_before, copy_target_root, ignore=_logpath)
               
        if os.path.isfile(g_test_db_name):
            os.remove(g_test_db_name)
            if os.path.isfile(g_test_db_name):
                cls.Error = 'failed to delete testbase({0}) during unit test set up.'.format(g_test_db_name)
                return
        
        args = shlex.split(g_command_line_update_scan)

        if scan.main(args) !=0:
            cls.Error = 'Simple call to Scan failed (1): return code = ' + str(i)
            return
        
        if not os.path.isfile(g_test_db_name):
            cls.Error = 'Scan failed to create database'
            return
        
        cls.db = sqlite3.connect(g_test_db_name)
        cls.db_cursor = cls.db.cursor()
        cls.db_cursor.execute('SELECT count(id) FROM tags')
        i = cls.db_cursor.fetchone()[0]
        if i != expected_tags_record_count:
            cls.Error = 'Unexpected record count in Tags table before update, found {0}, expected {1}'.format(i,expected_tags_record_count)
            return    
        
        #clear slate before starting tests
        shutil.rmtree(copy_target_root)
        if os.path.isdir(copy_target_root):
            cls.Error = 'failed to delete directory DURING test'
            return
            
        print 'Cloning AFTER data to: {0}'.format(copy_target_root)
        shutil.copytree(copy_source_after, copy_target_root, ignore=_logpath) 
        
        '''
        One of the tests is to ensure that the track without art is updated if it's folder is updated to have cover art.
        We need to save a snapshot of the database situation before the introduction of the folder cover art.
        We also do a few pre-edits, but pass nay failures to the test method, so not to affect any non-realted tests.
        '''
        cls.art_track = "'Has_no_art_of_its_own.flac'"
        cls.art_query_string = "SELECT tags.folderartid, tags.trackartid FROM tags WHERE tags.filename = {0} AND tags.title = 'Has no art of its own'".format(cls.art_track)
        cls.art_setup_error = None  
        try:
            cls.db_cursor.execute(cls.art_query_string)
            list_rows = cls.db_cursor.fetchall()
            if len(list_rows) != 1:
                cls.art_setup_error = 'Setup error for art test: Expected 1 copy of file, but found {0}: {1}'.format(len(list_rows),cls.art_track)
            cls.art_track_before_update = list_rows[0]
            shutil.copyfile(art_file_source, art_file_target)
            if not os.path.isfile(art_file_target):
                cls.art_setup_error = 'Cannot copy art file during test set up; {0}'.format(art_file_target)
        except Exception as X:
            cls.art_setup_error = 'Error setting up for art file test (#1). Exception received in @classmethod: {0}'.format(X.args)  
            
        args = shlex.split(g_command_line_update_scan)
        i = scan.main(args)
        if i != 0:
            cls.Error = 'Simple call to Scan failed (2): return code = ' + str(i)
            return
        
        
    @classmethod
    def tearDownClass (cls):
        try:
            cls.db.close()
        except:
            return
    
    def setUp(self):
        # Don't allow the test suite to start of there was a set up problem.
        self.assertIsNone(self.Error, 'Test set up error: {0}'.format(self.Error))
           
    def test_table_record_counts(self): 
        expected_tags_record_count_after_update = 7
        expected_albums_record_count_after_update = 2
        expected_art_record_count_after_update = 3
        expected_artists_record_count_after_update = 2
        expected_tracks_record_count_after_update = 7
        
        self.db_cursor.execute('SELECT count(id) FROM tags')
        i = self.db_cursor.fetchone()[0]
        self.assertEqual(i,expected_tags_record_count_after_update, 'Unexpected record count in Tags table after update, found {0}, expected {1}'.format(i,expected_tags_record_count_after_update))
        
        self.db_cursor.execute('SELECT count(id) FROM albums')
        i = self.db_cursor.fetchone()[0]
        self.assertEqual(i,expected_albums_record_count_after_update, 'Unexpected record count in Albums table after update, found {0}, expected {1}'.format(i,expected_albums_record_count_after_update))
        
        self.db_cursor.execute('SELECT count(id) FROM art')
        i = self.db_cursor.fetchone()[0]
        self.assertEqual(i,expected_art_record_count_after_update, 'Unexpected record count in Art table after update, found {0}, expected {1}'.format(i,expected_art_record_count_after_update))
        
        self.db_cursor.execute('SELECT count(id) FROM artists')
        i = self.db_cursor.fetchone()[0]
        self.assertEqual(i,expected_artists_record_count_after_update, 'Unexpected record count in Artists table after update, found {0}, expected {1}'.format(i,expected_artists_record_count_after_update))
                 
        self.db_cursor.execute('SELECT count(id) FROM tracks')
        i = self.db_cursor.fetchone()[0]
        self.assertEqual(i,expected_tracks_record_count_after_update, 'Unexpected record count in Tracks table after update, found {0}, expected {1}'.format(i,expected_tracks_record_count_after_update))
        
    def test_table__album_contents(self):
        param = prepare_row_comparison_parms('Albums')
        param.csvFileName = 'albumsUpdated.csv'
        param.queryString = 'select * from albums'
        param.setDefault('albums')
        #param.ignoredRows = param.ignoredRows + ('created',)    # why created mismatch here ?
        param.whichRowStart = 'all'         
        perform_and_assert_comparison(self,param)  
        
    def test_table__track_contents(self):
        param = prepare_row_comparison_parms('Tracks')
        param.csvFileName = 'tracksUpdated.csv'
        param.queryString = 'select * from tracks'
        param.setDefault('tracks')
        param.whichRowStart = 'all'         
        perform_and_assert_comparison(self,param)  
        
        #Ensure that a track which has no imbedded art is updated if it's folder acquires art.
    def test_unmodified_folder_art(self):
        
        self.assertIsNone(self.art_setup_error, self.art_setup_error)
        self.assertIsNone(self.art_track_before_update[0], 'Art test setup error: these should have been no folder art for {0}'.format(self.art_track))
        self.assertIsNone(self.art_track_before_update[1], 'Art test setup error: these should have been no track art for {0}'.format(self.art_track))
        self.db_cursor.execute(self.art_query_string)
        list_rows = self.db_cursor.fetchall()
        self.assertEquals(len(list_rows), 1,'Error after update during art test: Expected 1 copy of file, but found {0}: {1}'.format(len(list_rows), self.art_track))
        self.assertIsNotNone(list_rows[0][0], 'Track should have gained folder art. {0}'.format(self.art_track))
        self.assertIsNone(list_rows[0][1],'This track should not have track art. {0}'.format(self.art_track))
          
if __name__ == '__main__':   
    unittest.main()

