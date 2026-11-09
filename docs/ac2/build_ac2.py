"""Gera a documentação da AC2 (UPX II) do EcoVerse em PDF.

Uso: python docs/ac2/build_ac2.py
Saída: docs/ac2/EcoVerse_Documentacao_AC2.pdf
"""
from pathlib import Path
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image, Flowable, CondPageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ASSETS = HERE / 'assets'
TELAS = ASSETS / 'telas'
LOGO = ASSETS / 'facens-logo.png'
PDF = HERE / 'EcoVerse_Documentacao_AC2.pdf'
for name, file in [('Calibri', 'calibri.ttf'), ('Calibri-Bold', 'calibrib.ttf'), ('Calibri-Italic', 'calibrii.ttf')]:
    pdfmetrics.registerFont(TTFont(name, 'C:/Windows/Fonts/' + file))
pdfmetrics.registerFontFamily('Calibri', normal='Calibri', bold='Calibri-Bold', italic='Calibri-Italic', boldItalic='Calibri-Bold')
PAGE = (612, 792)
W = PAGE[0] - 4 * cm
INK = HexColor('#111111')
GRAY = HexColor('#555555')
LINE = HexColor('#d9d9d9')
BLUE = HexColor('#08466f')
LIGHT = HexColor('#9db7c9')
PALE = HexColor('#f2f5f7')
styles = {
    'body': ParagraphStyle('Body', fontName='Calibri', fontSize=11, leading=15, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7),
    'h1': ParagraphStyle('H1', fontName='Calibri-Bold', fontSize=14, leading=20, textColor=black, spaceAfter=10, spaceBefore=6, keepWithNext=True),
    'h2': ParagraphStyle('H2', fontName='Calibri-Bold', fontSize=13, leading=18, textColor=black, spaceBefore=10, spaceAfter=6, keepWithNext=True),
    'small': ParagraphStyle('Small', fontName='Calibri', fontSize=9, leading=12, textColor=GRAY, spaceAfter=6),
    'caption': ParagraphStyle('Caption', fontName='Calibri', fontSize=9, leading=12, textColor=INK, alignment=TA_CENTER, spaceBefore=5, spaceAfter=8),
    'tcap': ParagraphStyle('TCap', fontName='Calibri', fontSize=9, leading=12, textColor=INK, alignment=TA_CENTER, spaceBefore=4, spaceAfter=4),
    'cell': ParagraphStyle('Cell', fontName='Calibri', fontSize=9.5, leading=12.4, textColor=INK),
    'th': ParagraphStyle('TH', fontName='Calibri-Bold', fontSize=9.5, leading=12, textColor=white),
    'center': ParagraphStyle('Center', fontName='Calibri', fontSize=11, leading=15, alignment=TA_CENTER, textColor=INK, spaceAfter=5),
    'title': ParagraphStyle('Title', fontName='Calibri-Bold', fontSize=16, leading=22, alignment=TA_CENTER, textColor=INK, spaceAfter=6),
    'ref': ParagraphStyle('Ref', fontName='Calibri', fontSize=10, leading=13, textColor=INK, spaceAfter=7),
    'toc1': ParagraphStyle('TOC1', fontName='Calibri', fontSize=11, leading=17, leftIndent=0),
    'toc2': ParagraphStyle('TOC2', fontName='Calibri', fontSize=10.5, leading=15, leftIndent=18),
}
story = []
counters = {'fig': 0, 'tab': 0}


def P(text, sty='body'):
    return Paragraph(text, styles[sty])


def p(text, sty='body'):
    story.append(P(text, sty))


def h1(text, new_page=True):
    if new_page:
        story.append(PageBreak())
    else:
        story.append(CondPageBreak(160))
    p(text, 'h1')


def h2(text):
    story.append(CondPageBreak(90))
    p(text, 'h2')


def next_fig(caption):
    counters['fig'] += 1
    return f"Figura {counters['fig']} - {caption}"


def tcap(caption):
    counters['tab'] += 1
    story.append(CondPageBreak(110))
    p(f"Tabela {counters['tab']} - {caption}", 'tcap')


def table(headers, rows, widths=None):
    data = [[P(x, 'th') for x in headers]] + [[P(str(x), 'cell') for x in row] for row in rows]
    widths = [W * x / sum(widths) for x in widths] if widths else [W / len(headers)] * len(headers)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), BLUE), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('GRID', (0, 0), (-1, -1), 0.5, LINE), ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, PALE]), ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7), ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]))
    t.spaceAfter = 8
    story.append(t)


def framed(path, width, height):
    """Imagem com borda fina, ajustada para caber em width x height."""
    im = PILImage.open(path)
    scale = min(width / im.width, height / im.height)
    img = Image(str(path), width=im.width * scale, height=im.height * scale)
    t = Table([[img]], colWidths=[im.width * scale + 2])
    t.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.5, LINE), ('LEFTPADDING', (0, 0), (-1, -1), 1), ('RIGHTPADDING', (0, 0), (-1, -1), 1), ('TOPPADDING', (0, 0), (-1, -1), 1), ('BOTTOMPADDING', (0, 0), (-1, -1), 1)]))
    return t


def fig(path, caption, maxh=260):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    story.append(KeepTogether([framed(path, W, maxh), P(next_fig(caption), 'caption')]))


def fig_pair(items, maxh=200):
    """Duas capturas lado a lado, cada uma com sua legenda numerada."""
    colw = W / 2 - 6
    cells, caps = [], []
    for path, caption in items:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path)
        cells.append(framed(path, colw - 4, maxh))
        caps.append(P(next_fig(caption), 'caption'))
    t = Table([cells, caps], colWidths=[W / 2, W / 2])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3)]))
    story.append(KeepTogether([t]))


def link(label, url):
    return f'<link href="{url}" color="#08466f"><u>{label}</u></link>'


TEAM = [('Nathan Borges', '263944'), ('Vinícius Stadler Gorov', '263317'), ('Antonio Carlos Damante de Souza', '263304'), ('Guilherme Henrique de Assis Carvalho', '264362'), ('Lincoln Mariozzi Proença Sobrinho do Prado', '264303'), ('Matheus Lisbôa Paludeto', '263392')]
BOARD = 'https://trello.com/b/xqoCzfOG/ecoverse'
SITE = 'https://mosfet.com.br'
GIT = 'https://github.com/borges-br/ecoverse'
TITLE = 'EcoVerse - Plataforma de orientação e acompanhamento do descarte responsável'

# Estudo de mercado: mesmo funil apresentado na AC1, sobre a base IBGE 2025.
POP_RMS = 2268579
NET = 0.905
RECICLA = 0.47
ADOCAO = 0.02
TAM = round(POP_RMS * NET)
SAM = round(TAM * RECICLA)
SOM = round(SAM * ADOCAO)


def br(n):
    return f'{n:,}'.replace(',', '.')


