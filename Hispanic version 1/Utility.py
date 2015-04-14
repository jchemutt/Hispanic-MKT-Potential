#-------------------------------------------------------------------------------
# Name:        Utility
# Purpose:
#
# Author:      Chemutt
#
# Created:     07/094/20144
# Copyright:   (c) Chemutt 2015
# Licence:
#-------------------------------------------------------------------------------
import os, sys
import arcpy
import traceback
from arcpy import env

import logging

##------------------Beginning of Functions--------------------------------------------

def exportToTextfile(_log, workspace,input_features, fields, exportFieldsAlias,textfile):
    try:
		##Set the overwriteOutput environment setting to True
		env.overwriteOutput = True





		# Set the current workspace (to avoid having to specify the full path to the feature classes each time)
		arcpy.env.workspace = workspace


		#Open the report text file in write mode
		file = open (textfile, "w")



		# Create cursor to search gas mains by material
		with arcpy.da.SearchCursor(input_features, fields) as cursor:
			for row in cursor:
				#Get field values
				OBJECTID = str(row[0])
				store_id = str(row[1])





				#Write to file as below
				# Store_is "Update type" "Flag Name" "Value"
				file.write(store_id + "\t" + "U" + "\t" + "YUS_FLG_ETHNICITY" + "\t" + " 01" + "\n")

		#Close file to release handle
		file.close()

    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n Utility Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                    "Line {0}".format(tb.tb_lineno)
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows
            print pymsg
            print "\n" +msgs
            _log.info("exportToTextfile in Utility "+pymsg)
            _log.info("exportToTextfile in Utility "+msgs)


    #Return Nothing
    return ""

def main():
    pass

if __name__ == '__main__':

    main()



    #Exports to file but using search cursor
    exportToTextfile(_log, workspace,input_features, fields, exportFieldsAlias, textfile)

