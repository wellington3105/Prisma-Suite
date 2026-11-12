#!/usr/bin/env python3
"""Instala o Prisma-Suite numa maquina: todas as skills no Claude Code, caminhos corrigidos,
modelos, dependencias Python e (opcional) o separador de voz.

Uso (de dentro da pasta do Prisma-Suite clonada com --recurse-submodules):
    python install-suite.py                     # instala/atualiza o que falta
    python install-suite.py --force             # atualiza por cima das skills ja instaladas
    python install-suite.py --separador auto    # tambem cria o ambiente do separador de voz
    python install-suite.py --home D:/teste     # instala em outra pasta de usuario (teste)

Nunca apaga nada: com --force copia por cima e preserva arquivos locais (.env, .venv, modelos).
Nunca toca numa skill que seja clone git ou link. Somente biblioteca padrao.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8")

SUITE = Path(__file__).resolve().parent
ORIGIN_PRISMA = r"C:\Users\welli\.claude\skills\prisma"        # caminho gravado nos aliases
ORIGIN_LIB = r"C:\Users\welli\.aiox-global\vendor\prisma-video-skills"
ORIGIN_SKILLS = r"C:\Users\welli\.claude\skills"
GRUPOS = ("engines", "motion-vfx", "audio")
IGNORAR = shutil.ignore_patterns(".git", ".venv", ".venv-separador", "node_modules", "__pycache__",
                                 "*.pyc", ".env", "out", "output", "build", "sparse", "*.log", "modelos")
MODELOS = (  # destino dentro da skill prisma, URL oficial
    ("helpers/models/face_detection_yunet_2023mar.onnx",
     "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"),
    ("assets/models/blaze_face_short_range.tflite",
     "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite"),
    ("assets/models/selfie_multiclass_256x256.tflite",
     "https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite"),
)
avisos: list[str] = []


def log(msg: str = "") -> None:
    print(msg, flush=True)


def instalar(src: Path, dest: Path, force: bool) -> str:
    if dest.is_symlink() or (dest / ".git").exists():
        return "pulada (link ou clone git — nunca tocado)"
    if dest.exists() and not force:
        return "ja existe (use --force para atualizar)"
    novo = not dest.exists()
    shutil.copytree(src, dest, ignore=IGNORAR, dirs_exist_ok=True)
    return "instalada" if novo else "atualizada"


def trocar_texto(arq: Path, pares: list[tuple[str, str]]) -> None:
    if not arq.is_file():
        return
    t = arq.read_text(encoding="utf-8")
    n = t
    for a, b in pares:
        n = n.replace(a, b)
    if n != t:
        arq.write_text(n, encoding="utf-8")


def baixar(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(url, timeout=120) as r, open(tmp, "wb") as f:
        shutil.copyfileobj(r, f)
    tmp.replace(dest)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12]


def run(cmd: list[str], cwd: Path | None = None) -> bool:
    log("    $ " + " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd).returncode == 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--home", type=Path, default=Path.home(), help="pasta de usuario de destino")
    ap.add_argument("--force", action="store_true", help="atualizar skills ja instaladas (copia por cima)")
    ap.add_argument("--no-sync", action="store_true", help="nao rodar uv sync no Prisma")
    ap.add_argument("--extras", default="cinematic", help="extras do Prisma, separados por virgula (ex.: cinematic,reframe,camera3d)")
    ap.add_argument("--sem-modelos", action="store_true", help="nao baixar os modelos de rosto/segmentacao")
    ap.add_argument("--separador", choices=("no", "auto", "gpu", "cpu"), default="no",
                    help="criar o ambiente Python 3.11 do separador de voz (trilha-cinematografica)")
    a = ap.parse_args()
    skills = a.home / ".claude" / "skills"
    prisma = skills / "prisma"

    log(f"Prisma-Suite — instalacao\n  suite:  {SUITE}\n  skills: {skills}\n")

    # 1. a suite esta completa?
    if not (SUITE / "core" / "SKILL.md").is_file():
        log("! core/ vazio — inicializando o submodulo do Prisma")
        if not run(["git", "submodule", "update", "--init", "core"], cwd=SUITE):
            log("x nao consegui baixar o core. Clone com: git clone --recurse-submodules <url>")
            return 1
    ext = SUITE / "external" / "prisma-video-skills"
    n_ext = sum(1 for p in ext.iterdir() if (p / ".git").exists()) if ext.is_dir() else 0
    if n_ext < 24:
        avisos.append(f"recursos externos: {n_ext}/24 baixados — rode `git submodule update --init --recursive`")

    # 2. skills
    skills.mkdir(parents=True, exist_ok=True)
    log("skills:")
    log(f"  prisma: {instalar(SUITE / 'core', prisma, a.force)}")
    for g in GRUPOS:
        for d in sorted(p for p in (SUITE / g).iterdir() if p.is_dir() and (p / "SKILL.md").exists()):
            log(f"  {d.name}: {instalar(d, skills / d.name, a.force)}")
    for d in sorted(p for p in (SUITE / "core" / "skill-aliases").iterdir() if p.is_dir()):
        r = instalar(d, skills / d.name, a.force)
        trocar_texto(skills / d.name / "SKILL.md", [(ORIGIN_PRISMA, str(prisma))])
        log(f"  {d.name}: {r}")

    # 3. caminhos desta maquina
    if prisma.is_dir() and not (prisma / ".git").exists():
        (prisma / ".prisma-suite").write_text(str(SUITE), encoding="utf-8")
        trocar_texto(prisma / "references" / "external-video-skills.md",
                     [(ORIGIN_LIB, str(ext)), (ORIGIN_SKILLS, str(skills))])
        env, exemplo = prisma / ".env", prisma / ".env.example"
        if not env.exists() and exemplo.exists():
            shutil.copy2(exemplo, env)
            avisos.append(f"preencha as chaves que for usar em {env}")

    # 4. modelos
    if not a.sem_modelos and prisma.is_dir():
        log("\nmodelos:")
        for rel, url in MODELOS:
            dest, local = prisma / rel, SUITE / "core" / rel
            if dest.is_file():
                log(f"  ok {rel} ({sha(dest)})")
                continue
            try:
                if local.is_file():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(local, dest)
                    log(f"  copiado {rel} ({sha(dest)})")
                else:
                    baixar(url, dest)
                    log(f"  baixado {rel} ({sha(dest)})")
            except Exception as e:  # noqa: BLE001
                avisos.append(f"modelo {rel} nao veio ({e}); baixe de {url}")

    # 5. dependencias Python do Prisma
    uv = shutil.which("uv")
    if not a.no_sync and prisma.is_dir():
        log("\npython (uv sync):")
        if not uv:
            avisos.append("uv ausente — winget install astral-sh.uv (ou brew install uv) e rode de novo")
        else:
            cmd = [uv, "sync"]
            for x in filter(None, (e.strip() for e in a.extras.split(","))):
                cmd += ["--extra", x]
            # Hardlink do cache do uv falha em alguns discos (OneDrive/arquivos de nuvem,
            # outro volume): os error 396. Copiar e mais lento, mas sempre funciona.
            if not run(cmd, cwd=prisma) and not run(cmd + ["--link-mode=copy"], cwd=prisma):
                avisos.append("uv sync falhou no Prisma — veja a mensagem acima")

    # 6. separador de voz (opcional)
    if a.separador != "no":
        alvo = skills / "trilha-cinematografica" / ".venv-separador"
        gpu = a.separador == "gpu" or (a.separador == "auto" and shutil.which("nvidia-smi"))
        log(f"\nseparador de voz ({'GPU' if gpu else 'CPU'}): {alvo}")
        py = alvo / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        ok = bool(uv) and run([uv, "venv", "--python", "3.11", str(alvo)])
        if ok and gpu:
            ok = run([uv, "pip", "install", "--python", str(py), "torch", "torchaudio",
                      "--index-url", "https://download.pytorch.org/whl/cu128"])
        if ok:
            ok = run([uv, "pip", "install", "--python", str(py), f"audio-separator[{'gpu' if gpu else 'cpu'}]"])
        if not ok:
            avisos.append("separador de voz nao instalado — veja a mensagem acima")

    # 7. programas do sistema
    log("\nprogramas:")
    for b, dica in (("ffmpeg", "winget install Gyan.FFmpeg | brew install ffmpeg"),
                    ("node", "winget install OpenJS.NodeJS.LTS | brew install node"),
                    ("uv", "winget install astral-sh.uv | brew install uv"),
                    ("git", "winget install Git.Git | brew install git")):
        if shutil.which(b):
            log(f"  ok {b}")
        else:
            log(f"  x  {b} — {dica}")
            avisos.append(f"{b} ausente")

    log("\n" + ("PRONTO, sem avisos." if not avisos else "Concluido com avisos:"))
    for x in avisos:
        log(f"  - {x}")
    log("\nFeche e reabra o Claude Code para ele carregar as skills novas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
