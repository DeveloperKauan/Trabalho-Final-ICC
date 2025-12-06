import tkinter as tk
import threading
import sys
from unidecode import unidecode
from src import config
from src.backend import TermoBackend
from src.view import TermoView


class TermoController:
    def __init__(self):
        # Cria a janela
        self.root = tk.Tk()

        # inicia
        self.backend = TermoBackend()
        self.view = TermoView(self.root, self)  # callback

        # Salva estado
        self.palavra_digitada = [""] * config.TAMANHO_PALAVRA
        self.coluna_atual = 0
        self.jogo_acabou = False
        self.app_rodando = True  # Flag para controlar a thread do terminal

        # Teclado
        self.root.bind('<Key>', self.handle_keypress)

        # Garante que o processo feche totalmente ao fechar a janela
        self.root.protocol("WM_DELETE_WINDOW", self._ao_fechar)

    def iniciar(self):
        # Mostra instruções no terminal
        self._mostrar_instrucoes_terminal()

        # Inicia o ouvido do terminal em paralelo (Thread) essa parte foi o gemini que recomendou

        t = threading.Thread(target=self._monitorar_terminal, daemon=True)
        t.start()

        self.iniciar_novo_jogo()
        self.root.mainloop()

    def _ao_fechar(self):
        self.app_rodando = False
        self.root.destroy()
        sys.exit()

    def _mostrar_instrucoes_terminal(self):
        print("\n" + "=" * 40)
        print("      T E R M O   ( C L O N E )      ")
        print("=" * 40)
        print("COMO JOGAR NA TELA:")
        print(" • Digite palavras de 5 letras.")
        print(" • [VERDE]: Letra certa, lugar certo.")
        print(" • [AMARELO]: Letra certa, lugar errado.")
        print(" • [CINZA]: Letra não existe.")
        print("-" * 40)
        print("SEGREDOS DO BASTIDOR (Digite aqui no terminal):")
        print(" > 'resposta' : Revela a palavra secreta atual.")
        print(" > 'stats'    : Mostra a frequência das palavras que você mais usa.")
        print(" > 'ajuda'    : Mostra estas instruções novamente.")
        print("=" * 40 + "\n")

    def _monitorar_terminal(self):
        while self.app_rodando:
            try:
                # O input espera você digitar algo e dar Enter
                comando = input().strip().lower()

                if not self.app_rodando: break

                if comando == "resposta":
                    print(f"\n[SPOILER] A palavra secreta é: {self.backend.palavra_secreta}")
                    print("Psiu... nosso segredo hein Matheus.\n")

                elif comando == "stats":
                    self._imprimir_frequencia_detalhada()

                elif comando == "ajuda":
                    self._mostrar_instrucoes_terminal()

                elif comando:
                    print(f"Comando '{comando}' não compreendido. Tente 'ajuda'.")

            except (EOFError, KeyboardInterrupt):
                break

    def _imprimir_frequencia_detalhada(self):
        freq = self.backend.stats.get("palavras_frequentes", {})
        print("\n" + "-" * 30)
        print("SUAS PALAVRAS MAIS USADAS")
        print("-" * 30)

        if not freq:
            print("O caderno está em branco. Jogue mais!")
        else:
            # Ordena
            ranking = sorted(freq.items(), key=lambda item: item[1], reverse=True)[:15]
            for i, (palavra, qtd) in enumerate(ranking, 1):
                print(f"{i:02d}. {palavra} ({qtd}x)")
        print("-" * 30 + "\n")

    def alternar_tema(self):
        config.alternar_modo()
        self.view.aplicar_tema_visual()

    def iniciar_novo_jogo(self, window_to_close=None):
        if window_to_close:
            window_to_close.destroy()

        # Reseta
        self.jogo_acabou = False
        self.coluna_atual = 0
        self.palavra_digitada = [""] * config.TAMANHO_PALAVRA

        # sorteia dnv
        self.backend.sortear_palavra()

        print(f">>> Nova partida iniciada.")

        # reseta
        self.view.resetar_tabuleiro()
        self.view.destacar_linha(self.backend.tentativa_atual)

    # Teclado
    def handle_keypress(self, event):
        if self.jogo_acabou: return

        key = event.keysym

        if key == "Return":
            self._verificar_tentativa()
        elif key == "BackSpace":
            self._apagar_letra()
        # ve se pode
        elif len(key) == 1 and event.char.isalpha() and unidecode(event.char).isalpha():
            self._inserir_letra(event.char.upper())

    def _inserir_letra(self, letra):
        if self.coluna_atual < config.TAMANHO_PALAVRA:
            self.palavra_digitada[self.coluna_atual] = letra

            # Karen isso aqui é oq desenha
            self.view.atualizar_celula(
                self.backend.tentativa_atual,
                self.coluna_atual,
                letra,
                ativo=True
            )

            self.coluna_atual += 1

    def _apagar_letra(self):
        if self.coluna_atual > 0:
            self.coluna_atual -= 1
            self.palavra_digitada[self.coluna_atual] = ""

            # Esse é oq apaga nao mexe nao
            self.view.atualizar_celula(
                self.backend.tentativa_atual,
                self.coluna_atual,
                "",
                ativo=False
            )

    def _verificar_tentativa(self):
        # Evitar aquelas pintada errada
        if self.coluna_atual != config.TAMANHO_PALAVRA:
            return

        guess = "".join(self.palavra_digitada)

        if not self.backend.palavra_existe(guess):
            self.view.animar_erro_linha(self.backend.tentativa_atual)
            print(f"Validação: '{guess}' não aceita.")
            return

        linha_para_pintar = self.backend.tentativa_atual
        resultado_cores = self.backend.processar_tentativa(guess)
        self.view.pintar_resultado(linha_para_pintar, guess, resultado_cores)

        # Fechar o jogo
        if guess == self.backend.palavra_secreta_norm:
            self._finalizar_jogo(vitoria=True)

        elif self.backend.tentativa_atual >= config.MAX_TENTATIVAS:
            self._finalizar_jogo(vitoria=False)

        else:
            self.coluna_atual = 0
            self.palavra_digitada = [""] * config.TAMANHO_PALAVRA
            self.view.destacar_linha(self.backend.tentativa_atual)

    def _finalizar_jogo(self, vitoria):
        self.jogo_acabou = True

        # Salva estatística
        self.backend.registrar_fim_jogo(vitoria)

        # Não tira o delay
        tempo_delay = 600
        self.root.after(tempo_delay, lambda: self.view.mostrar_estatisticas(
            vitoria,
            self.backend.palavra_secreta,
            self.backend.stats
        ))