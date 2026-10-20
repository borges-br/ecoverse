# Homepage cinematográfica EcoVerse

Implementação e validação local em 20/10/2026. Nenhuma publicação externa foi realizada.

## Resultado

Hero com vídeo em tela cheia, headline “O fim não é o fim.”, contraste localizado e ações na base da cena. A marca original, a tipografia Manrope/DM Sans, as cores institucionais e as rotas existentes foram preservadas. O cabeçalho fica transparente sobre a cena e ganha superfície off-white ao chegar ao conteúdo. O menu mobile mantém os links, fecha com Escape e devolve o foco ao botão.

A busca fica imediatamente depois do vídeo. Mantém as quatro categorias, seleção inicial de pilhas, localização com limite de 120 caracteres, remoção de espaços nas extremidades e navegação por `/mapa?material=...&search=...`. “Registrar descarte” continua acessível no painel e no fluxo “Como funciona”. As seções de materiais, parceiros, dúvidas e rodapé foram mantidas.

A página e o hero são Server Components. Somente reprodução, navegação, formulário, FAQ e os componentes interativos já existentes usam estado no cliente. Nenhuma dependência foi adicionada.

## Desktop e mobile

- `100svh`, com fallback `100vh`, dimensões mínimas para telas curtas e atenção às safe areas.
- Imagem e vídeo usam `object-fit: cover`, sem distorção nem barras. O poster vertical é um recorte central da imagem estática original.
- Até 800 px em orientação vertical: MP4 1080 × 1920. Nas demais telas: MP4 1920 × 1080. A origem é atribuída somente depois de conhecer a preferência do dispositivo; não existem dois vídeos simultâneos.
- No ultrawide e no celular horizontal, o texto ocupa a área lateral livre para preservar os objetos centrais. Nos demais tamanhos, fica no céu. No celular horizontal curto, o CTA secundário é omitido; o principal e as seções continuam acessíveis.
- As telas mais curtas exigem uma pequena rolagem para ver a base completa da cena. O CTA principal permanece visível em 320 × 568 e 844 × 390.

## Mídia e carregamento

As propriedades foram inspecionadas com FFmpeg, incluindo decodificação dos 240 frames de cada origem:

| Propriedade | Desktop | Mobile |
| --- | --- | --- |
| Resolução | 1920 × 1080 | 1080 × 1920 |
| Codec / pixel format | H.264 High / yuv420p | H.264 High / yuv420p |
| Cor | bt709, progressivo | bt709, progressivo |
| Duração / FPS | 8 s / 30 FPS | 8 s / 30 FPS |
| Bitrate do vídeo | aproximadamente 9532 kb/s | aproximadamente 5377 kb/s |
| Tamanho | 9.534.444 bytes | 5.380.419 bytes |
| Áudio | Ausente | Ausente |

Ambas as origens já contêm `moov` antes de `mdat`, compatível com faststart. As cópias finais são idênticas aos vídeos fornecidos: não houve recompressão, alteração de resolução, FPS ou loop. Uma tentativa de recompressão não foi possível com o FFmpeg disponível; nenhum arquivo dessa tentativa é usado. A seleção da versão vertical evita transferir o vídeo horizontal maior em celulares. Não foi criado WebM sem benefício comprovado.

O poster paisagem original tem 387.664 bytes; o recorte vertical tem 115.754 bytes. A imagem recebe prioridade alta e aparece no HTML inicial. O vídeo começa sem `src`, com `preload="none"`; a origem é anexada após a primeira oportunidade de pintura. O poster permanece sob o vídeo e só dá lugar à reprodução após `playing`, com transição de opacidade. As duas camadas têm a mesma área e o mesmo posicionamento.

`autoplay`, `muted`, `loop` e `playsInline` estão presentes, sem controles nativos ou botão de áudio. A preferência por movimento reduzido e `navigator.connection.saveData`, quando disponível, impedem a requisição do MP4. Mudanças de preferência são respeitadas durante a sessão. Falha de mídia ou de autoplay mantém a imagem estática. O vídeo pausa fora da tela e quando a aba fica oculta.

## Arquivos

Fontes alteradas ou criadas em `web/components/ecoverse/`:

