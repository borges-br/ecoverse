import type { Metadata } from 'next';
import '@/styles/globals.css';
import '@/styles/ecoverse.css';
import '@/styles/ecoverse-refined.css';
import '@/styles/ecoverse-components.css';
import 'leaflet/dist/leaflet.css';
import { SessionProvider } from 'next-auth/react';
import { Toaster } from 'sonner';
import { auth } from '@/lib/auth';
import { ThemeProvider } from '@/components/layout/theme-provider';
import { CookieConsentBanner } from '@/components/layout/cookie-consent-banner';
import { AccountSessionGuard } from '@/components/layout/account-session-guard';
import { THEME_BOOTSTRAP_SCRIPT } from '@/lib/theme-preference';

export const metadata: Metadata = {
  title: 'EcoVerse | Cada material, um destino certo',
  description: 'Encontre pontos de coleta para pilhas, eletrônicos, lâmpadas e óleo de cozinha. Registre a entrega e acompanhe sua jornada.',
  manifest: '/ecoverse/site.webmanifest',
  icons: {
    icon: [
      { url: '/favicon.ico' },
      { url: '/ecoverse/ecoverse-icon-32.png', sizes: '32x32', type: 'image/png' },
      { url: '/ecoverse/ecoverse-icon-16.png', sizes: '16x16', type: 'image/png' },
      { url: '/ecoverse/ecoverse-icon-192.png', sizes: '192x192', type: 'image/png' },
      { url: '/ecoverse/ecoverse-icon-512.png', sizes: '512x512', type: 'image/png' },
    ],
    apple: [{ url: '/apple-icon.png', sizes: '180x180', type: 'image/png' }],
    shortcut: ['/favicon.ico'],
    other: [
      { rel: 'mask-icon', url: '/ecoverse/ecoverse-simbolo-primary.svg', color: '#153F35' },
    ],
  },
  other: {
    'theme-color': '#153F35',
  },
};

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();

  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <head>
        {/* Inline script to apply dark class before first paint — prevents FOUC */}
        <script
          dangerouslySetInnerHTML={{
            __html: THEME_BOOTSTRAP_SCRIPT,
          }}
        />
      </head>
      <body className="min-h-screen bg-surface text-on-surface dark:bg-surface-ink dark:text-gray-100">
        <SessionProvider
          session={session}
          refetchInterval={60}
          refetchOnWindowFocus
          refetchWhenOffline={false}
        >
          <ThemeProvider>
            {children}
            <AccountSessionGuard />
            <CookieConsentBanner />
            <Toaster position="bottom-right" richColors closeButton />
          </ThemeProvider>
        </SessionProvider>
      </body>
    </html>
  );
}
