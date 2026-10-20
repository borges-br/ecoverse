'use client';

import { useEffect, useRef, useState } from 'react';
import { Bell, Menu } from 'lucide-react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { EcoVerseLogo } from '@/components/branding/ecoverse-brand';
import type { AppNotification } from '@/hooks/use-notifications';
import { getMobileNavItems, isNavigationItemActive } from './navigation';

interface TopBarProps {
  onMenuOpen: () => void; unreadCount: number; notifPreview: AppNotification[];
  onNotifRead: (id:string) => Promise<void>; onMarkAllRead: () => Promise<void>;
}

function timeAgo(date:Date) {
  const minutes = Math.max(0,Math.floor((Date.now()-date.getTime())/60000));
  return minutes < 1 ? 'Agora' : minutes < 60 ? `${minutes} min` : minutes < 1440 ? `${Math.floor(minutes/60)} h` : `${Math.floor(minutes/1440)} d`;
}

export function TopBar({onMenuOpen,unreadCount,notifPreview,onNotifRead,onMarkAllRead}:TopBarProps) {
  const pathname = usePathname();
  const router = useRouter();
  const {data:session} = useSession();
  const [dropdownOpen,setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(()=>{
    function close(event:MouseEvent) {if(dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) setDropdownOpen(false);}
    function escape(event:KeyboardEvent) {if(event.key==='Escape') setDropdownOpen(false);}
    if(dropdownOpen) {document.addEventListener('mousedown',close);document.addEventListener('keydown',escape);}
    return ()=>{document.removeEventListener('mousedown',close);document.removeEventListener('keydown',escape);};
  },[dropdownOpen]);
  useEffect(()=>setDropdownOpen(false),[pathname]);

  return <header className="eco-app-topbar"><div className="eco-app-topbar-inner">
    <Link href="/inicio" aria-label="EcoVerse, início"><EcoVerseLogo/></Link>
    <nav className="eco-desktop-nav" aria-label="Navegação principal do app">
      {getMobileNavItems(session?.user?.role ?? 'DONOR').map(item => <Link key={item.href} href={item.href} aria-current={isNavigationItemActive(pathname,item) ? 'page' : undefined}>{item.label}</Link>)}
    </nav>
    <div className="eco-topbar-actions">
      <div ref={dropdownRef}>
        <button className="eco-icon-action eco-notification-toggle" onClick={()=>setDropdownOpen(value=>!value)} aria-label="Abrir notificações" aria-expanded={dropdownOpen} aria-controls="eco-notifications">
          <Bell size={19}/>{unreadCount>0 && <span>{unreadCount>9?'9+':unreadCount}</span>}
        </button>
        {dropdownOpen && <div id="eco-notifications" className="eco-notification-panel">
          <div className="eco-notification-heading"><strong>Notificações</strong>{unreadCount>0 && <button type="button" onClick={onMarkAllRead}>Marcar como lidas</button>}</div>
          {notifPreview.length===0 ? <p className="eco-notification-empty">Nenhuma notificação.</p> : <ul>{notifPreview.map(notification => <li key={notification.id}>
            <button className={notification.read?'':'is-unread'} onClick={async()=>{await onNotifRead(notification.id);setDropdownOpen(false);if(notification.href)router.push(notification.href);}}>
              <strong>{notification.title}</strong><span>{notification.body}</span><small>{timeAgo(notification.createdAt)}</small>
            </button>
          </li>)}</ul>}
          <Link href="/notificacoes" onClick={()=>setDropdownOpen(false)}>Ver todas</Link>
        </div>}
      </div>
      <button className="eco-icon-action" onClick={onMenuOpen} aria-label="Abrir menu de conta e configurações"><Menu size={21}/></button>
    </div>
  </div></header>;
}
