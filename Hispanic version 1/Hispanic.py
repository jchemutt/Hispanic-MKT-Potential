#------------------------------------------------------------------------------
# Name:        ULIMS Perfomance Management
# Purpose:     Script scheduled in windows scheduler used to perform enteprise geodatabase perfoamnce tuning
#
# Author:      dmuthami
# Email :      waruid@gmail.com
#
# Created:     17/03/2015
# Copyright:   (c) dmuthami 2015
# Licence:     Absolutely Free for use and distribution
#-------------------------------------------------------------------------------
import os, sys
import logging
import arcpy
import traceback
from arcpy import env
from datetime import datetime

import Utility
import mail


#Set-up logging
logger = logging.getLogger('hispanic')

def makeSelection(workspace, blockGroup):

    #Apply field delimeters for the Query supplied
    HSP_PercFieldDelimeter = arcpy.AddFieldDelimiters(env.workspace , "HSP_Perc")
    NHSPBLK_PFieldDelimeter = arcpy.AddFieldDelimiters(env.workspace , "NHSPBLK_P")
    NHSPAI_PFieldDelimeter = arcpy.AddFieldDelimiters(env.workspace , "NHSPAI_P")
    NHSPASN_PFieldDelimeter = arcpy.AddFieldDelimiters(env.workspace , "NHSPASN_P")
    NHSPPI_PFieldDelimeter = arcpy.AddFieldDelimiters(env.workspace , "NHSPPI_P")
    NHSPWHT_PFieldDelimeter = arcpy.AddFieldDelimiters(env.workspace , "NHSPWHT_P")
    NHSPOTH_PFieldDelimeter = arcpy.AddFieldDelimiters(env.workspace , "NHSPOTH_P")
    NHSPMLT_PFieldDelimeter = arcpy.AddFieldDelimiters(env.workspace , "NHSPMLT_P")

    #Selection required
    #HSP_Perc >= 40 OR (HSP_Perc > NHSPWHT_P AND
    #HSP_Perc > NHSPBLK_P AND HSP_Perc > NHSPAI_P AND
    #HSP_Perc > NHSPASN_P AND HSP_Perc > NHSPPI_P AND
    #HSP_Perc > NHSPOTH_P AND HSP_Perc > NHSPMLT_P)

    # Build the query expression
    SQLExp =  HSP_PercFieldDelimeter + " >= " + "40" + " or ("
    SQLExp +=  HSP_PercFieldDelimeter + " > " + NHSPWHT_PFieldDelimeter + " and "
    SQLExp +=  HSP_PercFieldDelimeter + " > " + NHSPBLK_PFieldDelimeter + " and "
    SQLExp +=  HSP_PercFieldDelimeter + " > " + NHSPAI_PFieldDelimeter + "  and "
    SQLExp +=  HSP_PercFieldDelimeter + " > " + NHSPASN_PFieldDelimeter + " and "
    SQLExp +=  HSP_PercFieldDelimeter + " > " + NHSPPI_PFieldDelimeter + "  and "
    SQLExp +=  HSP_PercFieldDelimeter + " > " + NHSPOTH_PFieldDelimeter + " and "
    SQLExp +=  HSP_PercFieldDelimeter + " > " + NHSPMLT_PFieldDelimeter + " )"

    try:
        # Make a layer from blockgroups feature class
        blockGroupFeatureLayer = blockGroup + '_lyr'

        #delete the in memory feature layer
        # something terrible must have happened since we run the tool and now we have to destroy the
        # the memory imprint of the feature layer
        arcpy.Delete_management(blockGroupFeatureLayer)

    except:
        try:

            #variable pointer to the in-memory feature layer
            blockGroupFeatureLayer = blockGroup + '_lyr'

        except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows _log
            ##print pymsg
            ##print "\n" +msgs
            logger.info("Forcefully deletes the in memory stores feature layer "+pymsg)
            logger.info("Forcefully deletes the in memory stores feature layer "+msgs)

    #Make feature layer
    arcpy.MakeFeatureLayer_management(blockGroup, blockGroupFeatureLayer)

    #make a fresh selection here
    arcpy.SelectLayerByAttribute_management(blockGroupFeatureLayer, "NEW_SELECTION", SQLExp)


    #Deafult 28748 out of 217486 features from Block groups layer for hispanic as check
    featCount = arcpy.GetCount_management(blockGroupFeatureLayer)
    message = "Number of Hispanic blocks: {0} ".format(featCount)

    logger.info(message)
    #print message

    return blockGroupFeatureLayer

