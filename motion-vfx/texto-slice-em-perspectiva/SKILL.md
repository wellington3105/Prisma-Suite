---
name: texto-slice-em-perspectiva
description: Coloca um texto grande preso a uma superfície real (parede, chão, porta, fachada) na perspectiva certa, passando por trás de quem está na frente, e cortado por uma linha ("slice"). Funciona em foto e em vídeo de câmera parada, e orienta o caminho opcional de animar a cena com um gerador de vídeo (Kling). Use quando a pessoa pedir texto na parede, texto em perspectiva, letreiro na cena, efeito slice, texto cortado, ou mandar uma foto ou vídeo querendo um texto encaixado no lugar.
---

# Texto slice em perspectiva

Você é o diretor de arte e o finalizador. A pessoa dirige; você executa, mostra a prova e só então finaliza.
O efeito só convence quando o texto parece estar NO lugar: mesma perspectiva, mesma luz, atrás de quem está na frente.
Um texto colado por cima da imagem é o erro que esta skill existe para evitar.

A pessoa que recebeu esta skill pode nunca ter editado um vídeo. Explique cada pedido em uma frase: o que você precisa e por quê.
Fale simples, sem termos técnicos soltos. Quando usar um termo (prova, quadro vazio, superfície), diga o que é na primeira vez.

## O que vem na pasta
| Arquivo | Para quê |
|---|---|
| `scripts/slice_texto.py` | Faz a prova e o resultado final (foto ou vídeo). |
| `scripts/quadro.py` | Tira um quadro de um vídeo, para medir, para o quadro vazio ou para o gerador de vídeo. |
| `scripts/virada.py` | Troca o take real pelo take gerado no instante escolhido (só no caminho com Kling). |
| `guia/gravacao.md` | Como gravar para o efeito funcionar. Leia antes de orientar uma gravação. |
| `guia/direcao-visual.md` | Como decidir letra, tamanho, cor, corte e o instante do corte. |
| `guia/problemas.md` | O que fazer quando algo sai errado. Leia quando a prova ou o resultado tiver defeito. |
| `guia/kling.md` | O caminho opcional com gerador de vídeo. Leia só se a pessoa quiser animar a cena. |
| `exemplos/` | Uma cena de teste desenhada, com os arquivos de configuração prontos. |
| `assets/` | A fonte Anton (licença livre) que o script usa por padrão. |

Precisa de Python com `numpy`, `opencv-python` e `pillow`, e do `ffmpeg` para vídeo.
Se faltar algum pacote, instale com `pip install numpy opencv-python pillow`.

## Antes de começar: em que ponto a pessoa está?
Descubra com uma pergunta só, se não estiver claro:
- **Ainda vai gravar** → abra `guia/gravacao.md` e passe a lista do que gravar. É aqui que o efeito se ganha ou se perde.
- **Já tem a foto ou o vídeo** → siga os 5 passos abaixo.
- **Quer só testar** → rode o exemplo: `python scripts/slice_texto.py exemplos/config-foto.json prova` e mostre o que saiu.

Diga os limites antes de gastar o tempo dela (estão no fim deste arquivo). Câmera em movimento é o mais comum.

## O que pedir (só o que faltar)
1. **A imagem ou o vídeo** onde o texto entra. Vídeo precisa ser de câmera parada (tripé ou apoiada).
2. **O texto** (curto: 1 a 3 palavras rendem mais) e, se quiser, um rótulo pequeno acima.
3. **Onde ele mora**: qual superfície (a parede da esquerda, o chão, a porta).
4. **O mesmo enquadramento vazio**, sem a pessoa, se houver alguém na frente da superfície. É isso que faz o texto passar por trás do corpo. Sem ele, o texto só pode ficar em área livre. Se o vídeo tem um trecho em que ninguém está na frente, tire o quadro vazio dali com `scripts/quadro.py`.
5. **Uma referência de estilo**, se a pessoa tiver.

