
def InsertAssetsStatusData(dbConnection):
    cursor = dbConnection.cursor()
    statements = [
        "INSERT INTO Asset_Status (ID, Label) VALUES (0, 'No breakdown by status')",
        "INSERT INTO Asset_Status (ID, Label) VALUES (1, 'Non defaulted assets')",
        "INSERT INTO Asset_Status (ID, Label) VALUES (2, 'Defaulted assets')",
        "INSERT INTO Asset_Status (ID, Label) VALUES (3, 'New defaulted assets')",
        "INSERT INTO Asset_Status (ID, Label) VALUES (4, 'Old defaulted assets')"
    ]
    for statement in statements:
        cursor.execute(statement)
    dbConnection.commit()
