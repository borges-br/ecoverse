'use client';

import { useState } from 'react';
import Link from 'next/link';
import { MapPin, ScanLine, Truck } from 'lucide-react';

const steps = [
  {title:'Escolha o ponto',icon:MapPin,text:'Busque pelo material e confira o endereço e o horário.',href:'/mapa',action:'Buscar pontos'},
  {title:'Entregue com o QR',icon:ScanLine,text:'Registre os materiais e apresente o QR no ponto.',href:'/descartar',action:'Registrar descarte'},
  {title:'Consulte as etapas',icon:Truck,text:'Veja o recebimento, o transporte e a chegada ao parceiro.',href:'/rastreio',action:'Meus descartes'},
];

export function CollectionJourney() {
  const [selected,setSelected] = useState(0);
  const current = steps[selected];
  return <section className="eco-container eco-process" id="jornada" aria-labelledby="eco-process-title">
    <h2 id="eco-process-title">Como funciona</h2>
    <div className="eco-process-tabs" role="tablist" aria-label="Etapas da entrega">
      <div className="eco-process-line" aria-hidden="true"><svg viewBox="0 0 100 12" preserveAspectRatio="none"><path d="M0 6h100"/><path className="eco-process-progress" d="M0 6h100" pathLength="1" style={{strokeDashoffset:1-selected/2}}/></svg><span style={{left:`${selected*50}%`}}/></div>
      {steps.map((step,index)=><button key={step.title} id={`eco-process-${index}`} role="tab" type="button" aria-selected={selected===index} aria-controls="eco-process-detail" tabIndex={selected===index?0:-1}
        onClick={()=>setSelected(index)} onKeyDown={event=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(event.key)){event.preventDefault();const next=event.key==='Home'?0:event.key==='End'?2:(index+(event.key==='ArrowRight'?1:2))%3;setSelected(next);document.getElementById(`eco-process-${next}`)?.focus();}}}>
        <span className="eco-process-station"><step.icon size={24}/></span><span>{index+1}. {step.title}</span>
      </button>)}
    </div>
    <div id="eco-process-detail" role="tabpanel" aria-labelledby={`eco-process-${selected}`} className="eco-process-detail" tabIndex={0}>
      <p key={selected}>{current.text}</p><Link href={current.href}>{current.action}</Link>
    </div>
  </section>;
}
