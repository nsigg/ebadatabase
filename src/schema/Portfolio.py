def InsertPortfolioData(dbConnection):
    cursor = dbConnection.cursor()
    statements = [
        "INSERT INTO Portfolio(ID, Label) VALUES(0, 'Total / No breakdown by portfolio')",
        "INSERT INTO Portfolio(ID, Label) VALUES(1, 'SA')",
        "INSERT INTO Portfolio(ID, Label) VALUES(2, 'IRB')",
        "INSERT INTO Portfolio(ID, Label) VALUES(3, 'F-IRB')",
        "INSERT INTO Portfolio(ID, Label) VALUES(4, 'A-IRB')",
        "INSERT INTO Portfolio(ID, Label) VALUES(5, 'IM')",
        "INSERT INTO Portfolio(ID, Label) VALUES(6, 'Fixed rate portfolio')",
        "INSERT INTO Portfolio(ID, Label) VALUES(7, 'Floating rate portfolio')"
    ]
    for statement in statements:
        cursor.execute(statement)
    dbConnection.commit()
