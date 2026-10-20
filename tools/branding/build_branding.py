"""Build the EcoVerse identity kit and its reviewed brand guide.

The application source, API contracts, persistent data and deployment files are
intentionally outside this authoring script. Run from the repository root.
"""
from pathlib import Path
import sys, json, math, shutil, hashlib, zipfile
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tmp/pythonpackages'))
from fontTools.ttLib import TTFont as FTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw
import pymupdf

KIT = ROOT / 'output/branding/ecoverse-v1'
TMP = ROOT / 'tmp/pdfs'
PDF = ROOT / 'output/pdf/ecoverse-guia-de-marca-v1.pdf'
for name in ['logos', 'fonts', 'images', 'motion', 'applications']:
    (KIT / name).mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)

P = dict(forest='#153F35', green='#28735A', lime='#CBEA73', cream='#F4F3EA',
         ink='#23352D', stone='#5D6C63', mist='#DCE8DE', white='#FFFFFF',
         blue='#325F84', bluebg='#DDEAF5', amber='#85551A', amberbg='#F4E5C9',
         red='#A63E36', redbg='#F6E1DC', line='#C8D3C9')

# Keep the licensed original variable fonts; produce static instances for PDF
# embedding and portable editing. Original OFL files accompany both families.
font_specs = [('Manrope', 'Manrope[wght].ttf', {'wght': 600}, 'M'),
              ('Manrope', 'Manrope[wght].ttf', {'wght': 700}, 'MB'),
              ('Manrope', 'Manrope[wght].ttf', {'wght': 800}, 'MX'),
              ('DMSans', 'DMSans[opsz,wght].ttf', {'opsz': 14, 'wght': 400}, 'D'),
              ('DMSans', 'DMSans[opsz,wght].ttf', {'opsz': 14, 'wght': 500}, 'DM'),
              ('DMSans', 'DMSans[opsz,wght].ttf', {'opsz': 14, 'wght': 700}, 'DB')]
FONT_FILES = {}
for fam, varname, axes, key in font_specs:
    dest = KIT / 'fonts' / f'{fam}-{int(axes["wght"])}.ttf'
    if not dest.exists():
        instantiateVariableFont(FTFont(KIT/'fonts'/varname), axes, inplace=False).save(dest)
    FONT_FILES[key] = dest
    pdfmetrics.registerFont(TTFont(key, str(dest)))
pdfmetrics.registerFontFamily('D', normal='D', bold='DB', italic='D', boldItalic='DB')
pdfmetrics.registerFontFamily('M', normal='M', bold='MB', italic='M', boldItalic='MB')
FTS = {key: FTFont(path) for key, path in FONT_FILES.items()}

def outline(text, x, baseline, size, font='MB', color=None):
    ft = FTS[font]; gs = ft.getGlyphSet(); cmap = ft.getBestCmap()
    scale = size / ft['head'].unitsPerEm
    paths = []
    for ch in text:
        glyph = cmap.get(ord(ch), '.notdef')
        pen = SVGPathPen(gs)
        gs[glyph].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
        paths.append(pen.getCommands())
        x += ft['hmtx'][glyph][0] * scale
    return '<path fill="'+(color or P['forest'])+'" d="'+' '.join(paths)+'"/>'

MARK_D = 'M20 50 H82 C82 32.327 67.673 18 50 18 C32.327 18 18 32.327 18 50 C18 67.673 32.327 82 50 82 C56.3 82 62.2 80.2 67.2 77'
def svg_mark(x=0, y=0, size=100, color=None, dot=None):
    return f'<g transform="translate({x} {y}) scale({size/100})"><path d="{MARK_D}" fill="none" stroke="{color or P["forest"]}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/><circle cx="82" cy="70" r="6.5" fill="{dot or color or P["forest"]}"/></g>'

def svg_file(path, w, h, contents, label, bg=None):
    background = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}"><title>{escape(label)}</title>{background}{contents}</svg>', encoding='utf-8')

def logo_svg(kind='primary', stacked=False, mark_only=False):
    color, dot = P['forest'], P['green']
    if kind == 'reverse': color, dot = P['cream'], P['lime']
    elif kind == 'black': color = dot = '#000000'
    elif kind == 'white': color = dot = '#FFFFFF'
    if mark_only: return 100, 100, svg_mark(color=color, dot=dot)
    if stacked:
        wordw = pdfmetrics.stringWidth('EcoVerse', 'MB', 56)
        return 360, 240, svg_mark(130, 8, 100, color, dot) + outline('EcoVerse', (360-wordw)/2, 181, 56, color=color)
    return 510, 118, svg_mark(0, 9, 100, color, dot) + outline('EcoVerse', 116, 86, 74, color=color)

for kind in ['primary', 'reverse', 'black', 'white']:
    for name, stacked, mo in [('logo-horizontal',False,False),('logo-vertical',True,False),('simbolo',False,True)]:
        w,h,body = logo_svg(kind,stacked,mo)
        svg_file(KIT/'logos'/f'ecoverse-{name}-{kind}.svg',w,h,body,'EcoVerse')
svg_file(KIT/'logos/ecoverse-app-icon.svg',128,128,
         '<rect width="128" height="128" rx="30" fill="'+P['forest']+'"/>'+svg_mark(14,14,100,P['cream'],P['lime']), 'Ícone EcoVerse')

def luminance(value):
    nums=[int(value[i:i+2],16)/255 for i in [1,3,5]]
    nums=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in nums]
    return .2126*nums[0]+.7152*nums[1]+.0722*nums[2]
def contrast(a,b):
    aa,bb=sorted([luminance(a),luminance(b)])
    return (bb+.05)/(aa+.05)

