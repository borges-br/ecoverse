# Do VestGO ao EcoVerse: leitura do produto e transição

Data: 19/10/2026. Escopo desta entrega: diagnóstico arquitetural e de fluxos, estratégia e identidade de marca. A aplicação, os contratos da API, o schema, os dados e a infraestrutura não foram modificados. A leitura de código não substitui testes em execução.

## 1. O que o produto atual faz

O VestGO organiza o ciclo de doação. A pessoa registra itens, escolhe um ponto e recebe um código/QR. O ponto confirma a chegada. Uma ONG parceira participa da retirada e do recebimento, e a operação pode consolidar doações em lotes. O doador acompanha os estados. O administrador governa a publicação de perfis operacionais e revisões de informações públicas.

O código suporta mais categorias do que roupas: `CLOTHING`, `SHOES`, `ACCESSORIES`, `BAGS`, `TOYS`, `FOOD`, `OTHER`. Todas continuam inseridas no domínio de doação, com estados de conservação `EXCELLENT` e `GOOD`.

### Papéis e permissões

| Papel técnico | Experiência atual | Papel de produto proposto |
| --- | --- | --- |
| `DONOR` | Registra doações, escolhe ponto, rastreia, recebe pontos e conquistas | Pessoa que descarta; publicamente, “Pessoa” ou simplesmente “Você” |
| `COLLECTION_POINT` | Recebe materiais, gerencia fila, parcerias, retiradas e lotes | Ponto de coleta |
| `NGO` | Aprova parceria, solicita retirada, recebe e distribui doações | Operador parceiro, com atribuições ainda a definir |
| `ADMIN` | Aprova perfis, revisões e gerencia campanhas | Administrador da rede |

O cadastro público restringe os papéis permitidos; `ADMIN` não é criado por esse fluxo. Não se recomenda renomear enums e permissões por substituição global. Primeiro é preciso decidir se coleta, transporte e destinação serão papéis separados, capacidades de uma mesma organização ou entidades relacionadas.

### Jornada observada

1. Cadastro/login por Auth.js no frontend e JWT/sessões no backend. Existem fluxos de verificação de e-mail, recuperação de senha, segundo fator TOTP, revogação de sessões e encerramento com anonimização.
2. Ponto e ONG preenchem perfil operacional: identificação, endereço, geolocalização, horários, regras, categorias aceitas, acessibilidade e mídia. Há estados `DRAFT`, `PENDING`, `ACTIVE`, `VERIFIED` e retenção de alterações públicas críticas para revisão.
3. O ponto solicita parceria. A ONG aceita ou rejeita. A parceria ativa é pré-condição para registrar doações destinadas ao ponto.
4. A pessoa usa um wizard de quatro etapas: itens; como levar; ponto de coleta; revisão. O frontend guarda rascunhos e integra a seleção ao mapa.
5. A API cria o registro, itens, volumes, código e primeiro evento. A criação não credita pontos reais.
6. O ponto usa o código/QR para localizar o registro e confirmar recebimento, conforme as permissões do fluxo.
7. A ONG solicita retirada com data/janela e o ponto responde. Essa direção foi conferida no código: não é uma solicitação do cidadão para retirada domiciliar.
8. Doações podem ser associadas a um lote. O ponto prepara e despacha; o parceiro confirma recebimento. Fechamento é uma ação operacional posterior.
9. A linha de acompanhamento e os painéis refletem os eventos. A ONG também tem uma fila para distribuição social.

Estados de doação: `PENDING → AT_POINT → IN_TRANSIT → DELIVERED → DISTRIBUTED`, além de cancelamento. Estados de lote: `OPEN`, `READY_TO_SHIP`, `IN_TRANSIT`, `DELIVERED`, `CLOSED`, `CANCELLED`. As ações têm condições e verificações de papel; as listas de estados não significam liberdade de transição entre quaisquer valores.

## 2. Arquitetura e superfícies

Frontend Next.js 14/App Router, React, TypeScript, Tailwind, React Query, Leaflet, Framer Motion e componentes Three.js. Navegação e painéis mudam conforme o papel. O mapa possui busca, geolocalização e escolha de ponto compatível. Existe consulta de perfil público com regras e informações do local.

