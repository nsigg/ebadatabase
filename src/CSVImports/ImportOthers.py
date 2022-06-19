import os
import csv
import time
import mysql.connector as mysql
from mysql.connector import errorcode
import src.CSVImports.Output as output
import src.core.SQLHelper as sqlhelper


def cleanData(line):
    if 'AMOUNT' in line:
        line['Amount'] = line['AMOUNT']
    if line['Amount'] == '':
        line['Amount'] = '0'
    if 'LEI_code' in line:
        line['LEI_Code'] = line['LEI_code']
    if 'footnote' not in line:
        line['footnote'] = ''
    if 'n_quarters' not in line:
        line['n_quarters'] = 4
    if 'ASSETS_FV' not in line:
        line['ASSETS_FV'] = 0
    if 'ASSETS_Stages' not in line:
        line['ASSETS_Stages'] = 0
    line['Amount'] = line['Amount'].replace(',', '')


def getFilePath(year, path):
    return os.path.join(path, str(year), 'tr_oth.csv')


def InsertOthers(year, connection, path):
    output.printBegin('other data', year)
    fullQualifiedFileName = getFilePath(year, path)
    cursor = connection.cursor()
    scannedLines = 0
    itemDictionary = sqlhelper.getItemDictionary(connection)
    bankDic = sqlhelper.getBanksDictionary(connection)
    preparedInsertQuery = 'INSERT INTO others (GlobalLEI_Code, ItemID, Period, ASSETS_FvID, ASSETS_StagesID, Amount, N_Quarters, Footnote) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    startTime = time.process_time()
    with open(fullQualifiedFileName) as file:
        reader = csv.DictReader(file, delimiter=',')
        for line in reader:
            scannedLines += 1
            if (scannedLines % 10000 == 0):
                output.printProcessingStatus(scannedLines)
            cleanData(line)
            globalId = itemDictionary.get(int(line['Item']))
            globalLEI_Code = bankDic.get(line['LEI_Code'].upper())
            data = (globalLEI_Code,
                    globalId,
                    line['Period'],
                    line['ASSETS_FV'],
                    line['ASSETS_Stages'],
                    line['Amount'],
                    line['n_quarters'],
                    line['footnote'])
            try:
                cursor.execute(preparedInsertQuery, data)
            except mysql.errors.IntegrityError as error:
                if error.errno == errorcode.ER_DUP_ENTRY:
                    preparedUpdateQuery = 'UPDATE others SET Amount = Amount + %s WHERE GlobalLEI_Code = %s AND ItemID = %s AND Period = %s AND ASSETS_FvID = %s AND ASSETS_StagesID = %s'
                    data = (line['Amount'],
                            globalLEI_Code,
                            globalId,
                            line['Period'],
                            line['ASSETS_FV'],
                            line['ASSETS_Stages']
                            )
                    cursor.execute(preparedUpdateQuery, data)
                    pass
    connection.commit()
    endTime = time.process_time()
    elapsedTime = endTime - startTime
    output.printSummary(elapsedTime, scannedLines)
