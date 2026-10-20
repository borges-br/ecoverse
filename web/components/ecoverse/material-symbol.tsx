import type { MaterialCategory } from '@/lib/materials';

/** Geometry adapted from the user supplied Gemini Argon pack (06–09). */
export function MaterialSymbol({category,className=''}:{category:MaterialCategory;className?:string}) {
  return <svg className={`eco-material-symbol ${className}`} viewBox="0 0 48 48" fill="none" aria-hidden="true" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round">
    {category==='BATTERIES' && <><rect x="11" y="7" width="26" height="36" rx="4"/><path d="M20 3h8M24 15v10M19 20h10M19 33h10"/></>}
    {category==='ELECTRONICS' && <><rect x="5" y="7" width="38" height="27" rx="4"/><path d="M12 27h24M24 34v7M15 42h18"/></>}
    {category==='LAMPS' && <path d="M16 31c-1-7-6-7-6-14C10 0 38 0 38 17c0 7-5 8-6 14M17 33h14M18 39h12M21 44h6"/>}
    {category==='COOKING_OIL' && <><rect x="18" y="2" width="12" height="7" rx="2"/><path d="M18 9v5c-8 4-7 6-7 12v14c0 5 26 5 26 0V26c0-6 1-8-7-12V9M16 30h16"/></>}
  </svg>;
}