class Diagram(Flowable):

    def __init__(self, kind):
        Flowable.__init__(self)
        self.kind = kind
        self.width = W
        self.height = {'flow': 160, 'empathy': 255, 'value': 360, 'lean': 422, 'gantt': 262}[kind]

    def box(self, c, x, y, w, h, title, body, fs=9):
        c.setFillColor(white)
        c.setStrokeColor(LINE)
        c.rect(x, y, w, h, fill=1, stroke=1)
        q = Paragraph('<b>' + title + '</b>' + ('<br/>' + body if body else ''), ParagraphStyle('box', fontName='Calibri', fontSize=fs, leading=fs * 1.25, textColor=INK))
        a, b = q.wrap(w - 16, h - 10)
        if b > h - 10:
            raise ValueError('Diagram overflow ' + title + ' ' + str(b) + '/' + str(h))
        if body:
            q.drawOn(c, x + 8, y + h - 8 - b)
        else:
            q.drawOn(c, x + 8, y + (h - b) / 2)

    def draw(self):
        c = self.canv
        if self.kind == 'flow':
            steps = [('1 Identificar', 'Escolher o material e consultar orientações.'), ('2 Encontrar', 'Buscar ponto compatível com o material.'), ('3 Registrar', 'Entrar na conta e gerar código ou QR.'), ('4 Entregar', 'Ponto confirma o recebimento.'), ('5 Acompanhar', 'Consultar histórico e etapas informadas.')]
            ww = (W - 24) / 3
            for i, (a, b) in enumerate(steps):
                self.box(c, i % 3 * (ww + 12), 84 - i // 3 * 84, ww, 72, a, b, 9.5)
            c.setStrokeColor(GRAY)
            for a, b in [(ww + 1, ww + 11), (2 * ww + 13, 2 * ww + 23)]:
                c.line(a, 120, b, 120)
            self.box(c, 2 * (ww + 12), 0, ww, 72, 'Rede parceira', 'Ponto → retirada → lote → operador. A operação mantém a trilha do material.', 9.5)
        elif self.kind == 'empathy':
            entries = [('Pensa e sente', 'Quer descartar corretamente e transformar o material já separado em uma entrega prática.'), ('Vê', 'Pilhas, baterias e óleo acumulados; informações de descarte espalhadas entre diferentes fontes.'), ('Ouve', 'Orientações sobre preservação ambiental e sobre a necessidade de separar resíduos específicos.'), ('Fala e faz', 'Separa os materiais e procura no aplicativo ou site um local capaz de recebê-los.'), ('Dores', 'Não sabe onde levar cada material e perde tempo buscando pontos compatíveis.'), ('Ganhos', 'Encontra o destino adequado, consulta as regras e conclui o descarte com mais praticidade.')]
            for i, (a, b) in enumerate(entries):
                self.box(c, i % 2 * (W / 2 + 4), 170 - i // 2 * 85, W / 2 - 4, 77, a, b, 10)
        elif self.kind == 'value':
            a = [('Produtos e serviços', 'Busca por material; mapa de pontos; orientações; cadastro de descarte; QR ou código; histórico; ferramentas para pontos e operadores.'), ('Aliviadores de dores', 'Filtrar pelo aceite do ponto; impedir registro incompatível; informar unidades; permitir consulta pública; guardar a confirmação de recebimento.'), ('Criadores de ganhos', 'Reduzir incerteza antes do deslocamento; organizar a entrega; tornar as etapas visíveis; reconhecer a participação após o recebimento.')]
            b = [('Tarefas do participante', 'Separar o material; descobrir onde entregar; preparar o deslocamento; registrar e acompanhar a entrega.'), ('Dores do participante', 'Informação dispersa; dúvidas sobre materiais; deslocamento desperdiçado; falta de retorno sobre a entrega.'), ('Ganhos desejados', 'Encontrar um ponto adequado; concluir com pouco esforço; receber confirmação; consultar o histórico em outro momento.')]
            for i in range(3):
                self.box(c, 0, 240 - i * 120, W / 2 - 7, 110, *a[i], 10)
                self.box(c, W / 2 + 7, 240 - i * 120, W / 2 - 7, 110, *b[i], 10)
        elif self.kind == 'lean':
            cw = W / 5
            costh = 90
            bodyh = 322
            half = bodyh / 2
            self.box(c, 0, costh, cw, bodyh, '1 Problema', 'Descarte adiado.<br/><br/>Aceite e localização pouco claros.<br/><br/>Operação com registros dispersos.<br/><br/><b>Alternativas</b><br/>Busca na web, localizadores setoriais e contato direto.', 9)
            self.box(c, cw, costh + half, cw, half, '4 Solução', 'Busca compatível, orientação, QR e acompanhamento por perfil.', 9)
            self.box(c, cw, costh, cw, half, '8 Métricas', 'Usuários ativos.<br/>Buscas concluídas.<br/>Entregas confirmadas.<br/>Pontos ativos.<br/>Tempo de atendimento.', 9)
            self.box(c, 2 * cw, costh, cw, bodyh, '3 Proposta de valor', 'Encontrar o destino adequado e acompanhar a entrega em uma mesma jornada.<br/><br/>A rede ganha organização do recebimento à retirada.<br/><br/><b>Conceito</b><br/>Orientação e registro de descarte conectados.', 9)
            self.box(c, 3 * cw, costh + half, cw, half, '9 Vantagem', 'Integração entre orientação ao participante, registro da entrega e acompanhamento operacional em uma mesma aplicação.', 9)
            self.box(c, 3 * cw, costh, cw, half, '5 Canais', 'Webapp e landing page; redes sociais; divulgação acadêmica e ações com a rede de coleta.', 9)
            self.box(c, 4 * cw, costh, cw, bodyh, '2 Segmentos', 'Cidadãos que precisam descartar resíduos específicos.<br/><br/>Pontos de coleta, cooperativas e operadores.<br/><br/><b>Implantação</b><br/>Sorocaba, com expansão para os 27 municípios da região metropolitana.', 9)
            self.box(c, 0, 0, 2.5 * cw, costh, '7 Estrutura de custos', 'Hospedagem, domínio, armazenamento, manutenção, suporte e integração da rede de coleta.', 9.5)
            self.box(c, 2.5 * cw, 0, 2.5 * cw, costh, '6 Fontes de receita', 'Acesso gratuito para os participantes. A continuidade considera apoio institucional e parcerias para sustentar infraestrutura e manutenção, preservando a gratuidade.', 9.5)
        elif self.kind == 'gantt':
            # Escala semanal de 03/08 a 30/11/2026; colunas mensais.
            months = [('Agosto', 4), ('Setembro', 4), ('Outubro', 5), ('Novembro', 4)]
            weeks = sum(n for _, n in months)
            lw = W * 0.36
            ww = (W - lw) / weeks
            rh = 28
            top = self.height - 30
            rows = [('Formação do grupo e tema', 1, 3, 1), ('Persona, canvas e mercado', 3, 6, 1), ('Entrega e apresentação AC1', 6, 7, 1), ('Desenvolvimento do webapp', 6, 12, 1), ('Testes e publicação', 11, 12, 1), ('Documentação da AC2', 12, 13, 1), ('Avaliação com usuários (previsto)', 13, 17, 2)]
            self.box(c, 0, top, lw, 30, 'Etapa', '', 9.5)
            x = lw
            for label, n in months:
                self.box(c, x, top, n * ww, 30, label, '', 9.5)
                x += n * ww
            for i, (label, a, b, kind) in enumerate(rows):
                yy = top - (i + 1) * rh
                self.box(c, 0, yy, lw, rh, label, '', 9)
                c.setStrokeColor(LINE)
                c.rect(lw, yy, W - lw, rh, fill=0, stroke=1)
                c.setFillColor(BLUE if kind == 1 else LIGHT)
                c.rect(lw + (a - 1) * ww + 2, yy + 9, (b - a + 1) * ww - 4, rh - 18, fill=1, stroke=0)
            x = lw
            c.setStrokeColor(LINE)
            for _, n in months[:-1]:
                x += n * ww
                c.line(x, top - len(rows) * rh, x, top)


def header_footer(c, doc):
    c.saveState()
    # Cabeçalho do modelo institucional
    logo = PILImage.open(LOGO)
    lh = 26
    lw = lh * logo.width / logo.height
    c.drawImage(str(LOGO), 2 * cm, PAGE[1] - 1.1 * cm - lh, width=lw, height=lh, mask='auto')
    c.setFont('Calibri-Bold', 9)
    c.setFillColor(INK)
    c.drawRightString(PAGE[0] - 2 * cm, PAGE[1] - 1.45 * cm, 'CENTRO UNIVERSITÁRIO FACENS')
    c.setFont('Calibri', 9)
    c.drawRightString(PAGE[0] - 2 * cm, PAGE[1] - 1.85 * cm, 'CST EM ANÁLISE E DESENVOLVIMENTO DE SISTEMAS')
    c.setStrokeColor(GRAY)
    c.setLineWidth(0.6)
    c.line(2 * cm, PAGE[1] - 2.2 * cm, PAGE[0] - 2 * cm, PAGE[1] - 2.2 * cm)
    if doc.page < 3:
        c.setFont('Calibri', 11)
        c.drawCentredString(PAGE[0] / 2, 2.2 * cm, 'Sorocaba/SP')
        c.drawCentredString(PAGE[0] / 2, 1.6 * cm, '2026')
    else:
        c.setFont('Calibri', 9)
        c.setFillColor(GRAY)
        c.drawString(2 * cm, 1.05 * cm, 'EcoVerse | UPX II | AC2 | 2026')
        c.drawRightString(PAGE[0] - 2 * cm, 1.05 * cm, str(doc.page))
    c.restoreState()


class Doc(BaseDocTemplate):

    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='main')
        self.addPageTemplates([PageTemplate(id='page', frames=[frame], onPage=header_footer)])

    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and f.style.name in ('H1', 'H2'):
            level = 0 if f.style.name == 'H1' else 1
            text = f.getPlainText()
            key = 'h%d' % id(f)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=level > 0)
            self.notify('TOCEntry', (level, text, self.page, key))


