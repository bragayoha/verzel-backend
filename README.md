# Instalação da Aplicação

**Clone o repositório:**
`git clone https://github.com/bragayoha/verzel-backend.git`
`cd verzel-backend`

**Instale as Dependências:**

`pip install -r requirements.txt`

# Configuração do Banco de Dados

**Execute as Migrações do Banco de Dados:**

`flask db init`
`flask db migrate`
`flask db upgrade`

# Execução da Aplicação

**Execute a Aplicação:**

`flask run` \*_A aplicação estará disponível em http://localhost:5000._

# Docker (Opcional)

**Construa a Imagem Docker:**

`docker build -t verzel-backend .`

**Execute o Contêiner Docker:**

`docker run -p 5000:5000 verzel-backend` \*_A aplicação estará disponível em http://localhost:5000._

##### Atenção: Certifique-se de ter o Python e o pip instalados.
