"""Gera o HTML das linhas de itens com marcas (método dos marcadores).
Uso: python3 linhas.py  -> lê _03_marcadores_modelo.qmd e escreve ../03_marcadores.qmd
No modelo, {{L:nome}} é substituído pela linha definida em LINHAS."""
import re, pathlib

def lab(s):
    return f"{s[0]}<sub>{s[1:]}</sub>"

def linha(itens, marcas=(), dono=None, sobras=(), compacta=False, idp="L", letra=False):
    """itens: lista de emojis/letras; marcas: lista (rotulo, classe, posicao) — posição = depois do item k;
    dono: dict item->classe; sobras: itens do excedente."""
    dono = dono or {}
    n = len(itens)
    por_pos = {}
    for r, c, p in marcas:
        por_pos.setdefault(p, []).append((r, c))
    h = [f'<div class="linha{" compacta" if compacta else ""}">']
    for k in range(1, n + 1):
        cls = dono.get(k, "sobra" if k in sobras else "")
        e = f'<span class="e{" letra" if letra else ""}">{itens[k-1]}</span>'
        h.append(f'<div class="it {cls}" data-id="{idp}it{k}">{e}<span class="n">{k}</span></div>')
        if k < n:
            if k in por_pos:
                ls = "".join(f'<span class="mk {c}" data-id="{idp}mk{r}">{lab(r)}</span>' for r, c in por_pos[k])
                h.append(f'<div class="gap"><div class="barras">{ls}</div><div class="barra" data-id="{idp}b{k}"></div></div>')
            else:
                h.append('<div class="gap"></div>')
    h.append('</div>')
    return "```{=html}\n" + "".join(h) + "\n```"

def M(prefixo, classe, posicoes):
    return [(f"{prefixo}{j+1}", classe, p) for j, p in enumerate(posicoes)]

def faixa(a, b, c):
    return {k: c for k in range(a, b + 1)}

S, C, K = "🍫", "🍬", "🍭"
doces = [S, S, S, C, C, C, K, K, K]
T, V, R = M("T", "p1", [3, 6]), M("V", "p2", [4, 5]), M("R", "p3", [2, 5])
LINHAS = {
    "i0": linha(doces, idp="i"),
    "i1": linha(doces, T, idp="i"),
    "i2": linha(doces, T + V, idp="i"),
    "i3": linha(doces, T + V + R, idp="i"),
    "i4": linha(doces, T + V, dono=faixa(1, 2, "p3"), idp="i"),
    "i5": linha(doces, T, dono={**faixa(1, 2, "p3"), 5: "p2"}, idp="i"),
    "i6": linha(doces, [], dono={**faixa(1, 2, "p3"), 5: "p2", **faixa(7, 9, "p1")}, sobras={3, 4, 6}, idp="i"),
    "i7": linha(doces, [], dono={**faixa(1, 3, "p3"), 4: "p2", 5: "p2", **faixa(6, 9, "p1")}, idp="i"),
}
# Problema 1 (16 itens)
g16 = ["🎁"] * 16
P1M = M("A", "p1", [1, 6, 12]) + M("B", "p2", [3, 8, 15]) + M("C", "p3", [2, 9, 14]) + M("D", "p4", [2, 7, 12])
LINHAS["p1v"] = linha(g16, [], compacta=True, idp="a")
LINHAS["p1m"] = linha(g16, P1M, compacta=True, idp="a")
LINHAS["p1s"] = linha(g16, P1M, dono={1: "p1", **faixa(3, 7, "p4"), **faixa(10, 14, "p3"), 16: "p2"},
                      sobras={2, 8, 9, 15}, compacta=True, idp="a")
# Problema 2 (joias, 20 itens, empate)
j20 = ["💎"] * 20
P2M = M("A", "p1", [5, 8, 14]) + M("B", "p2", [5, 9, 14]) + M("C", "p3", [3, 8, 15]) + M("D", "p4", [4, 7, 13])
LINHAS["p2m"] = linha(j20, P2M, compacta=True, idp="b")
LINHAS["p2B"] = linha(j20, P2M, dono={**faixa(1, 3, "p3"), **faixa(5, 7, "p4"), **faixa(10, 14, "p2"), **faixa(15, 20, "p1")},
                      sobras={4, 8, 9}, compacta=True, idp="b")
LINHAS["p2A"] = linha(j20, P2M, dono={**faixa(1, 3, "p3"), **faixa(5, 7, "p4"), **faixa(9, 14, "p1"), **faixa(15, 20, "p2")},
                      sobras={4, 8}, compacta=True, idp="b")
# Problema 3 (Sérgio, Leonardo, Paula)
l3 = [S, C, C, C, K, K, S, S, K]
P3M = M("S", "p1", [2, 3]) + M("L", "p2", [5, 7]) + M("P", "p3", [3, 6])
LINHAS["p3v"] = linha(l3, [], idp="c")
LINHAS["p3m"] = linha(l3, P3M, idp="c")
LINHAS["p3s"] = linha(l3, P3M, dono={**faixa(1, 2, "p1"), **faixa(4, 6, "p3"), **faixa(8, 9, "p2")}, sobras={3, 7}, idp="c")
# Problema 4 (Rita, Bruno, Carla)
P4M = M("R", "p1", [7, 8]) + M("B", "p2", [2, 4]) + M("C", "p3", [3, 6])
LINHAS["p4v"] = linha(doces, [], idp="d")
LINHAS["p4m"] = linha(doces, P4M, idp="d")
LINHAS["p4s"] = linha(doces, P4M, dono={**faixa(1, 2, "p2"), **faixa(4, 6, "p3"), 9: "p1"}, sobras={3, 7, 8}, idp="d")
# Problema 5 (banda desenhada, marcas aproximadas)
bd = list("WSSGSWWBGGGSGSGSBB")
P5M = M("Q", "p1", [4, 7, 13]) + M("R", "p2", [5, 8, 14]) + M("S", "p3", [5, 9, 15]) + M("T", "p4", [5, 9, 14])
LINHAS["p5m"] = linha(bd, P5M, compacta=True, letra=True, idp="e")
LINHAS["p5s"] = linha(bd, P5M, dono={**faixa(1, 4, "p1"), **faixa(6, 8, "p2"), **faixa(10, 14, "p4"), **faixa(16, 18, "p3")},
                      sobras={5, 9, 15}, compacta=True, letra=True, idp="e")

if __name__ == "__main__":
    aqui = pathlib.Path(__file__).parent
    modelo = (aqui / "_03_marcadores_modelo.qmd").read_text()
    def sub(m):
        return LINHAS[m.group(1)]
    saida = re.sub(r"\{\{L:(\w+)\}\}", sub, modelo)
    falta = re.findall(r"\{\{L:(\w+)\}\}", saida)
    assert not falta, falta
    (aqui.parent / "03_marcadores.qmd").write_text(saida)
    print("escrito 03_marcadores.qmd")
