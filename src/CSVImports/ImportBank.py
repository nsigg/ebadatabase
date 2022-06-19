import os
import csv
import time
import mysql.connector as mysql
from mysql.connector import errorcode
import src.CSVImports.Output as output
import src.core.SQLHelper as sqlhelper


def getFilePath(year, path):
    return os.path.join(path, str(year), 'banks.csv')


def getLEICode(csvLine):
    if 'LEI_code' in csvLine:
        return csvLine['LEI_code'].upper()
    elif 'LEI_Code' in csvLine:
        return csvLine['LEI_Code'].upper()
    elif 'LEI Code' in csvLine:
        return csvLine['LEI Code'].upper()
    else:
        return


def getBankName(csvLine):
    if 'Bank_name' in csvLine:
        return csvLine['Bank_name']
    elif 'Name' in csvLine:
        return csvLine['Name']
    else:
        return


def getCountryCode(csvLine):
    if 'Country_code' in csvLine:
        return csvLine['Country_code']
    elif 'Country code' in csvLine:
        return csvLine['Country code']
    elif 'Country' in csvLine:
        return csvLine['Country']
    else:
        return


def getSSM(csvLine):
    if 'SSM' in csvLine:
        return csvLine['SSM']
    else:
        return


def getFinRep(csvLine):
    if 'Finrep' in csvLine:
        return csvLine['Finrep']
    else:
        return


def getFinancialYearEnd(csvLine):
    if 'Fin_year_end' in csvLine:
        yearEnd = csvLine['Fin_year_end']
    elif 'Financial Year End' in csvLine:
        yearEnd = csvLine['Financial Year End']
    elif 'Financial year end' in csvLine:
        yearEnd = csvLine['Financial year end']
    else:
        return
    if 'Dez' in yearEnd or 'Dec' in yearEnd:
        yearEnd = '31/12'
    return yearEnd


def getGlobalLEI_Code(leiCode, csvLine, dbConnection):
    allLeiCodes = sqlhelper.getAllLEI_Codes(dbConnection)
    if leiCode in allLeiCodes:
        return sqlhelper.getGlobalLEI_Code(dbConnection, leiCode)
    else:
        for col in csvLine:
            possibleLeiCode = csvLine[str(col)]
            if possibleLeiCode in allLeiCodes:
                return sqlhelper.getGlobalLEI_Code(dbConnection, possibleLeiCode)
        return sqlhelper.InsertNewGlobalLEI_Code(dbConnection)


def InsertBank(year, dbConnection, path):
    output.printBegin('banks', year)
    fullQualifiedFileName = getFilePath(year, path)
    cursor = dbConnection.cursor()
    scannedCSVLineCount = 0
    alreadyInsertedLines = 0
    startTime = time.process_time()
    with open(fullQualifiedFileName, encoding='utf-8') as file:
        csvDictionary = csv.DictReader(file, delimiter=';')
        bankInsertQuery = 'INSERT INTO bank(year, Country_Code, SSM, LEI_Code, GlobalLEI_Code, Name, FinRep, FinancialYearEnd) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
        for csvLine in csvDictionary:
            scannedCSVLineCount = scannedCSVLineCount + 1
            if(scannedCSVLineCount % 10000 == 0):
                output.printProcessingStatus(scannedCSVLineCount)
            leiCode = getLEICode(csvLine)
            globalLEI_Code = getGlobalLEI_Code(leiCode, csvLine, dbConnection)
            name = getBankName(csvLine)
            countryCode = getCountryCode(csvLine)
            ssm = getSSM(csvLine)
            finrep = getFinRep(csvLine)
            financialYearEnd = getFinancialYearEnd(csvLine)
            if countryCode == 'OT':
                countryCode = '00'
            elif countryCode == 'UK':
                countryCode = 'GB'
            try:
                cursor.execute(bankInsertQuery,
                               (year, countryCode, ssm, leiCode, globalLEI_Code, name, finrep, financialYearEnd))
            except mysql.errors.IntegrityError as error:
                if error.errno == errorcode.ER_DUP_ENTRY:
                    alreadyInsertedLines = alreadyInsertedLines + 1
                    # Doppelter Eintrag ist nicht erlaubt, aber kein Prob da schon gespeichert.
                else:
                    raise error
    dbConnection.commit()
    endTime = time.process_time()
    elapsedTime = endTime - startTime
    insertedLines = scannedCSVLineCount - alreadyInsertedLines
    output.printSummary(elapsedTime, insertedLines)
