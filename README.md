<p align="center">
  <img src="brand/banner-suite.svg" alt="PRISMA SUITE" width="100%">
</p>

<p align="center">
  <b>O Prisma e todo o seu ecossistema</b> — editor de vídeo por conversa, motores de render, motion/VFX, trilha e 24 recursos externos.<br>
  <sub>Claude Code &nbsp;·&nbsp; HyperFrames + Remotion &nbsp;·&nbsp; instalação em um comando</sub>
</p>

---

# Prisma-Suite

O Prisma (editor de video por conversa) e tudo que o orbita, numa pasta so.
Mapa de tarefas, helpers e skills: **[ECOSYSTEM.md](ECOSYSTEM.md)**.

```bash
git clone --recurse-submodules https://github.com/wellington3105/Prisma-Suite.git
cd Prisma-Suite
python prisma-suite.py install                  # skills no Claude Code, modelos, uv sync, caminhos
python prisma-suite.py install --separador auto # + separador de voz (Python 3.11; GPU se houver NVIDIA)
python prisma-suite.py doctor                   # confere tudo
```

O repositório é privado: no primeiro `git clone`, o Git abre o login do GitHub no navegador (uma vez só por máquina).
Antes: `uv`, `ffmpeg`, `node` 18+ e `git` (o instalador diz como instalar o que faltar).
Depois: preencha `~/.claude/skills/prisma/.env` so com as chaves que for usar, e reabra o Claude Code.

| Pasta | Conteudo | Como entra |
|---|---|---|
| `core/` | repo Prisma | submodulo (wellington3105/Prisma) |
| `external/prisma-video-skills/*` | 24 recursos externos | 24 submodulos fixados por commit |
| `engines/`, `motion-vfx/` | HyperFrames, Remotion, GSAP, Three.js, Rive, Lottie... | copiados (arquivos) |
| `manifests/` | versoes fixas (`ecosystem.lock.json`) | gerado por `prisma-suite.py manifest` |

## Identidade visual

A marca é a do Prisma (abertura de câmera, ver `core/references/brand.md`): `brand/prisma-logo.svg` (símbolo + nome),
`brand/prisma-mark.svg` (favicon/avatar), `brand/banner.svg` e `brand/banner-suite.svg` (fundo `#07080a`).

## O que um clone NAO traz

- **Modelos** (`.onnx`/`.tflite`): fora do git; o `install` baixa os tres das fontes oficiais (OpenCV Zoo e MediaPipe).
- **`.env`** com as chaves: nunca versionado; use `core/.env.example`.
- **`external/prisma-video-skills/motion-skills-packs/`** (152 MB, sem git proprio): existe so
  na maquina de origem.
- `core/.venv`, `node_modules` e caches de modelos (~9 GB): reconstruidos por `uv sync` e no primeiro uso.

As skills de `engines/` e `motion-vfx/` sao copias de projetos de terceiros (origem e hash em
`manifests/ecosystem.lock.json`); cada uma segue a licenca do seu autor.
