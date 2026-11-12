"""Texto preso a uma superfície (parede, chão, porta) em perspectiva, cortado por uma linha ("slice").
Funciona em foto e em vídeo de câmera parada. Só precisa de Python com numpy, opencv e pillow (e ffmpeg para vídeo).

Uso:
    python slice_texto.py config.json prova     -> prova.jpg  (grade + contorno do texto, para aprovar o encaixe)
    python slice_texto.py config.json final     -> resultado.jpg ou resultado.mp4

config.json (campos com * são obrigatórios):
  * "entrada":   foto ou vídeo
  * "quad":      os 4 cantos da superfície na imagem, em pixels: [topo-esq, topo-dir, base-dir, base-esq]
  * "proporcao": largura / altura REAL desse retângulo (ex.: parede de 4 m por 1 m = 4.0)
  * "texto":     a palavra ou frase grande
    "rotulo":    texto pequeno acima (opcional)
    "fonte":     caminho de um .ttf/.otf (padrão: Anton, que vem junto)
    "cor":       [r, g, b] do texto (padrão: branco)
    "cor_corte": [r, g, b] do brilho do corte (padrão: azul claro)
    "opacidade": 0 a 1 (padrão 0.82)
    "altura":    quanto da altura da superfície o texto ocupa, 0 a 1 (padrão 0.62)
    "margem":    margem lateral dentro da superfície, 0 a 0.4 (padrão 0.06)
    "corte":     {"de": [u, v], "para": [u, v]} linha do corte em coordenadas da superfície, 0 a 1 (padrão: diagonal suave)
    "abertura":  quanto as metades se afastam, em fração da altura do texto (padrão 0.16)
    "vazio":     foto do MESMO enquadramento sem a pessoa: o texto passa por trás de quem estiver na frente
    "mascara":   alternativa ao "vazio": imagem em que branco = o que fica na frente do texto
    "limiar":    sensibilidade da diferença com o "vazio", 0 a 1 (padrão 0.10)
    "t_corte":   (vídeo) segundo em que o corte acontece (padrão: 40% da duração)
    "dur_corte": (vídeo) quanto dura a abertura, em segundos (padrão 0.35)
    "saida":     pasta de saída (padrão: a pasta do config)
"""
import json, os, subprocess, sys
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
ss = lambda x: (lambda c: c * c * (3 - 2 * c))(np.clip(x, 0, 1))
ease = lambda x: 1 - (1 - np.clip(x, 0, 1)) ** 3
blur = lambda a, s: cv2.GaussianBlur(a, (0, 0), s)
screen = lambda a, b: 1 - (1 - a) * (1 - np.clip(b, 0, 1))
VIDEO = (".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v")

