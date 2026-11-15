#!/bin/bash
# Gera o livro MACS A...Z (index.qmd + capítulos) e põe-no na raiz de ~/site/macs-a-z
# (index.html + libs/). Não faz commit nem push.
set -euo pipefail
AQUI="$(cd "$(dirname "$0")/.." && pwd)"          # .../macs-a-z/fontes
SITE="$(cd "$AQUI/.." && pwd)"                    # .../macs-a-z
cd "$AQUI"
python3 _ferramentas/links_python.py
python3 _fonte_licitacoes/tabela.py
python3 _fonte_ajuste/tabela_aw.py
python3 _fonte_marcadores/linhas.py
rm -rf _site
quarto render
rm -rf "${SITE:?}/libs"
mkdir -p "$SITE/libs"
cp -r _site/index_files/libs/. "$SITE/libs/"
sed "s#index_files/libs/#libs/#g" _site/index.html > "$SITE/index.html"
rm -rf _site
du -sh "$SITE/libs"; ls "$SITE"
