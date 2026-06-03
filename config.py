"""
Configurações para o Conversor de Moedas
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Chaves das APIs
API_KEYS = {
    "FIXER": os.getenv("FIXER_API_KEY", ""),
    "OPEN_EXCHANGE": os.getenv("OPEN_EXCHANGE_API_KEY", ""),
}

# Configurações de Cache
CACHE = {
    "ativo": True,
    "duracao_segundos": 3600,  # 1 hora
}

# Moedas padrão
MOEDAS_PADRAO = {
    "BRL": "Real Brasileiro",
    "USD": "Dólar Americano",
    "EUR": "Euro",
    "GBP": "Libra Esterlina",
}

# Timeout para requisições
TIMEOUT = 10

# Rate limiting
RATE_LIMIT = {
    "ativo": True,
    "requisicoes_por_minuto": 60,
}
