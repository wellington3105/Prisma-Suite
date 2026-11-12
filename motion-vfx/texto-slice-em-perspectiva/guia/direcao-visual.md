# Direção visual: as decisões que fazem parecer profissional

A técnica põe o texto na parede. A direção decide se ele fica bonito. São poucas decisões, e cada uma tem um motivo.

## 1. A palavra
- **Curta.** Uma a três palavras. O texto ocupa a superfície inteira; frase longa vira letra pequena.
- **Uma ideia por imagem.** Um texto grande e, no máximo, um rótulo pequeno acima.
- Maiúsculas. Letra alta e condensada rende mais porque enche a altura da parede sem estourar a largura.

## 2. O tamanho (`altura`, `margem`)
- `altura` entre 0.55 e 0.70 da superfície é o ponto em que o texto parece pintado no lugar. Abaixo de 0.4 parece uma placa; acima de 0.8 encosta nas bordas.
- Deixe a `margem` respirar (0.05 a 0.10). Letra encostada no fim da parede parece erro.

## 3. A cor (`cor`, `cor_corte`, `opacidade`)
- Contraste primeiro: texto claro em parede média ou escura, texto escuro em parede clara.
- Uma cor de destaque só, e só no brilho do corte (`cor_corte`). Se a pessoa tem cor de marca, é aqui que ela entra.
- `opacidade` entre 0.75 e 0.9 deixa o rejunte e a textura aparecerem por dentro da letra. É isso que faz o olho acreditar que a tinta está na parede. Com 1.0 vira adesivo.
- Sem sombra projetada e sem contorno. Sombra é o truque de quem não acertou a perspectiva.

## 4. O corte (`corte`, `abertura`)
O corte é uma linha que atravessa o texto e separa as duas metades.
- **Siga o gesto da cena.** Um braço que aponta, um objeto que passa, a direção de um olhar: o corte tem a mesma inclinação. Sem gesto, uma diagonal suave (de 0.62 à esquerda para 0.42 à direita, por exemplo) funciona quase sempre.
- **Passe pelo meio das letras**, nunca rente ao topo ou à base: as duas metades precisam continuar legíveis.
- **Abertura**: 0.10 é elegante, 0.16 é o padrão, 0.25 é dramático. Acima disso a palavra deixa de ser lida.
- Um corte por texto. Dois cortes viram ruído.

| Clima | Linha do corte | Abertura | Duração |
|---|---|---|---|
| Golpe, impacto | diagonal marcada | 0.20 a 0.25 | 0.20 a 0.30 s |
| Tecnologia, precisão | quase horizontal | 0.10 a 0.14 | 0.30 a 0.40 s |
| Calmo, editorial | diagonal bem suave | 0.08 a 0.12 | 0.50 a 0.80 s |

## 5. O instante (só em vídeo: `t_corte`, `dur_corte`)
O corte tem de acontecer por algum motivo. Escolha um, nesta ordem:
1. **O gesto**: o quadro em que o braço chega ao fim do movimento.
2. **A palavra forte** da fala.
3. **A batida** da música.
O Claude não ouve o vídeo: para 2 e 3, diga a ele o segundo exato.
Deixe o texto inteiro aparecer por pelo menos meio segundo antes do corte. Quem assiste precisa ler a palavra antes de vê-la partir.

## 6. O que estraga
- Texto por cima do rosto ou do corpo. Ele mora na parede: passa por trás.
- Texto cortado pela borda do quadro.
- Muita coisa junto: texto, rótulo, três cores, dois cortes. Tire até sobrar uma ideia.
- Aceitar a primeira prova. A segunda quase sempre é melhor, e mudar na prova não custa nada.

## Como pedir ajustes ao Claude
Diga o que você vê, não o número. "O texto está subindo mais que o rodapé" resolve mais rápido que "muda o canto 2".
Um ajuste por vez. Muitos pedidos juntos fazem a cena perder a consistência.
