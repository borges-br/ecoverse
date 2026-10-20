'use client';

import { useEffect, useRef } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { signOut, useSession } from 'next-auth/react';
import { Globe, LogOut, Plus, X } from 'lucide-react';
import { getPrimaryNavItems, getUtilityNavItems, isNavigationItemActive, ROLE_LABELS } from './navigation';
import { getOperationalDisplayName } from '@/lib/profile-display';

export function Sidebar({ isOpen, onClose }: { isOpen:boolean; onClose:()=>void }) {
  const pathname = usePathname();
  const { data:session } = useSession();
  const panel = useRef<HTMLElement>(null);
  const closeRef = useRef(onClose);
  closeRef.current = onClose;
  const role = session?.user?.role ?? 'DONOR';
  const operational = role === 'NGO' || role === 'COLLECTION_POINT';
  const name = getOperationalDisplayName({name:session?.user?.name ?? 'Conta',organizationName:operational ? session?.user?.organizationName : null});
  const items = [...getPrimaryNavItems(role), ...getUtilityNavItems(role)].filter((item,index,all) => all.findIndex(other=>other.href===item.href)===index);

  // Closed drawers are unmounted, so hidden links never enter the tab order.
  useEffect(() => {
    if (!isOpen) return;
    const previous = document.activeElement as HTMLElement | null;
    panel.current?.querySelector<HTMLButtonElement>('button')?.focus();
    function handleKey(event:KeyboardEvent) {
      if (event.key === 'Escape') closeRef.current();
      if (event.key !== 'Tab') return;
      const focusable = panel.current?.querySelectorAll<HTMLElement>('a[href],button:not([disabled])');
      if (!focusable?.length) return;
      const first = focusable[0], last = focusable[focusable.length-1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
    document.addEventListener('keydown',handleKey);
    return () => { document.removeEventListener('keydown',handleKey); previous?.focus(); };
  },[isOpen]);

  if (!isOpen) return null;
  return <div className="eco-menu-overlay">
    <button className="eco-menu-backdrop" aria-label="Fechar menu" tabIndex={-1} onClick={onClose}/>
    <aside ref={panel} className="eco-account-menu" role="dialog" aria-modal="true" aria-labelledby="eco-menu-title">
      <div className="eco-menu-heading"><h2 id="eco-menu-title">Menu</h2><button className="eco-icon-action" aria-label="Fechar menu" onClick={onClose}><X size={20}/></button></div>
      <Link href="/perfil" onClick={onClose} className="eco-menu-identity"><strong>{name}</strong><span>{ROLE_LABELS[role]}</span></Link>
      {role === 'DONOR' && <Link href="/descartar" className="eco-menu-create" onClick={onClose}><Plus size={18}/> Registrar descarte</Link>}
      <nav aria-label="Todas as áreas">{items.map(item => <Link key={item.href} href={item.href} onClick={onClose} aria-current={isNavigationItemActive(pathname,item) ? 'page' : undefined}><item.icon size={18}/>{item.label}</Link>)}
        {operational && <Link href={`/mapa/${session?.user?.id}?preview=1`} onClick={onClose}><Globe size={18}/> Perfil público</Link>}
        <Link href="/" onClick={onClose}><Globe size={18}/> Página inicial do site</Link>
      </nav>
      <button className="eco-menu-signout" onClick={()=>signOut({callbackUrl:'/login'})}><LogOut size={18}/> Sair da conta</button>
    </aside>
  </div>;
}
