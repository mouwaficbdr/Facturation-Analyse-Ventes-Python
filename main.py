from services.statistics_service import StatisticsService
from models.client import Client

stats = StatisticsService(
    'exports/historique_factures.xlsx',
    'data/Clients.xlsx',
    'data/Produits.xlsx',
    'data/CartesReduction.xlsx'
)


print(Client.getallClients())