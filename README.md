# League of Legends: Challenger Meta Analytics

## Sobre o Projeto
Este é um projeto end-to-end de engenharia e análise de dados focado em League of Legends. O objetivo principal é extrair dados reais de partidas de jogadores do tier Challenger (fila Solo/Duo) para analisar o comportamento do meta atual do jogo. 

Através de um pipeline ETL construído em Python, o projeto consome a API oficial da Riot Games, transforma os dados brutos e os carrega em um banco de dados relacional. Por fim, um dashboard interativo consome essas informações para gerar insights táticos, como taxas de vitória, impacto de rotas (KDA, dano, ouro) e performance de campeões.

O projeto conta também com uma infraestrutura conteinerizada, permitindo que a aplicação e o banco de dados sejam executados em qualquer ambiente de forma isolada e com poucos comandos.

## Stack Tecnológica
* **Extração e transformação:** Python, requests, pandas, python-dotenv
* **Armazenamento e banco de dados:** MySQL, sqlalchemy, pymysql
* **Visualização de dados (dashboard):** Streamlit, Plotly
* **Infraestrutura e Deploy:** Docker, Docker Compose

## Arquitetura do Projeto
O projeto foi modularizado para separar as responsabilidades do pipeline ETL, da camada analítica e da infraestrutura:

* `config.py`: Centraliza a leitura de variáveis de ambiente e credenciais.
* `etl/`: Módulo contendo os scripts de extração (Riot API), transformação (limpeza com Pandas) e carga (inserção no MySQL).
* `sql/`: Scripts de criação das tabelas e as views analíticas consumidas pelo dashboard.
* `main.py`: O orquestrador que executa o pipeline ETL de ponta a ponta.
* `dashboard.py`: A aplicação Streamlit que renderiza os gráficos e métricas.
* `.env`: Arquivo contendo as variáveis de ambiente sensíveis (deve ser criado manualmente a partir do `.env.example`).
* `Dockerfile` e `docker-compose.yml`: Arquivos responsáveis por criar e orquestrar os containers da aplicação e do banco de dados.

## Como rodar o projeto na sua máquina

### Pré-requisitos
* Chave de desenvolvedor da API da Riot Games (pode ser gerada gratuitamente no Riot Developer Portal). A chave expira a cada 24 horas.
* Para rodar via Docker: Docker e Docker Desktop instalados.
* Para rodar localmente: Python 3.8+ e Servidor MySQL rodando localmente.

### Passo a Passo

Primeiramente, faça o clone do repositório e configure as variáveis de ambiente:

1. Clone o repositório:
    ```bash
    git clone [https://github.com/SEU_USUARIO/projeto-lol-analytics.git](https://github.com/SEU_USUARIO/projeto-lol-analytics.git)
    cd projeto-lol-analytics
    ```

2. Configuração das Variáveis de Ambiente:
    * Renomeie o arquivo `.env.example` para `.env`.
    * Preencha o arquivo com a sua Riot API Key. As credenciais do banco de dados já estarão preenchidas no padrão local (`127.0.0.1`), o que é compatível com ambas as opções de execução abaixo.

---

#### Opção 1: Rodando com Docker (Recomendado)

A infraestrutura orquestrará a aplicação Python e o banco de dados MySQL simultaneamente, executando os scripts SQL automaticamente na primeira inicialização.

1. Suba os containers da aplicação e do banco de dados:
    ```bash
    docker-compose up -d --build
    ```

2. Execute o Pipeline ETL para popular o banco de dados:
    * Como a aplicação roda isoladamente, utilize o comando abaixo para acionar o orquestrador dentro do container:
    ```bash
    docker exec -it lol_app python main.py
    ```

3. Abra o Dashboard:
    * Acesse a aplicação no seu navegador através do endereço `http://localhost:8501`.
    * Na primeira vez, limpe o cache do Streamlit (clicando no ícone de menu no canto superior direito e selecionando "Clear cache", ou apertando a tecla "C") para forçar a leitura dos novos dados recém-inseridos.

---

#### Opção 2: Rodando Localmente (Sem Docker)

1. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

2. Configuração do Banco de Dados:
    * Crie um banco de dados no seu MySQL chamado `riot_data`.
    * Execute os scripts localizados na pasta `sql/` para criar a tabela `estatisticas_partidas` e as views necessárias para o dashboard.

3. Execute o Pipeline ETL:
    * Rode o orquestrador para extrair e carregar os dados:
    ```bash
    python main.py
    ```

4. Abra o Dashboard:
    * Inicie a aplicação do Streamlit:
    ```bash
    streamlit run dashboard.py
    ```

## Licença
Distribuído sob a licença MIT. Sinta-se à vontade para utilizar, modificar e contribuir.
