def InsertMKTRiskData(dbConnection):
    cursor = dbConnection.cursor()
    statements = [
        "INSERT INTO MKT_Risk VALUES(0, 'No breakdown by MKT_Risk')",
        "INSERT INTO MKT_Risk VALUES(1, 'General risk')",
        "INSERT INTO MKT_Risk VALUES(2, 'Specific risk')"
    ]
    for statement in statements:
        cursor.execute(statement)
    dbConnection.commit()
