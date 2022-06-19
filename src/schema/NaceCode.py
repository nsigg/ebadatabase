def InsertNaceCodeData(dbConnection):
    cursor = dbConnection.cursor()
    statements = [
        "INSERT INTO NACE_Code(ID, Label) VALUES(0, 'No breakdown by NACE_codes');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(1, 'A Agriculture, forestry and fishing');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(2, 'B Mining and quarrying');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(3, 'C Manufacturing');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(4, 'D Electricity, gas, steam and air conditioning supply');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(5, 'E Water supply');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(6, 'F Construction');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(7, 'G Wholesale and retail trade');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(8, 'H Transport and storage');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(9, 'I Accommodation and food service activities');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(10, 'J Information and communication');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(11, 'K Financial and insurance activities');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(12, 'L Real estate activities');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(13, 'M Professional, scientific and technical activities');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(14, 'N Administrative and support service activities');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(15, 'O Public administration and defence, compulsory social security');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(16, 'P Education');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(17, 'Q Human health services and social work activities');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(18, 'R Arts, entertainment and recreation');",
        "INSERT INTO NACE_Code(ID, Label) VALUES(19, 'S Other services');"
    ]
    for statement in statements:
        cursor.execute(statement)
    dbConnection.commit()
