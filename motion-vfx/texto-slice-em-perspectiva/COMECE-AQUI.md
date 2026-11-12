# Comece aqui

Você recebeu a skill **Texto slice em perspectiva**: o método para colocar um texto grande preso a uma parede, a um chão ou a uma porta, na perspectiva certa, passando por trás de você e cortado por uma linha.

Uma skill é uma pasta de instruções e ferramentas que o Claude lê quando o assunto aparece. Você não programa nada. Você dirige; o Claude executa.

## O que tem dentro
| Arquivo | O que é |
|---|---|
| `SKILL.md` | O roteiro que o Claude segue com você, em 5 passos. |
| `guia/gravacao.md` | Como gravar para o efeito funcionar. **Leia este antes de gravar.** |
| `guia/direcao-visual.md` | Como escolher letra, tamanho, cor, corte e o instante do corte. |
| `guia/problemas.md` | Tabela de defeitos comuns e o conserto de cada um. |
| `guia/kling.md` | Opcional: como animar a cena com um gerador de vídeo e juntar tudo. |
| `scripts/` | As três ferramentas que o Claude roda para você. |
| `exemplos/` | Uma cena de teste pronta, para ver funcionando antes de usar o seu material. |

## Como instalar
**No aplicativo do Claude:** Configurações → Capacidades → Skills → enviar o arquivo `.zip` desta skill. É preciso estar com a execução de código e a criação de arquivos ligadas.
**No Claude Code:** descompacte a pasta `texto-slice-em-perspectiva` dentro de `.claude/skills/` do seu projeto (ou de `~/.claude/skills/`, para valer em todos).
Os nomes dos menus mudam de vez em quando. Se não achar, pergunte ao próprio Claude: "como instalo uma skill?".

## O caminho em 5 passos
1. **A referência.** Mostre ao Claude um exemplo do estilo que você quer e peça para ele descrever. Se ele descreve certo, ele executa certo.
2. **O lugar.** Antes de gravar, escolha onde o texto vai morar: parede, chão ou porta.
3. **A gravação.** Câmera parada. Grave a cena com você e, sem mexer na câmera, grave o mesmo espaço vazio.
4. **A prova.** Envie os arquivos e aponte a superfície. O Claude devolve uma imagem com a grade na perspectiva. Você aprova, pede para polir ou corrige.
5. **A direção visual.** Corte, cor, tamanho e o instante. Depois ele finaliza.

## O primeiro pedido
Para testar sem gravar nada:
> Rode o exemplo da skill texto slice e me mostre a prova.

Com o seu material:
> Quero o texto "ABRE HOJE" nesta parede da direita. Aqui está o vídeo e o mesmo quadro vazio.

Se ainda vai gravar:
> Vou gravar para usar a skill texto slice. Me diga exatamente o que eu preciso gravar.

## O que ela faz e o que ela não faz
**Faz:** foto e vídeo de câmera parada; texto atrás de quem está na frente; corte animado no segundo que você escolher; mantém o som original.
**Não faz:** vídeo com a câmera em movimento; superfície curva (cortina, árvore); gerar vídeo sozinha (para isso existe o caminho opcional do `guia/kling.md`, com um serviço à parte e pago).

## Três conselhos de quem já errou
- Grave o quadro vazio sempre. Custa cinco segundos e é ele que faz o texto passar atrás do corpo.
- Não aceite a primeira prova por educação. Ajustar na prova é de graça.
- Um pedido por vez. Muitos ajustes juntos fazem a cena perder a consistência.

A IA faz. Quem dirige é você.
