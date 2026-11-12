# Trilha cinematográfica com Claude Code

Este é o passo a passo do Reel "o meu Claude virou DJ". Nele, o Claude Code pegou "Laugh Now Cry Later", do Drake, e montou uma abertura de cinema: a voz do cantor quase sozinha, com eco de sala de concerto, efeitos tonais no tom da música em volta e a música inteira entrando de uma vez no drop (o momento em que a batida entra). O pacote traz o vídeo, os scripts que fizeram a trilha, uma skill que ensina o método ao seu Claude Code e um prompt para você fazer a versão de uma música sua.

Feito por **@iamjeff.ia**.

## Como a trilha foi feita

Ninguém abriu um programa de áudio para montar a trilha. O Claude Code mediu a música (tom, BPM, afinação, o segundo exato do bumbo), separou a voz da própria faixa, escolheu um som para cada papel (golpe, drones, cello, acordes, risers) e escreveu um plano em JSON com o segundo, o nível e o filtro de cada camada. Os scripts em Python montaram tudo com o ffmpeg. A cada versão, ele comparou a trilha com uma referência no espectrograma e no balanço de graves, médios e agudos, e ouviu as duas lado a lado com o Gemini. Foram 11 versões até a aprovada. As mudanças que mais pesaram vieram de três ajustes: o eco da voz, a qualidade da voz separada e a regra de que os tonais nunca passam por cima da voz.

## O que tem em cada pasta

| Pasta | O que é |
|---|---|
| `1-video/` | o Reel (`reel-claude-virou-dj.mp4`), 64 s, 1080×1920 |
| `2-projeto/` | os scripts que fizeram a trilha e o plano da versão aprovada. Comece pelo `README.md` de dentro |
| `3-skill-trilha-cinematografica/` | a skill `trilha-cinematografica`: o método, os números, as variações e uma cópia dos scripts |
| `4-prompt/` | `PROMPT.md`, para colar no Claude Code e fazer a versão cinematográfica de uma música sua |

## O que você precisa

- **Claude Code**.
- **ffmpeg** no PATH. Windows: `winget install Gyan.FFmpeg`. Mac: `brew install ffmpeg`.
- **Python 3.10 ou mais novo**, com `pip install numpy scipy soundfile librosa pyloudnorm pedalboard matplotlib` (ou o `requirements.txt` de `2-projeto/`).
- **Python 3.11 num ambiente separado para o `audio-separator`**, o separador de voz. No Python 3.14, uma dependência dele não compila. Os comandos estão no `2-projeto/README.md`. Com placa NVIDIA, um trecho de 50 s separa em ~15 s; na CPU, leva alguns minutos.
- **Os seus sons** para cada papel do passo 4, no tom da música.
- Opcional: `faster-whisper` (tempo de cada palavra da voz), um editor de áudio como o REAPER (para ajustar de ouvido) e uma conta no Gemini (para uma segunda opinião sobre a mixagem).

## Passo a passo

### 1. Escolha a música e o momento

Procure uma frase de voz forte que venha antes de uma entrada de batida. A intro vai da voz quase sozinha até esse bumbo. Na trilha do exemplo, a voz entra aos 9,9 s e o drop cai aos 39,4 s. Num vídeo curto, deixe uns 13 s antes da voz e o drop por volta dos 22 s, porque uma intro longa cansa.

### 2. Meça o tom, o BPM e a afinação

```bash
python 2-projeto/scripts/medir_musica.py musica.wav --bumbo 28 32
```

O script devolve o tom e o relativo, o BPM com a duração de um compasso, a afinação em cents e, com `--bumbo`, o segundo exato do bumbo dentro do intervalo. Confira o tom no Hooktheory ou no tunebat, porque detector de tom erra, principalmente entre o tom e o relativo. Desconfie também do BPM que aparece no Google: na música do exemplo ele dizia 134, e a medida deu 136. Se a afinação passar de ±20 cents, qualquer som tonal vai soar desafinado por cima dela.

No exemplo: Lá menor, 136 BPM, afinação padrão e bumbo do drop em 30,485 s da música.

### 3. Separe a voz da própria música

```bash
python 2-projeto/scripts/separar_voz.py musica.wav voz.wav --dur 50
```

O script chama o `audio-separator` com o modelo `melband_roformer_big_beta4.ckpt`, que baixa sozinho na primeira vez (~1,5 GB). O comando direto, se preferir:

```bash
audio-separator trecho.wav -m melband_roformer_big_beta4.ckpt --output_dir saida --output_format WAV
```

Saem dois arquivos, `(vocals)` e `(other)`. A voz fica alinhada com a música. Num teste cego com a mesma frase, no ouvido do Gemini, a voz separada por esse modelo teve nota 8,5; a acapella baixada do YouTube teve 4 e soou "oca, subaquática". Separe da música, mesmo que exista acapella oficial.

### 4. Escolha os sons no tom

Cada camada tem um papel. Use sons gravados no tom da música: os sons tonais costumam vir em versões para os 12 tons, e basta pegar a do tom certo.

