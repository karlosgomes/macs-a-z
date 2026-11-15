"""Gera as tabelas de cálculos «sempre presentes» da apresentação do método das licitações secretas.

Uso: python3 tabela.py  -> lê _01_licitacoes_secretas_modelo.qmd e escreve ../01_licitacoes_secretas.qmd

No modelo, {{T:caso:estados}} é substituído pela tabela do «caso» com as linhas dos «estados» destacadas.
  estados: um número (ex.: 4), uma lista (3,4) ou um intervalo (3-6).
  Estados das linhas: 1 licitações · 2 total e parte justa · 3 bens recebidos · 4 alocação provisória
                      5 excedente · 6 alocação final · 7 valor para o próprio · 8 linha extra (se existir)
As linhas com estado menor do que os destacados aparecem normais; as seguintes aparecem a cinzento e vazias.
Todos os cálculos são feitos em frações exatas.
"""
import re, pathlib
from fractions import Fraction as F


# ---------------------------------------------------------------- formatação
def num(x):
    x = F(x)
    if x.denominator == 1:
        v = x.numerator
        s = f"{abs(v):,}".replace(",", "&nbsp;") if abs(v) >= 10000 else str(abs(v))
        return ("−" if v < 0 else "") + s
    v = float(x)
    t = f"{abs(v):,.2f}" if abs(v) >= 10000 else f"{abs(v):.2f}"
    t = t.replace(",", "X").replace(".", ",").replace("X", "&nbsp;")
    return ("−" if v < 0 else "") + t


def acerto(x, zero="0"):
    if x > 0:
        return f'<span class="neg">paga {num(x)}</span>'
    if x < 0:
        return f'<span class="pos">recebe {num(-x)}</span>'
    return zero


# ---------------------------------------------------------------- casos
class Caso:
    def __init__(self, jog, bens, lic, unidade, inverso=False, dono=None, rotulos=None, max_sempre=False, extra=None, sem_prop=False,
                 quotas=None, cab=None):
        self.jog, self.bens, self.lic, self.unidade = jog, bens, lic, unidade
        self.inverso = inverso            # tarefas: fica quem pede menos
        self.dono_forcado = dono or {}    # desempate (sorteio)
        self.rot = {"total": "Total", "pj": "Parte justa", "bens": "Bens recebidos",
                    "ini": "Alocação provisória", "exc": "Excedente", "fin": "Alocação final",
                    "prop": "Valor para o próprio", **(rotulos or {})}
        self.max_sempre = max_sempre
        self.extra = extra                # (rótulo, {jogador: html}) — estado 8
        self.sem_prop = sem_prop or inverso
        self.quotas = quotas or {p: F(1, len(jog)) for p in jog}
        self.cab = cab or {}
        self.calcular()

    def calcular(self):
        J, B, L, N = self.jog, self.bens, self.lic, len(self.jog)
        self.total = {p: sum(L[p][b] for b, _, _ in B) for p in J}
        self.pj = {p: self.quotas[p] * self.total[p] for p in J}
        escolha = min if self.inverso else max
        self.melhor = {b: escolha(L[p][b] for p in J) for b, _, _ in B}
        self.empatados = {b: [p for p in J if L[p][b] == self.melhor[b]] for b, _, _ in B}
        self.dono = {}
        for b, _, _ in B:
            e = self.empatados[b]
            self.dono[b] = self.dono_forcado.get(b) if len(e) > 1 and b in self.dono_forcado else (e[0] if len(e) == 1 else None)
        self.val = {p: sum(L[p][b] for b, _, _ in B if self.dono[b] == p) for p in J}
        if None in self.dono.values():
            return
        # bens: quem recebe mais do que a parte justa paga; tarefas: quem trabalha menos paga
        self.ini = {p: (self.pj[p] - self.val[p]) if self.inverso else (self.val[p] - self.pj[p]) for p in J}
        self.E = sum(self.ini.values())
        self.fin = {p: self.ini[p] - self.quotas[p] * self.E for p in J}
        self.prop = {p: self.pj[p] + self.quotas[p] * self.E for p in J}
        assert self.E >= 0 and sum(self.fin.values()) == 0

    def emojis(self, p):
        return getattr(self, "sep", "").join(e for b, _, e in self.bens if self.dono[b] == p)

    def ac(self, x, zero="0"):
        """acerto: por extenso (paga/recebe) ou, nas tabelas largas, com sinal e cor"""
        if not getattr(self, "acerto_curto", False):
            return acerto(x, zero)
        if x > 0:
            return f'<span class="neg">−{num(x)}</span>'
        if x < 0:
            return f'<span class="pos">+{num(-x)}</span>'
        return zero

    def linhas(self):
        J, R = self.jog, self.rot
        L = []
        for i, (b, rot, _) in enumerate(self.bens):
            L.append((b, rot, 1, 1 if i == 0 else None,
                      {p: num(self.lic[p][b]) for p in J},
                      {p: p in self.empatados[b] for p in J}))
        L.append(("total", R["total"], 2, 2, {p: num(self.total[p]) for p in J}, None))
        L.append(("pj", R["pj"], 2, None, {p: f"<b>{num(self.pj[p])}</b>" for p in J}, None))
        if None in self.dono.values():
            return L
        L.append(("bens", R["bens"], 3, 3,
                  {p: (f"{self.emojis(p)} {num(self.val[p])}" if self.emojis(p) else "—") for p in J}, None))
        L.append(("ini", R["ini"], 4, 4, {p: self.ac(self.ini[p]) for p in J}, None))
        L.append(("exc", R["exc"], 5, 5, {p: f"+{num(self.quotas[p] * self.E)}" for p in J}, None))
        L.append(("fin", R["fin"], 6, None, {p: f"<b>{self.ac(self.fin[p], '<b>0</b>')}</b>" for p in J}, None))
        if not self.sem_prop:
            L.append(("prop", R["prop"], 7, "✔", {p: f"<b>{num(self.prop[p])}</b>" for p in J}, None))
        if self.extra:
            L.append(("extra", self.extra[0], 8, "?", self.extra[1], None))
        return L


