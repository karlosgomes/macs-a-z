"""Tabelas de cálculos «sempre presentes» da apresentação do Ajuste na Partilha (Adjusted Winner).

Uso: python3 tabela_aw.py  -> lê _02_ajuste_na_partilha_modelo.qmd e escreve ../02_ajuste_na_partilha.qmd
No modelo, {{A:caso:estados}} é substituído pela tabela do «caso» com as linhas dos «estados» destacadas
(um número, uma lista 3,4 ou um intervalo 3-6). Estados das linhas:
  1 pontos · 2 1.ª fase (totais) · 3 ordem do ajuste (razões) · 4 transferências por inteiro (testes)
  5 equação do ajuste · 6 partilha final e pontos finais · 7 parte do outro (inveja) · 8 linha extra
Convenção: x = fração do item dividido que PASSA do vencedor inicial para o outro jogador:
  V − v·x = P + p·x  (V, P: pontos de cada um nesse momento; v, p: pontos que cada um deu ao item).
Todos os cálculos em frações exatas."""
import re, pathlib
from fractions import Fraction as F


def dec(x, casas=2):
    s = f"{float(x):.{casas}f}".rstrip("0").rstrip(".")
    return s.replace(".", ",").replace("-", "−")


def num(x):
    """inteiro; decimal exato com ≤ 2 casas; senão fração ≈ decimal"""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    if (x * 100).denominator == 1:
        return dec(x)
    return f"\\(\\frac{{{x.numerator}}}{{{x.denominator}}}\\approx {dec(x, 1).replace(',', '{,}')}\\)"