| Papel | O que é | Onde entra |
|---|---|---|
| Golpe tonal ("ping") | uma nota de piano na tônica, com cauda longa de catedral, só no médio | no 1º quadro, de leve no 1º e no último acorde, e no drop |
| Drone e textura | som grave e contínuo, quase parado, no tom | de ~2,5 s até o drop, entrando em 4 s; dois juntos dão corpo |
| Melodia de cello | frases curtas de cello | sozinho antes da voz (a "pergunta") e no respiro depois da 1ª frase (a "resposta") |
| Progressão de acordes | piano tocando um acorde de cada vez | fatiada, um acorde por compasso, seguindo a harmonia da música |
| Risers | sons que crescem até um pico | dois, que começam ~5 s e ~3,7 s antes e têm o pico no drop |
| Impacto | golpe grave | no drop, junto com o bumbo |

Para o ping, o `prep_ping.py` monta o golpe a partir de notas soltas de qualquer piano sampleado. No exemplo, foram Lá4 e Lá5, com o Lá3 de leve, numa catedral de 8 s e filtrados entre 150 Hz e 2,2 kHz. Um golpe com grave demais embola com os acordes.

**A regra do tom.** Lá menor e Dó maior usam as mesmas sete notas: Dó maior é o relativo maior de Lá menor (a tônica do relativo maior fica 3 semitons acima da tônica menor). Por isso o cello e os acordes do exemplo estão em Dó maior, numa música em Lá menor, e soam certos. Numa música menor, use sons menores no tom, sons maiores no relativo maior e sons que servem para os dois modos. Nunca ponha um som maior na mesma tônica de uma música menor (Lá maior sobre Lá menor), nem o contrário: aí as terças brigam e tudo desafina.

### 5. Coloque cada camada na linha do tempo

A estrutura do exemplo, que vale como ponto de partida:

| Tempo | O que acontece |
|---|---|
| 0 s | o ping, sozinho, no 1º quadro |
| 2,5 s | os dois drones começam, com fade-in de 4 s, e vão até o drop |
| 4,2–10,6 s | o cello faz a "pergunta", sozinho |
| 9,9 s | entra a voz do cantor, com o reverb |
| 13,4–18 s | o cello "responde" no respiro da voz, mais baixo |
| 16,1 · 21,5 · 25,0 · 28,7 · 32,2 · 35,9 s | um acorde fatiado em cada um: Lám, Sol, Fá, Sol, Lám, Sol |
| 34,3 s e 35,7 s | os dois risers começam |
| 39,37 s | tudo corta seco; a música inteira entra no bumbo, com o ping e o impacto |

Como achar os seus tempos:

- **Acordes:** cada fatia cai no 1º tempo de um compasso, junto de uma palavra forte da voz, e segue o acorde que a música toca ali. Na música do exemplo, os acordes vieram do croma (`medicao/chromat.py`), e o tempo exato de cada um saiu dos saltos de energia abaixo de 80 Hz (`medicao/env.py`). As palavras e os respiros saem do `medicao/tr.py`. O arquivo de progressão do exemplo tinha 6 acordes de 8 s; o `medicao/chords.py` mostra onde começa cada um, para você fatiar.
- **Cello:** só nos respiros. Ele nunca toca por cima de uma frase cantada.
- **Risers:** o pico de cada um cai exatamente no drop. No plano, isso é `"pico_em"`, e o script calcula de onde cortar.
- **Drop:** a música inteira entra seca, no bumbo, sem respiro antes. O impacto vem do contraste entre a subida e a entrada da batida. O impacto tonal leva passa-altas de 60 Hz para não brigar com o bumbo da música.

Com os tempos na mão, copie o `2-projeto/plano-exemplo.json`, troque os tempos e os arquivos e rode o `trilha_momentos.py` para ouvir um rascunho.

### 6. Dê eco à voz e deixe a voz por cima

```bash
python 2-projeto/scripts/prep_voz.py voz.wav voz-reverb.wav --ini 1.0 --fim 31.0
```

O reverb imita um preset de sala de concerto: 4 s de decaimento, 20 ms de predelay, graves mais longos, agudos curtos e mix de ~40%. O eco fica uns 5 dB abaixo da voz. Nos testes, 50% com catedral deu eco demais, e 10 a 20% deixaram a voz "a capela demais". O reverb vai só na voz cantada; uma narração sua por cima do vídeo continua seca.

Depois, a mixagem com a voz na frente:

```bash
python 2-projeto/scripts/stems.py plano.json saida/stems
python 2-projeto/scripts/mix_voz_na_frente.py saida/stems saida/final.wav saida/camadas
```

Enquanto o cantor canta, o médio dos tonais (acima de 250 Hz, onde a voz mora) fica pelo menos 5 dB abaixo da voz, com redução de até 7 dB, e o grave desce no máximo 2 dB, para o piano não perder o peso. Uma redução fixa não resolve: no exemplo, com 2,5 dB fixos, um acorde ainda passava a voz em 2 a 5 dB, e a voz "se perdia" aos 17 s.

