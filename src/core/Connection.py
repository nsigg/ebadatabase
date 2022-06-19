import mysql.connector as mysql

def getRootConnection(db_user, db_password):
    connection = mysql.connect(
        user = db_user,
        password = db_password,
        database = '',
        host = 'localhost'
    )
    return connection

def getConnection(db_name, db_user, db_password):
    connection = mysql.connect(
        user = db_user,
        password = db_password,
        database = db_name,
        host = 'localhost'
    )
    return connection
