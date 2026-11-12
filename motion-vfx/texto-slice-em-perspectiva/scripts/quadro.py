"""Tira um quadro de um vídeo, no segundo que você escolher. Serve para três coisas:
  - olhar o enquadramento e medir os 4 cantos da superfície;
  - guardar o "quadro vazio" (o mesmo enquadramento sem ninguém na frente);
  - tirar o quadro inicial de um trecho que vai ser animado num gerador de vídeo (ver guia/kling.md).

Uso:
    python quadro.py video.mp4 2.4                  -> video_2.40s.png (ao lado do vídeo)
    python quadro.py video.mp4 2.4 quadro.png       -> salva com o nome que você deu
    python quadro.py video.mp4 fim                  -> o último quadro

Só precisa de Python com opencv-python.
"""
import os
import sys

import cv2


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    video, quando = sys.argv[1], sys.argv[2]
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        sys.exit(f"Não consegui abrir: {video}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    i = n - 1 if quando == "fim" else int(round(float(quando.replace(",", ".")) * fps))
    i = max(0, min(n - 1, i))
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ok, q = cap.read()
    while not ok and i > 0:          # alguns arquivos não entregam o último quadro: volta um
        i -= 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, q = cap.read()
    if not ok:
        sys.exit("Não consegui ler esse quadro.")
    saida = sys.argv[3] if len(sys.argv) > 3 else f"{os.path.splitext(video)[0]}_{i / fps:.2f}s.png"
    cv2.imwrite(saida, q)
    h, w = q.shape[:2]
    print(f"quadro {i} ({i / fps:.2f} s) de {n}, {w}x{h}, proporção {w / h:.2f}, {fps:.2f} quadros por segundo")
    print("salvo:", saida)


if __name__ == "__main__":
    main()
