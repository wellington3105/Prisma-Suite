# Projeto: os scripts da trilha do Reel

Estes são os scripts que montaram a intro cinematográfica de "Laugh Now Cry Later" mostrada no Reel, limpos para rodar no seu computador. Eles não tocam em nenhum programa de áudio: tudo sai de Python e ffmpeg, a partir de um plano em JSON que diz qual som entra, em que segundo, em que nível e com que filtro.

A música, a voz separada e os sons ficam por sua conta. As pastas `musica/`, `prep/` e `sons/` são criadas por você, ao lado deste README, com os nomes que o plano espera.

## O que tem aqui

| Arquivo | Para que serve |
|---|---|
| `plano-exemplo.json` | o plano da versão aprovada do Reel: tempos, níveis e filtros de cada camada, com uma explicação (`_obs`) em cada uma |
| `plano-so-efeitos-comuns.json` | a versão "som normal" para comparar: mesma voz, mesmo drop, só boom, whoosh e prato invertido |
| `scripts/medir_musica.py` | tom, BPM, afinação e o segundo exato do bumbo do drop |
| `scripts/separar_voz.py` | separa a voz da música com o MelBand RoFormer Big Beta 4 |
| `scripts/prep_voz.py` | corta o trecho da voz e põe o reverb de sala de concerto (4 s, mix ~40%) |
| `scripts/prep_ping.py` | faz o golpe tonal de piano na tônica a partir de notas soltas de piano |
| `scripts/trilha_momentos.py` | o motor: lê o plano e mixa todas as camadas em −14 LUFS |
| `scripts/stems.py` | exporta cada grupo de camadas (ping, drones, cello, voz, acordes, risers, música) no mesmo ganho da mixagem |
| `scripts/mix_voz_na_frente.py` | a mixagem final, com a voz sempre por cima dos tonais |
| `scripts/conferir.py` | nível, pico, espectrograma ao lado da referência e um vídeo de comparação para ouvir |
| `scripts/medicao/` | ferramentas para medir uma referência: alinhamento, envelope, ataques, acordes, notas, faixas de frequência, ranking de sons parecidos e transcrição com tempo por palavra |
| `requirements.txt` | as bibliotecas de Python dos scripts |

Todo script mostra como usar quando você roda sem argumentos (`python scripts/trilha_momentos.py`).

## Instalação

1. **ffmpeg** no PATH. Windows: `winget install Gyan.FFmpeg`. Mac: `brew install ffmpeg`.
2. **Python 3.10 ou mais novo** para os scripts:
   ```bash
   pip install -r requirements.txt
   ```
   Se o `soundfile` reclamar ao importar, rode `pip install cffi`.
3. **Ambiente separado, em Python 3.11, para o separador de voz.** O `audio-separator` não instala no Python 3.14, porque uma dependência dele não compila. Dentro desta pasta:
   ```bash
   # Windows
   py -3.11 -m venv .venv-separador
   .venv-separador\Scripts\pip install "audio-separator[gpu]"     # com placa NVIDIA
   .venv-separador\Scripts\pip install "audio-separator[cpu]"     # sem placa NVIDIA

   # Mac (instale antes o Python 3.11: brew install python@3.11)
   python3.11 -m venv .venv-separador
   .venv-separador/bin/pip install "audio-separator[cpu]"
   ```
   O `separar_voz.py` acha esse ambiente sozinho. Com placa NVIDIA, se a separação rodar na CPU, instale antes o PyTorch com CUDA pelo seletor de pytorch.org e repita o `pip install "audio-separator[gpu]"`.
4. Opcional: `pip install faster-whisper` para o tempo de cada palavra da voz (`medicao/tr.py`) e `pip install essentia` (Mac ou Linux) para um tom mais confiável no `medir_musica.py`.

## Como montar as pastas

