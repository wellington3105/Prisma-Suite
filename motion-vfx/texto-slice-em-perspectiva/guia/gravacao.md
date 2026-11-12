# Como gravar para o texto encaixar

O efeito é decidido na gravação. Com o material certo, o resto são minutos. Com o material errado, nenhum ajuste salva.

## A lista (grave nesta ordem)
1. **Escolha onde o texto vai morar antes de ligar a câmera.** Uma parede, o chão, uma porta, um muro, uma fachada. Tem de ser plano e ter um trecho livre grande. Olhe para ele e imagine a palavra ali.
2. **Trave a câmera.** Tripé, ou apoiada em algo firme. Ela não pode sair do lugar entre um take e outro, nem um centímetro.
3. **Trave a imagem.** Se a câmera ou o celular permitir, fixe foco e exposição (no celular: segure o dedo na tela até travar). Assim a luz não muda sozinha no meio do take.
4. **Take 1: a cena com você.** Faça a ação do jeito que quiser, naturalmente. Pode passar na frente da superfície: é isso que dá o efeito do texto por trás do corpo.
5. **Take 2: o mesmo quadro, vazio.** Saia de cena e grave 3 a 5 segundos do espaço sem ninguém, sem mexer na câmera. Pode ser no mesmo arquivo: basta sair do quadro antes de parar de gravar.

## Por que cada coisa
| O que | Por quê |
|---|---|
| Superfície plana | O texto é desenhado num retângulo e inclinado na perspectiva. Cortina, árvore e parede curva não são um retângulo. |
| Câmera parada | O texto fica fixo num ponto da imagem. Se a câmera anda, a parede anda e o texto fica para trás. |
| Quadro vazio | Comparando o quadro com você e o quadro vazio, dá para saber exatamente onde está o seu corpo. O texto é apagado ali, e parece estar atrás de você. |
| Mesma luz nos dois takes | A comparação é por diferença. Se uma nuvem passou ou uma luz acendeu, a parede inteira "muda" e o recorte falha. |
| Trecho livre grande | Texto apertado entre uma janela e uma luminária fica pequeno. O texto precisa de espaço para ser grande. |

## Escolhendo a superfície
- **Parede lateral, vista em diagonal**, é a que mais impressiona: a perspectiva fica evidente e o texto "foge" para o fundo.
- **Parede de frente** é a mais fácil de acertar, mas parece menos 3D.
- **Chão** funciona muito bem visto de cima ou com a câmera baixa.
- Prefira superfície com linhas visíveis (rodapé, rejunte, tijolo, encontro com o teto). São elas que mostram a perspectiva para o Claude.
- Superfície lisa e de uma cor só deixa o texto mais legível. Muita informação (grafite, quadros, plantas) briga com a letra.
- Texto claro pede parede média ou escura. Parede branca estourada pede texto escuro.

## Enquadramento
- Deixe a superfície inteira dentro do quadro, com folga nas bordas.
- Deixe um trecho da superfície **sem você na frente em nenhum momento**: é onde a maior parte da palavra vai ser lida.
- Se vai postar na vertical, grave pensando no recorte: o texto tem de caber no miolo.

## Se você já gravou e não tem o quadro vazio
- Procure no próprio vídeo um instante em que ninguém está na frente da superfície. O Claude tira esse quadro com `scripts/quadro.py`.
- Se você passa pela cena, dois quadros em que você está em lados diferentes podem ser juntados num vazio. Peça isso ao Claude.
- Sem nenhum dos dois, o texto ainda funciona, mas só na parte da superfície onde você nunca passa.

## Erros que mais acontecem
- Encostar na câmera entre o take 1 e o take 2.
- Gravar o vazio com outra luz (porta aberta, lâmpada acesa depois).
- Usar roupa da mesma cor da parede: o recorte não sabe onde você termina.
- Sombra forte do corpo na parede: a sombra conta como "diferença" e apaga um pedaço do texto. Afaste-se da parede ou use luz mais difusa.
