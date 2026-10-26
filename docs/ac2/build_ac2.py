from pathlib import Path
from hashlib import sha256
import json, math, sys, os
sys.stdout.reconfigure(encoding='utf-8')
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from pypdf import PdfReader
HERE = Path(__file__).resolve().parent
ASSETS = HERE / 'assets'
TELAS = ASSETS / 'telas'
TEMPLATE = Path('C:/Users/natha/Downloads/Modelo Documentação.docx')
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
PALE = HexColor('#f2f5f7')
styles = {'body': ParagraphStyle('Body', fontName='Calibri', fontSize=11, leading=14.5, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7), 'h1': ParagraphStyle('H1', fontName='Calibri-Bold', fontSize=14, leading=20, textColor=black, spaceAfter=12, spaceBefore=3, keepWithNext=True), 'h2': ParagraphStyle('H2', fontName='Calibri-Bold', fontSize=13, leading=18, textColor=black, spaceBefore=10, spaceAfter=7, keepWithNext=True), 'small': ParagraphStyle('Small', fontName='Calibri', fontSize=9, leading=12, textColor=GRAY, spaceAfter=6), 'caption': ParagraphStyle('Caption', fontName='Calibri', fontSize=9, leading=12, textColor=INK, alignment=TA_CENTER, spaceBefore=6, spaceAfter=8), 'cell': ParagraphStyle('Cell', fontName='Calibri', fontSize=9.5, leading=12.4, textColor=INK), 'cellsmall': ParagraphStyle('CellSmall', fontName='Calibri', fontSize=9, leading=11.5, textColor=INK), 'th': ParagraphStyle('TH', fontName='Calibri-Bold', fontSize=9.5, leading=12, textColor=white), 'center': ParagraphStyle('Center', fontName='Calibri', fontSize=11, leading=15, alignment=TA_CENTER, textColor=INK, spaceAfter=6), 'ref': ParagraphStyle('Ref', fontName='Calibri', fontSize=9.5, leading=12.5, textColor=INK, spaceAfter=7)}
story = []
page_titles = []

def P(text, sty='body'):
    return Paragraph(text, styles[sty])

def p(text, sty='body'):
    story.append(P(text, sty))

def h(text, level=2):
    p(text, 'h1' if level == 1 else 'h2')

def page(title):
    if story:
        story.append(PageBreak())
    page_titles.append(title)
    h(title, 1)

def table(headers, rows, widths=None, small=False):
    data = [[P(x, 'th') for x in headers]] + [[P(str(x), 'cellsmall' if small else 'cell') for x in row] for row in rows]
    widths = [W * x / sum(widths) for x in widths] if widths else [W / len(headers)] * len(headers)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), BLUE), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('GRID', (0, 0), (-1, -1), 0.5, LINE), ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, PALE]), ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
    t.spaceAfter = 8
    story.append(t)

def fig(path, caption, maxh=320):
    path = Path(path)
    if not path.exists():
        return
    im = PILImage.open(path)
    iw, ih = im.size
    scale = min(W / iw, maxh / ih)
    story.append(KeepTogether([Image(str(path), width=iw * scale, height=ih * scale), P(caption, 'caption')]))

def link(label, url):
    return f'<link href="{url}" color="#08466f"><u>{label}</u></link>'
TEAM = [('Nathan Borges', '263944'), ('Vinícius Stadler Gorov', '263317'), ('Antonio Carlos Damante de Souza', '263304'), ('Guilherme Henrique de Assis Carvalho', '264362'), ('Lincoln Mariozzi Proença Sobrinho do Prado', '264303'), ('Matheus Lisbôa Paludeto', '263392')]
BOARD = 'https://trello.com/b/xqoCzfOG/ecoverse'
SITE = 'https://mosfet.com.br'
GIT = 'https://github.com/borges-br/ecoverse'

