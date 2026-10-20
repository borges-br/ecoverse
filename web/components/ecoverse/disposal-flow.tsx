'use client';
import { useEffect, useRef, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { useSession } from 'next-auth/react';
import Link from 'next/link';
import QRCode from 'react-qr-code';
import { ArrowLeft, ArrowRight, Check, MapPin, Plus, Trash2, Info, ScanLine } from 'lucide-react';
import { createDonation, getCollectionPoint, getNearbyPoints, type CollectionPoint, type DonationRecord } from '@/lib/api';
import { MATERIALS, MATERIAL_LABELS, isMaterialCategory, formatMaterialQuantity, type MaterialCategory } from '@/lib/materials';
import { BrandLoading } from '@/components/branding/ecoverse-brand';
import { formatAddressSummary } from '@/lib/address';

type DraftItem = { id: string; category: MaterialCategory; quantity: number; name: string };
const DRAFT_KEY = 'ecoverse:disposal-draft-v1';
function validItem(item: DraftItem) { return Number.isFinite(item.quantity) && item.quantity > 0 && item.quantity <= 1000 && (item.category === 'COOKING_OIL' ? Math.abs(item.quantity * 100 - Math.round(item.quantity * 100)) < 1e-7 : Number.isInteger(item.quantity)); }
function compatible(point: CollectionPoint, items: DraftItem[]) { return point.role === 'COLLECTION_POINT' && point.donationEligibility?.canDonateHere === true && items.every(item => point.acceptedCategories.includes(item.category)); }

export function DisposalFlow() {
  const { data: session, status } = useSession(); const search = useSearchParams();
  const [step, setStep] = useState(0); const [items, setItems] = useState<DraftItem[]>([]); const [notes, setNotes] = useState('');
  const [points, setPoints] = useState<CollectionPoint[]>([]); const [point, setPoint] = useState<CollectionPoint | null>(null);
  const [query, setQuery] = useState(''); const [loading, setLoading] = useState(false); const [error, setError] = useState('');
  const [ready, setReady] = useState(false); const [confirmed, setConfirmed] = useState(false); const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<DonationRecord | null>(null);
  const [draftSaved, setDraftSaved] = useState(false);
  const surface = useRef<HTMLElement>(null);
  const previousStep = useRef(step);
  const success = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!result) return;
    window.scrollTo({top:0,behavior:'auto'});
    const heading = success.current?.querySelector('h1');
    if (heading) { heading.tabIndex = -1; heading.focus({preventScroll:true}); }
  },[result]);
  useEffect(() => {
    if (previousStep.current === step) return;
    previousStep.current = step;
    const heading = surface.current?.querySelector('h2');
    if (heading) { heading.tabIndex = -1; heading.focus({preventScroll:true}); heading.scrollIntoView({block:'start',behavior:'auto'}); }
  },[step]);

  useEffect(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(DRAFT_KEY) ?? 'null');
      if (saved && Array.isArray(saved.items)) {
        setItems(saved.items.filter((i: DraftItem) => i && typeof i.id === 'string' && typeof i.name === 'string' && isMaterialCategory(i.category) && validItem(i)));
        setNotes(typeof saved.notes === 'string' ? saved.notes.slice(0,600) : '');
      } else if (isMaterialCategory(search.get('material'))) {
        setItems([{ id: crypto.randomUUID(), category: search.get('material') as MaterialCategory, quantity:1, name:'' }]);
      }
    } catch { /* Storage may be unavailable. The flow remains usable. */ }
    setReady(true);
  // Restore once. Query changes only apply a selected point below.
  }, []);
  useEffect(() => { if (!ready || result) return; try { localStorage.setItem(DRAFT_KEY, JSON.stringify({ items, notes })); setDraftSaved(true); } catch { setDraftSaved(false); /* Registration works without local storage. */ } }, [ready, items, notes, result]);
  useEffect(() => {
    const id = search.get('selectedPointId'); if (!id) return; let active = true;
    getCollectionPoint(id, { forDonation:true }).then(p => { if (active) { setPoint(p); setStep(0); } }).catch(() => { if (active) setError('Não foi possível consultar o ponto escolhido. Tente selecionar novamente.'); });
    return () => { active = false; };
  }, [search]);
  useEffect(() => { setConfirmed(false); }, [items, point]);
  useEffect(() => {
    if (step !== 1) return; let active = true; setLoading(true); setError('');
    const timer = setTimeout(() => {
      getNearbyPoints({ role:'COLLECTION_POINT', forDonation:true, limit:50, search:query.trim().length >= 2 ? query.trim() : undefined, accessToken:session?.user?.accessToken })
        .then(r => { if (active) setPoints(r.data.filter(p => compatible(p,items))); })
        .catch(() => { if (active) setError('Não conseguimos consultar a rede agora. Mantenha esta página aberta e tente novamente.'); })
        .finally(() => { if (active) setLoading(false); });
    },250);
    return () => { active = false; clearTimeout(timer); };
  }, [step,query,items,session?.user?.accessToken]);
  function add(category: MaterialCategory) { setItems(current => [...current,{id:crypto.randomUUID(),category,quantity:1,name:''}]); }
  function update(id: string, changes: Partial<DraftItem>) { setItems(current => current.map(item => item.id === id ? {...item,...changes} : item)); }
  async function submit() {
    if (!session?.user?.accessToken || !point || !confirmed || submitting || !items.length || !items.every(validItem) || !compatible(point,items)) return;
    setSubmitting(true);setError('');
    try {
      const created = await createDonation({ collectionPointId:point.id, notes:notes.trim() || undefined, items:items.map(item => ({ name:item.name.trim() || MATERIAL_LABELS[item.category], category:item.category, quantity:item.quantity, condition:'GOOD' as const })), packages:[] },session.user.accessToken);
      setResult(created); try { localStorage.removeItem(DRAFT_KEY); } catch { /* Server registration succeeded. */ }
    } catch(e) { setError(e instanceof Error ? e.message : 'Não foi possível registrar. Confira os dados e tente novamente.'); } finally { setSubmitting(false); }
  }
  if (status === 'loading' || !ready) return <BrandLoading/>;
  if (session?.user?.role !== 'DONOR') return <div className="eco-workspace"><h1>Esta área é para quem vai descartar.</h1><p>Seu perfil parceiro mantém suas ferramentas de recebimento, retirada e acompanhamento.</p><Link className="eco-button" href="/operacoes">Abrir operações<ArrowRight size={17}/></Link></div>;
  if (result) return <div ref={success} className="eco-workspace eco-success"><span className="eco-success-icon"><Check size={26}/></span><h1>Descarte registrado</h1><p>Apresente o QR ao entregar os materiais no ponto.</p><div className="eco-qr"><QRCode value={result.code} size={180}/><strong>{result.code}</strong></div><div className="eco-notice"><MapPin size={22}/><div><strong>{point?.organizationName ?? point?.name}</strong><p>{point ? formatAddressSummary(point) : ''}</p></div></div><div className="eco-form-actions"><Link href={`/rastreio/${result.id}`} className="eco-button">Acompanhar descarte<ArrowRight size={17}/></Link><Link href="/inicio" className="eco-text-link">Voltar ao início</Link></div></div>;
  const canNext = step === 0 ? items.length > 0 && items.every(validItem) : Boolean(point && compatible(point,items));
  return <div className="eco-workspace eco-disposal"><div className="eco-workspace-title"><div><h1>Registrar descarte</h1><p>Informe os materiais e escolha onde entregar.</p></div><span className="eco-draft-note">{draftSaved ? 'Rascunho salvo neste dispositivo' : 'Rascunho disponível nesta página'}</span></div>
    <ol className="eco-stepper" aria-label="Etapas do registro">{['Seus materiais','Ponto e orientações','Revisar e confirmar'].map((label,i) => <li key={label} aria-current={step === i ? 'step' : undefined} className={i <= step ? 'is-active' : ''}><span>{i < step ? <Check size={15}/> : i+1}</span>{label}</li>)}</ol>
    {error && <div className="eco-form-error" role="alert">{error}</div>}
    <div className="eco-flow-grid"><section key={step} ref={surface} className="eco-form-surface">
      {step === 0 && <><h2>O que você vai entregar?</h2><p className="eco-field-hint">Adicione os materiais e informe a quantidade. Óleo de cozinha é registrado em litros.</p><div className="eco-material-picker eco-flow-picker">{MATERIALS.map(m => <button key={m.id} type="button" onClick={() => add(m.id)} disabled={items.length >= 20}><m.icon size={22}/><span>{m.label}</span><Plus size={14}/></button>)}</div><div className="eco-draft-items">{items.map(item => <div className="eco-draft-item" key={item.id}><div className="eco-item-title"><strong>{MATERIAL_LABELS[item.category]}</strong><button type="button" onClick={() => setItems(current => current.filter(i => i.id !== item.id))} aria-label={`Remover ${MATERIAL_LABELS[item.category]}`}><Trash2 size={17}/></button></div><div className="eco-item-fields"><label>Tipo ou descrição <span>(opcional)</span><input value={item.name} maxLength={120} onChange={e => update(item.id,{name:e.target.value})} placeholder={item.category === 'LAMPS' ? 'Ex.: lâmpada LED' : 'Identifique o material'}/></label><label>Quantidade ({item.category === 'COOKING_OIL' ? 'litros' : 'unidades'})<input type="number" inputMode={item.category === 'COOKING_OIL' ? 'decimal' : 'numeric'} min={item.category === 'COOKING_OIL' ? .01 : 1} max={1000} step={item.category === 'COOKING_OIL' ? .01 : 1} value={item.quantity || ''} onChange={e => update(item.id,{quantity:Number(e.target.value)})}/></label></div>{!validItem(item) && <p className="eco-inline-error">Confira a quantidade e a unidade deste material.</p>}</div>)}</div>{items.length === 0 && <div className="eco-empty-inline"><Plus size={26}/><p>Escolha acima o primeiro material.</p></div>}</>}
      {step === 1 && <><h2>Ponto de coleta</h2><p className="eco-field-hint">Pontos que recebem os materiais selecionados. Confira as condições de entrega.</p><label className="eco-form-label">Buscar ponto, bairro ou cidade<input value={query} onChange={e => setQuery(e.target.value)} placeholder="Digite para buscar" maxLength={120}/></label><Link href="/mapa?mode=select-point&returnTo=%2Fdescartar" className="eco-text-link eco-map-action"><MapPin size={16}/> Escolher pelo mapa<ArrowRight size={15}/></Link>{loading ? <BrandLoading label="Consultando os pontos da rede…"/> : <div className="eco-point-options">{points.map(p => <button key={p.id} type="button" className={point?.id === p.id ? 'is-selected' : ''} onClick={() => setPoint(p)}><MapPin size={21}/><span><strong>{p.organizationName ?? p.name}</strong><small>{formatAddressSummary(p)}</small><small>{p.openingHours || 'Consulte o horário no perfil do ponto.'}</small></span>{point?.id === p.id && <Check size={19}/>}</button>)}{!points.length && !error && <div className="eco-empty-inline"><MapPin size={28}/><p>Nenhum ponto compatível encontrado. Tente outra busca ou consulte o mapa.</p></div>}</div>}{point && compatible(point,items) && <div className="eco-point-guidance"><h3>{point.organizationName ?? point.name}</h3><p>{point.publicNotes || 'Confira as condições de entrega com o ponto antes de levar os materiais.'}</p>{point.rules?.length ? <ul>{point.rules.map(rule => <li key={rule}>{rule}</li>)}</ul> : null}{point.nonAcceptedItems?.length ? <p><strong>Não recebe:</strong> {point.nonAcceptedItems.join(', ')}.</p> : null}<Link href={`/mapa/${point.id}`} target="_blank" rel="noopener noreferrer" className="eco-text-link">Consultar perfil completo<ArrowRight size={15}/></Link></div>}</>}
      {step === 2 && <><h2>Revisar entrega</h2><p className="eco-field-hint">Após registrar, apresente o QR no ponto.</p><div className="eco-review-items">{items.map(item => <div key={item.id}><span>{item.name || MATERIAL_LABELS[item.category]}</span><strong>{formatMaterialQuantity(item)}</strong></div>)}</div><div className="eco-point-guidance"><h3><MapPin size={19}/> {point?.organizationName ?? point?.name}</h3><p>{point ? formatAddressSummary(point) : ''}</p><p>{point?.openingHours}</p></div><label className="eco-form-label">Observações <span>(opcional)</span><textarea value={notes} onChange={e => setNotes(e.target.value)} rows={3} maxLength={600}/></label><label className="eco-consent"><input type="checkbox" checked={confirmed} onChange={e => setConfirmed(e.target.checked)}/><span>Conferi os tipos de materiais, as condições e as orientações de recebimento do ponto escolhido.</span></label><div className="eco-notice"><ScanLine size={21}/><p>O recebimento confirmado vale <strong>10 pontos de participação</strong>.</p></div></>}
      <div className="eco-form-actions"><button type="button" className="eco-text-link" disabled={step === 0 || submitting} onClick={() => {setStep(s => s-1);setError('');}}><ArrowLeft size={17}/> Voltar</button>{step < 2 ? <button className="eco-button" type="button" disabled={!canNext} onClick={() => {setStep(s => s+1);setError('');}}>Continuar<ArrowRight size={17}/></button> : <button className="eco-button" type="button" disabled={!confirmed || submitting || !canNext} onClick={submit}>{submitting ? 'Registrando…' : 'Registrar e gerar QR'}<ScanLine size={18}/></button>}</div>
    </section><Link href="/materiais" className="eco-text-link">Guia de materiais</Link></div>
  </div>;
}