def render(jog, linhas, unidade, estados, classe="", cab=None):
    cab = cab or {}
    S = set(estados)
    h = [f'<div class="tabela-metodo {classe}" data-id="tabmetodo"><table>',
         f'<tr><th></th><th>{unidade}</th>' + "".join(f"<th>{cab.get(p, p)}</th>" for p in jog) + "</tr>"]
    for rid, rot, est, passo, vals, maxs in linhas:
        cls = "atual" if est in S else ("feito" if est < min(S) else "futuro")
        badge = f'<span class="npasso">{passo}</span>' if passo is not None else ""
        cells = []
        for p in jog:
            mx = maxs is not None and maxs.get(p) and (max(S) >= 3 or MAX_SEMPRE.get(id(linhas)))
            c = ' class="max"' if mx else ""
            cells.append(f'<td{c} data-id="c-{rid}-{p}">{vals[p] if est <= max(S) else "&nbsp;"}</td>')
        h.append(f'<tr class="{cls}" data-id="r-{rid}"><td class="colpasso">{badge}</td>'
                 f'<td class="rot">{rot}</td>{"".join(cells)}</tr>')
    h.append("</table></div>")
    return "```{=html}\n" + "".join(h) + "\n```"


MAX_SEMPRE = {}


def tabela_caso(caso, estados):
    linhas = caso.linhas()
    if caso.max_sempre:
        MAX_SEMPRE[id(linhas)] = True
    classe = "quatro" if len(caso.jog) >= 4 else ""
    if getattr(caso, "classe", ""):
        classe += " " + caso.classe
    return render(caso.jog, linhas, caso.unidade, estados, classe, caso.cab)


# ---------------------------------------------------------------- dados
CASOS = {}

# Exemplo introdutório: herança dos avós (milhares de €)
CASOS["intro"] = Caso(["Afonso", "Beatriz", "Carlos"], [("casa", "🏠 Casa", "🏠"), ("iate", "⛵ Iate", "⛵")],
                      {"Afonso": {"casa": 100, "iate": 200}, "Beatriz": {"casa": 180, "iate": 150},
                       "Carlos": {"casa": 150, "iate": 90}}, "(milhares de €)")

