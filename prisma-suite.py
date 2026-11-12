#!/usr/bin/env python3
"""Prisma-Suite — ponto de entrada unico.

  python prisma-suite.py install    instala tudo nesta maquina (repassa as opcoes ao install-suite.py)
  python prisma-suite.py doctor     confere binarios, skills, vendor, modelos e extras Python
  python prisma-suite.py manifest   regera manifests/ecosystem.lock.json
  python prisma-suite.py map        lista o mapa tarefa -> helper/skill (ECOSYSTEM.md)

Somente biblioteca padrao. Fora o `install`, nenhum comando instala nada: dizem o que falta.
"""
import json, shutil, subprocess, sys
from pathlib import Path

SUITE = Path(__file__).resolve().parent
OK, BAD, WARN = "ok ", "x  ", "!  "

BINARIOS = (("uv", True, "winget install astral-sh.uv"),
            ("ffmpeg", True, "winget install Gyan.FFmpeg"),
            ("ffprobe", True, "vem com o ffmpeg"),
            ("node", True, "winget install OpenJS.NodeJS.LTS"),
            ("npx", True, "vem com o node"),
            ("yt-dlp", False, "uv sync (esta nas dependencias base)"),
            ("nvidia-smi", False, "so para aceleracao por GPU"))

MODELOS = ("core/helpers/models/face_detection_yunet_2023mar.onnx",
           "core/assets/models/blaze_face_short_range.tflite",
           "core/assets/models/selfie_multiclass_256x256.tflite")

# modulo importavel -> extra do pyproject (ou 'base')
EXTRAS = {"whisperx": "base", "cv2": "base", "scenedetect": "base", "librosa": "base",
          "mediapipe": "reframe", "pyannote.audio": "diarize", "sherpa_onnx": "parakeet",
          "torch": "matting / scenes-neural", "pycolmap": "camera 3D (declarar no pyproject)"}


def doctor() -> int:
    falhas = 0
    print("Binarios")
    for b, obrig, dica in BINARIOS:
        if shutil.which(b):
            print(f"  {OK}{b}")
        else:
            print(f"  {BAD if obrig else WARN}{b:10} {dica}")
            falhas += obrig
    print("Pastas da suite")
    for d in ("core", "engines", "motion-vfx", "external", "manifests"):
        n = sum(1 for _ in (SUITE / d).iterdir()) if (SUITE / d).is_dir() else 0
        print(f"  {OK if n else BAD}{d:11} {n} itens")
        falhas += not n
    print("Skills (cada pasta precisa de SKILL.md)")
    for grp in ("engines", "motion-vfx"):
        sem = [p.name for p in (SUITE / grp).iterdir() if p.is_dir() and not (p / "SKILL.md").exists()]
        print(f"  {OK if not sem else WARN}{grp}: " + ("todas com SKILL.md" if not sem else "sem SKILL.md -> " + ", ".join(sem)))
    print("Modelos")
    for m in MODELOS:
        inst = Path.home() / ".claude/skills/prisma" / m.removeprefix("core/")
        ok = (SUITE / m).is_file() or inst.is_file()
        print(f"  {OK if ok else BAD}{m}")
        falhas += not ok
    print("Recursos externos (vendor)")
    v = SUITE / "external/prisma-video-skills"
    gits = sum(1 for p in v.iterdir() if (p / ".git").exists()) if v.is_dir() else 0
    print(f"  {OK if gits else BAD}{gits} repositorios git em {v.relative_to(SUITE)}")
    falhas += not gits
    print("Extras Python (no .venv do core, se existir)")
    cands = [Path.home() / ".claude/skills/prisma/.venv/Scripts/python.exe", Path.home() / ".claude/skills/prisma/.venv/bin/python",
             SUITE / "core/.venv/Scripts/python.exe", SUITE / "core/.venv/bin/python"]
    py = next((c for c in cands if c.exists()), cands[0])
    if not py.exists():
        print(f"  {WARN}nenhum .venv do Prisma — rode: python prisma-suite.py install")
    else:
        for mod, extra in EXTRAS.items():
            r = subprocess.run([str(py), "-c", f"import importlib.util as u,sys;sys.exit(0 if u.find_spec('{mod.split('.')[0]}') else 1)"])
            print(f"  {OK if r.returncode == 0 else WARN}{mod:15} ({extra})")
    print("\n" + ("PRONTO" if not falhas else f"{falhas} problema(s) obrigatorio(s)"))
    return 1 if falhas else 0


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "doctor"
    if cmd == "doctor":
        return doctor()
    if cmd == "install":
        return subprocess.call([sys.executable, str(SUITE / "install-suite.py"), *sys.argv[2:]])
    if cmd == "manifest":
        return subprocess.call([sys.executable, str(SUITE / "manifests/build_manifest.py")])
    if cmd == "map":
        print((SUITE / "ECOSYSTEM.md").read_text(encoding="utf-8"))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
