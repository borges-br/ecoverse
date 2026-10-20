# EcoVerse — contexto para manutenção

A marca EcoVerse v1.0 foi aprovada pelo usuário. O repositório é um clone do VestGO autorizado para alterações locais. Nome de pasta EcoVence não altera a grafia da marca.

## Decisões aprovadas

Pessoa entrega no ponto; operadores retiram dos pontos. Escopo inicial: pilhas/baterias, eletrônicos, lâmpadas e óleo de cozinha. Medicamentos, seringas, perfurocortantes e resíduos de serviços de saúde ficam fora. Manter gamificação com entregas confirmadas e marcos pessoais.

O acompanhamento vai até o recebimento na unidade parceira; não existe certificação de reciclagem implementada. O endereço do operador representa sua unidade de recebimento. Não inventar uma entidade de destino independente, licenças, certificados ou contatos oficiais.

## Estado atual

Identidade, home pública, guia de materiais, mapa filtrado, registro em três etapas, QR, painel do participante, rastreio, navegação, autenticação e comunicação dos parceiros foram adaptados. A navegação móvel do participante tem Início, Pontos, + para registrar descarte, Descartes e Conta, com destaque que acompanha a rota. A revisão de UX usa perfil compacto, QR antes dos demais dados no rastreio móvel, textos diretos e SVGs interativos. Não repetir avisos sobre materiais fora do catálogo. Funções operacionais e de segurança existentes foram preservadas.

Identificadores técnicos DONOR / COLLECTION_POINT / NGO / ADMIN, tabelas Donation e rotas existentes continuam. Novos registros usam quatro categorias adicionais. As sete antigas permanecem no histórico; nunca converter roupas em resíduos automaticamente. Óleo usa litros com duas casas; demais materiais usam unidades inteiras. O ponto precisa aceitar todos os materiais e ter parceria ativa.

Cada descarte EcoVerse recebido no ponto gera 10 pontos de participação sem bônus por quantidade, estado ou variedade. Conquistas e créditos históricos continuam. Novos códigos ECO, antigos VGO aceitos, lotes LOT. `/doar` continua alias de `/descartar`.

O tema inicial é claro, independente do sistema. Preferências explícitas de Claro, Escuro ou Sistema continuam salvas nas configurações. A equipe atual é Nathan Borges, Vinícius Stadler Gorov, Antonio Carlos Damante de Souza Guilherme Henrique de Assis Carvalho, Lincoln Mariozzi Proença Sobrinho do Prado e Matheus Lisbôa Paludeto, mantida em `web/lib/team.ts` e exibida no mesmo acordeão em Sobre e Apresentação. Registros acadêmicos não são exibidos.

## Infraestrutura e validação

A publicação EcoVerse foi autorizada em um novo repositório público `borges-br/ecoverse`, reutilizando o domínio `mosfet.com.br`. O Compose de produção cria a stack `ecoverse`, cinco serviços próprios e volumes `ecoverse_db_data`, `ecoverse_redis_data`, `ecoverse_minio_data`. Não renomear ou reaproveitar os volumes da stack anterior `mosfet`. A referência do VestGO permanece em `docs/legacy/vestgo-PRODUCTION.md`.

A atualização de segurança usa Next.js 16, React 19, Tailwind 4, Fastify 5 e Node.js 24. A proteção de navegação fica em `web/proxy.ts`, e parâmetros de páginas/rotas são assíncronos. O ambiente `ecoverse-release-test` validou migrações, quatro papéis, Auth.js, QR, upload/leitura real no MinIO e readiness com falha de armazenamento. Consulte `docs/ecoverse/publicacao-validacao.md` para os limites e o estado de publicação. Segredos de produção ficam apenas em `.env.portainer` ou no Portainer.

Build da API, 5 testes de domínio, build do Next, 17 verificações da API, 9 verificações HTTP e ensaio de migração com histórico fictício passaram. Os testes anteriores não validavam layout; a revisão de UX acrescenta a conferência no navegador. Produção continua não verificada. Na primeira etapa a ferramenta ficou bloqueada na página de erro. Na revisão seguinte a aba HTTP já estava acessível e foram realizados testes visuais e de interação em 320 px, 390 px e desktop; não foi necessário contornar bloqueios. Câmera, geolocalização, SMTP e 2FA reais não foram retestados.

## Regras para alterações

1. Descrever o estado real. Distinguir implementado, parcial, planejado e não verificado; não inventar métricas, certificados ou evidências.
2. Preservar comentários explicativos e docstrings úteis, dados e histórico. Ajustar comentários desatualizados sem apagar explicações necessárias.
3. Não comitar segredos. Manter `.env` e dados locais fora do controle de versão; usar placeholders em exemplos.
4. Manter `/api/backend/[...path]` no navegador e `INTERNAL_API_URL` no SSR.
5. Interface, mensagens, e-mails e documentação em PT-BR.
6. Usar a identidade aprovada: Manrope, DM Sans e paleta do guia. Movimento: traço 800 ms, ponto 250 ms e repouso, com reduzir movimento.
7. Não remover funções existentes de conta, administração ou operação como parte de uma limpeza visual. Rascunhos anteriores não devem ser sobrescritos por conversão automática.

Consulte [implementação](docs/ecoverse/redesign-implementado.md), [validação](docs/ecoverse/validacao-local.md), [branding](docs/ecoverse/README.md) e [arquitetura](ARCHITECTURE.md). O contexto anterior permanece em `docs/legacy/vestgo-CONTEXT.md` para referência histórica.

Revisão de UX e evidências: `docs/ecoverse/revisao-ux.md`.

Atualização de equipe, navegação e tema: `docs/ecoverse/equipe-navegacao.md`.

Conteúdo atual: não exibir registros acadêmicos dos integrantes nem referências à marca anterior na interface. Vídeo, documentos e quadro de tarefas antigos não aparecem na apresentação atual. Dúvidas da home (9) e da central de ajuda (21) compartilham `web/lib/faq.ts`.

A equipe tem seis integrantes. A barra inferior mantém o indicador retangular deslizante, sem feixe de luz.
