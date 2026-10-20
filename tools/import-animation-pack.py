"""Inspect user-supplied SVGs as data; copy only reviewed adaptations to public/."""
from pathlib import Path
import zipfile,re,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
source=root/'docs/ecoverse/animation-reference';source.mkdir(parents=True,exist_ok=True)
public=root/'web/public/ecoverse/motion';public.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(Path('C:/Users/natha/Downloads/ecoverse_svg_animations_pack.zip')) as z:
    for item in z.infolist():
        if not item.filename.endswith('.svg'):continue
        data=z.read(item);tree=ET.fromstring(data)
        assert not tree.findall('.//{http://www.w3.org/2000/svg}script')
        assert not tree.findall('.//{http://www.w3.org/2000/svg}foreignObject')
        assert not any(k.startswith('on') for e in tree.iter() for k in e.attrib)
        text=data.decode('utf-8');name=Path(item.filename).name
        (source/name).write_text(text,encoding='utf-8')
        # Static inspection previews are not production assets.
        preview=re.sub(r'@import\s+url\(.*?\);\s*','',text)
        preview=preview.replace('</style>','* {animation:none!important;stroke-dashoffset:0!important;opacity:1!important}</style>')
        (root/'tmp'/('animation-preview-'+name)).write_text(preview,encoding='utf-8')
        if name[:2] not in ['06','07','08','09']:continue
        # Crop the visual field; labels remain semantic HTML outside the SVG.
        body=re.search(r'<g transform="translate\(74, 38\) scale\(1.5\)">(.*?)</g>',text,re.S)
        assert body,name
        i=int(name[:2])-5
        color='#DDEAF5' if i==2 else '#F4E5C9' if i==4 else '#DCE8DE'
        shape=body.group(1).replace(f'mat-stroke-{i}','eco-draw')
        content=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 140" fill="none"><style>
.eco-draw{{stroke:#153F35;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:200;stroke-dashoffset:200;animation:draw .8s ease-out forwards}}
.eco-dot{{opacity:0;animation:dot .25s ease-out .8s forwards}}@keyframes draw{{to{{stroke-dashoffset:0}}}}@keyframes dot{{to{{opacity:1}}}}
@media(prefers-reduced-motion:reduce){{.eco-draw{{animation:none;stroke-dashoffset:0}}.eco-dot{{animation:none;opacity:1}}}}
</style><rect x="10" y="10" width="200" height="120" rx="12" fill="{color}"/><g transform="translate(74 38) scale(1.5)">{shape}</g><circle class="eco-dot" cx="182" cy="34" r="6" fill="#28735A"/></svg>'''
        (public/f'material-{i}.svg').write_text(content,encoding='utf-8')
(public/'percurso.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 864 148" fill="none"><style>.route{stroke-dasharray:820;stroke-dashoffset:820;animation:draw .8s ease-out forwards}.dot{opacity:0;animation:arrive .25s ease-out .8s forwards}@keyframes draw{to{stroke-dashoffset:0}}@keyframes arrive{to{opacity:1}}@media(prefers-reduced-motion:reduce){.route{animation:none;stroke-dashoffset:0}.dot{animation:none;opacity:1}}</style><rect width="864" height="148" rx="18" fill="#153F35"/><path class="route" d="M43 96H217C267 96 267 42 318 42H542C592 42 592 113 642 113H793" stroke="#28735A" stroke-width="19" stroke-linecap="round"/><circle class="dot" cx="793" cy="113" r="12" fill="#CBEA73"/></svg>''',encoding='utf-8')
(source/'README.md').write_text('''# Pacote complementar de animações

Origem: arquivo fornecido pelo usuário, criado com Gemini Argon, recebido em 19/10/2026.

As 12 fontes foram inspecionadas como SVG. A interface aproveita somente os desenhos dos ícones 06-09 e o percurso 04, adaptados em `web/public/ecoverse/motion/`.

Adaptações: entrada de 800 ms, ponto em 250 ms e estado final estático; retirada de imports remotos de fontes e de textos duplicados; respeito a reduzir movimento. O logotipo principal continua usando o componente aprovado. Os diagramas 11/12 não são usados como estado operacional, e a etapa futura de comprovação não é apresentada como implementada.
''',encoding='utf-8')
print('12 SVG sources inspected; 5 selective adaptations prepared.')
