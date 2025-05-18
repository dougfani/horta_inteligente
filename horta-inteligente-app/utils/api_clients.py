# utils/api_clients.py
import json
import random
import time
from datetime import datetime # Se alguma função utilitária precisar
import requests
from urllib.parse import quote
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import geopy.exc

# Para Gemini
import google.generativeai as genai

# --- Configurações Globais do Gemini (usadas por gerar_conteudo_com_gemini) ---
# Essas podem ser passadas como argumento ou definidas aqui se utils/api_clients.py
# também lida com a instanciação do modelo.
# Na nossa estrutura atual, app.py instancia gemini_model_global_instance e o passa para esta função.
# OU, como fizemos no Colab, 'gemini_model' pode ser uma global neste módulo,
# setada por app.py.

gemini_model = None # Será setado por app.py
MODEL_CONFIG_UTIL = None # Será setado por app.py
# SAFETY_SETTINGS_UTIL = None # Será setado por app.py (embora não usado diretamente por gerar_conteudo_com_gemini)

def set_gemini_model_and_config_for_utils(model_instance, model_config_dict):
    """Função para app.py chamar e setar o modelo e config para este módulo."""
    global gemini_model, MODEL_CONFIG_UTIL
    gemini_model = model_instance
    MODEL_CONFIG_UTIL = model_config_dict
    if gemini_model and MODEL_CONFIG_UTIL:
        print("✅ Modelo e Config do Gemini setados para utils.api_clients.")
    else:
        print("⚠️ Falha ao setar modelo/config do Gemini para utils.api_clients.")


# Copie as funções:
# geocode_address_nominatim (e suas dependências mock_estimar_solo_regional, mock_estimar_clima_regional)
# get_simulated_average_weather
# mock_api_dados_solo_regional
# gerar_link_Maps_lojas
# gerar_link_google_shopping
# gerar_conteudo_com_gemini (a versão com correção de SyntaxError e tentativa de auto-correção de JSON)

# --- Função de Geocodificação ---
def mock_estimar_clima_regional(latitude): # Usada por geocode_address_nominatim
    clima_regional = "Tropical" 
    try:
        if not isinstance(latitude, (int, float)): latitude = -15.78 # Default se None
        if latitude < -25: clima_regional = "Subtropical"
        elif -25 <= latitude < -15: clima_regional = "Tropical de Altitude"
        elif -15 <= latitude < -5: clima_regional = "Tropical"
        else: clima_regional = "Equatorial"
    except TypeError: pass
    return clima_regional

def mock_estimar_solo_regional(latitude, longitude, cidade_nome="Local"): # Usada por geocode_address_nominatim
    tipos_solo = ["Latossolo", "Argissolo", "Cambissolo", "Neossolo"]
    try:
        if not isinstance(latitude, (int, float)): latitude = -15.78 # Default se None
        if latitude < -23: tipos_solo = ["Argissolo", "Latossolo Vermelho", "Cambissolo", "Neossolo Litólico"]
        elif -23 <= latitude < -15: tipos_solo = ["Latossolo Vermelho-Amarelo", "Neossolo Quartzarênico", "Cambissolo Húmico"]
        elif -15 <= latitude < -5: tipos_solo = ["Argissolo Amarelo", "Planossolo Nátrico", "Neossolo Flúvico", "Latossolo Bruno"]
        else: tipos_solo = ["Latossolo Amarelo Distrófico", "Argissolo Acinzentado", "Gleissolo Tiomórfico", "Plintossolo Pétrico"]
    except TypeError: pass
    return random.choice(tipos_solo)

