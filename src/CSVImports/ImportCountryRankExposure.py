import os
import csv
import time
import mysql.connector as mysql
from mysql.connector import errorcode
import src.core.SQLHelper as sqlhelper
import src.CSVImports.Output as output


def getFilePath(year, path):
    return os.path.join(path, str(year), 'tr_cre.csv')


def getLEICode(line):
    if 'LEI_code' in line:
        return line['LEI_code']
    elif 'LEI_Code' in line:
        return line['LEI_Code']


def getAmount(line):
    if 'AMOUNT' in line:
        return line['AMOUNT'].replace(',', '')
    elif 'Amount' in line:
        return line['Amount'].replace(',', '')


def getNaceCode(line):
    if 'NACE_Codes' in line:
        return line['NACE_Codes']
    else:
        return '0'


def InsertCountryRankExposure(year, dbConnection, path):
    output.printBegin('credit risk exposure data', year)
    fullQualifiedFileName = getFilePath(year, path)
    cursor = dbConnection.cursor()
    t = time.process_time()
    scannedCSVLineCount = 0
    missingLines = 0
    with open(fullQualifiedFileName) as file:
        reader = csv.DictReader(file, delimiter=',')
        badLeiCodeList = list()
        itemDic = sqlhelper.getItemDictionary(dbConnection)
        bankDic = sqlhelper.getBanksDictionary(dbConnection)
        insertqueryCreditRiskExposure = 'INSERT INTO credit_risk (GlobalLEI_Code, ItemID, Period, PortfolioID, CountryID, Country_rank, ExposureID, Asset_StatusID, Perf_StatusID, NACE_CodeID, Amount) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        for line in reader:
            scannedCSVLineCount = scannedCSVLineCount + 1
            leiCode = getLEICode(line)
            globalLEI_Code = bankDic.get(leiCode)
            # globalLEI_Code = sqlhelper.getGlobalLEI_Code(dbConnection, leiCode)
            amount = getAmount(line)
            nace_code = getNaceCode(line)
            if(scannedCSVLineCount % 10000 == 0):
                output.printProcessingStatus(scannedCSVLineCount)
            globalId = itemDic.get(int(line['Item']))
            try:
                cursor.execute(insertqueryCreditRiskExposure,
                               (globalLEI_Code, globalId, line['Period'], line['Portfolio'], line['Country'], line['Country_rank'], line['Exposure'], line['Status'], line['Perf_Status'], nace_code, amount))
            except mysql.errors.IntegrityError as error:
                if error.errno == errorcode.ER_NO_REFERENCED_ROW_2:
                    missingLines = missingLines + 1
                    if leiCode in badLeiCodeList:
                        pass
                    else:
                        badLeiCodeList.append(leiCode)
    dbConnection.commit()
    endtime = time.process_time()
    elapsed_time = endtime - t
    output.printSummary(elapsed_time, scannedCSVLineCount)
    if (len(badLeiCodeList) > 0):
        output.printMissingLEICodes(badLeiCodeList, year, missingLines)
