'use client';

import { useEffect, useRef, useState } from 'react';
import QRCode from 'react-qr-code';
import { Check, Copy, Maximize2, X } from 'lucide-react';

interface CodeQrCardProps {code:string;title:string;description:string;compact?:boolean;className?:string;}

export function CodeQrCard({code,title,description,compact=false,className=''}:CodeQrCardProps) {
  const [copied,setCopied] = useState(false);
  const [expanded,setExpanded] = useState(false);
  const [copyError,setCopyError] = useState(false);
  const close = useRef<HTMLButtonElement>(null);
  const enlarge = useRef<HTMLButtonElement>(null);
  useEffect(()=>{
    if(!expanded)return;
    close.current?.focus();
    function onKey(event:KeyboardEvent) {if(event.key==='Escape')setExpanded(false);if(event.key==='Tab'){event.preventDefault();close.current?.focus();}}
    document.addEventListener('keydown',onKey);
    return ()=>{document.removeEventListener('keydown',onKey);enlarge.current?.focus();};
  },[expanded]);

  async function copy() {
    try {await navigator.clipboard.writeText(code);setCopied(true);setCopyError(false);window.setTimeout(()=>setCopied(false),1800);}
    catch {setCopyError(true);}
  }

  return <div className={`eco-code-card ${compact?'is-compact':''} ${className}`}>
    <button ref={enlarge} className="eco-code-visual" aria-label={`Ampliar QR ${code}`} onClick={()=>setExpanded(true)}>
      <QRCode value={code} size={152} level="M"/><span><Maximize2 size={12}/> Ampliar</span>
    </button>
    <div className="eco-code-info"><p>{title}</p><strong>{code}</strong><small>{description}</small>
      <button type="button" className="eco-code-copy" aria-label={copied ? 'Código copiado' : 'Copiar código'} onClick={copy}>{copied?<Check size={15} className="eco-copy-check"/>:<Copy size={14}/>}<span role="status">{copied?'Copiado':'Copiar código'}</span></button>
      {copyError && <span className="eco-copy-error" role="alert">Selecione o código para copiar.</span>}
    </div>
    {expanded && <div className="eco-qr-overlay"><button className="eco-qr-backdrop" aria-label="Fechar QR ampliado" tabIndex={-1} onClick={()=>setExpanded(false)}/><section role="dialog" aria-modal="true" aria-label={`QR ampliado ${code}`} className="eco-qr-dialog"><button ref={close} className="eco-icon-action" onClick={()=>setExpanded(false)} aria-label="Fechar QR ampliado"><X size={21}/></button><QRCode value={code} size={256} level="M"/><strong>{code}</strong><p>{description}</p></section></div>}
  </div>;
}