# Capa
story.append(Spacer(1, 70))
p('<b>Usina de Projetos Experimentais (UPX-2)</b>', 'title')
story.append(Spacer(1, 40))
p('<b>ECOVERSE</b>', 'title')
p('Plataforma de orientação e acompanhamento<br/>do descarte responsável', 'center')
story.append(Spacer(1, 40))
for name, ra in TEAM:
    p(name + ' - RA ' + ra, 'center')
story.append(PageBreak())
# Folha de rosto
story.append(Spacer(1, 10))
p('<b>CENTRO UNIVERSITÁRIO FACENS</b>', 'center')
p('CURSO SUPERIOR TECNÓLOGO EM ANÁLISE E DESENVOLVIMENTO DE SISTEMAS', 'center')
story.append(Spacer(1, 30))
for name, ra in TEAM:
    p(name + ' - RA ' + ra, 'center')
story.append(Spacer(1, 36))
p('<b>ECOVERSE</b>', 'title')
p('Plataforma de orientação e acompanhamento<br/>do descarte responsável', 'center')
story.append(Spacer(1, 30))
q = Table([[P('Segunda parte da documentação do projeto apresentado ao Centro Universitário Facens, como exigência parcial para a composição de nota na Avaliação Continuada 2 (AC2) da disciplina de Usina de Projetos Experimentais II, orientada pela Professora Ma. Cilene Renata Real.', 'body')]], colWidths=[W * 0.58])
q.hAlign = 'RIGHT'
q.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
story.append(q)
# Sumário
story.append(PageBreak())
p('<b>Sumário</b>', 'title')
story.append(Spacer(1, 8))
toc = TableOfContents()
toc.levelStyles = [styles['toc1'], styles['toc2']]
toc.dotsMinLevel = 0
story.append(toc)

h1('1 Informações do Projeto')
p(f'<b>Título do projeto:</b> {TITLE}.<br/><b>Orientadora:</b> Profa. Ma. Cilene Renata Real.<br/><b>Curso:</b> Análise e Desenvolvimento de Sistemas.<br/><b>Disciplina:</b> Usina de Projetos Experimentais II.<br/><b>Período letivo:</b> segundo semestre de 2026.<br/><b>Grupo:</b> MOSFET.')
p('<b>Integrantes:</b> ' + '; '.join(f'{n} (RA {ra})' for n, ra in TEAM) + '.')
p('<b>Tema do semestre:</b> Desenvolvimento Sustentável.<br/><b>Recorte do projeto:</b> orientar o descarte de pilhas, baterias, eletroeletrônicos, lâmpadas e óleo de cozinha, conectar cidadãos a pontos compatíveis e organizar o registro das entregas. A implantação inicial concentra-se em Sorocaba/SP, com expansão prevista para a Região Metropolitana de Sorocaba.')
p('<b>Protótipo publicado:</b> ' + link('mosfet.com.br', SITE) + '<br/><b>Quadro de acompanhamento:</b> ' + link('EcoVerse no Trello', BOARD) + '<br/><b>Código-fonte:</b> ' + link('github.com/borges-br/ecoverse', GIT))

h1('2 Introdução', new_page=False)
p('O descarte de materiais domésticos exige mais do que a intenção de separar resíduos. O morador precisa reconhecer o material, identificar um local que o aceite e compreender como realizar a entrega. Quando essas informações ficam dispersas, a decisão pode ser adiada ou resultar em deslocamento para um ponto incompatível, e materiais potencialmente poluentes acabam direcionados ao lixo comum.')
p('Na primeira etapa da disciplina, o grupo definiu o problema e estruturou a proposta de um guia e mapeamento de logística reversa, com persona, Canvas de Proposta de Valor, Lean Canvas e estudo inicial de mercado. Nesta segunda etapa, a proposta foi concretizada no EcoVerse, uma aplicação web responsiva publicada em domínio próprio.')
p('No EcoVerse, a consulta pública permite buscar pontos de coleta por material; após a autenticação, o participante registra o descarte, gera um código de entrega e acompanha as etapas informadas pela rede. Pontos de coleta e operadores parceiros contam com recursos para recebimento, parcerias, retiradas e lotes. Este documento apresenta os objetivos, a metodologia, o desenvolvimento do protótipo, os modelos de negócio e o planejamento das próximas etapas.')

