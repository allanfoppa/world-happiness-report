# World Happines Report Regression Model

- [World Happines Report Regression Model](#world-happines-report-regression-model)
  * [Badges](#badges)
  * [Descrição do projeto](#descri--o-do-projeto)
  * [Arquitetura](#arquitetura)
    + [Dependências](#depend-ncias)
  * [Rodando ou acessando o projeto](#rodando-ou-acessando-o-projeto)
    + [Publicação Azure](#publica--o-azure)
    + [Rodando API localmente](#rodando-api-localmente)
    + [Gerando imagem do Docker](#gerando-imagem-do-docker)
    + [Executando via console](#executando-via-console)
    + [Gerando exemplos de retorno](#gerando-exemplos-de-retorno)
  * [Variáveis de ambiente](#vari-veis-de-ambiente)
  * [Modelos utilizados](#modelos-utilizados)
  * [Endpoints](#endpoints)
    + [`/data-ingestion`](#--data-ingestion-)
        * [`POST /ingest`](#-post--ingest-)
        * [`GET /ingested/processed-data`](#-get--ingested-processed-data-)
        * [`GET /ingested/pandemic-data`](#-get--ingested-pandemic-data-)
    + [`/region-classification/{knn|random-forest}`](#--region-classification--knn-random-forest--)
        * [`GET /evaluate`](#-get--evaluate-)
        * [`GET /balanced/evaluate`](#-get--balanced-evaluate-)
        * [`PUT /predict`](#-put--predict-)
    + [`/score-regression/{knn|random-forest}`](#--score-regression--knn-random-forest--)
        * [`GET /evaluate`](#-get--evaluate--1)
        * [`PUT /predict`](#-put--predict--1)
  * [Melhorias futuras](#melhorias-futuras)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>TOC gerado com markdown-toc</a></i></small>
## Badges

![Badge em Desenvolvimento](https://img.shields.io/static/v1?label=STATUS&message=ENTREGUE&color=GREEN&style=for-the-badge)

## Descrição do projeto

Este projeto contém modelos de regressão para prever o nível de felicidade de um país no mundo utilizando os dados do [WHR 2021 dataset](https://worldhappiness.report/ed/2021/). Além disso, utiliza modelos de classificação para prever a região de um país no mundo através da relação entre o score de felicidade e as métricas do dataset.

> Nota: Os dados utilizados não foram os do Kaggle. O dataset deles não constam os dados originais, apenas dados relativos.

## Arquitetura

A arquitetura do código do projeto está melhor detalhada [aqui](https://github.com/SalatielBairros/world-happiness-report/blob/main/docs/Architecture.md). Além disso o próprio código contém diversos comentários para facilitar o entendimento.

### Dependências

* [pandas](https://pandas.pydata.org/)
* [xlrd](https://pypi.org/project/xlrd/)
* [pydantic](https://pydantic-docs.helpmanual.io/)
* [scikit-learn](https://scikit-learn.org/)
* [numpy](https://numpy.org/)
* [eli5](https://eli5.readthedocs.io/)
* [fastapi](https://fastapi.tiangolo.com/)
* [joblib](https://joblib.readthedocs.io/)
* [uvicorn](https://uvicorn.org/)
* [wget](https://www.gnu.org/software/wget/)
* [imbalanced-learn](https://imbalanced-learn.readthedocs.io/)
* [pandas-profiling](https://pandas-profiling.readthedocs.io/)

## Rodando ou acessando o projeto

### Publicação Azure

A API do projeto pode ser acessada via [https://tcc-world-happines-report.azurewebsites.net/docs](https://tcc-world-happines-report.azurewebsites.net/docs).

Ela é publicada através de dois serviços do Azure: 

1. [Azure Container Registry](https://azure.microsoft.com/en-us/services/container-registry/) - armazena os containers Docker gerados.
2. [Azure App Service](https://azure.microsoft.com/pt-br/services/app-service/) - Publicação do serviço de API.

Eles são automatizados através da publicação da imagem via Gihub Workflow.

A escolha desses serviços para publicação e a utilização de armazenamento local, não utilizando ferramentas como Hadoop, Spark, etc, foi feita porque (1) o volume de dados utilizado não é tão grande e (2) o custo para criar uma publicação em núvem é muito menor, permitindo até mesmo o uso de serviços gratuitos.

### Rodando API localmente

Para rodar o projeto localmente é necessário primeiro instalar as dependências presentes no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Após isso, basta rodar o projeto através do comando:

>Obs: Utilizar a versão 3.10 do python

```bash
uvicorn main:app --host 0.0.0.0 --port 80
```

### Gerando imagem do Docker

Para gerar a imagem do projeto basta rodar o comando:

```bash
docker build -t tccworldhappinessreport.azurecr.io/modelapi .
```

O nome da imagem informado acima (`tccworldhappinessreport.azurecr.io/modelapi`) é o mesmo utilizado no serviço do Azure.

> Caso realize alguma alteração no arquivo `Dockerfile` após ter gerado a imagem alguma vez, é necessário remover a imagem anterior e apagar a cache dos comandos:

```bash
docker builder prune
docker rmi tccworldhappinessreport.azurecr.io/modelapi
```

Para rodar a imagem basta rodar o comando:

```bash
docker run -p 80:80 tccworldhappinessreport.azurecr.io/modelapi
```

Por fim, para publicar manualmente uma imagem no serviço de registro de containers do Azure basta rodar os comandos:

```bash
docker login tccworldhappinessreport.azurecr.io
docker push tccworldhappinessreport.azurecr.io/modelapi
```

### Executando via console

O arquivo `console_main.py` tem como objetivo permitir a execução de comandos individuais do projeto via console. Basta chamar a função desejada nesse arquivo e executá-lo:

```bash
python console_main.py
```

### Gerando exemplos de retorno

Uma outra funcionalidade implementada é a geração dos exemplos de retorno dos endpoints implementados. Eles são salvos na pasta `docs/api_return_samples`. Para executar basta rodar o comando:

```bash
python generate_samples.py
```

## Variáveis de ambiente

Para que a API rode corretamente algumas variáveis de ambiente são necessárias. Essas variáveis podem ser configuradas tanto a nível de ambiente quando em um arquivo `appsettings.json` no diretório raiz do projeto. O valor _default_ desses parâmetros é:

```json
{
    "OriginalHistoricDataUrl": "https://github.com/SalatielBairros/world-happiness-report/raw/main/docs/used_data/original/HistoricData.xls",
    "Data2021Url": "https://github.com/SalatielBairros/world-happiness-report/raw/main/docs/used_data/original/Data_2021.xls",
    "Kaggle2015Url": "https://raw.githubusercontent.com/SalatielBairros/world-happiness-report/main/docs/used_data/original/kaggle_2015.csv",
    "Kaggle2016Url": "https://raw.githubusercontent.com/SalatielBairros/world-happiness-report/main/docs/used_data/original/kaggle_2016.csv",
    "CountriesUsaDatabaseUrl": "https://raw.githubusercontent.com/SalatielBairros/world-happiness-report/main/docs/used_data/original/countries_usa_database.csv"
}
```

## Modelos utilizados

A versão final do projeto na API utiliza os seguintes modelos tanto para classificação quanto para regressão:

* **Random Forest** [regressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html) | [classifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
* **KNN** [regressor](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html) | [classifier](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)

> É destacável que o KNN é utilizado também pela biblioteca de `data-balancing` para classificação, através do algoritmo [SMOTE](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html).

A escolha desses modelos foi devido ao seu desempenho na etapa de estudo e análise dos modelos. Na etapa de estudo alguns outros modelos foram considerados, como:

* **Linear** [regressor](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) | [classifier](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)
* **SVM** [regressor](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html) | [classifier](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)
* **Decision Tree** [regressor](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html) | [classifier](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)

Não foram utilizados algoritmos de Redes Neurais pois os resultados de algoritmos mais simples e mais explicáveis foram satisfatórios.

> Inclusive, a preocupação com a explicabilidade dos algoritimos utilizados na versão final se mostra presente ao retornamos nos endpoints de `evaluate` dos modelos a lista de importância das `features`, realizada através da lib [eli5](https://eli5.readthedocs.io/en/latest/), mencionada acima.

## Endpoints

### `/data-ingestion`
##### `POST /ingest`
Realiza a ingestão dos dados.
##### `GET /ingested/processed-data`
Retorna os dados processados.
##### `GET /ingested/pandemic-data`
Retorna os dados processados mas apenas com os países presentes na pesquisa de 2020. O propósito é permitir uma análise correta do impacto da pandemia nos dados, visto que houve uma queda no número de países presentes na pesquisa de 2020.
### `/region-classification/{knn|random-forest}`
##### `GET /evaluate`
Retorna os resultados da avaliação dos modelos, como acurácia, importância das features, precisão, recall, f1-score e a matriz de confusão. A avaliação é feita em separação simples de treino e teste, selecionando 20% dos dados para teste aleatoriamente a partir dos dados originais processados.
##### `GET /balanced/evaluate`
Retorna as mesmas métricas do endpoint `/evaluate` mas utilizando para treinamento do modelo os dados balanceados com o algoritmo [SMOTE](https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html). Nesse endpoint são retornadas as avaliações de teste e de validação, onde os dados de teste são oriuntos da separação simples de treino e teste dos dados balanceados, enquanto os dados de validação foram separados antes do balanceamento.
##### `PUT /predict`
Realiza a predição de uma região através dos dados informados de score e métricas.
### `/score-regression/{knn|random-forest}`
##### `GET /evaluate`
Retorna os resultados da avaliação dos modelos de regressão, como R² e R² ajustado, MSE e SMSE, além da relação de importância dos atributos para o respectivo modelo. O retorno é por ano de pesquisa. Dessa forma o modelo é treinado $n$ vezes, onde $n$ é o número de anos de pesquisa e em cada treinamento um dos anos é selecionado como teste. O resultado é a performance do modelo para cada ano quando ele foi selecionado como teste. O objeto de retorno desse endpoint é uma lista da classe `RegressionModelEvaluationResponse`.
##### `PUT /predict`
Realiza a predição de um score através dos dados informados.

## Melhorias futuras

* Criação de um Frontend para a visualização dos dados e dos resultados;
* Utilização de um banco de dados para armazenar o dataset ingerido e os resultados obtidos;
* Paralelizar algumas etapas das transformações dos dados;
* Utilizar Azure files para armazenar os dados ingerido;
* Criar testes unitários;
* Adicionar Azure Application Insights para monitorar o desempenho do serviço.
