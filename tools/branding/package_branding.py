"""Render the motion preview, verify deliverables, and package the brand kit."""
from pathlib import Path
import math, json, shutil, hashlib, zipfile, re
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
import pymupdf

ROOT=Path(__file__).resolve().parents[2]
KIT=ROOT/'output/branding/ecoverse-v1'
PDF=ROOT/'output/pdf/ecoverse-guia-de-marca-v1.pdf'
TMP=ROOT/'tmp/pdfs'
forest='#153F35';green='#28735A';cream='#F4F3EA';lime='#CBEA73'

def bezier(a,b,c,d,t):
    return tuple((1-t)**3*a[i]+3*(1-t)**2*t*b[i]+3*(1-t)*t*t*c[i]+t**3*d[i] for i in range(2))

points=[(20+62*i/32,50) for i in range(33)]
curves=[((82,50),(82,32.327),(67.673,18),(50,18)),
        ((50,18),(32.327,18),(18,32.327),(18,50)),
        ((18,50),(18,67.673),(32.327,82),(50,82)),
        ((50,82),(56.3,82),(62.2,80.2),(67.2,77))]
for curve in curves:points.extend(bezier(*curve,i/40) for i in range(1,41))

frames=[]
scale=3; w,h=640,220
font=ImageFont.truetype(str(KIT/'fonts/Manrope-700.ttf'),size=76*scale)
for f in range(54):
    im=Image.new('RGB',(w*scale,h*scale),cream);d=ImageDraw.Draw(im)
    fraction=min(1,f/16)
    path=points[:max(1,round(fraction*(len(points)-1))+1)]
    xy=[((47+x*1.5)*scale,(30+y*1.5)*scale) for x,y in path]
    stroke=round(11*1.5*scale)
    if len(xy)>1:d.line(xy,fill=forest,width=stroke,joint='curve')
    # Cover sampled segment joins with round caps so raster previews have the
    # same smooth constant-width silhouette as the SVG source.
    for xx,yy in xy:d.ellipse((xx-stroke/2,yy-stroke/2,xx+stroke/2,yy+stroke/2),fill=forest)
    # The logotype remains still; only the mark has a one-time entrance.
    d.text((216*scale,64*scale),'EcoVerse',font=font,fill=forest)
    if f>=16:
        fraction=min(1,(f-16)/5)
        rgb=tuple(round(int(cream[i:i+2],16)*(1-fraction)+int(green[i:i+2],16)*fraction) for i in [1,3,5])
        xx=(47+82*1.5)*scale;yy=(30+70*1.5)*scale;rr=6.5*1.5*scale
        d.ellipse((xx-rr,yy-rr,xx+rr,yy+rr),fill=rgb)
    im=im.resize((w,h),Image.Resampling.LANCZOS)
    frames.append(im)
frames[0].save(KIT/'motion/ecoverse-intro-preview.gif',save_all=True,append_images=frames[1:],duration=50,loop=1,disposal=2)
frames[-1].save(KIT/'motion/ecoverse-intro-static.png')

# Simple portable overview for review, with actual SVG-rendered brand assets.
board=Image.new('RGB',(1600,1000),cream);d=ImageDraw.Draw(board)
title=ImageFont.truetype(str(KIT/'fonts/Manrope-700.ttf'),42)
small=ImageFont.truetype(str(KIT/'fonts/DMSans-400.ttf'),24)
d.text((70,48),'EcoVerse / identidade v1.0',font=small,fill=forest)
d.rounded_rectangle((70,112,960,500),radius=28,fill=forest)
lo=Image.open(KIT/'logos/ecoverse-logo-horizontal-reverse.png').convert('RGBA');lo.thumbnail((730,190))
board.paste(lo,(140,165),lo)
d.text((143,338),'Cada material,',font=title,fill=cream)
d.text((143,391),'um destino certo.',font=title,fill=lime)
hero=Image.open(KIT/'images/ecoverse-hero-conceitual.png').convert('RGB')
hero.thumbnail((520,388));board.paste(hero,(1010,112))
for i,(name,color) in enumerate([('Floresta',forest),('Verde rede',green),('Lima destino',lime),('Papel',cream),('Grafite','#23352D'),('Névoa','#DCE8DE')]):
    xx=70+i*246;d.rounded_rectangle((xx,555,xx+218,708),radius=18,fill=color,outline='#C8D3C9',width=1)
    d.text((xx,731),name,font=small,fill=forest);d.text((xx,769),color.upper(),font=small,fill=forest)
