# EcoVerse no Portainer

O EcoVerse será publicado em **mosfet.com.br**, no ambiente **Borges VPS** do [Portainer](https://vps.borgesti.com). A stack se chama **ecoverse** e começa com uma base independente. A stack anterior, `mosfet`, continua disponível para retorno até a validação da troca.

Este guia descreve a configuração. O [registro de validação](ecoverse/publicacao-validacao.md) distingue testes locais, publicação das imagens e verificação no domínio.

## O que será criado

| Serviço | Função | Acesso |
| --- | --- | --- |
| `ecoverse-web` | Next.js / Auth.js | Proxy → HTTP `ecoverse-web:3000` |
| `ecoverse-api` | Fastify / Prisma / uploads persistentes | Rede própria, porta 3001 |
| `ecoverse-db` | PostgreSQL 16 / PostGIS | Rede própria, porta 5432 |
| `ecoverse-redis` | Sessões auxiliares, limites e 2FA | Rede própria, porta 6379 |

O [Compose de produção](../docker-compose.prod.yml) não publica portas no host nem depende de pastas montadas do servidor. Somente o serviço web participa da rede externa `rvproxy_npm_backend_network`.

| Recurso | Nome exclusivo |
| --- | --- |
| Banco e usuário PostgreSQL | `ecoverse` |
| Volume do banco | `ecoverse_db_data` |
| Volume Redis | `ecoverse_redis_data` |
| Volume de imagens | `ecoverse_uploads_data`, montado em `/app/uploads` na API |

A conexão PostgreSQL é montada no Compose com o host `ecoverse-db`. Não importe `DATABASE_URL`, segredos ou nomes de volumes do VestGO. O SMTP pode ser o mesmo; o banco e as chaves de autenticação devem ser exclusivos.

## 1. Publicar as imagens

O repositório de destino é [borges-br/ecoverse](https://github.com/borges-br/ecoverse). Um envio para `main` inicia o [GitHub Actions](https://github.com/borges-br/ecoverse/actions).

Antes de publicar, o fluxo verifica lint, tipos, auditoria das dependências de produção, build, testes de domínio e isolamento do Compose. Depois publica:

- `ghcr.io/borges-br/ecoverse-web:sha-<commit completo>`
- `ghcr.io/borges-br/ecoverse-api:sha-<commit completo>`
- As duas imagens também recebem a tag `latest`.

Para a stack, prefira a tag `sha-...` do mesmo commit nas duas imagens. Isso permite identificar e reverter a versão. `latest` é útil para experimentação, mas muda a cada publicação.

Se os pacotes GHCR estiverem privados, selecione no Portainer o registro com credencial de leitura. Um repositório público não garante, por si só, que seus pacotes estejam públicos. Tokens não pertencem ao Compose ou ao GitHub público.

## 2. Preparar as variáveis

Na pasta do projeto, com Node.js 24:

```bash
node tools/deploy/prepare-env.mjs
```

O gerador cria `.env.portainer` com segredos aleatórios independentes. O arquivo é ignorado pelo Git e não é sobrescrito em uma segunda execução. Guarde uma cópia privada para recuperação do ambiente.

Preencha no arquivo:

| Variável | Valor |
| --- | --- |
| `ECOVERSE_IMAGE_TAG` | `sha-` seguido do commit que concluiu o pipeline |
| `ECOVERSE_APP_URL` | `https://mosfet.com.br` |
| `ECOVERSE_CORS_ORIGIN` | `https://mosfet.com.br,https://www.mosfet.com.br` |
| `ECOVERSE_PROXY_NETWORK` | `rvproxy_npm_backend_network` |
| `ECOVERSE_ADMIN_EMAIL` | E-mail do primeiro administrador |
| `ECOVERSE_ADMIN_PASSWORD` | Senha gerada, mantida em local privado |

O remetente, usuário, senha e servidor SMTP devem ser preenchidos para `ECOVERSE_EMAIL_ENABLED=true`. Com e-mail desativado, confirmação de conta e recuperação por e-mail ficam indisponíveis. A configuração privada desta publicação pode reaproveitar o SMTP já usado pelo VestGO, conforme autorizado pelo responsável.

Não troque as senhas de banco ou Redis em uma atualização comum: alterar apenas a variável não altera necessariamente a credencial já persistida no volume. Preserve o arquivo utilizado na primeira implantação.

As imagens são gravadas pela API no volume exclusivo `ecoverse_uploads_data`. O processo roda como usuário `node`; arquivos têm nomes gerados pelo serviço e acesso por `/api/backend/uploads/...`. O volume novo não recebe os arquivos internos do MinIO antigo. Faça backup do banco e desse volume de imagens em conjunto. Esta configuração atende uma API em uma única VPS; para múltiplos hosts, é necessário armazenamento compartilhado antes de escalar.

Geocodificação usa Nominatim por padrão. Mapbox é opcional. As chaves não estão incluídas no repositório.

## 3. Criar a stack ecoverse

No Portainer, selecione **Borges VPS → Stacks → Add stack**.

1. Nome: `ecoverse`. Crie uma stack nova; não atualize a stack `mosfet` com este arquivo.
2. Em **Repository**, use `https://github.com/borges-br/ecoverse`, referência `refs/heads/main` e caminho `docker-compose.prod.yml`. O repositório é público.
3. Outra opção é **Web editor**, colando o conteúdo integral do Compose de produção.
4. Em **Environment variables**, importe `.env.portainer`. Esse conteúdo é privado e deve ficar restrito aos administradores do ambiente.
5. Confira a tag das duas imagens e a rede externa existente. Mantenha o acesso à stack restrito aos administradores.
6. Inicie a implantação e acompanhe os quatro serviços. A API executa `prisma migrate deploy` antes de iniciar, com o Prisma já instalado na imagem.

Uma falha de pull deve ser corrigida no registro/tag. Não substitua as imagens por `vestgo-*`. Uma falha por rede ausente exige conferir o nome da rede compartilhada do proxy, sem criar uma rede desconectada dele.

## 4. Validar antes de mudar o domínio

A web só fica saudável depois da API. A API verifica banco, Redis e as permissões de leitura/gravação do volume de imagens em `/health/ready`; `/health` indica apenas que o processo respondeu.

No console do container `ecoverse-web`, é possível verificar a API internamente:

```bash
wget -qO- http://ecoverse-api:3001/health/ready
```

Resultado esperado: `status: ready` e `database`, `redis`, `storage` com valor `ok`. Confira também nos logs da API a conclusão das migrações e a criação do administrador. Não copie logs contendo credenciais para o repositório.

Antes da troca, mantenha o backup habitual do VestGO e registre o destino atual do proxy. Seus volumes devem continuar associados à stack antiga. **Não use `down -v` nem selecione remoção de volumes.**

## 5. Direcionar mosfet.com.br

No [Nginx Proxy Manager](https://npm-b.shop/), edite o Proxy Host existente de `mosfet.com.br` e `www.mosfet.com.br`:

| Campo | Valor novo |
| --- | --- |
| Scheme | `http` |
| Forward Hostname / IP | `ecoverse-web` |
| Forward Port | `3000` |

Preserve os domínios, o certificado e a configuração HTTPS do host. O endereço de destino é o nome do serviço na rede Docker; `localhost` apontaria para o próprio proxy.

A API e as imagens usam `https://mosfet.com.br/api/backend/...`. O EcoVerse não depende dos antigos hosts separados de API ou armazenamento. O serviço web encaminha essas requisições para a sua própria API.

## 6. Conferir a publicação real

Faça a verificação no domínio depois da troca:

- Homepage, vídeo desktop/mobile e imagens estáticas carregam por HTTPS.
- `/api/backend/health/ready` retorna 200 com as três dependências prontas.
- O administrador consegue entrar e abrir a área administrativa.
- Cadastro, envio da confirmação e recuperação chegam à caixa de e-mail.
- Busca por material funciona. Uma rede inicialmente vazia deve aparecer vazia, sem pontos fictícios.
- Um teste controlado de registro/QR respeita os papéis e as quantidades.
- Uma imagem enviada pelo perfil pode ser lida novamente pelo mesmo domínio.

As verificações locais estão documentadas separadamente. Uma imagem construída ou um container saudável não comprovam que todos esses passos funcionam no domínio.

Após o primeiro login, remova `ECOVERSE_ADMIN_EMAIL` e `ECOVERSE_ADMIN_PASSWORD` das variáveis da stack e atualize-a. O usuário já criado permanece no banco; a remoção das variáveis evita manter a credencial de bootstrap na configuração ativa. Guarde a senha em seu gerenciador e use a tela de conta para alterá-la.

## Atualizar e voltar à versão anterior

Para atualizar, aguarde o pipeline do novo commit, altere somente `ECOVERSE_IMAGE_TAG` e atualize a stack com pull das imagens. Preserve todas as demais variáveis e volumes. Faça backup antes de migrações que alterem o esquema.

Para desfazer apenas a troca inicial do domínio, restaure no proxy o destino anterior do VestGO (normalmente `vestgo-web:3000`, confirme no host antes de editar). O banco antigo continua na stack `mosfet`.

Para voltar uma versão do EcoVerse, use a tag anterior das duas imagens. Uma reversão de imagem não reverte migrações; avalie compatibilidade do esquema antes de iniciar a versão anterior. Não misture os bancos dos dois projetos.

## Referências

- [Portainer: criar stacks](https://docs.portainer.io/user/docker/stacks/add)
- [Docker Compose: nomes de projeto](https://docs.docker.com/compose/how-tos/project-name/)
- [GitHub Actions: publicar imagens Docker](https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images)
- [Guia anterior do VestGO, preservado como histórico](legacy/vestgo-PRODUCTION.md)
