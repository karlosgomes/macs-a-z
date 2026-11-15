# MACS A...Z

Site com as apresentações de MACS (10.º ano, currículo português), irmão do Matemática A...Z e das Apps de Matemática. Texto sempre em português europeu.

## Estrutura
- `index.html` — página inicial (HTML simples, sem build): menu igual ao do weblog (com «MACS A...Z» ativo), faixa escura #170C3A com o título (Jost 600 34px, 126px), e um bloco por tema com cartões (estilo das Apps de Matemática: borda superior escura, título laranja #EE6A24). Tema novo → novo `h2` + `h3` + `.grelha`.
- `partilha/` — **gerado, não editar aqui**: as três apresentações de partilha (caso discreto), `partilha/libs/` (bibliotecas partilhadas pelas três) e as versões do professor `*-speaker.html` (só locais, no `.gitignore`).
- `img/logo.png` — logótipo.

## Fontes
- `fontes/partilha/`: **fontes das apresentações de Partilha** (Quarto). Estão aqui desde 15/11/2026; antes estavam em `~/MACS_26_27/Partilha/apresentacoes`. O `README.md` de lá explica tudo:
  - os ficheiros gerados por Python: `01_licitacoes_secretas.qmd` sai de `_fonte_licitacoes/_01_licitacoes_secretas_modelo.qmd` + `tabela.py`, e `03_marcadores.qmd` sai de `_fonte_marcadores/_03_marcadores_modelo.qmd` + `linhas.py`;
  - o tema `estilo.scss`;
  - os links para a app Python (`_ferramentas/links_python.py`).
- Atualizar o site: `fontes/partilha/_ferramentas/publicar_site.sh`.
  - Gera as tabelas, as linhas e os links, e faz `quarto render --profile site`. O perfil `_quarto-site.yml` acrescenta a barra do weblog e esconde o logótipo dos diapositivos.
  - Põe o resultado em `partilha/`, com as bibliotecas juntas em `partilha/libs/`.
  - As versões do professor (`partilha/*-speaker.html`, com o segredo do multiplex) ficam ao lado, mas estão no `.gitignore`. O script verifica que nenhum segredo fica num ficheiro publicável.
- Multiplex: o professor abre o `-speaker.html` local; os alunos abrem a página publicada. Depois de recompilar, publicar, porque o `id` pode mudar.
- Materiais de apoio que não são do site (o PDF dos itens de exame, fichas) ficam em `~/MACS_26_27/Partilha`.

## Publicação
- Repositório: https://github.com/karlosgomes/macs-a-z (ramo `main`), GitHub Pages a partir da raiz (desde 2026-11-15).
- Publicar = `git commit` + `git push`. Pedir confirmação ao utilizador antes de fazer push.
- O item «MACS A...Z» está nos menus do weblog, do Matemática A...Z e das Apps de Matemática (2026-11-15). Se o menu do weblog mudar, atualizar à mão a barra do `index.html` daqui e `fontes/partilha/_ferramentas/site/barra.html`.