Não faça um interrogatório. Se a pessoa mandou a imagem e o texto, comece; pergunte só o que impede o próximo passo.

## Passo 1 — Ler a referência
Se veio referência, olhe e descreva em 3 a 5 linhas o que define o estilo: tipo de letra (alta e condensada, grossa, fina), cor, quanto da superfície o texto ocupa, de onde até onde vai o corte, como o texto recebe a luz.
Mostre a descrição e pergunte se é isso. Se você descreve certo, executa certo; se a descrição está errada, o resto sai errado.
Só copie a gramática (proporção, peso, gesto), nunca o conteúdo nem a marca da referência.
Sem referência, proponha: letra alta e condensada, branca, ocupando cerca de 60% da altura da superfície, corte em diagonal suave.

## Passo 2 — Achar a superfície
Olhe a imagem e ache o retângulo real onde o texto vai morar. Você precisa de:
- **`quad`**: os 4 cantos desse retângulo na imagem, em pixels, nesta ordem: topo-esquerda, topo-direita, base-direita, base-esquerda (do ponto de vista de quem lê o texto).
- **`proporcao`**: largura dividida pela altura REAL do retângulo (um trecho de parede de 4 m por 1 m tem 4.0).

Como achar os cantos: use as linhas que a própria cena dá (rodapé, encontro de parede e teto, rejuntes, bordas de janela e porta). As duas linhas horizontais do retângulo têm de apontar para o mesmo ponto de fuga dessas linhas. Abra a imagem, meça as coordenadas e confira no passo 3. Não chute sem conferir.
Deixe o retângulo inteiro dentro da superfície e longe das bordas do quadro (texto cortado pela borda é defeito).
Peça à pessoa para apontar a superfície com palavras ("a parede da direita, da janela até o fim") e, se ela souber, a medida real. Quanto mais ela descreve, menos você adivinha.

## Passo 3 — Prova antes de tudo
A prova é uma imagem de conferência: mostra a grade assentada na superfície e, ao lado, como o texto vai ficar. Serve para acertar o encaixe antes de gastar tempo no resultado.
Escreva o `config.json` ao lado dos arquivos e rode:

```bash
python scripts/slice_texto.py config.json prova
```

Sai `prova.jpg` com duas metades: à esquerda a grade em perspectiva, os 4 cantos numerados, o contorno do texto e a linha do corte; à direita, como vai ficar.
**Abra a prova e olhe.** Confira você mesmo antes de mostrar:
- As linhas da grade acompanham as linhas da cena (rodapé, rejunte, teto)? Se abrem ou fecham em relação a elas, mova os cantos e rode de novo.
- Os quadrados da grade parecem quadrados no mundo real? Se parecem esticados, corrija a `proporcao`.
- O texto cabe inteiro, sem encostar em porta, janela, luminária ou na borda do quadro?
- O texto some atrás da pessoa por inteiro (sem buraco e sem sobra)? Se não, ajuste `limiar` (maior = recorta menos).

Repita até a grade assentar. Só então mostre a prova e peça o "pode seguir". Mudar agora é de graça; depois do render, custa tempo.
Ao mostrar, diga em duas linhas o que a pessoa está vendo e o que ela deve conferir. Ela pode aprovar, pedir para polir ou corrigir.

## Passo 4 — A direção visual
Com o encaixe aprovado, decida com a pessoa (proponha, não pergunte tudo). O raciocínio completo está em `guia/direcao-visual.md`.
- **Corte** (`corte`): de onde até onde, em coordenadas da superfície de 0 a 1. Se há um gesto na cena (um braço, uma espada, um olhar), o corte segue a mesma linha desse gesto.
- **Abertura** (`abertura`): quanto as metades se afastam. 0.10 é discreto, 0.25 é dramático.
- **Cor** (`cor`, `cor_corte`): texto claro em superfície escura e o contrário. Uma cor de destaque só no brilho do corte. Pergunte se a pessoa tem uma cor de marca.
- **Tamanho** (`altura`, `margem`) e **opacidade** (`opacidade`): 0.8 deixa a textura da parede aparecer no texto.
- **Vídeo**: `t_corte` é o segundo em que o corte acontece; ponha no instante do gesto, da batida da música ou da palavra forte. `dur_corte` curto (0.25 a 0.4 s) parece golpe; longo parece deslizar.

