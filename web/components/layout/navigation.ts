import {
  CalendarDays,
  CircleUser,
  ClipboardList,
  HelpCircle,
  Home,
  Map,
  Plus,
  Package,
  Settings,
  Shield,
  Truck,
  User,
  type LucideIcon,
} from 'lucide-react';

export type NavigationItem = {
  href: string;
  label: string;
  mobileLabel?: string;
  icon: LucideIcon;
  matchers?: string[];
  exact?: boolean;
  primaryAction?: boolean;
  accessibleLabel?: string;
};

const DONOR_PRIMARY_NAV_ITEMS: NavigationItem[] = [
  {
    href: '/inicio',
    label: 'Início',
    mobileLabel: 'Início',
    icon: Home,
    exact: true,
  },
  {
    href: '/mapa',
    label: 'Pontos',
    mobileLabel: 'Pontos',
    icon: Map,
    matchers: ['/mapa', '/pontos'],
  },
  {
    href: '/rastreio',
    label: 'Descartes',
    mobileLabel: 'Descartes',
    icon: Package,
    matchers: ['/rastreio', '/descartar', '/doar'],
  },
];

const OPERATIONAL_PRIMARY_NAV_ITEMS: NavigationItem[] = [
  {
    href: '/inicio',
    label: 'Início',
    mobileLabel: 'Início',
    icon: Home,
    exact: true,
  },
  {
    href: '/mapa',
    label: 'Pontos',
    mobileLabel: 'Pontos',
    icon: Map,
    matchers: ['/mapa', '/pontos'],
  },
  {
    href: '/operacoes',
    label: 'Operações',
    mobileLabel: 'Fila',
    icon: ClipboardList,
    exact: true,
  },
  {
    href: '/rastreio',
    label: 'Meus descartes',
    mobileLabel: 'Rastreio',
    icon: Truck,
  },
];

const ADMIN_PRIMARY_NAV_ITEMS: NavigationItem[] = [
  {
    href: '/inicio',
    label: 'Início',
    mobileLabel: 'Início',
    icon: Home,
    exact: true,
  },
  {
    href: '/admin/perfis',
    label: 'Perfis',
    mobileLabel: 'Perfis',
    icon: Shield,
    matchers: ['/admin/perfis'],
  },
  {
    href: '/admin/campanhas-sazonais',
    label: 'Campanhas',
    mobileLabel: 'Campanhas',
    icon: CalendarDays,
    matchers: ['/admin/campanhas-sazonais'],
  },
  {
    href: '/operacoes',
    label: 'Operações',
    mobileLabel: 'Fila',
    icon: ClipboardList,
    exact: true,
  },
  {
    href: '/mapa',
    label: 'Pontos',
    mobileLabel: 'Mapa',
    icon: Map,
    matchers: ['/mapa', '/pontos'],
  },
];

export const UTILITY_NAV_ITEMS: NavigationItem[] = [
  {
    href: '/perfil',
    label: 'Perfil',
    icon: User,
    exact: true,
  },
  {
    href: '/configuracoes',
    label: 'Configurações',
    icon: Settings,
    exact: true,
  },
  {
    href: '/perfil/privacidade',
    label: 'Privacidade',
    icon: Shield,
  },
  {
    href: '/suporte',
    label: 'Suporte',
    icon: HelpCircle,
  },
];

export function getUtilityNavItems(role: string) {
  if (role === 'DONOR') {
    return UTILITY_NAV_ITEMS;
  }

  const items: NavigationItem[] =
    role === 'ADMIN'
      ? [...UTILITY_NAV_ITEMS]
      : [
          {
            href: '/operacoes',
            label: 'Operações',
            icon: ClipboardList,
            exact: true,
          },
          ...UTILITY_NAV_ITEMS,
        ];

  if (role === 'ADMIN') {
    items.unshift({
      href: '/admin/perfis',
      label: 'Perfis',
      icon: Shield,
      exact: false, // matches child routes too
    });
    items.splice(1, 0, {
      href: '/admin/campanhas-sazonais',
      label: 'Campanhas Sazonais',
      icon: CalendarDays,
      exact: false,
    });
  }

  return items;
}

export const ROLE_LABELS: Record<string, string> = {
  DONOR: 'Participante',
  COLLECTION_POINT: 'Ponto de Coleta',
  NGO: 'Operador parceiro',
  ADMIN: 'Administrador',
};

export function getPrimaryNavItems(role: string) {
  if (role === 'ADMIN') {
    return ADMIN_PRIMARY_NAV_ITEMS;
  }

  if (role === 'COLLECTION_POINT' || role === 'NGO') {
    return OPERATIONAL_PRIMARY_NAV_ITEMS;
  }

  return DONOR_PRIMARY_NAV_ITEMS;
}

const PROFILE_MOBILE_NAV_ITEM: NavigationItem = {
  href: '/perfil',
  label: 'Conta',
  mobileLabel: 'Conta',
  icon: CircleUser,
  matchers: ['/perfil', '/configuracoes', '/suporte', '/notificacoes'],
};

export function getMobileNavItems(role: string) {
  const primary = getPrimaryNavItems(role);
  const visible = role === 'ADMIN'
    ? primary.filter(item => ['/inicio', '/admin/perfis', '/operacoes'].includes(item.href))
    : role === 'DONOR' ? primary : primary.filter(item => item.href !== '/rastreio');
  return [...visible, PROFILE_MOBILE_NAV_ITEM];
}

/** Creation is a separate destination on phones; desktop keeps its current tabs. */
export function getBottomNavItems(role: string): NavigationItem[] {
  if (role !== 'DONOR') return getMobileNavItems(role);
  return [
    DONOR_PRIMARY_NAV_ITEMS[0],
    DONOR_PRIMARY_NAV_ITEMS[1],
    {
      href: '/descartar', label: 'Descartar', accessibleLabel: 'Registrar descarte',
      icon: Plus, primaryAction: true, matchers: ['/descartar', '/doar'],
    },
    { ...DONOR_PRIMARY_NAV_ITEMS[2], matchers: ['/rastreio'] },
    PROFILE_MOBILE_NAV_ITEM,
  ];
}

export function isNavigationItemActive(pathname: string, item: NavigationItem) {
  const matchers = item.matchers ?? [item.href];

  return matchers.some((matcher) => {
    if (item.exact) {
      return pathname === matcher;
    }

    return pathname === matcher || pathname.startsWith(`${matcher}/`);
  });
}