class Diagram(Flowable):

    def __init__(self, kind):
        Flowable.__init__(self)
        self.kind = kind
        self.width = W
        self.height = {'flow': 160, 'empathy': 255, 'value': 360, 'lean': 422, 'gantt': 205}[kind]

    def box(self, c, x, y, w, h, title, body, fs=9):
        c.setFillColor(white)
        c.setStrokeColor(LINE)
        c.rect(x, y, w, h, fill=1, stroke=1)
        q = Paragraph('<b>' + title + '</b><br/>' + body, ParagraphStyle('box', fontName='Calibri', fontSize=fs, leading=fs * 1.25, textColor=INK))
        a, b = q.wrap(w - 16, h - 14)
        if b > h - 14:
            raise ValueError('Diagram overflow ' + title + ' ' + str(b) + '/' + str(h))
        q.drawOn(c, x + 8, y + h - 8 - b)

    def draw(self):
        c = self.canv
        if self.kind == 'flow':
            steps = [('1 Identificar', 'Escolher o material e consultar orientações.'), ('2 Encontrar', 'Buscar ponto compatível com o material.'), ('3 Registrar', 'Entrar na conta e gerar código ou QR.'), ('4 Entregar', 'Ponto confirma o recebimento.'), ('5 Acompanhar', 'Consultar histórico e etapas informadas.')]
            ww = (W - 24) / 3
            for i, (a, b) in enumerate(steps):
                row = i // 3
                col = i % 3
                self.box(c, col * (ww + 12), 84 - row * 84, ww, 72, a, b, 9.5)
            c.setStrokeColor(GRAY)
            for a, b in [(ww + 1, ww + 11), (2 * ww + 13, 2 * ww + 23)]:
                c.line(a, 120, b, 120)
            self.box(c, 2 * (ww + 12), 0, ww, 72, 'Rede parceira', 'Ponto → retirada → lote → operador. A operação mantém a trilha do material.', 9.5)
        elif self.kind == 'empathy':
            entries = [('Pensa e sente', 'Quer descartar corretamente e transformar o material já separado em uma entrega prática.'), ('Vê', 'Pilhas, baterias e óleo acumulados; informações de descarte espalhadas entre diferentes fontes.'), ('Ouve', 'Orientações sobre preservação ambiental e sobre a necessidade de separar resíduos específicos.'), ('Fala e faz', 'Separa os materiais e procura no aplicativo ou site um local capaz de recebê-los.'), ('Dores', 'Não sabe onde levar cada material e perde tempo buscando pontos compatíveis.'), ('Ganhos', 'Encontra o destino adequado, consulta as regras e conclui o descarte com mais praticidade.')]
            for i, (a, b) in enumerate(entries):
                self.box(c, i % 2 * (W / 2 + 4), 170 - i // 2 * 85, W / 2 - 4, 77, a, b, 10)
        elif self.kind == 'value':
            a = [('Produtos e serviços', 'Busca por material; mapa de pontos; orientações; cadastro de descarte; QR ou código; histórico; ferramentas para pontos e operadores.'), ('Aliviadores de dores', 'Filtrar pelo aceite do ponto; impedir registro incompatível; informar unidades; permitir consulta pública; guardar a confirmação de recebimento.'), ('Criadores de ganhos', 'Reduzir incerteza antes da viagem; organizar a entrega; tornar as etapas visíveis; reconhecer participação após recebimento.')]
            b = [('Tarefas do participante', 'Separar o material; descobrir onde entregar; preparar o deslocamento; registrar e acompanhar a entrega.'), ('Dores do participante', 'Informação dispersa; dúvidas sobre materiais; deslocamento desperdiçado; falta de retorno sobre a entrega.'), ('Ganhos desejados', 'Encontrar um ponto adequado; concluir com pouco esforço; receber confirmação; consultar o histórico em outro momento.')]
            for i in range(3):
                self.box(c, 0, 240 - i * 120, W / 2 - 7, 110, *a[i], 10)
                self.box(c, W / 2 + 7, 240 - i * 120, W / 2 - 7, 110, *b[i], 10)
        elif self.kind == 'lean':
            cw = W / 5
            top = 422
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
            self.box(c, 2.5 * cw, 0, 2.5 * cw, costh, '6 Fontes de receita', 'Acesso gratuito para os participantes. O planejamento de continuidade considera apoio institucional e parcerias para sustentar infraestrutura e manutenção, preservando a gratuidade.', 9.5)
        elif self.kind == 'gantt':
            cols = ['Etapa', 'Início', 'Planej.', 'Execução', '19-20/10', '25-26/10']
            widths = [W * 0.42] + [W * 0.116] * 5
            x = [0]
            for a in widths:
                x.append(x[-1] + a)
            rows = [('Concepção do projeto', [1, 0, 0, 0, 0]), ('Pesquisa e planejamento', [0, 1, 0, 0, 0]), ('Implementação do webapp', [0, 0, 1, 1, 0]), ('Testes e publicação', [0, 0, 0, 1, 0]), ('Documentação da AC2', [0, 0, 0, 0, 1])]
            for j, t in enumerate(cols):
                self.box(c, x[j], 170, widths[j], 35, t, '', 9)
            for i, (label, flags) in enumerate(rows):
                yy = 136 - i * 34
                self.box(c, 0, yy, widths[0], 34, label, '', 9)
                for j, f in enumerate(flags):
                    self.box(c, x[j + 1], yy, widths[j + 1], 34, '', '', 9)
                    if f:
                        c.setFillColor(BLUE if f == 1 else HexColor('#c7d5df'))
                        c.rect(x[j + 1] + 7, yy + 10, widths[j + 1] - 14, 14, fill=1, stroke=0)

def footer(c, doc):
    if doc.page < 3:
        c.saveState()
        c.setFont('Calibri', 11)
        c.setFillColor(INK)
        c.drawCentredString(PAGE[0] / 2, 2.2 * cm, 'Sorocaba/SP')
        c.drawCentredString(PAGE[0] / 2, 1.6 * cm, '2026')
        c.restoreState()
        return
    c.saveState()
    c.setFont('Calibri', 9)
    c.setFillColor(GRAY)
    c.drawString(2 * cm, 1.05 * cm, 'EcoVerse | UPX II | AC2 | 2026')
    c.drawRightString(PAGE[0] - 2 * cm, 1.05 * cm, str(doc.page))
    c.restoreState()
story.append(Spacer(1, 0))
logoim = PILImage.open(LOGO)
lw = 260
lh = lw * logoim.height / logoim.width
story.extend([Image(str(LOGO), width=lw, height=lh), Spacer(1, 20)])
p('CENTRO UNIVERSITÁRIO FACENS', 'center')
p('CURSO SUPERIOR DE TECNOLOGIA EM<br/>ANÁLISE E DESENVOLVIMENTO DE SISTEMAS', 'center')
story.append(Spacer(1, 24))
for name, ra in TEAM:
    p(name + ' - RA ' + ra, 'center')
story.append(Spacer(1, 30))
p('<b>ECOVERSE</b>', 'center')
p('<b>Plataforma de orientação e acompanhamento<br/>do descarte responsável</b>', 'center')
p('Usina de Projetos Experimentais II', 'center')
p('Documentação do projeto para a AC2', 'center')
story.append(Spacer(1, 10))
story.append(PageBreak())
p('<b>CENTRO UNIVERSITÁRIO FACENS</b>', 'center')
p('ANÁLISE E DESENVOLVIMENTO DE SISTEMAS', 'center')
story.append(Spacer(1, 26))
for name, ra in TEAM:
    p(name + ' - RA ' + ra, 'center')
story.append(Spacer(1, 35))
p('<b>ECOVERSE</b>', 'center')
p('Plataforma de orientação e acompanhamento<br/>do descarte responsável', 'center')
story.append(Spacer(1, 24))
q = Table([[P('Documentação apresentada ao Centro Universitário Facens como parte da Avaliação Continuada 2 da disciplina de Usina de Projetos Experimentais II, sob orientação da Profa. Ma. Cilene Renata Real.', 'body')]], colWidths=[W * 0.58])
q.hAlign = 'RIGHT'
q.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
story.append(q)
story.append(Spacer(1, 10))
page('1 Informações do Projeto')
p('<b>Título do projeto:</b> EcoVerse - Plataforma de orientação e acompanhamento do descarte responsável.<br/><b>Instituição:</b> Centro Universitário Facens.<br/><b>Curso:</b> Análise e Desenvolvimento de Sistemas.<br/><b>Disciplina:</b> Usina de Projetos Experimentais II.<br/><b>Orientadora:</b> Profa. Ma. Cilene Renata Real.<br/><b>Período letivo:</b> segundo semestre de 2026.<br/><b>Entrega:</b> AC2, prevista para 26/10/2026, às 18h, pelo Canvas.')
p('<b>Equipe:</b> Nathan Borges, Vinícius Stadler Gorov, Antonio Carlos Damante de Souza, Guilherme Henrique de Assis Carvalho, Lincoln Mariozzi Proença Sobrinho do Prado e Matheus Lisbôa Paludeto.')
p('<b>Recorte do projeto:</b> orientar o descarte de pilhas, baterias, eletroeletrônicos, lâmpadas e óleo de cozinha; conectar cidadãos a pontos compatíveis e organizar o registro das entregas. A implantação inicial concentra-se em Sorocaba/SP, com expansão prevista para a Região Metropolitana de Sorocaba.')
p('<b>Acesso ao protótipo:</b> ' + link('mosfet.com.br', SITE) + '<br/><b>Quadro de acompanhamento:</b> ' + link('EcoVerse no Trello', BOARD) + '<br/><b>Código do projeto:</b> ' + link('Repositório EcoVerse', GIT))
p('Este relatório apresenta a etapa de desenvolvimento correspondente à AC2, com a estrutura do produto, os resultados técnicos e o planejamento de evolução do EcoVerse.', 'small')
h('2 Introdução', 1)
p('O descarte de materiais domésticos exige mais do que a intenção de separar resíduos. O morador precisa reconhecer o material, identificar um local que o aceite e compreender como realizar a entrega. Quando essas informações ficam dispersas, a decisão pode ser adiada ou resultar em deslocamento para um ponto incompatível.')
p('O EcoVerse organiza essa jornada em uma aplicação web. A consulta pública permite buscar pontos de coleta por material; após a autenticação, o participante pode registrar o descarte, gerar um código de entrega e acompanhar as etapas informadas pela rede. Pontos e operadores contam com recursos para recebimento, parcerias, retiradas e lotes.')
p('O projeto reúne orientação ao participante e gestão das etapas de recebimento em uma aplicação web. Sua implementação integra interface, serviços e persistência de dados, com foco na clareza da jornada e na organização da rede de coleta.')
page('3 Objetivos')
h('3.1 Objetivo Geral')
p('Desenvolver e avaliar uma plataforma web que facilite o descarte responsável de materiais domésticos, conectando orientação, localização de pontos compatíveis, registro de entregas e acompanhamento das etapas operacionais em uma jornada acessível pelo navegador.')
h('3.2 Objetivos Específicos')
for t in ['1. Organizar a consulta de pontos por categoria de material e apresentar orientações de descarte antes da necessidade de criar uma conta.', '2. Registrar materiais e quantidades em unidades adequadas, aceitando litros decimais para óleo e quantidades inteiras para materiais contáveis.', '3. Emitir QR ou código consultável para vincular o registro à confirmação de recebimento por um ponto autorizado.', '4. Disponibilizar histórico de etapas ao participante e recursos de parceria, retirada e lote aos perfis operacionais.', '5. Proteger o acesso às informações e transições por autenticação e regras de autorização, com persistência em banco de dados.', '6. Verificar as regras de domínio e os fluxos integrados, documentar a evidência obtida e preparar testes de usabilidade com participantes e parceiros.', '7. Relacionar a solução ao desenvolvimento sustentável e organizar sua evolução por tarefas, responsáveis e critérios de aceite no Trello.']:
    p(t)
h('4 Justificativa', 1)
p('O Global E-waste Monitor 2024 registra a geração mundial de 62 milhões de toneladas de resíduos eletroeletrônicos em 2022, das quais 22,3% tiveram coleta e reciclagem formalmente documentadas. Esse cenário evidencia a relevância de iniciativas voltadas à orientação do descarte e à organização dos fluxos de recebimento (ITU; UNITAR, 2024).')
p('No âmbito local, a Prefeitura de Sorocaba mantém informações específicas de recebimento e ressalta restrições distintas entre seus serviços. Isso reforça a necessidade de conferir o aceite por ponto, em vez de presumir que todo local recebe qualquer material. O projeto pretende facilitar esse acesso à informação e organizar o registro da entrega (Sorocaba, s.d.).')
p('A proposta se relaciona ao ODS 12, especialmente à gestão de resíduos, à redução do descarte inadequado e ao acesso à informação. No âmbito acadêmico, o projeto articula análise de requisitos, desenvolvimento de interfaces, banco de dados, redes e gestão de projetos em torno de uma demanda socioambiental (ONU Brasil, s.d.).')
page('5 Cronograma')
p('O projeto teve início com a disciplina de Usina de Projetos Experimentais II, no segundo semestre de 2026. O cronograma organiza a concepção, o planejamento, a implementação e a consolidação da AC2. Os marcos de testes e publicação ocorreram em outubro, com entrega da documentação prevista para 26/10/2026.')
story.append(Diagram('gantt'))
p('Figura 1 - Cronograma do EcoVerse: fases iniciais da UPX II e marcos de consolidação da AC2. Fonte: elaboração da equipe.', 'caption')
table(['Etapa', 'Período', 'Atividades'], [('Concepção', 'Início da UPX II', 'Definição do tema de desenvolvimento sustentável e do problema de descarte.'), ('Planejamento', 'Fase inicial da UPX II', 'Pesquisa documental, delimitação do público, organização dos requisitos e planejamento da experiência.'), ('Desenvolvimento', 'Ao longo da UPX II', 'Implementação da aplicação web, serviços, banco de dados e recursos operacionais.'), ('Verificação técnica', '19 e 20/10/2026', 'Execução dos testes de domínio e integração, revisão da interface e verificação da publicação.'), ('Consolidação da AC2', '25 e 26/10/2026', 'Organização da documentação, das capturas do sistema e do relatório do Trello.'), ('Entrega', '26/10/2026', 'Apresentação da documentação do projeto na plataforma Canvas, até as 18h.')], [1.15, 1.15, 2.8])
page('6 Metodologia')
p('O EcoVerse foi iniciado no começo da disciplina de Usina de Projetos Experimentais II. A metodologia combina pesquisa documental, definição de requisitos, modelagem da experiência de uso e desenvolvimento incremental. O problema foi decomposto em jornadas, telas, regras de negócio e serviços integrados ao banco de dados.')
h('6.1 Compreensão do problema e definição do escopo')
p('O escopo abrange pilhas e baterias, eletroeletrônicos, lâmpadas e óleo de cozinha. A análise considera as necessidades do morador, do ponto de coleta e do operador parceiro. As categorias orientam a consulta, as unidades de medida e a compatibilidade de recebimento. Materiais de serviços de saúde e perfurocortantes permanecem fora do escopo.')
h('6.2 Organização do trabalho')
p('O acompanhamento das atividades é organizado no Trello, pelas listas Tarefas, Em progresso, Pronto e Aprovado. Os cartões reúnem entregas, responsáveis e prazos, permitindo acompanhar a passagem entre execução, conclusão e revisão. O relatório de acompanhamento é apresentado no Apêndice A.')
h('6.3 Implementação e controle de versão')
p('A aplicação separa interface web e API. As alterações são organizadas em código TypeScript, migrações de banco e documentação de validação. O Git registra as versões e o fluxo de publicação utiliza imagens de containers. A interface usa componentes compartilhados e reaproveita as funções operacionais da base anterior, adaptadas ao domínio de descarte.')
h('6.4 Verificação e validação')
p('A verificação técnica contempla regras de categoria e quantidade, autorização por perfil, compatibilidade dos pontos, persistência de registros, armazenamento de imagens e navegação. Os ensaios de domínio e integração verificam o comportamento dos serviços; a etapa de avaliação de usabilidade prevê a análise da clareza das telas e da execução das tarefas pelo usuário.')
h('6.5 Integração dos conteúdos do curso')
p('O desenvolvimento articula conteúdos de Engenharia de Software, Banco de Dados e Redes de Computadores. A definição de requisitos orienta as regras da aplicação; a modelagem relacional organiza registros e eventos; a comunicação entre serviços e a publicação web integram os conceitos de redes ao protótipo.')
page('7 Equipe do Projeto')
p('O projeto EcoVerse é desenvolvido por seis estudantes do curso de Análise e Desenvolvimento de Sistemas do Centro Universitário Facens, no âmbito da disciplina de Usina de Projetos Experimentais II.')
p('Tabela 1 - Integrantes da equipe EcoVerse.', 'caption')
table(['Integrante', 'Registro Acadêmico'], [(name, ra) for name, ra in TEAM], [4, 1])
page('8 Desenvolvimento do Projeto')
h('8.1 Solução e jornada principal')
p('A concepção do EcoVerse parte do guia e mapeamento de logística reversa, com foco na localização de pontos e na orientação por material. A versão desenvolvida para a AC2 concretiza essa proposta em um webapp responsivo e acrescenta registro de entregas, confirmação de recebimento e acompanhamento das etapas operacionais.')
story.append(Diagram('flow'))
p('Figura 2 - Fluxo principal do participante e continuidade na rede parceira. Fonte: elaboração da equipe a partir da aplicação.', 'caption')
p('A consulta pública identifica pontos compatíveis. A conta permite registrar e acompanhar a entrega. O ponto autorizado confirma o recebimento pelo código ou QR; em seguida, a rede pode organizar retiradas e lotes com o operador parceiro.')
h('8.2 Requisitos e regras do domínio')
table(['Regra', 'Comportamento implementado'], [('Categorias atuais', 'Pilhas e baterias; eletroeletrônicos; lâmpadas; óleo de cozinha. A implementação rejeita novas entradas em categorias excluídas ou apenas históricas.'), ('Quantidade', 'Óleo admite litros com até duas casas decimais. Materiais contáveis exigem unidades inteiras e quantidades positivas.'), ('Compatibilidade', 'Todos os materiais do registro devem constar no aceite do ponto. Uma lista vazia não significa aceite universal.'), ('Confirmação', 'O participante não pode confirmar o próprio recebimento. As transições dependem do papel e da operação autorizada.'), ('Participação', 'Registro pendente não gera pontos. O recebimento confirmado credita 10 pontos uma única vez, sem bônus por volume.'), ('Histórico', 'Etapas e eventos são mantidos. Litros e unidades não devem ser somados como uma única medida física.')], [1, 3.3])
page('8 Desenvolvimento do Projeto')
h('8.3 Arquitetura e persistência')
p('A interface utiliza Next.js 16, React 19 e TypeScript. A API é desenvolvida com Fastify 5 e Prisma. PostgreSQL com PostGIS mantém os dados da aplicação, enquanto Redis atende às necessidades de estado auxiliar. Essa separação permite organizar a interface e as regras de negócio em serviços com responsabilidades definidas.')
table(['Camada', 'Responsabilidade', 'Tecnologias'], [('Interface', 'Páginas públicas, sessão, formulários, mapa e painéis por perfil.', 'Next.js, React, TypeScript, Tailwind CSS, Leaflet e Auth.js.'), ('Serviços', 'Autenticação, autorização, registros, recebimentos, parcerias, retiradas e lotes.', 'Fastify, validação de dados e serviços de domínio.'), ('Dados', 'Usuários, materiais, eventos, parceiros, quantidades e trilha operacional.', 'Prisma, PostgreSQL/PostGIS e migrações versionadas.'), ('Estado e arquivos', 'Estado auxiliar e imagens enviadas à aplicação.', 'Redis e volume persistente de uploads da API.'), ('Execução', 'Separação de serviços e publicação web em domínio HTTPS.', 'Docker Compose, pipeline GitHub Actions, Portainer e proxy reverso.')], [0.8, 2.3, 1.7])
p('O navegador acessa os serviços pelo caminho /api/backend, no mesmo domínio da aplicação. A comunicação entre web e API ocorre pela rede interna dos containers. As imagens enviadas são mantidas em volume persistente vinculado à API, separado dos dados de configuração da infraestrutura.')
h('8.4 Modelo de dados e papéis')
p('As entidades internas Donation, DonationItem e DonationEvent representam registro, itens e eventos. OperationalPartnership, PickupRequest e OperationalBatch organizam parcerias, retiradas e lotes. Os identificadores históricos foram mantidos por compatibilidade. A interface apresenta os papéis Participante, Ponto de coleta, Operador parceiro e Administrador.')
p('O histórico organiza as etapas de registro, recebimento no ponto, transporte e recebimento no destino. O acompanhamento representa os eventos registrados pela rede. A certificação ambiental de destinação constitui uma possibilidade de evolução, dependente dos documentos e processos dos operadores.')
page('8 Desenvolvimento do Projeto')
h('8.5 Landing page e consulta pública')
p('A página inicial apresenta a proposta e direciona à busca por material. A consulta é pública; o cadastro fica reservado às funções pessoais. Capturas reais da aplicação publicada, realizadas em 25/10/2026.')
fig(TELAS / '01-landing.png', 'Figura 3 - Landing page do EcoVerse. Ação principal: encontrar pontos de descarte. Origem: aplicação publicada em mosfet.com.br, captura de 25/10/2026.', 210)
fig(TELAS / '02-busca.png', 'Figura 4 - Seleção do material e busca por pontos de descarte na página inicial do EcoVerse.', 210)
page('8 Desenvolvimento do Projeto')
h('8.6 Mapa e acesso à conta')
p('O mapa apresenta a localização da rede e permite filtrar os pontos pelo material aceito. O acesso à conta permite registrar entregas, consultar o histórico e utilizar as funções correspondentes ao perfil. Na etapa de implantação, o cadastro de parceiros estabelece a cobertura disponível para consulta.')
fig(TELAS / '03-mapa-publico.png', 'Figura 5 - Consulta de pontos com filtro de eletrônicos e localização em Sorocaba.', 210)
fig(TELAS / '04-login.png', 'Figura 6 - Tela de entrada para acesso ao registro e acompanhamento por perfil. Captura real de 25/10/2026.', 210)
p('A documentação visual do protótipo é apresentada por capturas da aplicação web implementada, abrangendo a landing page, a seleção de materiais, a consulta da rede e o acesso à conta.', 'small')
page('8 Desenvolvimento do Projeto')
h('8.7 Testes e verificação técnica')
p('A verificação técnica foi organizada em testes de domínio, testes de integração e conferência da publicação. A tabela apresenta os conjuntos executados, suas datas e os comportamentos avaliados.')
table(['Data e ambiente', 'Evidência registrada', 'Alcance'], [('19/10 - ambiente local isolado', '5 testes de domínio, 17 verificações integradas e 9 verificações HTTP aprovados.', 'Regras de materiais/quantidades, perfis, QR, recebimento e transporte; páginas e proxy.'), ('20/10 - teste de versão isolado', '18 verificações integradas com status PASS.', 'Sessões por papel, busca, litros, permissões, uploads, 20 migrações, falha/recuperação da prontidão e persistência após reinício.'), ('20/10 - domínio publicado', '8 verificações com status PASS.', 'Homepage HTTPS, prontidão, autenticação administrativa, upload/leitura, páginas protegidas, busca pública, mídia e redirecionamento www.'), ('25/10 - documentação', 'Capturas reais da interface pública e do Trello.', 'Registro da interface pública e da organização das entregas da AC2.')], [1.1, 1.8, 2.2])
p('Fonte: registros de testes e relatórios técnicos do projeto EcoVerse, referentes a 19 e 20 de outubro de 2026.', 'small')
h('8.8 Estágio de desenvolvimento')
p('Na etapa da AC2, o protótipo reúne orientação de descarte, consulta pública, autenticação, registro de materiais, emissão de código ou QR, confirmação de recebimento e ferramentas operacionais. As regras de autorização e de compatibilidade entre material e ponto conectam a interface aos serviços e ao banco de dados.')
p('A próxima etapa compreende a implantação da rede local, o acompanhamento do uso e o aperfeiçoamento dos recursos de interação com dispositivos, incluindo câmera e localização. A avaliação da experiência do participante e da rotina dos pontos orientará a priorização das melhorias.')
page('9 Resultados Esperados')
p('Espera-se que o participante encontre um ponto compatível, registre sua entrega e acompanhe as etapas de recebimento. Para a rede, espera-se organizar os registros de entrada, as retiradas e a formação de lotes. A contribuição social pretendida é reduzir as dificuldades de acesso à informação sobre descarte responsável.')
table(['Dimensão', 'Indicador proposto', 'Como verificar'], [('Descoberta', 'Pessoas que encontram um ponto compatível sem ajuda.', 'Ensaio de usabilidade com tarefas de busca e registro; medição de tempo, dúvidas e conclusão.'), ('Conversão', 'Entregas confirmadas ÷ registros criados.', 'Apuração por período, com classificação de abandono, cancelamento e tempo de espera.'), ('Confiabilidade', 'Registros com histórico coerente e sem confirmação indevida.', 'Roteiro de teste por perfil e conferência dos eventos persistidos.'), ('Operação', 'Tempo entre entrada no ponto e retirada pelo operador.', 'Comparação entre as datas dos eventos de recebimento e retirada.'), ('Rede', 'Pontos com aceite, contato e situação revisados.', 'Revisão do cadastro junto ao ponto, com registro de data e método.'), ('Impacto', 'Quantidade recebida por material e unidade.', 'Totais apresentados separadamente por material e unidade de medida.')], [0.85, 1.8, 2.45])
h('9.1 Critérios para o piloto')
p('A implantação piloto prevê uma rede local de pontos e operadores, com conferência das condições de recebimento. A avaliação percorrerá seleção do material, busca, compreensão das orientações, registro, confirmação e consulta do histórico. As dificuldades observadas serão organizadas por frequência e impacto sobre a conclusão das tarefas.')
p('A avaliação do piloto será orientada pela conclusão das tarefas, pela clareza das informações e pela consistência dos registros. A expansão da iniciativa considera a capacidade de atendimento dos pontos e a manutenção de informações atualizadas.')
page('10 Persona')
p('<b>Rafael Brandão, 20 anos, desenvolvedor júnior, residente em Santa Rita do Sapucaí/MG.</b> Acumula pilhas, baterias e óleo em casa por não saber onde realizar o descarte. Sua principal necessidade é encontrar rapidamente, em um aplicativo ou site, o local adequado para cada material.')
p('A persona representa o comportamento de um cidadão que já separa os materiais, mas encontra dificuldade para localizar o destino adequado. O perfil orienta a linguagem, a organização das categorias, a busca geográfica e a apresentação das informações dos pontos. Frase representativa: “Eu separo certinho, só não sei pra onde levar.”')
table(['Aspecto', 'Caracterização e implicação para o produto'], [('Objetivo', 'Encontrar rapidamente onde descartar cada material.'), ('Dificuldade', 'Informações dispersas e dúvida sobre o aceite dos pontos.'), ('Comportamento', 'Separa pilhas, baterias e óleo, mas mantém esses materiais em casa por falta de orientação.'), ('Necessidade', 'Mapa, filtros por categoria e informações claras sobre o local de entrega.'), ('Decisão de interface', 'Permitir consulta pública e tornar a busca por material simples e direta.')], [1, 3.5])
h('10.1 Mapa de Empatia')
story.append(Diagram('empathy'))
p('Figura 7 - Mapa de empatia do público de referência do EcoVerse. Fonte: elaboração da equipe.', 'caption')
page('10 Persona')
h('10.2 Jornada do Usuário')
p('A jornada descreve a relação entre a necessidade do participante, suas ações e as respostas oferecidas pelo produto. O percurso começa na identificação do material e termina na consulta das etapas posteriores à confirmação do recebimento.')
table(['Etapa', 'Ação e necessidade', 'Dificuldade provável', 'Resposta do EcoVerse'], [('1 Perceber', 'Identifica material guardado e decide descartar.', 'Dúvida sobre o tipo e o preparo.', 'Página pública com materiais e explicação do processo.'), ('2 Encontrar', 'Busca um local viável no trajeto.', 'Informação dispersa ou ponto incompatível.', 'Filtro por material e mapa; conferir aceite e condições do ponto.'), ('3 Preparar', 'Escolhe o ponto e registra a entrega.', 'Formulário longo ou unidades confusas.', 'Conta para funções pessoais; itens, quantidade e unidade adequadas.'), ('4 Entregar', 'Apresenta o material e o código ao ponto.', 'Temor de não haver confirmação.', 'Ponto autorizado registra o recebimento; código vincula o evento.'), ('5 Acompanhar', 'Consulta o andamento após a entrega.', 'Falta de retorno ou interpretação errada de status.', 'Histórico das etapas informadas e limites claros da comprovação.')], [0.8, 1.45, 1.45, 1.65])
p('Tabela 2 - Jornada do participante: necessidades, ações e respostas da aplicação. Fonte: elaboração da equipe.', 'caption')
h('10.3 Avaliação da experiência de uso')
p('A avaliação com usuários integra a próxima etapa do projeto. O roteiro contempla a identificação do material, a localização de um ponto compatível, o registro da entrega e a interpretação do histórico. A análise considera o tempo de execução, as dificuldades de navegação e a compreensão das informações apresentadas.')
p('A análise da pesquisa relacionará as dificuldades observadas às decisões de interface, com atenção às diferenças entre os perfis de uso e à clareza das etapas de registro e recebimento.')
page('11 Canvas de Proposta de Valor')
p('O Canvas de Proposta de Valor relaciona as necessidades do participante aos recursos do EcoVerse. O mapa de valor reúne a oferta da solução; o perfil do cliente descreve tarefas, dores e ganhos que orientam seu desenvolvimento.')
story.append(Diagram('value'))
p('Figura 8 - Canvas de proposta de valor. Esquerda: mapa de valor. Direita: perfil do cliente. Fonte: elaboração da equipe, a partir do modelo de proposta de valor.', 'caption')
h('11.1 Correspondência entre necessidade e solução')
p('A busca por compatibilidade responde à necessidade de encontrar um local adequado. O registro e o código organizam a entrega, enquanto a confirmação e o histórico oferecem continuidade ao acompanhamento. A atualização dos cadastros e dos eventos sustenta essa proposta de valor.')
p('Para os pontos e operadores, a solução centraliza recebimentos, retiradas e lotes. A integração entre essas funções permite acompanhar a movimentação dos materiais e distribuir responsabilidades ao longo da operação.')
page('12 Lean Canvas')
p('O Lean Canvas apresenta o modelo de uma iniciativa gratuita de impacto socioambiental. A proposta integra orientação ao participante e organização da rede de coleta, com expansão orientada pela capacidade de atendimento e pelos resultados da utilização.')
story.append(Diagram('lean'))
p('Figura 9 - Lean Canvas do EcoVerse, com nove blocos. Fonte: elaboração da equipe, a partir do modelo Lean Canvas.', 'caption')
h('12.1 Viabilidade e priorização')
p('A estratégia inicial concentra-se na implantação de uma rede local, com informações de aceite atualizadas e acompanhamento das entregas. A integração entre consulta pública e operação constitui o diferencial buscado em relação às soluções centradas exclusivamente na localização de pontos.')
p('A utilização da plataforma é gratuita. A sustentabilidade da iniciativa considera o planejamento de infraestrutura e manutenção, além da possibilidade de apoio institucional para sua continuidade.')
page('13 Estudo de Mercado TAM SAM SOM')
h('13.1 Segmentos e alternativas')
p('O EcoVerse atende à necessidade de localizar destinos adequados para pilhas, baterias, eletroeletrônicos, lâmpadas e óleo de cozinha. O público principal é formado por cidadãos que precisam de orientação prática para o descarte. Pontos de coleta, ecopontos, cooperativas e operadores compõem a rede de atendimento. Universidades, governos locais e organizações ambientais constituem possíveis canais de articulação e divulgação.')
table(['Alternativa', 'Oferta consultada', 'Relação com o EcoVerse'], [('Green Eletron', 'Consulta de locais e orientações para descarte de eletroeletrônicos e pilhas.', 'Referência para informações específicas por categoria e para a organização da rede.'), ('Reciclus', 'Localização de pontos de entrega de lâmpadas e condições de recebimento.', 'Evidencia a necessidade de identificar o aceite e as regras de cada ponto.'), ('Serviços municipais', 'Informações sobre serviços de recebimento e restrições em Sorocaba.', 'Integram o contexto local de orientação sobre descarte.'), ('Busca e contato direto', 'Pesquisa em sites, mapas e contato com estabelecimentos.', 'Oportunidade de reunir consulta, orientação e acompanhamento em uma mesma jornada.')], [1, 2, 2.15])
p('Fontes: Green Eletron; Reciclus; Prefeitura de Sorocaba. Consulta em 25/10/2026.', 'small')
h('13.2 Recorte e contexto de adoção')
p('O estudo considera a Região Metropolitana de Sorocaba, composta por 27 municípios, como universo regional de expansão. A implantação inicial concentra-se no município de Sorocaba. Como o acesso à plataforma é gratuito, o dimensionamento é expresso em pessoas potencialmente alcançadas, sem conversão em faturamento.')
p('Os indicadores nacionais ajudam a caracterizar esse público. A PNAD Contínua TIC 2025 informa que 90,5% das pessoas com 10 anos ou mais utilizaram a internet no período pesquisado. Na pesquisa CNI/Nexus de setembro de 2024, 47% dos entrevistados afirmaram que, em suas casas, os materiais sempre são separados para reciclagem. Esses indicadores contextualizam acesso digital e comportamento ambiental; não são utilizados como taxas locais de adesão ao EcoVerse (IBGE, 2026; CNI; NEXUS, 2024).')
page('13 Estudo de Mercado TAM SAM SOM')
h('13.3 Dimensionamento territorial e cenário de adoção')
p('Adota-se 2025 como ano-base comum para as estimativas populacionais dos dois recortes. A Região Metropolitana de Sorocaba reúne 2.268.579 habitantes, segundo o IBGE. O município de Sorocaba possui 762.172 habitantes na mesma base anual (IBGE, 2025; Sorocaba, s.d.).')
table(['Indicador', 'Delimitação', 'Dimensionamento'], [('TAM', 'Universo regional potencial: moradores dos 27 municípios da Região Metropolitana de Sorocaba.', '2.268.579 pessoas.'), ('SAM', 'Recorte territorial de implantação: moradores do município de Sorocaba.', '762.172 pessoas.'), ('SOM', 'Cenário exploratório de adoção no primeiro ano: 2% do recorte municipal.', '762.172 × 0,02 = aproximadamente 15.243 usuários.')], [0.65, 2.7, 1.7])
p('Tabela 3 - Dimensionamento do alcance do EcoVerse. TAM e SAM: bases populacionais de 2025. SOM: cenário de planejamento com taxa de adoção de 2%. Fonte: IBGE; Prefeitura de Sorocaba; elaboração da equipe.', 'caption')
p('TAM e SAM representam os limites demográficos dos territórios considerados. O alcance efetivo depende do acesso digital, da necessidade de descarte, da divulgação e da cobertura da rede. O SOM expressa uma hipótese de planejamento para o primeiro ano de disponibilização, e não um resultado já observado.')
h('13.4 Implantação e acompanhamento')
p('A implantação começa em Sorocaba, com organização dos pontos de coleta e conferência dos materiais aceitos. A ampliação para os demais municípios considera a qualidade das informações, a capacidade de atendimento e a continuidade da operação. O acesso gratuito favorece a participação do cidadão, enquanto o planejamento de custos e a articulação institucional sustentam a expansão.')
p('O acompanhamento contempla usuários ativos mensais, buscas concluídas, registros de descarte, entregas confirmadas e pontos ativos. Esses indicadores permitem comparar a utilização observada ao cenário de adoção e identificar em quais etapas a jornada necessita de ajustes.')
page('14 Conclusão')
p('O desenvolvimento do EcoVerse resultou em uma aplicação web que integra orientação, localização de pontos e registro de descarte. A organização por perfis distingue as responsabilidades de participantes, pontos e operadores, enquanto as regras de material, quantidade e autorização estruturam a jornada digital.')
p('Os testes de domínio e integração verificaram comportamentos centrais da aplicação, como validação de quantidades, compatibilidade de pontos, autenticação e persistência. O trabalho permitiu relacionar os requisitos do produto às regras dos serviços e ao modelo de dados, além de consolidar uma interface comum às diferentes jornadas.')
p('A continuidade do projeto concentra-se na implantação da rede de parceiros, na avaliação da experiência de uso e no aperfeiçoamento do acompanhamento das entregas. Essas etapas ampliam a aplicação prática do protótipo e sustentam a evolução da proposta de descarte responsável.')
h('15 Estudos Futuros', 1)
table(['Prioridade', 'Estudo ou melhoria', 'Benefício e condição'], [('1', 'Piloto com usuários e pontos de coleta', 'Avaliar a busca por material, a compreensão das etapas e o funcionamento da rede.'), ('1', 'Qualidade da informação', 'Organizar revisão de aceite, contato, horários e disponibilidade dos pontos.'), ('1', 'Acessibilidade e dispositivos reais', 'Avaliar teclado, leitor de tela, conexão móvel, câmera e localização.'), ('2', 'Participação colaborativa', 'Estudar avaliações, comentários e sugestões de pontos, com critérios de moderação e atualização.'), ('2', 'Evolução mobile', 'Avaliar uma versão distribuída como aplicativo, conforme os resultados de uso do webapp.'), ('2', 'Expansão regional e sustentabilidade', 'Ampliar a cobertura na Região Metropolitana de Sorocaba e planejar a manutenção do acesso gratuito.')], [0.55, 1.5, 2.55])
p('A priorização das próximas versões considera a qualidade das informações da rede, o esforço exigido do usuário e a capacidade operacional dos parceiros. Recursos de automação serão incorporados conforme as necessidades identificadas na utilização da plataforma.')
page('16 Referências Bibliográficas')
refs = [('FACENS.', 'Modelo de documentação de projeto. Sorocaba: Centro Universitário Facens, 2026.'), ('FACENS.', 'UPXII - Usina de Projetos Experimentais II: plano de ensino. Tecnologia em Análise e Desenvolvimento de Sistemas. Sorocaba: Centro Universitário Facens, 2025.'), ('REAL, Cilene Renata.', 'UPX II: aulas 01, 02 e 03. Material didático. Sorocaba: Centro Universitário Facens, 2026.'), ('REAL, Cilene Renata.', 'Projeto funcional 70%: orientações para a Avaliação Continuada 2. Sorocaba: Centro Universitário Facens, 2026.'), ('EQUIPE ECOVERSE.', 'EcoVerse: código-fonte e documentação técnica. 2026. Disponível em: ' + link('github.com/borges-br/ecoverse', GIT) + '. Acesso em: 25 out. 2026.'), ('EQUIPE ECOVERSE.', 'Relatórios de testes e verificação da publicação. Documentação técnica do projeto. Sorocaba, 19-20 out. 2026.'), ('EQUIPE ECOVERSE.', 'Quadro EcoVerse. Trello, 2026. Disponível em: ' + link('trello.com/b/xqoCzfOG/ecoverse', BOARD) + '. Acesso e captura em: 25 out. 2026.'), ('ITU; UNITAR.', 'The Global E-waste Monitor 2024. 2024. Disponível em: ' + link('Publicação oficial da ITU', 'https://www.itu.int/en/ITU-D/Environment/Pages/Publications/The-Global-E-waste-Monitor-2024.aspx') + '. Acesso em: 25 out. 2026.'), ('NAÇÕES UNIDAS BRASIL.', 'Objetivo de Desenvolvimento Sustentável 12: consumo e produção responsáveis. [s.d.]. Disponível em: ' + link('ODS 12', 'https://brasil.un.org/pt-br/sdgs/12') + '. Acesso em: 25 out. 2026.'), ('SOROCABA. Prefeitura Municipal.', 'Educação Ambiental: lixo eletrônico. [s.d.]. Disponível em: ' + link('Informações municipais de recebimento', 'https://meioambiente.sorocaba.sp.gov.br/educacaoambiental/lixo-eletronico/') + '. Acesso em: 25 out. 2026.'), ('SOROCABA. Prefeitura Municipal.', 'Portal 156: carta de serviço - Ecopontos. [s.d.]. Disponível em: ' + link('Carta de Serviço', 'https://portal156.sorocaba.sp.gov.br/portal156/carta-servico/assunto/C4F424F3-02B9-E411-9E1C-005056BF74CB/') + '. Acesso em: 25 out. 2026.'), ('GREEN ELETRON.', 'Perguntas frequentes. [s.d.]. Disponível em: ' + link('Perguntas frequentes', 'https://greeneletron.org.br/perguntas-frequentes/') + '. Acesso em: 25 out. 2026.'), ('RECICLUS.', 'Onde descartar. [s.d.]. Disponível em: ' + link('Localizador Reciclus', 'https://reciclus.org.br/onde-descartar/') + '. Acesso em: 25 out. 2026.'), ('STRATEGYZER.', 'The Value Proposition Canvas. Modelo conceitual utilizado para organizar mapa de valor e perfil do cliente. Disponível em: ' + link('Value Proposition Canvas', 'https://www.strategyzer.com/library/the-value-proposition-canvas') + '. Acesso em: 25 out. 2026.'), ('LEANSTACK.', 'Lean Canvas. Modelo conceitual de nove blocos. Disponível em: ' + link('Lean Canvas', 'https://leanstack.com/lean-canvas') + '. Acesso em: 25 out. 2026.'), ('EQUIPE DO PROJETO.', 'Documentação formal de logística reversa UPX II. Guia e Mapeamento de Logística Reversa. Sorocaba: Facens, set. 2026. 11 p.'), ('IBGE.', 'Estimativas 2025: população das regiões metropolitanas e regiões integradas de desenvolvimento. 2025. Disponível em: ' + link('Tabela de população regional', 'https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/8383bdedce5a6d972e60dd32671e533a.pdf') + '. Acesso em: 25 out. 2026.'), ('IBGE.', 'Proporção de usuários da internet no país ultrapassou 90% da população de 10 anos ou mais, em 2025. Agência de Notícias, 2 jul. 2026. Disponível em: ' + link('PNAD Contínua TIC 2025', 'https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/47408-proporcao-de-usuarios-da-internet-no-pais-ultrapassou-90-da-populacao-de-10-anos-ou-mais-em-2025') + '. Acesso em: 25 out. 2026.'), ('CNI; NEXUS.', 'Sustentabilidade e opinião pública. Set. 2024. p. 3 e 63. Disponível em: ' + link('Pesquisa CNI e Nexus', 'https://static.portaldaindustria.com.br/portaldaindustria/noticias/media/filer_public/c0/3a/c03a0890-d087-4a51-acc3-7c6a6bb6ae75/opiniao_publica_e_sustentabilidade.pdf') + '. Acesso em: 25 out. 2026.'), ('SOROCABA. Prefeitura Municipal.', 'Governo municipal: caracterização de Sorocaba. População estimada pelo IBGE em 2025. Disponível em: ' + link('Portal oficial do município', 'https://www.sorocaba.sp.gov.br/governo-municipal/') + '. Acesso em: 25 out. 2026.')]
for a, b in refs:
    p('<b>' + a + '</b> ' + b, 'ref')
page('Apêndice A Relatório de Atualização do Trello')
p('<b>Quadro:</b> EcoVerse.<br/><b>Consulta:</b> 25/10/2026.<br/><b>Link:</b> ' + link('Abrir o quadro EcoVerse', BOARD) + '.')
table(['Lista', 'Organização das atividades'], [('Tarefas', 'Entregas de apresentação/pitch, banner digital e artigo acadêmico.'), ('Em progresso', 'Documentação principal, entrega parcial do Trello e material de telas com landing page.'), ('Pronto', 'Componentes e materiais da aplicação: GitHub, telas, landing page, integração e ferramentas.'), ('Aprovado', 'Registros de definição do projeto, pesquisa, persona e canvas, organizados na etapa de revisão.')], [1, 4])
p('O quadro concentra o acompanhamento das entregas acadêmicas e técnicas, com organização por estado, prazos e responsáveis. A equipe e a orientadora participam do ambiente compartilhado de acompanhamento.')
h('A.1 Acompanhamento das entregas')
p('Na data de referência, as entregas da documentação principal, do Trello parcial e das telas com landing page estavam organizadas em Em progresso. Os cartões em Pronto reuniam os componentes da aplicação e os materiais de apresentação para a consolidação da AC2.')
p('O acompanhamento relaciona a execução técnica às entregas acadêmicas. O registro de responsáveis e prazos permite distribuir atividades e identificar dependências, enquanto os materiais vinculados aos cartões apoiam a revisão do trabalho.')
p('As listas estruturam a sequência de trabalho da equipe, desde a definição das tarefas até a revisão das entregas.')
page('Apêndice A Evidência Visual do Trello')
fig(ASSETS / 'trello-quadro.png', 'Figura 10 - Quadro EcoVerse no Trello, com as listas Tarefas, Em progresso, Pronto e Aprovado. Registro de 25/10/2026.', 515)
p('Os prazos exibidos nos cartões integram o planejamento da AC2. A captura apresenta o acompanhamento da equipe na data de referência do relatório.', 'small')
before = sha256(TEMPLATE.read_bytes()).hexdigest()
doc = SimpleDocTemplate(str(PDF), pagesize=PAGE, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=3 * cm, bottomMargin=2 * cm, title='EcoVerse Documentação do Projeto AC2', author='Equipe EcoVerse', subject='UPX II Facens AC2 2026', allowSplitting=1)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
after = sha256(TEMPLATE.read_bytes()).hexdigest()
assert before == after
r = PdfReader(PDF)
text = '\n'.join((p.extract_text() or '' for p in r.pages))
required = ['Informações do Projeto', 'Introdução', 'Objetivos', 'Objetivo Geral', 'Objetivos Específicos', 'Justificativa', 'Cronograma', 'Metodologia', 'Equipe do Projeto', 'Desenvolvimento do Projeto', 'Resultados Esperados', 'Persona', 'Canvas de Proposta de Valor', 'Lean Canvas', 'Estudo de Mercado', 'Conclusão', 'Estudos Futuros', 'Referências Bibliográficas']
assert all((a in text for a in required)), [a for a in required if a not in text]
assert all((ra in text and n in text for n, ra in TEAM))
assert len(r.pages) >= 18
assert not any((a in text for a in ['Insira aqui', 'RA123456', 'RA654321', 'Escreva aqui', 'Lorem ipsum']))
links = []
for i, pg in enumerate(r.pages):
    for a in pg.get('/Annots', []):
        an = a.get_object()
        dest = an.get('/A', {}).get('/URI')
        if dest:
            links.append({'page': i + 1, 'url': str(dest)})
manifest = {'pdf': str(PDF), 'pages': len(r.pages), 'template_sha256': before, 'template_unchanged': before == after, 'sections_checked': required, 'team': TEAM, 'links': links, 'bytes': PDF.stat().st_size}
(HERE / 'validation.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
(HERE / 'final-extracted.txt').write_text(text, encoding='utf-8')
print(json.dumps({'pages':manifest['pages'],'pdf':manifest['pdf'],'bytes':manifest['bytes'],'links':len(manifest['links'])},ensure_ascii=False))
