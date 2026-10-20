'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronRight } from 'lucide-react';
export function WorkspaceBreadcrumbs() {
  const path = usePathname(); const parts = path.split('/').filter(Boolean); if (parts.length < 2) return null;
  const labels:Record<string,string> = {perfil:'Perfil',privacidade:'Privacidade',operacional:'Perfil operacional',configuracoes:'Configurações',rastreio:'Meus descartes',admin:'Administração',perfis:'Perfis da rede','campanhas-sazonais':'Campanhas',mapa:'Pontos de coleta'};
  return <nav className="eco-breadcrumbs" aria-label="Caminho de navegação"><Link href="/inicio">Início</Link>{parts.map((part,i) => <span key={i}><ChevronRight size={13}/>{i === parts.length-1 ? <span aria-current="page">{labels[part] ?? 'Detalhes'}</span> : <Link href={part === 'admin' ? '/admin/perfis' : '/'+parts.slice(0,i+1).join('/')}>{labels[part] ?? 'Registro'}</Link>}</span>)}</nav>;
}
