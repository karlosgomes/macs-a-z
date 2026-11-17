# MACS A...Z

Livro de apresentações de MACS (10.º ano, currículo português), feito como o Matemática A...Z: uma só apresentação Reveal.js que abre com o índice e se divide em capítulos. Texto sempre em português europeu.

## Estrutura
- `index.html` + `libs/`: **gerados, não editar aqui**. Saem de `fontes/` com `fontes/_ferramentas/publicar_site.sh`.
- `fontes/`: fontes Quarto e Python. Tudo está explicado em `fontes/README.md`:
  - índice (1.º diapositivo) e capítulos (`index.qmd`);
  - geradores das tabelas de síntese (`_fonte_*`);
  - tema (`estilo.scss`);
  - barra do weblog (`_ferramentas/site/`).
- `img/logo.png`: logótipo.

## Organização (2026-11-15)
- **Navegação:** índice (1.º diapositivo) → Capítulo 1 «Divisão Justa» → para cada método (1.1 Licitações secretas, 1.2 Ajuste na Partilha, 1.3 Marcadores), um **Resumo** (abertura e ↓ diapositivos) e os **Problemas** (lista e ↓ problemas) → Síntese.
  - → passa de secção em secção e ↓ desce dentro de cada secção (`navigation-mode: vertical`).
  - Links de regresso «↩ índice» e «↩ problemas», postos por JavaScript em `navegacao.html`.
- **Ids:** `#/indice`, `#/lic`, `#/lic-problemas`, `#/lic-p1`…, `#/aw…`, `#/mk…`, `#/sintese`.
- **Formato:** 1600×900. A faixa escura do título fica fora do `.reveal` e só aparece no índice (classe `na-capa`), como no Matemática A...Z. Sem rodapé nem número do diapositivo; botões do canto inferior esquerdo e ícones da barra iguais aos do Matemática A...Z.
- **Multiplex:** não é usado, por decisão do utilizador. As apresentações são para projetar.
- **Tabela de síntese sempre à esquerda**, com as linhas do passo em curso destacadas, e cálculos à direita, em todos os métodos.
- **Licitações secretas (desde 2026-11-16):** ponto de vista do jogador, como no Tannenbaum: alocação provisória = parte justa − valor dos bens recebidos; valores sempre com sinal, [+]{.pos} verde = recebe, [−]{.neg} vermelho = paga; o excedente calcula-se do ponto de vista do **fundo** (os sinais trocam: quem tem − entra com +, quem tem + entra com −; ex.: «Fundo: 100 + 70 − 80 = 90»); a parte do excedente soma-se (+30) e a alocação final é provisória + excedente. Nos textos finais junta-se «(paga)»/«(recebe)». Nas contas ao lado das tabelas, o resultado colorido vai dentro do LaTeX: `\textcolor{#16A34A}{\mathbf{+80}}` / `\textcolor{#DC2626}{\mathbf{-100}}` (o MathJax não aceita `\textcolor[HTML]{…}`); nas tabelas, texto com `.pos`/`.neg`. A app Divisão Justa faz o mesmo. (O exame só pede «paga/recebe»; os critérios do IAVE não usam sinais.)
- **Caixa do fundo:** os cálculos do fundo comum vão numa `::: {.cofre}` (estilo em `estilo.scss`: título «Fundo comum (cofre)» numa etiqueta vermelha ao centro do rebordo azul, como uma tcolorbox), com a conta partida em duas linhas se for comprida.
- **Ajuste na Partilha:** $x$ é a fração que **passa** para o outro jogador.
- **Capítulo novo** (por exemplo, partilha no caso contínuo, eleições, finanças):
  - um corpo `_corpo_…qmd` com `# … {#id .capitulo data-rotulo="2.1 · Resumo"}` e `# … · Problemas {#id-problemas .lista-problemas}`;
  - um bloco no índice de `index.qmd`;
  - o `{{< include >}}`.

## Publicação
- **Repositório:** https://github.com/karlosgomes/macs-a-z (ramo `main`), com GitHub Pages a partir da raiz. Endereço: https://karlosgomes.github.io/macs-a-z/ (links por diapositivo: `#/lic-p3`).
- **Publicar** = `publicar_site.sh` + `git commit` + `git push`. Se o `estilo.scss` mudou, o tema gerado muda de nome (`libs/revealjs/dist/theme/quarto-<hash>.css`): fazer `git add -A libs`, senão o site fica sem tema. **Perguntar ao utilizador antes do push.**
- **Menu:** o item «MACS A...Z» está nos menus do weblog, do Matemática A...Z e das Apps de Matemática. Se o menu do weblog mudar, atualizar à mão `fontes/_ferramentas/site/barra.html`.
