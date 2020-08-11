# fundScrapping
This is a program to download and parse all fund holdings for a selected list of funds
The source of the reports SEC Edgar https://sec.report
The package used to bulf download reports can be found at https://pypi.org/project/sec-edgar-downloader/

To add new funds to the download and update list, add a fund name and ID (found on the SEC website) to the funds.xlsx file at the root of the report

To download all required files and update the funds holding .csv files, run Scripts/execute.py
After executing this script, the folder Data/ will contain folders with the funds scrapped
the .csv file named after the name of the funds contains all historical holdings
the folder contains all downloaded SEC reports

## deploy 
Check requirements .txt to create the anaconda environment with all required dependancies

## contents

/Funds.xlsx an excel spreadhsheet with fund names and id to control which fudns get updated
/requirements.txt the list of requirements to create an anaconda environment to run this program

Scripts/update.ipynb a jupyter notebook to download all required pdf reports from SEC website
Scripts/update.py a script to to download all required pdf reports from SEC website

Scripts/process.ipynb a jupyter notebook to process downloaded reports and update fund holdings .csv
Scripts/process.py a script to process downloaded reports and update fund holdings .csv

execute.py a script that will run update.py and process.py to fill all funds .csv files automatically
