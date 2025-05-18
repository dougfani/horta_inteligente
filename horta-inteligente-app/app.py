# app.py
import streamlit as st
import os
import json 
from datetime import datetime 
import random 
from dotenv import load_dotenv 

# --- Configurações da Página Streamlit (PRIMEIRO COMANDO STREAMLIT) ---
st.set_page_config(
    page_title="Horta Inteligente", 
    page_icon="🌱", 
    layout="centered", # Layout centralizado para melhor leitura
    initial_sidebar_state="expanded" 
)

# --- CSS Customizado para Tema Claro "Roça/Horta" ---
# Injetado diretamente para simplicidade e garantir aplicação.
st.markdown("""
<style>
    /* Importa as fontes do Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Domine:wght@400;700&display=swap');

    /* --- Variáveis de Cor (Tema "Roça/Horta" Simplificado) --- */
    :root {
        --cor-fundo-pagina: #F9F6F0;     /* Bege bem claro, como papel reciclado */
        --cor-fundo-container: #FFFFFF;  
        --cor-texto-titulos: #5D4037;    /* Marrom escuro */
        --cor-texto-principal: #6D4C41; /* Marrom médio */
        --cor-texto-secundario: #7A6C62; /* Marrom claro */
        --cor-verde-principal: #aae576;      /* Verde oliva/folha */
        --cor-verde-destaque: #aae576;   /* Verde lima claro */
        --cor-laranja-acao: #F57C00;     /* Laranja mais vibrante para botões principais */
        --cor-laranja-acao-hover: #EF6C00;
        --cor-borda: #D7CCC8;            
        --sombra-suave: 0 2px 8px rgba(0, 0, 0, 0.08);
        --border-radius-padrao: 8px;
        --fonte-titulos: 'Domine', serif;        
        --fonte-corpo: 'Inter', sans-serif;
    }

    /* --- Estilos Globais --- */
    body, .stApp {
        font-family: var(--fonte-corpo);
        color: var(--cor-texto-principal);
        background-color: var(--cor-fundo-pagina) !important;
    }

    /* Container principal do Streamlit (onde o conteúdo das etapas aparece) */
    /* Este seletor pode precisar de ajuste dependendo da versão do Streamlit e do tema base */
    .main .block-container {
        max-width: 720px; 
        margin: 1.5rem auto 3rem auto; /* Menor margem no topo */
        padding: 1.5rem 2rem !important; 
        background-color: var(--cor-fundo-container);
        border-radius: var(--border-radius-padrao);
        box-shadow: var(--sombra-suave);
    }

    /* Tipografia */
    h1 { /* Para st.title() */
        font-family: var(--fonte-titulos); 
        color: var(--cor-texto-titulos); 
        text-align: center; 
        font-size: 2.2em; 
        margin-bottom: 1rem; 
    }
    h2 { /* Para st.header() - Títulos de seção */
        font-family: var(--fonte-titulos);
        color: var(--cor-texto-titulos); 
        border-bottom: 2px solid var(--cor-verde-destaque); 
        padding-bottom: 0.5rem; 
        margin-top: 2rem; 
        margin-bottom: 1.2rem; 
        font-size: 1.6em; 
        text-align: left;
    }
    h3 { /* Para st.subheader() e ### do Markdown */
        font-family: var(--fonte-titulos);
        color: var(--cor-verde-principal); 
        margin-top: 1.5rem; 
        margin-bottom: 0.8rem; 
        font-size: 1.3em; 
        text-align: left;
    }
    p, .stMarkdown p, li { color: var(--cor-texto-secundario); font-size: 1em; line-height: 1.65; margin-bottom: 0.8rem; }
    strong { color: var(--cor-texto-titulos); }
    a { color: var(--cor-laranja-acao); font-weight: 600; }
    a:hover { color: var(--cor-laranja-acao-hover); }

    /* Componentes Streamlit */
    .stButton>button {
        border: none; border-radius: var(--border-radius-padrao); color: white; 
        background-color: var(--cor-verde-principal); 
        padding: 9px 22px; font-weight: 600; font-size: 0.95em; /* Botões um pouco menores */
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { background-color: #4A5D23; transform: translateY(-1px); }
    
    /* Botão de ação principal (ex: "Analisar Localização", "Buscar Sugestões") */
    .stButton[key*="btn_submit"] button, 
    .stButton[key*="btn_iniciar"] button { /* A chave do seu botão "Iniciar Minha Horta" deve ser btn_iniciar_app... */
        background-color: var(--cor-laranja-acao);
        font-size: 1em; /* Tamanho do botão principal */
    }
    .stButton[key*="btn_submit"] button:hover,
    .stButton[key*="btn_iniciar"] button:hover {
        background-color: var(--cor-laranja-acao-hover);
    }

    .stTextInput input, .stTextArea textarea {
        border-radius: 6px; border: 1.5px solid var(--cor-borda);
        background-color: #FFFFFF; padding: 10px 12px; 
        font-size: 0.95em; /* Fonte do input um pouco menor */
        color: var(--cor-texto-principal);
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--cor-verde-principal); box-shadow: 0 0 0 2px rgba(85, 107, 47, 0.15);
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder { color: #A89F97 !important; opacity: 1; }

    /* Estilo para os Rádios */
    .stRadio div[role="radiogroup"] { margin-top: 0.5rem; } /* Reduz espaço acima dos radios */
    .stRadio div[role="radiogroup"] > label { 
        background-color: #FDFDF5; /* Fundo do card da opção mais sutil */
        padding: 0.7rem 0.9rem; 
        border-radius: 8px; 
        margin-bottom: 0.5rem; /* Menos espaço entre opções */
        border: 1px solid var(--cor-borda);
        cursor: pointer;
    }
    .stRadio div[role="radiogroup"] > label:hover { border-color: var(--cor-verde-destaque); background-color: #F5F5E8;}
    .stRadio > label > div[data-baseweb="radio"] > div > div { border-color: var(--cor-verde-principal) !important; }
    .stRadio > label[data-baseweb="radio"] input[type="radio"]:checked + div {
        background-color: var(--cor-verde-destaque) !important; 
        border-color: var(--cor-verde-folha) !important;
    }
    .stRadio div[role="radiogroup"] > label p { color: var(--cor-texto-principal); font-weight: 500; margin-bottom:0 !important; }
    
    /* Alertas (st.info, st.success, etc.) */
    .stAlert { border-radius: 8px; padding: 1rem; font-size: 0.95em; border-left-width: 4px;}
    .stAlert[data-testid="stInfo"] { border-left-color: #607D8B; background-color: #ECEFF1;} 
    .stAlert[data-testid="stSuccess"] { border-left-color: var(--cor-verde-principal); background-color: #E6F4EA;}
    .stAlert[data-testid="stWarning"] { border-left-color: var(--cor-laranja-terracota); background-color: #FFF3E0;}
    .stAlert[data-testid="stError"] { border-left-color: #C62828; background-color: #FFEBEE;}

    /* Sidebar */
    .stSidebar { background-color: #F4F1EA; /* Bege mais quente para sidebar */ border-right: 1px solid var(--cor-borda); }
    .stSidebar .stButton>button { background-color: var(--cor-verde-folha); width: 100%; color: white; }
    .stSidebar .stButton>button:hover { background-color: #4A5D23; }
    .stSidebar h1, .stSidebar h2, .stSidebar h3 { color: var(--cor-texto-titulos); }

    /* Estilos específicos para cards de sugestão e guia (se você os usa com classes CSS) */
    .suggestion-card { /* Se você envolve suas sugestões com <div class='suggestion-card'> */
        background-color: var(--cor-fundo-container); border-radius: var(--border-radius-padrao);
        padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: var(--sombra-suave);
        border-left: 4px solid var(--cor-verde-principal);
    }
    .suggestion-card img { width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 1rem; }
    .guide-content { /* Se você envolve seu guia com <div class='guide-content'> */
         padding: 0.5rem; /* O container principal já tem padding */
    }
    .guide-content h3 {font-size: 1.3em; margin-top: 1.8rem;}

    div[data-baseweb="tooltip"], 
    div[data-testid="stTooltipContent"] {
    background-color: #FFFFFF !important; /* Fundo branco para o tooltip */
    color: var(--cor-texto-principal) !important; /* Texto escuro */
    border: 1px solid var(--cor-borda) !important;
    border-radius: var(--border-radius-padrao) !important;
    box-shadow: var(--sombra-suave) !important;
    padding: 0.5rem 0.75rem !important;
    font-size: 0.9em !important;
    font-family: var(--fonte-corpo) !important;
}

/* Se o tooltip for o title nativo do HTML, este CSS não terá efeito.
   Nesse caso, a solução é evitar que o Streamlit coloque texto longo no atributo 'title'
   do input, o que geralmente acontece com o parâmetro 'help' do st.text_input. */

/* Para garantir que o input em si não tenha cores escuras inesperadas no hover/focus que possam parecer um tooltip */
.stTextInput input:hover, 
.stTextInput input:focus {
    background-color: #FFFFFF !important; /* Garante fundo branco no hover/focus */
    color: var(--cor-texto-principal) !important; /* Garante texto escuro */
}
            
</style>
""", unsafe_allow_html=True)



