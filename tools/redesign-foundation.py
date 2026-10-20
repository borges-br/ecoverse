from pathlib import Path
import re, shutil
root=Path(__file__).resolve().parents[1]
# Public copy changes only. English identifiers, API paths, persisted keys,
# environment variables and role/status enums remain compatible.
phrases=[
 ('Nova doação','Novo descarte'),('Nova doacao','Novo descarte'),('nova doação','novo descarte'),('nova doacao','novo descarte'),
 ('Minha doação','Meu descarte'),('minha doação','meu descarte'),('Sua doação','Seu descarte'),('sua doação','seu descarte'),
 ('Uma doação','Um descarte'),('uma doação','um descarte'),('a doação','o descarte'),('A doação','O descarte'),
 ('da doação','do descarte'),('na doação','no descarte'),('esta doação','este descarte'),('Esta doação','Este descarte'),
 ('Doações','Descartes'),('doações','descartes'),('Doacoes','Descartes'),('doacoes','descartes'),
 ('Doação','Descarte'),('doação','descarte'),('Doacao','Descarte'),
 ('Doadores','Participantes'),('doadores','participantes'),('Doador','Participante'),('doador','participante'),
 ('ONGs','Operadores'),('ONG','Operador'),
 ('VestGO','EcoVerse'),('MOSFET','EcoVerse'),('Mosfet','EcoVerse'),
 ('Distribuídas','Finalizadas'),('distribuídas','finalizadas'),('Distribuída','Finalizado'),('distribuída','finalizado'),
 ('Distribuição social','Processamento informado'),('distribuição social','processamento informado'),
 ('Solidariedade','Responsabilidade'),('solidariedade','responsabilidade ambiental'),
 ('Solidário','Ambiental'),('solidário','ambiental'),('Solidária','Ambiental'),('solidária','ambiental'),
 ('Doar com proposito','Descarte com destino'),('Doacao com proposito','Cada material, um destino certo'),
]
files=list((root/'web/app').rglob('*.tsx'))+list((root/'web/components').rglob('*.tsx'))+list((root/'web/lib').rglob('*.ts'))
files+=list((root/'api/src').rglob('*.ts'))
for p in files:
    s=p.read_text('utf-8');old=s
    for a,b in phrases:s=s.replace(a,b)
    # Grammar adjustments after the domain noun changed gender.
    s=re.sub(r'([Dd]escarte) (registrada|criada|cancelada|recebida|confirmada|distribuída|vinculada)',lambda m:m[1]+' '+m[2][:-1]+'o',s)
    s=s.replace('Operador parceira','Operador parceiro').replace('operador parceira','operador parceiro')
    s=s.replace('para a Operador','para o operador').replace('pela Operador','pelo operador').replace('da Operador','do operador').replace('à Operador','ao operador').replace('a Operador','o operador')
    if old!=s:p.write_text(s,encoding='utf-8')

kit=root/'output/branding/ecoverse-v1'
pub=root/'web/public/ecoverse';pub.mkdir(exist_ok=True)
for folder in ['logos','icons']:
    for p in (kit/folder).glob('*.svg'):shutil.copy2(p,pub/p.name)
for p in (kit/'logos').glob('ecoverse-icon-*.png'):shutil.copy2(p,pub/p.name)
for name in ['Manrope[wght].ttf','DMSans[opsz,wght].ttf','manrope-OFL.txt','dmsans-OFL.txt']:
    shutil.copy2(kit/'fonts'/name,pub/name.replace('[wght]','-variable').replace('[opsz,wght]','-variable'))
shutil.copy2(kit/'logos/ecoverse-favicon.ico',root/'web/app/favicon.ico')
shutil.copy2(kit/'logos/ecoverse-icon-180.png',root/'web/app/apple-icon.png')

tail=root/'web/tailwind.config.ts';s=tail.read_text('utf-8')
colors={'#006a62':'#28735A','#00544d':'#205C49','#00333c':'#153F35','#e6f4f3':'#EAF0E6','#b2e8e3':'#CBEA73','#21d3c4':'#CBEA73','#f2f4f5':'#F4F3EA','#f6f3ec':'#F4F3EA','#0a1f22':'#102C25','#0f2a2e':'#183D32','#1a1a1a':'#23352D'}
for a,b in colors.items():s=s.replace(a,b)
s=s.replace('["Inter", "ui-sans-serif", "system-ui", "sans-serif"]','["DM Sans", "ui-sans-serif", "system-ui", "sans-serif"]',1)
s=s.replace('["Inter", "ui-sans-serif", "system-ui", "sans-serif"]','["Manrope", "ui-sans-serif", "system-ui", "sans-serif"]')
tail.write_text(s,encoding='utf-8')
css=root/'web/styles/globals.css';s=css.read_text('utf-8')
s=re.sub(r"@import url\('https://fonts.googleapis.com[^\n]+\n",'',s)
s=s.replace("font-family: 'Inter', ui-sans-serif, system-ui, sans-serif;","font-family: 'DM Sans', ui-sans-serif, system-ui, sans-serif;")
for a,b in colors.items():s=s.replace(a,b)
css.write_text(s,encoding='utf-8')
print('Identity assets, palette and compatible public copy prepared.')
