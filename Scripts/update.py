import pandas as pd
import os
from pathlib import Path
import csv
from sec_edgar_downloader import Downloader #https://pypi.org/project/sec-edgar-downloader/

############## define functions ############
def checkCreateFolder(fundName):
    #check if fund folder exists in /Data/, if not create one
    #also check if csv file exists in /Data/[fund_name]/, if not create it
    formattedFundName = fundName.replace(' ', '_')
        #create fund folder if it does not exist
    fundPath = os.path.abspath(os.path.join('..','Data', formattedFundName))
    Path(fundPath).mkdir(parents=True, exist_ok=True)
    #create csv with fund positions if does not exist
    fileName = formattedFundName + '.csv'
    if fileName not in os.listdir(fundPath):
        filePath = os.path.abspath(os.path.join('..','Data', formattedFundName, fileName))
        #add headers to csv file
        with(open(filePath, 'w', newline = '')) as csv_file:
                #will create the file if it does not exist
            writer = csv.writer(csv_file)
            writer.writerow(['sub_rpt_dt','cusip','s_name','value','nshares','sub_rpttyp','sub_fil_dt'])


def downloadFiles(sec_id, fundName):
    #will download all required 13F-HR reports for a given sec_id
    #this seems to handle and avoid duplication from the package
    formattedFundName = fundName.replace(' ', '_')
    downloadPath = os.path.abspath(os.path.join('..','Data', formattedFundName))
    #inialize downloader instance
    dl = Downloader(downloadPath)
    #download all reports
    dl.get("13F-HR",sec_id)




############## process things ###################
fundlistPath = os.path.abspath(os.path.join('..', 'Funds.xlsx')) #read funds.xlsx spreadsheet at root folder
fundsDf = pd.read_excel (fundlistPath)

for i in range(len(fundsDf.index)):
    #get fund name and ID
    fundName = fundsDf['FUND'].iloc[i]
    fundId = fundsDf['SEC ID'].iloc[i]
    checkCreateFolder(fundName) #call checkCreateFolder to create folders and files that are missing
    downloadFiles(sec_id = fundId,fundName = fundName)
    