def carrega(cfg_path):
    c = json.load(open(cfg_path, encoding="utf-8")); base = os.path.dirname(os.path.abspath(cfg_path))
    for k in ("entrada", "vazio", "mascara", "fonte", "saida"):
        if c.get(k) and not os.path.isabs(c[k]): c[k] = os.path.join(base, c[k])
    c.setdefault("saida", base); c.setdefault("fonte", os.path.join(AQUI, "..", "assets", "Anton-Regular.ttf"))
    if not os.path.exists(c["fonte"]):
        alt = [f for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf", "C:/Windows/Fonts/impact.ttf", "/System/Library/Fonts/Supplemental/Impact.ttf") if os.path.exists(f)]
        if not alt: sys.exit("Fonte não encontrada: informe \"fonte\" no config.")
        c["fonte"] = alt[0]
    for k, v in dict(cor=[245, 245, 245], cor_corte=[110, 200, 255], opacidade=0.82, altura=0.62, margem=0.06, abertura=0.16, limiar=0.10, dur_corte=0.35).items(): c.setdefault(k, v)
    c.setdefault("corte", {"de": [0.0, 0.40], "para": [1.0, 0.60]})
    assert len(c["quad"]) == 4, "quad precisa de 4 pontos"
    return c

def tela_da_superficie(c):
    """desenha o texto num retângulo plano com a proporção real da superfície; devolve as máscaras e a geometria do corte"""
    PH = 900; PW = int(round(PH * float(c["proporcao"])))
    if PW > 6000: PH = int(PH * 6000 / PW); PW = 6000
    txt = c["texto"].upper(); mx = c["margem"] * PW; alvo_h = c["altura"] * PH
    f = ImageFont.truetype(c["fonte"], 400); b = f.getbbox(txt); tam = 400 * alvo_h / (b[3] - b[1])
    f = ImageFont.truetype(c["fonte"], int(tam)); b = f.getbbox(txt)
    if b[2] - b[0] > PW - 2 * mx:                                   # não coube na largura: reduz até caber
        tam *= (PW - 2 * mx) / (b[2] - b[0]); f = ImageFont.truetype(c["fonte"], int(tam)); b = f.getbbox(txt)
    tw, th = b[2] - b[0], b[3] - b[1]; x0 = (PW - tw) / 2 - b[0]; y0 = (PH - th) / 2 - b[1] + (0.05 * PH if c.get("rotulo") else 0)
    im = Image.new("L", (PW, PH), 0); d = ImageDraw.Draw(im); d.text((x0, y0), txt, font=f, fill=255)
    if c.get("rotulo"):
        fr = ImageFont.truetype(c["fonte"], max(12, int(tam * 0.16))); rot = "  ".join(c["rotulo"].upper())
        d.text((x0 + b[0], y0 + b[1] - int(tam * 0.26)), rot, font=fr, fill=255)
    m = np.asarray(im, np.float32) / 255
    (u0, v0), (u1, v1) = c["corte"]["de"], c["corte"]["para"]
    p0 = np.float32([u0 * PW, v0 * PH]); p1 = np.float32([u1 * PW, v1 * PH]); dr = (p1 - p0) / (np.linalg.norm(p1 - p0) + 1e-6); nr = np.float32([-dr[1], dr[0]])
    yy, xx = np.mgrid[0:PH, 0:PW].astype(np.float32); dist = (xx - p0[0]) * nr[0] + (yy - p0[1]) * nr[1]
    return dict(m=m, dist=dist, dr=dr, nr=nr, PW=PW, PH=PH, th=th, caixa=(x0 + b[0], y0 + b[1], tw, th))

def fatia(T, c, u):
    """u = 0 (inteiro) a 1 (aberto): devolve (texto, linha de luz) no retângulo plano"""
    if u <= 0: return T["m"], np.zeros_like(T["m"])
    ab = c["abertura"] * T["th"] * ease(u); cima = T["m"] * (T["dist"] < 0); baixo = T["m"] * (T["dist"] >= 0)
    desl = lambda a, s: cv2.warpAffine(a, np.float32([[1, 0, s * (T["dr"][0] * ab - T["nr"][0] * ab * 0.22)], [0, 1, s * (T["dr"][1] * ab - T["nr"][1] * ab * 0.22)]]), (T["PW"], T["PH"]))
    linha = np.exp(-(T["dist"] / (T["PH"] * 0.006)) ** 2) * (blur(T["m"], T["PH"] * 0.05) > 0.02) * float(np.clip(1.35 - u * 0.75, 0, 1))
    return desl(cima, 1) + desl(baixo, -0.35), linha

def frente(img, c, plate, mascara):
    """o que está na frente do texto (0 a 1): pela diferença com o quadro vazio ou por uma máscara pronta"""
    H, W = img.shape[:2]
    if mascara is not None: return blur(cv2.resize(mascara, (W, H)).astype(np.float32) / 255, 1.5)
    if plate is None: return np.zeros((H, W), np.float32)
    a = blur(img, 2.0); b = blur(plate, 2.0)
    dif = np.abs(a - b).max(2) / (0.5 * (a.max(2) + b.max(2)) + 0.12)        # diferença relativa: aguenta sombra leve
    m = ss((dif - c["limiar"]) / (c["limiar"] * 0.8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    return blur(m, 1.8)

def compoe(img, c, T, Hm, u, occ):
    """img RGB 0..1. O texto pega a luz e a textura da superfície (não é um adesivo) e some atrás de quem está na frente."""
    H, W = img.shape[:2]; txt, linha = fatia(T, c, u)
    w = lambda a: cv2.warpPerspective(a, Hm, (W, H), flags=cv2.INTER_AREA if T["PW"] > W else cv2.INTER_LINEAR)
    a = w(txt) * (1 - occ); l = w(linha) * (1 - occ)
    lum = img @ np.float32([.2126, .7152, .0722]); media = blur(lum, 40) + 1e-3
    textura = np.clip(lum / media, 0.55, 1.35)                                # trama, rejunte e sombra fina continuam visíveis
    luz = np.clip(0.55 + 0.75 * media / (media.max() + 1e-3), 0.5, 1.15)      # onde a parede é escura, o texto também é
    cor = np.float32(c["cor"]) / 255 * (textura * luz)[..., None]
    al = (a * c["opacidade"])[..., None]
    out = img * (1 - al) + cor * al
    cc = np.float32(c["cor_corte"]) / 255
    out = screen(out, (blur(l, 1.2) * 0.9)[..., None] * (cc * 0.5 + 0.5) + (blur(l, 9) * 0.7 + blur(l, 34) * 0.5)[..., None] * cc)
    return np.clip(out, 0, 1)

def homografia(c, T, W, H):
    q = np.float32(c["quad"]); return cv2.getPerspectiveTransform(np.float32([[0, 0], [T["PW"], 0], [T["PW"], T["PH"]], [0, T["PH"]]]), q)

def prova(img, c, T, Hm):
    """grade em perspectiva + contorno do texto + linha do corte: para aprovar o encaixe ANTES de renderizar"""
    H, W = img.shape[:2]; g = np.zeros((T["PH"], T["PW"]), np.uint8); n = max(4, int(round(8 * T["PW"] / T["PH"] / 2)))
    for i in range(n + 1): cv2.line(g, (int(i * (T["PW"] - 1) / n), 0), (int(i * (T["PW"] - 1) / n), T["PH"] - 1), 255, 3)
    for j in range(5): cv2.line(g, (0, int(j * (T["PH"] - 1) / 4)), (T["PW"] - 1, int(j * (T["PH"] - 1) / 4)), 255, 3)
    cont = cv2.morphologyEx((T["m"] * 255).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((7, 7), np.uint8))
    (u0, v0), (u1, v1) = c["corte"]["de"], c["corte"]["para"]; lc = np.zeros_like(g)
    cv2.line(lc, (int(u0 * T["PW"]), int(v0 * T["PH"])), (int(u1 * T["PW"]), int(v1 * T["PH"])), 255, 6)
    w = lambda a: cv2.warpPerspective(a, Hm, (W, H)).astype(np.float32) / 255
    out = img * 0.75
    out = screen(out, w(g)[..., None] * np.float32([0.25, 0.75, 1.0]) * 0.55)
    out = screen(out, w(cont)[..., None] * np.float32([1, 1, 1]))
    out = screen(out, w(lc)[..., None] * np.float32([1.0, 0.25, 0.9]))
    o8 = (np.clip(out, 0, 1) * 255).astype(np.uint8).copy()
    for k, (x, y) in enumerate(c["quad"]):
        cv2.circle(o8, (int(x), int(y)), 12, (255, 220, 0), -1); cv2.putText(o8, str(k + 1), (int(x) + 16, int(y) - 12), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 220, 0), 3)
    return o8

def le_img(p):
    a = cv2.imread(p, cv2.IMREAD_COLOR)
    if a is None: sys.exit(f"Não consegui abrir: {p}")
    return cv2.cvtColor(a, cv2.COLOR_BGR2RGB).astype(np.float32) / 255

def main():
    if len(sys.argv) < 3: sys.exit(__doc__)
    c = carrega(sys.argv[1]); modo = sys.argv[2]; os.makedirs(c["saida"], exist_ok=True)
    T = tela_da_superficie(c); eh_video = c["entrada"].lower().endswith(VIDEO)
    if eh_video:
        cap = cv2.VideoCapture(c["entrada"]); fps = cap.get(cv2.CAP_PROP_FPS) or 30; N = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    else:
        img = le_img(c["entrada"]); H, W = img.shape[:2]
    Hm = homografia(c, T, W, H)
    plate = cv2.resize(le_img(c["vazio"]), (W, H)) if c.get("vazio") else None
    masc = cv2.imread(c["mascara"], 0) if c.get("mascara") else None
    if modo == "prova":
        if eh_video:
            cap.set(cv2.CAP_PROP_POS_FRAMES, N // 2); ok, fr = cap.read(); img = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255
        p = os.path.join(c["saida"], "prova.jpg"); o = prova(img, c, T, Hm)
        fin = (compoe(img, c, T, Hm, 1.0, frente(img, c, plate, masc)) * 255).astype(np.uint8)       # ao lado, como vai ficar
        cv2.imwrite(p, cv2.cvtColor(np.hstack([o, fin]) if W <= 2200 else np.vstack([o, fin]), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92]); print("prova:", p); return
    if not eh_video:
        o = compoe(img, c, T, Hm, 1.0, frente(img, c, plate, masc)); p = os.path.join(c["saida"], "resultado.jpg")
        cv2.imwrite(p, cv2.cvtColor((o * 255 + 0.5).astype(np.uint8), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 95]); print("resultado:", p); return
    tc = c.get("t_corte", 0.4 * N / fps); p = os.path.join(c["saida"], "resultado.mp4"); tmp = os.path.join(c["saida"], "_sem_audio.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                            "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    i = 0
    while True:
        ok, fr = cap.read()
        if not ok: break
        img = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255
        u = (i / fps - tc) / c["dur_corte"]
        enc.stdin.write((compoe(img, c, T, Hm, float(np.clip(u, 0, 1)) if u > 0 else 0.0, frente(img, c, plate, masc)) * 255 + 0.5).astype(np.uint8).tobytes()); i += 1
        if i % 30 == 0: print(f"quadro {i} de {N}", flush=True)
    enc.stdin.close(); enc.wait()
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-i", c["entrada"], "-map", "0:v", "-map", "1:a?", "-c:v", "copy", "-c:a", "aac", "-shortest", p])
    if r.returncode == 0: os.remove(tmp)
    else: os.replace(tmp, p)
    print("resultado:", p)

if __name__ == "__main__":
    main()
