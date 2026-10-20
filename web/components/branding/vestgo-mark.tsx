import { EcoVerseMark } from './ecoverse-brand';
/** Compatibility export for retained screens. */
export function VestgoMark({ className = '', imageClassName = '', alt = 'EcoVerse' }: { className?: string; imageClassName?: string; alt?: string }) {
  return <EcoVerseMark className={`${className} ${imageClassName}`} aria-label={alt}/>;
}