W,H=960,640
c=canvas.Canvas(str(PDF),pagesize=(W,H))
c.setTitle('EcoVerse | Guia de marca v1.0')
c.setAuthor('EcoVerse | Projeto UPX')
c.setSubject('Identidade, estratégia e diretrizes para a transição do VestGO')
PAGE=0; CHECKS=[]

def rect(x,y,w,h,color,r=0,stroke=None):
    c.setFillColor(HexColor(color)); c.setStrokeColor(HexColor(stroke or color))
    c.setLineWidth(.8)
    if r: c.roundRect(x,H-y-h,w,h,r,stroke=bool(stroke),fill=1)
    else: c.rect(x,H-y-h,w,h,stroke=bool(stroke),fill=1)

def line(x,y,xx,yy,color=None,width=1):
    c.setStrokeColor(HexColor(color or P['line']));c.setLineWidth(width)
    c.line(x,H-y,xx,H-yy)

def text(txt,x,y,size=14,font='D',color=None):
    c.setFillColor(HexColor(color or P['ink'])); c.setFont(font,size)
    c.drawString(x,H-y-size*.82,txt)
    CHECKS.append(dict(page=PAGE,kind='text',x=x,y=y,w=pdfmetrics.stringWidth(txt,font,size),h=size,text=txt))

def para(txt,x,y,w,size=14,font='D',color=None,leading=None):
    sty=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.47,
                       textColor=HexColor(color or P['ink']),spaceAfter=0)
    p=Paragraph(txt,sty);ww,hh=p.wrap(w,1000);p.drawOn(c,x,H-y-hh)
    CHECKS.append(dict(page=PAGE,kind='paragraph',x=x,y=y,w=w,h=hh,text=txt))
    return hh

def mark(x,y,s,color=None,dot=None):
    c.saveState();c.translate(x,H-y);c.scale(s/100,-s/100)
    c.setStrokeColor(HexColor(color or P['forest']));c.setLineWidth(11);c.setLineCap(1);c.setLineJoin(1)
    p=c.beginPath();p.moveTo(20,50);p.lineTo(82,50);p.curveTo(82,32.327,67.673,18,50,18)
    p.curveTo(32.327,18,18,32.327,18,50);p.curveTo(18,67.673,32.327,82,50,82)
    p.curveTo(56.3,82,62.2,80.2,67.2,77);c.drawPath(p)
    c.setFillColor(HexColor(dot or color or P['green']));c.circle(82,70,6.5,stroke=0,fill=1)
    c.restoreState()

def logo(x,y,width=300,reverse=False,mono=None):
    s=width/510
    color=mono or (P['cream'] if reverse else P['forest'])
    dot=mono or (P['lime'] if reverse else P['green'])
    mark(x,y+9*s,100*s,color,dot)
    text('EcoVerse',x+116*s,y+25.32*s,74*s,'MB',color)

def circle(x,y,r,color,stroke=None):
    c.setFillColor(HexColor(color));c.setStrokeColor(HexColor(stroke or color));c.setLineWidth(1)
    c.circle(x,H-y,r,stroke=bool(stroke),fill=1)

def start(section,title=None,sub=None,dark=False):
    global PAGE
    PAGE+=1
    bg=P['forest'] if dark else P['cream'];fg=P['cream'] if dark else P['forest']
    rect(0,0,W,H,bg)
    text('ECOVERSE',48,28,10,'MB',fg)
    text(section.upper(),675,28,9,'DM',P['lime'] if dark else P['stone'])
    line(48,53,912,53,'#416257' if dark else P['line'])
    if title:text(title,48,78,37,'MB',fg)
    if sub:para(sub,50,126,820,13,color=P['mist'] if dark else P['stone'])
    line(48,595,912,595,'#416257' if dark else P['line'])
    text('GUIA DE MARCA  /  v1.0  /  OUTUBRO 2026',48,610,8.5,'DM',P['mist'] if dark else P['stone'])
    text(f'{PAGE:02d}',889,607,12,'MB',fg)
    c.bookmarkPage(f'p{PAGE}');c.addOutlineEntry(title or section,f'p{PAGE}',0)

def end(): c.showPage()

def pill(txt,x,y,w,bg=None,fg=None):
    rect(x,y,w,28,bg or P['mist'],14);text(txt,x+13,y+8,10,'DB',fg or P['forest'])

def card(x,y,w,h,num,title,body,bg=None):
    rect(x,y,w,h,bg or P['white'],18)
    text(num,x+22,y+22,11,'MB',P['green'])
    text(title,x+22,y+52,21,'MB',P['forest'])
    para(body,x+22,y+91,w-44,13)

def icon(kind,x,y,size=48,color=None):
    color=color or P['forest']; c.saveState();c.translate(x,H-y);c.scale(size/48,-size/48)
    c.setStrokeColor(HexColor(color));c.setFillColor(HexColor(color));c.setLineWidth(2.6);c.setLineCap(1);c.setLineJoin(1)
    p=c.beginPath()
    if kind=='battery':
        c.roundRect(11,7,26,36,4,stroke=1,fill=0);c.line(20,3,28,3);c.line(24,15,24,25);c.line(19,20,29,20);c.line(19,33,29,33)
    elif kind=='electronics':
        c.roundRect(5,7,38,27,4,stroke=1,fill=0);c.line(24,34,24,41);c.line(15,42,33,42);c.line(12,27,36,27)
    elif kind=='lamp':
        p.moveTo(16,31);p.curveTo(15,24,10,24,10,17);p.curveTo(10,0,38,0,38,17);p.curveTo(38,24,33,25,32,31)
        c.drawPath(p);c.line(17,33,31,33);c.line(18,39,30,39);c.line(21,44,27,44)
    elif kind=='oil':
        c.roundRect(18,2,12,7,2,stroke=1,fill=0)
        p.moveTo(18,9);p.lineTo(18,14);p.curveTo(10,18,11,20,11,26);p.lineTo(11,40);p.curveTo(11,45,37,45,37,40);p.lineTo(37,26);p.curveTo(37,20,38,18,30,14);p.lineTo(30,9);c.drawPath(p);c.line(16,30,32,30)
    c.restoreState()

