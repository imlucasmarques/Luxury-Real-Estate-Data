# Luxury-Real-Estate-Data

Repositório destinado ao projeto de raspagem de dados imobiliários de luxo.

## Ferramentas utilizadas

- Versão do [Python](https://www.python.org/): 3.10 ou 3.8
- [MySQL](https://www.mysql.com/)
- [Firefox](https://www.mozilla.org/pt-BR/firefox/new/)
- [Geckodriver](https://github.com/mozilla/geckodriver/releases)

## Setup do projeto

1. Faça a instalação das ferramentas
2. Crie o schema / banco de dados `scrap-estates` no MySQL (`create database scrap_estates`)
3. `pip3 install -r requirements.txt`

## Como usar o projeto

- Para rodar a API: `python3 main.py`
- Para rodar o webscrapping: `python3 -m webscrapping`
- Para rodar os testes: `pytest`
