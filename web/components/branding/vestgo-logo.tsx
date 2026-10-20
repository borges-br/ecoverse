import { EcoVerseLogo } from './ecoverse-brand';
/** Compatibility wrapper for account and security screens. */
export function VestgoLogo({ className = '', imageClassName = '', fallbackTextClassName = '', alt = 'EcoVerse' }: { className?: string; imageClassName?: string; fallbackTextClassName?: string; alt?: string }) {
  return <span className={className} aria-label={alt}><EcoVerseLogo inverse={imageClassName.includes('invert') || fallbackTextClassName.includes('text-white')} className="h-full"/></span>;
}
