import csv
import random
import os
from unidecode import unidecode
from src import config


class TermoBackend:
    def __init__(self):
        self.palavras_alvo = self._carregar_csv(config.FILE_SORTEIO)
        self.palavras_obscuras = self._carregar_csv(config.FILE_OBSCURO)

        if not self.palavras_alvo:
            self.palavras_alvo = config.BACKUP_SORTEIO

        self.palavras_totais = set(self.palavras_alvo + self.palavras_obscuras)
        self.stats = self._carregar_estatisticas()

        self.palavra_secreta = ""
        self.palavra_secreta_norm = ""
        self.tentativa_atual = 0

    def _carregar_csv(self, caminho):
        lista = []
        if os.path.exists(caminho):
            try:
                with open(caminho, newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        for palavra in row:
                            p_limpa = palavra.strip().upper()
                            if len(p_limpa) == config.TAMANHO_PALAVRA and p_limpa.isalpha():
                                lista.append(p_limpa)
            except Exception:
                pass
        return lista

    def sortear_palavra(self):
        self.palavra_secreta = random.choice(self.palavras_alvo).upper()
        self.palavra_secreta_norm = unidecode(self.palavra_secreta)
        self.tentativa_atual = 0

    def palavra_existe(self, tentativa):
        tentativa_norm = unidecode(tentativa).upper()
        # Verifica se existe no conjunto total (otimizado)
        return any(unidecode(w) == tentativa_norm for w in self.palavras_totais)

    def processar_tentativa(self, tentativa):
        """Calcula cores e avança a rodada."""
        self._registrar_frequencia_palavra(tentativa)

        guess_norm = list(unidecode(tentativa).upper())
        secret_list = list(self.palavra_secreta_norm)  # Cópia para gastar as letras

        resultado_cores = [config.COR_AUSENTE] * config.TAMANHO_PALAVRA

        # Passo 1: VERDES (Prioridade Máxima)
        for i in range(config.TAMANHO_PALAVRA):
            if guess_norm[i] == secret_list[i]:
                resultado_cores[i] = config.COR_ACERTO
                secret_list[i] = None  # Consome a letra da secreta
                guess_norm[i] = None  # Consome a letra do chute

        # Passo 2: AMARELOS
        for i in range(config.TAMANHO_PALAVRA):
            if guess_norm[i] is not None:  # Se não foi verde
                letra = guess_norm[i]
                if letra in secret_list:
                    resultado_cores[i] = config.COR_LUGAR_ERRADO
                    # Consome a primeira ocorrência disponível dessa letra
                    secret_list[secret_list.index(letra)] = None

        # Agora sim avançamos a linha
        self.tentativa_atual += 1
        return resultado_cores

    # --- ESTATÍSTICAS ---
    def _default_stats(self):
        return {
            "jogos": 0, "vitorias": 0, "sequencia_atual": 0, "melhor_sequencia": 0,
            "distribuicao": {str(i): 0 for i in range(1, config.MAX_TENTATIVAS + 1)},
            "palavras_frequentes": {}
        }

    def _carregar_estatisticas(self):
        stats = self._default_stats()
        if os.path.exists(config.STATS_FILE):
            try:
                with open(config.STATS_FILE, mode='r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) < 2: continue
                        key, val = row[0], row[1]
                        if key in ['jogos', 'vitorias', 'sequencia_atual', 'melhor_sequencia']:
                            stats[key] = int(val)
                        elif key.startswith('dist_'):
                            stats['distribuicao'][key.split('_')[1]] = int(val)
                        elif key.startswith('freq_'):
                            stats['palavras_frequentes'][key[5:]] = int(val)
            except Exception:
                pass
        return stats

    def _salvar_estatisticas(self):
        try:
            with open(config.STATS_FILE, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for k in ['jogos', 'vitorias', 'sequencia_atual', 'melhor_sequencia']:
                    writer.writerow([k, self.stats[k]])
                for k, v in self.stats['distribuicao'].items():
                    writer.writerow([f'dist_{k}', v])
                for k, v in self.stats['palavras_frequentes'].items():
                    writer.writerow([f'freq_{k}', v])
        except Exception:
            pass

    def registrar_fim_jogo(self, vitoria):
        self.stats["jogos"] += 1
        if vitoria:
            self.stats["vitorias"] += 1
            self.stats["sequencia_atual"] += 1
            if self.stats["sequencia_atual"] > self.stats["melhor_sequencia"]:
                self.stats["melhor_sequencia"] = self.stats["sequencia_atual"]
            # Usa tentativa_atual (que já é o índice real 1-6 pois foi incrementado)
            t_str = str(self.tentativa_atual)
            if t_str in self.stats["distribuicao"]:
                self.stats["distribuicao"][t_str] += 1
        else:
            self.stats["sequencia_atual"] = 0
        self._salvar_estatisticas()

    def _registrar_frequencia_palavra(self, palavra):
        p = palavra.upper()
        self.stats["palavras_frequentes"][p] = self.stats["palavras_frequentes"].get(p, 0) + 1
        self._salvar_estatisticas()