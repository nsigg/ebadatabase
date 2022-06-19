def InsertMKTModProdData(dbConnection):
    cursor = dbConnection.cursor()
    statements = [
        "INSERT INTO MKT_modprod VALUES(0, 'No breakdown by MKT_Modprod')",
        "INSERT INTO MKT_modprod VALUES(1, 'Traded debt instruments')",
        "INSERT INTO MKT_modprod VALUES(2, 'Equities')",
        "INSERT INTO MKT_modprod VALUES(3, 'Foreign Exchange risk')",
        "INSERT INTO MKT_modprod VALUES(4, 'Commodity risk')"
    ]
    for statement in statements:
        cursor.execute(statement)
    dbConnection.commit()
