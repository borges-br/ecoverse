import TailwindImageAccordion from '@/components/ui/tailwind-image-accordion';

export function TeamSection() {
  return <section id="equipe" className="eco-team-section" aria-labelledby="eco-team-heading">
    <div className="eco-container">
      <header className="eco-team-heading">
        <div><p>UPX · FACENS</p><h2 id="eco-team-heading">Equipe EcoVerse</h2></div>
        <span>Conheça os integrantes</span>
      </header>
      <TailwindImageAccordion/>
    </div>
  </section>;
}

export default TeamSection;
