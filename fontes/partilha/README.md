# Apresentações: partilha no caso discreto (MACS, 10.º ano)

Três apresentações reveal.js feitas com Quarto (1.9). Cada uma segue a mesma estrutura: exemplo introdutório, generalização e descrição do método, e 5 problemas com resolução.

| Ficheiro | Método | Exemplo introdutório | Problemas |
|---|---|---|---|
| `01_licitacoes_secretas.qmd` | Licitações secretas (Knaster) | Herança dos avós: casa e iate, 3 irmãos | 5 itens de **Exame Nacional** (adaptados): 2026 Ép. esp. (jornal da escola) · 2015 1.ª F (agência de viagens, com alínea extra sobre inveja) · 2010 1.ª F (4 herdeiras) · 2022 1.ª F (licitação desconhecida *a*) · 2021 Ép. esp. (partes de 50 %, 30 % e 20 %) |
| `02_ajuste_na_partilha.qmd` | Ajuste na Partilha (*Adjusted Winner*, Brams–Taylor) | Divórcio Madalena/Gonçalo | Animais da avó (ficha) · empate marido/esposa (ficha) · Leonido/Marco (teste 2015) · Paulo/Rosa (mini-teste) · mentir compensa? (Brams–Taylor) |
| `03_marcadores.qmd` | Marcadores (Lucas) | 9 doces, Teodoro/Vanessa/Rudy (ficha) | Ler marcas (ficha) · empate que muda o excedente · colocar marcas (teste 2015) · inveja · marcas aproximadas (Tannenbaum) |

A última apresentação termina com um quadro que compara os três métodos.

