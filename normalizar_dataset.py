import csv
import unicodedata
import random
import os

# Configurações
ARQUIVO_ENTRADA = 'termo.txt'
SAIDA_SORTEIO = 'DataSet_Sorteio.csv'
SAIDA_OBSCURO = 'DataSet_obscuro.csv'
META_MINIMA_SORTEIO = 2000


def normalizar(texto):
    """Remove acentos e coloca em minúsculas para comparação."""
    if not texto: return ""
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower()


def eh_palavra_de_sorteio(palavra):
    """
    Retorna True se a palavra parece ser um bom candidato para a resposta do dia.
    Retorna False se parecer verbo conjugado ou plural simples.
    """
    p_norm = normalizar(palavra)

    # --- WHITELIST (Salva palavras que parecem verbos/plurais mas são substantivos) ---
    excecoes_boas = {
        # Terminam em 's' ou 'u' ou 'i' mas são boas
        'lapis', 'tenis', 'virus', 'atlas', 'humus', 'bonus', 'onibus', 'venus',
        'caqui', 'pneu', 'ceu', 'reu', 'grau', 'bau', 'tchau', 'museu', 'penis'
        # Terminam em 'sse' mas são substantivos (para não cair no filtro abaixo)
        'posse', 'classe', 'tosse', 'musse', 'passe'
    }

    if p_norm in excecoes_boas:
        return True

    # --- BLACKLIST (Filtros de terminações verbais e plurais) ---

    # 1. Filtra Plurais terminados em 's'
    if p_norm.endswith('s'):
        return False

    # 2. Filtra terminações verbais indesejadas
    terminacoes_ruins = (
        'ram', 'mos', 'ste', 'ais', 'eis', 'vam',  # Passados/Plurais
        'u',  # Passado 3ª pessoa (falou)
        'i',  # Passado 1ª pessoa (falei)
        'em', 'am',  # 3ª pessoa plural
        'sse'  # NOVO: Filtra subjuntivo (fosse, disse, visse, risse)
    )

    if p_norm.endswith(terminacoes_ruins):
        return False

    return True


def processar_listas():
    # 1. Leitura e Deduplicação
    if not os.path.exists(ARQUIVO_ENTRADA):
        print(f"Erro: {ARQUIVO_ENTRADA} não encontrado.")
        return

    with open(ARQUIVO_ENTRADA, 'r', encoding='utf-8') as f:
        linhas = [l.strip() for l in f.readlines() if l.strip()]

    unicas = {}

    print("Processando e deduplicando...")
    for palavra in linhas:
        chave = normalizar(palavra)
        if len(chave) == 5:
            if chave not in unicas:
                unicas[chave] = palavra

    todas_palavras = list(unicas.values())

    # 2. Classificação
    lista_sorteio = []
    lista_obscura = []

    for palavra in todas_palavras:
        if eh_palavra_de_sorteio(palavra):
            lista_sorteio.append(palavra)
        else:
            lista_obscura.append(palavra)

    # 3. Validação da Meta (Minimo 2000)
    qtd_atual = len(lista_sorteio)

    if qtd_atual < META_MINIMA_SORTEIO:
        faltam = META_MINIMA_SORTEIO - qtd_atual
        print(f"Aviso: A heurística encontrou apenas {qtd_atual} palavras boas para sorteio.")
        print(f"Completando com {faltam} palavras da lista obscura para atingir a meta...")

        # Embaralha as obscuras para pegar aleatórias
        random.shuffle(lista_obscura)

        # Move palavras da obscura para sorteio
        resgatadas = lista_obscura[:faltam]
        lista_obscura = lista_obscura[faltam:]  # Remove as que foram movidas
        lista_sorteio.extend(resgatadas)

    # Embaralha a lista final de sorteio
    random.shuffle(lista_sorteio)

    # Ordena a lista obscura (apenas para ficar organizado no CSV)
    lista_obscura.sort()

    # 4. Salvando os arquivos
    print(f"\nSalvando arquivos...")

    # Salva Sorteio
    with open(SAIDA_SORTEIO, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # writer.writerow(['palavra']) # Remova o # se quiser cabeçalho
        for p in lista_sorteio:
            writer.writerow([p])

    # Salva Obscuro
    with open(SAIDA_OBSCURO, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # writer.writerow(['palavra']) # Remova o # se quiser cabeçalho
        for p in lista_obscura:
            writer.writerow([p])

    print("-" * 30)
    print(f"Concluído!")
    print(f"Arquivo '{SAIDA_SORTEIO}': {len(lista_sorteio)} palavras.")
    print(f"Arquivo '{SAIDA_OBSCURO}': {len(lista_obscura)} palavras.")


if __name__ == "__main__":
    processar_listas()