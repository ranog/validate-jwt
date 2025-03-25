## Instalação das Dependências do Projeto

### LINUX

### Instalar o pyenv
Para gerenciar versões do Python, instale o pyenv seguindo as instruções:
https://github.com/pyenv/pyenv#installation

### Instalar dependências para compilar e instalar o Python
Execute o seguinte comando para instalar as dependências necessárias:
`sudo apt-get update; sudo apt-get install make gcc build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev`

### Instalar o Python 3.12.3
`pyenv install 3.12.3`

### Definir a versão do Python para o projeto
`pyenv local 3.12.3`

### Instalar as dependências do Python
`pip install --upgrade pip setuptools wheel poetry`

### Criar o ambiente virtual com o Poetry
`poetry env use 3.12.3`

### Ativar o ambiente virtual
`source $(poetry env info --path)/bin/activate`

### Instalar as dependências do projeto
`make install-deps`

### Executar o projeto localmente
`make run`

### Acessar Swagger UI e ReDoc - Local

Após executar o projeto, a documentação interativa estará disponível nos seguintes endereços:

- Swagger UI: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
- ReDoc: [http://127.0.0.1:8080/redoc](http://127.0.0.1:8080/redoc)
