'use client';

import Link from 'next/link';
import type { CSSProperties } from 'react';
import type { LucideIcon } from 'lucide-react';

export type SpotlightNavItem = {
  href: string;
  label: string;
  accessibleLabel?: string;
  icon: LucideIcon;
  primaryAction?: boolean;
};

/** A route-driven selection indicator, with fluid cell widths instead of fixed pixel offsets. */
export function SpotlightNavigation({ items, activeIndex, label = 'Navegação do app' }: {
  items: SpotlightNavItem[];
  activeIndex: number;
  label?: string;
}) {
  return <nav className="eco-spotlight-nav" aria-label={label}>
    <div className="eco-spotlight-track" style={{ '--nav-count': items.length } as CSSProperties}>
      <span className="eco-spotlight-indicator" aria-hidden="true" style={{
        left: `${((Math.max(activeIndex, 0) + 0.5) / items.length) * 100}%`,
        opacity: activeIndex < 0 ? 0 : 1,
      }}/>
      {items.map((item, index) => {
        const Icon = item.icon;
        return <Link key={item.href} href={item.href} className="eco-spotlight-item"
          data-primary={item.primaryAction || undefined}
          aria-label={item.accessibleLabel ?? item.label}
          aria-current={index === activeIndex ? 'page' : undefined}>
          <span className="eco-spotlight-icon"><Icon size={21} strokeWidth={index === activeIndex ? 2.2 : 1.8} aria-hidden="true"/></span>
          <span className="eco-spotlight-label">{item.label}</span>
        </Link>;
      })}
    </div>
  </nav>;
}
