'use client';

import { useEffect, useRef, useState } from 'react';
import styles from './home.module.css';

type DataConnection = EventTarget & { saveData?: boolean };

/** No media source is attached until the user's motion/data preferences are known. */
export function HeroMedia() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const portrait = window.matchMedia('(max-width: 800px) and (orientation: portrait)');
    const connection = (navigator as Navigator & { connection?: DataConnection }).connection;
    const hero = video.closest('section');
    let visible = true;
    let disposed = false;
    let attempt = 0;

    function stop() {
      attempt += 1;
      video!.pause();
      setPlaying(false);
      video!.removeAttribute('src');
      video!.load();
    }

    async function sync() {
      if (disposed) return;
      if (motion.matches || connection?.saveData) { stop(); return; }
      if (document.hidden || !visible) { video!.pause(); return; }
      const source = `/ecoverse/hero/${portrait.matches ? 'portrait' : 'landscape'}.mp4`;
      if (video!.getAttribute('src') !== source) {
        stop();
        video!.src = source;
        video!.load();
      }
      const currentAttempt = ++attempt;
      try {
        video!.muted = true;
        await video!.play();
      } catch {
        if (!disposed && currentAttempt === attempt) setPlaying(false);
      }
    }

    const observer = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      void sync();
    });
    if (hero) observer.observe(hero);
    motion.addEventListener('change', sync);
    portrait.addEventListener('change', sync);
    connection?.addEventListener('change', sync);
    document.addEventListener('visibilitychange', sync);
    // Allow the high-priority poster and initial UI to paint before fetching video.
    const frame = requestAnimationFrame(() => { void sync(); });
    return () => {
      disposed = true;
      attempt += 1;
      cancelAnimationFrame(frame);
      observer.disconnect();
      motion.removeEventListener('change', sync);
      portrait.removeEventListener('change', sync);
      connection?.removeEventListener('change', sync);
      document.removeEventListener('visibilitychange', sync);
      video.pause();
      video.removeAttribute('src');
      video.load();
    };
  }, []);

  return <div className={styles.media} aria-hidden="true">
    <picture>
      <source media="(max-width: 800px) and (orientation: portrait)" srcSet="/ecoverse/hero/poster-portrait.webp" />
      <img className={styles.poster} src="/ecoverse/hero/poster.webp" width={1672} height={941} alt="" fetchPriority="high" />
    </picture>
    <video ref={videoRef} className={`${styles.video} ${playing ? styles.playing : ''}`}
      autoPlay muted loop playsInline preload="none" tabIndex={-1}
      onPlaying={() => setPlaying(true)} onError={() => setPlaying(false)} onEmptied={() => setPlaying(false)} />
  </div>;
}
