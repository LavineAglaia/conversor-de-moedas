"""
Conversor de Moedas - Consome APIs públicas de câmbio
Suporta múltiplas APIs e moedas
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from enum import Enum
import time

# ==================== CONFIGURAÇÃO DE LOGGING ====================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('currency_converter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== ENUMS ====================

class TipoAPI(str, Enum):
    """Tipos de APIs disponíveis"""
    EXCHANGE_RATE_API = "exchangerate"
    FREE_CURRENCY_API = "freecurrency"
    FIXER = "fixer"
    OPEN_EXCHANGE = "openexchange"

# ==================== CLASSE PRINCIPAL ====================

class CurrencyConverter:
    """Conversor de moedas com suporte a múltiplas APIs"""
    
    # URLs das APIs
    APIS = {
        TipoAPI.EXCHANGE_RATE_API: {
            "url": "https://api.exchangerate-api.com/v4/latest/",
            "docs": "https://exchangerate-api.com",
            "gratuita": True,
            "limite": 1500  # requisições por mês
        },
        TipoAPI.FREE_CURRENCY_API: {
            "url": "https://api.freecurrencyapi.com/v1/latest",
            "docs": "https://freecurrencyapi.com",
            "gratuita": True,
            "parametro_base": "base_currency",
            "limite": 300  # requisições por mês
        },
        TipoAPI.FIXER: {
            "url": "https://api.fixer.io/latest",
            "docs": "https://fixer.io",
            "gratuita": False,
            "chave_obrigatoria": True
        },
        TipoAPI.OPEN_EXCHANGE: {
            "url": "https://openexchangerates.org/api/latest.json",
            "docs": "https://openexchangerates.org",
            "gratuita": False,
            "chave_obrigatoria": True
        }
    }
    
    def __init__(self, api_tipo: TipoAPI = TipoAPI.EXCHANGE_RATE_API, chave_api: str = None):
        """
        Inicializa o conversor de moedas
        
        Args:
            api_tipo: Tipo de API a usar
            chave_api: Chave da API (se necessário)
        """
        self.api_tipo = api_tipo
        self.chave_api = chave_api
        self.cache = {}
        self.tempo_cache = {}
        self.duracao_cache = 3600  # 1 hora
        
        self.moedas_suportadas = {}
        self.taxa_conversao = {}
        
        logger.info(f"Conversor inicializado com API: {api_tipo.value}")
    
    def obter_moedas_suportadas(self) -> Dict[str, str]:
        """Retorna dicionário de moedas suportadas"""
        if self.moedas_suportadas:
            return self.moedas_suportadas
        
        # Dicionário padrão de moedas (ISO 4217)
        self.moedas_suportadas = {
            "USD": "Dólar Americano",
            "EUR": "Euro",
            "GBP": "Libra Esterlina",
            "JPY": "Iene Japonês",
            "AUD": "Dólar Australiano",
            "CAD": "Dólar Canadense",
            "CHF": "Franco Suíço",
            "CNY": "Yuan Chinês",
            "INR": "Rúpia Indiana",
            "MXN": "Peso Mexicano",
            "BRL": "Real Brasileiro",
            "ZAR": "Rand Sul-Africano",
            "NZD": "Dólar Neozelandês",
            "SGD": "Dólar de Singapura",
            "HKD": "Dólar de Hong Kong",
            "NOK": "Coroa Norueguesa",
            "SEK": "Coroa Sueca",
            "DKK": "Coroa Dinamarquesa",
            "KRW": "Won Coreano",
            "TRY": "Lira Turca",
            "RUB": "Rublo Russo",
            "IDR": "Rúpia Indonesésia",
            "THB": "Baht Tailandês",
            "MYR": "Ringgit Malaio",
            "PHP": "Peso Filipino",
            "VND": "Dong Vietnamita",
            "PKR": "Rúpia Paquistanesa",
            "AED": "Dirham dos EAU",
            "SAR": "Riyal Saudita",
            "QAR": "Riyal Catariano",
            "KWD": "Dinar Kuwaitiano",
            "COP": "Peso Colombiano",
            "ARS": "Peso Argentino",
            "CLP": "Peso Chileno",
            "PEN": "Sol Peruano",
            "UYU": "Peso Uruguaio"
        }
        
        return self.moedas_suportadas
    
    def validar_cache(self, chave: str) -> bool:
        """Verifica se cache ainda é válido"""
        if chave not in self.tempo_cache:
            return False
        
        tempo_decorrido = time.time() - self.tempo_cache[chave]
        return tempo_decorrido < self.duracao_cache
    
    def obter_taxas(self, moeda_base: str, moedas_alvo: List[str] = None) -> Optional[Dict]:
        """
        Obtém taxas de câmbio da API
        
        Args:
            moeda_base: Moeda base (ex: USD)
            moedas_alvo: Lista de moedas alvo (opcional)
        
        Returns:
            Dicionário com taxas de câmbio
        """
        moeda_base = moeda_base.upper()
        
        # Verificar cache
        chave_cache = f"{moeda_base}_{','.join(moedas_alvo or [])}"
        if chave_cache in self.cache and self.validar_cache(chave_cache):
            logger.info(f"✓ Usando taxa em cache para {moeda_base}")
            return self.cache[chave_cache]
        
        try:
            if self.api_tipo == TipoAPI.EXCHANGE_RATE_API:
                taxas = self._obter_exchangerate_api(moeda_base)
            elif self.api_tipo == TipoAPI.FREE_CURRENCY_API:
                taxas = self._obter_freecurrency_api(moeda_base, moedas_alvo)
            elif self.api_tipo == TipoAPI.FIXER:
                taxas = self._obter_fixer_api(moeda_base, moedas_alvo)
            elif self.api_tipo == TipoAPI.OPEN_EXCHANGE:
                taxas = self._obter_openexchange_api(moeda_base, moedas_alvo)
            else:
                logger.error(f"API desconhecida: {self.api_tipo}")
                return None
            
            if taxas:
                # Armazenar em cache
                self.cache[chave_cache] = taxas
                self.tempo_cache[chave_cache] = time.time()
                logger.info(f"✓ Taxas obtidas para {moeda_base}")
                return taxas
            else:
                logger.warning(f"Falha ao obter taxas para {moeda_base}")
                return None
        
        except Exception as e:
            logger.error(f"Erro ao obter taxas: {str(e)}")
            return None
    
    def _obter_exchangerate_api(self, moeda_base: str) -> Optional[Dict]:
        """Obtém taxas da ExchangeRate API"""
        try:
            url = f"{self.APIS[TipoAPI.EXCHANGE_RATE_API]['url']}{moeda_base}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            dados = response.json()
            return {
                "base": dados.get("base"),
                "data": dados.get("time_last_updated"),
                "taxas": dados.get("rates", {})
            }
        
        except Exception as e:
            logger.error(f"Erro na ExchangeRate API: {str(e)}")
            return None
    
    def _obter_freecurrency_api(self, moeda_base: str, moedas_alvo: List[str] = None) -> Optional[Dict]:
        """Obtém taxas da Free Currency API"""
        try:
            url = self.APIS[TipoAPI.FREE_CURRENCY_API]['url']
            params = {"base_currency": moeda_base}
            
            if moedas_alvo:
                params["currencies"] = ",".join(moedas_alvo)
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            dados = response.json()
            return {
                "base": moeda_base,
                "data": dados.get("time_last_updated"),
                "taxas": dados.get("data", {})
            }
        
        except Exception as e:
            logger.error(f"Erro na Free Currency API: {str(e)}")
            return None
    
    def _obter_fixer_api(self, moeda_base: str, moedas_alvo: List[str] = None) -> Optional[Dict]:
        """Obtém taxas da Fixer API (requer chave)"""
        if not self.chave_api:
            logger.error("Fixer API requer chave API")
            return None
        
        try:
            url = self.APIS[TipoAPI.FIXER]['url']
            params = {
                "access_key": self.chave_api,
                "base": moeda_base
            }
            
            if moedas_alvo:
                params["symbols"] = ",".join(moedas_alvo)
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            dados = response.json()
            return {
                "base": dados.get("base"),
                "data": dados.get("date"),
                "taxas": dados.get("rates", {})
            }
        
        except Exception as e:
            logger.error(f"Erro na Fixer API: {str(e)}")
            return None
    
    def _obter_openexchange_api(self, moeda_base: str, moedas_alvo: List[str] = None) -> Optional[Dict]:
        """Obtém taxas da Open Exchange Rates API (requer chave)"""
        if not self.chave_api:
            logger.error("Open Exchange Rates API requer chave API")
            return None
        
        try:
            url = self.APIS[TipoAPI.OPEN_EXCHANGE]['url']
            params = {"app_id": self.chave_api}
            
            if moeda_base != "USD":
                params["base"] = moeda_base
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            dados = response.json()
            return {
                "base": dados.get("base"),
                "data": datetime.fromtimestamp(dados.get("timestamp")).isoformat(),
                "taxas": dados.get("rates", {})
            }
        
        except Exception as e:
            logger.error(f"Erro na Open Exchange Rates API: {str(e)}")
            return None
    
    def converter(self, valor: float, moeda_origem: str, moeda_destino: str) -> Optional[float]:
        """
        Converte valor entre moedas
        
        Args:
            valor: Valor a converter
            moeda_origem: Moeda de origem (ex: USD)
            moeda_destino: Moeda de destino (ex: EUR)
        
        Returns:
            Valor convertido ou None se erro
        """
        moeda_origem = moeda_origem.upper()
        moeda_destino = moeda_destino.upper()
        
        if valor <= 0:
            logger.warning("Valor deve ser maior que zero")
            return None
        
        # Se são a mesma moeda
        if moeda_origem == moeda_destino:
            return valor
        
        # Obter taxas
        taxas = self.obter_taxas(moeda_origem, [moeda_destino])
        
        if not taxas or "taxas" not in taxas:
            logger.error(f"Não foi possível obter taxas para {moeda_origem}")
            return None
        
        try:
            # Buscar taxa de câmbio
            taxa = taxas["taxas"].get(moeda_destino)
            
            if taxa is None:
                logger.error(f"Moeda {moeda_destino} não encontrada")
                return None
            
            valor_convertido = valor * taxa
            logger.info(f"✓ Convertido: {valor} {moeda_origem} = {valor_convertido:.2f} {moeda_destino}")
            
            return round(valor_convertido, 2)
        
        except Exception as e:
            logger.error(f"Erro na conversão: {str(e)}")
            return None
    
    def converter_multiplo(self, valor: float, moeda_origem: str, moedas_destino: List[str]) -> Dict[str, float]:
        """
        Converte para múltiplas moedas de uma vez
        
        Args:
            valor: Valor a converter
            moeda_origem: Moeda de origem
            moedas_destino: Lista de moedas de destino
        
        Returns:
            Dicionário com conversões
        """
        moeda_origem = moeda_origem.upper()
        moedas_destino = [m.upper() for m in moedas_destino]
        
        resultado = {}
        
        taxas = self.obter_taxas(moeda_origem, moedas_destino)
        
        if not taxas or "taxas" not in taxas:
            logger.error(f"Não foi possível obter taxas")
            return resultado
        
        for moeda_destino in moedas_destino:
            taxa = taxas["taxas"].get(moeda_destino)
            
            if taxa:
                resultado[moeda_destino] = round(valor * taxa, 2)
        
        return resultado
    
    def obter_historico(self, moeda: str, dias: int = 7) -> Optional[List[Dict]]:
        """
        Simula histórico de taxas (com base em cache)
        
        Args:
            moeda: Moeda para obter histórico
            dias: Número de dias
        
        Returns:
            Lista com histórico simulado
        """
        logger.info(f"Obtendo histórico para {moeda}")
        
        historico = []
        moeda = moeda.upper()
        
        for i in range(dias):
            data = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            taxas = self.obter_taxas(moeda)
            
            if taxas:
                historico.append({
                    "data": data,
                    "taxas": taxas["taxas"]
                })
            
            time.sleep(0.5)  # Evitar rate limit
        
        return historico[::-1]  # Reverter para ordem cronológica
    
    def comparar_taxas(self, moeda_origem: str, moedas_destino: List[str]) -> Dict:
        """
        Compara taxas de câmbio para múltiplas moedas
        
        Args:
            moeda_origem: Moeda base
            moedas_destino: Lista de moedas para comparar
        
        Returns:
            Dicionário com comparação
        """
        moeda_origem = moeda_origem.upper()
        moedas_destino = [m.upper() for m in moedas_destino]
        
        taxas = self.obter_taxas(moeda_origem, moedas_destino)
        
        if not taxas or "taxas" not in taxas:
            return {}
        
        resultado = {
            "base": moeda_origem,
            "data": taxas.get("data"),
            "comparacao": []
        }
        
        for moeda_destino in moedas_destino:
            taxa = taxas["taxas"].get(moeda_destino)
            
            if taxa:
                nome_moeda = self.moedas_suportadas.get(moeda_destino, moeda_destino)
                resultado["comparacao"].append({
                    "moeda": moeda_destino,
                    "nome": nome_moeda,
                    "taxa": taxa,
                    "1_base_para": f"1 {moeda_origem} = {taxa:.4f} {moeda_destino}"
                })
        
        # Ordenar por taxa (descendente)
        resultado["comparacao"].sort(key=lambda x: x["taxa"], reverse=True)
        
        return resultado
    
    def exibir_relatorio(self, valor: float, moeda_origem: str, moedas_destino: List[str]):
        """Exibe relatório formatado de conversão"""
        moeda_origem = moeda_origem.upper()
        moedas_destino = [m.upper() for m in moedas_destino]
        
        conversoes = self.converter_multiplo(valor, moeda_origem, moedas_destino)
        
        print("\n" + "="*60)
        print("CONVERSOR DE MOEDAS")
        print("="*60)
        print(f"\nValor Original: {valor:.2f} {moeda_origem}\n")
        print("-"*60)
        
        for moeda_destino, valor_convertido in conversoes.items():
            nome_moeda = self.moedas_suportadas.get(moeda_destino, moeda_destino)
            print(f"{moeda_destino} ({nome_moeda:30s}): {valor_convertido:>15.2f}")
        
        print("-"*60)
        print(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*60 + "\n")


class ConversorAvancado(CurrencyConverter):
    """Versão avançada com análises adicionais"""
    
    def obter_taxa_mais_vantajosa(self, valor: float, moedas: List[str]) -> Tuple[str, float]:
        """
        Encontra a moeda com melhor taxa de câmbio
        
        Args:
            valor: Valor a converter
            moedas: Lista de moedas
        
        Returns:
            Tupla (moeda, valor_convertido)
        """
        conversoes = self.converter_multiplo(valor, moedas[0], moedas[1:])
        
        moeda_melhor = max(conversoes, key=conversoes.get)
        valor_melhor = conversoes[moeda_melhor]
        
        logger.info(f"Melhor taxa: {moeda_melhor} com {valor_melhor:.2f}")
        return moeda_melhor, valor_melhor
    
    def simular_rentabilidade(self, valor_inicial: float, moeda: str, percentual: float) -> float:
        """
        Simula rentabilidade com variação de taxa
        
        Args:
            valor_inicial: Valor inicial
            moeda: Moeda
            percentual: Percentual de variação
        
        Returns:
            Valor com variação
        """
        variacao = valor_inicial * (percentual / 100)
        valor_final = valor_inicial + variacao
        
        logger.info(f"Simulação: {valor_inicial:.2f} + {percentual}% = {valor_final:.2f} {moeda}")
        return round(valor_final, 2)
    
    def calcular_margem(self, taxa_compra: float, taxa_venda: float) -> float:
        """
        Calcula margem entre compra e venda
        
        Args:
            taxa_compra: Taxa de compra
            taxa_venda: Taxa de venda
        
        Returns:
            Percentual de margem
        """
        margem = ((taxa_venda - taxa_compra) / taxa_compra) * 100
        logger.info(f"Margem calculada: {margem:.2f}%")
        return round(margem, 2)


if __name__ == "__main__":
    # Exemplo de uso
    print("="*60)
    print("CONVERSOR DE MOEDAS")
    print("="*60 + "\n")
    
    # Criar conversor
    conversor = CurrencyConverter(api_tipo=TipoAPI.EXCHANGE_RATE_API)
    
    # Menu interativo
    while True:
        print("\n" + "="*60)
        print("MENU PRINCIPAL")
        print("="*60)
        print("1. Converter moeda única")
        print("2. Converter para múltiplas moedas")
        print("3. Comparar taxas")
        print("4. Listar moedas suportadas")
        print("5. Sair")
        print("="*60)
        
        opcao = input("\nEscolha uma opção (1-5): ").strip()
        
        if opcao == "1":
            try:
                valor = float(input("\nDigite o valor: "))
                moeda_origem = input("Moeda de origem (ex: USD): ").strip().upper()
                moeda_destino = input("Moeda de destino (ex: EUR): ").strip().upper()
                
                resultado = conversor.converter(valor, moeda_origem, moeda_destino)
                
                if resultado:
                    print(f"\n✓ {valor:.2f} {moeda_origem} = {resultado:.2f} {moeda_destino}")
                else:
                    print("\n✗ Erro na conversão")
            except ValueError:
                print("\n✗ Valor inválido")
        
        elif opcao == "2":
            try:
                valor = float(input("\nDigite o valor: "))
                moeda_origem = input("Moeda de origem (ex: USD): ").strip().upper()
                moedas_destino = input("Moedas de destino separadas por vírgula (ex: EUR,GBP,JPY): ").split(",")
                moedas_destino = [m.strip().upper() for m in moedas_destino]
                
                conversor.exibir_relatorio(valor, moeda_origem, moedas_destino)
            except ValueError:
                print("\n✗ Valor inválido")
        
        elif opcao == "3":
            moeda_origem = input("\nMoeda de origem (ex: USD): ").strip().upper()
            moedas_destino = input("Moedas para comparar separadas por vírgula (ex: EUR,GBP,JPY): ").split(",")
            moedas_destino = [m.strip().upper() for m in moedas_destino]
            
            comparacao = conversor.comparar_taxas(moeda_origem, moedas_destino)
            
            if comparacao.get("comparacao"):
                print(f"\n{'='*60}")
                print(f"Comparação de Taxas - Base: {moeda_origem}")
                print(f"{'='*60}")
                
                for item in comparacao["comparacao"]:
                    print(f"{item['moeda']} ({item['nome']:30s}): {item['taxa']:.4f}")
                
                print(f"{'='*60}\n")
            else:
                print("\n✗ Erro ao comparar taxas")
        
        elif opcao == "4":
            moedas = conversor.obter_moedas_suportadas()
            
            print(f"\n{'='*60}")
            print(f"Moedas Suportadas ({len(moedas)})")
            print(f"{'='*60}")
            
            for codigo, nome in sorted(moedas.items()):
                print(f"{codigo}: {nome}")
            
            print(f"{'='*60}\n")
        
        elif opcao == "5":
            print("\nSaindo...")
            break
        
        else:
            print("\n✗ Opção inválida")
