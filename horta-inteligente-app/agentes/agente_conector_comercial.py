# agentes/agente_conector_comercial.py
# from IPython.display import HTML, display # Em Streamlit, usaremos st.markdown
# As funções gerar_link_Maps_lojas e gerar_link_google_shopping
# virão de utils.api_clients e serão chamadas pelo app.py (Streamlit)
# Este agente pode então ser simplificado ou sua lógica movida para o app.py
# Por enquanto, vamos mantê-lo, mas app.py fará a chamada direta às funções de link.
# Ou, melhor, app.py chama os métodos deste agente, e este agente usa st.markdown.

import streamlit as st # Para usar st.markdown para exibir os links
from utils.api_clients import gerar_link_Maps_lojas, gerar_link_google_shopping

class AgenteConectorComercialPlantas:
    def __init__(self):
        print("AgenteConectorComercialPlantas (Reformulado para Streamlit) instanciado.")

    def encontrar_lojas_proximas_link(self, nome_planta, cidade_usuario_estado_str):
        print(f"\n--- {self.__class__.__name__}: Gerando link para lojas de '{nome_planta}' ---")
        cidade_para_busca = "sua localidade" 
        if isinstance(cidade_usuario_estado_str, str) and cidade_usuario_estado_str.strip():
            cidade_para_busca = cidade_usuario_estado_str
        else:
            print(f"[AVISO CONECTOR COMERCIAL] String de cidade/estado inválida ('{cidade_usuario_estado_str}').")

        link_gmaps = gerar_link_Maps_lojas(nome_planta, cidade_para_busca)
        st.markdown(f"<p>Para encontrar lojas físicas de '{nome_planta}' perto de {cidade_para_busca}, <a href='{link_gmaps}' target='_blank'>clique aqui para buscar no Google Maps</a>.</p>", unsafe_allow_html=True)
        return link_gmaps

    def comprar_online_link(self, nome_planta):
        print(f"\n--- {self.__class__.__name__}: Gerando link para comprar '{nome_planta}' online ---")
        link_gshopping = gerar_link_google_shopping(nome_planta)
        st.markdown(f"<p>Para comprar sementes/mudas de '{nome_planta}' online, <a href='{link_gshopping}' target='_blank'>clique aqui para buscar no Google Shopping</a>.</p>", unsafe_allow_html=True)
        return link_gshopping