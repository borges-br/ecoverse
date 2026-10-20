import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import { MATERIALS } from '@/lib/materials';
import { MaterialSymbol } from '@/components/ecoverse/material-symbol';
import { PublicHeader, PublicFooter } from '@/components/ecoverse/public-chrome';

export default function MaterialsPage() {
  return <div className="eco-public eco-public-refined"><PublicHeader/><main className="eco-container eco-guide">
    <Link href="/" className="eco-text-link"><ArrowLeft size={16}/> Início</Link><h1>Guia de materiais</h1>
    <p className="eco-lead">Confira o tipo aceito e as condições de entrega no perfil do ponto.</p>
    <div className="eco-guide-list">{MATERIALS.map(item=><article id={item.id.toLowerCase()} key={item.id} className="eco-guide-item">
      <div className={`eco-guide-icon eco-tone-${item.tone}`}><MaterialSymbol category={item.id}/></div>
      <div><h2>{item.label}</h2><p>{item.detail}</p><Link href={`/mapa?material=${item.id}`} className="eco-text-link">Buscar pontos</Link></div>
    </article>)}</div>
  </main><PublicFooter/></div>;
}
