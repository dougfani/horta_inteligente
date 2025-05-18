# agentes/agente_gestor_perfil.py
from datetime import datetime
# Em uma app Streamlit, display(Markdown(...)) não será usado aqui.
# A UI (app.py) chamará os métodos deste agente, e a UI cuidará da exibição.
# A coleta de input também será feita pela UI.
# Este agente se tornará mais um gerenciador de dados do perfil.

class AgenteGestorPerfilUsuario:
    def __init__(self):
        self.perfis_usuarios = {}
        self.usuario_atual_id = None # Será setado pelo app principal
        print("AgenteGestorPerfilUsuario instanciado.")

    def carregar_ou_criar_perfil(self, usuario_id="user_streamlit_default"):
        self.usuario_atual_id = usuario_id
        if usuario_id not in self.perfis_usuarios:
            self.perfis_usuarios[usuario_id] = {
                "id": usuario_id,
                "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "preferencias_plantio": None, # Será preenchido pela UI e setado
                "historico_sugestoes": [],
            }
            print(f"Novo perfil de dados criado para o usuário: {usuario_id}")
        return self.perfis_usuarios[usuario_id]

    def salvar_preferencias_plantio(self, usuario_id, preferencias_dict):
        """Salva as preferências coletadas pela UI."""
        if usuario_id not in self.perfis_usuarios:
            self.carregar_ou_criar_perfil(usuario_id)

        self.perfis_usuarios[usuario_id]["preferencias_plantio"] = preferencias_dict
        print(f"✅ Preferências de plantio salvas para {usuario_id}:")
        for k,v in preferencias_dict.items(): print(f"  {k}: {v}")
        return True

    def get_preferencias_plantio(self, usuario_id):
        perfil = self.perfis_usuarios.get(usuario_id, {})
        return perfil.get("preferencias_plantio")

    def adicionar_sugestao_ao_historico(self, usuario_id, sugestao_lista_nomes):
        if usuario_id in self.perfis_usuarios:
            if "historico_sugestoes" not in self.perfis_usuarios[usuario_id]:
                self.perfis_usuarios[usuario_id]["historico_sugestoes"] = []
            self.perfis_usuarios[usuario_id]["historico_sugestoes"].append({
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "sugestao_nomes": sugestao_lista_nomes
            })
            print(f"Sugestão ({', '.join(sugestao_lista_nomes)}) adicionada ao histórico de {usuario_id}.")

    # O método coletar_preferencias_plantio() do Colab, com seus inputs e prints,
    # não será usado diretamente. A UI do Streamlit (app.py) coletará os dados
    # e então chamará salvar_preferencias_plantio().