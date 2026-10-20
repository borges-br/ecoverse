'use client';

import { useState, type FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowUpRight, Check, MapPin, Search } from 'lucide-react';
import { MATERIALS } from '@/lib/materials';
import { MaterialSymbol } from './material-symbol';
import styles from './home.module.css';

export function HomeSearch() {
  const router = useRouter();
  const [material, setMaterial] = useState<string>('BATTERIES');
  const [location, setLocation] = useState('');

  function search(event: FormEvent) {
    event.preventDefault();
    const params = new URLSearchParams({ material });
    if (location.trim()) params.set('search', location.trim());
    router.push(`/mapa?${params}`);
  }

  return <section id="encontrar" className={`eco-container eco-search-section ${styles.search}`} aria-labelledby="busca-titulo">
    <form className={`eco-search-panel ${styles.searchPanel}`} onSubmit={search}>
      <div className={styles.searchHeading}>
        <div><p className={styles.eyebrow}>O próximo ciclo começa aqui</p><h2 id="busca-titulo">O que você vai descartar?</h2></div>
        <Link className="eco-text-link" href="/descartar">Registrar descarte <ArrowUpRight size={16} /></Link>
      </div>
      <div className="eco-material-picker" role="group" aria-label="Material para descartar">{MATERIALS.map(item => <button key={item.id} type="button" aria-pressed={material === item.id} onClick={() => setMaterial(item.id)}><MaterialSymbol category={item.id} /><span>{item.label}</span>{material === item.id && <Check size={16} className="eco-material-selected" />}</button>)}</div>
      <div className="eco-search-fields"><label className="eco-location-field"><MapPin size={19} /><span className="sr-only">Cidade, bairro ou CEP</span><input value={location} onChange={event => setLocation(event.target.value)} placeholder="Cidade, bairro ou CEP" maxLength={120} /></label><button className="eco-button" type="submit"><Search size={18} /> Buscar pontos</button></div>
    </form>
  </section>;
}
