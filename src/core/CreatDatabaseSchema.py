def setUpDatabase(connection, db_name):
    cursor = connection.cursor()
    # DROP EXISTING DATABASE
    cursor.execute(
        f"DROP DATABASE IF EXISTS {db_name}"
        )
    cursor.execute(
        f"CREATE DATABASE {db_name} CHARACTER SET utf8"
        )
    cursor.execute(
        f"USE {db_name}"
        )
    # SETUP SCHEMA
    cursor.execute(
        """CREATE TABLE Portfolio(
            ID int PRIMARY KEY, 
            Label varchar(2000)
        )"""
    )
    cursor.execute(
        """CREATE TABLE Exposure(
            ID int PRIMARY KEY, 
            Label varchar(2000)
        )"""
    )
    cursor.execute(
        """CREATE TABLE Asset_Status(
            ID int PRIMARY KEY, 
            Label varchar(2000)
        )"""
    )
    cursor.execute(
        """CREATE TABLE Perf_Status(
            ID int PRIMARY KEY, 
            Label varchar(2000)
        )"""
    )
    cursor.execute(
        """CREATE TABLE MKT_Modprod(
            ID int PRIMARY KEY, 
            Label varchar(2000)
        )"""
    )
    cursor.execute(
        """CREATE TABLE MKT_Risk(
            ID int PRIMARY KEY, 
            Label varchar(2000)
        )"""
    )
    cursor.execute(
        """CREATE TABLE Accounting_Portfolio(
            ID int PRIMARY KEY, 
            Label varchar(2000)
        )"""
    )
    cursor.execute(
        """CREATE TABLE Maturity(
            ID int PRIMARY KEY, 
            Label varchar(2000)
        )"""
    )
    cursor.execute(
        """CREATE TABLE ASSETS_FV(
            ID int PRIMARY KEY, 
            Label varchar(2000)
        )"""
    )
    cursor.execute(
        """CREATE TABLE ASSETS_Stages(
            ID int PRIMARY KEY, 
            Label varchar(2000)
        )"""
    )
    cursor.execute(
        """CREATE TABLE NACE_Code(
            ID int PRIMARY KEY, 
            Label varchar(2000)
        )"""
    )
    cursor.execute(
        """CREATE TABLE Country(
            ID int PRIMARY KEY, 
            Label varchar(2000), 
            ISO_Code varchar(3) UNIQUE
        )"""
    )
    cursor.execute(
        """CREATE TABLE BankMeta(
            GlobalLEI_Code int auto_increment PRIMARY KEY
        )"""
    )
    cursor.execute(
        """CREATE TABLE Bank(
            year int,
            Country_Code varchar(3),
            SSM varchar(3),
            LEI_Code char(20),
            GlobalLEI_Code int,
            Name varchar(2000),
            FinRep varchar(100),
            FinancialYearEnd char(5),
            PRIMARY KEY (year, LEI_Code),  
            CONSTRAINT FK_bank_bankmeta FOREIGN KEY (GlobalLEI_Code) REFERENCES BankMeta (GlobalLEI_Code),  
            CONSTRAINT FK_bank_country FOREIGN KEY (Country_code) REFERENCES Country (ISO_Code)
        )"""
    )
    cursor.execute(
        """CREATE TABLE ItemMeta(
            GlobalID int auto_increment PRIMARY KEY,
            Label varchar(2000)
        )"""
    )
    cursor.execute(
        """CREATE TABLE Item (
            ID int PRIMARY KEY,
            GlobalID int,
            CONSTRAINT FK_Item_ItemMeta FOREIGN KEY (GlobalID) REFERENCES ItemMeta (GlobalID)
        )"""
    )
    cursor.execute(
        """CREATE TABLE ItemTemplate (
            ID int,
            Template VARCHAR(200),
            PRIMARY KEY (ID, Template),
            CONSTRAINT FK_ItemTemplate_Item FOREIGN KEY (ID) REFERENCES Item (ID)
        )"""
    )
    cursor.execute(
        """CREATE TABLE Credit_risk(
            GlobalLEI_Code int,
            ItemID int,
            Period int,
            PortfolioID int,
            CountryID int,
            Country_rank int,
            ExposureID int,
            Asset_StatusID int,
            Perf_StatusID int,
            NACE_CodeID int,
            Amount decimal(28, 12),
            Footnote varchar(2000),
            Primary Key(GlobalLEI_Code, ItemID, Period, PortfolioID, CountryID, Country_rank, ExposureID, Asset_StatusID, Perf_StatusID, NACE_CodeID),
            CONSTRAINT FK_Credit_BankMeta FOREIGN KEY(GlobalLEI_Code) REFERENCES BankMeta(GlobalLEI_Code),
            CONSTRAINT FK_Credit_ItemMeta FOREIGN KEY(ItemID) REFERENCES ItemMeta(GlobalID),
            CONSTRAINT FK_Credit_Portfolio FOREIGN KEY(PortfolioID) REFERENCES Portfolio(ID),
            CONSTRAINT FK_Credit_Country FOREIGN KEY(CountryID) REFERENCES Country(ID),
            CONSTRAINT FK_Credit_Exposure FOREIGN KEY(ExposureID) REFERENCES Exposure(ID),
            CONSTRAINT FK_Credit_AssetStatus FOREIGN KEY(Asset_StatusID) REFERENCES Asset_Status(ID),
            CONSTRAINT FK_Credit_PerfStatus FOREIGN KEY(Perf_StatusID) REFERENCES Perf_Status(ID),
            CONSTRAINT FK_Credit_NACECode FOREIGN KEY(NACE_CodeID) REFERENCES NACE_Code(ID)
        )"""
    )
    cursor.execute(
        """CREATE TABLE Market_risk(
            GlobalLEI_Code int,
            ItemID int,
            Period int,
            PortfolioID int,
            MKT_ModprodID int,
            MKT_RiskID int,
            Amount decimal(28, 12),
            Footnote varchar(2000),
            Primary Key(GlobalLEI_Code, ItemID, Period, PortfolioID, MKT_ModprodID, MKT_RiskID),
            CONSTRAINT FK_Market_BankMeta FOREIGN KEY(GlobalLEI_Code) REFERENCES BankMeta(GlobalLEI_Code),
            CONSTRAINT FK_Market_ItemMeta FOREIGN KEY(ItemID) REFERENCES ItemMeta(GlobalID),
            CONSTRAINT FK_Market_Portfolio FOREIGN KEY(PortfolioID) REFERENCES Portfolio(ID),
            CONSTRAINT FK_Market_MKTModprod FOREIGN KEY(MKT_ModprodID)  REFERENCES MKT_Modprod(ID),
            CONSTRAINT FK_Market_MKTRisk FOREIGN KEY(MKT_RiskID) REFERENCES MKT_Risk(ID)
        )"""
    )
    cursor.execute(
        """CREATE TABLE others(
            GlobalLEI_Code int,
            ItemID int,
            Period int,
            ASSETS_FvID int,
            ASSETS_StagesID int,
            Amount decimal(28, 12),
            N_Quarters int,
            Footnote varchar(2000),
            Primary Key(GlobalLEI_Code, ItemID, Period, ASSETS_FvID, ASSETS_StagesID),
            CONSTRAINT FK_others_BankMeta FOREIGN KEY(GlobalLEI_Code) REFERENCES BankMeta(GlobalLEI_Code),
            CONSTRAINT FK_others_ItemMeta FOREIGN KEY (ItemID) REFERENCES ItemMeta (GlobalID),
            CONSTRAINT FK_others_ASSETSFV FOREIGN KEY (ASSETS_FvID) REFERENCES ASSETS_FV (ID),
            CONSTRAINT FK_others_ASSETSStages FOREIGN KEY (ASSETS_StagesID) REFERENCES ASSETS_Stages (ID)
        )"""
    )
    cursor.execute(
        """CREATE TABLE sovereign(
            GlobalLEI_Code int,
            ItemID int,
            Period int,
            CountryID int,
            Accounting_PortfolioID int,
            MaturityID int,
            Amount decimal(28, 12),
            Footnote varchar(2000),
            Primary Key(GlobalLEI_Code, ItemID, Period, CountryID, Accounting_PortfolioID, MaturityID),
            CONSTRAINT FK_sovereign_BankMeta FOREIGN KEY(GlobalLEI_Code) REFERENCES BankMeta(GlobalLEI_Code),
            CONSTRAINT FK_sovereign_ItemMeta FOREIGN KEY (ItemID) REFERENCES ItemMeta (GlobalID),
            CONSTRAINT FK_sovereign_Country FOREIGN KEY (CountryID) REFERENCES Country (ID),
            CONSTRAINT FK_sovereign_AccountingPortfolio FOREIGN KEY (Accounting_PortfolioID) REFERENCES Accounting_Portfolio (ID),
            CONSTRAINT FK_sovereign_Maturity FOREIGN KEY (MaturityID) REFERENCES Maturity (ID)
        )"""
    )
    connection.commit()
