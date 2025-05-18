# agentes/agente_localizador.py
import geopy.exc # Para tratamento de exceções geopy
# As funções como geocode_address_nominatim, get_simulated_average_weather, etc.
# serão importadas de utils.api_clients em app.py e usadas lá,
# ou o agente pode importá-las diretamente se utils.api_clients for auto-suficiente.
# Para este exemplo, assumiremos que as funções da Célula 2 do Colab estão em utils.api_clients
from utils.api_clients import (
    geocode_address_nominatim, 
    get_simulated_average_weather, 
    mock_api_dados_solo_regional
)
# mock_estimar_solo_regional e mock_estimar_clima_regional são chamadas por geocode_address_nominatim
# que está em utils.api_clients, então não precisam ser importadas aqui diretamente.


class AgenteLocalizadorAmbiental:
    def __init__(self):
        self.dados_localizacao_base = None
        self.dados_climaticos_atuais = None
        self.dados_solo_atuais = None
        print("AgenteLocalizadorAmbiental (Reformulado) instanciado.") # Mantenha prints para debug inicial

    def obter_localizacao_e_dados_ambientais_usuario(self, endereco_texto=None, app_nome_user_agent="MeuAppJardim/1.0"):
        print(f"\n--- {self.__class__.__name__}: Iniciando obtenção de localização e dados ambientais ---")
        if not endereco_texto:
            # Em Streamlit, o input virá da UI, não de input() aqui.
            # Este método será chamado com 'endereco_texto' já preenchido.
            print("🚨 [LOCALIZADOR] endereco_texto não fornecido ao método.")
            return None

        self.dados_localizacao_base = geocode_address_nominatim(endereco_texto, user_agent_app_name=app_nome_user_agent)

        if not self.dados_localizacao_base:
            print("🚨 [ERRO LOCALIZADOR] Não foi possível obter e geocodificar a localização do usuário.")
            return None

        lat = self.dados_localizacao_base['latitude']
        lon = self.dados_localizacao_base['longitude']
        cidade = self.dados_localizacao_base.get('cidade', 'Local Desconhecido')
        solo_base_estimado = self.dados_localizacao_base.get('solo_base_regiao', 'Não especificado')

        self.dados_climaticos_atuais = get_simulated_average_weather(lat, lon, cidade)
        self.dados_solo_atuais = mock_api_dados_solo_regional(lat, lon, cidade, solo_base_estimado)

        dados_consolidados = {
            "localizacao": self.dados_localizacao_base,
            "clima": self.dados_climaticos_atuais,
            "solo": self.dados_solo_atuais
        }

        if self.dados_climaticos_atuais and self.dados_solo_atuais:
             print(f"Dados ambientais (simulados/regionais) para {cidade} obtidos com sucesso.")
        else:
            print(f"⚠️ [AVISO LOCALIZADOR] Alguns dados ambientais para {cidade} podem não ter sido totalmente carregados.")
        return dados_consolidados

    def get_dados_ambientais_completos(self):
        if self.dados_localizacao_base and self.dados_climaticos_atuais and self.dados_solo_atuais:
            return { "localizacao": self.dados_localizacao_base, "clima": self.dados_climaticos_atuais, "solo": self.dados_solo_atuais }
        print("⚠️ [AVISO LOCALIZADOR] Dados ambientais incompletos ou não disponíveis no get_dados_ambientais_completos.")
        return None