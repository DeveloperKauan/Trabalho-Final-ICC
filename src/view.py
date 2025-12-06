import tkinter as tk
from src import config

class TermoView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self._configurar_janela()
        self.cells = []
        self.botoes_teclado = {}
        self._setup_ui()

    def _configurar_janela(self):
        self.root.title("Termo ICC")
        self.root.configure(bg=config.COR_FUNDO)
        #Não mexe, ta centralizado
        largura, altura = 450, 750
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - largura) // 2
        y = (screen_h - altura) // 2 - 50
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")
        self.root.resizable(True, True)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

    def _setup_ui(self):
        # Cabeçalho
        # frame e label para poder mudar a cor depois
        self.header_frame = tk.Frame(self.root, bg=config.COR_FUNDO, height=70)  # Altura fixa
        self.header_frame.pack_propagate(False)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        # Grid layout
        self.header_frame.columnconfigure(0, weight=1)
        self.header_frame.columnconfigure(1, weight=0)
        self.header_frame.columnconfigure(2, weight=1)

        self.lbl_titulo = tk.Label(
            self.header_frame,
            text="T E R M O O",
            font=config.FONTE_TITULO,
            bg=config.COR_FUNDO,
            fg=config.COR_TEXTO_INATIVO
        )
        self.lbl_titulo.place(relx=0.5, rely=0.5, anchor="center")

        # Botão de Tema no Canto Direito
        self.btn_tema = tk.Button(
            self.header_frame,
            text=config.ICONE_BOTAO,
            command=self.controller.alternar_tema,
            bg=config.COR_FUNDO,
            fg=config.COR_TEXTO_INATIVO,
            font=("Arial", 16),
            relief="flat", bd=-1000, cursor="hand2",
            activebackground=config.COR_FUNDO
        )
        self.btn_tema.grid(row=0, column=2, sticky="e", padx=20)

        # Tabuleiro
        self.container_board = tk.Frame(self.root, bg=config.COR_FUNDO)
        self.container_board.grid(row=1, column=0)
        self._construir_grade_letras()

        # Teclado
        self.container_teclado = tk.Frame(self.root, bg=config.COR_FUNDO, pady=30)
        self.container_teclado.grid(row=2, column=0, sticky="ew", padx=20)
        self._construir_teclado()

    def _construir_grade_letras(self):
        for r in range(config.MAX_TENTATIVAS):
            linha_cells = []
            # Frame da linha
            frame_linha = tk.Frame(self.container_board, bg=config.COR_FUNDO)
            frame_linha.pack(pady=2)

            for c in range(config.TAMANHO_PALAVRA):
                cell_frame = tk.Frame(frame_linha, width=65, height=65, bg=config.COR_BARRA_INATIVA)
                cell_frame.pack_propagate(False)
                cell_frame.pack(side="left", padx=1)

                label = tk.Label(cell_frame, text="", font=config.FONTE_TILE,
                                 bg=config.COR_BARRA_INATIVA, fg=config.COR_TEXTO_DIGITADO)
                label.place(relx=0.5, rely=0.5, anchor="center")

                # mudar o bg certin tem que guardar a versao
                linha_cells.append({"frame": cell_frame, "label": label, "parent_line": frame_linha})
            self.cells.append(linha_cells)

    def _construir_teclado(self):
        teclas = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        # guarda os frame do teclado
        self.teclado_rows = []

        for i, linha_teclas in enumerate(teclas):
            frame_row = tk.Frame(self.container_teclado, bg=config.COR_FUNDO)
            frame_row.pack(pady=1)
            self.teclado_rows.append(frame_row)

            # Se mudar o valor do i você escolhe a linha q fica o enter e o apagar
            if i == 2:
                self._criar_botao(frame_row, "ENTER", 7,
                                  lambda: self.controller.handle_keypress(type('E', (object,), {'keysym': 'Return'})))

            for char in linha_teclas:
                self._criar_botao(frame_row, char, 4,
                                  lambda c=char: self.controller._inserir_letra(c))

            if i == 2:
                self._criar_botao(frame_row, "⌫", 5,
                                  lambda: self.controller.handle_keypress(
                                      type('E', (object,), {'keysym': 'BackSpace'})))

    def _criar_botao(self, parent, text, width, command):
        btn = tk.Button(
            parent, text=text, command=command,
            bg=config.COR_TECLA_BASE, fg=config.COR_TEXTO_TECLA, font=config.FONTE_TECLA,
            relief="flat", borderwidth=0, highlightthickness=0, width=width, height=3, cursor="hand2"
        )
        btn.pack(side="left", padx=1)
        btn.bind("<Enter>", lambda e: self._on_hover(e, True))
        btn.bind("<Leave>", lambda e: self._on_hover(e, False))

        if len(text) == 1 and text.isalpha():
            self.botoes_teclado[text] = btn
        else:
            self.botoes_teclado[text] = btn

    def _on_hover(self, event, entering):
        #efeitin
        widget = event.widget
        cor = widget.cget("bg")
        if cor in [config.COR_TECLA_BASE, config.COR_TECLA_HOVER]:
            widget.config(bg=config.COR_TECLA_HOVER if entering else config.COR_TECLA_BASE)

    # --- ATUALIZAÇÃO VISUAL ---

    def aplicar_tema_visual(self):
        # Fundo
        self.root.configure(bg=config.COR_FUNDO)
        self.header_frame.configure(bg=config.COR_FUNDO)
        self.lbl_titulo.configure(bg=config.COR_FUNDO, fg=config.COR_TEXTO_INATIVO)
        self.container_board.configure(bg=config.COR_FUNDO)
        self.container_teclado.configure(bg=config.COR_FUNDO)

        # Botão Tema
        self.btn_tema.configure(text=config.ICONE_BOTAO, bg=config.COR_FUNDO,
                                fg=config.COR_TEXTO_INATIVO, activebackground=config.COR_FUNDO)

        # Tabuleiro
        for r in range(config.MAX_TENTATIVAS):
            for c in range(config.TAMANHO_PALAVRA):
                cell = self.cells[r][c]
                # Atualiza o fundo da linha
                cell["parent_line"].configure(bg=config.COR_FUNDO)
                bg_atual = cell["frame"].cget("bg")

                # testa se NÃO é resultado
                cores_resultado = [config.TEMAS["escuro"]["COR_ACERTO"], config.TEMAS["claro"]["COR_ACERTO"],
                                   config.TEMAS["escuro"]["COR_LUGAR_ERRADO"],
                                   config.TEMAS["claro"]["COR_LUGAR_ERRADO"]]


                if bg_atual not in cores_resultado:
                    # Se for a linha atual (ativa)
                    if r == self.controller.backend.tentativa_atual:
                        cell["frame"].configure(bg=config.COR_BARRA_ATIVA)
                        cell["label"].configure(bg=config.COR_BARRA_ATIVA)
                    else:
                        cell["frame"].configure(bg=config.COR_BARRA_INATIVA)
                        cell["label"].configure(bg=config.COR_BARRA_INATIVA)

                    # manter o texto
                    if cell["label"].cget("text") != "":
                        cell["label"].configure(fg=config.COR_TEXTO_DIGITADO)
                    else:
                        cell["label"].configure(fg=config.COR_TEXTO_DIGITADO)

        # Teclado
        for row in self.teclado_rows:
            row.configure(bg=config.COR_FUNDO)

        for btn in self.botoes_teclado.values():
            bg_atual = btn.cget("bg")
            # msm coisa de cima
            cores_res_tecla = cores_resultado + [config.TEMAS["escuro"]["COR_TECLA_HOVER"],
                                                 config.TEMAS["claro"]["COR_TECLA_HOVER"]]

            if bg_atual not in cores_resultado:
                btn.configure(bg=config.COR_TECLA_BASE, fg=config.COR_TEXTO_TECLA)

    def atualizar_celula(self, linha, coluna, letra, ativo=True):
        cell = self.cells[linha][coluna]
        cell["label"].config(text=letra)
        if ativo and letra:
            # dar contraste
            destaque = "#ffffff" if config.MODO_ATUAL == "escuro" else "#000000"
            cell["label"].config(fg=destaque)
        else:
            cell["label"].config(fg=config.COR_TEXTO_DIGITADO)

    def destacar_linha(self, linha_idx):
        #Mostrar qual é a linha do jogo
        if linha_idx >= config.MAX_TENTATIVAS: return
        for c in range(config.TAMANHO_PALAVRA):
            cell = self.cells[linha_idx][c]
            cell["frame"].config(bg=config.COR_BARRA_ATIVA)
            cell["label"].config(bg=config.COR_BARRA_ATIVA)

    def resetar_tabuleiro(self):
        for r in range(config.MAX_TENTATIVAS):
            for c in range(config.TAMANHO_PALAVRA):
                cell = self.cells[r][c]
                cell["label"].config(text="", bg=config.COR_BARRA_INATIVA)
                cell["frame"].config(bg=config.COR_BARRA_INATIVA)
        for btn in self.botoes_teclado.values():
            btn.config(bg=config.COR_TECLA_BASE, fg=config.COR_TEXTO_TECLA)

    def animar_erro_linha(self, linha_idx):
        #pisca vermelho
        cor_original = config.COR_BARRA_ATIVA
        for c in range(config.TAMANHO_PALAVRA):
            self.cells[linha_idx][c]["frame"].config(bg=config.COR_ERRO_PISCAR)
            self.cells[linha_idx][c]["label"].config(bg=config.COR_ERRO_PISCAR)
        self.root.after(250, lambda: self._restaurar_cor_linha(linha_idx, cor_original))

    def _restaurar_cor_linha(self, linha_idx, cor):
        if not self.controller.jogo_acabou:
            cor_atual = config.COR_BARRA_ATIVA
            for c in range(config.TAMANHO_PALAVRA):
                self.cells[linha_idx][c]["frame"].config(bg=cor_atual)
                self.cells[linha_idx][c]["label"].config(bg=cor_atual)

    def pintar_resultado(self, linha, palavra, cores):
        for i in range(config.TAMANHO_PALAVRA):
            c = cores[i]
            letra = palavra[i]

            cell = self.cells[linha][i]
            cell["frame"].config(bg=c)
            cell["label"].config(bg=c)
            if c == config.COR_AUSENTE:
                fg_color = "#ffffff" if config.MODO_ATUAL == "escuro" else "#ffffff"
            else:
                fg_color = "#ffffff" if config.MODO_ATUAL == "escuro" else "#ffffff"

            cell["label"].config(fg=fg_color)

            if letra in self.botoes_teclado:
                #muda cor
                btn = self.botoes_teclado[letra]
                cor_atual_btn = btn.cget("bg")
                nova_cor = cor_atual_btn

                if cor_atual_btn != config.COR_ACERTO:
                    #era pra mudar a cor do que já ta
                    if c == config.COR_ACERTO:
                        nova_cor = config.COR_ACERTO
                    elif c == config.COR_LUGAR_ERRADO and cor_atual_btn != config.COR_LUGAR_ERRADO:
                        nova_cor = config.COR_LUGAR_ERRADO
                    elif c == config.COR_AUSENTE and cor_atual_btn == config.COR_TECLA_BASE:
                        nova_cor = config.COR_AUSENTE

                fg_btn = "#ffffff" if nova_cor in [config.COR_AUSENTE, config.COR_ACERTO,
                                                   config.COR_LUGAR_ERRADO] else config.COR_TEXTO_TECLA
                btn.config(bg=nova_cor, fg=fg_btn)

    def mostrar_estatisticas(self, vitoria, palavra_secreta, stats):
        win = tk.Toplevel(self.root)
        win.configure(bg=config.COR_FUNDO)
        w, h = 320, 480
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)
        win.geometry(f"{w}x{h}+{x}+{y}")
        win.transient(self.root)
        win.grab_set()

        if not vitoria:
            tk.Label(win, text="O TERMO ERA:", font=(config.FONTE_TITULO),
                     bg=config.COR_FUNDO, fg=config.COR_TEXTO_INATIVO).pack(pady=5)

            tk.Label(win, text=palavra_secreta, font=("Arial", 45, "bold"),
                     bg=config.COR_FUNDO, fg=config.COR_ERRO_PISCAR).pack(pady=5)
        else:
            tk.Label(win, text="R E S U L T A D O", font=("Helvetica", 23, "bold"),
                     bg=config.COR_FUNDO, fg=config.COR_TEXTO_INATIVO).pack(pady=5)

            tk.Label(win, text="EXTRAORDINÁRIO", font=("Arial", 18, "bold"),
                     bg=config.COR_FUNDO, fg=config.COR_ACERTO).pack(pady=5)

        f_dados = tk.Frame(win, bg=config.COR_FUNDO)
        f_dados.pack(fill="x", padx=20, pady=10)

        jogos = stats["jogos"]
        pct = int((stats["vitorias"] / jogos) * 100) if jogos else 0
        dados_view = [(str(jogos), "JOGOS"), (f"{pct}%", "VITÓRIAS"), (str(stats["sequencia_atual"]), "SEQ.")]

        for i, (num, txt) in enumerate(dados_view):
            f = tk.Frame(f_dados, bg=config.COR_FUNDO)
            f.grid(row=0, column=i, sticky="ew")
            tk.Label(f, text=num, font=("Arial", 20, "bold"), bg=config.COR_FUNDO, fg=config.COR_TEXTO_DIGITADO).pack()
            tk.Label(f, text=txt, font=("Arial", 8), bg=config.COR_FUNDO, fg=config.COR_TEXTO_INATIVO).pack()
        for i in range(3): f_dados.columnconfigure(i, weight=1)

        # Gráfico
        f_graf = tk.Frame(win, bg=config.COR_FUNDO)
        f_graf.pack(fill="x", padx=30, pady=20)
        dist = stats["distribuicao"]
        max_v = max(dist.values()) if dist.values() and max(dist.values()) > 0 else 1
        tentativa_vitoria_idx = (
            self.controller.backend.tentativa_atual) if vitoria else None  # Nota: controller backend tentativa atual já é o idx + 1 no fim do jogo se não houve reset

        for i in range(1, 7):
            val = dist[str(i)]
            row = tk.Frame(f_graf, bg=config.COR_FUNDO)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=str(i), bg=config.COR_FUNDO, fg=config.COR_TEXTO_INATIVO, font=("Arial", 10),
                     width=2).pack(side="left")
            width_percent = max(0.05, val / max_v) if val else 0.02
            # Cor da barra
            cor_barra = config.COR_ACERTO if (vitoria and tentativa_vitoria_idx == i) else config.COR_BARRA_ATIVA

            bar_frame = tk.Frame(row, bg=config.COR_FUNDO, height=14)
            bar_frame.pack(side="left", fill="x", expand=True)
            tk.Frame(bar_frame, bg=cor_barra, width=1).place(rely=0, relheight=1, relwidth=width_percent)
            if val > 0: tk.Label(bar_frame, text=str(val), bg=cor_barra, fg="#fff", font=("Arial", 7, "bold")).place(
                relx=width_percent, x=-15, rely=0)

        tk.Button(win, text="JOGAR NOVAMENTE", command=lambda: self.controller.iniciar_novo_jogo(win),
                  bg=config.COR_TEXTO_TECLA, fg=config.COR_FUNDO, font=("Arial", 10, "bold"), relief="flat",
                  pady=10).pack(fill="x", padx=50, side="bottom", pady=30)