##Select hispanic areas based on selection
#def updateHispanicAreas(workspace,blockGroupFeatureLayer,field,updatevalue):
    #try:

        # Start an edit session. Must provide the workspace.
        #edit = arcpy.da.Editor(workspace)

        # Edit session is started without an undo/redo stack for versioned data
        #  (for second argument, use False for unversioned data)
        #Compulsory for above feature class participating in a complex data such as parcel fabric
        #edit.startEditing(False, False)

        # Start an edit operation
        #edit.startOperation()

        #Update cursor goes here
       # with arcpy.da.UpdateCursor(blockGroupFeatureLayer, field) as cursor:
            #for row in cursor:# loops per record in the recordset and returns an array of objects

                #update zone affiliationS
                #row[0] = int(updatevalue)

                # Update the cursor with the updated row object that contains now the new record
                #cursor.updateRow(row)

        # Stop the edit operation.and commit the changes
        #edit.stopOperation()

        # Stop the edit session and save the changes
        #Compulsory for release of locks arising from edit session. NB. Singleton principle is observed here
        #edit.stopEditing(True)

    #except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            #tb = sys.exc_info()[2]
            #tbinfo = traceback.format_tb(tb)[0]
            #pymsg = "PYTHON ERRORS:\n updateIPEDSID() Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                   # str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                   # "Line {0}".format(tb.tb_lineno)
           # msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            #arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            #arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows _log
            ##print pymsg
            ##print "\n" +msgs
            #logger.info( pymsg)
            #logger.info(msgs)

   # return ""

##Calculate race percentage
def calculateRacePercentage(workspace,blockGroupFeatureLayer,fieldsPer,fieldsPop):
    try:

        ## Below code
        ## Make (Non Collegiate) IPEDS null
        ##

        # Start an edit session. Must provide the workspace.
        edit = arcpy.da.Editor(workspace)

        # Edit session is started without an undo/redo stack for versioned data
        #  (for second argument, use False for unversioned data)
        #Compulsory for above feature class participating in a complex data such as parcel fabric
        edit.startEditing(False, False)

        # Start an edit operation
        edit.startOperation()

        #merge the list of the fields
        mergedFieldList =fieldsPer + fieldsPop

        #Update cursor goes here
        with arcpy.da.UpdateCursor(blockGroupFeatureLayer, mergedFieldList) as cursor:
            for row in cursor:# loops per record in the recordset and returns an array of objects

                #fieldsPer = ["HSP_Perc","NHSPWHT_P","NHSPBLK_P","NHSPAI_P","NHSPASN_P","NHSPPI_P","NHSPOTH_P","NHSPMLT_P"]
                #fieldsPop = ["HISPPOP_CY","NHSPWHT_CY","NHSPBLK_CY","NHSPAI_CY","NHSPASN_CY","NHSPPI_CY","NHSPOTH_CY","NHSPMLT_CY","TOTPOP_CY"]
                #Compute percentage for each group

                totalPopulation = row[mergedFieldList.index("TOTPOP_CY")]
                row[mergedFieldList.index("HSP_Perc")] = round(((float(row[mergedFieldList.index("HISPPOP_CY")])*100.0)/float(totalPopulation)),1)
                row[mergedFieldList.index("NHSPWHT_P")] = round(((float(row[mergedFieldList.index("NHSPWHT_CY")])*100.0)/float(totalPopulation)),1)
                row[mergedFieldList.index("NHSPBLK_P")] = round(((float(row[mergedFieldList.index("NHSPBLK_CY")])*100.0)/float(totalPopulation)),1)
                row[mergedFieldList.index("NHSPAI_P")] = round(((float(row[mergedFieldList.index("NHSPAI_CY")])*100.0)/float(totalPopulation)),1)
                row[mergedFieldList.index("NHSPASN_P")] = round(((float(row[mergedFieldList.index("NHSPASN_CY")])*100.0)/float(totalPopulation)),1)
                row[mergedFieldList.index("NHSPPI_P")] = round(((float(row[mergedFieldList.index("NHSPPI_CY")])*100.0)/float(totalPopulation)),1)
                row[mergedFieldList.index("NHSPOTH_P")] = round(((float(row[mergedFieldList.index("NHSPOTH_CY")])*100.0)/float(totalPopulation)),1)
                row[mergedFieldList.index("NHSPMLT_P")] = round(((float(row[mergedFieldList.index("NHSPMLT_CY")])*100.0)/float(totalPopulation)),1)

                # Update the cursor with the updated row object that contains now the new record
                cursor.updateRow(row)

        # Stop the edit operation.and commit the changes
        edit.stopOperation()

        # Stop the edit session and save the changes
        #Compulsory for release of locks arising from edit session. NB. Singleton principle is observed here
        edit.stopEditing(True)

        #delete the in memory feature layer just in case we need to recreate
        # feature layer or maybe run script an additional time
        arcpy.Delete_management(blockGroupFeatureLayer)

    except:
            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\n updateIPEDSID() Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                    "Line {0}".format(tb.tb_lineno)
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows _log
            ##print pymsg
            ##print "\n" +msgs
            logger.info( pymsg)
            logger.info(msgs)

    return ""