# 01 -------------------------------------------------------------------------
start('Identidade & estratégia',dark=True)
circle(788,316,185,P['green']);circle(788,316,129,P['forest'])
mark(625,150,320,P['cream'],P['lime'])
pill('PROJETO UPX  /  IDENTIDADE 1.0',50,88,226,P['lime'],P['forest'])
logo(47,163,482,True)
text('Cada material,',52,319,46,'MB',P['cream'])
text('um destino certo.',52,373,46,'MB',P['lime'])
para('Estratégia, identidade visual e linguagem para conectar pessoas, pontos de coleta e parceiros de destinação.',54,468,482,17,color=P['cream'])
text('Proposta de marca para avaliação do grupo.',54,556,11,'D',P['mist'])
end()

# 02 -------------------------------------------------------------------------
start('01 / Contexto','O destino faz parte do descarte.', 'A nova marca parte da jornada real que o produto precisa apoiar.')
para('Um material deixou de ser útil para alguém. Isso não encerra a responsabilidade sobre ele. O EcoVerse organiza o próximo passo: entender o que entregar, encontrar um ponto compatível e acompanhar os registros da rede.',50,181,790,20,'M',P['forest'],29)
card(48,310,276,218,'01','Clareza','A pessoa reconhece seu material e entende qual ponto pode recebê-lo. Menos dúvida antes de sair de casa.')
card(342,310,276,218,'02','Conexão','Pontos e operadores compartilham a jornada. A marca representa uma rede com responsabilidades visíveis.')
card(636,310,276,218,'03','Confiança','Cada etapa comunica o que foi registrado. Resultados ambientais dependem de dados e evidências verificáveis.')
text('Escopo inicial: pilhas e baterias, eletrônicos, lâmpadas e óleo de cozinha.',50,556,12,'DB')
end()

# 03 -------------------------------------------------------------------------
start('02 / Leitura do VestGO','Uma base operacional aproveitável.', 'Constatado no código local. Disponibilidade em execução não foi testada nesta etapa.')
rows=[('Entrada e descoberta','Cadastro, login, sessões, 2FA, mapa público e perfis operacionais.'),
      ('Entrega e recebimento','Registro guiado, código/QR e atualização de status com histórico.'),
      ('Rede parceira','Parcerias entre ponto e ONG, solicitação de retirada e aprovação.'),
      ('Logística e gestão','Lotes, despacho, recebimento, fechamento, notificações e governança.')]
for i,(a,b) in enumerate(rows):
    yy=181+i*78
    text(f'0{i+1}',50,yy+5,13,'MB',P['green']);text(a,93,yy,19,'MB')
    para(b,405,yy,479,13);line(93,yy+57,910,yy+57)
rect(48,508,864,61,P['mist'],12)
para('O que muda: “doação de peças” passa a ser “descarte de materiais”. Categorias, aceite, unidades e encerramento precisam de regras próprias; uma troca de textos não resolve essa mudança.',67,522,824,13,'DM')
end()

# 04 -------------------------------------------------------------------------
start('03 / Estratégia','Uma rede que orienta e conecta.')
pill('POSICIONAMENTO PROPOSTO',50,143,210)
para('Para quem quer descartar corretamente, o EcoVerse é a plataforma que conecta materiais, pontos de coleta e operadores parceiros, com orientação clara e acompanhamento dos registros da jornada.',50,195,780,23,'M',P['forest'],32)
line(50,336,910,336)
cols=[('Pessoas','“Onde posso levar este material?”','Acolher a intenção e indicar o próximo passo.'),('Pontos de coleta','“O que recebo e quem retira?”','Dar visibilidade às regras e à operação.'),('Operadores parceiros','“O que retirar e para onde levar?”','Organizar a conexão e a responsabilidade.')]
for i,(t,q,b) in enumerate(cols):
    x=50+i*293;text(t,x,369,19,'MB');para(q,x,407,260,15,'M');para(b,x,465,260,13)
text('Personalidade: próxima, organizada, responsável e otimista.',50,554,13,'DB',P['green'])
end()

# 05 -------------------------------------------------------------------------
start('04 / Rede de destinação','Quem participa de cada etapa.', 'Vocabulário de produto proposto; os parceiros e suas atribuições ainda precisam ser definidos pelo grupo.')
labels=[('Pessoa','Separa e registra'),('Ponto de coleta','Recebe e confere'),('Operador de coleta','Retira e transporta'),('Unidade de destino','Recebe para destinação')]
for i,(a,b) in enumerate(labels):
    x=50+i*219
    circle(x+22,228,20,P['forest']);text(str(i+1),x+17,219,19,'MB',P['cream'])
    if i<3:line(x+48,228,x+199,228,P['green'],3)
    para(a,x,277,195,18,'MB');para(b,x,335,191,13)