## Ficheiros partilhados
- `_quarto.yml`: opções comuns (tema, quadro, multiplex, transições, rodapé).
- `estilo.scss`: tema visual «clean», ao jeito do projeto Matemática A...Z:
  - fundo branco e cores do tema *white* do Reveal.js;
  - títulos azuis (#1d4ed8) em Source Sans Pro;
  - capa com a faixa escura do weblog (#170C3A, letra Jost);
  - diapositivos de capítulo («O método», «Problemas») em Palatino, com sublinhado azul;
  - destaques laranja, azul e vermelho, como no Matemática A...Z.

  O tema anterior (bege, Fraunces/Nunito) está guardado em `_ferramentas/estilo_anterior.scss`.
- `figs/Homem_Guitarra_CG_logo.png`: logótipo do rodapé das fichas e testes (copiado de `Teoria_eleicoes/figs`). Está embutido no `estilo.scss` e aparece no canto superior esquerdo de todos os diapositivos.

## Atenção: não editar `01_licitacoes_secretas.qmd` diretamente
`01_licitacoes_secretas.qmd` é **gerado**. No exemplo introdutório e na resolução dos 5 problemas, a tabela de cálculos fica sempre à esquerda, e as linhas do passo em curso aparecem destacadas. Os passos já feitos ficam normais; os que faltam aparecem a cinzento e vazios.

1. Editar `_fonte_licitacoes/_01_licitacoes_secretas_modelo.qmd`. Cada `{{T:caso:estados}}` é uma tabela:
   - `intro`, `e1` … `e5` (itens de exame; `e4a` é a tabela do E4 com a licitação desconhecida *a*);
   - os problemas anteriores (quatro irmãos, tarefas, empate, espreitar…) estão guardados em `_fonte_licitacoes/problemas_anteriores.qmd`, e as suas tabelas (`p1` … `p5b`) continuam definidas no `tabela.py`;
   - estados: 1 licitações · 2 total e parte justa · 3 bens · 4 alocação provisória · 5 excedente · 6 alocação final · 7 valor para o próprio · 8 linha extra (no E2, valor de cada parte para a Alice);
   - podem ser um número (`4`), uma lista (`3,4`) ou um intervalo (`3-6`).
2. Os dados estão em `_fonte_licitacoes/tabela.py`. Os cálculos são feitos em frações exatas e verificados.
3. Correr `python3 _fonte_licitacoes/tabela.py` e depois `quarto render 01_licitacoes_secretas.qmd`.

Se mudar os dados, o texto explicativo à direita, que está no modelo, também tem de ser atualizado.

## Atenção: não editar `02_ajuste_na_partilha.qmd` diretamente
É **gerado** (desde 15/11/2026) a partir de `_fonte_ajuste/_02_ajuste_na_partilha_modelo.qmd` com `python3 _fonte_ajuste/tabela_aw.py`.
- Cada `{{A:caso:estados}}` é a tabela de cálculos sempre presente.
- Casos: `intro`, `camp`, `p1` … `p4`, `p5h`, `p5m`, `p5a`.
- Estados: 1 pontos · 2 1.ª fase · 3 ordem do ajuste (razões) · 4 passar por inteiro? · 5 equação · 6 partilha e pontos finais · 7 parte do outro · 8 extra (pontos verdadeiros no P5).
- Convenção: $x$ = fração do bem dividido que **passa** para o outro jogador ($V - vx = P + px$). Nunca usar $1 - x$.

## Atenção: não editar `03_marcadores.qmd` diretamente
`03_marcadores.qmd` é **gerado**. Para mudar o texto ou as linhas de doces:
1. Editar `_fonte_marcadores/_03_marcadores_modelo.qmd`.
2. Se for preciso mudar as linhas de itens, editar também `_fonte_marcadores/linhas.py`. Cada `{{L:nome}}` do modelo corresponde a uma linha definida em `LINHAS`. Cada `{{S:caso:estados}}` é a tabela de síntese sempre presente (jogadores × parte justa, marcas, recebe, vale), definida com `def_sintese`. Os estados são: 1 marcas e parte justa; depois um estado por atribuição, pela ordem; o excedente fica no estado da última atribuição; segue-se a escolha do excedente.
3. Correr `python3 _fonte_marcadores/linhas.py`.
4. Fazer `quarto render 03_marcadores.qmd`.

## Compilar e apresentar
```bash
cd ~/site/macs-a-z/fontes/partilha
quarto render                          # gera as três apresentações (.html + pasta _files)
quarto preview 01_licitacoes_secretas.qmd   # abre no browser com servidor local
```
- **Diapositivos interativos** («Experimenta!», feitos com Observable): só funcionam através de um servidor, por exemplo `quarto preview` ou `python3 -m http.server`. Abrindo o `.html` com duplo clique, ficam em branco. Precisam de internet (bibliotecas e tipos de letra).
- **Teclas úteis:**
  - `C`: escrever por cima do diapositivo.
  - `B`: quadro branco.
  - `S`: notas do orador. Há notas com sugestões e fontes nalguns diapositivos.
  - `M`: menu.
  - `F`: ecrã inteiro.
  - `E`: modo de impressão para PDF, abrindo no Chrome com `?print-pdf`.
- **Multiplex** (os alunos seguem os diapositivos do professor nos seus aparelhos):
  - O professor abre `…-speaker.html`.
  - Os alunos abrem o `.html` normal.
  - Só funciona se a versão dos alunos estiver alojada num servidor, por exemplo GitHub Pages ou Quarto Pub.
  - O servidor de sincronização é o definido pelo Quarto (`multiplex.up.railway.app`).
- O quadro (chalkboard) impede gerar a apresentação num ficheiro único: é preciso manter a pasta `_files` junto do `.html`.

## Verificação
Todos os resultados numéricos foram calculados com scripts Python em frações exatas, incluindo os casos de empate. O código Python mostrado nos diapositivos também foi executado. Os dados vêm sobretudo das fichas e testes em `Divisao_Justa/Materiais` (ESA) e foram adaptados: nomes, emojis, contexto. Os problemas de empate (licitações) e de inveja (marcadores) foram construídos para a aula.

## Erros encontrados nas fontes (para corrigir materiais antigos)
- **Teste de 06/12/2018 (V2.5), questão 5 (Mordecai/Rigby, Ajuste na Partilha):** as quatro opções usam **53** em vez de **55**, por isso nenhuma está correta. A opção correta seria `70 − 20p = 55 + 15p` (p = 3/7). As versões de 2015 estão certas.
- **`Aplicaçaometodospartilha.pdf`:**
  - No Ajuste na Partilha, faz o ajuste pelo gato (razão 2,5) em vez do apartamento (1,5).
  - Escreve «Pedro» em vez de «Gonçalo».
  - Nas licitações secretas, afirma que o método é «livre de inveja», o que é falso.
- **`Teoria das Partilhas.pdf`, p. 14:** «145 000 € − 120 000 € = 265 000 €» deve ser **+**.
- **Massoud, Israel/Palestina (`Ron Cytron/2-b.pdf`):** a fração da Cisjordânia para Israel é 12/43, não 2/7.

## Itens de exame
`~/MACS_26_27/Partilha/divisao_justa.pdf` (compilação de mat.absolutamente.net; fica fora do site) tem 26 itens de exame sobre partilha.
- **Licitações secretas:** 2026 Ép. esp. · 2025 2.ª F · 2022 1.ª F · 2021 Ép. esp. · 2021 1.ª F · 2019 2.ª F (aluguer de espaços) · 2018 Ép. esp. · 2017 2.ª F · 2015 1.ª F · 2013 2.ª F (com Hondt) · 2011 2.ª F (40/30/30) · 2010 1.ª F · 2008 1.ª F.
- **Ajuste na Partilha:** 2025 Ép. esp. · 2023 1.ª F · 2021 1.ª F · 2020 1.ª F · 2018 1.ª F · 2016 Ép. esp. · 2015 Ép. esp. · 2015 2.ª F.
- **Marcadores:** 2026 2.ª F · 2024 Ép. esp. · 2019 1.ª F.

Os diapositivos «O algoritmo em Python» têm um botão **▶ Abrir e correr na app Python**, que abre o programa na app [Python no navegador](https://karlosgomes.github.io/apps-matematica/python/) (link `#codigo=…&nome=…`). Se mudar o código de um destes diapositivos, correr `python3 _ferramentas/links_python.py` antes de gerar e compilar, para atualizar os links.

`_ferramentas/capturas.py` tira capturas de ecrã dos diapositivos, para rever o aspeto sem abrir o browser.

## Publicação no site (MACS A...Z)
Estas fontes estão em `~/site/macs-a-z/fontes/partilha/`, desde 15/11/2026; antes estavam em `~/MACS_26_27/Partilha/apresentacoes`. As apresentações publicadas ficam em `~/site/macs-a-z/partilha/`.
- Atualizar: `./_ferramentas/publicar_site.sh`. O script refaz as tabelas, as linhas e os links Python, compila com o perfil `site` e copia o resultado para `../../partilha/`.
- O perfil `site` (`_quarto-site.yml` + `_ferramentas/site/`) acrescenta a barra do weblog e a contagem de visitas (GoatCounter), e tira o logótipo dos diapositivos, porque já está na barra.
- As versões do professor (`partilha/*-speaker.html`, para o multiplex) ficam ao lado das publicadas, mas estão no `.gitignore` e nunca vão para o GitHub. O script confirma isso no fim.
- Para publicar: `git commit` e `git push` em `~/site/macs-a-z`. O multiplex só funciona se a versão online for a da mesma compilação que o `-speaker.html` (o `id` muda quando se recompila do zero).
- Pré-visualizar enquanto se edita: `quarto preview 01_licitacoes_secretas.qmd`. Os `.html` que isto cria aqui estão no `.gitignore`.
