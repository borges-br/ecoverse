import { ArrowDown, ArrowUpRight } from 'lucide-react';
import { HeroMedia } from './hero-media';
import styles from './home.module.css';

export function CinematicHero() {
  return <section id="eco-cinematic-hero" className={styles.hero} aria-labelledby="hero-title">
    <HeroMedia />
    <div className={styles.shade} aria-hidden="true" />
    <div className={styles.copy}>
      <h1 id="hero-title">O fim não é o fim.</h1>
      <p>Encontre o destino certo para aquilo<br className={styles.mobileBreak} /> que merece um novo começo.</p>
    </div>
    <div className={styles.heroBottom}>
      <div className={styles.actions}>
        <a className={styles.primaryAction} href="#encontrar">Encontrar pontos de descarte <ArrowUpRight size={18} /></a>
        <a className={styles.secondaryAction} href="#jornada">Como funciona <ArrowDown size={16} /></a>
      </div>
      <div className={styles.heroCaption}>
        <span>Pequenas escolhas. Novos ciclos.</span>
        <a href="#encontrar" aria-label="Explore os materiais e encontre um ponto de descarte"><span>Explore os caminhos</span><ArrowDown size={14} /></a>
      </div>
    </div>
  </section>;
}