# Problema 1: quatro irmãos (€)
p1 = Caso(["António", "Bernardo", "Carla", "Daniela"],
          [("casa", "🏠 Casa", "🏠"), ("campo", "🌾 Campo", "🌾"), ("terreno", "🏞️ Terreno", "🏞️")],
          {"António": dict(casa=8600, campo=5500, terreno=3600), "Bernardo": dict(casa=3500, campo=4200, terreno=5100),
           "Carla": dict(casa=2300, campo=4400, terreno=3400), "Daniela": dict(casa=4800, campo=2700, terreno=2300)}, "(€)")
# valor de cada parte segundo as licitações da Daniela
_d = {p: sum(p1.lic["Daniela"][b] for b, _, _ in p1.bens if p1.dono[b] == p) - p1.fin[p] for p in p1.jog}
p1.extra = ("Valor para a Daniela", {p: (f'<span class="neg">{num(_d[p])}</span>' if _d[p] > _d["Daniela"] else num(_d[p])) for p in p1.jog})
CASOS["p1"] = p1

# Problema 3: tarefas (€) — leilão inverso
CASOS["p3"] = Caso(["Henrique", "Inês", "João"],
                   [("wc", "🚿 Casas de banho", "🚿"), ("parede", "🎨 Parede", "🎨"),
                    ("rodapes", "🧽 Rodapés", "🧽"), ("janelas", "🪟 Janelas", "🪟")],
                   {"Henrique": dict(wc=65, parede=100, rodapes=60, janelas=75),
                    "Inês": dict(wc=70, parede=85, rodapes=50, janelas=80),
                    "João": dict(wc=55, parede=95, rodapes=45, janelas=90)}, "(€)", inverso=True,
                   rotulos={"pj": "Parte justa de trabalho", "bens": "Tarefas atribuídas",
                            "prop": "Valor para o próprio"})

# Problema 4: empate (milhares de €)
_b4 = [("casa", "🏠 Casa", "🏠"), ("carro", "🚗 Carro", "🚗"), ("piano", "🎹 Piano", "🎹")]
_l4 = {"Rita": dict(casa=150, carro=15, piano=3), "Sara": dict(casa=150, carro=12, piano=9),
       "Tiago": dict(casa=135, carro=23, piano=4)}
CASOS["p4R"] = Caso(["Rita", "Sara", "Tiago"], _b4, _l4, "(milhares de €)", dono={"casa": "Rita"}, max_sempre=True)
CASOS["p4S"] = Caso(["Rita", "Sara", "Tiago"], _b4, _l4, "(milhares de €)", dono={"casa": "Sara"}, max_sempre=True)

# Problema 5: espreitar as licitações (milhares de €)
_b5 = [("casa", "🏠 Casa", "🏠"), ("agencia", "✈️ Agência", "✈️")]
_real = {"Catarina": dict(casa=1000, agencia=200), "Sofia": dict(casa=700, agencia=350), "Joana": dict(casa=650, agencia=250)}
CASOS["p5h"] = Caso(["Catarina", "Sofia", "Joana"], _b5, _real, "(milhares de €)")
p5b = Caso(["Catarina", "Sofia", "Joana"], _b5, {**_real, "Catarina": dict(casa=710, agencia=340)}, "(milhares de €)", sem_prop=True)
_vr = {p: sum(_real[p][b] for b, _, _ in _b5 if p5b.dono[b] == p) - p5b.fin[p] for p in p5b.jog}
_vh = {p: CASOS["p5h"].prop[p] for p in p5b.jog}
p5b.extra = ("Valor real", {p: f'{num(_vr[p])} <span class="{"pos" if _vr[p] > _vh[p] else "neg"}">'
                                            f'({"+" if _vr[p] > _vh[p] else ""}{num(_vr[p] - _vh[p])})</span>' for p in p5b.jog})
CASOS["p5b"] = p5b


