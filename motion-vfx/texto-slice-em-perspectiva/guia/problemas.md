# Quando algo sai errado

Ache o sintoma, leia a causa, aplique o conserto. Um ajuste por vez, e uma prova nova a cada ajuste.

## Na prova
| O que você vê | Causa | Conserto |
|---|---|---|
| A grade "abre" ou "fecha" em relação ao rodapé ou ao teto | Os cantos não seguem a perspectiva da cena | Mova os cantos do `quad` para cima das linhas reais (rodapé, rejunte, encontro com o teto) |
| Os quadrados da grade parecem esticados ou achatados | `proporcao` errada | Largura real dividida pela altura real do trecho. Parede de 3 m por 1 m = 3.0 |
| O texto ficou pequeno | Trecho estreito, texto longo, ou `altura` baixa | Menos palavras, superfície maior, `altura` até 0.70 |
| O texto encosta na borda do quadro | O retângulo vai até a borda da imagem | Encolha o `quad` ou aumente a `margem` |
| O texto está de cabeça para baixo ou espelhado | Ordem dos cantos trocada | A ordem é topo-esquerda, topo-direita, base-direita, base-esquerda, do ponto de vista de quem lê |

## O texto e a pessoa
| O que você vê | Causa | Conserto |
|---|---|---|
| O texto passa por cima da pessoa | Não há quadro vazio, ou a diferença é pequena | Informe `vazio`; se já informou, diminua o `limiar` (0.06) |
| Buracos no texto onde não há ninguém | Luz diferente entre os dois takes, ou sombra da pessoa na parede | Aumente o `limiar` (0.14 a 0.20); se não resolver, grave outro quadro vazio |
| Sobra texto dentro do corpo | Roupa da cor da parede | Diminua o `limiar`; se não resolver, use uma `mascara` |
| Contorno claro em volta da pessoa | Recorte largo demais | Aumente um pouco o `limiar` |
| O quadro vazio tem tamanho diferente | Foi tirado de outro arquivo | O script ajusta o tamanho, mas o enquadramento tem de ser o mesmo. Tire o vazio do mesmo vídeo com `scripts/quadro.py` |

## No vídeo
| O que você vê | Causa | Conserto |
|---|---|---|
| O texto "escorrega" na parede | A câmera se mexeu | Não tem ajuste: grave de novo com a câmera travada |
| O texto pisca | Exposição automática mudando a luz | Aumente o `limiar`; na próxima gravação, trave a exposição |
| O corte acontece na hora errada | `t_corte` chutado | Tire quadros com `scripts/quadro.py` em volta do gesto e ache o segundo exato |
| O corte parece lento | `dur_corte` longo | 0.25 a 0.35 s para golpe |
| O vídeo saiu sem som | O arquivo original não tinha áudio, ou o ffmpeg falhou | Confira se a entrada tem som; rode de novo e leia a mensagem de erro |

## Na instalação
| Mensagem | Conserto |
|---|---|
| `No module named cv2` (ou `numpy`, `PIL`) | `pip install numpy opencv-python pillow` |
| `ffmpeg` não encontrado | Instale o ffmpeg e deixe-o no caminho do sistema. Para foto ele não é necessário |
| `Fonte não encontrada` | Informe `"fonte"` no config com o caminho de um arquivo .ttf ou .otf |
| `Não consegui abrir` | Caminho errado. Os caminhos do config são relativos à pasta do próprio config |

## Se nada disso resolver
Mande para o Claude a prova, o `config.json` e uma frase dizendo o que você vê de errado. Com a imagem na frente ele acha mais rápido do que com a descrição.
