export type ThemePref = 'light' | 'dark' | 'system';
export const THEME_STORAGE_KEY = 'vestgo:theme-preference';
export const DEFAULT_THEME: ThemePref = 'light';

export function parseThemePreference(value: string | null): ThemePref {
  return value === 'dark' || value === 'system' || value === 'light' ? value : DEFAULT_THEME;
}

export function isDarkTheme(preference: ThemePref, systemDark: boolean): boolean {
  return preference === 'dark' || (preference === 'system' && systemDark);
}

/** Runs before paint. A blocked or empty storage still starts in light mode. */
export const THEME_BOOTSTRAP_SCRIPT = `(function(){var t='${DEFAULT_THEME}';try{var s=localStorage.getItem('${THEME_STORAGE_KEY}');if(s==='light'||s==='dark'||s==='system')t=s;}catch(e){}var d=t==='dark'||(t==='system'&&window.matchMedia('(prefers-color-scheme: dark)').matches);document.documentElement.classList.toggle('dark',d);})();`;
