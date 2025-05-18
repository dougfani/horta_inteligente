# agentes/agente_pesquisador.py
import json
from utils.api_clients import gerar_conteudo_com_gemini # Importa a função utilitária

class AgentePesquisadorPlantasGemini:
    def __init__(self, agente_estilizador_ref, gemini_model_inst, model_config_inst):
        self.agente_estilizador = agente_estilizador_ref
        self.gemini_model = gemini_model_inst
        self.model_config = model_config_inst
        self.cache_dados_plantas = {}
        print("AgentePesquisadorPlantasGemini (Prompt Reforçado v2) instanciado.")

    def obter_dados_detalhados_planta(self, nome_planta_popular, forcar_nova_busca=False):
        nome_planta_cache_key = nome_planta_popular.strip().lower()
        if not forcar_nova_busca and nome_planta_cache_key in self.cache_dados_plantas:
            print(f"Usando dados da planta '{nome_planta_popular}' do cache.")
            return self.cache_dados_plantas[nome_planta_cache_key]

        esquema_json = self.agente_estilizador.get_esquema_dados_planta()
        if not esquema_json:
            print(f"🚨 [PESQUISADOR] Esquema JSON não disponível. Tentando definir novamente...")
            esquema_json = self.agente_estilizador.definir_esquema_dados_planta(forcar_nova_definicao=True)
            if not esquema_json:
                 print(f"🚨 [PESQUISADOR] Ainda não foi possível obter o Esquema JSON. Abortando busca por '{nome_planta_popular}'.")
                 return None
        
        esquema_str_para_prompt = json.dumps(esquema_json, indent=2, ensure_ascii=False)

        # PROMPT ATUALIZADO E MAIS DETALHADO NAS INSTRUÇÕES:
        prompt_dados_planta = f"""
        Você é um especialista agronômico para jardinagem caseira no Brasil, focado em fornecer informações PRÁTICAS e COMPLETAS.
        Sua tarefa é fornecer informações detalhadas sobre a planta comestível: "{nome_planta_popular}".

        Preencha o seguinte esquema JSON com os dados da planta. É ABSOLUTAMENTE CRUCIAL que você tente preencher TODOS os campos da forma mais útil possível.
        Para campos com valores enumerados (enum), ESCOLHA E PREENCHA COM UM DOS VALORES VÁLIDOS FORNECIDOS NO ESQUEMA.
        NÃO use "N/A", "Não especificado" ou deixe campos importantes em branco, especialmente:
        - `cultivo_info.dificuldade`: Use "Fácil", "Médio", ou "Difícil". Se incerto, estime com base na necessidade de cuidados.
        - `cultivo_info.climas_ideais_texto_descritivo`: Forneça uma descrição útil, como "Prefere climas amenos (15-25°C), tolera subtropical, sensível a geadas" ou "Adaptável a climas tropicais e subtropicais quentes".
        - `cultivo_info.cultivo_em_vasos.adequacao`: Use "Excelente", "Bom", "Possível com cuidados", ou "Não recomendado". Se "Não especificado" for a única opção, explique brevemente em `observacoes_cultivo_vaso`.
        - `cultivo_info.necessidades_fundamentais_solo.dicas_adaptacao_solos_comuns`: Dê dicas práticas para melhorar solos arenosos e argilosos para esta planta.
        - `cultivo_info.espaco_necessario_descricao_geral`: Escolha uma das opções do enum.
        - `cultivo_info.tempo_dedicacao_semanal_estimado`: Escolha uma das opções do enum.

        Se uma informação exata não for universalmente conhecida, forneça a faixa mais comum ou uma estimativa informada.

        **Esquema JSON a ser preenchido:**
        ```json
        {esquema_str_para_prompt}
        ```

        Responda APENAS com o objeto JSON preenchido. Sem explicações fora do JSON.
        Certifique-se que o campo `nome_popular` na sua resposta seja "{nome_planta_popular}".
        """
        print(f"Buscando dados detalhados para '{nome_planta_popular}' via Gemini (prompt super reforçado)...")
        dados_planta_raw = gerar_conteudo_com_gemini(
            self.gemini_model,
            self.model_config,
            prompt_dados_planta, 
            solicitar_json=True
        )

        if isinstance(dados_planta_raw, dict):
            nome_popular_retornado = dados_planta_raw.get('nome_popular','').strip()
            if not nome_popular_retornado:
                dados_planta_raw['nome_popular'] = nome_planta_popular
            elif nome_popular_retornado.lower() != nome_planta_cache_key:
                 print(f"⚠️ [AVISO PESQUISADOR] Gemini retornou nome '{nome_popular_retornado}' para '{nome_planta_popular}'. Padronizando.")
                 dados_planta_raw['nome_popular_gemini'] = nome_popular_retornado
                 dados_planta_raw['nome_popular'] = nome_planta_popular     
            
            # Fallbacks mais robustos se Gemini ainda não preencher campos críticos
            cult_info = dados_planta_raw.setdefault('cultivo_info', {}) # Garante que cultivo_info existe
            if not cult_info.get('dificuldade'):
                cult_info['dificuldade'] = "Médio (verifique guia)" 
            if not cult_info.get('climas_ideais_texto_descritivo'):
                cult_info['climas_ideais_texto_descritivo'] = "Verificar adaptabilidade ao clima local no guia."
            
            vasos_info = cult_info.setdefault('cultivo_em_vasos', {}) # Garante que cultivo_em_vasos existe
            if not vasos_info.get('adequacao'):
                vasos_info['adequacao'] = "Verificar no guia"
            
            if not cult_info.get('espaco_necessario_descricao_geral'):
                cult_info['espaco_necessario_descricao_geral'] = "Verificar porte no guia"
            if not cult_info.get('tempo_dedicacao_semanal_estimado'):
                cult_info['tempo_dedicacao_semanal_estimado'] = "Verificar no guia"


            print(f"✅ Dados detalhados para '{dados_planta_raw.get('nome_popular')}' recebidos e parseados.")
            self.cache_dados_plantas[nome_planta_cache_key] = dados_planta_raw
            return dados_planta_raw
        else:
            print(f"🚨 [ERRO PESQUISADOR] Falha ao obter dados estruturados para '{nome_planta_popular}'.")
            print(f"   Resposta do Gemini:\n{dados_planta_raw}")
            return None