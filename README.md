# 🌱 Horta Inteligente 🥕

Bem-vindo(a) à Horta Inteligente! Seu assistente pessoal com Inteligência Artificial (Google Gemini) projetado para ajudar você a cultivar suas próprias plantas comestíveis, mesmo em pequenos espaços, vasos ou canteiros. Obtenha recomendações personalizadas, guias de plantio detalhados e dicas de manejo adaptadas à sua realidade!

## Acesse, está no ar!

https://hortainteligente-imersaoia.streamlit.app/

## 🎯 Objetivo do Projeto

O Horta Inteligente visa democratizar o cultivo de alimentos em casa, oferecendo uma ferramenta inteligente e acessível que considera as condições locais do usuário em qualquer lugar do Brasil, suas preferências de cultivo e o tempo disponível. Acreditamos que todos podem ter o prazer de colher o que plantam, e este sistema foi construído para empoderar você nessa jornada, fornecendo conhecimento e orientação prática.

## ✨ Funcionalidades Principais

* **Coleta Inteligente de Dados:**
    * **Localização Precisa:** Informa sua cidade/estado ou CEP para que o sistema identifique as coordenadas via Nominatim (OpenStreetMap).
    * **Dados Ambientais Regionais (Simulados):** Com base na sua localização, o sistema estima dados climáticos regionais e um tipo de solo base para contextualizar as recomendações.
    * **Perfil do Usuário Detalhado:** Você informa o tamanho do seu espaço, o método principal de cultivo (vasos, canteiros no solo, misto), seu tempo semanal disponível e os tipos de alimentos que deseja cultivar.
* **Recomendações de Plantas Personalizadas com IA (Google Gemini):**
    * O Gemini sugere plantas candidatas com base nos seus tipos de alimento preferidos.
    * Para cada candidata, o Gemini busca informações agronômicas detalhadas, preenchendo um esquema JSON estruturado.
    * Um sistema de pontuação avalia a compatibilidade de cada planta com seu perfil (clima, adequação ao método de cultivo, espaço, tempo), assumindo que você realizará o manejo necessário do solo ou usará substratos adequados em vasos.
* **Guias de Cultivo Detalhados e Personalizados (Gerados pelo Gemini):**
    * Para cada planta sugerida, acesse um guia completo em formato Markdown.
    * Instruções claras sobre preparo do local (vaso ou solo, com dicas para adaptar o solo regional às necessidades da planta), plantio, cuidados essenciais, colheita e mais.
    * Linguagem amigável, concisa e focada na praticidade.
* **Feedback Construtivo:**
    * As sugestões vêm com "Pontos Positivos" (justificativas) e "Pontos de Atenção", com textos gerados por um Agente Redator IA para maior clareza e utilidade.
    * A "Dificuldade Estimada" e o "Nível de Adequação Geral" ajudam na sua escolha.
* **Onde Encontrar Insumos:**
    * Links diretos para buscar sementes/mudas em lojas próximas (via Google Maps) e online (via Google Shopping).
* **Interface Web Interativa:**
    * Construída com Streamlit para uma experiência de usuário fluida e responsiva.

## 🛠️ Tecnologias Utilizadas

* **Linguagem Principal:** Python
* **Inteligência Artificial Generativa:** Google Gemini API (para pesquisa de dados de plantas, sugestão de candidatas, redação de conteúdo e guias)
* **Interface Web:** Streamlit
* **Geocodificação:** Geopy com Nominatim (OpenStreetMap)
* **Bibliotecas Python Comuns:** Pandas, Requests (podem estar em uso indireto ou direto pelos agentes ou utilitários).

## 🚀 Como Configurar e Rodar o Projeto Localmente

Siga estes passos para ter o Horta Inteligente rodando na sua máquina:

1.  **Pré-requisitos:**
    * Python 3.9 ou superior instalado.
    * Git instalado.

2.  **Clonar o Repositório:**
    ```bash
    git clone https://github.com/dougfani/horta_inteligente/
    cd horta-inteligente-app
    ```

3.  **Criar e Ativar Ambiente Virtual:**
    É altamente recomendável usar um ambiente virtual.
    ```bash
    python -m venv .venv
    # No Windows:
    # .venv\Scripts\activate
    # No macOS/Linux:
    # source .venv/bin/activate
    ```