```
2-projeto/
├── musica/musica.wav          ← a música inteira (WAV ou FLAC; MP3 também funciona)
├── notas/A4.wav, A5.wav, A3.wav   ← notas soltas de piano na tônica, para o ping
├── prep/                      ← o que os scripts geram: voz.wav, voz-reverb.wav, ping.wav
├── sons/                      ← os seus sons, no tom da música
│   ├── drone-1-A.wav, drone-2-A.wav
│   ├── cello-C.wav            ← cello no relativo maior (Dó maior para uma música em Lá menor)
│   ├── acordes-C.wav          ← progressão de piano, também no relativo maior
│   ├── riser-1-A.wav, riser-2-A.wav
│   ├── impacto-A.wav
│   └── comuns/boom.wav, whoosh.wav, prato-invertido.wav   ← só para a versão "som normal"
└── saida/                     ← o que sai: mixagens, stems e camadas finais
```

No plano, `{tom}` vira o valor de `"tom"` (no exemplo, `A`), e `{nota}` vira a `"nota"` da camada (no exemplo, `C`, o relativo maior). Para outra música, mude o tom num lugar só e dê aos arquivos os nomes com a nota certa. Se preferir, escreva o caminho completo de cada arquivo no campo `"arquivo"`.

## Rodar o exemplo do começo ao fim

Com a música em `musica/musica.wav` e os sons em `sons/`, de dentro desta pasta:

```bash
python scripts/medir_musica.py musica/musica.wav --bumbo 28 32       # tom, BPM, afinação e bumbo do drop
python scripts/separar_voz.py musica/musica.wav prep/voz.wav --dur 50   # voz da própria música
python scripts/prep_voz.py prep/voz.wav prep/voz-reverb.wav --ini 1.0 --fim 31.0
python scripts/prep_ping.py prep/ping.wav notas/A4.wav notas/A5.wav notas/A3.wav
python scripts/trilha_momentos.py plano-exemplo.json saida/rascunho.wav  # rascunho rápido
python scripts/stems.py plano-exemplo.json saida/stems
python scripts/mix_voz_na_frente.py saida/stems saida/cinematografico.wav saida/camadas
python scripts/conferir.py saida/cinematografico.wav
```

O `saida/cinematografico.wav` é a versão final. O `saida/camadas/` traz cada grupo já com a prioridade da voz aplicada: somados, dão a mixagem, e servem para montar a trilha num editor ou para desenhar a timeline no vídeo.

Para a versão "som normal", rode `python scripts/trilha_momentos.py plano-so-efeitos-comuns.json saida/normal.wav`. Ela tem a mesma linha do tempo e o drop no mesmo nível da cinematográfica, então dá para alternar as duas no vídeo sem pulo de volume.

## O que trocar para a sua música

- **Tempos:** todos os `em`, `ate`, `pico_em` e `corte` do plano são da música do exemplo. O passo a passo do `LEIA-ME.md` da raiz mostra como achar os seus (voz, palavras fortes, compassos, bumbo).
- **Tom:** `"tom"` no topo do plano e a `"nota"` das camadas no relativo.
- **Cortes dos acordes:** os `corte` das fatias de acorde dependem do arquivo de progressão. Rode `python scripts/medicao/chords.py sons/acordes-C.wav` para ver onde começa cada acorde.
- **Trecho da voz:** `--ini` e `--fim` do `prep_voz.py`, em segundos da música.
- **Bumbo do drop:** o intervalo do `--bumbo` e, no plano, o `corte` e o `ataque` da camada da música.
- **Pasta dos modelos do separador:** `MODELOS`, no topo do `separar_voz.py` (o padrão é `modelos/`, ao lado de `scripts/`). Para usar um `audio-separator` instalado em outro lugar, aponte a variável de ambiente `AUDIO_SEPARATOR` para o executável.
- **Prioridade da voz:** `FOLGA_DB`, `MAX_DB` e `MAX_GRAVE_DB`, no topo do `mix_voz_na_frente.py`.

## Problemas comuns

- **"arquivo não encontrado"**: o caminho do plano parte da pasta onde está o JSON. Confira o nome com a nota (`drone-1-A.wav`) e a extensão.
- **A camada acaba antes da hora:** o arquivo é mais curto que o trecho pedido. Use um som mais longo ou repita a camada com outro `em` e `a_partir_de`.
- **A voz "some" em algum trecho:** rode o `mix_voz_na_frente.py` (a mixagem do `trilha_momentos.py` sozinho não protege a voz) ou suba `FOLGA_DB`.
- **Tudo soa desafinado:** confira a afinação no `medir_musica.py`. Acima de ±20 cents, troque de música ou corrija o tom dos sons antes.
