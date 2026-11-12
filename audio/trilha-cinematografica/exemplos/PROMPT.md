# Prompt para fazer a versão cinematográfica de uma música

Cole o bloco abaixo no Claude Code e troque tudo o que está entre `[colchetes]`. Antes, instale a skill `trilha-cinematografica` (pasta `3-skill-trilha-cinematografica`) e o que está em "O que você precisa", no `LEIA-ME.md`.

```text
Use a skill trilha-cinematografica. Quero a versão cinematográfica de uma música, montada por script, no método do projeto de exemplo em [caminho da pasta 2-projeto].

MÚSICA: [caminho do arquivo, de preferência WAV ou FLAC, ex.: C:/trilhas/minha-musica/musica.wav]
MOMENTO: [a frase de voz que abre e o drop, ex.: "do 'Baby, we took a trip' até a batida do verso", ou "você escolhe a melhor frase antes de um drop"]
USO: [ex.: abertura de um Reel de 30 s, vertical; ou abertura de um vídeo de YouTube]
TAMANHO DA INTRO: [ex.: voz aos ~13 s e drop aos ~22 s; ou "igual ao exemplo, drop aos ~39 s"]
REFERÊNCIA (opcional): [caminho de um remix ou de uma demo de que eu gosto, ou "sem referência"]
MEUS SONS: [caminho da pasta com os sons, ex.: C:/sons/tonais/, com os tons no nome ou em subpastas]
PIANO PARA O PING: [pasta com notas soltas de piano, ou "use um som de golpe tonal da minha pasta"]
PASTA DE TRABALHO: [ex.: C:/trilhas/minha-musica/]
NARRAÇÃO DEPOIS DO DROP: [sim ou não; se sim, o arquivo da narração]

DIREÇÃO
- A voz do cantor entra quase sozinha, com eco de sala de concerto (~40%). Ela é a prioridade; os efeitos tonais entram como complemento e não atrapalham a voz cantando.
- Tudo no tom da música: meça tom, BPM e afinação, confirme o tom antes de escolher os sons e respeite a regra do relativo maior.
- Golpe tonal no 1º quadro; drones entrando devagar; cello em pergunta (sozinho) e resposta (no respiro da voz); acordes de piano fatiados, um por compasso, no 1º tempo e numa palavra forte; dois risers com o pico exatamente no drop.
- No drop, tudo corta seco e a música inteira entra no bumbo, sem respiro antes.
- Menos é mais: cada camada precisa ter função.

COMO FAZER
1. Leia o README.md e o plano-exemplo.json do projeto de exemplo e siga o mesmo método e os mesmos scripts.
2. Meça a música (medir_musica.py) e me diga tom, relativo, BPM, afinação e o segundo do bumbo do drop. Se a afinação passar de ±20 cents, me avise antes de seguir.
3. Separe a voz da própria música com o separar_voz.py (MelBand RoFormer Big Beta 4). Não use acapella da internet.
4. Liste os meus sons por papel (golpe, drones, cello, acordes, risers, impacto) no tom certo. Com referência, ranqueie os candidatos com o medicao/match.py. Se faltar algum papel, diga qual e proponha o mais próximo.
5. Tire as palavras e os respiros da voz (medicao/tr.py) e a harmonia do trecho (medicao/chromat.py). Antes de mixar, me mostre a tabela de camadas: tempo, camada, arquivo, nível.
6. Escreva o plano.json, prepare a voz (prep_voz.py) e o ping (prep_ping.py), rode o stems.py e o mix_voz_na_frente.py.
7. Confira com o conferir.py (espectrograma e, com referência, o vídeo A/B) e com o medicao/bands.py. Meça antes de culpar qualquer efeito. Corrija e repita até ficar bom.
8. Entregue na pasta de trabalho: o WAV final em −14 LUFS, as camadas separadas, o plano.json e um resumo com a música, o tom, o BPM e o que foi trocado em relação ao exemplo.

PRONTO QUANDO: [ex.: eu ouvir a versão final e aprovar, com as camadas separadas na pasta]
```

## O pedido original do Reel

O pedido foi recriar uma intro cinematográfica do primeiro minuto de "Laugh Now Cry Later", "com o impacto, que é o hype", para um Reel mostrando a diferença entre um som cinematográfico e um som que só tem efeito sonoro. Depois de ouvir as primeiras versões, o criador resumiu a ideia em duas mensagens:

> O cantor entra praticamente a capela, e os tonal sounds ficam evidentes em volta. A gente não atrapalha a voz dele cantando, só deixa melhor.
>
> Tem que ter um eco, e a voz dele tem que ser prioridade nessa parte; os tonal sounds entram como complemento.

Os retornos que mudaram o resultado foram curtos e apontavam o problema: "muito eco na voz" (o reverb desceu de 50% para 20%), "a capela demais" (voltou para ~40%, com a réplica da sala de concerto) e "a voz vai ficando perdida" aos 17 s (voz separada com um modelo melhor e prioridade dinâmica da voz).

## Dicas para o seu pedido sair melhor

- Mande a música no melhor arquivo que tiver. Áudio de streaming comprimido piora a separação da voz.
- Diga o momento que você quer. Se não souber, peça que ele proponha três frases antes de um drop e escolha de ouvido.
- Uma referência ajuda muito: com ela, os tempos, os níveis e os filtros saem de medida.
- Na revisão, aponte o segundo e o que incomoda ("aos 17 s a voz some", "o eco está alto demais"). Dá para corrigir só aquilo.
- Peça também a versão "som normal" (plano-so-efeitos-comuns.json) se for mostrar o antes e depois num vídeo.