h1('3 Objetivos')
p('O projeto busca reduzir a distância entre a intenção de descartar corretamente e a execução dessa ação, oferecendo informação confiável sobre onde e como entregar cada material e registrando o caminho percorrido pela entrega.')
h2('3.1 Objetivo Geral')
p('Desenvolver uma plataforma web que facilite o descarte responsável de materiais domésticos, conectando orientação, localização de pontos compatíveis, registro de entregas e acompanhamento das etapas operacionais em uma jornada acessível pelo navegador.')
h2('3.2 Objetivos Específicos')
for t in ['1. Organizar a consulta de pontos por categoria de material e apresentar orientações de descarte sem exigir a criação de conta.', '2. Registrar materiais e quantidades em unidades adequadas, aceitando litros decimais para óleo e quantidades inteiras para materiais contáveis.', '3. Emitir QR ou código consultável que vincule o registro à confirmação de recebimento por um ponto autorizado.', '4. Disponibilizar ao participante o histórico das etapas da entrega e, aos perfis operacionais, recursos de parceria, retirada e lote.', '5. Proteger informações e transições por autenticação e regras de autorização, com persistência em banco de dados relacional.', '6. Verificar as regras de domínio e os fluxos integrados por testes automatizados e preparar a avaliação de usabilidade com participantes e parceiros.', '7. Relacionar a solução ao ODS 12 e acompanhar sua evolução por tarefas, prazos e responsáveis no Trello.']:
    p(t)

h1('4 Justificativa', new_page=False)
p('O Global E-waste Monitor 2024 registra a geração mundial de 62 milhões de toneladas de resíduos eletroeletrônicos em 2022, das quais 22,3% tiveram coleta e reciclagem formalmente documentadas. Esse cenário evidencia a relevância de iniciativas voltadas à orientação do descarte e à organização dos fluxos de recebimento (ITU; UNITAR, 2024).')
p('No âmbito local, a Prefeitura de Sorocaba mantém informações específicas de recebimento e restrições distintas entre seus serviços. Isso reforça a necessidade de conferir o aceite de cada ponto, em vez de presumir que todo local recebe qualquer material. O EcoVerse facilita o acesso a essa informação e organiza o registro da entrega (Sorocaba, s.d.).')
p('A proposta se relaciona ao ODS 12 - Consumo e Produção Responsáveis, especialmente à gestão de resíduos e ao acesso à informação (Nações Unidas Brasil, s.d.). No âmbito acadêmico, o projeto articula análise de requisitos, desenvolvimento de interfaces, banco de dados, redes de computadores e gestão de projetos em torno de uma demanda socioambiental, conforme os objetivos da disciplina.')

story.append(KeepTogether([P('5 Cronograma', 'h1'), P('O projeto teve início com a disciplina de Usina de Projetos Experimentais II, em agosto de 2026. A Figura 1 apresenta as etapas executadas até a AC2 e a etapa prevista na sequência; a Tabela 1 detalha os marcos de cada fase.'), Diagram('gantt'), P(next_fig('Cronograma das atividades do projeto. Barras escuras: etapas realizadas; barra clara: etapa prevista. Fonte: elaboração da equipe.'), 'caption')]))
tcap('Marcos do cronograma.')
table(['Data', 'Etapa', 'Atividades'], [('10/08/2026', 'Formação do grupo', 'Definição dos seis integrantes do grupo MOSFET.'), ('24/08/2026', 'Tema e acompanhamento', 'Criação do quadro no Trello com a orientadora e validação do tema no eixo Desenvolvimento Sustentável.'), ('Ago. a set./2026', 'Concepção', 'Pesquisa documental, persona, Canvas de Proposta de Valor, Lean Canvas e estudo inicial de mercado.'), ('14/09/2026', 'AC1', 'Entrega e apresentação da primeira parte da documentação.'), ('Set. a out./2026', 'Desenvolvimento', 'Implementação da aplicação web, da API, do banco de dados e dos recursos operacionais.'), ('19 e 20/10/2026', 'Verificação e publicação', 'Execução dos testes de domínio e integração e publicação em mosfet.com.br.'), ('25 e 26/10/2026', 'AC2', 'Consolidação da documentação, das capturas do protótipo e do relatório do Trello; entrega em 26/10/2026.'), ('Nov./2026 (previsto)', 'Avaliação', 'Avaliação de usabilidade com participantes, ajustes no protótipo e preparação da entrega final.')], [1.1, 1.15, 2.9])

h1('6 Metodologia')
p('A condução do projeto combina Design Thinking, gestão ágil com quadro Kanban e desenvolvimento incremental. O problema foi decomposto em jornadas, telas, regras de negócio e serviços integrados ao banco de dados, e cada ciclo de implementação foi seguido de verificação técnica.')
h2('6.1 Compreensão do problema e definição do escopo')
p('A etapa de imersão reuniu pesquisa documental sobre descarte e logística reversa e a construção da persona e do mapa de empatia. O escopo abrange pilhas e baterias, eletroeletrônicos, lâmpadas e óleo de cozinha, e considera as necessidades do morador, do ponto de coleta e do operador parceiro. As categorias orientam a consulta, as unidades de medida e a compatibilidade de recebimento. Resíduos de serviços de saúde e perfurocortantes permanecem fora do escopo.')
h2('6.2 Ideação e modelagem do negócio')
p('O Canvas de Proposta de Valor relacionou tarefas, dores e ganhos do participante aos recursos da solução. O Lean Canvas organizou problema, segmentos, canais, custos, métricas e vantagem, e o estudo TAM, SAM e SOM dimensionou o alcance regional. Esses artefatos, apresentados na AC1, orientaram a priorização das funcionalidades do protótipo.')
h2('6.3 Organização do trabalho')
p('O acompanhamento das atividades é feito no Trello, com as listas Tarefas, Em progresso, Pronto e Aprovado. Os cartões reúnem entregas, responsáveis e prazos, e a orientadora participa do quadro. O relatório de atualização é apresentado no Apêndice A.')
h2('6.4 Implementação e controle de versão')
p('A aplicação separa interface web e API, desenvolvidas em TypeScript. O banco de dados evolui por migrações versionadas, o Git registra o histórico do código e a publicação utiliza containers Docker, com pipeline de integração no GitHub Actions. A interface usa componentes compartilhados entre as jornadas de cada perfil.')
h2('6.5 Verificação e validação')
p('A verificação técnica contempla regras de categoria e quantidade, autorização por perfil, compatibilidade dos pontos, persistência de registros, armazenamento de imagens e navegação. Os testes de domínio e integração verificam o comportamento dos serviços. A validação com usuários, prevista para a próxima etapa, avaliará a clareza das telas e a execução das tarefas principais.')
h2('6.6 Integração dos conteúdos do curso')
p('O desenvolvimento articula Engenharia de Software, Banco de Dados e Redes de Computadores. A definição de requisitos orienta as regras da aplicação; a modelagem relacional organiza registros e eventos; a comunicação entre serviços em rede interna e a publicação web com HTTPS aplicam os conceitos de redes ao protótipo.')

h1('7 Equipe do Projeto', new_page=False)
p('O projeto EcoVerse é desenvolvido pelo grupo MOSFET, formado por seis estudantes do curso de Análise e Desenvolvimento de Sistemas do Centro Universitário Facens.')
tcap('Integrantes do grupo.')
table(['Integrante', 'RA'], [(name, ra) for name, ra in TEAM], [4, 1])

