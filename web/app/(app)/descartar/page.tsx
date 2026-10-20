import { Suspense } from 'react';
import { DisposalFlow } from '@/components/ecoverse/disposal-flow';
import { BrandLoading } from '@/components/branding/ecoverse-brand';
export default function DisposalPage() { return <Suspense fallback={<BrandLoading/>}><DisposalFlow/></Suspense>; }
