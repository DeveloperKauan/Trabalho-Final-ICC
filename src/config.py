"""
Define visual, caminhos de arquivo e regras do jogo.
"""

# --- CAMINHOS DOS ARQUIVOS ---
FILE_SORTEIO = r"objetos\DataSet_Sorteio.csv"
FILE_OBSCURO = r"objetos\DataSet_obscuro.csv"
STATS_FILE   = r"objetos\termoo_stats.csv"

# -------------- PALETA  -----
TEMAS = {
    "escuro": {
        # Ambiente
        "COR_FUNDO": "#1e293b",  # Azul escuro
        "COR_BARRA_ATIVA": "#334155",  # Cinza responsa
        "COR_BARRA_INATIVA": "#0f172a",  # Quase preto
        # Tipografia
        "COR_TEXTO_DIGITADO": "#f8fafc",  # Branco
        "COR_TEXTO_INATIVO": "#475569",  # Cinza
        # Teclado Virtual
        "COR_TECLA_BASE": "#334155",
        "COR_TECLA_HOVER": "#475569",
        "COR_TEXTO_TECLA": "#cbd5e1",
        # Estado da letra
        "COR_ACERTO": "#10b981",  # verde
        "COR_LUGAR_ERRADO": "#f59e0b",  # amarelo
        "COR_AUSENTE": "#0f172a",  # Escuro
        "COR_ERRO_PISCAR": "#7f1d1d", #vermelho
        "ICONE_BOTAO": "☀"  # Botão claro
    },
    "claro": {
    # AMbiente
    "COR_FUNDO": "#f1f5f9",  # Branco
    "COR_BARRA_ATIVA": "#cbd5e1",  # Cinza suav
    "COR_BARRA_INATIVA": "#e2e8f0",  # Cinza claro
    # Tipografia
    "COR_TEXTO_DIGITADO": "#1e293b",  # Azul Escuro
    "COR_TEXTO_INATIVO": "#94a3b8",  # Cinza
    # Teclado Virtual
    "COR_TECLA_BASE": "#cbd5e1",  #
    "COR_TECLA_HOVER": "#94a3b8",
    "COR_TEXTO_TECLA": "#1e293b",  # Texto escuro
    # Estado Letra
    "COR_ACERTO": "#059669",  # Verde
    "COR_LUGAR_ERRADO": "#d97706",  # Laranja queimado
    "COR_AUSENTE": "#94a3b8",  # Cinza (Erro)
    "COR_ERRO_PISCAR": "#fca5a5",  # Vermelho claro
    "ICONE_BOTAO": "☾"  # Botão escuro
}
}

MODO_ATUAL = "escuro"

# Inicializa as variáveis com o tema padrão


def _aplicar_dicionario(tema_dict):
    global COR_FUNDO, COR_BARRA_ATIVA, COR_BARRA_INATIVA, COR_TEXTO_DIGITADO
    global COR_TEXTO_INATIVO, COR_TECLA_BASE, COR_TECLA_HOVER, COR_TEXTO_TECLA
    global COR_ACERTO, COR_LUGAR_ERRADO, COR_AUSENTE, COR_ERRO_PISCAR, ICONE_BOTAO

    COR_FUNDO = tema_dict["COR_FUNDO"]
    COR_BARRA_ATIVA = tema_dict["COR_BARRA_ATIVA"]
    COR_BARRA_INATIVA = tema_dict["COR_BARRA_INATIVA"]
    COR_TEXTO_DIGITADO = tema_dict["COR_TEXTO_DIGITADO"]
    COR_TEXTO_INATIVO = tema_dict["COR_TEXTO_INATIVO"]
    COR_TECLA_BASE = tema_dict["COR_TECLA_BASE"]
    COR_TECLA_HOVER = tema_dict["COR_TECLA_HOVER"]
    COR_TEXTO_TECLA = tema_dict["COR_TEXTO_TECLA"]
    COR_ACERTO = tema_dict["COR_ACERTO"]
    COR_LUGAR_ERRADO = tema_dict["COR_LUGAR_ERRADO"]
    COR_AUSENTE = tema_dict["COR_AUSENTE"]
    COR_ERRO_PISCAR = tema_dict["COR_ERRO_PISCAR"]
    ICONE_BOTAO = tema_dict["ICONE_BOTAO"]


def alternar_modo():
    global MODO_ATUAL
    MODO_ATUAL = "claro" if MODO_ATUAL == "escuro" else "escuro"
    _aplicar_dicionario(TEMAS[MODO_ATUAL])
    return MODO_ATUAL


# Aplica o padrão quando importar
_aplicar_dicionario(TEMAS["escuro"])

# ------------- TIPOGRAFIA ---------
FONTE_TITULO = ("Helvetica", 20, "bold") # Título 
FONTE_TILE = ("Arial", 28, "bold")       # Letras do tabuleiro
FONTE_TECLA = ("Arial", 10, "bold")      # Letras do teclado

# --- REGRA ---
TAMANHO_PALAVRA = 5
MAX_TENTATIVAS = 6

# --- REDE DE SEGURANÇA (BACKUP) ---
# Se der bug no csv roda isso aqui
BACKUP_SORTEIO = [
    "TERMO", "NOBRE", "VAZIO", "MUITO", "COMER", "IDEIA", 
    "AMIGO", "POETA", "TEMPO", "NOITE", "MUNDO", "ARTE",
    "ALMA", "SONHO", "VIDA", "CAOS", "LUZES", "VASCO", "casco"
]