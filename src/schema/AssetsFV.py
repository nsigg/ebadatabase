
def InsertAssetsFVData(dbConnection):
    cursor = dbConnection.cursor()
    statements = [
        "INSERT INTO ASSETS_FV(ID, Label) VALUES (0, 'No breakdown by ASSETS_FV')",
        "INSERT INTO ASSETS_FV(ID, Label) VALUES (1, 'Fair value hierarchy: Level 1')",
        "INSERT INTO ASSETS_FV(ID, Label) VALUES (2, 'Fair value hierarchy: Level 2')",
        "INSERT INTO ASSETS_FV(ID, Label) VALUES (3, 'Fair value hierarchy: Level 3')"
    ]
    for statement in statements:
        cursor.execute(statement)
    dbConnection.commit()
