# Revisão de interface — 19/10/2026

Referência solicitada: [frontend-design, Anthropic](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md).

## Direção antes de implementar

Objetivo: encontrar um ponto, registrar a entrega e recuperar o QR com poucos passos. O perfil precisa permitir consultar e editar a conta sem uma longa rolagem.

Tokens mantidos da marca aprovada: Floresta #153F35, Verde rede #28735A, Lima #CBEA73, Papel #F4F3EA, Grafite #23352D, Névoa #DCE8DE. Manrope nos títulos e DM Sans nos controles e textos. Títulos do app entre 22–28 px; corpo entre 13–15 px. Espaçamento base 4/8/12/16/24. A cor lima identifica seleção e progresso; não vira fundo de cada card.

Layout alinhado à esquerda, com ações curtas e superfícies agrupadas por tarefa.

```text
Mobile: [marca             alertas/menu]
        [tarefa atual              ação]
        [conteúdo compacto]
        [Início | Pontos | + | Descartes | Conta]

Perfil: [foto | nome / email    editar]
        [registros | concluídos | materiais]
        [nível + pontos + progresso compacto]
        [conquistas]
        [últimos registros]
        [configurações / segurança / ajuda]

Rastreio: [voltar / código]
          [QR e copiar]
          [estado / materiais / eventos]
```

Crítica do plano: repetir blocos de slogans, cards iguais, subtítulos em caixa alta e círculos enormes de gamificação manteria os problemas enviados pelo usuário. A revisão troca essas escolhas por dados, rótulos de ação e alinhamento compacto. A ilustração do hero aprovado permanece; o percurso decorativo isolado passa a integrar uma sequência interativa com três etapas reais. A animação responde à escolha da etapa, à expansão de um registro e à confirmação de cópia. Sem loops permanentes ou animação de entrada em toda seção.

Não exibir avisos sobre materiais fora do catálogo. Manter as restrições reais da operação nos dados e nas validações existentes. Preservar funções de conta, histórico, parceiros e administração.

Backup anterior à revisão: `tmp/ecoverse-before-ux-review.zip`.


## Verificação durante a revisão

- Perfil conferido no navegador em 390 px e 320 px: indicadores na mesma linha, nível compacto e sem rolagem horizontal da página.
- Rastreio móvel com o QR antes do status e do histórico; ampliação testada com retorno de foco ao fechar por Esc.
- Navegação com quatro áreas fixas; menu fechado fora da ordem de foco. Menu testado com abertura, fechamento e acesso à página pública.
- Sequência da home testada por clique e setas do teclado. O texto e a ação acompanham a etapa selecionada.
- Formulário testado com óleo em litros e foco no título da próxima etapa.

Os dados usados são fictícios. O catálogo e as regras do backend não foram ampliados nesta revisão. Botão Google desativado e métrica fixa de 890 parceiros foram retirados: eram preenchimentos de interface, sem função ou dado real por trás.

- Registro completo pelo navegador com 1,25 L, ponto fictício, revisão, geração de QR e abertura do rastreio: PASS. O registro de teste foi cancelado pela interface; o histórico foi preservado e não houve crédito de participação.
- Os desenhos 06–09 do pacote enviado foram inlinados para responder à seleção e ao foco. O grafismo isolado do percurso saiu da home; a conexão agora faz parte da sequência interativa de entrega.
- Foco e posição de rolagem ajustados na mudança de etapa, sem deixar o título sob a barra fixa.
- Indicadores de perfil usam estado de carregamento em vez de apresentar zero como resultado antes da resposta.

A revisão não alterou catálogo, autenticação, regras de pontos, serviços ou volumes. O cancelamento pendente permanece acessível no detalhe do descarte, e as funções operacionais continuam usando as permissões do backend.


## Encerramento da verificação

- Build final de produção: PASS, 32 rotas/páginas compiladas e tipos verificados.
- Nove verificações HTTP contra a versão compilada: PASS, incluindo login e páginas de participante, ponto e operador, arquivos JS/CSS e código VGO histórico.
- Versão servida pelo entrypoint standalone, com public e static copiados para o diretório de execução.
- Rastreio em viewport 320: largura útil 305 px (barra de rolagem do ambiente); página com 305 px, sem overflow. QR em y=149,9 antes do status em y=342,5.
- Rastreio em viewport 1200: largura útil 1185 px; página com 1185 px. QR na coluna lateral (x=828,4), conteúdo à esquerda (x=66,4).
- Capturas reais: `output/review/perfil-mobile.png`, `output/review/rastreio-mobile.png`, `output/review/home-processo.png`.
- Tamanho temporário do navegador restaurado. A aba ficou no perfil.

Câmera, geolocalização, SMTP, 2FA real e produção continuam fora da validação desta revisão. Não houve alteração de dados de usuários reais, backend, volumes ou stacks existentes.


## Atualização de 20/10/2026

A barra do participante agora tem cinco destinos, com + central para registrar descarte e destaque animado. O tema inicial é claro e continua configurável. A equipe atual usa um acordeão de fotos compartilhado pelas duas páginas públicas. Consulte [equipe e navegação](equipe-navegacao.md) para implementação e validação.
