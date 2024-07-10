# Sistema de Estoque
Este projeto é um sistema de gerenciamento de estoque desenvolvido em Python, utilizando as bibliotecas 'tkinter' e 'customtkinter' para criar a interface gráfica do sistema, 'sqlite3' para a criação do banco de dados para o estoque e dos históricos de entrada e saída das mercadorias, 'pandas' para manipular os dados em dataframes, 'matplotlib' para plotar os dados em gráficos e 'barcode' para junto com outras funções gerar um código de barras para cada produto. O sistema permite gerenciar produtos, gerar códigos de barras, e visualizar relatórios.

## Funcionalidades

- Cadastro de Produtos: Permite adicionar novos produtos ao estoque com detalhes como nome, quantidade, preço, etc.
- Gerenciamento de Estoque: Permite atualizar, excluir e visualizar produtos no estoque.
- Criação de Códigos de Barras: Gera códigos de barras para os produtos cadastrados.
- Relatórios e Gráficos: Visualiza relatórios e gráficos sobre o estoque e vendas.
  
## Tecnologias Utilizadas
- Python: Linguagem de programação principal utilizada no projeto.

## Tela de Login
<img src="https://github.com/MrcsFaria/Sistema-de-Estoque/blob/main/Prints/9.PNG">

## Tela de Menu
<img src="https://github.com/MrcsFaria/Sistema-de-Estoque/blob/main/Prints/8.PNG">

## Tela de Estoque
<img src="https://github.com/MrcsFaria/Sistema-de-Estoque/blob/main/Prints/2.PNG">

## Tela de Visualização do Código de Barras
<img src="https://github.com/MrcsFaria/Sistema-de-Estoque/blob/main/Prints/4.PNG">

## Tela de Retirada do Item
<img src="https://github.com/MrcsFaria/Sistema-de-Estoque/blob/main/Prints/6.PNG">

## Tela de Menu - Gráficos
<img src="https://github.com/MrcsFaria/Sistema-de-Estoque/blob/main/Prints/5.PNG">

## Tela de Acompanhamento - Estoque
<img src="https://github.com/MrcsFaria/Sistema-de-Estoque/blob/main/Prints/3.PNG">

## Tela de Acompanhamento - Entrada e Saída de Mercadorias
<img src="https://github.com/MrcsFaria/Sistema-de-Estoque/blob/main/Prints/7.PNG">


## Bibliotecas Python:
- datetime: Para manipulação de datas.
- random: Para geração de números aleatórios.
- tkinter: Biblioteca padrão do Python para interfaces gráficas.
- customtkinter: Utilizada para criar uma interface gráfica com componentes customizáveis.
- sqlite3: Biblioteca para gerenciar o banco de dados SQLite.
- pandas: Para manipulação e análise de dados.
- matplotlib: Para geração de gráficos.
- barcode: Para geração de códigos de barras.
- PIL: Para manipulação de imagens.


## Estrutura do Projeto

- 'Banco_de_dados/estoque.db': Banco de dados SQLite onde os produtos são armazenados.
- 'assets/': Diretório contendo as imagens e ícones utilizados na interface gráfica.
- 'códigos_de_barras/': Diretório onde os códigos de barras são salvos
- 'criar_banco.py': Script que cria as tabelas no banco.
- 'main.py': Script principal que executa o sistema de gerenciamento de estoque.

## Como Executar
Pré-requisitos: Python

```bash
# clonar repositório
git clone https://github.com/MrcsFaria/Sistema-de-Estoque

# Navegue até o diretório do projeto:
cd Sistema-de-Estoque

# Instale as dependências necessárias
pip install customtkinter tkinter pandas sqlite3 matplotlib python-barcode pillow

# Crie uma pasta `códigos_de_barras` na raiz do projeto

# executar o projeto
python main.py
```

# Autor

Marcos Vinicius Faria

https://br.linkedin.com/in/marcos-vinicius-faria-124266186