h1('8 Desenvolvimento do Projeto')
h2('8.1 Solução e jornada principal')
p('A concepção do EcoVerse parte do guia e mapeamento de logística reversa elaborado na AC1, com foco na localização de pontos e na orientação por material. A versão desenvolvida para a AC2 concretiza essa proposta em um webapp responsivo e acrescenta registro de entregas, confirmação de recebimento e acompanhamento das etapas operacionais.')
story.append(KeepTogether([Diagram('flow'), P(next_fig('Fluxo principal do participante e continuidade na rede parceira. Fonte: elaboração da equipe.'), 'caption')]))
p('A consulta pública identifica pontos compatíveis. A conta permite registrar e acompanhar a entrega. O ponto autorizado confirma o recebimento pelo código ou QR; em seguida, a rede organiza retiradas e lotes com o operador parceiro.')
h2('8.2 Requisitos e regras do domínio')
tcap('Regras de negócio implementadas.')
table(['Regra', 'Comportamento implementado'], [('Categorias', 'Pilhas e baterias; eletroeletrônicos; lâmpadas; óleo de cozinha. Novas entradas em categorias excluídas ou apenas históricas são rejeitadas.'), ('Quantidade', 'Óleo admite litros com até duas casas decimais. Materiais contáveis exigem unidades inteiras e quantidades positivas.'), ('Compatibilidade', 'Todos os materiais do registro devem constar no aceite do ponto. Uma lista de aceite vazia não significa aceite universal.'), ('Confirmação', 'O participante não pode confirmar o próprio recebimento. As transições dependem do perfil e da operação autorizada.'), ('Participação', 'Registro pendente não gera pontos. O recebimento confirmado credita 10 pontos uma única vez, sem bônus por volume.'), ('Histórico', 'Etapas e eventos são mantidos. Litros e unidades não são somados como uma única medida física.')], [1, 3.3])
h2('8.3 Arquitetura e persistência')
p('A interface utiliza Next.js 16, React 19 e TypeScript. A API é desenvolvida com Fastify 5 e Prisma. PostgreSQL com PostGIS mantém os dados da aplicação, incluindo a localização dos pontos, e Redis atende ao estado auxiliar.')
tcap('Camadas da aplicação.')
table(['Camada', 'Responsabilidade', 'Tecnologias'], [('Interface', 'Páginas públicas, sessão, formulários, mapa e painéis por perfil.', 'Next.js, React, TypeScript, Tailwind CSS, Leaflet e Auth.js.'), ('Serviços', 'Autenticação, autorização, registros, recebimentos, parcerias, retiradas e lotes.', 'Fastify, validação de dados e serviços de domínio.'), ('Dados', 'Usuários, materiais, eventos, parceiros, quantidades e trilha operacional.', 'Prisma, PostgreSQL/PostGIS e migrações versionadas.'), ('Estado e arquivos', 'Estado auxiliar e imagens enviadas à aplicação.', 'Redis e volume persistente de uploads da API.'), ('Execução', 'Separação de serviços e publicação web em domínio HTTPS.', 'Docker Compose, GitHub Actions, Portainer e proxy reverso.')], [0.8, 2.3, 1.7])
p('O navegador acessa os serviços pelo caminho /api/backend, no mesmo domínio da aplicação, e a comunicação entre web e API ocorre pela rede interna dos containers. As imagens enviadas ficam em volume persistente vinculado à API.')
h2('8.4 Modelo de dados e perfis')
p('As entidades Donation, DonationItem e DonationEvent representam o registro de descarte, seus itens e seus eventos. OperationalPartnership, PickupRequest e OperationalBatch organizam parcerias, retiradas e lotes. A interface apresenta os perfis Participante, Ponto de coleta, Operador parceiro e Administrador.')
p('O histórico organiza as etapas de registro, recebimento no ponto, transporte e recebimento no destino, sempre a partir dos eventos registrados pela rede. A certificação ambiental de destinação é uma possibilidade de evolução, dependente dos documentos e processos dos operadores.')

h2('8.5 Landing page e consulta pública')
p('A landing page apresenta a proposta e direciona à busca por material. A consulta é pública; o cadastro é exigido apenas para as funções pessoais. As figuras desta seção são capturas da aplicação publicada em mosfet.com.br, realizadas em 25/10/2026. Os pontos exibidos são cadastros de demonstração do ambiente de testes.')
fig(TELAS / '01-landing.png', 'Landing page do EcoVerse, com acesso direto à busca de pontos de descarte.', 235)
fig(TELAS / '02-busca.png', 'Seleção do material e busca por pontos na página inicial.', 235)
fig(TELAS / '03-mapa-demo.png', 'Mapa de pontos de coleta com filtro de eletrônicos em Sorocaba.', 235)
h2('8.6 Acesso à conta e registro de descarte')
p('O participante cria a conta e acessa seu painel, de onde inicia o registro. O fluxo de registro tem três passos: escolha dos materiais e quantidades, escolha de um ponto compatível e revisão. Ao final, a aplicação gera o QR e o código da entrega.')
fig_pair([(TELAS / '04-login.png', 'Tela de entrada na conta.'), (TELAS / '05-cadastro.png', 'Cadastro de participante.')], 150)
fig_pair([(TELAS / '07-painel.png', 'Painel inicial do participante.'), (TELAS / '08-materiais-inteiro.png', 'Passo 1: materiais e quantidades.')], 175)
fig_pair([(TELAS / '09-ponto-inteiro.png', 'Passo 2: escolha do ponto compatível.'), (TELAS / '10-revisao-inteira.png', 'Passo 3: revisão da entrega.')], 215)
h2('8.7 Confirmação e acompanhamento da entrega')
p('Com o código ou QR, o ponto de coleta confirma o recebimento. O participante acompanha as etapas seguintes, registradas pelo ponto e pelo operador parceiro, até o recebimento no destino.')
fig_pair([(TELAS / '11-qr-gerado.png', 'Descarte registrado, com QR e código de entrega.'), (TELAS / '12-aguardando.png', 'Acompanhamento: aguardando entrega.')], 175)
fig_pair([(TELAS / '13-no-ponto.png', 'Acompanhamento: material recebido no ponto.'), (TELAS / '14-destino.png', 'Acompanhamento: recebido no destino.')], 175)

h2('8.8 Estágio do protótipo')
p('A Tabela 5 resume as funcionalidades disponíveis na versão publicada e as que compõem a próxima etapa do projeto.')
tcap('Funcionalidades do protótipo.')
table(['Funcionalidade', 'Situação'], [('Landing page, orientações por material e consulta pública de pontos', 'Implementada'), ('Mapa com filtro por material, página do ponto e rota em serviço de mapas', 'Implementada'), ('Cadastro, login, confirmação de e-mail e recuperação de senha', 'Implementada'), ('Registro de descarte com materiais, quantidades e ponto compatível', 'Implementada'), ('QR e código de entrega; confirmação de recebimento pelo ponto', 'Implementada'), ('Histórico de etapas, notificações e pontos de participação', 'Implementada'), ('Painéis operacionais: parcerias, retiradas, lotes e administração de perfis', 'Implementada'), ('Avaliação de usabilidade com participantes e pontos de coleta', 'Próxima etapa'), ('Avaliações, comentários e sugestão colaborativa de novos pontos', 'Próxima etapa'), ('Uso de câmera e localização em dispositivos móveis', 'Próxima etapa')], [3.6, 1])
h2('8.9 Testes e verificação técnica')
p('A verificação técnica foi organizada em testes de domínio, testes de integração e conferência da publicação.')
tcap('Testes executados.')
table(['Data e ambiente', 'Resultado', 'Alcance'], [('19/10 - ambiente local isolado', '5 testes de domínio, 17 verificações integradas e 9 verificações HTTP aprovados.', 'Regras de materiais e quantidades, perfis, QR, recebimento e transporte; páginas e proxy.'), ('20/10 - teste de versão isolado', '18 verificações integradas aprovadas.', 'Sessões por perfil, busca, litros, permissões, uploads, 20 migrações, recuperação após falha e persistência após reinício.'), ('20/10 - domínio publicado', '8 verificações aprovadas.', 'HTTPS, prontidão, autenticação administrativa, upload e leitura de imagens, páginas protegidas, busca pública e redirecionamento www.')], [1.1, 1.8, 2.2])
p('Fonte: relatórios de testes do projeto EcoVerse, 19 e 20 de outubro de 2026.', 'small')

