from src.CSVImports.ImportDataDictionary import InsertDataDictionary
from src.CSVImports.ImportSovereign import InsertSovereign
from src.CSVImports.ImportCountryRankExposure import InsertCountryRankExposure
from src.CSVImports.ImportMarketRisk import InsertMarketRisk
from src.CSVImports.ImportBank import InsertBank
from src.CSVImports.ImportOthers import InsertOthers


def InsertCsvData(year, connection, path):
    InsertBank(year, connection, path)
    InsertDataDictionary(year, connection, path)
    InsertSovereign(year, connection, path)
    InsertMarketRisk(year, connection, path)
    InsertCountryRankExposure(year, connection, path)
    InsertOthers(year, connection, path)
    print()
