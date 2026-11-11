"""Gera ecosystem.lock.json: versoes fixas de tudo que o Prisma usa.
Le o estado real desta maquina (venv do Prisma, vendor, skills, caches de modelo)."""
import json, subprocess, sys, shutil, os, hashlib
from pathlib import Path
H = Path.home(); SUITE = Path(__file__).resolve().parent.parent
out = {"generated": __import__("datetime").date.today().isoformat(), "binaries": {}, "python": {}, "npm": {}, "skills": {}, "vendor": {}, "models": {}, "caches": {}}

def run(*a, cwd=None):
    try: return subprocess.run(a, capture_output=True, text=True, cwd=cwd, timeout=60).stdout.strip()
    except Exception as e: return f"erro: {e}"

for b in ("ffmpeg", "ffprobe", "node", "npm", "npx", "uv", "yt-dlp", "git"):
    p = shutil.which(b); out["binaries"][b] = {"path": p, "version": (run(p, "-version" if b in ("ffmpeg", "ffprobe") else "--version").splitlines() or [""])[0] if p else None}
out["binaries"]["nvidia-smi"] = {"path": shutil.which("nvidia-smi")}

venv_py = H/".claude/skills/prisma/.venv/Scripts/python.exe"
if venv_py.exists():
    for line in run(str(venv_py), "-m", "pip", "freeze").splitlines():
        if "==" in line:
            k, v = line.split("==", 1); out["python"][k.lower()] = v
    if not out["python"]:  # venv sem pip: le dist-info
        for d in (venv_py.parent.parent/"Lib/site-packages").glob("*.dist-info"):
            n, _, v = d.name[:-10].rpartition("-"); out["python"][n.lower().replace("_", "-")] = v
for pj in sorted((SUITE/"core/assets").glob("*/package.json")):
    d = json.loads(pj.read_text(encoding="utf-8")); out["npm"][pj.parent.name] = {**d.get("dependencies", {}), **d.get("devDependencies", {})}

lock = H/".agents/.skill-lock.json"
if lock.exists():
    for k, v in json.loads(lock.read_text(encoding="utf-8")).get("skills", {}).items():
        out["skills"][k] = {"source": v.get("source"), "path": v.get("skillPath"), "hash": v.get("skillFolderHash") or v.get("hash")}

vendor = H/".aiox-global/vendor/prisma-video-skills"
for d in sorted(p for p in vendor.iterdir() if p.is_dir()):
    if (d/".git").exists():
        out["vendor"][d.name] = {"remote": run("git", "remote", "get-url", "origin", cwd=d), "commit": run("git", "rev-parse", "HEAD", cwd=d),
                                 "dirty": bool(run("git", "status", "--porcelain", cwd=d))}
    else: out["vendor"][d.name] = {"git": False}

for f in list((SUITE/"core").rglob("*.onnx")) + list((SUITE/"core").rglob("*.tflite")):
    out["models"][str(f.relative_to(SUITE)).replace("\\", "/")] = {"bytes": f.stat().st_size, "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
for name, p in {"huggingface": H/".cache/huggingface", "torch": H/".cache/torch", "whisper": H/".cache/whisper"}.items():
    out["caches"][name] = {"path": str(p), "exists": p.exists(), "mb": round(sum(x.stat().st_size for x in p.rglob("*") if x.is_file())/1e6) if p.exists() else 0}

(SUITE/"manifests/ecosystem.lock.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print({k: len(v) for k, v in out.items() if hasattr(v, "__len__")})
