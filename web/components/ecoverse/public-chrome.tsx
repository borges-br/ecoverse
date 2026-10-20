'use client';
import Link from 'next/link';
import { useEffect, useId, useRef, useState } from 'react';
import { useSession } from 'next-auth/react';
import { Menu, X } from 'lucide-react';
import { EcoVerseLogo } from '@/components/branding/ecoverse-brand';
import styles from './public-chrome.module.css';

export function PublicHeader({ cinematic = false }: { cinematic?: boolean }) {
  const [open, setOpen] = useState(false); const { data: session } = useSession();
  const [pastHero, setPastHero] = useState(false);
  const menuButton = useRef<HTMLButtonElement>(null);
  const navId = useId();

  useEffect(() => {
    if (!cinematic) return;
    const hero = document.getElementById('eco-cinematic-hero');
    if (!hero) return;
    const observer = new IntersectionObserver(([entry]) => setPastHero(!entry.isIntersecting), { rootMargin: '-78px 0px 0px 0px' });
    observer.observe(hero);
    return () => observer.disconnect();
  }, [cinematic]);

  useEffect(() => {
    if (!open) return;
    function close(event: KeyboardEvent) {
      if (event.key === 'Escape') { setOpen(false); menuButton.current?.focus(); }
    }
    document.addEventListener('keydown', close);
    return () => document.removeEventListener('keydown', close);
  }, [open]);

  return <header className={`eco-public-header ${cinematic ? styles.cinematic : ''} ${cinematic && (pastHero || open) ? styles.solid : ''}`}><div className="eco-container eco-header-inner"><Link href="/" aria-label="EcoVerse, início"><EcoVerseLogo/></Link><nav id={navId} aria-label="Navegação principal" className={open ? 'eco-public-nav is-open' : 'eco-public-nav'}><Link href="/mapa" onClick={() => setOpen(false)}>Encontrar pontos</Link><Link href="/materiais" onClick={() => setOpen(false)}>Como descartar</Link><Link href="/#rede" onClick={() => setOpen(false)}>Para parceiros</Link><Link href="/sobre" onClick={() => setOpen(false)}>O projeto</Link></nav><div className="eco-header-actions"><Link className="eco-button eco-button-small" href={session ? '/inicio' : '/login'}>{session ? 'Minha área' : 'Entrar'}</Link><button ref={menuButton} className="eco-menu-button" onClick={() => setOpen(!open)} aria-label={open ? 'Fechar navegação' : 'Abrir navegação'} aria-expanded={open} aria-controls={navId}>{open ? <X size={22}/> : <Menu size={22}/>}</button></div></div></header>;
}
export function PublicFooter() { return <footer className="eco-footer"><div className="eco-container"><div className="eco-footer-main"><div><Link href="/" aria-label="EcoVerse, início"><EcoVerseLogo inverse/></Link><p>Cada material, um destino certo.</p></div><nav aria-label="Links do rodapé"><Link href="/mapa">Encontrar pontos</Link><Link href="/materiais">Guia de materiais</Link><Link href="/sobre">Sobre o projeto</Link><Link href="/cadastro?role=COLLECTION_POINT">Fazer parte da rede</Link><Link href="/perfil/privacidade">Privacidade e conta</Link></nav></div><div className="eco-footer-bottom"><p>EcoVerse · Projeto acadêmico UPX / FACENS</p></div></div></footer>; }
