def InsertMaturityData(dbConnection):
    cursor = dbConnection.cursor()
    statements = [
        "INSERT INTO Maturity VALUES(0, 'No breakdown by maturity')",
        "INSERT INTO Maturity VALUES(1, '[ 0 - 3M ]')",
        "INSERT INTO Maturity VALUES(2, '[ 3M - 1Y ]')",
        "INSERT INTO Maturity VALUES(3, '[ 1Y - 2Y ]')",
        "INSERT INTO Maturity VALUES(4, '[ 2Y - 3Y ]')",
        "INSERT INTO Maturity VALUES(5, '[3Y - 5Y ]')",
        "INSERT INTO Maturity VALUES(6, '[5Y - 10Y ]')",
        "INSERT INTO Maturity VALUES(7, '[10Y - more ]')",
        "INSERT INTO Maturity VALUES(8, 'Total')"
    ]
    for statement in statements:
        cursor.execute(statement)
    dbConnection.commit()
