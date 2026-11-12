# Análise — pacote "trilha-cinematografica-claude-code" (@iamjeff.ia)

Fonte: `Downloads/trilha-cinematografica-claude-code-20261112T123554Z-1-001.zip`
Extraído (sem executar nada) em `Downloads/_extract-trilha/`. Data: 2026-11-12.

## 1. O que é

Um método, com scripts, para transformar a intro de uma música real numa **abertura de cinema**:
voz do cantor quase sozinha com reverb de sala de concerto, efeitos tonais no tom da música
em volta (ping, drones, cello pergunta/resposta, acordes fatiados, risers) e a música inteira
entrando seca no drop. Tudo medido (tom, BPM, afinação, bumbo) e mixado por Python + ffmpeg em
−14 LUFS. Exemplo aprovado: intro de "Laugh Now Cry Later" (Drake), 11 versões até a final.

| Pasta | Conteúdo |
|---|---|
| `1-video/` | o Reel do método, 64 s, 1080×1920, h264/aac (69,8 MB) |
| `2-projeto/` | 17 scripts + `plano-exemplo.json` + `plano-so-efeitos-comuns.json` + README + requirements |
| `3-skill-trilha-cinematografica/` | skill `trilha-cinematografica`: SKILL.md + 4 references + cópia dos scripts |
| `4-prompt/PROMPT.md` | prompt para colar no Claude Code com a sua música |

Os 17 scripts de `2-projeto/scripts` e `3-skill…/scripts` são **byte a byte idênticos** (verificado com `cmp`).

## 2. Segurança

- 46 arquivos, nenhum caminho absoluto nem `..`.
- Scripts: só `numpy scipy soundfile librosa pyloudnorm pedalboard matplotlib`, opcionais `faster_whisper` e `essentia`.
  Chamadas externas: apenas `ffmpeg` e o executável `audio-separator` (via `subprocess`, lista de argumentos, sem shell).
- Sem `eval`/`exec`, sem rede direta, sem chaves. O único download é o do modelo de separação
  (`melband_roformer_big_beta4.ckpt`, ~1,5 GB) feito pelo próprio `audio-separator` na primeira execução,
  para `../modelos` ao lado dos scripts.
- `PROMPT.md` não tem instruções suspeitas (só pede para instalar a skill e trocar os colchetes).

## 3. O pipeline (10 passos da skill)

1. Combinar o "pronto" (uso, duração, narração depois do drop?, entregas).
2. `medir_musica.py musica.wav --bumbo INI FIM` → tom/relativo, BPM, compasso, afinação (cents), segundo do bumbo.
3. `separar_voz.py musica.wav voz.wav --dur 50` → MelBand RoFormer Big Beta 4 (nota 8,5 vs 4 da acapella do YouTube no teste cego).
4. Sons por papel e por tom (`references/papeis-e-tom.md`); `medicao/match.py` ranqueia candidatos contra uma referência.
5. Tempos: `medicao/tr.py` (palavras, faster-whisper), `chromat.py` (harmonia), `env.py` (ataque do grave), `chords.py`, `onsets.py`, `notes.py`, `align.py`.
6. Plano JSON (`duracao`, `saida_lufs`, `tom`, `momentos`, `camadas`; `{tom}`/`{nota}` substituídos; risers com `pico_em`) → `trilha_momentos.py` (rascunho).
7. `prep_voz.py` → reverb Concert Hall 4 s, predelay 20 ms, mix 0,407.
8. `stems.py` + `mix_voz_na_frente.py` → médio dos tonais ≥ 5 dB abaixo da voz (até −7 dB), grave −2 dB no máx.; −14 LUFS, pico < −1 dBFS.
9. `conferir.py` (espectrograma vs referência, vídeo A/B para o Gemini) + `medicao/bands.py` (balanço por faixa, drop como régua ±1 dB).
10. Entregar WAV final, camadas, plano e uma linha de resumo.

Regras fortes: voz é prioridade; cello só nos respiros; acordes no 1º tempo numa palavra forte;
drop seco (fade 20–60 ms); ping só no médio (150 Hz–2,2 kHz); **regra do relativo maior** (nunca
maior na mesma tônica de uma música menor); medir antes de culpar um efeito.

## 4. Comparação com o Prisma