- `home.tsx`: composição da página no servidor.
- `cinematic-hero.tsx`: cena, texto e CTAs.
- `hero-media.tsx`: reprodução, fonte responsiva e fallbacks.
- `home.module.css`: composição e estilos locais responsivos.
- `home-search.tsx`: formulário existente isolado em componente interativo.
- `home-faq.tsx`: comportamento existente de dúvidas.
- `public-chrome.tsx` e `public-chrome.module.css`: variante cinematográfica do cabeçalho.

Assets em `web/public/ecoverse/hero/`: `landscape.mp4`, `portrait.mp4`, `poster.webp` e `poster-portrait.webp`. As origens em `hero/` foram preservadas. `.gitignore` também ignora as pastas temporárias de compilação desta revisão.

## Validação executada

| Verificação | Resultado |
| --- | --- |
| TypeScript: `npm.cmd run type-check` | PASS |
| Lint dos seis componentes TSX envolvidos | PASS |
| Lint completo: `npm.cmd run lint` | Falha preexistente: regra `react-hooks/exhaustive-deps` ausente em `disposal-flow.tsx:54` |
| Compilação de produção | PASS, 32 rotas |
| Navegador Chromium, versão compilada | 21 grupos PASS |
| Console da homepage durante a bateria responsiva | Nenhuma exceção ou mensagem de erro capturada |
| CLS inicial observado na sessão medida | 0,001136; não é zero, e não houve deslocamento causado pela troca poster/vídeo |
| API local de pontos de coleta | BLOCKED: HTTP 503 |

Dimensões verificadas: 1440 × 900, 1920 × 1080, 2560 × 1080, 1366 × 768, 1024 × 768, 768 × 1024, 390 × 844, 320 × 568, 360 × 640, 430 × 932 e 844 × 390. Nenhuma apresentou overflow horizontal. A revisão verificou poster carregado, reprodução real, um único MP4 solicitado por carregamento e separação entre texto e a região dos objetos.

Também foram executados: observação de uma volta completa do loop; todas as seleções de material; busca com localização; CTAs; menu mobile e foco com Escape; links e rotas públicas; redirecionamento autenticado de `/descartar`; abas com teclado; abertura e fechamento do FAQ; alteração dinâmica de movimento reduzido; troca de orientação; pausa fora da cena; poster em redução de movimento, economia de dados, falha de rede e recusa simulada de autoplay.

O envio dos filtros ao mapa foi validado. A obtenção de resultados reais depende da API local, que respondeu 503 nesta sessão. Não foram criados registros nem alterados dados de usuários.

## Compilação local e evidências

A pasta gerada `.next/standalone` já estava bloqueada por outro processo. O Next.js ficou preso ao tentar limpá-la. Para validar sem encerrar esse processo, a compilação foi direcionada a `.next-cinematic-review` pelo auxiliar local `.validation/isolated-next-output.cjs`. Esse auxiliar altera somente o diretório de saída em memória; `next.config.mjs` permanece inalterado. Os acréscimos automáticos temporários ao `tsconfig.json` foram removidos.

Comandos usados em PowerShell, dentro de `web/`, para a compilação isolada:

```powershell
$env:NEXT_TELEMETRY_DISABLED='1'
$env:NEXT_IGNORE_INCORRECT_LOCKFILE='1'
$env:ECOVERSE_DIST_DIR='.next-cinematic-review'
$env:NODE_OPTIONS='--require C:/Users/natha/Downloads/EcoVence/.validation/isolated-next-output.cjs'
npm.cmd run build
```

A supressão da tentativa automática de corrigir o lockfile evita acesso ao registro de pacotes durante a validação; nenhuma dependência ou lockfile foi atualizada. A compilação exibiu avisos do Browserslist e da biblioteca de autenticação no Edge Runtime, sem impedir o resultado.

Evidências em `output/review/cinematic/`: capturas nos onze tamanhos, fallbacks, página completa, propriedades da mídia e `browser-results.json`. O executor está em `.validation/cinematic-review.cjs`. As capturas usam a escolha de cookies essenciais já registrada para permitir a inspeção da interface.

Limites: validação local em Chromium com viewports simuladas, sem teste em Safari/iPhone físico, sem auditoria formal WCAG de cada frame e sem medição em rede móvel real. Nenhum asset está pendente.