def frac(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"\\(\\tfrac{{{x.numerator}}}{{{x.denominator}}}\\)"


def m(s):
    return f"\\({s}\\)"


class Caso:
    def __init__(self, jog, bens, pts, extra=None):
        self.jog, self.bens, self.pts, self.extra = jog, bens, pts, extra
        A, B = jog
        for p in jog:
            assert sum(pts[p][b] for b, _, _ in bens) == 100, (p, "pontos não somam 100")
        ids = [b for b, _, _ in bens]
        self.emo = {b: e for b, _, e in bens}
        # 1.ª fase (empates para quem tem menos pontos nesse momento)
        self.dono, self.empates = {}, []
        t = {A: F(0), B: F(0)}
        for b in ids:
            if pts[A][b] != pts[B][b]:
                d = A if pts[A][b] > pts[B][b] else B
                self.dono[b] = d; t[d] += pts[d][b]
            else:
                self.empates.append(b)
        for b in self.empates:
            d = A if t[A] <= t[B] else B
            self.dono[b] = d; t[d] += pts[d][b]
        self.t1 = dict(t)
        self.frac = {b: F(1) for b in ids}           # fração de b que fica com o dono inicial
        self.testes, self.dividido, self.x = [], None, None
        if t[A] == t[B]:
            self.dador = None
        else:
            G = A if t[A] > t[B] else B
            R = B if G == A else A
            self.dador, self.recetor = G, R
            ordem = sorted([b for b in ids if self.dono[b] == G], key=lambda b: F(pts[G][b], pts[R][b]))
            self.ordem = ordem
            for b in ordem:
                v, p = pts[G][b], pts[R][b]
                if t[G] - v >= t[R] + p:            # passa por inteiro
                    t[G] -= v; t[R] += p; self.frac[b] = F(0)
                    self.testes.append((b, t[G], t[R], True))
                    if t[G] == t[R]:
                        break
                else:
                    self.testes.append((b, t[G] - v, t[R] + p, False))
                    self.V, self.P, self.v, self.p = t[G], t[R], v, p
                    self.x = (t[G] - t[R]) / (v + p)
                    self.dividido = b
                    t[G] -= v * self.x; t[R] += p * self.x
                    self.frac[b] = 1 - self.x
                    break
        self.tf = dict(t)
        assert t[A] == t[B]
        # o que cada um fica a valer, para si e para o outro
        def parte(q):  # fração de cada item que fica com q
            return {b: (self.frac[b] if self.dono[b] == q else 1 - self.frac[b]) for b in ids}
        self.parte = {q: parte(q) for q in jog}
        self.outro = {q: sum(pts[q][b] * self.parte[jog[1] if q == A else A][b] for b in ids) for q in jog}

    def fica(self, q):
        itens = []
        for b, _, e in self.bens:
            f = self.parte[q][b]
            if f == 1:
                itens.append(e)
            elif f > 0:
                itens.append(f"{frac(f)} {e}")
        return " + ".join(itens) or "—"

    def linhas(self):
        A, B = self.jog
        L = []
        for i, (b, rot, e) in enumerate(self.bens):
            tag = " <small>(empate)</small>" if b in self.empates else ""
            L.append(dict(id=b, rot=rot + tag, est=1, passo=1 if i == 0 else None,
                          cel={A: str(self.pts[A][b]), B: str(self.pts[B][b])},
                          max={q: self.dono[b] == q for q in self.jog}))
        nota = "" if self.dador is None else f" → dador: {self.dador}"
        L.append(dict(id="fase1", rot="1.ª fase", est=2, passo=2,
                      cel={A: f"<b>{num(self.t1[A])}</b>", B: f"<b>{num(self.t1[B])}{''}</b>"}, nota=nota))
        if self.dador is None:
            L.append(dict(id="ordem", rot="Ajuste", est=3, passo=3, span="Totais iguais: <b>não há ajuste</b>"))
        else:
            G, R = self.dador, self.recetor
            ordem = " &lt; ".join(f"{self.emo[b]} {m(f'{self.pts[G][b]}/{self.pts[R][b]}')}" for b in self.ordem)
            L.append(dict(id="ordem", rot="Ordem (razão)", est=3, passo=3, span=ordem))
            for k, (b, tg, tr, ok) in enumerate(self.testes):
                cel = {G: num(tg), R: num(tr)}
                L.append(dict(id=f"t{k}", rot=f"Passar {self.emo[b]} todo?",
                              est=4, passo=4 if k == 0 else None, cel=cel,
                              nota=" ✔ passa" if ok else " ✘ inverte"))
            if self.dividido is not None:
                b = self.dividido
                eq = m(f"{num(self.V)}-{self.v}x={num(self.P)}+{self.p}x") + " ⟹ " + m("x=") + frac(self.x)
                L.append(dict(id="eq", rot=f"Divide-se {self.emo[b]}", est=5, passo=5, span=eq))
        L.append(dict(id="fica", rot="Fica com", est=6, passo=6, cel={q: self.fica(q) for q in self.jog}))
        L.append(dict(id="final", rot="Pontos finais", est=6, passo=None,
                      cel={q: f"<b>{num(self.tf[q])}</b>" for q in self.jog}))
        L.append(dict(id="outro", rot="Parte do outro vale", est=7, passo="✔",
                      cel={q: num(self.outro[q]) for q in self.jog}))
        if self.extra:
            L.append(dict(id="extra", rot=self.extra[0], est=8, passo="?", cel=self.extra[1]))
        return L


def render(caso, estados, unidade="(pontos)"):
    S = set(estados); A, B = caso.jog
    longa = " longa" if len(caso.bens) >= 6 else ""
    h = [f'<div class="tabela-metodo aw{longa}" data-id="tabmetodo"><table>',
         f'<tr><th></th><th>{unidade}</th><th>{A}</th><th>{B}</th></tr>']
    for r in caso.linhas():
        est = r["est"]
        cls = "atual" if est in S else ("feito" if est < min(S) else "futuro")
        badge = f'<span class="npasso">{r["passo"]}</span>' if r.get("passo") is not None else ""
        visivel = est <= max(S)
        if "span" in r:
            corpo = f'<td colspan="2" class="span">{r["span"] if visivel else "&nbsp;"}</td>'
        else:
            tds = []
            for q in caso.jog:
                mx = r.get("max", {}).get(q) and max(S) >= 2
                v = r["cel"][q] if visivel else "&nbsp;"
                if visivel and q == caso.jog[1] and r.get("nota"):
                    v += f'<span class="nota">{r["nota"]}</span>'
                tds.append(f'<td{" class=\"max\"" if mx else ""} data-id="c-{r["id"]}-{q}">{v}</td>')
            corpo = "".join(tds)
        h.append(f'<tr class="{cls}" data-id="r-{r["id"]}"><td class="colpasso">{badge}</td>'
                 f'<td class="rot">{r["rot"]}</td>{corpo}</tr>')
    h.append("</table></div>")
    return "```{=html}\n" + "".join(h) + "\n```"


# ---------------------------------------------------------------- dados
CASOS = {}
CASOS["intro"] = Caso(["Madalena", "Gonçalo"],
    [("iate", "⛵ Iate", "⛵"), ("gato", "🐈 Gato", "🐈"), ("apart", "🏢 Apartamento", "🏢"), ("quadro", "🖼️ Quadro", "🖼️")],
    {"Madalena": dict(iate=10, gato=50, apart=30, quadro=10), "Gonçalo": dict(iate=30, gato=20, apart=20, quadro=30)})
CASOS["camp"] = Caso(["Israel", "Egito"],
    [("sinai", "🏜️ Sinai", "🏜️"), ("rec", "🤝 Reconhecimento", "🤝"), ("cis", "🗺️ Cisjordânia e Gaza", "🗺️"),
     ("lig", "🔗 Ligação dos acordos", "🔗"), ("dir", "⚖️ Direitos palestinianos", "⚖️"), ("jer", "🕌 Jerusalém", "🕌")],
    {"Israel": dict(sinai=35, rec=10, cis=20, lig=10, dir=5, jer=20), "Egito": dict(sinai=55, rec=5, cis=10, lig=5, dir=20, jer=5)})
CASOS["p1"] = Caso(["Irmã", "Irmão"],
    [("gato", "🐈 Gato", "🐈"), ("cao", "🐕 Cão", "🐕"), ("iguana", "🦎 Iguana", "🦎"), ("papagaio", "🦜 Papagaio", "🦜")],
    {"Irmã": dict(gato=40, cao=30, iguana=10, papagaio=20), "Irmão": dict(gato=10, cao=50, iguana=30, papagaio=10)})
CASOS["p2"] = Caso(["Marido", "Esposa"],
    [("casa", "🏠 Casa", "🏠"), ("auto", "🚗 Automóvel", "🚗"), ("cabana", "🛖 Cabana", "🛖"),
     ("barco", "🚤 Barco", "🚤"), ("tv", "📺 Televisão", "📺"), ("som", "🔊 Som", "🔊")],
    {"Marido": dict(casa=30, auto=25, cabana=20, barco=16, tv=5, som=4), "Esposa": dict(casa=15, auto=25, cabana=40, barco=15, tv=3, som=2)})
CASOS["p3"] = Caso(["Leonido", "Marco"],
    [("cpd", "📣 Campanha de promoção", "📣"), ("api", "💲 Preço inicial", "💲"), ("dp", "🎨 Design do produto", "🎨"),
     ("acp", "🧾 Custo da promoção", "🧾"), ("mp", "🛠️ Protótipo", "🛠️"), ("acpo", "📊 Custo do produto", "📊"),
     ("tm", "🧪 Teste de mercado", "🧪")],
    {"Leonido": dict(cpd=40, api=13, dp=18, acp=6, mp=16, acpo=5, tm=2), "Marco": dict(cpd=32, api=20, dp=16, acp=9, mp=14, acpo=6, tm=3)})
CASOS["p4"] = Caso(["Paulo", "Rosa"],
    [("porc", "🏺 Porcelana", "🏺"), ("mesa", "🪑 Mesa", "🪑"), ("piano", "🎹 Piano", "🎹"),
     ("ferias", "🏖️ Casa de férias", "🏖️"), ("barco", "🚤 Barco", "🚤"), ("rel", "⌚ Relógios", "⌚")],
    {"Paulo": dict(porc=25, mesa=20, piano=20, ferias=10, barco=10, rel=15), "Rosa": dict(porc=30, mesa=9, piano=23, ferias=28, barco=5, rel=5)})
_q = [("mat", "🖼️ Matisse", "Matisse"), ("pic", "🖼️ Picasso", "Picasso")]
_real = {"Ana": dict(mat=75, pic=25), "Bruno": dict(mat=25, pic=75)}
CASOS["p5h"] = Caso(["Ana", "Bruno"], _q, _real)
for nome, decl in [("p5m", {"Ana": dict(mat=26, pic=74), "Bruno": dict(mat=25, pic=75)}),
                   ("p5a", {"Ana": dict(mat=26, pic=74), "Bruno": dict(mat=74, pic=26)})]:
    c = Caso(["Ana", "Bruno"], _q, decl)
    reais = {q: sum(_real[q][b] * c.parte[q][b] for b, _, _ in _q) for q in c.jog}
    c.extra = ("Pontos verdadeiros", {q: f"<b>{num(reais[q])}</b>" for q in c.jog})
    CASOS[nome] = c

# verificações (resultados já conhecidos)
assert CASOS["intro"].x == F(2, 5) and CASOS["intro"].tf["Madalena"] == 68
assert CASOS["camp"].x == F(1, 6)
assert CASOS["p1"].x == F(1, 4) and CASOS["p2"].x == F(1, 5) and CASOS["p3"].x == F(1, 15) and CASOS["p4"].x == F(36, 43)
assert CASOS["p5m"].x == F(49, 149) and CASOS["p5h"].dador is None


def estados(s):
    if "-" in s:
        a, b = map(int, s.split("-")); return list(range(a, b + 1))
    return [int(x) for x in s.split(",")]


if __name__ == "__main__":
    aqui = pathlib.Path(__file__).parent
    modelo = (aqui / "_02_ajuste_na_partilha_modelo.qmd").read_text()
    saida = re.sub(r"\{\{A:(\w+):([\d,\-]+)\}\}", lambda mm: render(CASOS[mm.group(1)], estados(mm.group(2))), modelo)
    assert "{{A:" not in saida
    (aqui.parent / "_corpo_02_ajuste.qmd").write_text(saida)
    for k, c in CASOS.items():
        print(f"{k:6s} 1.ª fase {dict((q, num(v)) for q, v in c.t1.items())}  x={c.x}  final {dict((q, num(v)) for q, v in c.tf.items())}")
    print("escrito 02_ajuste_na_partilha.qmd")
