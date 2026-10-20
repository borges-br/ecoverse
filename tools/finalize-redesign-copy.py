"""Targeted copy corrections after the EcoVerse domain adaptation."""
from pathlib import Path
import re, zipfile

root = Path(__file__).resolve().parents[1]
def replace(path, pairs):
    file = root / path
    text = file.read_text(encoding='utf-8')
    for old, new in pairs:
        text = text.replace(old, new)
    file.write_text(text, encoding='utf-8')

replace('web/app/layout.tsx', [('#006a62', '#153F35')])
replace('web/components/profile/operational-profile-form.tsx', [
    ('Ex.: Até 100 sacolas por semana', 'Ex.: Limite de recebimento por material'),
    ('Ex.: Entregar roupas limpas e separadas por tipo', 'Ex.: Consultar tipos e embalagens aceitos antes da entrega'),
    ("'Base e área de atendimento'", "'Unidade de recebimento e área de atendimento'"),
    ('Estes dados alimentam o mapa, o detalhe público e a confiança do participante.', 'Informe o endereço do local de recebimento. No perfil de operador, esta unidade é o destino parceiro usado nesta versão.'),
])
replace('web/components/profile/public-profile-hero.tsx', [('label="concluídas"', 'label="concluídos"'), ('label="itens entregues"', 'label="materiais registrados"')])
replace('web/components/dashboard/donor/impact-pills.tsx', [("'peça doada' : 'peças doadas'", "'material registrado' : 'materiais registrados'")])
replace('web/components/dashboard/donor/onboarding-card.tsx', [('Separar peças', 'Separar materiais')])
replace('web/components/dashboard/donor/donor-dashboard-hero.tsx', [('primeira peça registrada', 'primeira entrega registrada')])
replace('web/components/donations/tracking-board.tsx', [('Nenhum descarte encontrada', 'Nenhum descarte encontrado'), ('Esto descarte foi cancelada', 'Este descarte foi cancelado')])
replace('web/components/ui/award-badge.tsx', [("title: 'Primeira Descarte'", "title: 'Primeira entrega'")])
replace('web/app/(app)/rastreio/[id]/page.tsx', [
    ('Destino social será exibido quando o fluxo for vinculado', 'O destino parceiro será exibido após o vínculo operacional'),
    ('Registrada em', 'Registrado em'), ('Descarte não encontrada', 'Descarte não encontrado'),
    ('Seu descarte foi registrada com sucesso.', 'Seu descarte foi registrado com sucesso.'),
    ('Seu descarte entra no fluxo de processamento real. Acompanhe a triagem pelo ponto de coleta\n                e a processamento pelo operador parceiro em tempo real.', 'Apresente seu QR na entrega e acompanhe as etapas registradas pelo ponto e pelo operador parceiro.'),
    ('O rastreio, o dashboard e o perfil agora refletem esta entrega a partir do mesmo\n                  dado persistido.', 'O ponto confirmou o recebimento. As próximas etapas aparecerão conforme a rede atualizar seu registro.'),
    ('Confirmada', 'Confirmado'),
    ('Seu descarte já está pronta para gerar impacto e apoiar famílias atendidas pela rede.', 'Os materiais seguem para as próximas etapas da rede parceira.'),
    ('Vinculada à carga', 'Vinculado à carga'), ('Itens doados', 'Materiais registrados'),
    ('Codigo da doacao', 'Código do descarte'), ('localizar a doacao na operacao', 'localizar o descarte na operação'),
    ('Codigo publico da carga vinculada a sua doacao.', 'Código público da carga vinculada ao seu descarte.'),
])
for path in ['web/components/operations/operational-batches-panel.tsx', 'web/components/dashboard/operational-home-scan-button.tsx']:
    replace(path, [
        ('a doacao', 'o descarte'), ('A doacao', 'O descarte'), ('uma doacao', 'um descarte'),
        ('esta doacao', 'este descarte'), ('doacao adicionada', 'descarte adicionado'),
        ('Localizar doacao', 'Localizar descarte'), ('doacao VGO', 'descarte ECO'),
    ])
