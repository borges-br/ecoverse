import styles from './home.module.css';

/** Static hero background (the former looping video was removed to keep the page light). */
export function HeroMedia() {
  return <div className={styles.media} aria-hidden="true">
    <img className={styles.poster} src="/ecoverse/hero/poster.webp" width={1672} height={941} alt="" fetchPriority="high" />
  </div>;
}
