"""A virada: troca o take REAL pelo take GERADO (Kling ou outro gerador de vídeo) no instante exato que você escolher.

Por que isso existe: gerador de vídeo não obedece relógio. Você pede "a parede racha aos 2 segundos" e ela já
aparece rachando no primeiro quadro. Então o gerador faz o ESTADO FINAL (a cena já com o efeito) e a hora da
mudança é decidida aqui, no quadro que você quiser. Como os dois takes têm a mesma câmera parada, a troca não aparece.

Uso:
    python virada.py real.mp4 gerado.mp4 --t 2.4
    python virada.py real.mp4 gerado.mp4 --t 2.4 --dur 0.25 --modo linha --de 0,0.6 --para 1,0.4
    python virada.py real.mp4 gerado.mp4 --t 2.4 --inicio 1.9 --saida final.mp4

  --t        segundo do take real em que a virada COMEÇA (o instante do gesto, da batida, da palavra forte)
  --dur      quanto dura a virada, em segundos (padrão 0.20; golpe = curto, magia = mais longo)
  --inicio   segundo do take real de onde saiu o quadro inicial do take gerado (padrão: igual a --t)
  --modo     "fusao" (um take dissolve no outro) ou "linha" (uma linha atravessa a tela e revela o take gerado)
  --de/--para  no modo linha: a linha de corte, em fração da tela (0,0 = canto de cima à esquerda; 1,1 = de baixo à direita).
             A linha nasce nessa posição e varre a tela para os dois lados, como um corte que abre.
  --brilho   cor r,g,b da luz na borda da linha (padrão 255,255,255); "0,0,0" desliga
  --saida    arquivo de saída (padrão: virada.mp4 ao lado do take real)

O som é o do take real. O resultado tem o tamanho e os quadros por segundo do take real.
Precisa de Python com numpy e opencv-python, e do ffmpeg.
"""
import argparse
import os
import subprocess
import sys

import cv2
import numpy as np


def par(s):
    a, b = s.replace(" ", "").split(",")
    return float(a), float(b)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("real")
    ap.add_argument("gerado")
    ap.add_argument("--t", type=float, required=True)
    ap.add_argument("--dur", type=float, default=0.20)
    ap.add_argument("--inicio", type=float)
    ap.add_argument("--modo", choices=("fusao", "linha"), default="fusao")
    ap.add_argument("--de", default="0,0.5")
    ap.add_argument("--para", default="1,0.5")
    ap.add_argument("--brilho", default="255,255,255")
    ap.add_argument("--saida")
    a = ap.parse_args()
    inicio = a.t if a.inicio is None else a.inicio
    saida = a.saida or os.path.join(os.path.dirname(os.path.abspath(a.real)), "virada.mp4")

    real, ger = cv2.VideoCapture(a.real), cv2.VideoCapture(a.gerado)
    if not real.isOpened() or not ger.isOpened():
        sys.exit("Não consegui abrir um dos vídeos.")
    fps = real.get(cv2.CAP_PROP_FPS) or 30
    fps_g = ger.get(cv2.CAP_PROP_FPS) or fps
    W, H = int(real.get(cv2.CAP_PROP_FRAME_WIDTH)), int(real.get(cv2.CAP_PROP_FRAME_HEIGHT))
    n_g = int(ger.get(cv2.CAP_PROP_FRAME_COUNT))
    fim = inicio + n_g / fps_g                                    # onde o take gerado acaba, no relógio do take real
    if a.t < inicio:
        sys.exit("--t não pode ser antes de --inicio: o take gerado ainda não começou nesse ponto.")
    if a.t + a.dur > fim:
        sys.exit(f"O take gerado acaba em {fim:.2f} s, antes do fim da virada. Use um --t menor ou gere um take mais longo.")

    # distância de cada ponto da tela até a linha de corte (modo linha), de 0 a 1
    (x0, y0), (x1, y1) = par(a.de), par(a.para)
    p0, p1 = np.float32([x0 * W, y0 * H]), np.float32([x1 * W, y1 * H])
    d = (p1 - p0) / (np.linalg.norm(p1 - p0) + 1e-6)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.abs((xx - p0[0]) * -d[1] + (yy - p0[1]) * d[0])
    dist /= dist.max() + 1e-6
    cor = np.float32([float(v) for v in a.brilho.split(",")]) / 255

    tmp = saida + "._sem_som.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", f"{fps:.6f}", "-i", "-",
                            "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    i, lido_g, quadro_g = 0, -1, None
    while True:
        t = i / fps
        if t >= fim:
            break
        ok, q = real.read()
        if not ok:
            break
        if t >= a.t:
            alvo = min(n_g - 1, int(round((t - inicio) * fps_g)))  # o mesmo instante, no take gerado
            while lido_g < alvo:
                okg, g = ger.read()
                if not okg:
                    break
                quadro_g, lido_g = g, lido_g + 1
            g = cv2.resize(quadro_g, (W, H), interpolation=cv2.INTER_AREA if quadro_g.shape[1] > W else cv2.INTER_CUBIC)
            u = min(1.0, (t - a.t) / max(a.dur, 1e-3))
            u = 1 - (1 - u) ** 3                                    # abre rápido e assenta
            if a.modo == "fusao":
                q = cv2.addWeighted(q, 1 - u, g, u, 0)
            else:
                m = np.clip((u * 1.08 - dist) / 0.03, 0, 1)[..., None]              # 1 = já revelou o take gerado
                borda = (np.exp(-((u * 1.08 - dist) / 0.012) ** 2) * (1 - u) ** 0.5)[..., None]
                q = q.astype(np.float32) * (1 - m) + g.astype(np.float32) * m
                q = np.clip(q + borda * cor[::-1] * 255, 0, 255).astype(np.uint8)
        enc.stdin.write(np.ascontiguousarray(q).tobytes())
        i += 1
    enc.stdin.close()
    enc.wait()
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-i", a.real, "-map", "0:v", "-map", "1:a?", "-c:v", "copy", "-c:a", "aac", "-shortest", saida])
    if r.returncode == 0:
        os.remove(tmp)
    else:
        os.replace(tmp, saida)
    print(f"virada em {a.t:.2f} s ({a.modo}, {a.dur:.2f} s); duração final {i / fps:.2f} s")
    print("salvo:", saida)


if __name__ == "__main__":
    main()
