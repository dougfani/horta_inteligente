# agentes/agente_redator_ia.py
from utils.api_clients import gerar_conteudo_com_gemini

class AgenteRedatorConteudoIA:
    def __init__(self, gemini_model_inst, model_config_inst):
        self.gemini_model = gemini_model_inst
        self.model_config = model_config_inst
        print("AgenteRedatorConteudoIA instanciado.")

    def gerar_texto_ponto_atencao(self, nome_planta, tipo_atencao, contexto_planta, contexto_usuario):
        """
        Gera um texto amigável e acionável para um ponto de atenção.
        tipo_atencao: ex: "espaco_limitado", "clima_nao_ideal", "tempo_dedicacao_alto", "adequacao_vaso_incerta"
        contexto_planta: Descrição da necessidade da planta (ex: "Requer vaso/canteiro médio", "Prefere climas tropicais")
        contexto_usuario: Descrição da condição do usuário (ex: "Espaço <1m²", "Clima Subtropical")
        """
        prompt = f"""
        Você é um redator de jardinagem amigável e experiente.
        Para a planta "{nome_planta}", um possível desafio foi identificado para o usuário.
        Desafio: O usuário tem "{contexto_usuario}", enquanto a planta tem a característica/necessidade: "{contexto_planta}".
        Tipo do desafio (para seu contexto): {tipo_atencao}

        Crie uma frase CURTA (1-2 linhas no máximo), CLARA e ACIONÁVEL como um "Ponto de Atenção".
        Evite linguagem negativa. Foque em observação ou sugestão de manejo.
        Exemplos de tom:
        - Se o espaço do usuário é "<1m²" e a planta "requer vaso/canteiro médio": "Esta planta pode precisar de um vaso um pouco maior do que o ideal para espaços muito pequenos. Considere variedades anãs ou podas."
        - Se o clima do usuário é "Subtropical" e a planta "prefere climas tropicais": "No clima Subtropical, esta planta pode precisar de um local mais protegido ou cuidados extras no inverno."
        - Se a adequação a vasos é "Não especificado": "Para cultivo em vasos, é bom verificar o tamanho ideal do recipiente e usar um substrato de qualidade para esta planta."

        Gere apenas a frase do ponto de atenção.
        """
        ponto_atencao_texto = gerar_conteudo_com_gemini(
            self.gemini_model, self.model_config, prompt, solicitar_json=False
        )
        return ponto_atencao_texto.strip() if ponto_atencao_texto else f"Atenção ao cultivar {nome_planta} considerando: {contexto_planta} vs {contexto_usuario}."

    def gerar_texto_justificativa_sugestao(self, nome_planta, tipo_justificativa, contexto_planta, contexto_usuario):
        """Gera um texto amigável para uma justificativa de sugestão."""
        prompt = f"""
        Você é um redator de jardinagem amigável e experiente.
        A planta "{nome_planta}" está sendo sugerida ao usuário.
        Um dos motivos positivos é: "{contexto_planta}" que se alinha com a preferência/condição do usuário de "{contexto_usuario}".
        Tipo da justificativa (para seu contexto): {tipo_justificativa}

        Crie uma frase CURTA (1-2 linhas no máximo) e POSITIVA como uma "Justificativa da Sugestão".
        Exemplos:
        - "Ótima para vasos, como você prefere!"
        - "Adapta-se bem ao clima {contexto_usuario} da sua região."
        - "Seu tempo disponível é ideal para os cuidados que ela necessita."

        Gere apenas a frase da justificativa.
        """
        justificativa_texto = gerar_conteudo_com_gemini(
            self.gemini_model, self.model_config, prompt, solicitar_json=False
        )
        return justificativa_texto.strip() if justificativa_texto else f"{nome_planta} parece uma boa opção considerando {contexto_usuario}."

    def gerar_secao_preparo_local_guia(self, nome_planta, dados_planta_json, dados_ambientais_locais, preferencias_usuario):
        """Gera a seção 'Preparando o Local de Plantio' para o guia de cultivo."""
        
        metodo_cultivo = preferencias_usuario.get('metodo_cultivo_predominante', 'desconhecido')
        solo_regional_tipo = dados_ambientais_locais.get('solo', {}).get('tipo_solo_predominante', 'Não informado')
        cultivo_em_vaso_info = dados_planta_json.get('cultivo_info', {}).get('cultivo_em_vasos', {})
        necessidades_solo_planta = dados_planta_json.get('cultivo_info', {}).get('necessidades_fundamentais_solo', {})
        dicas_adaptacao_solos_planta = necessidades_solo_planta.get('dicas_adaptacao_solos_comuns', '')

        contexto_prompt = ""
        if "vaso" in metodo_cultivo:
            contexto_prompt = f"O usuário optou por cultivar '{nome_planta}' principalmente em vasos. O tipo de substrato recomendado pela planta é '{cultivo_em_vaso_info.get('tipo_substrato_recomendado_vaso', 'um substrato rico e bem drenado')}' e o tamanho mínimo de vaso sugerido é '{cultivo_em_vaso_info.get('tamanho_minimo_vaso_sugerido_litros', 'verificar porte da planta')} litros'. As observações para cultivo em vaso são: '{cultivo_em_vaso_info.get('observacoes_cultivo_vaso', 'garantir boa drenagem')}'."
        elif "solo" in metodo_cultivo:
            contexto_prompt = (
                f"O usuário optou por cultivar '{nome_planta}' em canteiros no solo local. O solo regional estimado é '{solo_regional_tipo}'. "
                f"As necessidades fundamentais de solo para '{nome_planta}' são: Drenagem: '{necessidades_solo_planta.get('drenagem_requerida', 'N/A')}', "
                f"Matéria Orgânica: '{necessidades_solo_planta.get('materia_organica_necessidade', 'N/A')}', "
                f"pH ideal: {necessidades_solo_planta.get('ph_faixa_ideal_planta', {}).get('min', 'N/A')}-{necessidades_solo_planta.get('ph_faixa_ideal_planta', {}).get('max', 'N/A')}. "
                f"Dicas gerais de adaptação da planta para solos comuns são: '{dicas_adaptacao_solos_planta}'. "
                f"Lembre-se que o sistema assume que o usuário irá preparar o solo."
            )

        prompt = f"""
        Você é um redator de jardinagem experiente, escrevendo para iniciantes de forma clara e motivadora.
        Gere a seção "### Preparando o Local de Plantio (Seu Cenário: {metodo_cultivo.replace('_', ' ')})" para o guia de cultivo da planta "{nome_planta}".

        Contexto do Usuário e da Planta:
        {contexto_prompt}

        Instruções para a Seção:
        - Se for cultivo em vasos, foque em: escolha do vaso (tamanho, material), importância da drenagem (camada de drenagem, furos), e como preparar ou qual tipo de substrato/terra comprar.
        - Se for cultivo no solo local, explique como o usuário pode preparar o solo regional '{solo_regional_tipo}' para atender às necessidades fundamentais de '{nome_planta}'. Detalhe a adição de matéria orgânica (composto, húmus), como melhorar a drenagem (se necessário), e uma breve menção sobre como verificar e ajustar o pH de forma simples (ex: com calcário ou enxofre, se aplicável, ou sugerindo um kit de teste).
        - Use linguagem simples, direta e em tom encorajador.
        - Utilize bullet points para listas de materiais ou passos.
        - Mantenha a seção concisa, mas informativa (3-5 parágrafos curtos ou equivalentes em listas).
        - A saída deve ser APENAS o texto em Markdown para esta seção.
        """
        secao_texto = gerar_conteudo_com_gemini(
            self.gemini_model, self.model_config, prompt, solicitar_json=False
        )
        return secao_texto.strip() if secao_texto else f"Para preparar o local para '{nome_planta}', verifique as necessidades de solo e drenagem. Se em vaso, use um bom substrato. Se no chão, melhore o solo com composto orgânico."