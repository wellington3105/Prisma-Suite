# Prisma-Suite

O Prisma (editor de video por conversa) e tudo que o orbita, numa pasta so.
Mapa de tarefas, helpers e skills: **[ECOSYSTEM.md](ECOSYSTEM.md)**.

```bash
gh auth login                                   # o repositorio e privado
git clone --recurse-submodules https://github.com/wellington3105/Prisma-Suite.git
cd Prisma-Suite
python prisma-suite.py install                  # skills no Claude Code, modelos, uv sync, caminhos
python prisma-suite.py install --separador auto # + separador de voz (Python 3.11; GPU se houver NVIDIA)
python prisma-suite.py doctor                   # confere tudo
```

Antes: `uv`, `ffmpeg`, `node` 18+ e `git` (o instalador diz como instalar o que faltar).
Depois: preencha `~/.claude/skills/prisma/.env` so com as chaves que for usar, e reabra o Claude Code.

| Pasta | Conteudo | Como entra |
|---|---|---|
| `core/` | repo Prisma | submodulo (wellington3105/Prisma) |
| `external/prisma-video-skills/*` | 24 recursos externos | 24 submodulos fixados por commit |
| `engines/`, `motion-vfx/` | HyperFrames, Remotion, GSAP, Three.js, Rive, Lottie... | copiados (arquivos) |
| `manifests/` | versoes fixas (`ecosystem.lock.json`) | gerado por `prisma-suite.py manifest` |

## O que um clone NAO traz

- **Modelos** (`.onnx`/`.tflite`): fora do git; o `install` baixa os tres das fontes oficiais (OpenCV Zoo e MediaPipe).
- **`.env`** com as chaves: nunca versionado; use `core/.env.example`.
- **`external/prisma-video-skills/motion-skills-packs/`** (152 MB, sem git proprio): existe so
  na maquina de origem.
- `core/.venv`, `node_modules` e caches de modelos (~9 GB): reconstruidos por `uv sync` e no primeiro uso.

As skills de `engines/` e `motion-vfx/` sao copias de projetos de terceiros (origem e hash em
`manifests/ecosystem.lock.json`); cada uma segue a licenca do seu autor.
