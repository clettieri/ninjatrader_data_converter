# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 12:51:32 2016

@author: chris

This script will take a csv file in Sprywarw's tick data format and
convert that into a new csv file for use in NinjaTrader 8.

This script assumes SPRY columns of ["Date", "Time", "Symbol", "TransType", "ItemType", 
"Condition", "Scale", "Sequence", "Exchange", "Price", "Size"],
and that you want NinjaTrader format of yyyyMMdd HHmmss;price;volume.

This script assumes the csv file you wish to convert is in the same
directory as the script.

To use this data in NinjaTrader 8:
    Tools -> Import Data -> Tick data, time zone GMT -5
    Either Connection -> Playback -> Open Chart of symbol -> Press Play
    Or No Connection -> Open Chart -> Manual Bar by Bar Play Back
"""

import pandas as pd
import sys

'''### Global Variables ### '''
DF = None #original csv will read into this pandas dataframe
SPRY_COLUMNS = ["Date", "Time", "Symbol", "TransType", "ItemType", "Condition", "Scale", "Sequence", "Exchange", "Price", "Size"] #assumed format of original data
CONDITION_EXCLUDE_LIST = [2, 3, 4, 5, 13, 14, 16, 18, 30, 32, 34, 57, 58, 59, 63, 71, 72, 102, 105, 145]
NT_DF = None #will contain the converted dataframe

'''### Helper Functions ###'''
def convert_time(t):
    '''(string) -> string
    
    Will take a string of time in format from Spryware as
    HH:MM:SS.SSS and convert it to NinjaTrader desired
    time format.  Returns the NinjaTrader format string.
    
    This function designed to be applied to each row in the
    dataframe.
    '''
    t = t.split(".") #throw away the fractions of a second, don't need it
    t = t[0].split(":")
    t = "".join(t) #create new string with no punctuation
    return t


'''### MAIN - START OF SCRIPT ### '''
while True:
    '''### Open the File ###'''
    able_to_open_file = False
    
    while not able_to_open_file:
        print "Enter name of file to convert: "
        file_name = raw_input(">")
        try:
            DF = pd.read_csv(file_name)
            able_to_open_file = True
        except:
            try:
                DF = pd.read_csv(file_name + ".csv")
                able_to_open_file = True
            except:
                print "Error opening file.. try different file name."
                print ""
    
    '''### Convert to NinjaTrader Format ###'''
    DF.columns = SPRY_COLUMNS #data not expected to have column headers
    NT_DF = DF.copy()
    
    #Exclude rows (trades/ prints/ ticks) that have an exclude condition
    NT_DF = NT_DF.query('Condition not in @CONDITION_EXCLUDE_LIST')
    #Convert the time
    NT_DF['NTTime'] = NT_DF['Time'].apply(convert_time) #Apply helper function
    NT_DF['DT'] = NT_DF['Date'].astype(str) + " " + NT_DF['NTTime'] #Merge Date with Time strings
    #Convert the price
    NT_DF['P'] = NT_DF['Price'] / (10 ** NT_DF['Scale'])
    #Clean Up and Re-order the DataFrame
    CONVERTED_DF = pd.concat([NT_DF['DT'], NT_DF['P'], NT_DF['Size']], axis=1, keys=['DT', 'P', 'Size'])
    
    '''### Output the Converted Data ###'''
    print "Enter name for converted csv file of " + file_name + ":"
    output_name = raw_input(">")
    if output_name.endswith(".csv"):
        output_name = output_name[:-4]
    #Write the new csv
    CONVERTED_DF.to_csv(output_name+".csv", sep=";", header=False, index=False)
    print "Conversion Complete!"
    print ""
    
    '''### Convert Another File or Quit ###'''
    print "Convert another file (Y/N)? - N will quit."
    user_input = raw_input(">")
    if user_input == 'N' or user_input == 'n':
        sys.exit()



