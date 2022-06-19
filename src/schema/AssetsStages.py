
def InsertAssetsStagesData(dbConnection):
    cursor = dbConnection.cursor()
    statements = [
        "INSERT INTO ASSETS_Stages(ID, Label) VALUES (0, 'No breakdown by ASSETS_Stages')",
        "INSERT INTO ASSETS_Stages(ID, Label) VALUES (1, 'Stage 1: Assets without significant increase in credit risk since initial recognition')",
        "INSERT INTO ASSETS_Stages(ID, Label) VALUES (2, 'Stage 2: Assets with significant increase in credit risk since initial recognition but not credit-impaired')",
        "INSERT INTO ASSETS_Stages(ID, Label) VALUES (3, 'Stage 3: Credit-impaired assets')"
    ]
    for statement in statements:
        cursor.execute(statement)
    dbConnection.commit()