# ================================================================ PROBLEMAS DE EXAME
# E1. Exame 2026, Época especial — prémio do jornal da escola (€)
CASOS["e1"] = Caso(["Ana", "Bruno", "Carlos"], [("tablet", "📱 Tablet", "📱"), ("maquina", "📷 Máquina fotográfica", "📷")],
                   {"Ana": dict(tablet=100, maquina=140), "Bruno": dict(tablet=180, maquina=30),
                    "Carlos": dict(tablet=75, maquina=75)}, "(€)")

# E2. Exame 2015, 1.ª fase — prémio da agência de viagens (€); alínea extra sobre inveja
e2 = Caso(["Alice", "Bernardo", "Camila"],
          [("comp", "💻 Computador", "💻"), ("tablet", "📱 Tablet", "📱"), ("viagem", "🚌 Viagem", "🚌")],
          {"Alice": dict(comp=600, tablet=350, viagem=850), "Bernardo": dict(comp=950, tablet=300, viagem=1000),
           "Camila": dict(comp=750, tablet=300, viagem=810)}, "(€)")
_a = {p: sum(e2.lic["Alice"][b] for b, _, _ in e2.bens if e2.dono[b] == p) - e2.fin[p] for p in e2.jog}
e2.extra = ("Valor para a Alice", {p: (f'<span class="neg">{num(_a[p])}</span>' if _a[p] > _a["Alice"] else num(_a[p])) for p in e2.jog})
CASOS["e2"] = e2

# E3. Exame 2010, 1.ª fase — herança do senhor Francisco (€)
e3 = Caso(["Ana", "Berta", "Carla", "Daniela"],
          [("auto", "🚗 Automóvel", "🚗"), ("terreno", "🏞️ Terreno", "🏞️"), ("casa", "🏠 Casa", "🏠")],
          {"Ana": dict(auto=15000, terreno=33000, casa=117000), "Berta": dict(auto=18000, terreno=20000, casa=150000),
           "Carla": dict(auto=15600, terreno=27000, casa=120000), "Daniela": dict(auto=16500, terreno=30000, casa=180000)}, "(€)")
e3.acerto_curto = True
e3.rot["pj"] = "Porção justa"
CASOS["e3"] = e3

# E4. Exame 2022, 1.ª fase — viagens da Célia e do Guilherme (€); a = 600 porque a parte justa da Célia é 1550
CASOS["e4"] = Caso(["Célia", "Guilherme"], [("X", "✈️ Viagem X", "X"), ("Y", "✈️ Viagem Y", "Y"), ("Z", "✈️ Viagem Z", "Z")],
                   {"Célia": dict(X=1000, Y=1500, Z=600), "Guilherme": dict(X=1400, Y=1000, Z=550)}, "(€)")
assert CASOS["e4"].pj["Célia"] == 1550
CASOS["e4"].sep = " e "

# E5. Exame 2021, Época especial — prémio repartido 50 % / 30 % / 20 % (€)
CASOS["e5"] = Caso(["Dora", "Elsa", "Fernando"],
                   [("bilhete", "🎟️ Bilhete", "🎟️"), ("camisola", "👕 Camisola", "👕"), ("cd", "💿 CD", "💿")],
                   {"Dora": dict(bilhete=40, camisola=20, cd=26), "Elsa": dict(bilhete=34, camisola=22, cd=34),
                    "Fernando": dict(bilhete=36, camisola=26, cd=28)}, "(€)",
                   quotas={"Dora": F(1, 2), "Elsa": F(3, 10), "Fernando": F(1, 5)},
                   cab={"Dora": "Dora<br><small>50 %</small>", "Elsa": "Elsa<br><small>30 %</small>",
                        "Fernando": "Fernando<br><small>20 %</small>"},
                   rotulos={"pj": "Porção justa"})


def linhas_e4_simbolico():
    """Tabela do E4 antes de se conhecer a: a licitação da Célia pela viagem Z é a."""
    L = CASOS["e4"].linhas()
    out = []
    for rid, rot, est, passo, vals, maxs in L:
        vals = dict(vals)
        if rid == "Z":
            vals["Célia"] = "\\(a\\)"; maxs = None
        if rid == "total":
            vals["Célia"] = "\\(2500+a\\)"
        if rid == "pj":
            vals["Célia"] = "<b>\\(\\frac{2500+a}{2}=1550\\)</b>"
        out.append((rid, rot, est, passo, vals, maxs if est == 1 else None))
    return out


