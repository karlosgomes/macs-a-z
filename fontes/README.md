# MACS A...Z: fontes do livro de apresentações

O MACS A...Z é uma só apresentação Reveal.js, feita com Quarto (1.9), organizada como o Matemática A...Z. Começa com uma capa e um índice, e cada capítulo divide-se em subcapítulos.

```
capa → índice → Capítulo 1 · Divisão Justa
                  1.1 Licitações secretas · Resumo (↓ diapositivos) → Problemas (↓ lista e problemas)
                  1.2 Ajuste na Partilha  · Resumo → Problemas
                  1.3 Marcadores          · Resumo → Problemas
                  Síntese: os três métodos
```

- **Navegação:** **→** passa de secção em secção e **↓** desce dentro de cada secção (`navigation-mode: vertical`). Cada diapositivo tem um link de regresso: «↩ índice» nos resumos e nas aberturas, «↩ problemas» nos problemas.
- **Formato:** 1600×900.
- **Links diretos:** `#/indice`, `#/lic`, `#/lic-problemas`, `#/lic-p3`, … (no endereço). Nos `.qmd`, os links internos escrevem-se `[Resumo](#lic)`, sem a barra: o Quarto acrescenta-a (com `#/lic` ficava `#//lic` e ia parar à capa)
- **Multiplex:** não é usado. As apresentações são para projetar.

## Ficheiros
| Ficheiro | O que é |
|---|---|
| `index.qmd` | Capa, índice, abertura do capítulo; inclui os corpos dos subcapítulos e a síntese |
| `_corpo_01_licitacoes.qmd`, `_corpo_02_ajuste.qmd`, `_corpo_03_marcadores.qmd` | **Gerados, não editar.** Resumo e problemas de cada método |
| `_fonte_licitacoes/_01_licitacoes_secretas_modelo.qmd` + `tabela.py` | Modelo e gerador das licitações (`{{T:caso:estados}}`) |
| `_fonte_ajuste/_02_ajuste_na_partilha_modelo.qmd` + `tabela_aw.py` | Modelo e gerador do Ajuste na Partilha (`{{A:caso:estados}}`) |
| `_fonte_marcadores/_03_marcadores_modelo.qmd` + `linhas.py` | Modelo e gerador dos marcadores (`{{L:linha}}`, `{{S:caso:estados}}`) |
| `_fonte_licitacoes/problemas_anteriores.qmd` | Problemas que saíram das licitações quando entraram os itens de exame |
| `_sintese.qmd` | Quadro final: os três métodos do caso discreto |
| `_quarto.yml`, `estilo.scss` | Configuração e tema (estilo «clean» do Matemática A...Z) |
| `_ferramentas/site/` | Barra do weblog e faixa da capa (`barra.html`, `cabecalho.html`); links de regresso e faixa só na capa (`navegacao.html`) |
| `_ferramentas/publicar_site.sh` | Gera tudo e põe `index.html` + `libs/` na raiz de `~/site/macs-a-z` |
| `_ferramentas/links_python.py` | Põe, por baixo de cada código Python, o botão «▶ Abrir e correr na app Python» (link `#codigo=…&nome=…` para a app *Python no navegador*) |
| `_ferramentas/capturas.py` | Capturas de ecrã dos diapositivos (`RAIZ=~/site/macs-a-z python3 _ferramentas/capturas.py index.html pref 1 2 3`) |

## Regras de cada subcapítulo
- **Cabeçalho do subcapítulo:** `# Título {#lic .capitulo data-rotulo="1.1 · Resumo"}`, com os diapositivos do resumo por baixo, em `##`.
- **Problemas:**
  - `# Licitações secretas · Problemas {#lic-problemas .lista-problemas}`, com a lista de links `#/lic-p1` … e depois os problemas;
  - cada enunciado tem o id: `## Problema 1 · … {#lic-p1 auto-animate=true}`.
- **Tabela de síntese sempre presente**, em todos os métodos: tabela à esquerda, com as linhas do passo em curso destacadas, e explicações e cálculos à direita.
- **Ajuste na Partilha:** $x$ é sempre a fração do bem dividido que **passa** para o outro jogador, $V - vx = P + px$. Nunca usar $1-x$.
- **Números:** todos os cálculos dos geradores são feitos em frações exatas, com verificações (`assert`) contra os resultados conhecidos.

## Compilar e publicar
```bash
cd ~/site/macs-a-z/fontes
./_ferramentas/publicar_site.sh     # gera os corpos e os links, compila e copia index.html e libs/ para ~/site/macs-a-z
quarto preview index.qmd            # pré-visualizar enquanto se edita (os ficheiros locais estão no .gitignore)
```
Para publicar: `git commit` e `git push` em `~/site/macs-a-z`. Perguntar antes ao utilizador.

- **Teclas:** C escreve por cima, B abre o quadro branco, M abre o menu, F põe em ecrã inteiro, Esc mostra todos os diapositivos.
- **«Experimenta!»:** usa Observable e funciona no site (por HTTP). Com o ficheiro aberto por duplo clique, fica em branco.

## Itens de exame
`~/MACS_26_27/Partilha/divisao_justa.pdf` (compilação de mat.absolutamente.net; fica fora do site) tem 26 itens de exame sobre partilha.

| Método | Itens |
|---|---|
| **Licitações secretas** | 2026 Ép. esp. · 2025 2.ª F · 2022 1.ª F · 2021 Ép. esp. · 2021 1.ª F · 2019 2.ª F (aluguer) · 2018 Ép. esp. · 2017 2.ª F · 2015 1.ª F · 2013 2.ª F (com Hondt) · 2011 2.ª F (40/30/30) · 2010 1.ª F · 2008 1.ª F |
| **Ajuste na Partilha** | 2025 Ép. esp. · 2023 1.ª F · 2021 1.ª F · 2020 1.ª F · 2018 1.ª F · 2016 Ép. esp. · 2015 Ép. esp. · 2015 2.ª F |
| **Marcadores** | 2026 2.ª F · 2024 Ép. esp. · 2019 1.ª F |

Os problemas das licitações são itens de exame. Os do Ajuste e dos Marcadores vêm das fichas e testes da ESA e de livros (Tannenbaum; Brams e Taylor).

## Erros encontrados nas fontes antigas
- **Teste de 06/12/2018 (V2.5), q. 5 (Ajuste na Partilha):** as opções usam 53 em vez de 55, por isso nenhuma está correta.
- **`Aplicaçaometodospartilha.pdf`:** ajusta pelo gato em vez de pelo apartamento, escreve «Pedro» em vez de «Gonçalo» e diz que as licitações são «livres de inveja».
- **`Teoria das Partilhas.pdf`, p. 14:** escreve «145 000 − 120 000 = 265 000», com o sinal trocado.