h1('9 Resultados Esperados')
p('Espera-se que o participante encontre um ponto compatível, registre sua entrega e acompanhe as etapas de recebimento com menos incerteza e menos deslocamentos desnecessários. Para a rede de coleta, espera-se organizar os registros de entrada, as retiradas e a formação de lotes. A contribuição social pretendida é ampliar o acesso à informação sobre descarte responsável e reduzir o volume de materiais destinados ao lixo comum.')
tcap('Indicadores de resultado.')
table(['Dimensão', 'Indicador proposto', 'Como verificar'], [('Descoberta', 'Pessoas que encontram um ponto compatível sem ajuda.', 'Teste de usabilidade com tarefas de busca e registro; tempo, dúvidas e conclusão.'), ('Conversão', 'Entregas confirmadas em relação aos registros criados.', 'Apuração por período, com classificação de abandono e cancelamento.'), ('Confiabilidade', 'Registros com histórico coerente e sem confirmação indevida.', 'Roteiro de teste por perfil e conferência dos eventos persistidos.'), ('Operação', 'Tempo entre a entrada no ponto e a retirada pelo operador.', 'Comparação entre as datas dos eventos de recebimento e retirada.'), ('Rede', 'Pontos com aceite, contato e situação revisados.', 'Revisão periódica do cadastro junto a cada ponto.'), ('Impacto', 'Quantidade recebida por material e unidade.', 'Totais separados por material e unidade de medida.')], [0.85, 1.8, 2.45])
h2('9.1 Critérios para o piloto')
p('O piloto prevê uma rede local de pontos e operadores em Sorocaba, com conferência das condições de recebimento. A avaliação percorrerá seleção do material, busca, compreensão das orientações, registro, confirmação e consulta do histórico, e as dificuldades observadas serão priorizadas por frequência e impacto na conclusão das tarefas.')

h1('10 Persona')
p('<b>Rafael Brandão, 20 anos, desenvolvedor júnior, residente em Santa Rita do Sapucaí/MG.</b> Acumula pilhas, baterias e óleo em casa por não saber onde realizar o descarte. Sua principal necessidade é encontrar rapidamente, em um aplicativo ou site, o local adequado para cada material. Frase representativa: “Eu separo certinho, só não sei pra onde levar.”')
p('A persona representa o cidadão que já separa os materiais, mas encontra dificuldade para localizar o destino adequado. O perfil orienta a linguagem, a organização das categorias, a busca geográfica e a apresentação das informações dos pontos.')
tcap('Caracterização da persona.')
table(['Aspecto', 'Caracterização e implicação para o produto'], [('Objetivo', 'Encontrar rapidamente onde descartar cada material.'), ('Dificuldade', 'Informações dispersas e dúvida sobre o aceite dos pontos.'), ('Comportamento', 'Separa pilhas, baterias e óleo, mas mantém esses materiais em casa por falta de orientação.'), ('Necessidade', 'Mapa, filtros por categoria e informações claras sobre o local de entrega.'), ('Decisão de interface', 'Consulta pública, sem cadastro, e busca por material simples e direta.')], [1, 3.5])
h2('10.1 Mapa de Empatia')
story.append(KeepTogether([Diagram('empathy'), P(next_fig('Mapa de empatia da persona. Fonte: elaboração da equipe.'), 'caption')]))
h2('10.2 Jornada do Usuário')
p('A jornada relaciona a necessidade do participante, suas ações e as respostas oferecidas pelo produto, da identificação do material à consulta das etapas posteriores à entrega.')
tcap('Jornada do participante.')
table(['Etapa', 'Ação e necessidade', 'Dificuldade provável', 'Resposta do EcoVerse'], [('1 Perceber', 'Identifica material guardado e decide descartar.', 'Dúvida sobre o tipo e o preparo.', 'Página pública com materiais e explicação do processo.'), ('2 Encontrar', 'Busca um local viável no trajeto.', 'Informação dispersa ou ponto incompatível.', 'Filtro por material, mapa e aceite de cada ponto.'), ('3 Preparar', 'Escolhe o ponto e registra a entrega.', 'Formulário longo ou unidades confusas.', 'Registro em três passos, com unidade adequada a cada material.'), ('4 Entregar', 'Apresenta o material e o código ao ponto.', 'Receio de não haver confirmação.', 'O ponto registra o recebimento pelo QR ou código.'), ('5 Acompanhar', 'Consulta o andamento após a entrega.', 'Falta de retorno sobre o destino do material.', 'Histórico das etapas registradas pela rede.')], [0.8, 1.45, 1.45, 1.65])
p('Na próxima etapa, a jornada será avaliada com participantes em teste de usabilidade, considerando tempo de execução, dificuldades de navegação e compreensão das informações em cada etapa.')

h1('11 Canvas de Proposta de Valor')
p('O Canvas de Proposta de Valor relaciona as necessidades do participante aos recursos do EcoVerse. O mapa de valor reúne a oferta da solução; o perfil do cliente descreve tarefas, dores e ganhos.')
story.append(KeepTogether([Diagram('value'), P(next_fig('Canvas de Proposta de Valor. Esquerda: mapa de valor. Direita: perfil do cliente. Fonte: elaboração da equipe.'), 'caption')]))
p('A busca por compatibilidade responde à necessidade de encontrar um local adequado. O registro e o código organizam a entrega, e a confirmação e o histórico dão retorno ao participante. Para pontos e operadores, a solução centraliza recebimentos, retiradas e lotes, permitindo acompanhar a movimentação dos materiais ao longo da operação.')

h1('12 Lean Canvas')
p('O Lean Canvas apresenta o modelo de uma iniciativa gratuita de impacto socioambiental, que integra orientação ao participante e organização da rede de coleta.')
story.append(KeepTogether([Diagram('lean'), P(next_fig('Lean Canvas do EcoVerse. Fonte: elaboração da equipe.'), 'caption')]))
p('A estratégia inicial concentra-se em uma rede local com informações de aceite atualizadas e acompanhamento das entregas. A integração entre consulta pública e operação é o diferencial em relação às soluções centradas apenas na localização de pontos. O uso é gratuito, e a continuidade considera apoio institucional e parcerias para custear infraestrutura e manutenção.')