# Problema 2 (anterior): licitação em falta (simbólico; linhas escritas à mão)
def _m(s):
    return f"\\({s}\\)"


P2_JOG = ["Alice", "Beto"]
P2_LINHAS = [
    ("b1", "Bem 1", 1, 1, {"Alice": "1500", "Beto": "1600"}, {"Beto": True}),
    ("b2", "Bem 2", 1, None, {"Alice": "700", "Beto": _m("x")}, {"Beto": True}),
    ("b3", "Bem 3", 1, None, {"Alice": "300", "Beto": "200"}, {"Alice": True}),
    ("b4", "Bem 4", 1, None, {"Alice": "500", "Beto": "200"}, {"Alice": True}),
    ("total", "Total", 2, 2, {"Alice": "3000", "Beto": _m("2000+x")}, None),
    ("pj", "Parte justa", 2, None, {"Alice": "<b>1500</b>", "Beto": "<b>" + _m("1000+\\frac{x}{2}") + "</b>"}, None),
    ("bens", "Bens recebidos", 3, 3, {"Alice": "3 e 4: 800", "Beto": "1 e 2: " + _m("1600+x")}, None),
    ("ini", "Alocação provisória", 4, 4, {"Alice": '<span class="pos">recebe 700</span>',
                                          "Beto": '<span class="neg">paga ' + _m("600+\\frac{x}{2}") + "</span>"}, None),
    ("exc", "Excedente", 5, 5, {"Alice": _m("+\\frac{x}{4}-50"), "Beto": _m("+\\frac{x}{4}-50")}, None),
    ("fin", "Alocação final", 6, None, {"Alice": '<span class="pos">recebe ' + _m("650+\\frac{x}{4}") + "</span>",
                                        "Beto": '<span class="neg">paga ' + _m("650+\\frac{x}{4}") + "</span>"}, None),
    ("prop", "Com \\(x = 800\\)", 7, "✔", {"Alice": '<span class="pos"><b>recebe 850</b></span>',
                                            "Beto": '<span class="neg"><b>paga 850</b></span>'}, None),
]
# verificação numérica do problema 2
_c = Caso(P2_JOG, [(1, "", ""), (2, "", ""), (3, "", ""), (4, "", "")],
          {"Alice": {1: 1500, 2: 700, 3: 300, 4: 500}, "Beto": {1: 1600, 2: 800, 3: 200, 4: 200}}, "")
assert _c.fin == {"Alice": -850, "Beto": 850}
MAX_P2 = None


def tabela(nome, estados):
    if nome == "e4a":
        return render(CASOS["e4"].jog, linhas_e4_simbolico(), "(€)", estados)
    if nome == "p2":
        linhas = list(P2_LINHAS)
        MAX_SEMPRE[id(linhas)] = True
        return render(P2_JOG, linhas, "(€)", estados)
    return tabela_caso(CASOS[nome], estados)


def estados(s):
    if "-" in s:
        a, b = map(int, s.split("-"))
        return list(range(a, b + 1))
    return [int(x) for x in s.split(",")]


if __name__ == "__main__":
    for k, c in CASOS.items():
        if hasattr(c, "fin"):
            print(f"{k:6s} pj={ {p: num(v) for p, v in c.pj.items()} } E={num(c.E)} final={ {p: num(v) for p, v in c.fin.items()} }")
    aqui = pathlib.Path(__file__).parent
    modelo = (aqui / "_01_licitacoes_secretas_modelo.qmd").read_text()
    saida = re.sub(r"\{\{T:(\w+):([\d,\-]+)\}\}", lambda m: tabela(m.group(1), estados(m.group(2))), modelo)
    assert "{{T:" not in saida, re.findall(r"\{\{T:[^}]*\}\}", saida)
    (aqui.parent / "_corpo_01_licitacoes.qmd").write_text(saida)
    print("escrito 01_licitacoes_secretas.qmd")