replace('web/components/operations/operational-batch-trace-card.tsx', [('{batch.donationCount} descarte(ões), {batch.totalItemQuantity} peça(s)', '{batch.donationCount} descarte(s)')])
replace('web/components/operations/operational-batches-panel.tsx', [('{batch.donationCount} doacao(oes), {batch.totalItemQuantity} peça(s)', '{batch.donationCount} descarte(s)')])
replace('web/app/(app)/admin/campanhas-sazonais/page.tsx', [('categoria de doacao', 'categoria de descarte')])

# New identifiers carry the new brand; old QR codes continue to resolve.
replace('api/src/modules/donations/donations.ts', [('`VGO-${', '`ECO-${')])
replace('api/src/modules/operational-batches/operational-donations.ts', [('^VGO-', '^(?:ECO|VGO)-'), ('Codigo de doacao invalido', 'Código de descarte inválido')])
replace('web/lib/operational-codes.ts', [
    ('^VGO-', '^(?:ECO|VGO)-'), ('codigo VGO ou LOT', 'código ECO, VGO ou LOT'),
    ('Codigo muito longo.', 'Código muito longo.'), ('Codigo nao pode conter espacos internos.', 'O código não pode conter espaços internos.'),
    ('Codigo nao reconhecido. Use VGO-XXXXXX ou LOT-XXXXXX.', 'Código não reconhecido. Use ECO-XXXXXX, VGO-XXXXXX ou LOT-XXXXXX.'),
])
for path in ['web/components/operations/operational-batches-panel.tsx', 'web/components/operations/operational-code-scanner.tsx']:
    replace(path, [('VGO/LOT', 'ECO/VGO/LOT'), ('codigo VGO ou LOT', 'código ECO, VGO ou LOT'), ('Codigo VGO ou LOT', 'Código ECO, VGO ou LOT'), ('VGO-XXXXXX ou LOT-XXXXXX', 'ECO-XXXXXX, VGO-XXXXXX ou LOT-XXXXXX')])
replace('api/src/modules/profiles/profiles.ts', [('`vestgo-meus-dados-', '`ecoverse-meus-dados-')])

# Keep academic artifacts and their actual origin rather than relabeling them.
with zipfile.ZipFile(root/'tmp/ecoverse-before-redesign.zip') as archive:
    name = next(n for n in archive.namelist() if n.endswith('apresentacao/presentation-landing.tsx'))
    original = archive.read(name).decode('utf-8-sig')
    github = re.search(r"github: '(https://github.com/[^']+)'", original).group(1)
replace('web/app/(public)/apresentacao/presentation-landing.tsx', [
    ('https://github.com/borges-br/EcoVerse', github),
    ("description: 'Documento final'", "description: 'Histórico · VestGO'"),
    ("description: 'Versão final do artigo'", "description: 'Histórico · semestre anterior'"),
    ("description: 'Apresentação de 7 min'", "description: 'Histórico · VestGO'"),
    ("description: 'Repositório'", "description: 'Código de origem · VestGO'"),
    ('EcoVerse - Análise e Desenvolvimento de Sistemas 1º Semestre', 'EcoVerse · Projeto UPX / FACENS · evolução do VestGO'),
    ('Assista ao vídeo de 7 minutos apresentando o EcoVerse: nossa proposta, arquitetura, design e o impacto social da nossa plataforma de descartes rastreáveis.', 'Este vídeo apresenta o VestGO, projeto do semestre anterior que deu origem à base técnica do EcoVerse. O vídeo e os documentos desta página são registros históricos.'),
    ('title="EcoVerse - Vídeo Pitch"', 'title="VestGO - Vídeo Pitch histórico"'),
    ('Vídeo de apresentação acadêmica · 7 minutos', 'Histórico do semestre anterior · VestGO · 7 minutos'),
    ('Apoio direto a iniciativas sociais que fortalecem redes de cuidado e assistência.', 'Organização do descarte de materiais que precisam de pontos e condições específicas de recebimento.'),
    ('Conecta participantes, pontos de coleta e Operadores com uma operação mais acessível e transparente.', 'Conecta participantes, pontos de coleta e operadores com informações públicas sobre a rede.'),
    ('Estimula o reaproveitamento e uma logística mais consciente de itens doados.', 'Organiza o recebimento e o transporte de materiais na rede parceira, com etapas registradas.'),
])
print('Targeted interface copy updated; old QR and academic references preserved.')