h1('13 Estudo de Mercado (TAM, SAM, SOM)')
h2('13.1 Segmentos e alternativas')
p('O público principal é formado por cidadãos que precisam de orientação prática para descartar pilhas, baterias, eletroeletrônicos, lâmpadas e óleo de cozinha. Pontos de coleta, ecopontos, cooperativas e operadores compõem a rede de atendimento; universidades, governos locais e organizações ambientais são canais de articulação e divulgação.')
tcap('Alternativas disponíveis ao público.')
table(['Alternativa', 'Oferta', 'Relação com o EcoVerse'], [('Green Eletron', 'Consulta de locais e orientações para descarte de eletroeletrônicos e pilhas.', 'Referência para informações específicas por categoria.'), ('Reciclus', 'Localização de pontos de entrega de lâmpadas.', 'Evidencia a necessidade de informar o aceite e as regras de cada ponto.'), ('Serviços municipais', 'Informações sobre ecopontos e recebimento em Sorocaba.', 'Compõem o contexto local de orientação sobre descarte.'), ('Busca e contato direto', 'Pesquisa em sites, mapas e contato com estabelecimentos.', 'Oportunidade de reunir consulta, orientação e acompanhamento em uma jornada.')], [1, 2, 2.15])
h2('13.2 Dimensionamento')
p(f'O recorte geográfico é a Região Metropolitana de Sorocaba, formada por 27 municípios e com {br(POP_RMS)} habitantes estimados pelo IBGE para 2025, com implantação inicial no município de Sorocaba ({br(762172)} habitantes). O dimensionamento segue o funil definido na AC1. O TAM aplica à população regional a proporção de usuários de internet apurada pela PNAD Contínua TIC 2025 (90,5%). O SAM aplica a proporção de entrevistados que declaram sempre separar materiais para reciclagem em casa (47%, pesquisa CNI/Nexus). O SOM corresponde à meta de alcançar 2% do SAM no primeiro ano, começando por Sorocaba (IBGE, 2025; IBGE, 2026; CNI; Nexus, 2024).')
tcap('Dimensionamento do mercado do EcoVerse.')
table(['Indicador', 'Definição', 'Cálculo', 'Estimativa'], [('TAM', 'População da Região Metropolitana de Sorocaba com acesso à internet.', f'{br(POP_RMS)} × 90,5%', f'{br(TAM)} pessoas'), ('SAM', 'Parcela que já separa materiais para reciclagem e tem maior aderência ao problema.', f'{br(TAM)} × 47%', f'{br(SAM)} pessoas'), ('SOM', 'Meta de usuários no primeiro ano, a partir de Sorocaba.', f'{br(SAM)} × 2%', f'{br(SOM)} usuários')], [0.6, 2.2, 1.35, 1.15])
p('Fonte: IBGE; CNI/Nexus; elaboração da equipe.', 'small')
p('Os percentuais de internet e de separação de recicláveis são nacionais e foram aplicados à população regional como aproximação. Como o acesso ao EcoVerse é gratuito, o dimensionamento é expresso em pessoas alcançáveis, sem conversão em faturamento. O SOM é uma meta de planejamento, a ser comparada com o uso observado após a implantação.')
h2('13.3 Implantação e acompanhamento')
p('A implantação começa em Sorocaba, com a organização dos pontos de coleta e a conferência dos materiais aceitos. A ampliação para os demais municípios considera a qualidade das informações, a capacidade de atendimento e a continuidade da operação. O acompanhamento contempla usuários ativos mensais, buscas concluídas, registros de descarte, entregas confirmadas e pontos ativos.')

h1('14 Conclusão')
p('O desenvolvimento do EcoVerse resultou em uma aplicação web publicada que integra orientação, localização de pontos e registro de descarte. A organização por perfis distingue as responsabilidades de participantes, pontos e operadores, e as regras de material, quantidade e autorização estruturam a jornada digital.')
p('A passagem da proposta da AC1, centrada no mapeamento de pontos, para um protótipo que também registra e acompanha a entrega exigiu modelar eventos, permissões e unidades de medida com cuidado. Os testes de domínio e integração verificaram esses comportamentos centrais e a persistência dos dados, e a publicação em domínio próprio permitiu aplicar na prática os conceitos de redes e implantação.')
p('A continuidade do projeto concentra-se na avaliação da experiência de uso, na implantação da rede de parceiros em Sorocaba e no aperfeiçoamento do acompanhamento das entregas, etapas que verificarão se a solução reduz de fato o tempo e a incerteza envolvidos no descarte responsável.')

h1('15 Estudos Futuros', new_page=False)
tcap('Melhorias e estudos previstos.')
table(['Prioridade', 'Estudo ou melhoria', 'Benefício esperado'], [('1', 'Piloto com usuários e pontos de coleta', 'Avaliar a busca por material, a compreensão das etapas e o funcionamento da rede.'), ('1', 'Qualidade da informação', 'Revisar periodicamente aceite, contato, horários e disponibilidade dos pontos.'), ('1', 'Acessibilidade e dispositivos móveis', 'Avaliar teclado, leitor de tela, conexão móvel, câmera e localização.'), ('2', 'Participação colaborativa', 'Permitir avaliações, comentários e sugestão de pontos, com critérios de moderação.'), ('2', 'Aplicativo mobile', 'Avaliar uma versão distribuída em lojas de aplicativos, conforme o uso do webapp.'), ('2', 'Expansão regional', 'Ampliar a cobertura na Região Metropolitana de Sorocaba, preservando o acesso gratuito.')], [0.6, 1.5, 2.5])
p('No futuro, a plataforma poderá emitir comprovantes de destinação a partir dos documentos dos operadores e oferecer relatórios agregados a prefeituras e cooperativas, apoiando o planejamento da logística reversa local.')

