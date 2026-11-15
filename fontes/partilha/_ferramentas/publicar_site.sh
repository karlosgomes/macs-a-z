#!/bin/bash
# Gera as apresentações de Partilha e põe-nas em ~/site/macs-a-z/partilha/ (a pasta publicada).
# - as bibliotecas das três apresentações ficam numa só pasta partilha/libs/;
# - as versões do professor (-speaker.html, com o segredo do multiplex) também ficam em partilha/,
#   mas estão no .gitignore: nunca vão para o GitHub. O script confirma que nenhum segredo fica
#   num ficheiro que o git vá publicar.
# Não faz commit nem push.
set -euo pipefail
AQUI="$(cd "$(dirname "$0")/.." && pwd)"          # .../macs-a-z/fontes/partilha
SITE="$(cd "$AQUI/../.." && pwd)"                 # .../macs-a-z
DEST="$SITE/partilha"
cd "$AQUI"
python3 _ferramentas/links_python.py
python3 _fonte_licitacoes/tabela.py
python3 _fonte_marcadores/linhas.py
rm -rf _site
quarto render --profile site
mkdir -p "$DEST"
rm -rf "${DEST:?}"/*.html "${DEST:?}"/libs
mkdir -p "$DEST/libs"
for f in _site/0*.html; do
  b=$(basename "$f" .html); base=${b%-speaker}
  [ -d "_site/${base}_files/libs" ] && cp -r "_site/${base}_files/libs/." "$DEST/libs/"
  sed "s#${base}_files/libs/#libs/#g" "$f" > "$DEST/$b.html"
done
# o Quarto escreve as versões do professor (-speaker.html) junto das fontes, e não em _site
for f in 0*-speaker.html; do
  [ -e "$f" ] || continue
  b=$(basename "$f" .html); base=${b%-speaker}
  sed "s#${base}_files/libs/#libs/#g" "$f" > "$DEST/$b.html" && rm -f "$f"
done
rm -rf _site
# nenhum segredo do multiplex em ficheiros que o git publica
cd "$SITE"
for f in partilha/*.html; do
  if grep -q '"secret":"[0-9a-f]' "$f" && ! git check-ignore -q "$f"; then
    echo "ERRO: $f tem o segredo do multiplex e não está no .gitignore!"; exit 1
  fi
done
du -sh "$DEST"; ls "$DEST"
