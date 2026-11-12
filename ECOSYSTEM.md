# Prisma-Suite — mapa do ecossistema

Pasta única local. O Prisma (`core/`) é o editor; o resto são os motores, as skills de
motion/VFX/3D e os recursos externos que ele usa. Versões fixas em
`manifests/ecosystem.lock.json` (regerar: `python prisma-suite.py manifest`).
Conferir a instalação: `python prisma-suite.py doctor`.

> Estado: **cópia local**. Os originais (`~/.claude/skills/*`, `~/.aiox-global/vendor/…`)
> continuam intactos e são o que o Claude Code carrega hoje. Nada aqui foi publicado.

## Pastas

| Pasta | O que é | Origem |
|---|---|---|
| `core/` | repo Prisma (com `.git`): helpers, references, assets, instaladores, `skill-aliases/` | `~/.claude/skills/prisma` |
| `engines/` | motores de render e mídia: `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`, `slideshow`, `remotion-best-practices`, `remotion-motion-graphics` | `~/.claude/skills` |
| `motion-vfx/` | `animate`, `rive-skills`, `text-to-lottie`, `wiggle-claude-skill`, `texto-slice-em-perspectiva`, 8 `gsap-*`, 10 `threejs-*` | `~/.claude/skills` |
| `external/prisma-video-skills/` | os 24 recursos externos (1,7 GB, repos git aninhados) + `manifest.json` | `~/.aiox-global/vendor` |
| `models/` | índice dos modelos; os arquivos ficam em `core/` onde o código os procura | ver `models/MODELOS.md` |
| `manifests/` | `build_manifest.py` e `ecosystem.lock.json` | gerado |

## Tarefa → onde está

| Tarefa | Helper (`core/helpers/`) | Skill / referência |
|---|---|---|
| Transcrever, revisar, segunda escuta | `transcribe`, `revise_transcript`, `second_listen` | `core/references/transcription.md`, `transcript-review.md` |
| Cortar, EDL, verificar corte | `build_edl`, `verify_cut` | `core/SKILL.md` (Fase 1) |
| Cor, LUT, HDR | `grade`, `hdr_lut` | `core/references/log-grade.md`, `color-multitake.md` |
| Rastrear rosto, reenquadrar | `face_track` (Haar), `reframe`, `safe_layout` (YuNet) | `core/references/shortform.md` |
| Multicâmera | `multicam` (YuNet no master 4K), `sync_sources`, `diarize` | `core/references/multicam.md` |
| Speed ramp, edição na batida | `speed_ramp`, `beat_edit`, `beat_map` | `core/references/beat-sync.md`, `cinema-motion.md` |
| Cinema / câmera 3D | `cinema_edit`, `camera_solve`, `camera_solve_colmap`, `camera_track` | `core/OPUS-VFX-3D.md`, `compositing.md` |
| Motion graphics / cenas | `hf_motion_scenes`, `build_hyperframes`, `export_hyperframes` | `engines/hyperframes`, `core/references/hyperframes-engine.md`, `motion-craft.md` |
| Fallback de render | `captions_for_remotion` | `engines/remotion-best-practices`, `remotion-motion-graphics` |
| Legendas | `caption_style`, `captions_srt` | `core/references/shortform.md` |
| SFX e trilha | `sfx_events`, `sfx_index`, `sfx_peak`, `sfx_synth` | `core/references/sfx-craft.md`, `soundtrack.md` |
| Inserts / B-roll | `inserts_plan` | `engines/media-use`, `core/references/scenes.md` |
| Animação web (GSAP, Rive, Lottie, Three.js) | — | `motion-vfx/*` |
| Texto preso à parede em perspectiva, atrás da pessoa, cortado ("slice") | apoio: `detect_plane`, `person_matte` | `motion-vfx/texto-slice-em-perspectiva` (`scripts/slice_texto.py config.json prova|final`; câmera parada) |
| Recurso de terceiros (Clipify, OpenMontage…) | `helpers/external_skills.py list` | `external/prisma-video-skills/`, `core/references/external-video-skills.md` |

Os nomes de helper acima vêm da listagem de `core/helpers/`; para argumentos e ordem de uso,
a fonte é sempre o `SKILL.md` e a `references/` correspondente.

## Programas e extras

- **Sistema:** `uv`, `ffmpeg`, `ffprobe`, `node` 18+, `npx`; `yt-dlp` (vem no `uv sync`); `nvidia-smi` opcional.
- **Python base:** whisperx, opencv-python-headless 4.10, scenedetect, librosa, yt-dlp.
- **Extras:** `reframe` (mediapipe), `diarize` (pyannote.audio), `parakeet` (sherpa-onnx), `matting`/`scenes-neural` (torch), `animations` (manim).
- **Fora do pyproject:** `pycolmap` (instalado à mão; a câmera 3D depende dele).
- **Node:** HyperFrames `0.8.93` via `npx`; Remotion + three + @react-three/fiber nos `package.json` de `core/assets/*`.

## Serviços e MCPs

| Serviço | Como o Prisma usa | Chave (`core/.env.example`) |
|---|---|---|
| **Epidemic Sound** (MCP oficial) | `helpers/epidemic_music.py` fala MCP por HTTP puro (`search`, `sfx`, `sfx-download`); não depende do MCP estar ligado no agente | `EPIDEMIC_SOUND_MCP_API_KEY` |
| Treblo | `helpers/treblo_music.py` — trilha por IA | `TREBLO_API_KEY` |
| Pexels | `helpers/pexels_search.py` — banco de imagens/vídeo | `PEXELS_API_KEY` |
| Postiz | publicação (opcional) | `POSTIZ_API_KEY`, `POSTIZ_BASE_URL` |
| Hugging Face | pyannote (diarização) | `HF_TOKEN` |
| Premiere (MCP) | rota alternativa de edição: `core/references/premiere-mcp.md` | — |

Registrar downloads de banco/licença com `media_ledger.py`. Chaves reais só no `.env` (ignorado pelo git).

## Pendências conhecidas

1. `pycolmap` não declarado no `core/pyproject.toml`.
2. Modelos `.onnx`/`.tflite` estão no `.gitignore` do core: a suite os guarda, o repositório não.
3. O registro externo e os aliases ainda apontam para os caminhos originais (`~/.aiox-global/vendor`, `C:\Users\welli\.claude\skills\prisma`). Trocar para a suite só depois de validar.
4. `edvid` e `edvid.code-backup` (skills antigas) não foram copiadas: decidir se aposentam.
