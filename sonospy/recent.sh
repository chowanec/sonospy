#!/bin/bash
########################################################################################################################################
# TO DO
########################################################################################################################################
# OTHER FIELDS TO EXTRACT:
#
# year		-	all albums of a particular year
# genre		-	all albums of a particular genre
# artist	-	all albums of a particular artist
# composer	-	all albums of a particular composer
# bitrate	-	all songs of a bit range (=,<,<=,>,>=)
########################################################################################################################################

# CHECK FOR ARGUMENTS (NEEDS 4)
if [ $# -ne 4 ]
	then
		echo ""
		echo "A simple shell script that will extract a subset of your Sonos database"
		echo "to create a secondary database that meets a specific time criteria..."
		echo "You can, for example, scan your database for all music inserted into your"
		echo "master database within the last three months (90 days)."
		echo ""
		echo "Please provide arguments to the script:"
		echo "arg1 = Database to extract from"
		echo "arg2 = Database to extract to"
		echo "arg3 = date field to extract from: inserted, created, lastmodified or"
		echo "       lastscanned."
		echo "arg4 = # of days to scan for"
		echo ""
		echo "example:"
		echo ""
		echo "sh recent.sh sonos.sqlite last90days.db inserted 90"
		echo ""
		echo "This would scan a source database of sonos.sqlite, create a subset of that"
		echo "database called last90days.db for files added to sonos.sqlite in the last"
		ecjp "90 days."
		echo ""		
		exit 1
fi

# CHECK MY DATE ARGUMENT
if [ $3 != "inserted" ] && [ $3 != "lastmodified" ] && [ $3 != "created" ] && [ $3 != "lastscanned" ]
	then
	echo "Please provide an argument for the date field: inserted, lastmodified, created or lastscanned."
	exit 0
fi

# REMOVE THE OLD DATABASES - SO WE CAN REPLACE THEM
if [ -f $1.backup ]
	then
		rm -I $1.backup
fi

if [ -f $2 ]
	then
		rm -I $2
fi


# CREATE A BACKUP OF OUR ARG1 INPUT DATABASE
cp $1 $1.backup

# RUN OUR SCAN
./scan -d $1 -x $2 -w "where (julianday(datetime('now')) - julianday(datetime($3, 'unixepoch'))) <= $4"
