# Preparação da publicação — 20/10/2026

## Estado desta entrega

| Etapa | Resultado |
| --- | --- |
| Atualização de segurança e compatibilidade | Concluída e validada localmente |
| Build das imagens web e API | Aprovado em Docker / Node.js 24 |
| Testes integrados | 18 verificações aprovadas no ambiente isolado com volume de uploads |
| Homepage após a atualização | 22 verificações aprovadas em navegador, incluindo 11 dimensões de tela |
| Isolamento do Compose de produção | Verificado por `tools/deploy/check-stack.mjs` |
| GitHub / GHCR | Repositório público criado; web/API publicadas e pipeline aprovado no commit `7924b0023ad516e152bf78d5ebc9e18f7fd80513`; ajustes finais do Compose são acompanhados no histórico do Actions |
| Portainer e troca do domínio | Exigem implantação e validação no servidor; os resultados locais não comprovam produção |

## Dependências

Auditoria npm das dependências de produção, comparando os arquivos de lock anteriores e atualizados:

| Aplicação | Antes | Depois |
| --- | --- | --- |
| Web | 3 críticas, 9 altas, 3 moderadas | Nenhuma vulnerabilidade reportada |
| API | 3 críticas, 6 altas, 5 moderadas | Nenhuma vulnerabilidade reportada |

As dependências de desenvolvimento também foram verificadas: nenhuma alta ou crítica permaneceu. A auditoria é um retrato da base de avisos na data da consulta, não uma garantia de ausência de falhas no código ou nas imagens de sistema operacional.

Atualizações principais:

- Next.js 14 → 16.4.2; React 18 → 19.3.1; Auth.js beta.30 → beta.32.
- Tailwind CSS 3 → 4.3.3, com o plugin PostCSS correspondente.
- Fastify 4 → 5.12.7, JWT 10, CORS 11 e fastify-plugin 5.
- bcrypt 6 e Nodemailer 10.1.7; SDK MinIO removido.
- Imagens da aplicação em Node.js 24, execução final com usuário `node`.

As adaptações incluem parâmetros assíncronos de rotas, `proxy.ts` para a proteção de navegação, bibliotecas React compatíveis e a configuração de estilos. O esquema de dados e a autorização por papel foram preservados.

Os avisos moderados restantes da árvore do SDK MinIO foram eliminados com a remoção dessa dependência. A API usa apenas recursos nativos do Node.js para gravar e servir imagens no volume persistente, mantendo o contrato das rotas. Criação exclusiva de arquivos evita sobrescrita; leitura recusa caminhos arbitrários, extensões fora do catálogo e links simbólicos.

Na conferência das imagens, o servidor MinIO antigo não pôde ser baixado do registro original. Além disso, os avisos oficiais [GHSA-hv4r-mvr4-25vw](https://github.com/minio/minio/security/advisories/GHSA-hv4r-mvr4-25vw) e [GHSA-9c4q-hq6p-c237](https://github.com/minio/minio/security/advisories/GHSA-9c4q-hq6p-c237) afetam as releases finais da edição comunitária, sem correção nessa linha. Para a implantação em uma única VPS, a solução final usa **um volume exclusivo de uploads na API**. Não há servidor S3 na nova stack. Nenhum volume MinIO anterior é convertido ou reutilizado.

A auditoria npm não avalia os servidores de armazenamento, PostgreSQL, Redis ou os pacotes do sistema operacional. Não foi executada uma auditoria completa de vulnerabilidades de todas as imagens.

## Ambiente local de publicação

Foi criada a stack de teste `ecoverse-release-test`, com banco, Redis e volumes próprios. Somente as portas de loopback 3130/3131 foram usadas para testes. O Compose de produção não publica essas portas.

Foram executados:

- Build de produção de web e API em Docker; lint e verificação de tipos nas duas aplicações.
- Os testes de domínio e os três testes de armazenamento em `api/tests/`; o ensaio Linux inclui recusa de links simbólicos.
- Aplicação das 20 migrações Prisma em banco independente e novo início idempotente.
- Login real da API e sessão Auth.js para participante, ponto de coleta, operador e administrador.
- Renderização das páginas protegidas, incluindo filtros de operações e detalhe do registro com parâmetros assíncronos.
- Busca por material e parceria ativa, registro de 1,25 L, rejeição de quantidade fracionária em materiais contáveis e consulta por código QR.
- Recusa de confirmação pelo participante e confirmação autorizada pelo ponto.
- Upload real de PNG e recuperação pela rota pública da aplicação, comparando todos os bytes; a imagem persistiu com bytes idênticos após o reinício da API.
- Upload sem sessão, MIME divergente e tentativa de caminho codificado foram recusados.
- `/health/ready` com banco, Redis e armazenamento; revogar temporariamente o acesso ao volume de teste produziu 503 e restaurar as permissões recuperou 200.
- Usuário `node` nos containers web/API e verificação dos volumes montados no ambiente de teste.
- Páginas públicas, proteção anônima, posters e requisição parcial do vídeo com HTTP 206.

Os perfis usados nos testes são fictícios. Nenhuma conta ou ponto de coleta de demonstração é inserido automaticamente na produção.

## Verificação visual

A homepage atualizada foi aberta em 1440×900, 1920×1080, 2560×1080, 1366×768, 1024×768, 768×1024, 390×844, 320×568, 360×640, 430×932 e 844×390.

Foram verificados enquadramento, ausência de rolagem horizontal, carregamento de uma única versão do vídeo, autoplay silencioso, loop observado, preferências de movimento, economia de dados, falha de mídia e bloqueio de autoplay. Também foram exercitados menu mobile, Escape e foco, busca, seleção de materiais, navegação, abas do processo e FAQ. A busca alcançou a API real do ambiente de teste.

Os screenshots do README apresentam a aplicação, sem montagem de telas ou métricas fictícias. As evidências completas de execução ficam em `output/review/`, uma pasta local ignorada pelo Git; as imagens selecionadas estão em `docs/readme/`.

## Conferência no servidor

O ambiente Borges VPS foi consultado no Portainer. Os containers anteriores pertencem à stack `mosfet`, com imagens `vestgo-web` e `vestgo-api`. Eles não precisam ser recriados para instalar o EcoVerse. O Compose novo usa quatro serviços `ecoverse-*` e três volumes exclusivos.

O SMTP existente foi disponibilizado para reaproveitamento por autorização do responsável. A primeira autenticação foi recusada; após a atualização da senha pelo responsável, a conexão TLS e a autenticação foram aprovadas, sem envio de mensagem. A entrega de e-mail ao destinatário continua pendente de teste na aplicação publicada. As credenciais e os segredos novos ficam em `.env.portainer`, ignorado pelo Git, e não constam deste documento.

A publicação só deve ser considerada verificada depois dos passos do [guia de produção](../PRODUCTION.md), especialmente login no domínio, entrega de e-mail e leitura de uma imagem enviada. O domínio pode continuar servindo VestGO enquanto essa troca não for concluída.

## Referências das migrações de framework

- [Next.js 16](https://nextjs.org/docs/app/guides/upgrading/version-16)
- [Fastify 5](https://fastify.dev/docs/latest/Guides/Migration-Guide-V5/)
- [Correção de segurança do Auth.js](https://github.com/nextauthjs/next-auth/security/advisories/GHSA-8fpg-xm3f-6cx3)
