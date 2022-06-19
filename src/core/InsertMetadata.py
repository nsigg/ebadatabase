from src.schema.AccountingPortfolio import InsertAccountingPortfolioData
from src.schema.AssetsFV import InsertAssetsFVData
from src.schema.AssetsStages import InsertAssetsStagesData
from src.schema.AssetStatus import InsertAssetsStatusData
from src.schema.Country import InsertCountryData
from src.schema.Exposure import InsertExposureData
from src.schema.Maturity import InsertMaturityData
from src.schema.MKTModProd import InsertMKTModProdData
from src.schema.MKTRisk import InsertMKTRiskData
from src.schema.PerfStatus import InsertPerfStatusData
from src.schema.Portfolio import InsertPortfolioData
from src.schema.NaceCode import InsertNaceCodeData



def InsertMetadata(connection):
    InsertAccountingPortfolioData(connection)
    InsertAssetsFVData(connection)
    InsertAssetsStagesData(connection)
    InsertAssetsStatusData(connection)
    InsertCountryData(connection)
    InsertExposureData(connection)
    InsertMaturityData(connection)
    InsertMKTModProdData(connection)
    InsertMKTRiskData(connection)
    InsertPerfStatusData(connection)
    InsertPortfolioData(connection)
    InsertNaceCodeData(connection)