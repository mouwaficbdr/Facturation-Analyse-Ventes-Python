from services.statistics_service import StatisticsService

stats = StatisticsService(
    'exports/historique_factures .xlsx',
    'data/Clients.xlsx',
    'data/Produits.xlsx',
    'data/CartesReduction.xlsx'
)