def geocode_address_nominatim(address_text, user_agent_app_name="MeuAppDeJardinagemDemo/1.0"):
    if not address_text: print("[GEOCODING] Endereço não fornecido."); return None
    try:
        print(f"[NOMINATIM] Geocodificando: {address_text}...")
        geolocator = Nominatim(user_agent=user_agent_app_name)
        geocode_with_delay = RateLimiter(geolocator.geocode, min_delay_seconds=1.1, max_retries=2, error_wait_seconds=5.0)
        location = geocode_with_delay(address_text, country_codes="BR", addressdetails=True, exactly_one=True, timeout=10)
        if location and location.raw:
            raw_data = location.raw; address_details = raw_data.get('address', {})
            city_keys = ['city', 'town', 'village', 'county', 'municipality', 'suburb']
            city = next((address_details.get(key) for key in city_keys if address_details.get(key)), None)
            if not city and 'city_district' in address_details: city = address_details.get('city_district')
            if not city: city = address_details.get('region', 'Desconhecida') if 'region' in address_details else 'Desconhecida'
            state = address_details.get('state', 'Desconhecido')
            lat_val, lon_val = float(raw_data["lat"]), float(raw_data["lon"])
            geo_data = {
                "latitude": lat_val, "longitude": lon_val,
                "endereco_formatado": raw_data.get("display_name", address_text),
                "cidade": city, "estado": state,
                "solo_base_regiao": mock_estimar_solo_regional(lat_val, lon_val, city), # Chamada à função local
                "clima_base_regiao": mock_estimar_clima_regional(lat_val) # Chamada à função local
            }
            print(f"[NOMINATIM] Localização: {geo_data['endereco_formatado']} ({geo_data['latitude']:.4f}, {geo_data['longitude']:.4f})")
            return geo_data
        else: print(f"[NOMINATIM] Não foi possível geocodificar '{address_text}'."); return None
    except geopy.exc.GeocoderTimedOut: print(f"[NOMINATIM] Timeout em '{address_text}'."); return None
    except geopy.exc.GeocoderUnavailable as e: print(f"[NOMINATIM] Serviço indisponível: {e}"); return None
    except Exception as e: print(f"[NOMINATIM] Erro em '{address_text}': {type(e).__name__} - {e}"); return None

# --- Funções de Simulação Ambiental ---
def get_simulated_average_weather(latitude, longitude, cidade_nome="Local"):
    # (Copie a função completa da Célula 2 do Colab, como na minha resposta anterior de app.py)
    print(f"[CLIMA SIMULADO] Gerando dados climáticos médios para {cidade_nome} ({latitude:.2f}, {longitude:.2f})...")
    temp_media, umidade_media, condicao_predominante, clima_regional = 22, 70, "Parcialmente Nublado", "Tropical" 
    try:
        if not isinstance(latitude, (int, float)): latitude = -15.78 
        if latitude < -25: temp_media, umidade_media, condicao_predominante, clima_regional = 18, 75, "Parcialmente Nublado, variações sazonais", "Subtropical"
        elif -25 <= latitude < -15: temp_media, umidade_media, condicao_predominante, clima_regional = 22, 70, "Ensolarado com períodos nublados", "Tropical de Altitude"
        elif -15 <= latitude < -5: temp_media, umidade_media, condicao_predominante, clima_regional = 26, 65, "Quente e ensolarado", "Tropical"
        else: temp_media, umidade_media, condicao_predominante, clima_regional = 27, 85, "Quente e úmido, chuvas frequentes", "Equatorial"
    except TypeError: print("[CLIMA SIMULADO] Latitude inválida. Usando defaults."); latitude = -15.78
    temperatura = round(random.uniform(temp_media - 2, temp_media + 2), 1)
    umidade = random.randint(max(20, umidade_media - 15), min(100, umidade_media + 15))
    weather_info = {"cidade": cidade_nome, "temperatura_atual_c": temperatura, "umidade_percentual": umidade, "condicao_atual": condicao_predominante, "clima_regional_estimado": clima_regional, "observacao": "Dados climáticos médios simulados."}
    print(f"[CLIMA SIMULADO] Dados: {weather_info['condicao_atual']}, Temp. Média: {temperatura}°C, Clima Regional: {clima_regional}")
    return weather_info