No navegador, as requisições passam pelo proxy `/api/backend/[...path]`. Chamadas no servidor usam a URL interna configurada. Auth.js integra os tokens do Fastify e sua renovação.

Backend Fastify/TypeScript, Prisma/PostgreSQL, Redis para funcionalidades de suporte e MinIO para mídia. A infraestrutura está descrita nos arquivos Compose; esta etapa não iniciou containers nem acessou serviços externos do produto.

| Área | Arquivos de referência |
| --- | --- |
| Modelo de dados e relações | `api/prisma/schema.prisma` |
| Registro dos módulos | `api/src/server.ts` |
| Autenticação e sessões | `api/src/modules/auth/`, `web/lib/auth.ts` |
| Perfis e governança | `api/src/modules/profiles/`, `api/src/modules/admin/` |
| Mapa e perfis públicos | `api/src/modules/collection-points/`, `api/src/modules/addresses/`, `web/components/map/` |
| Registro e estados | `api/src/modules/donations/donations.ts`, `web/app/(app)/doar/page.tsx`, `web/components/donations/` |
| Parcerias e retiradas | `api/src/modules/partnerships/`, `api/src/modules/pickup-requests/`, `web/components/operations/` |
| Lotes e leitura de código | `api/src/modules/operational-batches/`, `web/components/operations/operational-code-scanner.tsx` |
| Pontuação e campanhas | `api/src/shared/donation-points.ts`, `api/src/modules/gamification/`, `api/src/modules/seasonal-campaigns/` |
| Comunicação e uploads | `api/src/shared/operational-emails.ts`, `api/src/modules/notifications/`, `api/src/modules/uploads/` |
| Superfície de marca | `web/components/branding/`, `web/components/ui/vestgo-hero.tsx`, `web/styles/globals.css`, `web/tailwind.config.ts` |
| Metadados e navegação | `web/app/layout.tsx`, `web/components/layout/navigation.ts`, favicons e manifest |

Há notificações persistidas com refetch/polling; não há necessidade de prometer atualização em tempo real. O projeto também tem páginas de apresentação, conteúdo acadêmico e equipe, que deverão entrar no inventário editorial do rebranding. Há referências visíveis a “Mosfet” além de “VestGO”.

## 3. O que pode ser reaproveitado

As estruturas de conta, endereço, mapa, perfil, aprovação administrativa, vínculo entre organizações, registro com código, histórico de eventos, lotes, notificações e mídia são uma base útil. Isso não é uma certificação de segurança ou de disponibilidade atual: não houve teste de login, QR, e-mail, storage ou banco nesta entrega.

As proteções e os contratos devem ser preservados durante a futura mudança visual. Serviços, buckets, volumes, variáveis e domínios não precisam ser renomeados como consequência imediata da identidade.

## 4. Adaptações de domínio necessárias

| Tema | Evidência atual | Encaminhamento proposto, ainda não implementado |
| --- | --- | --- |
| Catálogo | Enum contém categorias de doação | Criar famílias/subtipos de resíduos com regras de aceite. Não concentrar tudo em `OTHER` |
| Quantidade | Entrada usa inteiros, mínimo 1, máximo 200 por item | Separar unidade de contagem, massa e volume; óleo pode exigir litros e valores decimais |
| Conservação | `EXCELLENT`/`GOOD` são obrigatórios ou recebem default | Substituir por atributos pertinentes ao material, definidos com o parceiro |
| Acondicionamento | Sacola/caixa e estimador calibrado para categorias de doação | Remover a recomendação herdada e elaborar orientação específica por família, revisada pela operação |
| Aceite | Frontend compara categorias aceitas; criação backend consulta perfil e parceria | Validar compatibilidade de material/subtipo no servidor. A criação observada não cruza os itens com `acceptedCategories` do ponto |
| Operador | `NGO` centraliza recebimento e distribuição social | Definir operador de coleta/transporte e unidade de destinação, permitindo uma organização com mais de uma função |
| Destino | Não há entidade própria para instalação destinadora | Definir identidade/local da unidade, vínculo com lote e responsabilidade de recebimento |
| Fechamento | `CLOSED` fecha lote, sem equivaler a certificado | Separar fechamento operacional de evidência final de destinação |
| Comprovantes | Não há modelo dedicado de comprovante de destinação | Se fizer parte do escopo, definir documento, emissor, data, material, quantidade e vínculo ao lote |
| Pontos | Bônus por estado excelente, variedade e distribuição | Rever regras; premiar participação confirmada, sem confundir pontuação com impacto ambiental ou estimular volume artificial |
| Mensagens | E-mails, alertas e conquistas usam vocabulário solidário | Atualizar toda a comunicação, incluindo templates de backend, não apenas telas |
| Campanhas | Campanhas com categorias e multiplicador | Rever pertinência das campanhas e dos multiplicadores para resíduos |

