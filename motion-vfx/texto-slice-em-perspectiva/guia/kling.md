# Caminho opcional: animar a cena com um gerador de vídeo (Kling)

Este guia é para quando você quer mais do que o texto: a parede rachando, raios, fumaça, a roupa mudando, um objeto virando outro. Isso o código não desenha. Um gerador de vídeo desenha.
O exemplo aqui é o Kling, mas o método serve para qualquer gerador que aceite um quadro inicial.

Você não precisa disto para o texto slice. O texto continua sendo feito em código, por cima de tudo, no final.

## O que está acontecendo, em linguagem simples
Um gerador de vídeo recebe **uma imagem** (o primeiro quadro) e **um pedido escrito**, e devolve alguns segundos de vídeo continuando aquela imagem. Ele não edita o seu vídeo: ele inventa um vídeo novo que começa igual ao seu quadro.

Três coisas decorrem disso, e o método inteiro existe por causa delas:

| O gerador faz assim | Então a gente faz assim |
|---|---|
| Não obedece relógio. Você pede "aos 2 segundos a parede racha" e ela já racha no primeiro quadro. | O gerador entrega o **estado final** (a cena já com o efeito). A hora da mudança é decidida depois, na **virada**. |
| Inventa o que não está na imagem. Rosto pequeno, mão e texto saem diferentes. | O quadro inicial sai do **seu take real**, com o rosto grande o bastante. Sempre conferir rosto e mãos antes de aceitar. |
| Pode mexer a câmera e o fundo por conta própria. | O pedido diz "câmera parada" e descreve só o que muda. O take real é de câmera parada, então dá para comparar. |

## O que você precisa, e por quê
- **O take real, de câmera parada.** É a base. O clipe gerado tem de bater com ele no instante da troca, e isso só acontece se nada mais se mexeu.
- **O instante da virada.** O segundo em que o efeito começa: o fim de um gesto, uma batida, uma palavra.
- **Uma conta num gerador de vídeo.** É um serviço à parte e **pago por clipe**. Preço e limites mudam: confira no site antes de começar. Comece sempre na resolução mais barata para testar o pedido; só gere em alta quando o teste estiver certo.
- **Se o efeito troca a sua roupa ou põe um objeto na sua mão:** imagens de referência do que entra (a roupa sozinha, o objeto sozinho, o seu rosto de perto). Uma imagem para cada coisa. Rosto pequeno numa imagem cheia de coisas perde a semelhança.

## Passo a passo
### 1. Tirar o quadro inicial
O clipe gerado começa no instante da virada (ou um pouco antes).

```bash
python scripts/quadro.py meu_take.mp4 2.4 quadro_inicial.png
```

O script mostra o tamanho e a proporção do quadro. Se o gerador pedir outra proporção, avise o Claude: ele ajusta sem cortar você.

### 2. Escrever o pedido
O Claude escreve com você, a partir do modelo em `exemplos/pedido-kling.txt`. A estrutura que funciona tem seis partes, nesta ordem:
1. **O que fica igual**: a pessoa, o rosto, a roupa, o lugar, o enquadramento.
2. **A ação**: o que acontece, em uma frase.
3. **A reação do cenário**: o que a ação provoca em volta (poeira que sobe, luz que muda, chão que marca). É isso que tira a cara de efeito colado.
4. **A marca que fica**: o que continua na cena depois (a rachadura aberta, a fumaça baixa). Sem isso o efeito some e a cena volta ao normal.
5. **A câmera**: parada, no tripé, sem zoom.
6. **O que não pode**: sem texto, sem mudar o rosto, sem novos objetos.

Regras do pedido:
- Em inglês rende mais na maioria dos geradores. O Claude traduz.
- Descreva **só o que aparece no quadro**. Se os pés não aparecem, não fale dos pés: o gerador tenta mostrar e muda o enquadramento.
- Um efeito por clipe. Dois pedidos juntos saem os dois pela metade.
- Diga a cor exata da luz e de onde ela vem. "Luz lilás que nasce da rachadura" é melhor que "efeito de energia".

