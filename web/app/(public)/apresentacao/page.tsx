import type { Metadata } from 'next';
import { PresentationLanding } from './presentation-landing';

export const metadata: Metadata = {
  title: 'EcoVerse | Apresentação FACENS',
  description:
    'Descartes rastreáveis com tecnologia, transparência e impacto social.',
};

export default function ApresentacaoPage() {
  return <PresentationLanding />;
}
