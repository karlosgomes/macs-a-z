"""Tira capturas de ecrã de diapositivos (Chrome sem janela + protocolo DevTools).
Uso: python3 capturas.py ficheiro.html prefixo n1 n2 ...   (n = número do diapositivo, contagem linear)
As imagens ficam em capturas/; se houver ImageMagick, junta-as em folhas de 6."""
import asyncio, json, subprocess, sys, time, base64, urllib.request, os, http.server, threading, functools
import websockets
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.environ.get("RAIZ", os.path.dirname(AQUI))
pagina, prefixo, slides = sys.argv[1], sys.argv[2], sys.argv[3:]
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8765), functools.partial(Q, directory=RAIZ))
threading.Thread(target=srv.serve_forever, daemon=True).start()
p = subprocess.Popen(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                      "--window-size=1280,720", "--remote-debugging-port=9333", f"--user-data-dir={AQUI}/.perfil", "about:blank"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(50):
        try:
            tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9333/json")); break
        except Exception:
            time.sleep(0.2)
    ws_url = [t for t in tabs if t["type"] == "page"][0]["webSocketDebuggerUrl"]
    async def main():
        async with websockets.connect(ws_url, max_size=50_000_000) as ws:
            i = 0
            async def cmd(m, params={}):
                nonlocal i; i += 1; await ws.send(json.dumps({"id": i, "method": m, "params": params}))
                while True:
                    r = json.loads(await ws.recv())
                    if r.get("id") == i: return r
            await cmd("Emulation.setDeviceMetricsOverride", {"width": 1280, "height": 720, "deviceScaleFactor": 1, "mobile": False})
            await cmd("Page.navigate", {"url": f"http://127.0.0.1:8765/{pagina}"})
            await asyncio.sleep(7)
            for s in slides:
                js = (f"var ix=Reveal.getIndices(Reveal.getSlides()[{int(s)-1}]); Reveal.slide(ix.h, ix.v);"
                      "document.querySelectorAll('.reveal .slides section.present .fragment').forEach(e=>e.classList.add('visible'));")
                await cmd("Runtime.evaluate", {"expression": js}); await asyncio.sleep(1.5)
                r = await cmd("Page.captureScreenshot", {"format": "png"})
                open(f"{AQUI}/capturas/{prefixo}_{s}.png", "wb").write(base64.b64decode(r["result"]["data"]))
            r = await cmd("Runtime.evaluate", {"expression": "Reveal.getTotalSlides()", "returnByValue": True})
            print("total de diapositivos:", r["result"]["result"].get("value"))
    asyncio.run(asyncio.wait_for(main(), 110))
finally:
    p.kill(); srv.shutdown()
fs = [f"{AQUI}/capturas/{prefixo}_{s}.png" for s in slides]
for k in range(0, len(fs), 6):
    subprocess.run(["montage", *fs[k:k+6], "-tile", "2x3", "-geometry", "960x540+4+4", f"{AQUI}/capturas/folha_{prefixo}_{k//6}.png"])