def mock_api_dados_solo_regional(latitude, longitude, cidade_nome, tipo_solo_base):
    # (Copie a função completa da Célula 2 do Colab)
    print(f"[MOCK SOLO REGIONAL] Gerando dados de solo para {cidade_nome} (base: {tipo_solo_base})...")
    ph_ranges = {"Latossolo": (4.5, 6.0), "Argissolo": (5.0, 6.5), "Cambissolo": (5.5, 7.0),"Neossolo": (5.0, 7.5), "Planossolo": (4.0, 6.0), "Gleissolo": (5.0, 7.0),"Latossolo Vermelho": (5.0,6.0), "Latossolo Vermelho-Amarelo": (4.5, 5.5),"Neossolo Quartzarênico": (4.0,5.5), "Argissolo Amarelo": (4.5, 6.0),"Neossolo Litólico": (6.0, 7.5), "Latossolo Amarelo Distrófico": (4.0, 5.0),"Cambissolo Húmico": (5.0, 6.0), "Planossolo Nátrico": (6.5, 8.0),"Neossolo Flúvico": (5.5, 7.5), "Latossolo Bruno": (5.0, 6.5),"Argissolo Acinzentado": (5.5, 7.0), "Gleissolo Tiomórfico": (3.5, 5.0),"Plintossolo Pétrico": (4.0, 5.5)}
    ph_base_min, ph_base_max = ph_ranges.get(tipo_solo_base, (5.0, 7.0))
    dados_solo = {"tipo_solo_predominante": tipo_solo_base, "ph_estimado": round(random.uniform(ph_base_min, ph_base_max), 1), "materia_organica_percentual": round(random.uniform(0.5, 4.5), 1), "drenagem": random.choice(["Boa", "Moderada", "Imperfeita"]), "observacoes": f"Estimativa de solo ({tipo_solo_base}) para {cidade_nome}. Recomenda-se análise."}
    print(f"[MOCK SOLO REGIONAL] Dados: Solo {dados_solo['tipo_solo_predominante']}, pH {dados_solo['ph_estimado']}")
    return dados_solo

# --- Funções de Geração de Link ---
def gerar_link_Maps_lojas(nome_planta, cidade_usuario_estado):
    # (Copie a função completa da Célula 2 do Colab)
    query_base = f"viveiros OR loja jardinagem OR sementes {quote(nome_planta)} em {quote(cidade_usuario_estado)}"
    link = f"https://www.google.com/maps/search/?api=1&query={query_base}"
    print(f"[LINK GMAPS] Link para lojas de '{nome_planta}' em '{cidade_usuario_estado}': {link}")
    return link

def gerar_link_google_shopping(nome_planta):
    # (Copie a função completa da Célula 2 do Colab)
    query = f"sementes {quote(nome_planta)} OR mudas {quote(nome_planta)}"
    link = f"https://www.google.com/search?tbm=shop&q={query}&hl=pt-br&gl=br"
    print(f"[LINK GSHOPPING] Link para comprar '{nome_planta}': {link}")
    return link

