## Instruções de Deploy

Este documento descreve os passos para realizar o deploy do projeto em um ambiente de produção, utilizando Vercel para o frontend e um serviço de hospedagem para o backend e banco de dados PostgreSQL.

### Pré-requisitos

- Conta no GitHub: Para versionamento do código e integração com Vercel.
- Conta na Vercel: Para deploy do frontend e backend (usando serverless functions).
- Conta em um provedor de banco de dados PostgreSQL (ex: ElephantSQL, Heroku Postgres, Aiven, etc.).
- Node.js e npm/yarn instalados localmente para build e testes.

### Configuração do Ambiente

1.  **Clonar o Repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO_GIT>
    cd <NOME_DO_REPOSITORIO>
    ```

2.  **Instalar Dependências:**
    ```bash
    npm install
    # ou
    yarn install
    ```

3.  **Configurar Variáveis de Ambiente:**
    - Crie um arquivo `.env` na raiz do projeto.
    - Adicione as seguintes variáveis, substituindo pelos seus valores reais:
      ```
      DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DATABASE"
      SECRET_KEY="sua_chave_secreta_super_segura"
      # Outras variáveis de ambiente necessárias
      ```
    - **Importante:** Adicione `.env` ao arquivo `.gitignore` para não versionar informações sensíveis.

### Deploy do Backend (Flask com PostgreSQL)

1.  **Configurar Banco de Dados:**
    - Crie um banco de dados PostgreSQL no provedor escolhido.
    - Obtenha as credenciais de conexão (usuário, senha, host, porta, nome do banco).
    - Atualize a variável `DATABASE_URL` no arquivo `.env` com essas credenciais.

2.  **Aplicar Migrações:**
    - Certifique-se de que o Flask-Migrate está configurado corretamente.
    - Execute os seguintes comandos para criar e aplicar as migrações:
      ```bash
      flask db init  # Se ainda não foi inicializado
      flask db migrate -m "Initial migration with all models"
      flask db upgrade
      ```

3.  **Deploy na Vercel (ou outra plataforma similar):**
    - Conecte seu repositório GitHub à Vercel.
    - Configure o projeto na Vercel:
        - **Build Command:** `pip install -r requirements.txt && python setup.py install` (ou similar, dependendo da estrutura do seu projeto)
        - **Output Directory:** Geralmente não é necessário para Flask, mas se você tiver arquivos estáticos, configure o diretório correto.
        - **Environment Variables:** Adicione todas as variáveis de ambiente definidas no seu arquivo `.env` (como `DATABASE_URL`, `SECRET_KEY`, etc.) nas configurações do projeto na Vercel.
    - Faça o deploy.

### Deploy do Frontend (Next.js)

1.  **Configurar Variáveis de Ambiente:**
    - Se o frontend precisar de variáveis de ambiente (ex: URL da API), configure-as na Vercel.

2.  **Build do Projeto:**
    - O comando de build para projetos Next.js geralmente é `npm run build` ou `yarn build`.
    - Configure este comando nas configurações de build da Vercel.

3.  **Deploy na Vercel:**
    - Conecte seu repositório GitHub à Vercel.
    - Configure o projeto na Vercel, selecionando o framework Next.js.
    - A Vercel geralmente detecta automaticamente as configurações para projetos Next.js.

### Considerações Adicionais

- **Domínio Personalizado:** Após o deploy, você pode configurar um domínio personalizado tanto para o frontend quanto para o backend através das configurações da Vercel.
- **HTTPS:** A Vercel automaticamente provisiona certificados SSL/TLS para seus deployments, garantindo HTTPS.
- **Monitoramento e Logs:** Utilize as ferramentas de monitoramento e logs da Vercel para acompanhar a saúde e o desempenho da sua aplicação.

Lembre-se de substituir os placeholders (como `<URL_DO_REPOSITORIO_GIT>`, `<NOME_DO_REPOSITORIO>`, etc.) pelos seus valores reais. Se encontrar algum problema, consulte a documentação da Vercel e das tecnologias específicas que você está utilizando.
