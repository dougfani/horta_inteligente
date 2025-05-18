# agentes/agente_estilizador.py
import json
from utils.api_clients import gerar_conteudo_com_gemini

class AgenteEstilizadorConteudoGemini:
    def __init__(self, gemini_model_inst, model_config_inst):
        self.gemini_model = gemini_model_inst
        self.model_config = model_config_inst
        self.esquema_json_planta = None
        self.cache_guias_formatados = {} 
        print("AgenteEstilizadorConteudoGemini (Prompt Guia Melhorado e Correção NameError) instanciado.")

    def definir_esquema_dados_planta(self, forcar_nova_definicao=False):
        # (Este método permanece o mesmo da sua última versão funcional - com o prompt do esquema simplificado)
        # ... (COPIE O MÉTODO definir_esquema_dados_planta COMPLETO DA RESPOSTA ANTERIOR)
        if self.esquema_json_planta and not forcar_nova_definicao:
            print("Usando esquema JSON de planta em cache.")
            return self.esquema_json_planta
        prompt_esquema = """ 
        Você é um especialista em agronomia e estruturação de dados.
        Defina um esquema JSON para descrever plantas comestíveis para um aplicativo de jardinagem no Brasil.
        A resposta DEVE ser APENAS o objeto JSON do esquema.
        O esquema principal deve ter "type": "object" e uma chave "properties".

        Dentro de "properties", defina os seguintes campos principais e seus tipos.
        Para objetos, liste suas sub-propriedades e tipos. Para arrays, o tipo dos itens.
        Para enums, o esquema deve ter "type": "string" e um campo "enum" com os valores.

        Campos Principais:
        - nome_popular (type: string)
        - nome_cientifico (type: string)
        - descricao_curta (type: string)
        - descricao_longa (type: string)
        - categorias (type: array, items_type: string)
        - origem_geografica (type: string)
        - imagem_referencia_url (type: string, opcional)
        - cultivo_info (type: object), com sub-propriedades:
            - dificuldade (type: string, enum_values: ["Fácil", "Médio", "Difícil"])
            - espaco_necessario_descricao_geral (type: string, enum_values: ["Compacta, ideal para vasos pequenos", "Requer vaso/canteiro médio", "Crescimento vigoroso, precisa de mais espaço", "Rasteira ou trepadeira, considerar suporte/espaço lateral"])
            - tempo_dedicacao_semanal_estimado (type: string, enum_values: ["Muito Baixo (<1h)", "Baixo (1-2h)", "Médio (2-4h)", "Alto (>4h)"])
            - climas_ideais_texto_descritivo (type: string) 
            - temperatura_ideal_celsius (type: object, opcional) com: min (type: number), max (type: number), observacao_temperatura (type: string)
            - necessidades_fundamentais_solo (type: object) com:
                - drenagem_requerida (type: string, enum_values: ["Excelente", "Boa", "Moderada"])
                - materia_organica_necessidade (type: string, enum_values: ["Alta", "Média", "Baixa"])
                - ph_faixa_ideal_planta (type: object) com: min (type: number), max (type: number)
                - dicas_adaptacao_solos_comuns (type: string) 
            - cultivo_em_vasos (type: object) com:
                - adequacao (type: string, enum_values: ["Excelente", "Bom", "Possível com cuidados", "Não recomendado"])
                - tamanho_minimo_vaso_sugerido_litros (type: number, opcional)
                - tipo_substrato_recomendado_vaso (type: string, opcional)
                - observacoes_cultivo_vaso (type: string, opcional)
            - luminosidade_necessaria (type: string, enum_values: ["Sol Pleno (6h+)", "Meia Sombra (4-6h sol)", "Sombra Parcial (2-4h sol filtrado)", "Sombra (luz indireta)"])
            - rega_necessidades_descricao (type: string)
            - adubacao_recomendada_descricao (type: string)
        - plantio_info (type: object), com sub-propriedades:
            - metodo_propagacao (type: array, items_type: string)
            - epoca_plantio_ideal_brasil_geral (type: string)
            - profundidade_semeadura_cm (type: number, opcional)
            - espacamento_entre_plantas_cm (type: number, opcional)
            - tempo_germinacao_dias (type: string, opcional)
            - instrucoes_basicas_plantio (type: string)
        - cuidados_gerais_cultivo (type: string)
        - pragas_doencas_comuns_texto (type: string, opcional)
        - colheita_info (type: object) com:
            - tempo_ate_colheita_estimado (type: string)
            - indicadores_maturacao (type: string)
            - instrucoes_colheita (type: string)
        - usos_culinarios_outros (type: string, opcional)
        - variedades_sugeridas_adaptadas (type: array, items_type: object, opcional) com: nome_variedade (type: string), descricao_adaptacao (type: string)
        - curiosidades (type: string, opcional)
        O objeto JSON principal deve começar com {"type": "object", "properties": { ... }} e nada mais.
        NÃO inclua a chave "description" ou "required" nas definições de propriedade dentro do esquema em si.
        """
        print("Definindo esquema JSON para dados de plantas via Gemini (prompt ajustado)...")
        esquema_raw = gerar_conteudo_com_gemini(self.gemini_model, self.model_config, prompt_esquema, solicitar_json=True)
        if isinstance(esquema_raw, dict):
            self.esquema_json_planta = esquema_raw
            print("✅ Esquema JSON para dados de plantas (ajustado) definido e armazenado com sucesso.")
            return self.esquema_json_planta
        else:
            print("🚨 [ERRO ESQUEMA] Falha ao definir o esquema JSON da planta (ajustado)."); print(f"   Resposta recebida:\n{esquema_raw}")
            if self.esquema_json_planta: print("   Retornando esquema em cache anterior."); return self.esquema_json_planta
            return None

    def get_esquema_dados_planta(self):
        if not self.esquema_json_planta:
            return self.definir_esquema_dados_planta()
        return self.esquema_json_planta

    def formatar_guia_plantio_texto(self, dados_planta_json, dados_ambientais_locais, preferencias_usuario):
        localizacao_cache_key = tuple(sorted(dados_ambientais_locais.get('localizacao', {}).items()))
        preferencias_cache_key = tuple(sorted(preferencias_usuario.items()))
        cache_key_tuple = ( dados_planta_json.get('nome_popular', 'desconhecida'), localizacao_cache_key, preferencias_cache_key)
        cache_key = str(cache_key_tuple)

        if cache_key in self.cache_guias_formatados:
            print(f"Usando guia formatado do cache para planta: {dados_planta_json.get('nome_popular', 'desconhecida')}, local: {dados_ambientais_locais.get('localizacao', {}).get('cidade', 'N/A')}")
            return self.cache_guias_formatados[cache_key]

        if not dados_planta_json: return "Dados da planta não fornecidos para formatação do guia."
        if not dados_ambientais_locais or not dados_ambientais_locais.get('localizacao'):
            dados_ambientais_locais = {"localizacao": {"cidade": "sua localidade", "estado": "seu estado"}, 
                                       "clima": {"condicao_atual": "Variável", "clima_regional_estimado": "Variável"}, 
                                       "solo": {"tipo_solo_predominante": "Variável"}}
        if not preferencias_usuario: preferencias_usuario = {"metodo_cultivo_predominante": "vaso"}
        
        nome_planta = dados_planta_json.get('nome_popular', "esta planta")
        cidade_usuario = dados_ambientais_locais.get('localizacao',{}).get('cidade', 'sua cidade')
        estado_usuario = dados_ambientais_locais.get('localizacao',{}).get('estado', 'seu estado')
        clima_local_desc = dados_ambientais_locais.get('clima',{}).get('condicao_atual', 'Não informado')
        clima_regional_local = dados_ambientais_locais.get('clima',{}).get('clima_regional_estimado', 'Não informado')
        solo_regional_tipo = dados_ambientais_locais.get('solo', {}).get('tipo_solo_predominante', 'Não informado')
        metodo_cultivo = preferencias_usuario.get('metodo_cultivo_predominante', 'desconhecido')
        
        # Define cultivo_info_planta AQUI, ANTES de usá-lo para construir dados_planta_para_guia_prompt
        cultivo_info_planta = dados_planta_json.get('cultivo_info', {})
        plantio_info_planta = dados_planta_json.get('plantio_info', {})
        colheita_info_planta = dados_planta_json.get('colheita_info', {})
        
        # As sub-chaves abaixo agora usam cultivo_info_planta
        cultivo_em_vaso_info = cultivo_info_planta.get('cultivo_em_vasos', {})
        necessidades_solo_planta = cultivo_info_planta.get('necessidades_fundamentais_solo', {})

        contexto_cultivo_solo = ""
        if "vaso" in metodo_cultivo:
            contexto_cultivo_solo = (
                f"O usuário ({cidade_usuario}) provavelmente cultivará em vasos. "
                f"A adequação desta planta a vasos é: '{cultivo_em_vaso_info.get('adequacao', 'Verificar')}'."
                f"Substrato recomendado para vasos: '{cultivo_em_vaso_info.get('tipo_substrato_recomendado_vaso', 'um bom substrato comercial para hortaliças ou uma mistura caseira rica em matéria orgânica e com boa drenagem')}'."
                f"Observações para vasos: '{cultivo_em_vaso_info.get('observacoes_cultivo_vaso', 'Garanta furos de drenagem e um tamanho de vaso adequado ao porte final da planta.')}'"
            )
        elif "solo" in metodo_cultivo:
            contexto_cultivo_solo = (
                f"O usuário ({cidade_usuario}) pode cultivar em canteiros no solo local, que é estimado como '{solo_regional_tipo}'. "
                f"O sistema assume que o usuário preparará o solo. As necessidades fundamentais de solo para '{nome_planta}' são: "
                f"Drenagem: '{necessidades_solo_planta.get('drenagem_requerida', 'Boa')}', "
                f"Matéria Orgânica: '{necessidades_solo_planta.get('materia_organica_necessidade', 'Média a Alta')}', "
                f"pH ideal: {necessidades_solo_planta.get('ph_faixa_ideal_planta', {}).get('min', '6.0')}-{necessidades_solo_planta.get('ph_faixa_ideal_planta', {}).get('max', '7.0')}. "
                f"Dicas gerais de adaptação da planta para solos comuns são: '{necessidades_solo_planta.get('dicas_adaptacao_solos_comuns', 'Melhore a fertilidade com composto e garanta boa drenagem.')}'."
            )
        
        # Montando dados_planta_para_guia_prompt usando cultivo_info_planta corretamente
        dados_planta_para_guia_prompt = {
            "nome_popular": nome_planta,
            "nome_cientifico": dados_planta_json.get('nome_cientifico'),
            "descricao_curta": dados_planta_json.get('descricao_curta'),
            "categorias": dados_planta_json.get('categorias'),
            "cultivo_info": { # Usa cultivo_info_planta para preencher este objeto
                "dificuldade": cultivo_info_planta.get('dificuldade'),
                "climas_ideais_texto_descritivo": cultivo_info_planta.get('climas_ideais_texto_descritivo'),
                "luminosidade_necessaria": cultivo_info_planta.get('luminosidade_necessaria'),
                "rega_necessidades_descricao": cultivo_info_planta.get('rega_necessidades_descricao'),
                "adubacao_recomendada_descricao": cultivo_info_planta.get('adubacao_recomendada_descricao'),
                "cultivo_em_vasos": cultivo_em_vaso_info, 
                "necessidades_fundamentais_solo": necessidades_solo_planta 
            },
            "plantio_info": plantio_info_planta,
            "cuidados_gerais_cultivo": dados_planta_json.get('cuidados_gerais_cultivo'),
            "pragas_doencas_comuns_texto": dados_planta_json.get('pragas_doencas_comuns_texto'),
            "colheita_info": colheita_info_planta,
            "variedades_sugeridas_adaptadas": dados_planta_json.get('variedades_sugeridas_adaptadas')
        }
        dados_planta_str_resumido = json.dumps(dados_planta_para_guia_prompt, indent=2, ensure_ascii=False)

        prompt_formatacao = f"""
        Você é um redator de jardinagem experiente, apaixonado por ajudar iniciantes.
        Sua tarefa é gerar um GUIA DE CULTIVO COMPLETO, CLARO, CONCISO e MOTIVADOR para a planta "{nome_planta}".
        O guia será usado em um aplicativo mobile.

        **Contexto do Usuário e Local:**
        - Jardinagem em: {cidade_usuario}, {estado_usuario} (Clima regional estimado: {clima_regional_local})
        - Método de cultivo principal e solo: {contexto_cultivo_solo}

        **Dados da Planta como Referência (use os campos relevantes para construir o guia):**
        ```json
        {dados_planta_str_resumido} 
        ```

        **Instruções de Redação e Estilo para o Guia (Formato Markdown):**
        1.  **Título Principal:** `## Guia de Cultivo Completo para: {nome_planta}`.
        2.  **Linguagem:** Use frases curtas e diretas. Linguagem MUITO SIMPLES, como se estivesse conversando com um amigo que nunca plantou nada. Seja positivo e encorajador! Evite parágrafos longos; prefira 2-3 frases por parágrafo.
        3.  **Listas (Bullet Points):** Use بكثرة para passos de plantio, listas de materiais, dicas de cuidado. Isso torna a leitura fácil e rápida.
        4.  **Estrutura e Conteúdo das Seções (use `###` para subtítulos):**
            * `### Conhecendo a {nome_planta}`: (1-2 parágrafos curtos: o que é, principais características/usos).
            * `### Ambiente Ideal para sua {nome_planta}`:
                * **Luz:** De quanto sol ela gosta? (Use termos como "Sol pleno", "Algumas horas de sol direto", "Luz indireta brilhante").
                * **Clima:** Descreva de forma simples o clima que ela prefere, usando o `climas_ideais_texto_descritivo` da planta.
            * `### Mão na Terra: Preparando o Cantinho da {nome_planta}` (Adapte o subtítulo se for vaso: "Preparando o Vaso Perfeito")
                * **CRUCIAL:** Com base no `{contexto_cultivo_solo}`, explique de forma MUITO PRÁTICA.
                * Se vasos: Que tipo de vaso? Qual substrato (ou mistura simples)? Drenagem é chave!
                * Se solo local: Como deixar o solo `{solo_regional_tipo}` fofinho e nutritivo para a `{nome_planta}`? Dicas de adubo orgânico (composto, húmus). Fale de pH de forma simples (se precisa ser mais ácido ou neutro, e uma dica básica se precisar ajustar).
            * `### Plantando sua Muda ou Semente de {nome_planta}`:
                * Época boa para plantar (baseado em `epoca_plantio_ideal_brasil_geral`).
                * Passos simples em bullet points (ex: profundidade, espaçamento se sementes; como plantar a muda).
            * `### Cuidados que Fazem a Diferença`:
                * **Rega:** Quando e como regar? (Ex: "Mantenha o solo úmido, mas não encharcado. Toque a terra para sentir!").
                * **Adubação:** Precisa de "comida extra"? Se sim, uma dica simples de adubo orgânico e quando aplicar.
                * **Outros Cuidados:** Alguma poda rápida? Precisa de apoio para crescer? (Mencione brevemente só se for muito importante).
            * `### Olho Vivo! (Pragas e Doenças Comuns)`: (Se `pragas_doencas_comuns_texto` tiver info, mencione 1-2 de forma simples e uma dica de controle caseiro/orgânico para cada. Se não, diga "É uma planta geralmente resistente! Fique de olho em [sinal genérico] e aja rápido.").
            * `### A Melhor Parte: A Colheita!`:
                * Como saber que está no ponto?
                * Dicas rápidas de como colher.
            * `### Dica Extra (Opcional)`: Se houver uma variedade específica interessante (`variedades_sugeridas_adaptadas`) ou uma curiosidade (`curiosidades`) muito legal, mencione.
        5.  **Priorize Informações Acionáveis:** O que o usuário pode FAZER.
        6.  **Saída:** APENAS o texto do guia em formato Markdown.

        Seja breve, mas completo com o essencial. Imagine que o usuário tem pouco tempo e quer começar logo!
        """
        
        guia_formatado_md = gerar_conteudo_com_gemini(
            self.gemini_model, self.model_config, prompt_formatacao, solicitar_json=False
        )

        if guia_formatado_md and "não foi possível gerar" not in guia_formatado_md.lower():
            print(f"✅ Guia de plantio em Markdown para '{nome_planta}' gerado (Estilo Melhorado).")
            self.cache_guias_formatados[cache_key] = guia_formatado_md
            return guia_formatado_md
        else:
            print(f"🚨 [ERRO GUIA FORMATADO] Falha ao gerar o guia em Markdown para '{nome_planta}'.")
            fallback_guia = f"## Guia de Cultivo para: {nome_planta}\n\nLamentamos, não conseguimos gerar o guia detalhado no momento. \n\n**Dicas Gerais:**\n- Pesquise as necessidades específicas de luz, água e solo para {nome_planta} em sua região.\n- Comece com mudas de boa qualidade ou sementes de fornecedores confiáveis.\n- Observe suas plantas diariamente para identificar problemas cedo."
            self.cache_guias_formatados[cache_key] = fallback_guia
            return fallback_guia