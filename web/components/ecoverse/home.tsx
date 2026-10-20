import Link from 'next/link';
import { MapPin, Truck } from 'lucide-react';
import { MATERIALS } from '@/lib/materials';
import { MaterialSymbol } from './material-symbol';
import { CollectionJourney } from './collection-journey';
import { PublicHeader, PublicFooter } from './public-chrome';
import { CinematicHero } from './cinematic-hero';
import { HomeSearch } from './home-search';
import { HomeFaq } from './home-faq';
import styles from './home.module.css';

export function EcoVerseHome() {
  return <div className={`eco-public eco-public-refined ${styles.home}`}>
    <a className={styles.skipLink} href="#encontrar">Ir para a busca de pontos</a>
    <PublicHeader cinematic/><main id="conteudo">
    <CinematicHero/>
    <HomeSearch/>

    <CollectionJourney/>

    <section className="eco-material-editorial"><div className="eco-container"><div className="eco-section-heading"><h2>Materiais</h2><Link href="/materiais" className="eco-text-link">Guia de entrega</Link></div>
      <div className="eco-editorial-grid">{MATERIALS.map(item=><Link href={`/materiais#${item.id.toLowerCase()}`} key={item.id} className={`eco-material-story eco-tone-${item.tone}`}><MaterialSymbol category={item.id}/><div><h3>{item.label}</h3><p>{item.id==='COOKING_OIL'?'Quantidade em litros':'Quantidade em unidades'}</p></div></Link>)}</div>
    </div></section>

    <section className="eco-container eco-partners" id="rede"><h2>Para parceiros</h2><div>
      <Link href="/cadastro?role=COLLECTION_POINT"><MapPin size={26}/><span><strong>Ponto de coleta</strong><small>Receba materiais e organize as retiradas.</small></span><span className="eco-partner-action">Cadastrar ponto</span></Link>
      <Link href="/cadastro?role=NGO"><Truck size={26}/><span><strong>Operador parceiro</strong><small>Gerencie retiradas, transporte e recebimento.</small></span><span className="eco-partner-action">Cadastrar operador</span></Link>
    </div></section>

    <HomeFaq/>
  </main><PublicFooter/></div>;
}
