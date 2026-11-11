# Prisma-Suite

O Prisma (editor de video por conversa) e tudo que o orbita, numa pasta so.
Mapa de tarefas, helpers e skills: **[ECOSYSTEM.md](ECOSYSTEM.md)**.

```bash
git clone --recurse-submodules https://github.com/wellington3105/Prisma-Suite.git
cd Prisma-Suite
python prisma-suite.py doctor        # confere binarios, skills, modelos, vendor
cd core && uv sync                   # dependencias Python do Prisma
cp .env.example .env                 # preencha so as chaves que for usar
```

| Pasta | Conteudo | Como entra |
|---|---|---|
| `core/` | repo Prisma | submodulo (wellington3105/Prisma) |
| `external/prisma-video-skills/*` | 24 recursos externos | 24 submodulos fixados por commit |
| `engines/`, `motion-vfx/` | HyperFrames, Remotion, GSAP, Three.js, Rive, Lottie... | copiados (arquivos) |
| `manifests/` | versoes fixas (`ecosystem.lock.json`) | gerado por `prisma-suite.py manifest` |

## O que um clone NAO traz

- **Modelos** (`.onnx`/`.tflite`): ignorados pelo git do Prisma. Veja `models/MODELOS.md`
  (o YuNet tem URL de download em `core/helpers/safe_layout.py`).
- **`.env`** com as chaves: nunca versionado; use `core/.env.example`.
- **`external/prisma-video-skills/motion-skills-packs/`** (152 MB, sem git proprio): existe so
  na maquina de origem.
- `core/.venv`, `node_modules` e caches de modelos (~9 GB): reconstruidos por `uv sync` e no primeiro uso.

As skills de `engines/` e `motion-vfx/` sao copias de projetos de terceiros (origem e hash em
`manifests/ecosystem.lock.json`); cada uma segue a licenca do seu autor.
