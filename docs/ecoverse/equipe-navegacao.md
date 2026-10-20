# Equipe, navegação e aparência — 20/10/2026

## Implementação

A apresentação usa o acordeão de fotos da referência enviada, adaptado ao Next.js 14, React 18, TypeScript e Tailwind 3 já instalados. Os componentes reutilizáveis ficam em `web/components/ui/`; as regras visuais desta revisão ficam em `web/styles/ecoverse-components.css`, importadas pelo layout raiz. Next Image e lucide-react já eram dependências, sem instalação adicional nem reinicialização de shadcn.

`tailwind-image-accordion.tsx` expande a foto ao passar o ponteiro, receber foco ou tocar. Setas e Home/End mudam o integrante destacado. No celular, as fotos viram uma lista vertical com retratos menores e uma foto expandida; nomes permanecem visíveis. O movimento respeita `prefers-reduced-motion`.

A fonte única da equipe é `web/lib/team.ts`: Nathan Borges; Vinícius Stadler Gorov; Antonio Carlos Damante de Souza; Guilherme Henrique de Assis Carvalho. A foto de Nathan foi reaproveitada e as demais foram extraídas das fotos nos screenshots enviados. Apenas os contatos confirmados de Nathan foram mantidos. Os registros acadêmicos foram retirados da interface; funções não informadas foram omitidas. As páginas Sobre e Apresentação reutilizam `TeamSection`. Vídeo e documentos do semestre anterior foram retirados da apresentação atual.

A barra móvel usa `spotlight-button.tsx`, com indicador deslizante e feixe nas cores da marca. As cinco células do participante são Início, Pontos, +/Descartar, Descartes e Conta. O + abre `/descartar`; `/doar` continua compatível. Seleção e posição do destaque derivam da rota real, incluindo detalhes e configurações. As larguras são proporcionais ao espaço disponível. Papéis operacionais e administrador conservam seus atalhos e permissões; a criação de descarte continua exclusiva do participante. Navegação desktop preservada.

A preferência inicial passou a Claro tanto antes da primeira pintura quanto no contexto React. Um sistema operacional escuro não muda esse padrão. Escolhas explícitas salvas de Claro, Escuro ou Sistema continuam respeitadas; Sistema é uma opção voluntária. O identificador antigo de armazenamento foi mantido para preservar escolhas existentes. Sem acesso ao armazenamento, o tema ainda funciona durante a visita. As opções de aparência ficam em uma linha no celular, com contraste revisto no modo escuro.

## Verificação local

- Verificação de tipos e build de produção Next.js: aprovados, 32 rotas.
- Oito casos do script de tema antes da primeira pintura: padrão claro com sistema claro/escuro, escolha explícita clara/escura, Sistema, valor inválido e armazenamento indisponível.
- Contratos da barra: ação central, seleção única em cadastro/alias/rastreio/configurações/pontos e permissões por papel.
- Nove verificações HTTP de integração: aprovadas, incluindo sessão de participante/ponto/operador, detalhe de rastreio, proxy real e código histórico VGO.
- Navegador: fotos carregadas, expansão por clique e teclado; equipe sem excesso de largura em 320 px e desktop; + abre o fluxo real; destaque acompanha a rota; troca para escuro permanece após recarregar; retorno ao claro nas configurações.

Evidências em `output/review/equipe-accordion-*.png` e `output/review/navbar-*.png`. A revisão foi local, sem publicação.

Cópia anterior em `tmp/ecoverse-before-team-navbar.zip`. Relatórios técnicos ficam em `.validation/`, fora do controle de versão.

## Ajuste de conteúdo

Os registros acadêmicos foram removidos da fonte da equipe e do componente. A apresentação não exibe mais vídeo, PDFs nem quadro de tarefas do semestre anterior. O link GitHub abre o perfil de Nathan, sem apresentar o repositório anterior como código do EcoVerse. A seção Sobre e a assinatura das conquistas usam somente EcoVerse. Arquivos de exportação de dados e códigos de recuperação também usam o nome atual. Os arquivos históricos e os identificadores internos de compatibilidade foram preservados.

As dúvidas usam `web/lib/faq.ts`: nove perguntas na home e 21 na central de ajuda. A busca ignora acentuação e permite filtrar por categoria. Conteúdo cobre materiais, entrega no ponto, quantidades, QR, cancelamento, rastreio, pontos, perfil, tema e privacidade.

Validação do ajuste: build Next.js aprovado; verificação HTTP confirmou nove perguntas públicas, equipe sem registros acadêmicos e apresentação sem o vídeo e links de documentos antigos. No navegador, a apresentação foi conferida sem a marca anterior e a central passou por busca sem acento (oleo), filtro QR e rastreio e abertura das respostas. Em 320 px, largura do documento e da área visível ficaram em 305 px, sem excesso horizontal. Captura em `output/review/duvidas-qr-mobile.png`. A aba da home que estava em erro não pôde ser inspecionada pelo controle do navegador; a conferência da home nesta atualização foi por HTTP.

## Equipe completa e indicador sem luz

Lincoln Mariozzi Proença Sobrinho do Prado e Matheus Lisbôa Paludeto completam os seis integrantes. As fotos individuais fornecidas foram copiadas sem alterações; o screenshot com legendas serviu apenas para transcrever os nomes. Não foram copiados telefones nem registros acadêmicos. As páginas Sobre e Apresentação recebem automaticamente os dois integrantes pela mesma fonte.

Removido somente o gradiente de luz sob o indicador da barra. O pequeno retângulo superior, a transição de posição de 400 ms, o + central, os rótulos e as cores de cada tema continuam.

Validação: build aprovado (32 rotas); seis retratos carregados; foco por End seleciona Matheus; nomes longos cabem em 320 px sem excesso horizontal. Nos temas claro e escuro, o pseudo-elemento do feixe não é gerado, o retângulo superior permanece e a posição passa de 90% (Conta) a 50% (+) com transição de 400 ms. O + continua abrindo `/descartar`. Capturas `equipe-seis-integrantes.png` e `navbar-sem-luz-*.png` em `output/review/`.