# Importações das suas classes de agentes e funções utilitárias
from agentes.agente_localizador import AgenteLocalizadorAmbiental
from agentes.agente_gestor_perfil import AgenteGestorPerfilUsuario
from agentes.agente_estilizador import AgenteEstilizadorConteudoGemini
from agentes.agente_pesquisador import AgentePesquisadorPlantasGemini
from agentes.agente_recomendador import AgenteRecomendadorAgronomoVirtual
from agentes.agente_gerador_guia import AgenteGeradorConteudoPlantioDetalhado
from agentes.agente_conector_comercial import AgenteConectorComercialPlantas
from agentes.agente_redator_ia import AgenteRedatorConteudoIA # NOVO IMPORT

from utils.api_clients import (
    geocode_address_nominatim, # Assegure-se que esta e outras funções de utils estão completas
    get_simulated_average_weather,
    # mock_estimar_solo_regional, # Usado dentro de geocode_address_nominatim
    mock_api_dados_solo_regional,
    # mock_estimar_clima_regional, # Usado dentro de geocode_address_nominatim
    gerar_link_Maps_lojas,
    gerar_link_google_shopping,
    gerar_conteudo_com_gemini
)


import google.generativeai as genai

# --- 1. Configuração Inicial da Aplicação ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

MODEL_CONFIG = {"temperature": 0.7, "top_p": 0.95, "top_k": 40}
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
gemini_model_global_instance = None
gemini_configurado_com_sucesso = False

