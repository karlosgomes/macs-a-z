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


# ================================================================ tabela de síntese (sempre presente)
from fractions import Fraction as F


def fmt(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return f"{float(x):.2f}".replace(".", ",")


def segmento(itens, a, b, mostrar_itens=True):
    rng = f"{a}" if a == b else f"{a}–{b}"
    if not mostrar_itens:
        return rng
    return f"{rng} " + "".join(itens[k - 1] for k in range(a, b + 1))


def atribuir(marcas, ordem_jog, n, desempate=None):
    """método dos marcadores; devolve lista [(jogador, a, b)] pela ordem de atribuição e as sobras"""
    desempate = desempate or {}
    ativos = list(ordem_jog); N = len(ordem_jog); res = []
    for j in range(N - 1):
        mn = min(marcas[p][j] for p in ativos)
        ws = [p for p in ativos if marcas[p][j] == mn]
        v = desempate.get(j, ws[0]) if len(ws) > 1 else ws[0]
        a = 1 if j == 0 else marcas[v][j - 1] + 1
        res.append((v, a, marcas[v][j])); ativos.remove(v)
    u = ativos[0]; res.append((u, marcas[u][N - 2] + 1, n))
    usados = {k for _, a, b in res for k in range(a, b + 1)}
    return res, [k for k in range(1, n + 1) if k not in usados]


SINTESE = {}


def def_sintese(nome, jog, itens, marcas, valores=None, est_marcas=None, desempate=None, escolhas=None,
                extra=None, mostrar_itens=True, compacta=False):
    """jog: [(nome, classe)]; valores: {jogador: {item: valor}} (opcional); escolhas: [(jogador, n.º do item)]
    extra: (título da coluna, {jogador: html}) mostrado no último estado."""
    nomes = [j for j, _ in jog]
    est_marcas = est_marcas or {j: 1 for j in nomes}
    res, sobras = atribuir(marcas, nomes, len(itens), desempate)
    base = max(est_marcas.values())
    est_atr = {v: base + 1 + k for k, (v, a, b) in enumerate(res)}
    ordem_atr = {v: k + 1 for k, (v, a, b) in enumerate(res)}
    seg = {v: (a, b) for v, a, b in res}
    est_exc = base + len(res)   # o último recebe e as sobras ficam no mesmo passo
    est_fin = est_exc + 1
    dados = dict(jog=jog, itens=itens, marcas=marcas, valores=valores, est_marcas=est_marcas, est_atr=est_atr,
                 ordem_atr=ordem_atr, seg=seg, sobras=sobras, est_exc=est_exc, est_fin=est_fin, escolhas=escolhas,
                 extra=extra, mostrar_itens=mostrar_itens, compacta=compacta)
    if valores:
        tot = {j: sum(valores[j][t] for t in itens) for j in nomes}
        dados["pj"] = {j: F(tot[j], len(nomes)) for j in nomes}
        dados["vale"] = {j: sum(valores[j][itens[k - 1]] for k in range(seg[j][0], seg[j][1] + 1)) for j in nomes}
        if escolhas:
            dados["final"] = {j: dados["vale"][j] + sum(valores[j][itens[k - 1]] for q, k in escolhas if q == j) for j in nomes}
    SINTESE[nome] = dados
    return dados


def sintese(nome, estados):
    d = SINTESE[nome]; S = set(estados); mx = max(S)
    cols = ["Jogador"] + (["Parte justa"] if d["valores"] else []) + ["Marcas", "Recebe"] + \
           (["Vale"] if d["valores"] else []) + (["Com o excedente"] if d.get("final") else []) + \
           ([d["extra"][0]] if d["extra"] else [])
    est_extra = d["est_fin"] + (1 if d.get("final") else 0)
    cls_tab = "tabela-metodo marcadores" + (" quatro" if len(d["jog"]) >= 4 or d["compacta"] else "")
    h = [f'<div class="{cls_tab}" data-id="tabmetodo"><table><tr><th></th>' + "".join(f"<th>{c}</th>" for c in cols) + "</tr>"]
    for j, cls in d["jog"]:
        em, ea = d["est_marcas"][j], d["est_atr"][j]
        varios = len(set(d["est_marcas"].values())) > 1
        if ea in S or (em in S and varios) or (S == {1} and varios and d["valores"]):
            rcls = "atual"
        elif em > mx and not (mx >= 1 and d["valores"] and varios):
            rcls = "futuro"
        else:
            rcls = "feito"
        badge = f'<span class="npasso">{d["ordem_atr"][j]}</span>' if ea <= mx else ""
        vis = lambda e: e <= mx
        a, b = d["seg"][j]
        celas = [f'<span class="q {cls}"></span> {j}']
        if d["valores"]:
            celas.append(fmt(d["pj"][j]) if vis(1) else "&nbsp;")
        celas.append(", ".join(str(x) for x in d["marcas"][j]) if vis(em) else "&nbsp;")
        celas.append(segmento(d["itens"], a, b, d["mostrar_itens"]) if vis(ea) else "&nbsp;")
        if d["valores"]:
            if vis(ea):
                ok = d["vale"][j] >= d["pj"][j]
                celas.append(f'<span class="{"pos" if ok else "neg"}">{fmt(d["vale"][j])} {"✔" if ok else "✘"}</span>')
            else:
                celas.append("&nbsp;")
        if d.get("final"):
            celas.append(f"<b>{fmt(d['final'][j])}</b>" if vis(d["est_fin"]) else "&nbsp;")
        if d["extra"]:
            celas.append(d["extra"][1][j] if vis(est_extra) else "&nbsp;")
        h.append(f'<tr class="{rcls}" data-id="r-{j}"><td class="colpasso">{badge}</td>' +
                 "".join(f'<td{" class=\"rot\"" if k == 0 else ""}>{c}</td>' for k, c in enumerate(celas)) + "</tr>")
    # excedente
    e = d["est_exc"]
    rcls = "atual" if e in S else ("futuro" if e > mx else "feito")
    sob = ", ".join(f"{k}{d['itens'][k - 1] if d['mostrar_itens'] else ''}" for k in d["sobras"]) or "—"
    txt = sob if e <= mx else "&nbsp;"
    if d["escolhas"] and d["est_fin"] <= mx:
        txt += " → " + "; ".join(f"{q}: {k}{d['itens'][k - 1] if d['mostrar_itens'] else ''}" for q, k in d["escolhas"])
    h.append(f'<tr class="{rcls}" data-id="r-exc"><td class="colpasso"><span class="npasso">★</span></td>'
             f'<td class="rot">Excedente</td><td colspan="{len(cols) - 1}" class="span">{txt}</td></tr>')
    h.append("</table></div>")
    return "```{=html}\n" + "".join(h) + "\n```"


# ---- dados das tabelas de síntese
_V = {"Teodoro": {S: 1, C: 1, K: 1}, "Vanessa": {S: 0, C: 2, K: 0}, "Rudy": {S: F(3, 2), C: F(3, 4), K: F(3, 4)}}
def_sintese("intro", [("Teodoro", "p1"), ("Vanessa", "p2"), ("Rudy", "p3")], doces,
            {"Teodoro": [3, 6], "Vanessa": [4, 5], "Rudy": [2, 5]}, _V,
            est_marcas={"Teodoro": 2, "Vanessa": 3, "Rudy": 4}, escolhas=[("Vanessa", 4), ("Rudy", 3), ("Teodoro", 6)])
def_sintese("p1", [("A", "p1"), ("B", "p2"), ("C", "p3"), ("D", "p4")], g16,
            {"A": [1, 6, 12], "B": [3, 8, 15], "C": [2, 9, 14], "D": [2, 7, 12]}, mostrar_itens=False)
_j = {"Ana": [5, 8, 14], "Beatriz": [5, 9, 14], "Clara": [3, 8, 15], "Diana": [4, 7, 13]}
_jj = [("Ana", "p1"), ("Beatriz", "p2"), ("Clara", "p3"), ("Diana", "p4")]
def_sintese("p2B", _jj, j20, _j, desempate={2: "Beatriz"}, mostrar_itens=False)
def_sintese("p2A", _jj, j20, _j, desempate={2: "Ana"}, mostrar_itens=False)
def_sintese("p3", [("Sérgio", "p1"), ("Leonardo", "p2"), ("Paula", "p3")], l3,
            {"Sérgio": [2, 3], "Leonardo": [5, 7], "Paula": [3, 6]},
            {"Sérgio": {S: 0, C: 1, K: 0}, "Leonardo": {S: 1, C: 0, K: 1}, "Paula": {S: 1, C: 1, K: 1}},
            escolhas=[("Leonardo", 7), ("Paula", 3)])
_vb = {"Rita": {S: 0, C: 0, K: 1}, "Bruno": {S: 1, C: 1, K: 0}, "Carla": {S: 1, C: 1, K: 1}}
_d4 = def_sintese("p4", [("Rita", "p1"), ("Bruno", "p2"), ("Carla", "p3")], doces,
                  {"Rita": [7, 8], "Bruno": [2, 4], "Carla": [3, 6]}, _vb)
_pb = {j: sum(_vb["Bruno"][doces[k - 1]] for k in range(_d4["seg"][j][0], _d4["seg"][j][1] + 1)) for j in ["Rita", "Bruno", "Carla"]}
_d4["extra"] = ("Para o Bruno", {j: (f'<span class="neg">{_pb[j]}</span>' if _pb[j] > _pb["Bruno"] else str(_pb[j])) for j in _pb})
_vc = {"Quintino": dict(W=12, S=7, G=4, B=6), "Ramon": dict(W=9, S=5, G=5, B=11),
       "Stephanie": dict(W=8, S=7, G=6, B=14), "Tim": dict(W=5, S=4, G=4, B=7)}
def_sintese("p5", [("Quintino", "p1"), ("Ramon", "p2"), ("Stephanie", "p3"), ("Tim", "p4")], bd,
            {"Quintino": [4, 7, 13], "Ramon": [5, 8, 14], "Stephanie": [5, 9, 15], "Tim": [5, 9, 14]}, _vc)

# verificações
assert SINTESE["intro"]["seg"] == {"Rudy": (1, 2), "Vanessa": (5, 5), "Teodoro": (7, 9)} and SINTESE["intro"]["sobras"] == [3, 4, 6]
assert SINTESE["intro"]["final"] == {"Teodoro": 4, "Vanessa": 4, "Rudy": F(9, 2)}
assert SINTESE["p1"]["sobras"] == [2, 8, 9, 15] and SINTESE["p2B"]["sobras"] == [4, 8, 9] and SINTESE["p2A"]["sobras"] == [4, 8]
assert SINTESE["p3"]["sobras"] == [3, 7] and SINTESE["p4"]["sobras"] == [3, 7, 8] and _pb == {"Rita": 0, "Bruno": 2, "Carla": 3}
assert SINTESE["p5"]["vale"] == {"Quintino": 30, "Ramon": 29, "Stephanie": 35, "Tim": 20} and SINTESE["p5"]["sobras"] == [5, 9, 15]


if __name__ == "__main__":
    aqui = pathlib.Path(__file__).parent
    modelo = (aqui / "_03_marcadores_modelo.qmd").read_text()
    def sub(m):
        return LINHAS[m.group(1)]
    saida = re.sub(r"\{\{L:(\w+)\}\}", sub, modelo)
    saida = re.sub(r"\{\{S:(\w+):([\d,\-]+)\}\}", lambda m: sintese(m.group(1), [int(x) for x in m.group(2).split(",")] if "-" not in m.group(2) else list(range(int(m.group(2).split("-")[0]), int(m.group(2).split("-")[1]) + 1))), saida)
    assert "{{S:" not in saida
    falta = re.findall(r"\{\{L:(\w+)\}\}", saida)
    assert not falta, falta
    (aqui.parent / "_corpo_03_marcadores.qmd").write_text(saida)
    print("escrito 03_marcadores.qmd")
