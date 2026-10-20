# Validação da primeira etapa — 19/10/2026

Este relatório registra a primeira entrega. A revisão posterior acrescentou inspeção e interação no navegador; consulte [revisão de UX](revisao-ux.md).

## Resultado

API compilada e 5 testes automatizados de domínio passaram. O front-end gerou as 32 páginas/rotas no build Next.js, com verificação de tipos. As verificações de integração e HTTP foram executadas contra os processos compilados finais, não apenas contra mocks.

### Integração: 17 verificações aprovadas

Fixtures exclusivamente fictícias no banco `ecoverse_review`; login por papel; filtro público por material e parceria ativa; rejeição de unidades fracionárias; rejeição de ponto incompatível; persistência de 1,25 L e QR; nenhum crédito no cadastro pendente; participante impedido de confirmar a própria entrega; consulta por QR; recebimento no ponto; um único crédito de 10 pontos; retirada solicitada pelo operador e aprovada pelo ponto; preparação e transporte de lote até o parceiro; eventos persistidos; nenhuma duplicação de pontos no transporte; upload/leitura reais no MinIO; endpoint de conquistas e gamificação.

### Front-end via HTTP: 9 verificações aprovadas

Páginas públicas e arquivos JS/CSS; hero/SVGs/manifest; proteção de `/descartar`; proxy `/api/backend` com filtro de material; sessão Auth.js e páginas protegidas do participante; detalhe autenticado com 1,25 L e quatro etapas; sessão e páginas do ponto; sessão e páginas do operador; consulta operacional de código VGO antigo.

### Migração com histórico: aprovada

Foi criado um segundo banco isolado, `ecoverse_upgrade_review_20261019`, dentro do projeto de teste. Primeiro recebeu as 18 migrações originais. Depois foram inseridos usuário, registro `VGO-OLD123`, categoria `CLOTHING`, quantidade inteira 7, evento e crédito histórico de 70 pontos, todos fictícios. As duas migrações EcoVerse foram aplicadas em seguida.

A comparação completa do registro, itens e eventos antes/depois foi idêntica, e o crédito permaneceu em 70 pontos. A coluna passou a double precision e aceitou um novo item de óleo com 1,25 L. Este ensaio verifica preservação no caso exercitado; não substitui backup e ensaio com uma cópia do banco real antes de qualquer futura atualização em produção.

## Limites da verificação

- **NOT_RUN — navegador:** o controle automatizado ficou bloqueado na página de erro anterior. Não houve inspeção visual da página renderizada, teste em 320 px, teste de teclado ou captura de tela do site.
- **NOT_RUN — recursos do dispositivo:** câmera QR e geolocalização.
- **NOT_RUN — serviços externos:** entrega real de e-mail, Mapbox/Nominatim, vídeo e webhook de avaliação acadêmica. O ambiente de teste não envia e-mail.
- **NOT_RUN — segurança completa:** 2FA real e auditoria de segurança; suas funções foram preservadas, não recertificadas.
- **NOT_RUN — publicação:** nenhuma alteração em VPS, Git remoto, Portainer, domínio ou HTTPS.

Os SVGs adaptados foram inspecionados como arquivos e como imagens estáticas. Isso não comprova a animação no navegador.

O build emitiu aviso de base Browserslist antiga. O início com `next start` em configuração standalone emitiu aviso de modo de execução; ainda assim, os testes HTTP documentados passaram. Não houve atualização ampla de dependências nesta etapa.

Relatórios detalhados e contas fictícias ficam em `.validation/`, ignorada pelo Git. O código anterior foi copiado para `tmp/ecoverse-before-redesign.zip`. Nenhum dado de outras stacks foi usado ou modificado.
