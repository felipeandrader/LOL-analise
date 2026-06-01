# League of Legends: Challenger Meta Analytics

## Sobre o Projeto
Este é um projeto end-to-end de engenharia e análise de dados focado em League of Legends. O objetivo principal é extrair dados reais de partidas de jogadores do tier Challenger (fila Solo/Duo) para analisar o comportamento do meta atual do jogo. 

Através de um pipeline ETL construído em Python, o projeto consome a API oficial da Riot Games, transforma os dados brutos e os carrega em um banco de dados relacional. Por fim, um dashboard interativo consome essas informações para gerar insights táticos, como taxas de vitória, impacto de rotas (KDA, dano, ouro) e performance de campeões.

## Stack Tecnológica
* **Extração e transformação (Python):** requests, pandas, python-dotenv
* **Armazenamento e banco de dados:** MySQL, sqlalchemy, pymysql
* **Visualização de dados (dashboard):** Streamlit, Plotly

## Arquitetura do Projeto
O projeto foi modularizado para separar as responsabilidades do pipeline ETL e da camada analítica:

* config.py: Centraliza a leitura de variáveis de ambiente e credenciais.
* etl/: Módulo contendo os scripts de extração (Riot API), transformação (limpeza com Pandas) e carga (inserção no MySQL).
* sql/: Scripts de criação das tabelas e as views analíticas consumidas pelo dashboard.
* main.py: O orquestrador que executa o pipeline ETL de ponta a ponta.
* dashboard.py: A aplicação Streamlit que renderiza os gráficos e métricas.
* .env: contendo as variaveis de ambiente (deve ser criado manualmente)

## Como rodar o projeto na sua máquina

### Pré-requisitos
* Python 3.8+ instalado.
* Servidor MySQL rodando localmente.
* Uma chave de desenvolvedor da API da Riot Games (pode ser gerada gratuitamente no Riot Developer Portal). A chave de desenvolvimento da riot se expira a cada 24 horas.

### Passo a Passo

1. Clone o repositório:
    ```bash
    git clone [https://github.com/SEU_USUARIO/projeto-lol-analytics.git](https://github.com/SEU_USUARIO/projeto-lol-analytics.git)
    cd projeto-lol-analytics
    ```

2. Instale as dependências:
    ```bash
    pip install pandas requests python-dotenv sqlalchemy pymysql streamlit plotly
    ```

3. Configuração do Banco de Dados:
    * Crie um banco de dados no seu MySQL chamado riot_data.
    * Execute os scripts localizados na pasta sql/ para criar a tabela estatisticas_partidas e as views necessárias para o dashboard.

4. Configuração das Variáveis de Ambiente:
    * Renomeie o arquivo .env.example para .env.
    * Preencha o arquivo com as suas credenciais do MySQL e a sua Riot API Key.

5. Execute o Pipeline ETL:
    * Para popular o banco de dados com as partidas mais recentes, rode o orquestrador:
    ```bash
    python main.py
    ```

6. Abra o Dashboard:
    * Com o banco populado, inicie a aplicação do Streamlit:
    ```bash
    streamlit run dashboard.py
    ```

## Licença
Distribuído sob a licença MIT. Sinta-se à vontade para utilizar, modificar e contribuir.