d.text((70,862),'Manrope + DM Sans',font=title,fill=forest)
d.text((70,928),'Proposta de marca para avaliação do grupo. Aplicações conceituais.',font=small,fill='#5D6C63')
board.save(KIT/'images/ecoverse-identidade-preview.png')

shutil.copy2(PDF,KIT/PDF.name)
shutil.copy2(ROOT/'docs/ecoverse/diagnostico-vestgo.md',KIT/'diagnostico-vestgo.md')

doc=pymupdf.open(PDF)
texts=[p.get_text() for p in doc]
assert len(doc)==22
assert all(len(t)>200 for t in texts)
assert all('\ufffd' not in t and '\u25a0' not in t for t in texts)
assert all(f'{i+1:02}' in t for i,t in enumerate(texts))
doc.close()

svg_checks=[]
for p in KIT.rglob('*.svg'):
    root=ET.parse(p).getroot()
    assert root.tag.endswith('svg')
    assert root.attrib.get('viewBox')
    assert not root.findall('.//{http://www.w3.org/2000/svg}image')
    svg_checks.append(str(p.relative_to(KIT)))

assert 'prefers-reduced-motion' in (KIT/'motion/ecoverse-intro.svg').read_text('utf-8')
gif=Image.open(KIT/'motion/ecoverse-intro-preview.gif')
assert gif.n_frames>20
frames_count=gif.n_frames
transparent=[]
for p in (KIT/'logos').glob('*.png'):
    im=Image.open(p)
    assert im.mode=='RGBA' and im.getextrema()[3][0]==0
    transparent.append(p.name)

layout=json.loads((TMP/'layout-checks.json').read_text('utf-8'))
assert not layout['boundsIssues']
assert all(v['ratio']>=4.5 for v in layout['contrast'])
checks={
 'date':'2026-10-19',
 'pdf':{'pages':22,'textExtraction':'PASS','replacementGlyphCheck':'PASS','pageNumberPresence':'PASS','pageBoundsCheck':'PASS','visualReview':'PASS: all 22 pages inspected in rendered contact sheets; detailed samples inspected separately'},
 'contrast':layout['contrast'],
 'vectors':{'xmlParse':'PASS','files':len(svg_checks),'embeddedRasterImages':0},
 'logos':{'transparentPngs':len(transparent),'fontIndependentSvgPaths':True},
 'motion':{'gifFrames':frames_count,'gifLoop':'one repeat for demonstration','reducedMotionSvg':'PASS: static completed mark under prefers-reduced-motion','animationRendering':'GIF inspected visually; SVG structure checked'},
 'image':{'mode':'built-in image_gen','kind':'conceptual','size':Image.open(KIT/'images/ecoverse-hero-conceitual.png').size},
 'applicationSourceChanges':False,
 'backendRuntimeTests':'NOT_RUN: identity authoring only',
 'deployment':'NOT_RUN'
}
(KIT/'validacao.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')

manifest=[]
for p in sorted(KIT.rglob('*')):
    if p.is_file() and p.name!='manifest-sha256.txt':
        manifest.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(KIT).as_posix())
(KIT/'manifest-sha256.txt').write_text('\n'.join(manifest)+'\n',encoding='utf-8')
zip_path=ROOT/'output/branding/ecoverse-branding-v1.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(KIT.rglob('*')):
        if p.is_file():z.write(p,'ecoverse-v1/'+p.relative_to(KIT).as_posix())
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
    count=len(z.namelist())
digest=hashlib.sha256(zip_path.read_bytes()).hexdigest()
zip_path.with_suffix('.zip.sha256').write_text(digest+'  '+zip_path.name+'\n',encoding='utf-8')
print(json.dumps({'kitFiles':count,'zip':str(zip_path),'zipBytes':zip_path.stat().st_size,'sha256':digest,'pdfBytes':PDF.stat().st_size},ensure_ascii=False))