h1('16 Referências Bibliográficas')
refs = [('CNI; NEXUS.', 'Sustentabilidade e opinião pública. Brasília: Confederação Nacional da Indústria, set. 2024. Disponível em: ' + link('portaldaindustria.com.br', 'https://static.portaldaindustria.com.br/portaldaindustria/noticias/media/filer_public/c0/3a/c03a0890-d087-4a51-acc3-7c6a6bb6ae75/opiniao_publica_e_sustentabilidade.pdf') + '. Acesso em: 25 out. 2026.'),
        ('EQUIPE ECOVERSE.', 'EcoVerse: código-fonte e documentação técnica. 2026. Disponível em: ' + link('github.com/borges-br/ecoverse', GIT) + '. Acesso em: 25 out. 2026.'),
        ('EQUIPE ECOVERSE.', 'Quadro EcoVerse. Trello, 2026. Disponível em: ' + link('trello.com/b/xqoCzfOG/ecoverse', BOARD) + '. Acesso em: 25 out. 2026.'),
        ('EQUIPE MOSFET.', 'Guia e Mapeamento de Logística Reversa: documentação escrita completa (AC1). Sorocaba: Centro Universitário Facens, set. 2026.'),
        ('FACENS.', 'UPXII - Usina de Projetos Experimentais II: plano de ensino. Tecnologia em Análise e Desenvolvimento de Sistemas. Sorocaba: Centro Universitário Facens, 2025.'),
        ('GREEN ELETRON.', 'Perguntas frequentes. [s.d.]. Disponível em: ' + link('greeneletron.org.br', 'https://greeneletron.org.br/perguntas-frequentes/') + '. Acesso em: 25 out. 2026.'),
        ('IBGE.', 'Estimativas da população 2025: regiões metropolitanas. Rio de Janeiro: IBGE, 2025. Disponível em: ' + link('agenciadenoticias.ibge.gov.br', 'https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/8383bdedce5a6d972e60dd32671e533a.pdf') + '. Acesso em: 25 out. 2026.'),
        ('IBGE.', 'Proporção de usuários da internet no país ultrapassou 90% da população de 10 anos ou mais em 2025. Agência IBGE Notícias, 2026. Disponível em: ' + link('agenciadenoticias.ibge.gov.br', 'https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/47408-proporcao-de-usuarios-da-internet-no-pais-ultrapassou-90-da-populacao-de-10-anos-ou-mais-em-2025') + '. Acesso em: 25 out. 2026.'),
        ('ITU; UNITAR.', 'The Global E-waste Monitor 2024. Genebra: ITU; Bonn: UNITAR, 2024. Disponível em: ' + link('itu.int', 'https://www.itu.int/en/ITU-D/Environment/Pages/Publications/The-Global-E-waste-Monitor-2024.aspx') + '. Acesso em: 25 out. 2026.'),
        ('LEANSTACK.', 'Lean Canvas. [s.d.]. Disponível em: ' + link('leanstack.com', 'https://leanstack.com/lean-canvas') + '. Acesso em: 25 out. 2026.'),
        ('NAÇÕES UNIDAS BRASIL.', 'Objetivo de Desenvolvimento Sustentável 12: consumo e produção responsáveis. [s.d.]. Disponível em: ' + link('brasil.un.org', 'https://brasil.un.org/pt-br/sdgs/12') + '. Acesso em: 25 out. 2026.'),
        ('RECICLUS.', 'Onde descartar. [s.d.]. Disponível em: ' + link('reciclus.org.br', 'https://reciclus.org.br/onde-descartar/') + '. Acesso em: 25 out. 2026.'),
        ('SOROCABA. Prefeitura Municipal.', 'Educação ambiental: lixo eletrônico. [s.d.]. Disponível em: ' + link('meioambiente.sorocaba.sp.gov.br', 'https://meioambiente.sorocaba.sp.gov.br/educacaoambiental/lixo-eletronico/') + '. Acesso em: 25 out. 2026.'),
        ('SOROCABA. Prefeitura Municipal.', 'Governo municipal. [s.d.]. Disponível em: ' + link('sorocaba.sp.gov.br', 'https://www.sorocaba.sp.gov.br/governo-municipal/') + '. Acesso em: 25 out. 2026.'),
        ('SOROCABA. Prefeitura Municipal.', 'Portal 156: carta de serviço - ecopontos. [s.d.]. Disponível em: ' + link('portal156.sorocaba.sp.gov.br', 'https://portal156.sorocaba.sp.gov.br/portal156/carta-servico/assunto/C4F424F3-02B9-E411-9E1C-005056BF74CB/') + '. Acesso em: 25 out. 2026.'),
        ('STRATEGYZER.', 'The Value Proposition Canvas. [s.d.]. Disponível em: ' + link('strategyzer.com', 'https://www.strategyzer.com/library/the-value-proposition-canvas') + '. Acesso em: 25 out. 2026.')]
for a, b in refs:
    p('<b>' + a + '</b> ' + b, 'ref')
story.append(Spacer(1, 14))
sig = Table([[P('Data da entrega: 26/10/2026', 'center')], [Spacer(1, 22)], [P('_________________________________', 'center')], [P('Professora Cilene Renata Real<br/>Orientadora do Projeto', 'center')]], colWidths=[W])
story.append(KeepTogether([sig]))

h1('Apêndice A - Relatório de Atualização do Trello')
p('<b>Quadro:</b> EcoVerse.<br/><b>Data de referência:</b> 25/10/2026.<br/><b>Link:</b> ' + link(BOARD.replace('https://', ''), BOARD) + '.')
p('O quadro reúne os seis integrantes e a orientadora e organiza as entregas acadêmicas e técnicas em quatro listas. Cada cartão tem prazo e integrante responsável, indicados pelo avatar no cartão.')
tcap('Situação das listas do quadro.')
table(['Lista', 'Cartões'], [('Tarefas (3)', 'Apresentação/Pitch; Banner digital; Artigo acadêmico.'), ('Em progresso (3)', 'Tarefa principal - Projeto funcional 70% (26/10); Entrega do Trello parcial com print e link (28/10); Entrega das telas reais ou Figma e landing page (28/10).'), ('Pronto (7)', 'Entrega das telas reais (dois cartões); GitHub; Figma; Landing page; Integração com banco de dados, armazenamento e Redis; Ferramentas utilizadas.'), ('Aprovado', 'Nome do projeto; Distribuição das tarefas; Persona; Canvas; Lean Canvas e modelo de negócios; Documentação; Pesquisa.')], [1.1, 4])
p('Os cartões aprovados correspondem aos artefatos da AC1. Os cartões em Pronto reúnem os componentes do protótipo concluídos em outubro, e os cartões em progresso correspondem às entregas da AC2. As tarefas de apresentação, banner e artigo seguem para a etapa final da disciplina.')
fig(ASSETS / 'trello-membros.png', 'Membros do quadro: integrantes do grupo e orientadora, em 25/10/2026.', 230)
fig(ASSETS / 'trello-quadro.png', 'Quadro EcoVerse no Trello, com as listas Tarefas, Em progresso, Pronto e Aprovado, em 25/10/2026.', 540)

doc = Doc(str(PDF), pagesize=PAGE, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=3 * cm, bottomMargin=2 * cm, title='EcoVerse - Documentação do Projeto (AC2)', author='Grupo MOSFET', subject='UPX II - Facens - AC2 - 2026')
doc.multiBuild(story)

r = PdfReader(PDF)
text = '\n'.join((pg.extract_text() or '' for pg in r.pages))
required = ['Sumário', 'Informações do Projeto', 'Introdução', 'Objetivo Geral', 'Objetivos Específicos', 'Justificativa', 'Cronograma', 'Metodologia', 'Equipe do Projeto', 'Desenvolvimento do Projeto', 'Resultados Esperados', 'Persona', 'Mapa de Empatia', 'Jornada do Usuário', 'Canvas de Proposta de Valor', 'Lean Canvas', 'Estudo de Mercado', 'Conclusão', 'Estudos Futuros', 'Referências Bibliográficas', 'Trello']
missing = [a for a in required if a not in text]
assert not missing, missing
assert all((ra in text and n in text for n, ra in TEAM))
banned = ['Insira aqui', 'RA123456', 'Escreva aqui', 'Lorem ipsum', 'placeholder', 'a confirmar', 'TODO']
assert not [b for b in banned if b in text], [b for b in banned if b in text]
links = []
for i, pg in enumerate(r.pages):
    for a in pg.get('/Annots', []):
        an = a.get_object()
        dest = an.get('/A', {}).get('/URI')
        if dest:
            links.append({'page': i + 1, 'url': str(dest)})
manifest = {'pdf': PDF.name, 'pages': len(r.pages), 'figures': counters['fig'], 'tables': counters['tab'], 'market': {'TAM': TAM, 'SAM': SAM, 'SOM': SOM}, 'team': TEAM, 'links': links, 'bytes': PDF.stat().st_size}
(HERE / 'validation.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: manifest[k] for k in ('pages', 'figures', 'tables', 'market', 'bytes')}, ensure_ascii=False))
