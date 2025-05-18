# agentes/agente_gerador_guia.py
# agente_pesquisador e agente_estilizador são passados no __init__

class AgenteGeradorConteudoPlantioDetalhado:
    def __init__(self, agente_pesquisador_plantas, agente_estilizador_conteudo):
        self.agente_pesquisador = agente_pesquisador_plantas
        self.agente_estilizador = agente_estilizador_conteudo
        print("AgenteGeradorConteudoPlantioDetalhado (Lógica Ajustada) instanciado.")

    def gerar_guia_plantio_para_planta_sugerida(self, nome_planta_popular, dados_planta_json_sugerida, 
                                                dados_ambientais_completos, preferencias_usuario):
        print(f"\n--- {self.__class__.__name__}: Gerando guia para '{nome_planta_popular}' (Lógica Ajustada) ---")

        dados_planta_para_guia = dados_planta_json_sugerida
        if not dados_planta_para_guia: # Se o JSON completo não veio com a sugestão
            print(f"Dados da planta '{nome_planta_popular}' não fornecidos com a sugestão. Buscando novamente...")
            dados_planta_para_guia = self.agente_pesquisador.obter_dados_detalhados_planta(nome_planta_popular, forcar_nova_busca=True) # Força nova busca se não veio
            if not dados_planta_para_guia:
                return f"🚨 [ERRO GUIA] Não foi possível obter os dados detalhados para a planta '{nome_planta_popular}' para gerar o guia."

        guia_markdown = self.agente_estilizador.formatar_guia_plantio_texto(
            dados_planta_json=dados_planta_para_guia,
            dados_ambientais_locais=dados_ambientais_completos,
            preferencias_usuario=preferencias_usuario
        )

        if guia_markdown and "não foi possível gerar" not in guia_markdown.lower():
            print(f"✅ Guia em Markdown para '{nome_planta_popular}' gerado.")
            return guia_markdown
        else:
            print(f"🚨 [ERRO GUIA] Falha ao gerar guia em Markdown para '{nome_planta_popular}'.")
            return f"Lamentamos, não foi possível gerar o guia de plantio detalhado para {nome_planta_popular} no momento."