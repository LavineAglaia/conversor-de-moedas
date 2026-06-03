# Conversor de Moedas - Python

Um conversor de moedas completo que consome APIs públicas de câmbio em tempo real.

## 🚀 Instalação

### Pré-requisitos
- Python 3.7+
- pip

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/LavineAglaia/conversor-de-moedas.git
cd conversor-de-moedas
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o arquivo .env (opcional):
```bash
cp .env.example .env
```

## 🎪 APIs Suportadas

### 1. ExchangeRate API (Gratuita)
- **URL**: https://api.exchangerate-api.com
- **Limite**: 1.500 requisições/mês
- **Autenticação**: Não requer

```python
conversor = CurrencyConverter(api_tipo=TipoAPI.EXCHANGE_RATE_API)
```

### 2. Free Currency API (Gratuita)
- **URL**: https://api.freecurrencyapi.com
- **Limite**: 300 requisições/mês
- **Autenticação**: Não requer

```python
conversor = CurrencyConverter(api_tipo=TipoAPI.FREE_CURRENCY_API)
```

### 3. Fixer (Paga)
- **URL**: https://fixer.io
- **Autenticação**: Requer chave API

```python
conversor = CurrencyConverter(
    api_tipo=TipoAPI.FIXER,
    chave_api="sua_chave"
)
```

### 4. Open Exchange Rates (Paga)
- **URL**: https://openexchangerates.org
- **Autenticação**: Requer chave API

```python
conversor = CurrencyConverter(
    api_tipo=TipoAPI.OPEN_EXCHANGE,
    chave_api="sua_chave"
)
```

## 📖 Uso

### Conversão Simples

```python
from currency_converter import CurrencyConverter

conversor = CurrencyConverter()

# Converter 100 USD para EUR
resultado = conversor.converter(100, "USD", "EUR")
print(f"100 USD = {resultado} EUR")
```

### Conversão Múltipla

```python
# Converter para várias moedas
conversoes = conversor.converter_multiplo(
    100,
    "BRL",
    ["USD", "EUR", "GBP", "JPY"]
)

for moeda, valor in conversoes.items():
    print(f"100 BRL = {valor} {moeda}")
```

### Comparar Taxas

```python
# Comparar taxas de câmbio
comparacao = conversor.comparar_taxas(
    "USD",
    ["EUR", "GBP", "JPY"]
)

for item in comparacao["comparacao"]:
    print(f"{item['moeda']}: {item['taxa']:.4f}")
```

### Moedas Suportadas

```python
# Listar moedas
moedas = conversor.obter_moedas_suportadas()

for codigo, nome in moedas.items():
    print(f"{codigo}: {nome}")
```

### Análise Avançada

```python
from currency_converter import ConversorAvancado

conversor = ConversorAvancado()

# Simular rentabilidade
valor = conversor.simular_rentabilidade(1000, "USD", 5)
print(f"Com 5% de rentabilidade: {valor} USD")

# Calcular margem
margem = conversor.calcular_margem(4.95, 5.05)
print(f"Margem: {margem}%")
```

## 💾 Cache

O conversor usa cache automático de 1 hora para reduzir requisições:

```python
conversor = CurrencyConverter()

# Primeira requisição (consulta API)
resultado1 = conversor.converter(100, "USD", "EUR")

# Segunda requisição (usa cache)
resultado2 = conversor.converter(100, "USD", "EUR")
```

## 📋 Exemplos

### Exemplo 1: Menu Interativo

```bash
python currency_converter.py
```

### Exemplo 2: Scripts de Exemplo

```bash
python exemplos_uso.py
```

### Exemplo 3: Usar em seu projeto

```python
from currency_converter import CurrencyConverter

def meu_conversor():
    conversor = CurrencyConverter()
    valor = conversor.converter(100, "USD", "EUR")
    return valor

print(meu_conversor())
```

## 📋 Funcionalidades

✅ Conversão de múltiplas moedas
✅ Cache automático
✅ Suporte a 4 APIs diferentes
✅ Comparação de taxas
✅ Análise avançada
✅ Logging detalhado
✅ Menu interativo
✅ Relatórios formatados
✅ Exportação JSON
✅ Tratamento de erros

## 📝 Logs

Os logs são salvos em `currency_converter.log`:

```
2024-01-15 10:30:45,123 - INFO - Conversor inicializado com API: exchangerate
2024-01-15 10:30:47,456 - INFO - ✓ Conectado com sucesso!
```

## ⚙️ Configuração

### Variáveis de Ambiente

```bash
# .env
FIXER_API_KEY=sua_chave
OPEN_EXCHANGE_API_KEY=sua_chave
DEBUG=False
TIMEOUT=10
```

## 🔐 Segurança

- ✅ Chaves armazenadas em .env
- ✅ Não expõe chaves no código
- ✅ Timeout para requisições
- ✅ Tratamento de erros

## 📊 Moedas Suportadas

Mais de 150 moedas incluindo:

- **Principais**: USD, EUR, GBP, JPY
- **América Latina**: BRL, MXN, ARS, CLP
- **Ásia**: CNY, INR, IDR, THB, PHP
- **Oriente Médio**: AED, SAR, QAR, KWD
- E muitas mais...

## 🐛 Troubleshooting

### Erro de Conexão
```
✗ Erro ao obter taxas: Connection error
```
Solução: Verifique sua conexão com a internet

### Limite de Requisições
```
✗ API rate limit exceeded
```
Solução: Aguarde ou use API paga

### Moeda Não Encontrada
```
✗ Moeda desconhecida
```
Solução: Verifique o código ISO-4217

## 📄 Licença

MIT

## 👨‍💻 Autor

LavineAglaia