if not GEMINI_API_KEY:
    st.error("🚨 CHAVE DE API DO GEMINI (GOOGLE_API_KEY) não configurada! Verifique suas variáveis de ambiente ou arquivo .env.")
else:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model_global_instance = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            generation_config=MODEL_CONFIG,
            safety_settings=SAFETY_SETTINGS
        )
        print("✅ API do Gemini configurada e modelo instanciado com sucesso para a aplicação.")
        gemini_configurado_com_sucesso = True
    except Exception as e:
        st.error(f"🚨 Erro ao configurar o Gemini ou instanciar o modelo: {e}")
        print(f"🚨 Erro ao configurar o Gemini ou instanciar o modelo: {e}")

# --- 2. Instanciação dos Agentes ---
@st.cache_resource
def inicializar_agentes(_modelo_gemini_param, config_gemini_param):
    modelo_gemini = _modelo_gemini_param 
    print("Executando inicializar_agentes() com modelo, config E REDATOR...")
    ag_localizador = AgenteLocalizadorAmbiental()
    ag_perfil = AgenteGestorPerfilUsuario()
    
    ag_estilizador = AgenteEstilizadorConteudoGemini(modelo_gemini, config_gemini_param)
    ag_pesquisador = AgentePesquisadorPlantasGemini(ag_estilizador, modelo_gemini, config_gemini_param)
    
    # Instanciar o Redator
    ag_redator = AgenteRedatorConteudoIA(modelo_gemini, config_gemini_param) # NOVO
    
    # Passar o Redator para o Recomendador
    ag_recomendador = AgenteRecomendadorAgronomoVirtual(
        ag_pesquisador, 
        ag_estilizador, 
        modelo_gemini, 
        config_gemini_param,
        ag_redator # <--- PASSANDO O REDATOR
    )
    
    # O AgenteGeradorGuia usa o Estilizador, que agora tem um prompt de formatação melhorado.
    # Se quiséssemos que o GeradorGuia usasse o Redator para seções específicas de forma mais granular,
    # ele também precisaria receber ag_redator no seu __init__.
    # Por ora, a melhoria no prompt do Estilizador para o guia completo é o foco.
    ag_guia = AgenteGeradorConteudoPlantioDetalhado(ag_pesquisador, ag_estilizador)
    
    ag_comercial = AgenteConectorComercialPlantas()
    return {
        "localizador": ag_localizador, "perfil": ag_perfil, "estilizador": ag_estilizador,
        "pesquisador": ag_pesquisador, "recomendador": ag_recomendador,
        "guia": ag_guia, "comercial": ag_comercial,
        "redator": ag_redator # Adiciona ao dict para possível uso direto no app, se necessário
    }
    