| Capacidade | Prisma hoje | Trilha cinematográfica | Veredito |
|---|---|---|---|
| Achar trilha | `epidemic_music.py`, `treblo_music.py`, `references/soundtrack.md` | — (parte de uma música que você já tem) | complementar |
| Tempo/batida/drop | `beat_map.py` (BPM, beats, downbeats, hits, drops) | `medir_musica.py` (+ tom, afinação, bumbo exato) | **somar**: tom e afinação o Prisma não mede |
| Separar voz da música | não tem separação real; `music_carve.py` só divide em bandas | `separar_voz.py` (RoFormer Big Beta 4) | **lacuna que preenche** |
| Voz por cima da música | `music_carve.py` (side-chain só no médio), `deliver_mix.py` (ducking + loudnorm 2 passadas) | `mix_voz_na_frente.py` (médio ≥5 dB abaixo, grave −2 dB) | mesma ideia; o Prisma é para FALA, este para VOZ CANTADA |
| Loudness | `deliver_mix.py` −14 LUFS, `qa_mix.py` TP ≤ −1 dBTP | −14 LUFS, pico < −1 dBFS | **idênticos** no alvo |
| Efeitos sonoros | `sfx_*` (whoosh, hit, synth, index de bibliotecas) | sons **tonais no tom** por papel | **somar**: o Prisma não escolhe SFX pelo tom |
| Arranjo/linha do tempo de camadas | não tem | `trilha_momentos.py` + plano JSON | **novo** |
| Conferência | `qa_mix.py` | espectrograma vs referência, balanço por faixa, A/B | **somar** a `qa_mix` |
| Timeline animada do Reel | HyperFrames (motor do Prisma) | só descrita no LEIA-ME (sem código) | ideia para uma cena HyperFrames |

**Por que importa:** o Prisma trata a trilha como *fundo* (escolher, abaixar sob a fala, normalizar).
Este pacote trata a trilha como *peça de abertura* (arranjar uma música real em camadas no tom, até o drop).
Os dois alvos de mixagem já coincidem (−14 LUFS, pico −1), então a integração é natural na Fase 3.

## 5. Dependências que faltam no venv do Prisma

Já existem: numpy 2.4.6, scipy 1.18.0, soundfile 0.14.0, librosa 1.0.0, matplotlib 3.11.1, faster-whisper 1.2.1.
**Faltam:** `pyloudnorm`, `pedalboard` (pip comum) e `audio-separator` (ambiente **Python 3.11 separado**).
`essentia` é opcional e não roda no Windows nativo (só WSL).
Modelo de separação: ~1,5 GB no primeiro uso; separação ~15 s por 50 s de áudio com GPU NVIDIA (a máquina tem RTX 5070).

## 6. Riscos e limites

- **Direitos autorais:** o método usa a voz de uma gravação comercial (o exemplo é Drake). Para cliente ou
  conteúdo monetizado, só com música licenciada (Epidemic tem stems) ou autorização. O Reel do pacote é
  material do autor — não redistribuir.
- **Sons não vêm no pacote:** o plano aponta para `sons/drone-1-{tom}.wav`, `cello-{nota}.wav`, `riser-*`, etc.
  É preciso uma biblioteca de sons tonais nos 12 tons. O `sfx_index.py` do Prisma poderia indexá-la.
- **Gemini como ouvido:** segunda opinião opcional; envia áudio a um serviço externo — pedir autorização.
- **Não testado aqui:** nenhum script foi executado. Falta rodar com uma música e sons reais.

## 7. Recomendação

Integrar como **skill de Fase 3 do Prisma** ("abertura cinematográfica"), não como substituta:
1. Copiar a skill para `~/.claude/skills/trilha-cinematografica` e `Prisma-Suite/audio/trilha-cinematografica`
   (uma cópia dos scripts só; descartar a duplicata de `2-projeto`). Manter `plano-exemplo.json` e o PROMPT como exemplos.
2. Extras no Prisma: `pyloudnorm` e `pedalboard` como extra `cinematic` no `pyproject`; `audio-separator` num
   `.venv-separador` (Py 3.11) documentado no `ECOSYSTEM.md`.
3. Ligações: `beat_map.py` ↔ `medir_musica.py`; `epidemic_music.py` (stems licenciados) como fonte preferida;
   `sfx_index.py` para indexar a biblioteca tonal por tom; `qa_mix.py` continua sendo o gate final.
4. Rota no Maestro: "trilha cinematográfica", "intro de cinema", "build-up até o drop", "remix estilo trailer".
5. Teste de aceite: uma música licenciada do Epidemic + sons tonais → plano → mix → `qa_mix.py` dentro do alvo.
