"""Acrescenta (ou atualiza), a seguir a cada bloco de código Python dos diapositivos, um link que abre
o programa na app «Python no navegador» (https://karlosgomes.github.io/apps-matematica/python/).
O link usa o formato da app: #codigo=<base64 do texto em UTF-8>&nome=<nome.py>.
Uso: python3 _ferramentas/links_python.py   (corre sobre os três ficheiros-fonte; é idempotente)"""
import base64, pathlib, re, urllib.parse

APP = "https://karlosgomes.github.io/apps-matematica/python/"
RAIZ = pathlib.Path(__file__).resolve().parent.parent
FONTES = {
    "_fonte_licitacoes/_01_licitacoes_secretas_modelo.qmd": "licitacoes_secretas.py",
    "02_ajuste_na_partilha.qmd": "ajuste_na_partilha.py",
    "_fonte_marcadores/_03_marcadores_modelo.qmd": "marcadores.py",
}
BLOCO = re.compile(r"(```\{\.python[^}]*\}\n)(.*?)(\n```\n)((?:\n\[[^\n]*\{\.app-python[^\n]*\}\n)*)", re.S)


def link(codigo, nome):
    b64 = base64.b64encode(codigo.encode("utf-8")).decode("ascii")
    return f"{APP}#codigo={urllib.parse.quote(b64, safe='')}&nome={urllib.parse.quote(nome)}"


for ficheiro, nome in FONTES.items():
    f = RAIZ / ficheiro
    s = f.read_text()
    def sub(m):
        codigo = m.group(2) + "\n"
        return (m.group(1) + m.group(2) + m.group(3) +
                f'\n[▶ Abrir e correr na app Python]({link(codigo, nome)}){{.app-python target="_blank"}}\n')
    novo, n = BLOCO.subn(sub, s)
    f.write_text(novo)
    print(f"{ficheiro}: {n} bloco(s)")
