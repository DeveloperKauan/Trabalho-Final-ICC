# Termoo em Python/Tkinter

> "O código é a tela onde a lógica pinta a experiência."

Este projeto é uma recriação artística e técnica do jogo **Wordle** (conhecido como *Termo* no Brasil), desenvolvida inteiramente em **Python 3.11+** utilizando a biblioteca nativa **Tkinter**.

---

## 📸 Visão Geral

O projeto vai além de um simples jogo de adivinhação. Ele implementa conceitos de Engenharia de Software, incluindo:

* **Arquitetura MVC (Model-View-Controller):** Para separação de responsabilidades.
* **Concorrência (Threading):** Para manter um console de debug ativo simultaneamente à interface gráfica.
* **Design System Personalizado:** Construído do zero sobre widgets nativos.
* **Persistência de Dados (CSV):** Para salvar o histórico e "memória" do jogador.

---

## 🚀 Instalação e Execução

### Pré-requisitos
* **Python 3.10** ou superior.
* Biblioteca `unidecode` (essencial para tratar a acentuação da língua portuguesa na lógica do jogo).

### Passo a Passo

1.  **Clone o repositório ou baixe os arquivos:**
    Certifique-se de que a estrutura de pastas (`src/`, `assets/`) esteja preservada.

2.  **Instale as dependências:**
    Abra seu terminal na pasta do projeto e execute:
    ```bash
    pip install unidecode
    ```

3.  **Inicie a Obra:**
    Execute o arquivo principal na raiz:
    ```bash
    python main.py
    ```

---

## 🎮 Como Jogar

### Na Interface Gráfica

* **Objetivo:** Descobrir a palavra secreta de 5 letras em até 6 tentativas.
* **Feedback Visual:**
    * 🟩 **Verde:** A letra existe e está na posição correta (A harmonia perfeita).
    * 🟨 **Amarelo:** A letra existe na palavra, mas está na posição errada (Uma nota fora do lugar).
    * ⬛ **Escuro/Cinza:** A letra não existe na palavra (O silêncio).
* **Controles:** Use o teclado físico do seu computador ou clique no teclado virtual da tela.
* **Temas:** Clique no ícone de Sol/Lua (☀/☾) no canto superior direito para alternar entre o modo *Midnight Slate* (Escuro) e *Daylight* (Claro).

### No Terminal (O Subconsciente)

Enquanto a janela do jogo está aberta, o terminal do seu editor/sistema permanece vivo e interativo. Digite os comandos abaixo para acessar os bastidores:

* `stats`: Exibe um relatório detalhado das palavras que você mais tenta (seus "vícios" de linguagem).
* `resposta`: Revela a palavra secreta atual (para testes ou momentos de desespero poético).
* `ajuda`: Mostra o manual de instruções novamente.

---

## 🏗 Arquitetura do Sistema (MVC)

O código foi  em camadas distintas para garantir que alterações sejam feitas mais facilmente.

### 1. `src/controller.py`
* **Responsabilidade:** Ouve o teclado (`<Key>`), gerencia o loop principal do Tkinter e inicializa a Thread paralela que escuta o terminal.
* **Destaque:** Implementa um sistema de "buffer" (`palavra_digitada`) que só é enviado para validação quando o usuário pressiona Enter.

### 2. `src/backend.py`
* **Gerenciamento de Datasets:** Carrega dois arquivos CSV distintos.
* **Algoritmo de Cores:** Implementa a lógica prioritária:
    1.  Identifica e trava os Verdes.
    2.  Calcula os Amarelos baseados nas letras restantes (evitando falsos positivos em letras repetidas).
    3.  Define o restante como Ausente.
* **Persistência:** Lê e escreve no `termoo_stats.csv` a cada jogada válida.

### 3. `src/view.py`
* **Estética "Seamless":** Utiliza `pack` e `grid` com espaçamentos milimétricos (`padx=1`) para criar a ilusão de uma barra de progresso sólida, removendo o visual "blocado" padrão dos botões.
* **Tradutor de Temas:** Possui um método inteligente `aplicar_tema_visual()` que percorre todos os widgets vivos, verifica suas cores atuais e as "traduz" para o novo tema selecionado, mantendo o estado do jogo.

### 4. `src/config.py` 
Arquivo estático que centraliza todas as constantes. Cores hexadecimais, fontes, caminhos de arquivo e configurações de dificuldade ficam aqui. É o que permite mudar o visual do jogo alterando apenas algumas linhas.

---

## ⚙️ Decisões Técnicas e Desafios

### A Dualidade dos Datasets (csv)
Para criar uma experiência justa mas livre, o jogo utiliza dois dicionários:
* `DataSet_Sorteio.csv` (**Target**): Uma lista curada de palavras comuns e poéticas que podem ser a resposta final.
* `DataSet_obscuro.csv` (**Input**): Uma lista vasta contendo palavras arcaicas, plurais estranhos e verbos conjugados.
> **Por que isso?** Isso permite que o jogador use seu vocabulário extenso para testar letras ("FOSSE", "IAIS"), mas garante que ele nunca perca o jogo porque a resposta era uma palavra que ninguém conhece.

### Threading e o Terminal Vivo
O maior desafio técnico foi manter o terminal aceitando inputs (`input()`) sem congelar a interface gráfica (`root.mainloop()`).
* **Solução:** O uso da biblioteca `threading` com um *daemon thread*. Isso cria uma linha de execução paralela para o terminal que morre automaticamente quando a janela principal é fechada, garantindo uma experiência fluida e sem processos zumbis.

### Tratamento de Acentos (`unidecode`)
A língua portuguesa é complexa. O usuário vê "ÉPICO", mas o computador precisa comparar "EPICO".
* **Solução:** A View exibe a string original (com acento), mas o Backend normaliza tudo via `unidecode` antes de processar a lógica matemática das cores.

---

## 📂 Estrutura de Arquivos

```text
ProjetoTermo/
│
├── main.py                  # Ponto de ignição (Entry Point)
├── README.md                # Este documento
│
├── assets/                  # Material Bruto
│   ├── DataSet_Sorteio.csv  # Palavras Alvo
│   ├── DataSet_obscuro.csv  # Palavras de Input
│   └── termoo_stats.csv     # Memória do Jogador (Gerado auto)
│
└── src/                     # Código Fonte
    ├── __init__.py          # Marcador de pacote
    ├── config.py            # Configurações e Temas
    ├── controller.py        # Controle de Fluxo e Threads
    ├── backend.py           # Regras de Negócio e Dados
    └── view.py              # Interface Gráfica (UI)
