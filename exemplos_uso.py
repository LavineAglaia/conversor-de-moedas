"""
Exemplos de uso do Conversor de Moedas
"""

from currency_converter import CurrencyConverter, ConversorAvancado, TipoAPI
import json

def exemplo_1_conversao_simples():
    """Exemplo 1: Conversão simples"""
    print("\n" + "="*60)
    print("EXEMPLO 1: Conversão Simples")
    print("="*60 + "\n")
    
    conversor = CurrencyConverter()
    
    # Converter 100 USD para EUR
    resultado = conversor.converter(100, "USD", "EUR")
    print(f"100 USD = {resultado} EUR")

def exemplo_2_multiplas_moedas():
    """Exemplo 2: Converter para múltiplas moedas"""
    print("\n" + "="*60)
    print("EXEMPLO 2: Múltiplas Moedas")
    print("="*60 + "\n")
    
    conversor = CurrencyConverter()
    
    # Converter 100 BRL para várias moedas
    conversoes = conversor.converter_multiplo(
        100,
        "BRL",
        ["USD", "EUR", "GBP", "JPY"]
    )
    
    for moeda, valor in conversoes.items():
        print(f"100 BRL = {valor} {moeda}")

def exemplo_3_comparacao_taxas():
    """Exemplo 3: Comparar taxas"""
    print("\n" + "="*60)
    print("EXEMPLO 3: Comparação de Taxas")
    print("="*60 + "\n")
    
    conversor = CurrencyConverter()
    
    # Comparar taxas de USD para várias moedas
    comparacao = conversor.comparar_taxas(
        "USD",
        ["EUR", "GBP", "JPY", "BRL"]
    )
    
    print(f"Base: {comparacao['base']}\n")
    
    for item in comparacao.get("comparacao", []):
        print(f"{item['moeda']}: {item['taxa']:.4f} ({item['1_base_para']})")

def exemplo_4_moedas_suportadas():
    """Exemplo 4: Listar moedas suportadas"""
    print("\n" + "="*60)
    print("EXEMPLO 4: Moedas Suportadas")
    print("="*60 + "\n")
    
    conversor = CurrencyConverter()
    moedas = conversor.obter_moedas_suportadas()
    
    print(f"Total: {len(moedas)} moedas\n")
    
    for i, (codigo, nome) in enumerate(sorted(moedas.items())[:10], 1):
        print(f"{i}. {codigo}: {nome}")
    
    print("...")

def exemplo_5_analise_avancada():
    """Exemplo 5: Análise avançada"""
    print("\n" + "="*60)
    print("EXEMPLO 5: Análise Avançada")
    print("="*60 + "\n")
    
    conversor = ConversorAvancado()
    
    # Simular rentabilidade
    valor_inicial = 1000
    rentabilidade = conversor.simular_rentabilidade(valor_inicial, "USD", 5)
    print(f"Valor inicial: {valor_inicial} USD")
    print(f"Com 5% de rentabilidade: {rentabilidade} USD\n")
    
    # Calcular margem
    taxa_compra = 4.95
    taxa_venda = 5.05
    margem = conversor.calcular_margem(taxa_compra, taxa_venda)
    print(f"Taxa de compra: {taxa_compra}")
    print(f"Taxa de venda: {taxa_venda}")
    print(f"Margem: {margem}%")

def exemplo_6_salvar_resultados():
    """Exemplo 6: Salvar resultados em JSON"""
    print("\n" + "="*60)
    print("EXEMPLO 6: Salvar Resultados")
    print("="*60 + "\n")
    
    conversor = CurrencyConverter()
    
    conversoes = conversor.converter_multiplo(
        1,
        "BRL",
        ["USD", "EUR", "GBP"]
    )
    
    resultado = {
        "valor_original": 1,
        "moeda_origem": "BRL",
        "conversoes": conversoes,
        "timestamp": str(__import__("datetime").datetime.now())
    }
    
    # Salvar em arquivo
    with open("resultado_conversao.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    
    print("✓ Resultado salvo em resultado_conversao.json")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    exemplo_1_conversao_simples()
    exemplo_2_multiplas_moedas()
    exemplo_3_comparacao_taxas()
    exemplo_4_moedas_suportadas()
    exemplo_5_analise_avancada()
    exemplo_6_salvar_resultados()