# --- Função de Interação com Gemini ---
def gerar_conteudo_com_gemini(
    modelo_gemini_usar,       # <--- NOVO PARÂMETRO
    config_modelo_usar,       # <--- NOVO PARÂMETRO
    prompt_texto, 
    solicitar_json=False
):
    """Função genérica para enviar um prompt ao Gemini e obter a resposta."""
    if not modelo_gemini_usar:
        print("🚨 [UTIL:GERAR_CONTEUDO] Instância do Modelo Gemini não fornecida.")
        # Em um app Streamlit, você pode querer usar st.error() ou logar de forma diferente
        return None
    if not config_modelo_usar:
        print("🚨 [UTIL:GERAR_CONTEUDO] Configuração do Modelo Gemini não fornecida.")
        return None
    if not prompt_texto:
        print("🚨 [UTIL:GERAR_CONTEUDO] Prompt vazio fornecido.")
        return None

    print(f"\n🔄 Enviando prompt para o Gemini (JSON solicitado: {solicitar_json}, MimeType pedido: text/plain)... Aguarde...")
    try:
        prompt_final = prompt_texto
        if solicitar_json and not ("responda em formato JSON" in prompt_texto.lower() or "APENAS o objeto JSON" in prompt_texto.upper()):
             prompt_final += "\n\nATENÇÃO: Sua resposta DEVE ser um objeto JSON válido e nada mais."

        # Usa a configuração do modelo passada como argumento
        current_model_config = genai.types.GenerationConfig(
            temperature=config_modelo_usar["temperature"],
            top_p=config_modelo_usar["top_p"],
            top_k=config_modelo_usar["top_k"],
            response_mime_type="text/plain" 
        )
        # Usa a instância do modelo passada como argumento
        response = modelo_gemini_usar.generate_content(prompt_final, generation_config=current_model_config)

        if not response.candidates:
            block_reason_str = "Não especificado"; safety_ratings_str_list = ["Nenhuma info de safety rating."]
            if response.prompt_feedback:
                block_reason_str = response.prompt_feedback.block_reason if response.prompt_feedback.block_reason else "Não bloqueado, mas sem candidatos."
                if response.prompt_feedback.safety_ratings: 
                    safety_ratings_str_list = [f"  - Cat: {r.category}, Prob: {r.probability.name}" for r in response.prompt_feedback.safety_ratings]
            print(f"🚨 [AVISO GEMINI UTIL] Resposta sem candidatos. Razão: {block_reason_str}"); [print(s) for s in safety_ratings_str_list]
            return None

        resposta_texto = response.text
        if solicitar_json:
            try:
                texto_limpo_para_json = resposta_texto.strip()
                if texto_limpo_para_json.startswith("```json"): texto_limpo_para_json = texto_limpo_para_json[7:-3].strip() if texto_limpo_para_json.endswith("```") else texto_limpo_para_json[7:].strip()
                elif texto_limpo_para_json.startswith("```"): texto_limpo_para_json = texto_limpo_para_json[3:-3].strip() if texto_limpo_para_json.endswith("```") else texto_limpo_para_json[3:].strip()
                texto_limpo_para_json = texto_limpo_para_json.strip()
                if not texto_limpo_para_json: print("🚨 [ERRO GEMINI UTIL] Resposta JSON vazia pós-limpeza."); return None

                print(f"   [UTIL] Tentando parsear JSON. Tamanho: {len(texto_limpo_para_json)}. Fim (repr): {repr(texto_limpo_para_json[-70:])}")
                try: dados_json = json.loads(texto_limpo_para_json)
                except json.JSONDecodeError as e_initial:
                    if "Extra data" in e_initial.msg and texto_limpo_para_json.endswith("}") and e_initial.pos == len(texto_limpo_para_json) -1 :
                        print("   ⚠️ [UTIL] Erro 'Extra data' no último char. Tentando remover e re-parsear..."); texto_tentativa_2 = texto_limpo_para_json[:-1]
                        try: dados_json = json.loads(texto_tentativa_2); print("   ✅ [UTIL] Parse OK após remover char final.")
                        except json.JSONDecodeError as e_secondary: print(f"   🚨 [UTIL] Falha no re-parse: {e_secondary}"); raise e_initial
                    else: raise e_initial
                print("✅ [UTIL] Resposta JSON do Gemini parseada."); return dados_json
            except json.JSONDecodeError as e:
                print(f"🚨 [ERRO GEMINI UTIL] Falha ao parsear JSON: {e}"); print(f"   Detalhes: {e.msg}, Posição: {e.pos}, Trecho: '{e.doc[max(0,e.pos-20):e.pos+20]}'")
                return None # Não salvar arquivo aqui, app.py ou agente pode logar se quiser
            except Exception as e_gen: print(f"🚨 [ERRO GEMINI UTIL] Erro inesperado no JSON: {e_gen}"); return None
        else: 
            print("✅ [UTIL] Resposta textual do Gemini."); return resposta_texto
    except Exception as e: 
        print(f"🚨 [ERRO FATAL GEMINI UTIL] Erro ao gerar conteúdo: {e}")
        # Evitar imprimir e.response.text diretamente aqui, pode ser muito longo ou conter info sensível
        if hasattr(e, 'response'): print(f"   Erro da API Gemini (status code pode estar em e.response).")
        return None

# DB_PLANTAS (opcional, se você quiser manter o mock para algum fallback ou teste rápido)
DB_PLANTAS = {
    "Alface": { "nome_cientifico": "Lactuca sativa", "dificuldade_cultivo": "Fácil", 
                "climas_ideais_texto_descritivo": "Prefere climas amenos, entre 15°C e 25°C. Tolera subtropical. Sensível a calor excessivo e geadas fortes.",
                "cultivo_em_vasos": {"adequacao": "Excelente", "tamanho_minimo_vaso_sugerido_litros": 3, "tipo_substrato_recomendado_vaso": "Substrato leve, rico em matéria orgânica e bem drenado."}
                # Adicione mais campos conforme o novo esquema para testes
    },
    # ... (outras plantas do mock se desejar)
}

print("utils.api_clients carregado.")