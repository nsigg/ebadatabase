import os
import csv
import time
import mysql.connector as mysql
from src.core.SQLHelper import getItemDictionary
import src.CSVImports.Output as output
import src.core.SQLHelper as sqlhelper


def InsertSovereign(year, dbConnection, path):
    output.printBegin('sovereign data', year)
    year_path = os.path.join(path, str(year))
    count_of_sov_files = 0
    for file in os.listdir(year_path):
        if 'tr_sov' in file:
            count_of_sov_files += 1
    if count_of_sov_files > 1:
        fullQualifiedFileName = os.path.join(
            path, str(year), f'tr_sov_{year}06.csv')
        ActualInsert(year, fullQualifiedFileName, dbConnection)

        fullQualifiedFileName = os.path.join(
            path, str(year), f'tr_sov_{year - 1}12.csv')
        ActualInsert(year, fullQualifiedFileName, dbConnection)
    else:
        fullQualifiedFileName = os.path.join(path, str(year), 'tr_sov.csv')
        ActualInsert(year, fullQualifiedFileName, dbConnection)


def cleanData(line, year):
    if year == 2015:
        line['Amount'] = line['AMOUNT']
        line['LEI_Code'] = line['LEI_code']

    line['Amount'] = line['Amount'].replace(',', '')

    if 'Accounting_portfolio' not in line:
        line['Accounting_portfolio'] = '0'
    if 'Maturity' not in line:
        line['Maturity'] = '0'
    if 'Footnote' not in line:
        line['Footnote'] = ''
    if line['Amount'] == '':
        line['Amount'] = '0'


def ActualInsert(year, fileName, dbConnection):
    cursor = dbConnection.cursor()
    itemDictionary = getItemDictionary(dbConnection)
    bankDic = sqlhelper.getBanksDictionary(dbConnection)
    scannedLines = 0
    preparedInsertQuery = "INSERT INTO sovereign (GlobalLEI_Code, ItemID, Period, CountryID, Accounting_PortfolioID, MaturityID, Amount, Footnote) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    startTime = time.process_time()
    with open(fileName) as file:
        reader = csv.DictReader(file, delimiter=',')
        for line in reader:
            scannedLines += 1
            if scannedLines % 10000 == 0:
                output.printProcessingStatus(scannedLines)
            globalId = itemDictionary.get(int(line['Item']))
            cleanData(line, year)
            if line['LEI_Code'].isalnum():
                globalLEI_Code = bankDic.get(line['LEI_Code'].upper())
                data = (globalLEI_Code,
                        globalId,
                        line['Period'],
                        line['Country'],
                        line['Accounting_portfolio'],
                        line['Maturity'],
                        line['Amount'],
                        line['Footnote'])
                cursor.execute(preparedInsertQuery, data)
    dbConnection.commit()
    endTime = time.process_time()
    elapsedTime = endTime - startTime
    output.printSummary(elapsedTime, scannedLines)
