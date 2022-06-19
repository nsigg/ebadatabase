
def InsertAccountingPortfolioData(dbConnection):
    cursor = dbConnection.cursor()

    statements = [
        "INSERT INTO Accounting_portfolio(ID, Label) VALUES(0, 'No breakdown by Accounting_portfolio')",
        "INSERT INTO Accounting_portfolio(ID, Label) VALUES(1, 'Held for trading')",
        "INSERT INTO Accounting_portfolio(ID, Label) VALUES(2, 'Designated at fair value through profit or loss')",
        "INSERT INTO Accounting_portfolio(ID, Label) VALUES(3, 'Available-for-sale')",
        "INSERT INTO Accounting_portfolio(ID, Label) VALUES(4, 'Loans and Receivables')",
        "INSERT INTO Accounting_portfolio(ID, Label) VALUES(5, 'Held-to-maturity investments')"
    ]
    for statement in statements:
      cursor.execute(statement)

    dbConnection.commit()
