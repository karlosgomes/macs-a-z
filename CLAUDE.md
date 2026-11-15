# MACS A...Z

Site com as apresentações de MACS (10.º ano, currículo português), irmão do Matemática A...Z e das Apps de Matemática. Texto sempre em português europeu.

## Estrutura
- `index.html` — página inicial (HTML simples, sem build): menu igual ao do weblog (com «MACS A...Z» ativo), faixa escura #170C3A com o título (Jost 600 34px, 126px), e um bloco por tema com cartões (estilo das Apps de Matemática: borda superior escura, título laranja #EE6A24). Tema novo → novo `h2` + `h3` + `.grelha`.
- `partilha/` — **gerado, não editar aqui**: as três apresentações de partilha (caso discreto) e `partilha/libs/` (bibliotecas partilhadas pelas três).
- `img/logo.png` — logótipo.

## De onde vêm as apresentações
As fontes estão em `~/MACS_26_27/Partilha/apresentacoes/` (Quarto, ver o README.md de lá). Para atualizar o site:
```
~/MACS_26_27/Partilha/apresentacoes/_ferramentas/publicar_site.sh
```
O script gera as tabelas/linhas e os links para a app Python, faz `quarto render --profile site` (perfil `_quarto-site.yml`: acrescenta a barra do weblog e esconde o logótipo dos diapositivos), copia os `.html` para `partilha/`, junta as bibliotecas em `partilha/libs/` e **não copia os `-speaker.html`** (têm o segredo do multiplex; ficam só no computador do professor). Verifica no fim que nenhum segredo foi publicado.

Multiplex: o professor abre o `-speaker.html` local; os alunos abrem a página publicada e seguem os diapositivos.

## Publicação
- Repositório: https://github.com/karlosgomes/macs-a-z (ramo `main`), GitHub Pages a partir da raiz (desde 2026-11-15).
- Publicar = `git commit` + `git push`. Pedir confirmação ao utilizador antes de fazer push.
- O item «MACS A...Z» está nos menus do weblog, do Matemática A...Z e das Apps de Matemática (2026-11-15). Se o menu do weblog mudar, atualizar à mão a barra do `index.html` daqui e `~/MACS_26_27/Partilha/apresentacoes/_ferramentas/site/barra.html`.
