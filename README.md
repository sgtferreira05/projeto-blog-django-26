
🎾 Tennis Players Blog

Este é um projeto de blog desenvolvido com Django dedicado ao mundo do tênis, cobrindo informações sobre os líderes dos circuitos ATP (masculino) e WTA (feminino).

O projeto permite a gestão completa de conteúdos através de uma interface administrativa customizada e oferece uma navegação fluida para os usuários acompanharem o ranking e biografia dos atletas.

🚀 Funcionalidades

Frontend

    Página Inicial Dinâmica: Listagem de posts (cards de jogadores) com imagens e resumos.

    Filtragem por Categoria: Navegação entre ATP, WTA ou todos os jogadores.

    Sistema de Busca: Pesquisa rápida por nome ou conteúdo.

    Tags de Conquistas: Visualização de ícones/tags dos Grand Slams conquistados (Wimbledon, US Open, etc).

    Páginas Institucionais: Seção "About me" e outras páginas estáticas gerenciáveis.

Backend (Django Admin)

    Gestão de Posts: Criação de conteúdos com editor Rich Text, suporte a slugs automáticos e anexos.

    Categorias e Tags: Organização taxonômica dos jogadores.

    Configuração do Site: Gerenciamento de menus e parâmetros globais (Setup) via Admin.

    Segurança: Controle de acessos e tentativas de login via app Axes.

🛠️ Tecnologias Utilizadas

    Linguagem: Python 3.x

    Framework Web: Django

    Banco de Dados: SQLite (desenvolvimento) / PostgreSQL (produção via Docker)

    Frontend: HTML5, CSS3 (Custom Styles), JavaScript

    Containerização: Docker & Docker Compose

    Bibliotecas Principais: * django-summernote ou similar (para o editor de texto)

        django-axes (segurança)

        python-dotenv (variáveis de ambiente)


🔧 Como Executar o Projeto
Pré-requisitos

    Python 3.10+

    Virtualenv (recomendado) ou Docker instalado.

Passo a Passo (Local)

    Clone o repositório:
    Bash

    git clone https://github.com/sgtferreira05/projeto-blog-django-26.git
    cd projeto-blog-django-26

    Crie e ative uma virtualenv:
    Bash

    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate

    Instale as dependências:
    Bash

    pip install -r requirements.txt

    Configure as variáveis de ambiente:
    Crie um arquivo .env na raiz baseado no .env-example e preencha sua SECRET_KEY.

    Rode as migrações e inicie o servidor:
    Bash

    python manage.py migrate
    python manage.py runserver

    Acesse: http://127.0.0.1:8000/

Via Docker
Bash

docker-compose up --build

Criado por Ailton Ferreira 🚀
