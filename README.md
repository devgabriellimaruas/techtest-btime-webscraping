# Teste Btime - Dev RPA

## Visão Geral
Este projeto consiste em dois scripts em Python para automação de coleta de dados relacionados ao tema Séries:

- **Coleta via API** (`src/api_scraper.py`) — consome uma API pública, normaliza os dados e grava em CSV.

- **Coleta via Web Scraping** (`src/web_scraper.py`) — utiliza Selenium para extrair dados de páginas web, incluindo estratégias para lidar com bloqueios e restrições comuns.

Ambos os scripts geram arquivos CSV bem estruturados na pasta output/ e seguem boas práticas de arquitetura, como separação de responsabilidades e modularidade.

## Estrutura do Repositório
- `main.py` — Orquestra a execução dos scrapers
- `src/api_scraper.py` — Script de coleta via API
- `src/web_scraper.py` — Script de web scraping com Selenium
- `src/config.py` — Configurações e constantes
- `src/utils.py` — Funções utilitárias (CSV, XLSX, formatação)
- `log/logger.py` — Configuração do logger
- `output/` — Resultados em CSV/XLSX e logs
- `requirements.txt` — Dependências do projeto

## Requisitos
- Python 3.8+ (3.13.9)
- Instalar dependências principais: `pandas`, `requests`, `openpyxl`, `selenium`, `webdriver-manager`.

```bash
pip install -r requirements.txt
```

## Como Executar
1. Para executar ambos os scrapers sequencialmente (gerará os CSVs em `output/`):

```bash
python main.py
```

2. Executar individualmente:

- API:

```bash
python -m src.api_scraper
```

- Web Scraper:

```bash
python -m src.web_scraper
```

## Configuração

- Ajuste `TOP_N` em `src/config.py` para controlar o número de itens coletados.
- `src/config.py` também define diretório de saída e URLs/endereços usados.
- Para rodar o web scraper em modo headless, habilite a opção `headless` no `setup_driver()` em `src/web_scraper.py`.

## Saída (CSV)

- Os dois scrapers produzem arquivos CSV com esquema consistente para facilitar comparação e análises posteriores.
- Colunas típicas:

| Coluna  | Descrição                     |
|---------|-------------------------------|
| title   | Título do item (ex.: série)   |
| year    | Ano de lançamento             |
| rating  | Avaliação ou nota             |
| genre   | Gênero ou categoria           |
| url     | Link da página ou referência  |

## Logs e Tratamento de Erros

- Logs são configurados em `log/logger.py` e são exibidos no console; mensagens informam início/fim das execuções e erros.
- Cada scraper possui tratamento básico de exceções para melhorar robustez frente a falhas de rede, respostas inesperadas ou mudanças no DOM.

## Desenvolvedor
| Nome         | Email                     |
|--------------|---------------------------|
| Gabriel Lima | limaruasgabriel@gmail.com |