import type { SVGProps } from 'react';

/** Approved EcoVerse geometry. CurrentColor adapts to the host surface. */
export function EcoVerseMark({ animate = false, ...props }: SVGProps<SVGSVGElement> & { animate?: boolean }) {
  return <svg viewBox="0 0 100 100" fill="none" role="img" aria-label="EcoVerse" {...props}><path className={animate ? 'eco-mark-route' : undefined} d="M20 50H82C82 32.327 67.673 18 50 18C32.327 18 18 32.327 18 50C18 67.673 32.327 82 50 82C56.3 82 62.2 80.2 67.2 77" stroke="currentColor" strokeWidth="11" strokeLinecap="round" strokeLinejoin="round"/><circle className={animate ? 'eco-mark-destination' : undefined} cx="82" cy="70" r="6.5" fill="currentColor"/></svg>;
}
export function EcoVerseLogo({ className = '', inverse = false, animate = false }: { className?: string; inverse?: boolean; animate?: boolean }) {
  return <span className={`eco-logo ${inverse ? 'eco-logo-inverse' : ''} ${className}`} aria-label="EcoVerse"><EcoVerseMark animate={animate} aria-hidden="true"/><span>EcoVerse</span></span>;
}
export function BrandLoading({ label = 'Carregando…' }: { label?: string }) {
  return <div className="eco-loading" role="status" aria-live="polite"><EcoVerseMark animate aria-hidden="true"/><p>{label}</p></div>;
}
