'use client';

import { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react';
import { DEFAULT_THEME, THEME_STORAGE_KEY, isDarkTheme, parseThemePreference, type ThemePref } from '@/lib/theme-preference';

export type { ThemePref } from '@/lib/theme-preference';

interface ThemeContextValue {
  theme: ThemePref;
  setTheme: (theme: ThemePref) => void;
}

const ThemeContext = createContext<ThemeContextValue>({ theme: DEFAULT_THEME, setTheme: () => {} });
export function useTheme() { return useContext(ThemeContext); }

function resolveAndApply(pref: ThemePref) {
  document.documentElement.classList.toggle('dark', isDarkTheme(pref, window.matchMedia('(prefers-color-scheme: dark)').matches));
}

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<ThemePref>(DEFAULT_THEME);
  const preference = useRef<ThemePref>(DEFAULT_THEME);

  useEffect(() => {
    let initial = DEFAULT_THEME;
    try { initial = parseThemePreference(localStorage.getItem(THEME_STORAGE_KEY)); } catch { /* Storage can be disabled. */ }
    preference.current = initial;
    setThemeState(initial);
    resolveAndApply(initial);

    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    function onSystemChange() {
      if (preference.current === 'system') resolveAndApply('system');
    }
    mq.addEventListener('change', onSystemChange);
    return () => mq.removeEventListener('change', onSystemChange);
  }, []);

  const setTheme = useCallback((next: ThemePref) => {
    preference.current = next;
    setThemeState(next);
    try { localStorage.setItem(THEME_STORAGE_KEY, next); } catch { /* The choice still works for this visit. */ }
    resolveAndApply(next);
  }, []);

  return <ThemeContext.Provider value={{ theme, setTheme }}>{children}</ThemeContext.Provider>;
}