rect(48,395,864,150,P['white'],16)
text('Os nomes não são intercambiáveis.',70,418,21,'MB')
para('“Operador de coleta” identifica quem retira e transporta. “Unidade de destinação” identifica o local que recebe para triagem, reciclagem ou tratamento, conforme o material e a operação. Uma empresa pode acumular funções; isso deve aparecer no cadastro.',70,457,806,14)
text('No modelo atual, a ONG reúne recebimento e operação. A separação de atores é uma evolução proposta.',50,558,11,'DM',P['stone'])
end()

# 06 -------------------------------------------------------------------------
start('05 / Assinatura','Um “e” que mostra um caminho.',dark=True)
logo(173,174,610,True)
line(52,364,908,364,'#416257')
for x,num,t,b in [(52,'01','A inicial','O “e” ancora o símbolo no nome EcoVerse, facilitando o reconhecimento.'),(345,'02','O percurso','O traço contínuo conecta a entrada do material às etapas da rede.'),(638,'03','O destino','O ponto separado dá foco à chegada, sem sugerir uma certificação ambiental.')]:
    text(num,x,397,11,'MB',P['lime']);text(t,x,428,23,'MB',P['cream']);para(b,x,471,260,14,color=P['mist'])
end()

# 07 -------------------------------------------------------------------------
start('06 / Construção','Geometria simples. Leitura constante.', 'O símbolo tem desenho próprio. A assinatura usa Manrope 700, convertida em curvas nos arquivos finais.')
rect(48,178,380,372,P['white'],18)
for v in range(0,11):
    line(90+v*28,213,90+v*28,493,P['mist'],.5);line(90,213+v*28,370,213+v*28,P['mist'],.5)
mark(90,213,280)
para('Malha de referência: 100 × 100 unidades.',72,521,340,11,'DM',P['stone'])
items=[('Traço','Espessura de 11 unidades, extremidades e junções arredondadas.'),('Curva','Arco principal com raio de 32 unidades. A abertura preserva a sensação de continuidade.'),('Ponto','Diâmetro de 13 unidades. Mantém presença sem competir com o percurso.'),('Assinatura','Nome inteiro, com E e V maiúsculos: EcoVerse. Não separar “Eco” e “Verse” por cor.')]
y=183
for a,b in items:
    text(a,477,y,19,'MB');hh=para(b,477,y+33,409,13);y+=hh+60
end()

# 08 -------------------------------------------------------------------------
start('07 / Versões','Uma assinatura para cada contexto.', 'Usar os arquivos fornecidos; evitar reconstruir o logotipo por digitação.')
rect(48,177,420,150,P['white'],16);logo(90,216,333)
text('01  Principal / fundo claro',68,297,11,'DB')
rect(488,177,424,150,P['forest'],16);logo(533,216,333,True)
text('02  Reversa / fundo escuro',509,297,11,'DB',P['cream'])
rect(48,346,272,210,P['mist'],16);mark(134,362,95)
text('EcoVerse',111,470,30,'MB');text('03  Vertical',68,528,11,'DB')
rect(338,346,272,210,P['white'],16);logo(363,410,223,mono='#000000')
text('04  Uma tinta',358,528,11,'DB')
rect(628,346,284,210,P['white'],16);rect(707,383,109,109,P['forest'],25);mark(713,389,97,P['cream'],P['lime'])
text('05  Avatar e ícone',650,528,11,'DB')
end()

# 09 -------------------------------------------------------------------------
start('08 / Preservação','Espaço para a marca respirar.')
rect(48,159,523,235,P['white'],16)
c.setDash(4,4);line(88,195,531,195);line(88,348,531,348);line(88,195,88,348);line(531,195,531,348);c.setDash()
logo(116,219,386);text('x',96,252,14,'MB',P['green']);text('x',303,201,14,'MB',P['green'])
para('Área livre mínima = x em todos os lados. x é a espessura do traço do símbolo na escala utilizada.',73,411,466,14)
text('Tamanhos mínimos',618,171,22,'MB')
for i,(a,b) in enumerate([('Horizontal','128 px / 32 mm'),('Vertical','96 px / 25 mm'),('Símbolo isolado','24 px / 6 mm')]):
    text(a,618,222+i*52,13,'DB');text(b,618,243+i*52,12,'D',P['stone'])
rect(618,404,294,140,P['mist'],14)
para('Não esticar, girar, adicionar sombras, trocar cores por categoria ou aplicar sobre imagens sem uma área de contraste estável. Para 16 px, usar o favicon exportado.',638,423,254,13)
text('A assinatura não deve funcionar como selo de material reciclado, licença ou comprovação de destinação.',50,554,11,'DM',P['stone'])
end()