4.  **Instalar Dependências:**
    Com o ambiente virtual ativo, instale todas as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```
    (Certifique-se de que seu arquivo `requirements.txt` está completo e atualizado).

5.  **Configurar a Chave da API do Gemini:**
    * Crie um arquivo chamado `.env` na raiz do seu projeto (`horta-inteligente-app/`).
    * Adicione sua chave da API do Google Gemini a este arquivo:
        ```
        GOOGLE_API_KEY="SUA_CHAVE_API_DO_GEMINI_AQUI"
        ```
    * **Importante:** Certifique-se de que o arquivo `.env` está listado no seu `.gitignore` para não enviar sua chave secreta para o GitHub.

6.  **Rodar a Aplicação Streamlit:**
    Ainda no terminal, com o ambiente virtual ativo e na pasta raiz do projeto:
    ```bash
    streamlit run app.py
    ```
    A aplicação deverá abrir automaticamente no seu navegador web.

## 📂 Estrutura do Projeto (Visão Geral)

horta-inteligente-app/
├── app.py                     # Script principal da aplicação Streamlit
├── agentes/                   # Contém as classes dos diferentes agentes de IA
│   ├── init.py
│   ├── agente_localizador.py
│   ├── agente_gestor_perfil.py
│   ├── agente_estilizador.py      # Define esquema JSON, formata guias
│   ├── agente_pesquisador.py    # Busca dados de plantas com Gemini
│   ├── agente_recomendador.py   # Lógica de sugestão e pontuação
│   ├── agente_gerador_guia.py   # Orquestra a geração do guia
│   ├── agente_redator_ia.py     # Gera textos amigáveis (justificativas, dicas)
│   └── agente_conector_comercial.py # Gera links para compra
├── utils/                     # Módulos com funções auxiliares
│   ├── init.py
│   └── api_clients.py         # Funções para Nominatim, simulações, e chamada ao Gemini
├── assets/                    # Para imagens estáticas como logos, imagem da tela inicial
│   └── imagem_inicial.png     # Exemplo
├── .env                       # Para armazenar sua chave de API localmente (NÃO VERSIONAR)
├── requirements.txt           # Lista de dependências Python
├── .gitignore                 # Especifica arquivos e pastas a serem ignorados pelo Git
└── README.md                  # Este arquivo!

## 📖 Como Usar a Aplicação

1.  **Tela Inicial:** Ao abrir, você verá uma tela de boas-vindas. Clique em "Iniciar Minha Horta!".
2.  **Localização:** Informe sua cidade e estado ou CEP para que o sistema entenda suas condições ambientais regionais.
3.  **Suas Preferências:**
    * Escolha como e onde você planeja plantar (vasos, canteiros, tamanho do espaço).
    * Informe quanto tempo pode dedicar semanalmente.
    * Liste os tipos de alimentos que gostaria de cultivar (ex: "Frutos, Ervas" ou "todos").
4.  **Sugestões:** O sistema, com a ajuda do Gemini, analisará suas informações e apresentará uma lista de plantas sugeridas, com nível de adequação, dificuldade e dicas.
5.  **Guia de Cultivo:** Clique em "Ver Guia Detalhado" para qualquer planta sugerida e receba instruções completas e personalizadas sobre como cultivá-la.
6.  **Onde Encontrar:** No final do guia, você encontrará links para buscar sementes/mudas.
7.  **Nova Consulta:** Use o botão na barra lateral ou no final do fluxo para iniciar uma nova pesquisa.

## 🔮 Próximos Passos e Melhorias Futuras (Sugestões)

* Implementar um Agente Revisor IA para refinar ainda mais os textos gerados.
* Expandir o banco de dados de informações sobre plantas ou a capacidade do Gemini de encontrar dados para mais espécies.
* Integrar com APIs de previsão do tempo em tempo real (se os limites de cota permitirem).
* Permitir que o usuário salve suas plantas "plantadas" e acompanhe seu desenvolvimento.
* Interface visual ainda mais elaborada e interativa.

---

Sinta-se à vontade para usar, modificar e expandir este projeto!
