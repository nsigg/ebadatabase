import os
import csv
import time
import mysql.connector
from mysql.connector import errorcode
import src.CSVImports.Output as output


def getFilePath(year, path):
    return os.path.join(path, str(year), 'sdd.csv')


def InsertDataDictionary(year, dbConnection, path):
    output.printBegin('dictionary data', year)
    fullQualifiedFileName = getFilePath(year, path)
    cursor = dbConnection.cursor()
    startTime = time.process_time()
    with open(fullQualifiedFileName) as file:
        reader = csv.DictReader(file, delimiter=';')
        firstIteration: bool = True
        neededColumns = list()
        scannedCSVLineCount = 0
        NotInsertedLines = 0
        for line in reader:
            scannedCSVLineCount = scannedCSVLineCount + 1
            if firstIteration:
                firstIteration = False
                keys = line.keys()
                for key in keys:
                    if(key.startswith('Item_TR_')):
                        neededColumns.append(key)
            if(scannedCSVLineCount % 10000 == 0):
                output.printProcessingStatus(scannedCSVLineCount)
            if len(neededColumns) > 0:
                itemIds = list()
                for column in neededColumns:
                    id = line[column]
                    if len(id) > 0:
                        itemIds.append(id)
                if len(itemIds) > 0:
                    format_strings = ','.join(['%s'] * len(itemIds))
                    preparedQueryDistinctGlobalIdInId = "SELECT DISTINCT globalid as ID FROM item WHERE ID IN(%s)"
                    cursor.execute(preparedQueryDistinctGlobalIdInId %
                                   format_strings, tuple(itemIds))
                    res = cursor.fetchall()
                    globalId = res[0][0]
                    item = line['Item']
                    try:
                        preparedInsertQuery = f"INSERT INTO item (id, globalid) VALUES ({item}, {globalId})"
                        cursor.execute(preparedInsertQuery)
                        template = ''
                        if year == 2015:
                            template = line['Template No.']
                        elif 'DERIVED_TEMPLATE' in line:
                            template = line['DERIVED_TEMPLATE']
                        elif 'Template' in line:
                            template = line['Template']
                        preparedInsertQuery = f"INSERT INTO itemtemplate (ID, Template) VALUES ({item}, '{template}')"
                        cursor.execute(preparedInsertQuery)
                    except mysql.connector.errors.IntegrityError as error:
                        if error.errno == errorcode.ER_DUP_ENTRY:
                            # Doppelter Eintrag ist nicht erlaubt, aber kein Problem, da das Item schon gespeichert ist.
                            template = ''
                            if year == 2015:
                                template = line['Template No.']
                            elif 'DERIVED_TEMPLATE' in line:
                                template = line['DERIVED_TEMPLATE']
                            elif 'Template' in line:
                                template = line['Template']
                            try:
                                preparedInsertQuery = f"INSERT INTO itemtemplate (ID, Template) VALUES ({item}, '{template}')"
                                cursor.execute(preparedInsertQuery)
                            except mysql.connector.errors.IntegrityError as error:
                                if error.errno == errorcode.ER_DUP_ENTRY:
                                    print(
                                        f"Item {item} in Zeile {scannedCSVLineCount} ist doppelt vorhanden. Der Eintrag wird übersprungen und der Import fortgesetzt. --> möglicher Fehler in den Daten der EBA?")
                                    pass
                                else:
                                    raise error

                        else:
                            raise error
                else:
                    if year == 2015:
                        template = line['Template No.']
                    elif 'DERIVED_TEMPLATE' in line:
                        template = line['DERIVED_TEMPLATE']
                    elif 'Template' in line:
                        template = line['Template']
                    label = line['Label']
                    item = line['Item']
                    generatedGlobalId = cursor.lastrowid
                    try:
                        preparedInsertQuery = f"INSERT INTO itemmeta (Label) VALUES ('{label}')"
                        cursor.execute(preparedInsertQuery)
                        generatedGlobalId = cursor.lastrowid
                        preparedInsertQuery = f"INSERT INTO item (ID, GlobalID) VALUES ({item}, {generatedGlobalId})"
                        cursor.execute(preparedInsertQuery)
                        preparedInsertQuery = f"INSERT INTO itemtemplate (ID, Template) VALUES ({item}, '{template}')"
                        cursor.execute(preparedInsertQuery)
                    except mysql.connector.errors.IntegrityError as error:
                        if error.errno == errorcode.ER_DUP_ENTRY:
                            NotInsertedLines = NotInsertedLines + 1
                            preparedDeleteQuery = f"DELETE FROM itemmeta WHERE globalid = {generatedGlobalId}"
                            cursor.execute(preparedDeleteQuery)
                            preparedInsertQuery = f"INSERT INTO itemtemplate (ID, Template) VALUES ({item}, '{template}')"
                            cursor.execute(preparedInsertQuery)
                            # Doppelter Eintrag ist nicht erlaubt, aber kein Prob da schon gespeichert.
                        else:
                            raise error
            else:
                if year == 2020:
                    print(line)
                if year == 2015:
                    template = line['Template No.']
                elif 'DERIVED_TEMPLATE' in line:
                    template = line['DERIVED_TEMPLATE']
                elif 'Template' in line:
                    template = line['Template']
                label = line['Label']
                item = line['Item']
                try:
                    preparedInsertQuery = f"INSERT INTO itemmeta (Label) VALUES ('{label}')"
                    cursor.execute(preparedInsertQuery)
                    generatedGlobalId = cursor.lastrowid
                    preparedInsertQuery = f"INSERT INTO item (ID, GlobalID) VALUES ({item}, {generatedGlobalId})"
                    cursor.execute(preparedInsertQuery)
                    preparedInsertQuery = f"INSERT INTO itemtemplate (ID, Template) VALUES ({item}, '{template}')"
                    cursor.execute(preparedInsertQuery)
                except mysql.connector.errors.IntegrityError as error:
                    if error.errno == errorcode.ER_DUP_ENTRY:
                        NotInsertedLines = NotInsertedLines + 1
                        preparedDeleteQuery = f"DELETE FROM itemmeta WHERE globalid = {generatedGlobalId}"
                        cursor.execute(preparedDeleteQuery)
                        preparedInsertQuery = f"INSERT INTO itemtemplate (ID, Template) VALUES ({item}, '{template}')"
                        cursor.execute(preparedInsertQuery)
                        # Doppelter Eintrag ist nicht erlaubt, aber kein Prob da schon gespeichert.
                    else:
                        raise error
        dbConnection.commit()
        endTime = time.process_time()
        elapsedTime = endTime - startTime
        insertedLines = scannedCSVLineCount - NotInsertedLines
        output.printSummary(elapsedTime, insertedLines)
