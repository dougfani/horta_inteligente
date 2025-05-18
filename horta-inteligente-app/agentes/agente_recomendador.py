# agentes/agente_recomendador.py
import random
import time
import json
from utils.api_clients import gerar_conteudo_com_gemini
# Importe o novo agente redator
from agentes.agente_redator_ia import AgenteRedatorConteudoIA

class AgenteRecomendadorAgronomoVirtual:
    def __init__(self, agente_pesquisador_plantas, agente_estilizador_ref, 
                 gemini_model_inst, model_config_inst, 
                 agente_redator_inst): # <--- NOVO: Recebe o redator
        self.agente_pesquisador = agente_pesquisador_plantas
        self.agente_estilizador = agente_estilizador_ref 
        self.gemini_model = gemini_model_inst
        self.model_config = model_config_inst
        self.agente_redator = agente_redator_inst # <--- NOVO: Armazena o redator
        print("AgenteRecomendadorAgronomoVirtual (com Redator) instanciado.")

    # ... (métodos _sugerir_plantas_candidatas_por_tipo e _get_regiao_geografica_aproximada permanecem os mesmos) ...
    def _sugerir_plantas_candidatas_por_tipo(self, tipos_alimento_preferidos, max_candidatas_por_tipo=3):
        # (Copie a versão completa e funcional deste método da sua última célula 5 funcional)
        # ...
        if not self.gemini_model: print("🚨 [RECOMENDADOR:_sugerir_candidatas] Modelo Gemini não disponível."); return []
        if not tipos_alimento_preferidos: tipos_alimento_preferidos = ["hortaliças de fácil cultivo", "frutas para vasos", "ervas aromáticas comuns"]
        nomes_plantas_candidatas_set = set()
        for tipo_alimento in tipos_alimento_preferidos:
            prompt_candidatas = f"Liste {max_candidatas_por_tipo} nomes populares de plantas comestíveis da categoria '{tipo_alimento}' adequadas para hortas caseiras no Brasil, incluindo opções fáceis e para pequenos espaços. Responda APENAS com nomes separados por vírgula."
            # print(f"Sugerindo plantas candidatas para o tipo: '{tipo_alimento}' via Gemini...")
            resposta_nomes = gerar_conteudo_com_gemini(self.gemini_model, self.model_config, prompt_candidatas, solicitar_json=False)
            if resposta_nomes:
                nomes_individuais = [nome.strip().capitalize() for nome in resposta_nomes.split(',') if nome.strip()]
                nomes_plantas_candidatas_set.update(nomes_individuais); # print(f"  Candidatas para '{tipo_alimento}': {nomes_individuais}")
            # else: print(f"  Não foi possível obter candidatas para '{tipo_alimento}'.")
            time.sleep(0.1)
            print(f"    Aguardando após buscar candidatas para '{tipo_alimento}'...")
            time.sleep(5) # Delay aqui também se estiver chamando para múltiplos tipos
        lista_final_candidatas = list(nomes_plantas_candidatas_set)
        max_total_candidatas_para_detalhe = 5 
        if len(lista_final_candidatas) > max_total_candidatas_para_detalhe:
            # print(f"Limitando análise detalhada a {max_total_candidatas_para_detalhe} candidatas aleatórias de {len(lista_final_candidatas)}.")
            lista_final_candidatas = random.sample(lista_final_candidatas, max_total_candidatas_para_detalhe)
        # print(f"Lista final de plantas candidatas para análise detalhada: {lista_final_candidatas}")
        return lista_final_candidatas

    def _get_regiao_geografica_aproximada(self, latitude):
        if not isinstance(latitude, (int,float)): return "Não Determinada"
        if latitude < -20: return "Sul/Sudeste"
        elif -20 <= latitude < -10: return "Centro-Oeste/Sudeste (parte)/Nordeste (parte)"
        elif -10 <= latitude < 0: return "Nordeste (maioria)/Norte (parte)"
        elif latitude >= 0 : return "Norte (maioria)"
        else: return "Região não identificada"


    def _avaliar_compatibilidade_planta(self, info_planta_json, dados_ambientais, preferencias_usuario):
        if not info_planta_json or not isinstance(info_planta_json, dict): 
            return 0, ["Dados da planta inválidos."], []
        
        score = 1.0  
        justificativas_brutas = [] # Armazena fatos, não frases finais
        pontos_atencao_brutos = [] # Armazena fatos, não frases finais

        cultivo_info = info_planta_json.get('cultivo_info', {})
        nome_planta = info_planta_json.get('nome_popular', 'Esta planta')

        # 1. Clima
        clima_local_estimado = dados_ambientais.get('clima', {}).get('clima_regional_estimado', 'Não informado')
        climas_ideais_desc_planta = cultivo_info.get('climas_ideais_texto_descritivo', '').lower()
        if "verificar adaptabilidade" in climas_ideais_desc_planta or not climas_ideais_desc_planta.strip():
            pontos_atencao_brutos.append({"tipo": "clima_incerto", "planta_clima": "Não detalhado", "local_clima": clima_local_estimado})
            score *= 0.85 
        elif clima_local_estimado != 'Não informado':
            # ... (lógica de compatibilidade climática como antes, mas em vez de append em 'pontos_atencao',
            #      armazene os fatos em 'pontos_atencao_brutos' ou 'justificativas_brutas')
            # Exemplo simplificado:
            if clima_local_estimado.lower() in climas_ideais_desc_planta or "ampla adaptabilidade" in climas_ideais_desc_planta:
                justificativas_brutas.append({"tipo": "clima_ok", "planta_clima": cultivo_info.get('climas_ideais_texto_descritivo'), "local_clima": clima_local_estimado})
            else:
                score *= 0.7; pontos_atencao_brutos.append({"tipo": "clima_desafio", "planta_clima": cultivo_info.get('climas_ideais_texto_descritivo'), "local_clima": clima_local_estimado})
        
        # 2. Método de Cultivo e Solo
        metodo_cultivo_usr = preferencias_usuario.get('metodo_cultivo_predominante', 'misto_vaso_solo_pequeno')
        cultivo_vasos_info = cultivo_info.get('cultivo_em_vasos', {})
        adequacao_vaso_planta = cultivo_vasos_info.get('adequacao', 'Verificar no guia').lower()
        if "vaso" in metodo_cultivo_usr:
            if adequacao_vaso_planta in ["excelente", "bom"]:
                justificativas_brutas.append({"tipo": "vaso_ok", "planta_vaso_adequacao": adequacao_vaso_planta, "user_pref": "vasos"})
            elif adequacao_vaso_planta == "possível com cuidados":
                score *= 0.90; justificativas_brutas.append({"tipo": "vaso_ok_cuidados", "planta_vaso_adequacao": adequacao_vaso_planta, "user_pref": "vasos"})
            else: # Não recomendado ou verificar
                if metodo_cultivo_usr in ["vaso_pequeno", "vaso_medio"]: score *= 0.5
                else: score *= 0.75
                pontos_atencao_brutos.append({"tipo": "vaso_nao_ideal", "planta_vaso_adequacao": adequacao_vaso_planta, "user_pref": "vasos"})

        # 3. Espaço
        espaco_planta_desc = cultivo_info.get('espaco_necessario_descricao_geral', 'Verificar porte no guia').lower()
        espaco_usuario_str = preferencias_usuario.get("texto_opcao_espaco_metodo", "") # Usar o texto da opção do usuário
        if "verificar porte" not in espaco_planta_desc:
            if ("<1m²" in espaco_usuario_str and not ("vasos pequenos" in espaco_planta_desc or "compacta" in espaco_planta_desc)):
                score *= 0.6; pontos_atencao_brutos.append({"tipo": "espaco_limitado_pequeno", "planta_espaco": espaco_planta_desc, "user_espaco": espaco_usuario_str})
            elif ("1-3m²" in espaco_usuario_str and ("vigoroso" in espaco_planta_desc or "espaço amplo" in espaco_planta_desc or "canteiro grande" in espaco_planta_desc)):
                score *= 0.75; pontos_atencao_brutos.append({"tipo": "espaco_limitado_medio", "planta_espaco": espaco_planta_desc, "user_espaco": espaco_usuario_str})
            else:
                justificativas_brutas.append({"tipo": "espaco_ok", "planta_espaco": espaco_planta_desc, "user_espaco": espaco_usuario_str})
        else: score *= 0.95

        # 4. Tempo de Dedicação (similarmente, coletar fatos)
        tempo_planta_str = cultivo_info.get('tempo_dedicacao_semanal_estimado', 'Verificar no guia').lower()
        tempo_usuario_str = preferencias_usuario.get("tempo_dedicacao_semanal_texto", "")
        if "verificar no guia" not in tempo_planta_str and tempo_planta_str and tempo_usuario_str: # Checagem mais robusta
            tempo_planta_val = float(tempo_planta_str.split('-')[0].replace('<','').replace('>','').replace('h','').strip()) if tempo_planta_str[0].isdigit() or tempo_planta_str[0] == '<' else 0
            tempo_user_val = float(tempo_usuario_str.split('-')[0].replace('<','').replace('>','').replace('h','').strip()) if tempo_usuario_str[0].isdigit() or tempo_usuario_str[0] == '<' else 0
            if tempo_planta_val > tempo_user_val :
                score *= 0.70; pontos_atencao_brutos.append({"tipo": "tempo_insuficiente", "planta_tempo": tempo_planta_str, "user_tempo": tempo_usuario_str})
            else:
                justificativas_brutas.append({"tipo": "tempo_ok", "planta_tempo": tempo_planta_str, "user_tempo": tempo_usuario_str})
        else: score *=0.95
        
        # 5. Dificuldade
        dificuldade_planta = cultivo_info.get('dificuldade', 'Médio (verifique guia)').lower()
        if "difícil" in dificuldade_planta: score *= 0.80
        elif "fácil" in dificuldade_planta: justificativas_brutas.append({"tipo": "dificuldade_facil", "planta_dificuldade": dificuldade_planta})
        
        final_score = max(0.20, min(1, score))

        # GERAR TEXTOS FINAIS COM O REDATOR
        textos_justificativas = []
        for j_bruto in justificativas_brutas:
            # O redator pode precisar de mais contexto ou podemos simplificar
            texto = self.agente_redator.gerar_texto_justificativa_sugestao(nome_planta, j_bruto["tipo"], j_bruto.get("planta_info", "Característica da planta"), j_bruto.get("user_info", "Sua preferência/condição"))
            if texto: textos_justificativas.append(texto)

        textos_pontos_atencao = []
        for pa_bruto in pontos_atencao_brutos:
            texto = self.agente_redator.gerar_texto_ponto_atencao(nome_planta, pa_bruto["tipo"], pa_bruto.get("planta_info", "Característica da planta"), pa_bruto.get("user_info", "Sua preferência/condição"))
            if texto: textos_pontos_atencao.append(texto)
            
        if not textos_pontos_atencao and final_score < 0.75 and final_score > 0.3: # Limiar ajustado
             texto_generico = self.agente_redator.gerar_texto_ponto_atencao(nome_planta, "score_moderado_generico", "Score de compatibilidade não é o mais alto", "Avalie se é a melhor opção ou se requer cuidados extras não listados.")
             if texto_generico: textos_pontos_atencao.append(texto_generico)

        return final_score, textos_justificativas, textos_pontos_atencao

    def gerar_sugestoes_otimizadas(self, preferencias_usuario, dados_ambientais, max_sugestoes_finais=3):
        print(f"\n--- {self.__class__.__name__}: Gerando sugestões (Defensive nomes_candidatas) ---")
        
        # Inicialização defensiva da variável
        nomes_candidatas = []

        if not self.gemini_model: 
            print("🚨 [RECOMENDADOR:gerar_sugestoes] Modelo Gemini não disponível. Nenhuma sugestão será gerada.")
            return [] # Retorno imediato

        if not preferencias_usuario or not preferencias_usuario.get("tipos_alimento_preferidos"):
            print("⚠️ [AVISO RECOM] Tipos de alimento preferidos não especificados pelo usuário. Nenhuma sugestão será gerada.")
            return [] # Retorno imediato

        # Obter plantas candidatas
        try:
            nomes_candidatas = self._sugerir_plantas_candidatas_por_tipo(
                preferencias_usuario["tipos_alimento_preferidos"]
            )
        except Exception as e:
            print(f"🚨 [ERRO RECOM] Exceção ao tentar sugerir plantas candidatas: {e}")
            return [] # Retorno imediato em caso de erro aqui

        if not nomes_candidatas: # Checa se a lista está vazia ou se _sugerir_plantas_candidatas_por_tipo retornou []
            print("Nenhuma planta candidata foi sugerida pelo Gemini para os tipos de alimento escolhidos.")
            return [] # Retorno imediato

        # Neste ponto, nomes_candidatas DEVE ser uma lista (vazia ou não, mas definida)
        # A linha que deu o erro anteriormente:
        print(f"\nAvaliando {len(nomes_candidatas)} plantas candidatas em detalhe:") 
        
        sugestoes_processadas = []
        for nome_planta_cand in nomes_candidatas:
            print(f"  ➡️  Avaliando: {nome_planta_cand} (Chamando AgentePesquisador)...")
            dados_planta_json = self.agente_pesquisador.obter_dados_detalhados_planta(nome_planta_cand)
            
            print(f"    Aguardando para respeitar limite da API...") # Mantendo o delay
            time.sleep(5) 

            if not dados_planta_json:
                print(f"    ❌ Não foi possível obter dados detalhados para '{nome_planta_cand}'. Pulando."); continue

            nome_popular_real = dados_planta_json.get('nome_popular', nome_planta_cand)
            score_compat, justificativas, pontos_atencao = self._avaliar_compatibilidade_planta(
                dados_planta_json, dados_ambientais, preferencias_usuario
            )
            
            justificativas = list(dict.fromkeys(j for j in justificativas if j)) 
            pontos_atencao = list(dict.fromkeys(p for p in pontos_atencao if p))

            print(f"    Score para '{nome_popular_real}': {score_compat:.2f}")
            if justificativas: print(f"      👍 Pontos positivos: {'; '.join(justificativas)}")
            if pontos_atencao: print(f"      ⚠️ Pontos de atenção: {'; '.join(pontos_atencao)}")

            if score_compat >= 0.35: 
                cultivo_info = dados_planta_json.get('cultivo_info', {})
                dificuldade_raw = cultivo_info.get('dificuldade', 'Verificar no guia')
                dificuldade_final = dificuldade_raw.split('(')[0].strip() if '(' in dificuldade_raw else dificuldade_raw
                if not dificuldade_final or "verificar" in dificuldade_final.lower(): 
                    dificuldade_final = "Detalhes no guia"

                sugestoes_processadas.append({
                    "nome_popular": nome_popular_real,
                    "dificuldade_cultivo": dificuldade_final,
                    "score_compatibilidade": score_compat,
                    "justificativas": justificativas,
                    "pontos_atencao": pontos_atencao,
                    "_dados_completos_json": dados_planta_json
                })
                print(f"    ✅ '{nome_popular_real}' pré-selecionada.")
            else:
                print(f"    ❌ '{nome_popular_real}' descartada (score {score_compat:.2f} baixo).")
        
        if not sugestoes_processadas: 
            print("Nenhuma sugestão processada atingiu o score mínimo."); return []
        
        def sort_key_sugestao(sug):
            d_map = {"fácil":0, "médio":1, "verificar no guia": 1, "detalhes no guia": 1, "difícil":2}
            d_val = d_map.get(sug.get("dificuldade_cultivo","").lower(), 1)
            return (-sug["score_compatibilidade"], d_val) 
        sugestoes_processadas.sort(key=sort_key_sugestao)
        sugestoes_finais = sugestoes_processadas[:max_sugestoes_finais]
        print(f"\n🏆 Total de {len(sugestoes_finais)} sugestões finais selecionadas.")
        return sugestoes_finais