### 7. Mixe em −14 LUFS e confira

A mixagem já sai em −14 LUFS, com pico abaixo de −1 dBFS. Para conferir:

```bash
python 2-projeto/scripts/conferir.py saida/final.wav --ref referencia.wav --png espectro.png --video ab.mp4
```

- **Espectrograma:** a referência em cima e a sua versão embaixo, no mesmo tempo. Ali aparecem o golpe com sub demais, o piano sem baixo e o riser que não chega ao drop.
- **Balanço por faixa:** o `medicao/bands.py` compara graves, médios e agudos de cada trecho com a referência, as duas sem voz. O drop é a mesma música nas duas e serve de régua: ele tem de bater em até ~1 dB.
- **Ouvido:** ouça você. Para uma segunda opinião, o `ab.mp4` toca a referência, 2 s de silêncio e a sua versão, e pode ir para o Gemini com uma pergunta como esta: "Compare as duas trilhas. Dê uma nota de 0 a 10 de semelhança, liste os problemas da segunda com o tempo de cada um e diga o que corrigir, em números." O Gemini erra nome de instrumento, mas acerta estrutura, nível e artefato.

Antes de mexer no que parece errado, meça. No exemplo, "a voz some aos 17 s" parecia culpa do limitador; a medida mostrou que o limitador nem agia e que o acorde estava acima da voz.

A referência é opcional. Sem ela, o espectrograma e o balanço servem para comparar uma versão sua com a anterior.

## Como pedir tudo isso ao Claude Code

1. Copie a pasta `3-skill-trilha-cinematografica` para `~/.claude/skills/trilha-cinematografica/` (vale para todos os projetos) ou para `.claude/skills/trilha-cinematografica/` dentro do seu projeto. No Windows, `~` é a sua pasta de usuário (`%USERPROFILE%`).
2. Abra o `4-prompt/PROMPT.md`, troque o que está entre colchetes (música, momento, pasta dos sons, pasta de trabalho) e cole no Claude Code.
3. Ele mede a música, separa a voz, monta o plano e mostra a tabela de camadas antes de mixar. Você ouve, aponta o segundo que incomoda e ele corrige.

## O antes e depois do Reel

O Reel compara a mesma frase da música nas duas versões, para a diferença ficar clara. Primeiro toca a original, num ambiente cinza com um clipe só na timeline. A música para com um efeito de fita parando, o cursor volta, o clipe se divide em voz e instrumental, e a mesma frase toca de novo, agora com os tonais. Cada camada acende na timeline pelo nível real dela, até o drop. O drop da versão cinematográfica sai no mesmo nível do da original, então a diferença que se ouve vem só do arranjo.

Para montar uma comparação assim, o `2-projeto/plano-so-efeitos-comuns.json` faz uma terceira versão, com a mesma voz e o mesmo drop e só efeitos comuns (boom, whoosh, prato invertido). As duas têm a mesma linha do tempo, e dá para alternar entre elas no meio do vídeo sem pulo de volume.

**Bônus, a timeline viva.** No Reel, a trilha aparece tocando numa timeline de editor, por cima do vídeo: a música em azul, os tonais em verde-água, o nome de cada arquivo e um cursor vermelho. A forma de onda de cada clipe é a do áudio de verdade. Cada camada do plano foi renderizada sozinha, com o mesmo trecho, ganho e filtros da mixagem, e medida a cada 1/40 s, com o pico em dB levado para uma escala de 0 a 1 (−42 dB vira 0). Cada clipe acende conforme o nível real dele no instante do cursor, dá um pulinho quando o cursor passa pelo começo e apaga um pouco depois que acaba. Depois do drop, a câmera dá um empurrão leve a cada bumbo.

## Perguntas frequentes

**Preciso saber teoria musical?** Ajuda, mas os scripts medem o tom, o BPM, os acordes e o bumbo. A regra que você precisa guardar é a do relativo maior, no passo 4.

**Funciona com qualquer música?** Funciona melhor com uma frase de voz forte antes do drop e com afinação padrão. Se a música já começa com bateria, confira o drop de ouvido.

**Funciona no Mac?** Sim. Todos os scripts rodam no Mac e no Windows. Sem placa NVIDIA, a separação da voz roda na CPU e demora mais.

**E se a voz soar metálica?** Separe de um arquivo de melhor qualidade (WAV ou FLAC). Áudio de streaming comprimido piora a separação.

**Posso narrar por cima da intro?** Não é uma boa ideia, porque a voz da música é o centro da intro. Num vídeo narrado, o remix abre o vídeo e a sua fala começa depois do drop, com a música bem abaixo da voz.

**A trilha pode ter outro formato?** Pode. A skill traz variações que também funcionaram: abrir pelo instrumental abafado, desacelerar a voz para 85–90% e voltar a 100% na última frase, emendar duas partes da música sem que se perceba o corte.

## Créditos

Método, scripts, skill e Reel: **@iamjeff.ia**. Separação de voz: `audio-separator`, com o modelo MelBand RoFormer Big Beta 4 (unwa).