### 3. Gerar
Você envia o quadro inicial e o pedido no gerador e baixa o clipe. O Claude não faz essa parte: ele não tem acesso à sua conta.
Gere curto (5 segundos costuma bastar) e barato primeiro.

### 4. Conferir o clipe antes de usar
Mande o clipe para o Claude e peça para ele tirar 4 quadros e olhar. Vocês conferem juntos:
- O rosto ainda é o seu? As mãos têm cinco dedos?
- A câmera ficou parada? As bordas do quadro estão no mesmo lugar do take real?
- O efeito tem reação e deixa marca, ou parece colado?
- Tem algum trecho parado no começo ou no fim? Anote para cortar.

Se algo falhou, mude **uma coisa** no pedido e gere de novo. Mudar tudo de uma vez não ensina o que resolveu.

### 5. A virada
Aqui o take real vira o take gerado no instante que você escolheu.

```bash
python scripts/virada.py meu_take.mp4 clipe_gerado.mp4 --t 2.4
```

- `--t` é o segundo da virada. `--dur` é quanto ela dura (0.2 s parece golpe; 0.6 s parece magia).
- `--modo linha` faz uma linha atravessar a tela revelando o take gerado. Use a mesma inclinação do corte do texto (`--de` e `--para`), e os dois efeitos viram um só gesto.
- Se o quadro inicial saiu de um ponto antes da virada, informe com `--inicio`.

O resultado tem o som do take real e termina onde o clipe gerado termina.

### 6. O texto slice por cima
Com o `virada.mp4` pronto, volte aos 5 passos da skill usando esse vídeo como entrada. Ponha o `t_corte` do texto no mesmo instante da virada, ou logo depois.
Atenção ao quadro vazio: se o gerador mudou o fundo (rachou a parede, mudou a luz), o quadro vazio antigo não serve mais para o trecho gerado. Duas saídas:
- ponha o texto numa parte da superfície onde você não passa depois da virada; ou
- peça ao gerador um segundo clipe, igual, sem a pessoa, e tire o quadro vazio dele.

## Quando o efeito troca a roupa ou cria um objeto
1. Faça primeiro a **imagem perfeita** num gerador de imagem: você, de corpo inteiro, já com a roupa nova, no mesmo lugar e na mesma pose do quadro inicial. É mais barato acertar numa imagem do que num vídeo.
2. Use essa imagem como quadro **final** (se o gerador aceitar primeiro e último quadro) ou como referência.
3. A troca instantânea, no tempo certo, é feita na virada. Não peça ao gerador para "transformar aos poucos": ele veste a roupa nova desde o primeiro quadro.

## Erros que mais acontecem
| O que aconteceu | Por quê | O que fazer |
|---|---|---|
| O efeito já está no primeiro quadro | O gerador não segue tempo | É o esperado. A hora é decidida na virada. |
| A câmera andou ou deu zoom | Faltou travar no pedido | "Locked-off camera on a tripod, no camera movement, no zoom" |
| O rosto virou outra pessoa | Rosto pequeno no quadro ou pedido falando do rosto | Quadro inicial mais fechado; no pedido, só "keep his face exactly as in the image" |
| O fundo inteiro mudou de cor | O pedido descreveu um clima, não um efeito | Diga de onde a luz nasce e até onde vai |
| O efeito aparece e some | Faltou a marca que fica | Descreva o que continua na cena depois |
| A troca aparece na virada | Os dois takes não batem | Confira se o quadro inicial é do mesmo instante; use `--modo linha` para esconder a emenda no movimento |
| Um ou dois segundos parados | O gerador "pensa" antes de agir | Corte esse trecho ou comece a virada depois dele |

## O que é honesto dizer
- Custa dinheiro e nem todo clipe presta. Conte com duas ou três tentativas por efeito.
- O Claude prepara, confere e monta. Quem gera e quem decide é você.
- Se o efeito pode ser feito em código (o texto, uma linha de luz, um corte), faça em código: é de graça, exato e repetível.
