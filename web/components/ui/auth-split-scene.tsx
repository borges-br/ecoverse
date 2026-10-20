import { EcoVerseMark } from '@/components/branding/ecoverse-brand';
// The approved artwork replaces the old canvas without adding continuous motion.
// Keep the props compatible with account/security screens.
export function AuthSplitScene({ className = '' }: { className?:string; routes?:unknown[]; dotColor?:string; accentColor?:string }) {
  return <div className={`pointer-events-none absolute inset-0 overflow-hidden ${className}`} aria-hidden="true"><EcoVerseMark className="absolute -right-24 top-12 h-[28rem] w-[28rem] text-white/[0.045]"/><img src="/ecoverse/hero-materiais.webp" alt="" className="absolute -bottom-4 left-0 w-full opacity-[0.13] mix-blend-screen"/></div>;
}
