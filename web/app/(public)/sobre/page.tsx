import Link from 'next/link';
import { PublicHeader, PublicFooter } from '@/components/ecoverse/public-chrome';
import { TeamSection } from '@/components/ui/team-section';

export default function AboutPage() {
  return <div className="eco-public eco-public-refined"><PublicHeader/><main><section className="eco-container eco-guide">
    <h1>Sobre o EcoVerse</h1><p className="eco-lead">Projeto UPX / FACENS para registrar entregas e organizar a coleta de pilhas, eletrônicos, lâmpadas e óleo de cozinha.</p>
    <div className="eco-about-grid"><div><h2>Da entrega ao parceiro</h2><p>Você entrega no ponto de coleta. O ponto confirma o recebimento, e o operador organiza a retirada e o transporte. Cada etapa registrada aparece no seu acompanhamento.</p></div><div><h2>Projeto UPX / FACENS</h2><p>O grupo desenvolve uma plataforma para conectar quem descarta, os pontos de coleta e os operadores responsáveis pelo transporte dos materiais.</p></div></div>
    <Link href="/mapa" className="eco-button">Consultar pontos</Link>
  </section><TeamSection/></main><PublicFooter/></div>;
}
