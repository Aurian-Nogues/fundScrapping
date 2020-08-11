import pandas as pd
import os
import re
import json
from pathlib import Path
from datetime import datetime

############ define functions ##############

def parser13F(folder):
    #will scan a fund folder and return all parsed info from 13-f in a dataframe
    lst_13F = list()
    cols_names=['sub_rpt_dt','cusip','s_name','value','nshares','sub_rpttyp','sub_fil_dt']
    tab_13F = pd.DataFrame(columns=cols_names)
    n=0
    with os.scandir(folder) as entries:
        for file in entries:
            fh = open(file)
            Fname=file.name
            #print(Fname)
            n=0
            i0=0
            i1=1e6
            report_CAT= None
            for line in fh:
                n=n+1
                if line.find('CONFORMED PERIOD OF REPORT')>-1:
                    sub_rpt_dt = datetime.strptime(str(int(line.split(sep=":")[1])), '%Y%m%d').strftime('%d/%m/%Y')
                if line.find('FILED AS OF DATE')>-1:
                    sub_fil_dt = datetime.strptime(str(int(line.split(sep=":")[1])), '%Y%m%d').strftime('%d/%m/%Y')
                    sub_fil_dt = str(int(line.split(sep=":")[1]))
                if line.find('CONFORMED SUBMISSION TYPE')>-1:
                    sub_rpttyp = str(re.sub('\n','',re.sub('\t','',line.split(sep=":")[1])))
                if line.find('FILENAME')>-1:
                    report_CAT = str(re.sub('\n','',line.split(sep=">")[1].split(sep="<")[0]))[-3:]
                    #print(Fname+' > input typ:'+report_CAT)
                if len(line)<5 or report_CAT is None:
                    continue
                if report_CAT=='xml':      
                    line_words = line.split(sep=">")
                    if line.find('nameOfIssuer>')>-1:
                        s_name = line_words[1].split(sep="<")[0]
                    if line.find('cusip>')>-1:
                        cusip = line_words[1].split(sep="<")[0]
                    if line.find('value>')>-1:
                        value = line_words[1].split(sep="<")[0]
                    if line.find('sshPrnamt>')>-1:
                        nshares = float(line_words[1].split(sep="<")[0])
                        infoT=[[sub_rpt_dt,cusip,s_name,value,nshares,sub_rpttyp,sub_fil_dt]]
                        lst_13F.append(infoT)
                        infoT2 = pd.DataFrame(infoT,columns=cols_names)
                        tab_13F = tab_13F.append(infoT2,ignore_index=True)
                elif report_CAT=='txt':            
    #                if line.find('CAPTION')>-1:
    ##                    n=0
                    if line.find('<S>')>-1:
                        i0 = n
                        lC = [m.start() for m in re.finditer('<C>', line)]
                    if line.find('/TABLE')>-1:
                        i1=n
                        break
    #                    print('i1',n)
    #                print(n)
                    if n>i0 and i0>0 and n<i1:
                        line_words2 = list()
                        for i in range(len([x for x in lC if x<len(line)])+1):
                            if i==0:
                                line_words2.append(line[:lC[i]].strip())
                            elif i==len(lC)+1:
                                line_words2.append(line[lC[i]:].strip())
                            else:
                                line_words2.append(line[lC[i-1]:lC[i]].strip())
                        if line_words2==['No Reportable Holdings']:

                            #print(Fname+': No Reportable Holdings!!!!')
                            continue
                        else:
                            s_name = line_words2[0]
                            cusip = str(line_words2[2])
                            value = float(re.sub(',','',line_words2[3]))
                            nshares = float(re.sub(',','',line_words2[4]))
                            infoT=[[sub_rpt_dt,cusip,s_name,value,nshares,sub_rpttyp,sub_fil_dt]]
                            lst_13F.append(infoT)
                            infoT2 = pd.DataFrame(infoT,columns=cols_names)
                            tab_13F = tab_13F.append(infoT2,ignore_index=True)
    return(tab_13F)


############ process stuff #############

#get list of all funds
fundsFolderPath = os.path.abspath(os.path.join('..','Data'))
fundsList = os.listdir(fundsFolderPath)
fundsList.remove('.gitignore') #remove giti

#for each fund parse info and update fund csv
for fund in fundsList:
    #get fund id which is folder name in sec_edgar_filings
    tempPath = os.path.abspath(os.path.join('..','Data',fund,'sec_edgar_filings'))
    fundId = os.listdir(tempPath)[0]
    #get list of all available filings files for that fund
    fundPath = os.path.abspath(os.path.join('..','Data',fund,'sec_edgar_filings',fundId,'13F-HR'))
    fundHoldingsDf = parser13F(fundPath) #returns a dataframe with fund holdings parsed from all files
    #overwrite csv with new info
    fundHoldingsFilePath = os.path.abspath(os.path.join('..','Data',fund,fund +'.csv'))
    fundHoldingsDf.to_csv(fundHoldingsFilePath, mode = 'w+')