# 10 -------------------------------------------------------------------------
start('09 / Cores','Natureza com presença e precisão.', 'Verde profundo sustenta a confiança. O lima destaca momentos. O fundo quente aproxima a experiência.')
swatches=[('Floresta','forest','Base institucional e títulos.'),('Verde rede','green','Ações e ligações da jornada.'),('Lima destino','lime','Ênfase gráfica e pequenos pontos.'),('Papel','cream','Fundo principal e respiro.'),('Grafite','ink','Texto longo e informação.'),('Névoa','mist','Planos secundários e agrupamentos.')]
for i,(name,key,use) in enumerate(swatches):
    x=48+(i%3)*294;y=180+(i//3)*185
    rect(x,y,276,96,P[key],14)
    fg=P['cream'] if key in ['forest','green','ink'] else P['forest']
    text(P[key].upper(),x+18,y+64,16,'MB',fg)
    text(name,x+1,y+111,17,'MB');para(use,x+1,y+139,272,11.5)
para('Proporção sugerida em comunicação: 60% papel, 25% floresta/grafite, 10% verde/névoa, 5% lima. É uma referência de composição, não uma regra de interface.',50,553,855,11,'DM',P['stone'])
end()

# 11 -------------------------------------------------------------------------
start('10 / Acessibilidade','O contraste também faz parte da marca.', 'Pares calculados em sRGB para cores sólidas. A interface completa será avaliada durante o redesenho.')
pairs=[('Texto principal','ink','cream'),('Título institucional','forest','cream'),('Botão principal','white','green'),('Destaque claro','forest','lime')]
for i,(label,fg,bg) in enumerate(pairs):
    yy=180+i*74
    rect(48,yy,257,53,P[bg],10);text('Encontre um ponto',64,yy+17,17,'MB',P[fg])
    ratio=contrast(P[fg],P[bg]);text(f'{ratio:.2f}:1',339,yy+15,22,'MB',P['forest'])
    text(label,490,yy+17,14,'D');pill('AA / TEXTO NORMAL',730,yy+12,178,P['mist'])
rect(48,493,864,78,P['white'],14)
para('Texto normal: pelo menos 4,5:1. Texto grande: 3:1. Não usar lima para texto sobre papel. Status sempre combinam palavra, ícone e cor; o verde da marca sozinho não confirma uma etapa.',70,511,818,13)
end()

# 12 -------------------------------------------------------------------------
start('11 / Tipografia','Uma voz clara, do título ao detalhe.')
text('Manrope',49,161,49,'MB')
para('Títulos e assinatura · pesos 600 e 700',51,222,415,13,'DM',P['green'])
para('Formas abertas e curvas firmes dão presença ao nome e mantêm a marca próxima. Usar 800 apenas em campanhas de grande escala.',51,260,398,14)
text('DM Sans',497,164,49,'DB')
para('Leitura e interface · pesos 400, 500 e 700',499,222,413,13,'DM',P['green'])
para('Ritmo regular para orientações, endereços e etapas. Os acentos permanecem claros em português. Os números acompanham os registros sem ruído visual.',499,260,394,14)
line(50,358,910,358)
for yy,txt,sz,font in [(386,'Cada material, um destino certo.',31,'MB'),(438,'Encontre um ponto de coleta',23,'M'),(483,'Confira os materiais aceitos antes de levar seu descarte.',15,'D'),(524,'Pilhas · Eletrônicos · Lâmpadas · Óleo de cozinha · 0123456789',12,'DM')]:text(txt,51,yy,sz,font)
text('Escala digital inicial: H1 48/52; H2 32/38; H3 24/30; texto 16/24; rótulo 14/20 (px).',51,558,11,'DM',P['stone'])
end()

# 13 -------------------------------------------------------------------------
start('12 / Linguagem','Falar com clareza. Convidar à ação.', 'Tom próximo, direto e responsável. Orientar sem culpa e descrever etapas com precisão.')
left=[('Convide','“Encontre um ponto para este material.”'),('Explique o próximo passo','“Confira o que o ponto recebe antes de ir.”'),('Informe o registro','“Recebimento confirmado pelo parceiro.”')]
right=[('Evite termos herdados','“Doe suas peças”, “Doador”, “ONG beneficiada”.'),('Evite promessas sem base','“Tudo é reciclado”, “100% sustentável”, “salvamos o planeta”.'),('Evite conclusão antecipada','“Destinação comprovada” ao apenas fechar um lote.')]
for xx,items,color in [(50,left,P['green']),(500,right,P['red'])]:
    for i,(t,b) in enumerate(items):
        yy=185+i*109;text(t,xx,yy,18,'MB',color);para(b,xx,yy+35,392,14)
rect(48,519,864,52,P['forest'],12)
text('Assinatura verbal: Cada material, um destino certo.',70,536,19,'MB',P['cream'])
end()

# 14 -------------------------------------------------------------------------
start('13 / Materiais & ícones','Reconhecer antes de escolher.', 'Ícones de traço arredondado, mesma espessura e rótulos explícitos. Não depender apenas de cor.')
items=[('battery','Pilhas e baterias','Tipos e restrições definidos por parceiro.','mist'),('electronics','Eletrônicos','Subtipos devem estar visíveis no aceite.','bluebg'),('lamp','Lâmpadas','Distinguir os tipos na futura orientação.','mist'),('oil','Óleo de cozinha','Cadastro futuro deve considerar volume.','amberbg')]
for i,(kind,t,b,bg) in enumerate(items):
    x=48+i*219;rect(x,185,207,285,P['white'],17);rect(x+17,204,173,105,P[bg],12)
    icon(kind,x+77,229,53);para(t,x+18,333,175,18,'MB');para(b,x+18,397,170,12.5)
rect(48,493,864,76,P['redbg'],14)
para('<b>Fora do escopo:</b> medicamentos, seringas, perfurocortantes e resíduos de serviços de saúde. Outras famílias só entram após definição de parceiro, aceite e regras específicas.',68,511,821,13)
text('As cores dos ícones são editoriais; não substituem sinalização ou classificação técnica de coletores.',50,578,9.5,'D',P['stone'])
end()

# 15 -------------------------------------------------------------------------
start('14 / Direção de imagem','Materiais reais. Uma rede visível.')
hero=KIT/'images/ecoverse-hero-conceitual.png'
if hero.exists():
    im=Image.open(hero); iw,ih=im.size
    c.drawImage(ImageReader(im),48,H-164-336,width=540,height=336,mask='auto',preserveAspectRatio=True,anchor='c')
else:
    raise RuntimeError('Project hero asset must be saved before final authoring.')
text('Uma estética tátil',628,174,22,'MB')
para('Volumes simples, materiais reconhecíveis e luz suave tornam o tema acessível. O percurso gráfico conecta grupos que permanecem separados.',629,220,268,14)
text('Por que esta escolha',628,339,19,'MB')
para('A imagem apresenta a diversidade do descarte sem recorrer a aterros, catástrofes ou florestas genéricas. O foco fica na ação possível.',629,376,268,14)
para('Arte conceitual gerada por IA. Não representa uma instalação real, parceiro cadastrado, embalagem recomendada ou procedimento técnico de descarte.',51,530,847,12,'DM',P['stone'])
end()

# 16 -------------------------------------------------------------------------
start('15 / Grafismo & movimento','O percurso é parte da identidade.', 'Curvas de 90 graus, extremidades arredondadas e um ponto de destino. Usar como apoio à informação.')
rect(48,179,864,163,P['forest'],18)
c.setStrokeColor(HexColor(P['green']));c.setLineWidth(19);c.setLineCap(1)
p=c.beginPath();p.moveTo(91,H-275);p.lineTo(265,H-275);p.curveTo(315,H-275,315,H-221,366,H-221);p.lineTo(590,H-221);p.curveTo(640,H-221,640,H-292,690,H-292);p.lineTo(841,H-292);c.drawPath(p)
circle(841,292,12,P['lime'])
for i,(a,b) in enumerate([('01 / Entrada','Traço aparece em 800 ms.'),('02 / Conexão','Ponto entra em 250 ms.'),('03 / Repouso','Símbolo completo fica estático.')]):
    x=50+i*293;text(a,x,383,18,'MB');para(b,x,422,261,14)
rect(48,492,864,76,P['white'],14)
para('Movimento pontual, sem rotação contínua nem efeito de carregamento. Respeitar “reduzir movimento” com o símbolo já completo. O traço animado nunca indica progresso logístico real.',68,510,818,13)
end()

# 17 -------------------------------------------------------------------------
start('16 / Aplicações','Uma marca que funciona fora da tela.', 'Peças demonstrativas de identidade. Não identificam parceiros reais nem locais em funcionamento.')
rect(48,174,345,390,P['forest'],16);logo(74,197,220,True)
text('Seu descarte',76,297,32,'MB',P['cream']);text('tem destino.',76,340,32,'MB',P['lime'])
para('Encontre um ponto que recebe o seu material.',77,409,266,17,color=P['cream'])
para('Consulte os materiais aceitos em cada ponto.',77,513,262,10,color=P['mist'])
rect(418,174,494,169,P['white'],16);logo(445,194,213)
text('Registro acompanhado.',446,264,24,'MB');text('Etapas claras para seguir em frente.',446,304,13)
rect(418,366,494,198,P['mist'],16);circle(518,463,65,P['forest']);mark(477,422,82,P['cream'],P['lime'])
text('Ponto de coleta',611,412,22,'MB');para('Materiais aceitos, horários e regras precisam estar visíveis no local e no perfil.',612,454,268,14)
end()

# 18 -------------------------------------------------------------------------
start('17 / Princípios digitais','A identidade precisa ajudar a decidir.', 'Diretrizes para o próximo trabalho de interface; nenhuma tela funcional foi redesenhada nesta entrega.')
rules=[('Começar pelo material','A pessoa escolhe o que descartar. A rede mostra pontos compatíveis e orientações por tipo.'),('Priorizar a ação principal','“Encontrar ponto de coleta” na descoberta; “Registrar descarte” após conferir o ponto e suas regras.'),('Mostrar o responsável','Cada etapa deve identificar quem a registrou e quando. Um evento de entrega não equivale à reciclagem.'),('Servir ao uso no celular','Conteúdo compacto, controles legíveis, mapa com lista alternativa e checagem em 320 px.'),('Tratar informação incompleta','Sem pontos disponíveis, orientar a busca e o contato. Sem evidência final, informar o limite do rastreio.')]
for i,(a,b) in enumerate(rules):
    y=177+i*78;text(f'0{i+1}',50,y+3,13,'MB',P['green']);text(a,92,y,18,'MB');para(b,456,y,440,12.5)
    if i<4:line(92,y+60,911,y+60)
end()

# 19 -------------------------------------------------------------------------
start('18 / Transição','Reaproveitar a base. Adaptar o domínio.', 'Planejamento documental. Backend, banco e site continuam com o comportamento existente.')
rect(48,177,419,370,P['white'],16);text('Estruturas para reaproveitar',70,198,21,'MB')
para('Autenticação e proteção de contas.<br/><br/>Mapa, endereços e perfis públicos.<br/><br/>Governança de perfis e parcerias.<br/><br/>QR, eventos, retiradas e lotes.<br/><br/>Notificações e armazenamento de mídia.',71,249,367,15)
rect(487,177,425,370,P['mist'],16);text('Regras que precisam mudar',509,198,21,'MB')
para('Catálogo, subtipos, unidades e aceite por material.<br/><br/>Separação de coleta e destinação.<br/><br/>Acondicionamento e restrições de recebimento.<br/><br/>Estados finais, documentos e evidências.<br/><br/>Pontuação, e-mails e textos herdados de doação.',510,249,368,14)
para('Não usar OTHER para esconder todos os novos materiais nem reaproveitar o estimador de sacolas/caixas de roupas como orientação de acondicionamento.',50,560,855,11,'DM',P['stone'])
end()

# 20 -------------------------------------------------------------------------
start('19 / Rastreabilidade','O registro deve sustentar a promessa.')
states=[('Cadastro de descarte','Intenção registrada, antes da entrega.'),('Recebido no ponto','Recebimento confirmado no local.'),('Em transporte','Movimentação registrada pelo operador.'),('Recebido pelo parceiro','Chegada ao parceiro confirmada.'),('Destinação comprovada','Somente com evidência específica e verificável.')]
for i,(t,b) in enumerate(states):
    y=171+i*72;circle(65,y+11,10,P['green'] if i<4 else P['blue']);text(t,94,y,18,'MB');para(b,439,y,456,13)
    if i<4:line(65,y+23,65,y+58,P['line'],2)
pill('ETAPA FUTURA / NÃO IMPLEMENTADA',94,532,298,P['bluebg'],P['blue'])
para('O sistema atual não possui entidade própria de unidade destinadora nem comprovante de destinação. O fechamento de lote é operacional; não autoriza, por si só, a última afirmação acima.',439,532,456,12,'DM',P['stone'])
end()

# 21 -------------------------------------------------------------------------
start('20 / Próxima etapa','Da marca ao produto.', 'O kit já pode orientar a discussão visual do grupo. O desenho das telas começa após essa avaliação.')
card(48,178,276,287,'01','Consolidar a marca','Avaliar símbolo, assinatura, paleta e tom. EcoVerse é o nome definido no briefing; esta identidade é a proposta v1.0 para ele.')
card(342,178,276,287,'02','Fechar as regras','Definir parceiros, funções, materiais aceitos, unidades, restrições e qual evento encerra o acompanhamento do usuário.')
card(636,178,276,287,'03','Desenhar a jornada','Redesenhar descoberta, mapa, registro, rastreio e operação com dados locais de demonstração, preservando a integração existente.')
rect(48,492,864,77,P['forest'],14)
para('Critério de avanço: a marca aprovada orienta o visual; as regras acordadas orientam os formulários, permissões e mudanças do backend. O funcionamento será validado em uma etapa própria.',69,510,821,13,color=P['cream'])
end()

# 22 -------------------------------------------------------------------------
start('21 / Fontes & entrega','Referências e limites desta edição.')
sources=[('01 / Código local','Schema Prisma; módulos de doações, parcerias, retiradas, lotes, perfis e autenticação; mapa, navegação, wizard e componentes de marca do frontend.'),('02 / Referência fornecida','ReUse - Um novo destino começa com você. Leitura visual da página pública em 19/10/2026; sem auditoria de funcionamento.'),('03 / Termos de logística reversa','SINIR / Ministério do Meio Ambiente: visão geral e fluxo de pilhas e baterias. Óleo de cozinha é uma família do briefing, não óleo lubrificante.'),('04 / Tipografia e acessibilidade','Google Fonts: Manrope e DM Sans, licenças OFL incluídas no kit. W3C: WCAG 2.2, critério 1.4.3, para parâmetros de contraste.')]
for i,(a,b) in enumerate(sources):
    y=165+i*78;text(a,50,y,16,'MB');para(b,370,y,524,11.5)
links=[('Site de referência','https://reuse-logistica-reversa.mightybud67.chatgpt.site/'),('SINIR / logística reversa','https://www.sinir.gov.br/perfis/logistica-reversa/'),('Google Fonts / Manrope','https://github.com/google/fonts/tree/main/ofl/manrope'),('Google Fonts / DM Sans','https://github.com/google/fonts/tree/main/ofl/dmsans'),('W3C / WCAG 2.2','https://www.w3.org/TR/WCAG22/#contrast-minimum')]
for i,(label,url) in enumerate(links):
    x=50+(i%3)*294;y=496+(i//3)*28;text(label+' >',x,y,10,'DB',P['green']);c.linkURL(url,(x,H-y-14,x+260,H-y+2),relative=0)
para('Entrega: PDF, logos SVG/PNG, fontes, cores e tokens, ícones, arte conceitual, aplicações e amostra de movimento. Consulta de disponibilidade de nome, domínio e registro de marca não faz parte desta edição.',50,557,851,10,'D',P['stone'])
end()
c.save()

# Portable vector icons, no font dependency.
icon_paths={
 'pilhas-baterias':'<rect x="11" y="7" width="26" height="36" rx="4"/><path d="M20 3h8M24 15v10M19 20h10M19 33h10"/>',
 'eletronicos':'<rect x="5" y="7" width="38" height="27" rx="4"/><path d="M24 34v7M15 42h18M12 27h24"/>',
 'lampadas':'<path d="M16 31C15 24 10 24 10 17C10 0 38 0 38 17C38 24 33 25 32 31M17 33h14M18 39h12M21 44h6"/>',
 'oleo-cozinha':'<rect x="18" y="2" width="12" height="7" rx="2"/><path d="M18 9v5C10 18 11 20 11 26v14C11 45 37 45 37 40V26C37 20 38 18 30 14V9M16 30h16"/>'}
(KIT/'icons').mkdir(exist_ok=True)
for name,body in icon_paths.items():
    svg_file(KIT/'icons'/f'{name}.svg',48,48,f'<g fill="none" stroke="{P["forest"]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">{body}</g>',name.replace('-',' '))

# A campaign poster is a brand application, not a website screen.
poster=svg_mark(48,42,100,P['cream'],P['lime'])+outline('EcoVerse',166,119,71,color=P['cream'])
poster+=outline('Seu descarte',55,355,76,color=P['cream'])+outline('tem destino.',55,447,76,color=P['lime'])
poster+=outline('Encontre um ponto que recebe',58,553,30,'D',P['cream'])+outline('o seu material.',58,594,30,'D',P['cream'])
poster+='<path d="M65 780H235Q295 780 295 720T355 660H570" fill="none" stroke="'+P['green']+'" stroke-width="23" stroke-linecap="round"/><circle cx="570" cy="660" r="16" fill="'+P['lime']+'"/>'
poster+=outline('Consulte os materiais aceitos em cada ponto.',58,880,20,'D',P['cream'])
svg_file(KIT/'applications/ecoverse-cartaz-conceitual.svg',720,960,poster,'Cartaz conceitual EcoVerse',P['forest'])

motion=f'''<style>
 .route {{stroke-dasharray:300;stroke-dashoffset:300;animation:draw .8s ease-out forwards}}
 .destination {{opacity:0;animation:appear .25s ease-out .8s forwards}}
 @keyframes draw {{to {{stroke-dashoffset:0}}}}
 @keyframes appear {{to {{opacity:1}}}}
 @media (prefers-reduced-motion:reduce) {{.route{{animation:none;stroke-dashoffset:0}}.destination{{animation:none;opacity:1}}}}
 </style><path class="route" d="{MARK_D}" fill="none" stroke="{P['forest']}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/><circle class="destination" cx="82" cy="70" r="6.5" fill="{P['green']}"/>'''
svg_file(KIT/'motion/ecoverse-intro.svg',100,100,motion,'EcoVerse: percurso e destino')

tokens={'brand':'EcoVerse','version':'1.0','colors':P,'typography':{'heading':'Manrope','body':'DM Sans','headingWeights':[600,700],'bodyWeights':[400,500,700]},'spacing':[4,8,12,16,24,32,48,64],'radius':{'control':12,'card':20},'motion':{'introMs':800,'destinationMs':250,'reducedMotion':'static'},'contrast':[{'foreground':P[a],'background':P[b],'ratio':round(contrast(P[a],P[b]),4)} for _,a,b in pairs]}
(KIT/'brand-tokens.json').write_text(json.dumps(tokens,ensure_ascii=False,indent=2),encoding='utf-8')
css='/* Proposta EcoVerse v1.0. Tokens de referência, ainda não aplicados ao site. */\n:root {\n'
css+='\n'.join(f'  --ecoverse-{k}: {v};' for k,v in P.items())
css+='\n  --ecoverse-font-heading: "Manrope", sans-serif;\n  --ecoverse-font-body: "DM Sans", sans-serif;\n}\n'
(KIT/'brand-tokens.css').write_text(css,encoding='utf-8')

# Raster previews are rendered from vector PDF, preserving transparent alpha.
for kind in ['primary','reverse','black','white']:
    for name in ['logo-horizontal','simbolo']:
        mo=name=='simbolo';fw,fh=(100,100) if mo else (510,118)
        path=TMP/f'{name}-{kind}.pdf';cc=canvas.Canvas(str(path),pagesize=(fw,fh))
        prevc,prevh=c,H;c=cc;H=fh
        co,do=(P['cream'],P['lime']) if kind=='reverse' else (('#000000','#000000') if kind=='black' else (('#FFFFFF','#FFFFFF') if kind=='white' else (P['forest'],P['green'])))
        if mo:mark(0,0,100,co,do)
        else:logo(0,0,510,reverse=kind=='reverse',mono=co if kind in ['black','white'] else None)
        cc.save();c,H=prevc,prevh
        doc=pymupdf.open(path);doc[0].get_pixmap(matrix=pymupdf.Matrix(3,3),alpha=True).save(KIT/'logos'/f'ecoverse-{name}-{kind}.png');doc.close()

for size in [16,32,48,180,192,512]:
    path=TMP/'icon-render.pdf';cc=canvas.Canvas(str(path),pagesize=(128,128));prevc,prevh=c,H;c=cc;H=128
    rect(0,0,128,128,P['forest'],30);mark(14,14,100,P['cream'],P['lime']);cc.save();c,H=prevc,prevh
    doc=pymupdf.open(path);doc[0].get_pixmap(matrix=pymupdf.Matrix(size/128,size/128),alpha=True).save(KIT/'logos'/f'ecoverse-icon-{size}.png');doc.close()
Image.open(KIT/'logos/ecoverse-icon-512.png').save(KIT/'logos/ecoverse-favicon.ico',sizes=[(16,16),(32,32),(48,48)])

doc=pymupdf.open(PDF)
for n in range(len(doc)):
    doc[n].get_pixmap(matrix=pymupdf.Matrix(1.2,1.2),alpha=False).save(TMP/f'page-{n+1:02}.png')
doc[0].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5),alpha=False).save(KIT/'images/ecoverse-capa.png')
for sheet in range(3):
    nums=list(range(sheet*8,min((sheet+1)*8,len(doc))))
    board=Image.new('RGB',(1000,math.ceil(len(nums)/2)*365),'#d1d7d1')
    draw=ImageDraw.Draw(board)
    for j,n in enumerate(nums):
        im=Image.open(TMP/f'page-{n+1:02}.png').convert('RGB');im.thumbnail((480,320))
        xx=10+(j%2)*500;yy=10+(j//2)*365;board.paste(im,(xx,yy));draw.text((xx,yy+327),f'{n+1:02d}',fill='#153f35')
    board.save(TMP/f'contact-{sheet+1}.png')
extracted='\n'.join(page.get_text() for page in doc)
(TMP/'guide-extracted.txt').write_text(extracted,encoding='utf-8')
doc.close()
issues=[v for v in CHECKS if v['x']<0 or v['x']+v['w']>W+1 or v['y']+v['h']>H+1]
(TMP/'layout-checks.json').write_text(json.dumps({'pageCount':PAGE,'boundsIssues':issues,'contrast':tokens['contrast']},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pdf':str(PDF),'pages':PAGE,'boundsIssues':len(issues),'contrast':tokens['contrast']},ensure_ascii=False))
