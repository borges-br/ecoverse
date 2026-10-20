import Link from 'next/link';
import { ArrowLeft, Check, ChevronDown, MapPin, Package } from 'lucide-react';
import { auth } from '@/lib/auth';
import { getDonation, getOperationalBatch, type DonationRecord, type OperationalBatchRecord } from '@/lib/api';
import { MATERIAL_LABELS, formatMaterialQuantity, isMaterialCategory } from '@/lib/materials';
import { DONATION_STATUS_CONFIG, DONATION_STATUS_ORDER, formatDonationDateLabel } from '@/components/donations/donation-status';
import { CodeQrCard } from '@/components/operations/code-qr-card';
import { OperationalBatchTraceCard } from '@/components/operations/operational-batch-trace-card';
import { StatusActionPanel } from '@/components/donations/status-action-panel';
import { PostDonationRating } from '@/components/donations/post-donation-rating';

export default async function RastreioDetalhePage({params:routeParams,searchParams:routeSearch}:{params:Promise<{id:string}>;searchParams?:Promise<{celebrate?:string}>}) {
  const params = await routeParams;
  const searchParams = await routeSearch;
  const session = await auth();
  const token = session?.user?.accessToken;
  const role = session?.user?.role ?? 'DONOR';
  if(!token)return null;
  let record:DonationRecord|null = null;
  let batch:OperationalBatchRecord|null = null;
  try {
    record = await getDonation(params.id,token);
    if(role!=='DONOR' && record.operationalBatch)batch=await getOperationalBatch(record.operationalBatch.id,token).catch(()=>null);
  }catch {record=null;}
  if(!record)return <div className="eco-workspace"><h1>Descarte não encontrado</h1><Link href="/rastreio" className="eco-text-link">Voltar aos descartes</Link></div>;

  const config = DONATION_STATUS_CONFIG[record.status];
  const StatusIcon = config.icon;
  // Historical processing events remain readable without adding a future
  // certification stage to new EcoVerse records.
  const stages = record.items.every(item=>isMaterialCategory(item.category)) && record.status!=='DISTRIBUTED'
    ? DONATION_STATUS_ORDER.filter(status=>status!=='DISTRIBUTED') : DONATION_STATUS_ORDER;
  const current = stages.indexOf(record.status);
  const point = record.collectionPoint ?? record.dropOffPoint;
  const received = !['PENDING','CANCELLED'].includes(record.status);
  const partnerLocation = role==='DONOR' ? record.ngo?.serviceRegions?.join(', ') : record.ngo?.address;

  return <div className="eco-trace-page">
    <header className="eco-trace-heading"><Link href="/rastreio"><ArrowLeft size={17}/> Descartes</Link><h1>{record.code}</h1></header>
    <div className="eco-trace-grid">
      <CodeQrCard code={record.code} title={record.status==='CANCELLED'?'QR do registro':'QR da entrega'} description={record.status==='CANCELLED'?'Registro cancelado.':'Apresente ao entregar os materiais.'} className="eco-trace-qr"/>
      <div className="eco-trace-main">
        {searchParams?.celebrate==='registered' && <p className="eco-trace-feedback" role="status"><Check size={16}/> Descarte registrado.</p>}
        {searchParams?.celebrate==='1' && received && <p className="eco-trace-feedback" role="status"><Check size={16}/> Recebimento confirmado.</p>}
        <section className="eco-trace-status"><StatusIcon size={23}/><div><h2>{config.label}</h2><p>{config.description}</p><small>Atualizado em {formatDonationDateLabel(record.latestEvent?.createdAt ?? record.createdAt)}</small></div></section>

        {record.status!=='CANCELLED' && <ol className="eco-trace-stages" style={{gridTemplateColumns:`repeat(${stages.length},minmax(0,1fr))`}} aria-label="Etapas do descarte">{stages.map((status,index)=><li key={status} className={index<=current?'is-done':''} aria-current={status===record.status?'step':undefined}><span>{index<current?<Check size={12}/>:index+1}</span><strong>{DONATION_STATUS_CONFIG[status].label}</strong></li>)}</ol>}

        <section className="eco-trace-section"><h2>Materiais</h2><ul className="eco-trace-items">{record.items.map(item=><li key={item.id}><Package size={18}/><div><strong>{item.name}</strong><small>{MATERIAL_LABELS[item.category] ?? item.category}</small>{item.description && <p>{item.description}</p>}</div><b>{formatMaterialQuantity(item)}</b></li>)}</ul>{record.notes && <p className="eco-trace-notes">{record.notes}</p>}</section>

        <details className="eco-trace-events"><summary><span>Histórico <small>{record.timeline.length} {record.timeline.length===1?'registro':'registros'}</small></span><ChevronDown size={17}/></summary><ol>{[...record.timeline].reverse().map(event=><li key={event.id}><span className="eco-event-dot"/><div><strong>{DONATION_STATUS_CONFIG[event.status].label}</strong><p>{event.description}</p>{event.location && <small>{event.location}</small>}<time dateTime={event.createdAt}>{formatDonationDateLabel(event.createdAt)}</time></div></li>)}</ol></details>

        {batch && <OperationalBatchTraceCard initialBatch={batch} viewerRole={role} defaultExpanded={false} showQr/>}
        {record.allowedNextStatuses.length>0 && <section className="eco-trace-section"><h2>{role==='DONOR'?'Gerenciar registro':'Atualizar recebimento'}</h2><StatusActionPanel compact donation={record}/></section>}
        {role!=='DONOR' && <Link className="eco-text-link" href={`/operacoes?status=${record.status}`}>Abrir em operações</Link>}
        {searchParams?.celebrate==='1' && received && role==='DONOR' && <PostDonationRating donationId={record.id}/>}
      </div>

      <aside className="eco-trace-context">
        <section><h2>Ponto de coleta</h2><strong>{point?.organizationName ?? point?.name ?? 'Não informado'}</strong>{point?.address && <p>{point.address}</p>}{point && <Link href={`/mapa/${point.id}`}><MapPin size={14}/> Ver ponto</Link>}</section>
        {record.ngo && <section><h2>Operador parceiro</h2><strong>{record.ngo.organizationName ?? record.ngo.name}</strong>{partnerLocation && <p>{partnerLocation}</p>}</section>}
        {record.operationalBatch && !batch && <details><summary>Carga {record.operationalBatch.code}</summary><p>{record.operationalBatch.name}</p><CodeQrCard compact code={record.operationalBatch.code} title="Código da carga" description="Carga vinculada a esta entrega."/></details>}
        {role==='DONOR' && <section className="eco-trace-points"><strong>{record.pointsAwarded} pontos</strong><p>{record.status==='CANCELLED'?'Registro cancelado, sem crédito.':received?'Recebimento confirmado.':'Creditados após o recebimento no ponto.'}</p><Link href="/perfil">Ver minha conta</Link></section>}
      </aside>
    </div>
  </div>;
}
