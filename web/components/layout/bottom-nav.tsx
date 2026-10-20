'use client';

import { usePathname } from 'next/navigation';
import { useSession } from 'next-auth/react';
import { SpotlightNavigation } from '@/components/ui/spotlight-button';
import { getBottomNavItems, isNavigationItemActive } from './navigation';

/** Fixed task navigation stays available while reading long records. */
export function BottomNav() {
  const pathname = usePathname();
  const { data: session } = useSession();
  const items = getBottomNavItems(session?.user?.role ?? 'DONOR');
  const activeIndex = items.findIndex(item => isNavigationItemActive(pathname, item));
  return <div className="eco-bottom-nav"><SpotlightNavigation
    items={items.map(item => ({ ...item, label: item.mobileLabel ?? item.label }))}
    activeIndex={activeIndex}/></div>;
}