O schema tem `weightKg` no item, mas o fluxo de criação observado não recebe esse valor. A existência desse campo não prova medição real. Uma quantidade cadastrada pelo usuário também não deve virar peso verificado ou cálculo de CO2 sem método e evidência.

## 5. Observações editoriais para o redesenho

Na landing atual há métricas fixas como “45,8t”, “12,4k”, “890” e “93%”. São valores definidos no código da página, não consultas de métricas naquele componente. Não transportá-los para o EcoVerse como resultados reais. Exemplos de parceiros/distâncias também precisam ser tratados como demonstração ou substituídos por dados da rede.

README, ARCHITECTURE e CONTEXT possuem passagens contraditórias sobre recuperação de senha e e-mails operacionais. As rotas de recuperação e os módulos de e-mail existem no código. A documentação deve ser reconciliada na fase de adaptação, sem atribuir aos testes desta entrega uma validação que não ocorreu.

Ao substituir a marca, contemplar metadados, Open Graph, favicon, manifest, navegação, telas públicas e autenticadas, mensagens de erro, e-mails, conquistas, conteúdo acadêmico, créditos e textos de ajuda. Chaves de preferência/rascunho no armazenamento local devem ser migradas deliberadamente se mudarem de nome.

## 6. Premissa e limites do EcoVerse

O grupo definiu descarte correto como foco. Famílias iniciais: pilhas/baterias, eletrônicos, lâmpadas e óleo de cozinha. Medicamentos, seringas, perfurocortantes e resíduos de serviços de saúde ficam fora desta proposta. Novas famílias dependem de parceiro e regra de recebimento.

A referência ReUse foi lida visualmente: material + cidade/CEP, encontro de ponto, orientações, entrega e acompanhamento. Ela ainda contém o termo “doação” na explicação do fluxo. Essa leitura foi usada para entender a proposta; não é uma auditoria técnica do site e nenhum formulário foi submetido.

Fontes externas consultadas em 19/10/2026:

- [Site ReUse fornecido pelo grupo](https://reuse-logistica-reversa.mightybud67.chatgpt.site/).
- [SINIR: logística reversa](https://www.sinir.gov.br/perfis/logistica-reversa/) e [fluxo de pilhas e baterias](https://www.sinir.gov.br/perfis/logistica-reversa/logistica-reversa/pilhas-e-baterias/). Usados para contextualizar a rede, sem tratar óleo de cozinha como óleo lubrificante.
- [W3C: contraste mínimo](https://www.w3.org/TR/WCAG22/#contrast-minimum).
- [Manrope](https://github.com/google/fonts/tree/main/ofl/manrope) e [DM Sans](https://github.com/google/fonts/tree/main/ofl/dmsans), fontes oficiais com OFL incluída no kit.

## 7. Sequência sugerida após avaliação da marca

1. Consolidar a direção visual desta v1.0.
2. Identificar os parceiros e esclarecer se coletor, transportador e destinador serão funções separadas.
3. Fechar catálogo inicial, unidades, aceite, restrições e limite do rastreio.
4. Desenhar as jornadas de descoberta, registro, entrega, rastreio e operação.
5. Adaptar a camada de domínio de forma incremental, com migrações explícitas e preservação de dados válidos.
6. Aplicar a marca e validar os fluxos em ambiente local, inclusive 320 px, QR, permissões e integrações disponíveis.

Não houve alteração de backend nem implementação do novo frontend nesta fase.