agentes = {} # Inicializa o dict de agentes
if gemini_configurado_com_sucesso:
    agentes = inicializar_agentes(gemini_model_global_instance, MODEL_CONFIG)
    ag_localizador = agentes.get("localizador")
    ag_perfil = agentes.get("perfil")
    ag_estilizador = agentes.get("estilizador")
    ag_pesquisador = agentes.get("pesquisador")
    ag_recomendador = agentes.get("recomendador")
    ag_guia = agentes.get("guia")
    ag_comercial = agentes.get("comercial")
else:
    st.warning("Configuração do Gemini falhou. Algumas funcionalidades podem não estar disponíveis.")
    # Definir agentes como None ou mocks se necessário para o app não quebrar totalmente
    ag_localizador, ag_perfil, ag_estilizador, ag_pesquisador, ag_recomendador, ag_guia, ag_comercial = [None] * 7


# --- 3. Inicialização do st.session_state ---
if 'etapa_atual' not in st.session_state: st.session_state.etapa_atual = "inicio"
if 'id_usuario' not in st.session_state: st.session_state.id_usuario = f"user_streamlit_{random.randint(1000,9999)}"
if 'dados_ambientais' not in st.session_state: st.session_state.dados_ambientais = None
if 'preferencias_usuario' not in st.session_state: st.session_state.preferencias_usuario = None
if 'sugestoes_plantas' not in st.session_state: st.session_state.sugestoes_plantas = []
if 'planta_selecionada_guia' not in st.session_state: st.session_state.planta_selecionada_guia = None
if 'guia_gerado_md' not in st.session_state: st.session_state.guia_gerado_md = None

if 'esquema_definido' not in st.session_state and gemini_configurado_com_sucesso and ag_estilizador:
    with st.spinner("Bem vindo! Preparando nossas enxadas e regadores..."):
        esquema = ag_estilizador.get_esquema_dados_planta()
        if esquema: st.session_state.esquema_definido = True; print("Esquema de dados OK.")
        else: st.session_state.esquema_definido = False; st.error("Falha ao definir esquema de dados."); st.stop()