## Passo 5 — Finalizar e conferir

```bash
python scripts/slice_texto.py config.json final
```

Sai `resultado.jpg` ou `resultado.mp4` (com o áudio original). Abra o resultado e confira antes de entregar:
- Em vídeo, tire 3 quadros (começo, no corte, fim) com `scripts/quadro.py` e olhe os três.
- Texto por trás da pessoa em todos os quadros; nada tremendo; nada cortado na borda.
Entregue com o caminho do arquivo e diga em uma linha o que foi decidido (superfície, corte, cor). Se algo ficou abaixo do que você faria, diga o que é e proponha o ajuste. Se der defeito, abra `guia/problemas.md`.

## Caminho opcional — animar a cena com um gerador de vídeo (Kling)
O texto slice é feito em código: de graça, exato e no tempo que a pessoa quiser. Um gerador de vídeo entra quando ela quer algo que o código não desenha: a parede rachando de verdade, raios, fumaça, a roupa mudando, um objeto virando outro.
Só ofereça esse caminho se ela pedir esse tipo de efeito. Antes de seguir, diga três coisas com clareza:
1. O gerador é um serviço à parte, pago por clipe. Você não gera o vídeo: você prepara o quadro e o pedido, ela gera lá e traz o arquivo.
2. O gerador não obedece relógio. Ele entrega a cena já com o efeito desde o começo. A hora da mudança é decidida depois, com `scripts/virada.py`.
3. Rosto e mãos podem sair diferentes. Sempre conferir antes de aceitar um clipe.

Abra `guia/kling.md` e siga o passo a passo de lá. A ordem é: take real → quadro inicial → pedido → clipe gerado → virada → texto slice por cima.

## Exemplo de config.json

```json
{
  "entrada": "minha_foto.jpg",
  "vazio": "mesma_foto_sem_ninguem.jpg",
  "quad": [[600, 378], [1900, 203], [1900, 610], [600, 510]],
  "proporcao": 5.9,
  "texto": "SEU TEXTO",
  "rotulo": "RÓTULO",
  "corte": {"de": [0.0, 0.62], "para": [1.0, 0.42]},
  "abertura": 0.16,
  "cor": [245, 245, 245],
  "cor_corte": [110, 200, 255],
  "opacidade": 0.82,
  "t_corte": 1.2
}
```

Todos os campos e padrões estão no cabeçalho de `scripts/slice_texto.py`.

## Regras de acabamento
- Sem sombra projetada na letra e sem contorno: quem prende o texto na parede é a perspectiva e a luz, não a sombra.
- Uma ideia por imagem: um texto grande, no máximo um rótulo pequeno.
- O texto fica na superfície livre. Se ele cruza a pessoa, tem de passar por trás (quadro vazio ou máscara).
- Nunca entregue sem ter aberto a prova e o resultado.
- Nunca diga que ficou bom sem ter olhado. Se você não conseguiu conferir alguma coisa, diga qual.

## Limites (diga antes de começar, se for o caso)
- **Câmera em movimento não funciona**: o texto ficaria parado enquanto a cena anda. Peça um take com a câmera parada.
- **Sem o quadro vazio**, não há como passar o texto por trás de alguém. Alternativa: `mascara`, uma imagem em que o branco é o que fica na frente.
- O quadro vazio precisa ter a mesma luz e o mesmo enquadramento. Se a luz mudou muito, aumente o `limiar` ou peça outro quadro vazio.
- Superfícies curvas ou muito irregulares (cortina, árvore) não dão um plano: escolha outra superfície.
- Você não ouve o vídeo. Se o corte tem de cair numa batida ou numa palavra, peça o segundo exato para a pessoa.
