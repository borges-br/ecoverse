# EcoVerse — redesenho local

Estado em 19/10/2026. A identidade v1.0 foi aprovada pelo usuário. Esta implementação usa a base funcional do VestGO, com adaptações de domínio e preservação de dados históricos.

## Decisões de produto

- A pessoa leva os materiais ao ponto de coleta. Operadores parceiros retiram dos pontos.
- Novos registros aceitam pilhas e baterias, eletrônicos, lâmpadas e óleo de cozinha. Medicamentos, seringas, perfurocortantes e resíduos de serviços de saúde ficam fora do escopo.
- Pilhas, eletrônicos e lâmpadas usam unidades inteiras. Óleo usa litros, com até duas casas decimais. Limite técnico por linha: 1.000; até 20 linhas por registro. Esses limites não substituem a capacidade informada pelo ponto.
- O ponto deve aceitar explicitamente todas as categorias selecionadas e ter parceria operacional ativa. Lista de aceite vazia não significa aceite universal.
- O acompanhamento principal termina no recebimento pelo destino parceiro. Isso não certifica reciclagem nem tratamento final.
- O endereço cadastrado do operador representa sua unidade de recebimento nesta versão. Não foi criada uma entidade separada para destinadores, licenças, certificados ou MTR.
- Cada novo descarte recebido no ponto gera 10 pontos de participação, sem incentivo por volume, condição ou variedade. Conquistas, níveis, ranking e histórico continuam disponíveis. As regras e os créditos históricos não são reescritos.

## Telas e identidade

| Área | Resultado |
| --- | --- |
| Página inicial | Hero do kit, busca por material e local, jornada, guia, rede de parceiros e dúvidas |
| Materiais | Guia das quatro famílias, com consulta às regras específicas de cada ponto |
| Mapa | Busca pública, filtro de material, localização por ação da pessoa e escolha de ponto para o registro |
| Registro | Três etapas: materiais, ponto/orientações, revisão; quantidades com unidade correta, rascunho e QR real |
| Início do participante | Jornada recente, entregas confirmadas, pontos, nível, conquistas e acesso ao ranking |
| Meus descartes | Busca, filtro de etapa, ordenação, quantidades, QR, detalhes e histórico |
| Login e cadastro | Identidade aprovada aplicada, mantendo autenticação e segurança existentes |
| Parceiros e administração | Navegação, cores, fontes e linguagem adaptadas; recebimento, parcerias, retiradas, lotes e governança mantidos |
| Ajuda e apresentação | Orientações de descarte atualizadas; materiais acadêmicos do VestGO identificados como históricos |

Manrope nos títulos, DM Sans no corpo; fontes locais. Paleta Floresta, Verde rede, Lima destino, Papel, Grafite e Névoa do guia aprovado. O movimento do símbolo desenha o percurso em 800 ms, apresenta o ponto em 250 ms e repousa; respeita a preferência por reduzir movimento. O carregamento usa esse símbolo sem atraso artificial.

## Pacote SVG complementar

Os 12 SVGs enviados pelo usuário, criados com Gemini Argon, foram inspecionados. Foram adaptados apenas os quatro desenhos de materiais (06–09) e o percurso (04). Não foram substituídos o logotipo aprovado nem o hero do kit.

As adaptações removem imports remotos de fontes e textos duplicados, ajustam o enquadramento e terminam em estado estático. Originais em `animation-reference/`; assets usados em `web/public/ecoverse/motion/`. A etapa futura de comprovação não aparece como recurso implementado.

## Compatibilidade e dados

- Contas, papéis, sessões, 2FA, QR, notificações, uploads, parcerias, retiradas, lotes, administração e histórico permanecem na aplicação.
- Os identificadores técnicos `DONOR`, `COLLECTION_POINT`, `NGO`, `Donation` e rotas da API continuam, com nomes de interface atualizados.
- Novos códigos começam com `ECO-`. Códigos `VGO-` existentes continuam aceitos pelos leitores e pela consulta operacional. Códigos de lote `LOT-` permanecem.
- `/descartar` é a entrada atual; `/doar` continua compatível com links antigos.
- As sete categorias antigas permanecem no enum e no histórico, mas não são oferecidas para novos descartes.
- Duas migrações adicionam quatro categorias e convertem quantidade de inteiro para double precision. A adição dos valores de enum ocorre antes do uso do novo default.
- A sugestão automática de sacolas/caixas do vestuário não é aplicada aos novos resíduos; a preparação depende das orientações do ponto.
- Serviços, redes, buckets e volumes existentes com nomes VestGO não foram renomeados. A troca visual da marca não justifica mover dados de infraestrutura.
- Cópia inicial do código em `tmp/ecoverse-before-redesign.zip`; documentação anterior preservada em `docs/legacy/`.

## Verificação

| Verificação | Estado |
| --- | --- |
| Compilação da API e 5 testes de regras de descarte/pontos | PASS |
| Build de produção do Next.js, tipos e páginas | PASS |
| Aplicação das 20 migrações em banco vazio isolado | PASS |
| Login real por papel, autorização e compatibilidade do ponto | PASS |
| Registro de 1,25 L, QR, confirmação, retirada, lote, transporte e destino | PASS |
| Crédito único de 10 pontos, sem duplicação nas etapas seguintes | PASS |
| Upload e leitura reais no MinIO isolado | PASS |
| Páginas públicas, assets, proxy e sessões Auth.js via HTTP | PASS |
| Consulta de código VGO antigo | PASS |
| Migração com histórico previamente existente | Ver resultado em `validacao-local.md` |
| Inspeção visual das telas e interação no navegador | NOT_RUN |
| SMTP real, 2FA real, câmera, geolocalização e auditoria de acessibilidade | NOT_RUN nesta etapa |
| Publicação, DNS, HTTPS e ambiente de produção | NOT_RUN |

O navegador automatizado permaneceu bloqueado na página de erro anterior. As verificações HTTP não demonstram o layout renderizado em 320 px, funcionamento da câmera ou interação por teclado. Os desenhos SVG adaptados foram conferidos separadamente como imagens.

As verificações usam exclusivamente contas e materiais fictícios, com identificação de demonstração, no projeto Docker `ecoverse-review`. Outras stacks não foram alteradas. O ambiente de teste tem e-mail desativado.

## Revisão futura necessária

A operação real precisa validar quais organizações e materiais específicos cada ponto recebe, quais unidades são seus destinos e suas condições de funcionamento. Certificação ambiental, documentos de transporte, publicação de termos e política de privacidade e contatos oficiais dependem de definição dos responsáveis. Não foram inventados contatos, métricas de impacto ou comprovantes de reciclagem para preencher a interface.


Revisão posterior: [ajustes de navegação, densidade, conteúdo e SVGs](revisao-ux.md), com conferência no navegador.
