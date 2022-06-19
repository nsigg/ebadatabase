def getItemDictionary(dbConnection):
    itemDictionary = dict()
    cursor = dbConnection.cursor()
    preparedQueryDistinctGlobalIdInId = "SELECT id, globalid FROM item"
    cursor.execute(preparedQueryDistinctGlobalIdInId)
    for item in cursor:
        itemDictionary[item[0]] = item[1]
    return itemDictionary


def getBanksDictionary(dbConnection):
    banksDictionary = dict()
    cursor = dbConnection.cursor()
    preparedQueryDistinctGlobalIdInId = "SELECT LEI_Code, GlobalLEI_Code FROM bank"
    cursor.execute(preparedQueryDistinctGlobalIdInId)
    for line in cursor:
        banksDictionary[line[0]] = line[1]
    return banksDictionary


def getAllLEI_Codes(dbConnection):
    lei_codes = []
    cursor = dbConnection.cursor()
    cursor.execute("SELECT DISTINCT LEI_Code from bank")
    for row in cursor:
        lei_codes.append(row[0])
    return lei_codes


def getGlobalLEI_Code(dbConnection, leiCode):
    cursor = dbConnection.cursor()
    cursor.execute(
        f"SELECT DISTINCT GlobalLEI_Code from bank WHERE LEI_Code = '{leiCode}'")
    row = cursor.fetchone()
    return row[0]


def InsertNewGlobalLEI_Code(dbConnection):
    cursor = dbConnection.cursor()
    cursor.execute("INSERT INTO bankmeta VALUES ()")
    dbConnection.commit()
    return cursor.lastrowid


def getColumnDefinition(table):
    if table == 'sovereign':
        return ["GlobalLEI_Code", "ItemID", "Period", "CountryID",
                "Accounting_PortfolioID", "MaturityID", "Amount", "Footnote"]
    elif table == 'Market_risk':
        return ["GlobalLEI_Code", "ItemID", "Period", "PortfolioID", "MKT_ModprodID",
                "MKT_RiskID", "Amount", "Footnote"]
    elif table == 'Credit_risk':
        return ["GlobalLEI_Code", "ItemID", "Period", "PortfolioID", "CountryID", "Country_rank",
                "ExposureID", "Asset_StatusID", "Perf_StatusID", "NACE_CodeID", "Amount", "Footnote"]
    elif table == 'others':
        return ["GlobalLEI_Code", "ItemID", "Period", "Portfolio", "ASSETS_FvID",
                "ASSETS_StagesID", "Amount", "N_Quarters", "Footnote"]
