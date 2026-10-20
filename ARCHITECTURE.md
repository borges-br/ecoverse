# EcoVerse — arquitetura atual

## Estrutura

- `web/`: Next.js 16 App Router, React 19, TypeScript, Auth.js, Tailwind 4, React Query e Leaflet.
- `api/`: Fastify 5, Prisma, autenticação JWT/refresh, autorização por papel e módulos de domínio.
- PostgreSQL 16/PostGIS e Redis 7 mantêm os dados e o estado auxiliar. Uploads ficam em um volume exclusivo da API, servido pelas mesmas URLs `/api/backend/uploads/...`. Os servidores de objetos e o SDK MinIO foram removidos da nova stack.
- O navegador chama `/api/backend/...`; o servidor Next usa `INTERNAL_API_URL` diretamente.

O Compose de produção cria a stack EcoVerse com banco, credenciais e três volumes exclusivos. Somente a web entra na rede compartilhada do proxy. O pipeline publica imagens próprias no GHCR após as verificações de qualidade. O [guia de publicação](docs/PRODUCTION.md) descreve a troca do domínio; o [registro de validação](docs/ecoverse/publicacao-validacao.md) informa o que foi efetivamente executado. A stack e os volumes anteriores do VestGO são preservados.

## Papéis e unidades

| Identificador preservado | Nome na interface | Responsabilidade |
| --- | --- | --- |
| DONOR | Participante | Registrar e entregar no ponto; consultar o próprio histórico |
| COLLECTION_POINT | Ponto de coleta | Receber por QR, administrar parcerias e preparar retiradas/lotes |
| NGO | Operador parceiro | Organizar retirada, transporte e confirmar recebimento |
| ADMIN | Administrador | Governança de perfis e funções administrativas existentes |

Nesta versão, a unidade de recebimento usa o endereço do operador. Não há entidade independente de destinador ou módulo de certificados ambientais.

## Domínio preservado

`Donation`, `DonationItem` e `DonationEvent` continuam representando o registro e sua trilha. `OperationalPartnership`, `PickupRequest`, `OperationalBatch` e `OperationalBatchItem` mantêm as relações e transições logísticas. `UserSession`, estruturas de 2FA, notificações, `PointLedger` e conquistas não foram substituídos.

Status mantidos: PENDING, AT_POINT, IN_TRANSIT, DELIVERED, DISTRIBUTED e CANCELLED. A jornada principal EcoVerse mostra cadastro, recebimento no ponto, transporte e recebimento no destino. DISTRIBUTED permanece compatível com o histórico e é descrito como processamento informado; não comprova reciclagem.

## Adaptações EcoVerse

- Quatro categorias adicionais no enum ItemCategory; sete categorias antigas permanecem para leitura do histórico.
- DonationItem.quantity: Int → Float para litros decimais. Unidades inteiras continuam validadas na API; óleo admite até duas casas decimais.
- Novos registros são validados por `api/src/shared/disposal.ts`; somente as categorias atuais podem ser criadas. O aceite do ponto é validado também no backend.
- Migrações `202610190001_ecoverse_materials` e `202610190002_ecoverse_quantities`, nesta ordem.
- Participação EcoVerse: 10 pontos após confirmação no ponto, sem bônus por volume, condição ou distribuição. Fórmula antiga e ledger existente preservados para registros históricos.
- Totais de famílias/linhas de materiais não somam litros com unidades. Quantidades individuais carregam a unidade na interface.
- Códigos novos ECO; leitores e API aceitam também VGO; lotes mantêm LOT.
- `/descartar` usa a API existente; `/doar` é um alias compatível. Rascunho local EcoVerse usa chave própria.

## Interface

Assets aprovados em `web/public/ecoverse/`; identidade compartilhada em `components/branding/ecoverse-brand.tsx`; páginas e componentes novos em `components/ecoverse/`; estilos em `styles/ecoverse.css`. Manrope e DM Sans locais. Animações com entrada única, repouso e redução de movimento.

A navegação pública permite consultar a rede sem login. Cadastro e acompanhamento pessoal usam sessão. A interface operacional mantém suas funções com a nova identidade. Preferências antigas de tema e eventos internos foram mantidos por compatibilidade.

## Evidências e documentação anterior

[Decisões e telas](docs/ecoverse/redesign-implementado.md) e [validação local](docs/ecoverse/validacao-local.md) descrevem o que foi realmente executado e os limites. Detalhes históricos da arquitetura e dos fluxos anteriores permanecem em [docs/legacy/vestgo-ARCHITECTURE.md](docs/legacy/vestgo-ARCHITECTURE.md); essa cópia não descreve as novas regras de descarte.