elif not gemini_configurado_com_sucesso or not ag_estilizador:
     st.session_state.esquema_definido = False


# --- 4. Título Principal ---
st.title("🌿 Horta Inteligente 🥕")
st.markdown("""
Bem-vindo(a) ao **Horta Inteligente**! 🌱✨

Este sistema foi criado para te ajudar a planejar sua horta de forma personalizada. 
Basta nos informar sua **localização** e algumas **preferências de cultivo**, como o espaço disponível e o tipo de planta que deseja. 
Nossa Inteligência Artificial (IA) analisará esses dados e as condições ambientais da sua região para sugerir as plantas mais adequadas e fornecer um guia de cultivo detalhado para cada uma delas. 
Prepare a terra e vamos cultivar juntos!
""")
# st.markdown("---")

# --- 5. Lógica do Fluxo Principal ---

if not gemini_configurado_com_sucesso:
    st.stop() # Para a execução se o Gemini não estiver OK
if not st.session_state.get('esquema_definido', False) and st.session_state.etapa_atual != "inicio": # Permite que a tela de início carregue
    st.warning("Aguardando definição do esquema de dados... Se demorar, recarregue a página.")
    st.stop()


if st.session_state.etapa_atual != "inicio":
    if st.button("⬅️ Nova Consulta / Voltar ao Início", key="btn_reiniciar_main"):
        for key in ['etapa_atual', 'dados_ambientais', 'preferencias_usuario', 'sugestoes_plantas', 'planta_selecionada_guia', 'guia_gerado_md']:
            if key == 'etapa_atual': st.session_state[key] = "inicio"
            elif isinstance(st.session_state.get(key), list): st.session_state[key] = []
            else: st.session_state[key] = None
        st.rerun() # CORRIGIDO


if st.session_state.etapa_atual == "inicio":
    st.header("Onde você vai plantar?")
    # Garantir que ag_localizador foi instanciado
    if ag_localizador:
        endereco_digitado = st.text_input("Digite sua cidade e estado (ex: Salvador, BA) ou CEP:", key="loc_input_main")
        if st.button("Analisar Localização", key="btn_submit_loc_main"):
            if endereco_digitado:
                with st.spinner("Analisando sua localização..."):
                    app_user_agent_st = f"HortaInteligenteStreamlitApp/{random.randint(100,999)}"
                    dados_amb = ag_localizador.obter_localizacao_e_dados_ambientais_usuario(
                        endereco_texto=endereco_digitado, app_nome_user_agent=app_user_agent_st)
                if dados_amb and dados_amb.get('localizacao'):
                    st.session_state.dados_ambientais = dados_amb
                    st.session_state.etapa_atual = "preferencias"
                    st.rerun() # CORRIGIDO
                else: st.error("Não foi possível obter dados para esta localização. Tente um endereço mais específico.")
            else: st.warning("Por favor, insira sua localização.")
    else:
        st.error("Agente Localizador não inicializado. Verifique a configuração.")


