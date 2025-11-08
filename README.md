# Buscador de Vagas LinkedIn

Um projeto básico de web scraping para buscar vagas de emprego no LinkedIn, focado na região de Recife, Pernambuco, Brasil.

## 📋 Descrição

Este projeto implementa um web scraper que busca vagas de emprego na versão pública do LinkedIn (sem necessidade de login). O scraper coleta informações como título da vaga, empresa, localização e link para a vaga.

## 🚀 Funcionalidades

- Busca vagas no LinkedIn sem necessidade de autenticação
- Filtra por palavras-chave e localização
- Extrai informações das vagas:
  - Título da vaga
  - Nome da empresa
  - Localização
  - Link para a vaga
  - Data de postagem (quando disponível)
- Exibe resultados no console de forma formatada
- Exporta resultados para arquivo CSV

## 📦 Requisitos

- Python 3.7 ou superior
- Dependências listadas em `requirements.txt`:
  - requests
  - beautifulsoup4
  - lxml

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/marco-arruda/buscador-de-vagas-linkd.git
cd buscador-de-vagas-linkd
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 💻 Como Usar

### Uso Básico

Execute o script principal para buscar todas as vagas em Recife:

```bash
python buscador_vagas.py
```

### Personalização

Você pode personalizar a busca editando o arquivo `buscador_vagas.py` na função `main()`:

```python
# Buscar vagas com palavras-chave específicas
vagas = scraper.buscar_vagas(
    keywords="Python Desenvolvedor",  # Palavras-chave
    location="Recife, Pernambuco, Brasil",  # Localização
    num_paginas=2  # Número de páginas para buscar
)
```

### Uso Programático

Você também pode usar a classe `LinkedInJobScraper` em seus próprios scripts:

```python
from buscador_vagas import LinkedInJobScraper

# Criar instância do scraper
scraper = LinkedInJobScraper()

# Buscar vagas
vagas = scraper.buscar_vagas(
    keywords="desenvolvedor",
    location="Recife, Pernambuco, Brasil",
    num_paginas=1
)

# Exibir vagas
scraper.exibir_vagas(vagas)

# Salvar em CSV
scraper.salvar_csv(vagas, "minhas_vagas.csv")
```

## 📊 Formato de Saída

### Console
As vagas são exibidas no console com o seguinte formato:
```
1. Título da Vaga
   Empresa: Nome da Empresa
   Localização: Cidade, Estado
   Data: Data de postagem
   Link: URL da vaga
```

### CSV
Um arquivo CSV é gerado automaticamente com as colunas:
- titulo
- empresa
- localizacao
- link
- data_postagem

Nome do arquivo: `vagas_linkedin_YYYYMMDD_HHMMSS.csv`

## ⚠️ Observações Importantes

1. **Respeite os Termos de Uso**: Este scraper foi desenvolvido para uso educacional. Sempre respeite os termos de serviço do LinkedIn.

2. **Rate Limiting**: O script inclui pausas entre requisições para não sobrecarregar o servidor.

3. **Mudanças no HTML**: O LinkedIn pode alterar a estrutura HTML de suas páginas. Se o scraper parar de funcionar, pode ser necessário atualizar os seletores CSS.

4. **Limitações**: 
   - Funciona apenas com a versão pública do LinkedIn (não requer login)
   - Limitado às informações visíveis na página de busca
   - Pode não capturar todas as vagas disponíveis

## 🛠️ Estrutura do Projeto

```
buscador-de-vagas-linkd/
│
├── buscador_vagas.py      # Script principal
├── requirements.txt       # Dependências do projeto
├── .gitignore            # Arquivos a serem ignorados pelo Git
└── README.md             # Documentação
```

## 📝 Exemplo de Uso

```bash
$ python buscador_vagas.py

============================================================
BUSCADOR DE VAGAS LINKEDIN
============================================================

1. Buscando todas as vagas em Recife...
Buscando vagas para: todas as categorias
Localização: Recife, Pernambuco, Brasil
------------------------------------------------------------

Buscando página 1...
Encontradas 25 vagas na página 1

============================================================
VAGAS ENCONTRADAS: 25
============================================================

1. Desenvolvedor Python
   Empresa: Empresa XYZ
   Localização: Recife, PE
   Data: 2025-01-05
   Link: https://www.linkedin.com/jobs/view/...
------------------------------------------------------------
...

✓ 25 vagas salvas em: vagas_linkedin_20250107_151230.csv
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional.

## 👤 Autor

Marco Arruda

## 🔗 Links Úteis

- [LinkedIn Jobs](https://www.linkedin.com/jobs/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://requests.readthedocs.io/)

## 🚀 API

Este repositório inclui uma API simples usando FastAPI em `api/search.py`.

Endpoint principal (local):

- POST /  (quando o servidor estiver rodando em http://localhost:8000/)

Payload (JSON):

```json
{
   "query": "Desenvolvedor Python",
   "location": "Recife, Pernambuco, Brasil",
   "num_pages": 1
}
```

Resposta: lista de objetos com os campos `titulo`, `empresa`, `localizacao`, `link`, `data_postagem`.

Teste local com uvicorn:

```bash
pip install -r requirements.txt
uvicorn api.search:app --reload --port 8000
```

Em seguida, faça uma requisição POST para `http://localhost:8000/` com o JSON do payload acima.

Cache
-----

Esta API possui um cache em memória (LRU) com TTL para evitar chamadas repetidas ao LinkedIn
durante curtos intervalos. Configurações padrão (em `api/search.py`):

- TTL: 300 segundos (5 minutos)
- Máximo de entradas: 128 (eviction LRU automática)

O endpoint adiciona um header `X-Cache` na resposta com valor `HIT` quando o resultado veio do cache,
ou `MISS` quando foi buscado novamente.