#main function
def ulimsPerfomanceManagement():
    try:
        #Export to text file#
        currentDate = datetime.now().strftime("-%y-%m-%d_%H-%M-%S") # Current time

        #Set-up some error logging code.
        os.remove(r"C:\Users\gisetl\Hispanic\Hispanic Model\Log\logfile.txt")
        logfile = r"C:\Users\gisetl\Hispanic\Hispanic Model\Log" + "\\"+ "logfile" + ".txt"

        hdlr = logging.FileHandler(logfile)#file handler
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')# formatter object
        hdlr.setFormatter(formatter)#link handler and formatter object
        logger.addHandler(hdlr)# add handler to the logger object
        logger.setLevel(logging.INFO)#Set the logging level

        #Workspace
        _workspace = r"C:\Users\gisetl\Hispanic\Hispanic Model\Hispanic Modeling.gdb"
        env.workspace = _workspace

        ## Set overwrite in workspace to true
        env.overwriteOutput = True

        blockGroup = "US_Block_Groups"
        stores = "s_gis_store_pnt"

        #Make selection where total population is greater than 0
                    #collegiate definition
        totalPopulationFieldwithDelimeter = arcpy.AddFieldDelimiters(env.workspace , \
            "TOTPOP_CY")

        # Select  Total population greater than 0
        totalPopulationSQLExp =  totalPopulationFieldwithDelimeter + " > " + "0"

        try:
            # Make a layer from blockgroups feature class
            blockGroupFeatureLayer = blockGroup + '_lyr'

            #delete the in memory feature layer
            # something terrible must have happened since we run the tool and now we have to destroy the
            # the memory imprint of the feature layer
            arcpy.Delete_management(blockGroupFeatureLayer)

        except:
            try:

                #variable pointer to the in-memory feature layer
                blockGroupFeatureLayer = blockGroup + '_lyr'

            except:
                ## Return any Python specific errors and any error returned by the geoprocessor
                ##
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                        str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
                msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

                ##Add custom informative message to the Python script tool
                arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
                arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

                ##For debugging purposes only
                ##To be commented on python script scheduling in Windows _log
                ##print pymsg
                ##print "\n" +msgs
                logger.info("Forcefully deletes the in memory stores feature layer "+pymsg)
                logger.info("Forcefully deletes the in memory stores feature layer "+msgs)

        #Make feature layer for block group
        arcpy.MakeFeatureLayer_management(blockGroup, blockGroupFeatureLayer)

        #make a fresh selection here
        arcpy.SelectLayerByAttribute_management(blockGroupFeatureLayer, "NEW_SELECTION", totalPopulationSQLExp)

        #Fields array
        fieldsPer = ["HSP_Perc","NHSPWHT_P","NHSPBLK_P","NHSPAI_P","NHSPASN_P","NHSPPI_P","NHSPOTH_P","NHSPMLT_P"]
        fieldsPop = ["HISPPOP_CY","NHSPWHT_CY","NHSPBLK_CY","NHSPAI_CY","NHSPASN_CY","NHSPPI_CY","NHSPOTH_CY","NHSPMLT_CY","TOTPOP_CY"]

        ##Call function to compute percentages
        calculateRacePercentage(env.workspace,blockGroupFeatureLayer,fieldsPer,fieldsPop)

        #Make selection of hispanic layer and return feature layer
        blockGroupFeatureLayer = makeSelection(env.workspace, blockGroup)

        #field = ["zone_affiliation"]
        #updatevalue = 1
        #For hispanic layer. Persist to value 1
        #updateHispanicAreas(env.workspace,blockGroupFeatureLayer,field,updatevalue)

        #Switch selection to non hispanic
        arcpy.SelectLayerByAttribute_management(blockGroupFeatureLayer, "SWITCH_SELECTION")
        updatevalue = 0 #set update value for non-hispanic layer

        # Default check =217486-28748 non-hispanic blocks from Block groups layer
        featCount = arcpy.GetCount_management(blockGroupFeatureLayer)
        message = "Number of Non-Hispanic blocks: {0} ".format(featCount)

        #For hispanic layer. Persist to value 0
        #updateHispanicAreas(env.workspace,blockGroupFeatureLayer,field,updatevalue)

        #Switch selection to Hispanic
        arcpy.SelectLayerByAttribute_management(blockGroupFeatureLayer, "SWITCH_SELECTION")

        #Make feature layer for stores
        storesFeatureLayer = stores + "_Lyr"

        #Make feature layer for stores feature class
        arcpy.MakeFeatureLayer_management(stores, storesFeatureLayer)

        #Select by location only those stores falling under Hispanic
        arcpy.SelectLayerByLocation_management(storesFeatureLayer, 'intersect', blockGroupFeatureLayer, "","NEW_SELECTION")

        # Persist selected stores features to a new featureclass
        #arcpy.CopyFeatures_management(storesFeatureLayer, "stores_hispanic")

        featCount1 = arcpy.GetCount_management(storesFeatureLayer)
        message = "Number of Stores Within Hispanic blocks: {0} ".format(featCount1)

        logger.info(message)
        print message

        #Export to text file#
        currentDate = datetime.now().strftime("-%y-%m-%d_%H-%M-%S") # Current time
        textFile = r"C:\Users\gisetl\Hispanic\Hispanic Model\Stores" + "\\"+ "hispanicstores" + str(currentDate)+ ".txt"

        #Define text file export fields exportFields
        exportFieldsAlias = ["OBJECTID","store_id","store_name"]

        #Define export field field aliases. This are the column headers on the output text file
        exportFields = ["OBJECTID","store_id","store_name"]

        Utility.exportToTextfile(logger, env.workspace,storesFeatureLayer, exportFields, exportFieldsAlias,textFile)


        #Attempt to delete block group feature layer
        try:
            #delete the in memory feature layer
            # something terrible must have happened since we run the tool and now we have to destroy the
            # the memory imprint of the feature layer
            arcpy.Delete_management(blockGroupFeatureLayer)

        except:

            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows _log
            ##print pymsg
            ##print "\n" +msgs
            logger.info("Forcefully deletes the in memory stores feature layer "+pymsg)

        #Attempt to delete stores feature layer
        try:
            #delete the in memory feature layer
            # something terrible must have happened since we run the tool and now we have to destroy the
            # the memory imprint of the feature layer
            arcpy.Delete_management(storesFeatureLayer)

        except:

            ## Return any Python specific errors and any error returned by the geoprocessor
            ##
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                    str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
            msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

            ##Add custom informative message to the Python script tool
            arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
            arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

            ##For debugging purposes only
            ##To be commented on python script scheduling in Windows _log
            ##print pymsg
            ##print "\n" +msgs
            logger.info("Forcefully deletes the in memory stores feature layer "+pymsg)

        #On success perfomace tuning complete is written to a variable
        msg = "Hispanic Tool Automation Succeeded"
        #Write to console
        #print msg
        #Write to log file
        logger.info(msg)
        emails=["vwahome@northriftsolutions.com","chemuttjose@gmail.com"]
        mail.mail(";".join(emails),"Hello from Hispanic MKT Automation Tool!","See the attached logfile",r"C:\Users\gisetl\Hispanic\Hispanic Model\Log\logfile.txt")
    except:
        ## Return any Python specific errors and any error returned by the geoprocessor
        ##
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\n ulimsPerfomanceManagement() Function : Traceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n" +\
                "Line {0}".format(tb.tb_lineno)
        msgs = "Geoprocessing  Errors :\n" + arcpy.GetMessages(2) + "\n"

        ##Add custom informative message to the Python script tool
        arcpy.AddError(pymsg) #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).
        arcpy.AddError(msgs)  #Add error message to the Python script tool(Progress dialog box, Results windows and Python Window).

        ##For debugging purposes only
        ##To be commented on python script scheduling in Windows _log
        ##print pymsg
        logger.info(pymsg)
        ##print "\n" +msgs
        logger.info(msgs)

def main():
    pass

if __name__ == '__main__':
    main()
    #Run perfomance management module
    ulimsPerfomanceManagement()