elif st.session_state.etapa_atual == "preferencias":
    st.header("Suas Preferências de Cultivo")
    if st.session_state.dados_ambientais:
        loc_info = st.session_state.dados_ambientais['localizacao']
        st.markdown(f"**Localização Confirmada:** {loc_info.get('endereco_formatado', 'N/A')}")
        # ... (outros prints de clima/solo se desejar) ...
    
    # st.markdown("---"); 
    st.markdown("**Sobre o Preparo do Solo/Vasos:**")
    st.info("Lembre-se: Ao escolher 'Canteiros no solo', nossas sugestões assumem que você preparará e melhorará seu solo local. Para 'Vasos', o foco será no substrato adequado.")
    # st.markdown("---")

    espaco_metodo_opcoes_st = {
        "1": "Vasos e espaços bem pequenos (ex: janela, varandinha, <1m²)",
        "2": "Vasos e varandas/pátios pequenos (1-3m²)",
        "3": "Canteiros no chão ou vasos em quintal médio (3-5m²)",
        "4": "Quintal grande com canteiros no chão (>5m²)"}
    escolha_em_key = st.radio("Como e onde você planeja plantar principalmente?", options=list(espaco_metodo_opcoes_st.keys()), format_func=lambda k: espaco_metodo_opcoes_st[k], key="radio_esp_met_main")
    tempo_opcoes_st = {"1": "Pouco (<1-2h/semana)", "2": "Moderado (2-4h/semana)", "3": "Bastante (>4h/semana)"}
    escolha_tempo_key = st.radio("Quanto tempo você pode dedicar às plantas por semana?", options=list(tempo_opcoes_st.keys()), format_func=lambda k: tempo_opcoes_st[k], key="radio_tempo_main")
    tipos_alimento_input_st = st.text_input("Quais tipos de plantas você tem preferência? (Ex: Folhosas, Frutos, Ervas. Digite 'todos' ou separe por vírgula)", placeholder="Folhosa, Fruto", key="text_tipo_alim_main")

    if st.button("Buscar Sugestões de Plantas", key="btn_submit_prefs_main"):
        map_escolha_em = {
            "1": {"metodo": "vaso_pequeno", "tamanho_valor": 0.5, "texto_opcao": espaco_metodo_opcoes_st["1"]},
            "2": {"metodo": "vaso_medio", "tamanho_valor": 2.0, "texto_opcao": espaco_metodo_opcoes_st["2"]},
            "3": {"metodo": "misto_solo_vaso_medio", "tamanho_valor": 4.0, "texto_opcao": espaco_metodo_opcoes_st["3"]},
            "4": {"metodo": "solo_grande", "tamanho_valor": 10.0, "texto_opcao": espaco_metodo_opcoes_st["4"]}}
        pref_esp_met = map_escolha_em[escolha_em_key]
        map_escolha_tempo = {"1": {"texto": tempo_opcoes_st["1"], "valor": 1.5}, "2": {"texto": tempo_opcoes_st["2"], "valor": 3.0}, "3": {"texto": tempo_opcoes_st["3"], "valor": 5.0}}
        pref_tempo = map_escolha_tempo[escolha_tempo_key]
        if not tipos_alimento_input_st.strip() or tipos_alimento_input_st.strip().lower() == 'todos':
            pref_tipos_alimento = ["Folhosa", "Fruto", "Raiz", "Erva Aromática", "Tempero", "Pimenta", "Grão", "Leguminosa", "Flor Comestível"]
        else: pref_tipos_alimento = [p.strip().capitalize() for p in tipos_alimento_input_st.split(',') if p.strip()]
        
        st.session_state.preferencias_usuario = {
            "texto_opcao_espaco_metodo": pref_esp_met["texto_opcao"], "metodo_cultivo_predominante": pref_esp_met["metodo"],
            "espaco_disponivel_m2_valor_aprox": pref_esp_met["tamanho_valor"], "tempo_dedicacao_semanal_texto": pref_tempo["texto"],
            "tempo_dedicacao_semanal_horas_valor_aprox": pref_tempo["valor"], "tipos_alimento_preferidos": pref_tipos_alimento,
            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        if ag_perfil: ag_perfil.salvar_preferencias_plantio(st.session_state.id_usuario, st.session_state.preferencias_usuario)
        
        st.session_state.etapa_atual = "sugestoes"
        st.session_state.sugestoes_plantas = [] # Limpa sugestões antigas antes de buscar novas
        st.session_state.guia_gerado_md = None # Limpa guia antigo
        st.rerun() # CORRIGIDO

elif st.session_state.etapa_atual == "sugestoes":
    st.header("Nossas Sugestões Para Você 🌱")
    if not st.session_state.sugestoes_plantas and ag_recomendador and st.session_state.preferencias_usuario and st.session_state.dados_ambientais:
        with st.spinner("Aguarde enquanto o Gemini analisa e busca as melhores plantas... Pode demorar um pouquinho mas vale a pena!"):
            sugestoes = ag_recomendador.gerar_sugestoes_otimizadas(
                st.session_state.preferencias_usuario, st.session_state.dados_ambientais, max_sugestoes_finais=3)
            st.session_state.sugestoes_plantas = sugestoes
    
    sugestoes_atuais = st.session_state.sugestoes_plantas

    if not sugestoes_atuais:
        # MENSAGEM DE FALLBACK MELHORADA
        st.warning("🙁 Com base nos seus critérios exatos, não encontramos uma combinação perfeita no momento.")
        st.markdown("**No entanto, não desanime! Muitas plantas são bastante adaptáveis, especialmente com os cuidados certos.**")
        st.markdown(f"Para seu cenário (espaço: `{st.session_state.preferencias_usuario.get('texto_opcao_espaco_metodo', 'Não informado')}`, tempo: `{st.session_state.preferencias_usuario.get('tempo_dedicacao_semanal_texto', 'Não informado')}` na região de `{st.session_state.dados_ambientais.get('localizacao',{}).get('cidade', 'sua localidade')}`), aqui vão algumas ideias gerais que costumam funcionar bem para iniciantes ou com manejo:")
        st.markdown("""
            * **Ervas Aromáticas em Vasos:** Manjericão, Hortelã, Cebolinha, Salsinha, Orégano, Alecrim. Geralmente fáceis, ocupam pouco espaço e precisam de sol.
            * **Hortaliças de Folha de Ciclo Curto:** Alfaces (variedades soltas), Rúcula. Podem ir bem em vasos ou jardineiras com bom substrato.
            * **Morango:** Variedades adaptadas a vasos podem produzir bem com sol e rega regular.
            * **Pimentas de Porte Pequeno:** Algumas variedades são compactas e produtivas em vasos.
        """)
        st.markdown("Experimente refinar suas preferências ou pesquisar variedades específicas dessas plantas. Você também pode clicar em 'Nova Consulta' para tentar outros tipos de alimentos!")
    else:
        st.markdown("Baseado em suas preferências e na sua região, estas são algumas plantas que o nosso assistente Gemini sugere para você cultivar:")
        for i, planta_sug in enumerate(sugestoes_atuais):
            with st.container():
                st.markdown(f"### {i+1}. {planta_sug['nome_popular']}")
                
                dificuldade_exibir = planta_sug.get('dificuldade_cultivo', 'Verificar no guia')
                if dificuldade_exibir.lower() == "n/a" or "não especificado" in dificuldade_exibir.lower() or not dificuldade_exibir.strip() or "verificar" in dificuldade_exibir.lower():
                    dificuldade_exibir = "Confira os detalhes no guia de cultivo."
                
                score_num = planta_sug.get('score_compatibilidade', 0)
                score_texto = ""
                if score_num >= 0.80: score_texto = "Excelente Compatibilidade com seu perfil ✅"
                elif score_num >= 0.60: score_texto = "Boa Compatibilidade com seu perfil 👍"
                elif score_num >= 0.35: score_texto = "Compatível com alguns cuidados e atenção 👀" # Limiar do recomendador
                else: score_texto = "Compatibilidade Baixa (Pode ser desafiador) 👎"

                st.markdown(f"*Dificuldade Estimada: {dificuldade_exibir}*")
                st.info(f"**Nível de Adequação Geral:** {score_texto}")

                if planta_sug.get('justificativas') and any(j.strip() for j in planta_sug['justificativas']): 
                    with st.expander("👍 Por que esta planta pode ser uma boa escolha para você:", expanded=False):
                        for just in planta_sug['justificativas']: 
                            if just.strip(): st.markdown(f"- {just}")
                
                if planta_sug.get('pontos_atencao') and any(p.strip() for p in planta_sug['pontos_atencao']):
                    with st.expander("⚠️ Pontos importantes para ter sucesso:", expanded=True): # Deixar expandido por padrão
                        for pa in planta_sug['pontos_atencao']: 
                            if pa.strip(): st.markdown(f"- {pa}")
                elif not planta_sug.get('pontos_atencao') and score_num < 0.80 : # Se não tem pontos de atenção específicos mas score não é excelente
                     with st.expander("⚠️ Pontos importantes para ter sucesso:", expanded=True):
                        st.markdown("- Verifique todos os detalhes no guia de cultivo para garantir as melhores condições para esta planta.")


                if st.button(f"Ver Guia Detalhado para {planta_sug['nome_popular']}", key=f"guia_btn_app_{i}_v3"):
                    st.session_state.planta_selecionada_guia = planta_sug
                    st.session_state.etapa_atual = "guia"
                    st.session_state.guia_gerado_md = None 
                    st.rerun()
                # st.markdown("---") 

elif st.session_state.etapa_atual == "guia":
    planta_para_guia = st.session_state.planta_selecionada_guia
    if not planta_para_guia or not ag_guia or not ag_pesquisador: # Checa se agentes existem
        st.error("Erro: Informações da planta ou agentes necessários não disponíveis."); st.stop()
    
    nome_planta_guia = planta_para_guia['nome_popular']
    st.header(f"📖 Guia de Cultivo para: {nome_planta_guia}")

    if not st.session_state.guia_gerado_md:
        with st.spinner(f"Gerando guia personalizado para {nome_planta_guia}..."):
            dados_json_planta_guia = planta_para_guia.get('_dados_completos_json')
            if not dados_json_planta_guia: # Fallback se o JSON não veio com a sugestão
                dados_json_planta_guia = ag_pesquisador.obter_dados_detalhados_planta(nome_planta_guia)

            if dados_json_planta_guia:
                guia_md = ag_guia.gerar_guia_plantio_para_planta_sugerida(
                    nome_planta_guia, dados_json_planta_guia,
                    st.session_state.dados_ambientais, st.session_state.preferencias_usuario)
                st.session_state.guia_gerado_md = guia_md
            else:
                st.session_state.guia_gerado_md = f"Não foi possível obter os dados detalhados para {nome_planta_guia}."
    
    st.markdown(st.session_state.guia_gerado_md, unsafe_allow_html=True)

    if ag_comercial:
        st.subheader(f"🛒 Onde Encontrar Sementes/Mudas de {nome_planta_guia}")
        col_lojas, col_online = st.columns(2)
        with col_lojas:
            if st.button("Buscar Lojas Próximas", key="btn_lojas_guia_main"):
                loc_data = st.session_state.dados_ambientais.get('localizacao')
                cidade_estado_usr = f"{loc_data.get('cidade', 'N/A')}, {loc_data.get('estado', '')}" if loc_data else "sua cidade"
                with st.spinner("Gerando link para Google Maps..."):
                    ag_comercial.encontrar_lojas_proximas_link(nome_planta_guia, cidade_estado_usr)
        with col_online:
            if st.button("Comprar Online", key="btn_online_guia_main"):
                 with st.spinner("Gerando link para Google Shopping..."):
                    ag_comercial.comprar_online_link(nome_planta_guia)
    
    if st.button("Ver outras sugestões", key="btn_voltar_sug_guia"):
        st.session_state.etapa_atual = "sugestoes"; st.session_state.planta_selecionada_guia = None
        st.session_state.guia_gerado_md = None; st.rerun() # CORRIGIDO

# --- Rodapé ---
st.sidebar.header("Sobre o Horta Inteligente")
st.sidebar.info("Seu assistente de IA para jardinagem. As informações ambientais são estimativas para demonstração.")
if st.sidebar.button("Começar Nova Consulta", key="sidebar_restart_main"):
    for key in st.session_state.keys(): # Limpa todo o session_state
        del st.session_state[key]
    st.rerun() # CORRIGIDO