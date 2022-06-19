def InsertPerfStatusData(dbConnection):
    cursor = dbConnection.cursor()
    statements = [
        "INSERT INTO Perf_Status(ID, Label) VALUES(0, 'No breakdown by Perf_status')",
        "INSERT INTO Perf_Status(ID, Label) VALUES(1, 'Performing')",
        "INSERT INTO Perf_Status(ID, Label) VALUES(2, 'Non Performing')",
        "INSERT INTO Perf_Status(ID, Label) VALUES(3, 'Performing but past due >30 days and <=90 days')",
        "INSERT INTO Perf_Status(ID, Label) VALUES(4, 'Non Performing and Defaulted')",
        "INSERT INTO Perf_Status(ID, Label) VALUES(5, 'Loans and advances subject to impairment')"
    ]
    for statement in statements:
        cursor.execute(statement)
    dbConnection.commit()
