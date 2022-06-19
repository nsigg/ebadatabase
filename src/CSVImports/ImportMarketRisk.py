import os
import csv
import time
import mysql.connector as mysql
from mysql.connector import errorcode
import src.core.SQLHelper as sqlhelper
import src.CSVImports.Output as output


def getFilePath(year, path):
    return os.path.join(path, str(year), 'tr_mrk.csv')


def getLEICode(csvLine):
    if 'LEI_code' in csvLine:
        return csvLine['LEI_code'].upper()
    elif 'LEI_Code' in csvLine:
        return csvLine['LEI_Code'].upper()
    else:
        return


def getAmount(csvLine):
    if 'AMOUNT' in csvLine:
        return csvLine['AMOUNT'].replace(',', '')
    elif 'Amount' in csvLine:
        return csvLine['Amount'].replace(',', '')
    else:
        return


def getFootnote(csvLine):
    if 'Footnote' in csvLine:
        return csvLine['Footnote']
    else:
        return


def InsertMarketRisk(year, dbConnection, path):
    output.printBegin('market risk data', year)
    fullQualifiedFileName = getFilePath(year, path)
    cursor = dbConnection.cursor()
    missingLEICodes = list()
    scannedCSVLineCount = 0
    notInsertedLines = 0
    startTime = time.process_time()
    with open(fullQualifiedFileName) as file:
        csvDictionary = csv.DictReader(file, delimiter=',')
        itemDictionary = sqlhelper.getItemDictionary(dbConnection)
        bankDic = sqlhelper.getBanksDictionary(dbConnection)
        marketRiskInsertQuery = 'INSERT INTO market_risk (GlobalLEI_Code, ItemID, Period, PortfolioID, MKT_ModprodID, MKT_RiskID, Amount, Footnote) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
        for csvLine in csvDictionary:
            scannedCSVLineCount = scannedCSVLineCount + 1
            if(scannedCSVLineCount % 10000 == 0):
                output.printProcessingStatus(scannedCSVLineCount)
            leiCode = getLEICode(csvLine)
            globalLEI_Code = bankDic.get(leiCode)
            amount = getAmount(csvLine)
            footnote = getFootnote(csvLine)
            globalId = itemDictionary.get(int(csvLine['Item']))
            try:
                cursor.execute(marketRiskInsertQuery,
                               (globalLEI_Code, globalId, csvLine['Period'], csvLine['Portfolio'], csvLine['MKT_Modprod'], csvLine['Mkt_risk'], amount, footnote))
            except mysql.errors.IntegrityError as error:
                if error.errno == errorcode.ER_NO_REFERENCED_ROW_2:
                    notInsertedLines = notInsertedLines + 1
                    if leiCode in missingLEICodes:
                        pass
                    else:
                        missingLEICodes.append(leiCode)
    dbConnection.commit()
    endTime = time.process_time()
    elapsedTime = endTime - startTime
    insertedLines = scannedCSVLineCount - notInsertedLines
    output.printSummary(elapsedTime, insertedLines)
    if (len(missingLEICodes) > 0):
        output.printMissingLEICodes(missingLEICodes, year, notInsertedLines)
