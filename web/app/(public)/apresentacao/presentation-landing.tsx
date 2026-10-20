'use client';

import {
  ArrowRight,
  Code2,
  ExternalLink,
  Globe,
  Send,
  Smartphone,
  Star,
  HelpCircle,
  Users,
  X,
  type LucideIcon,
} from 'lucide-react';
import { AnimatePresence, motion, useReducedMotion, type Variants } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { useEffect, useState, type MouseEvent, type ReactNode } from 'react';
import { EcoVerseMark } from '@/components/branding/ecoverse-brand';
import { cn } from '@/lib/utils';
import { TeamSection } from '@/components/ui/team-section';

// Edite estes links antes da feira se houver URLs finais de deploy e contatos.
const LINKS = {
  app: '/login',
  github: 'https://github.com/borges-br',
  team: '#equipe',
  feedbackWebhook: 'https://n8n.borgesti.com/webhook/mosfet-unifacens',
};

type ActiveModal = 'rating' | null;

const quickLinks: Array<{
  label: string;
  description: string;
  href?: string;
  icon: LucideIcon;
  disabled?: boolean;
  modal?: Exclude<ActiveModal, null>;
}> = [
  {
    label: 'App',
    description: 'Acessar a plataforma',
    href: LINKS.app,
    icon: Smartphone,
  },
  {
    label: 'GitHub',
    description: 'Nathan Borges',
    href: LINKS.github,
    icon: Code2,
  },
  {
    label: 'Dúvidas',
    description: 'Entrega, QR e acompanhamento',
    href: '/#duvidas',
    icon: HelpCircle,
  },
  {
    label: 'Equipe',
    description: 'Integrantes do EcoVerse',
    href: LINKS.team,
    icon: Users,
  },
  {
    label: 'Nos avalie',
    description: 'Avaliação anônima',
    icon: Star,
    modal: 'rating',
  },
];

const odsItems = [
  {
    number: '03',
    title: 'Saúde e bem-estar',
    text: 'Organização do descarte de materiais que precisam de pontos e condições específicas de recebimento.',
  },
  {
    number: '10',
    title: 'Redução das desigualdades',
    text: 'Conecta participantes, pontos de coleta e operadores com informações públicas sobre a rede.',
  },
  {
    number: '12',
    title: 'Consumo e produção responsáveis',
    text: 'Organiza o recebimento e o transporte de materiais na rede parceira, com etapas registradas.',
  },
  {
    number: '17',
    title: 'Parcerias e meios de implementação',
    text: 'Valoriza integração entre universidade, comunidade e organizações parceiras.',
  },
];

const fadeUp: Variants = {
  hidden: { opacity: 0, y: 22 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.65, ease: [0.22, 1, 0.36, 1] },
  },
};

const container: Variants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.08, delayChildren: 0.05 },
  },
};

type RatingKey = 'apresentacao' | 'uiux' | 'proposta' | 'justificativa' | 'clareza';

type RatingState = Record<RatingKey, number>;

const RATING_FIELDS: Array<{ key: RatingKey; label: string }> = [
  { key: 'apresentacao', label: 'Apresentação' },
  { key: 'uiux', label: 'UI/UX' },
  { key: 'proposta', label: 'Proposta' },
  { key: 'justificativa', label: 'Justificativa' },
  { key: 'clareza', label: 'Clareza' },
];

const RATING_LABELS = {
  1: 'Não satisfatório',
  2: 'Pode melhorar',
  3: 'Razoável',
  4: 'Bom',
  5: 'Ótimo',
} as const;

type RatingValue = keyof typeof RATING_LABELS;

const RATING_FEEDBACK_STYLES: Record<RatingValue, string> = {
  1: 'border-red-200 bg-red-50 text-red-700',
  2: 'border-orange-200 bg-orange-50 text-orange-700',
  3: 'border-yellow-200 bg-yellow-50 text-yellow-800',
  4: 'border-lime-200 bg-lime-50 text-lime-700',
  5: 'border-emerald-200 bg-emerald-50 text-emerald-700',
};

const RATING_STAR_STYLES: Record<RatingValue, string> = {
  1: 'text-red-500',
  2: 'text-orange-500',
  3: 'text-yellow-500',
  4: 'text-lime-500',
  5: 'text-emerald-500',
};

const INITIAL_RATINGS: RatingState = {
  apresentacao: 0,
  uiux: 0,
  proposta: 0,
  justificativa: 0,
  clareza: 0,
};

type AnimatedLinkProps = {
  href: string;
  children: ReactNode;
  className?: string;
  ariaLabel?: string;
  icon?: LucideIcon;
  showArrow?: boolean;
  disabled?: boolean;
};

function AnimatedLink({
  href,
  children,
  className,
  ariaLabel,
  icon: Icon,
  showArrow = true,
  disabled = false,
}: AnimatedLinkProps) {
  const router = useRouter();
  const shouldReduceMotion = useReducedMotion();
  const [isLeaving, setIsLeaving] = useState(false);

  function handleClick(event: MouseEvent<HTMLAnchorElement>) {
    if (disabled) {
      event.preventDefault();
      return;
    }

    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.altKey ||
      event.ctrlKey ||
      event.shiftKey
    ) {
      return;
    }

    event.preventDefault();
    setIsLeaving(true);

    const delay = shouldReduceMotion ? 0 : 160;

    window.setTimeout(() => {
      if (!href || href === '#') {
        setIsLeaving(false);
        return;
      }

      if (href.startsWith('#')) {
        document.querySelector(href)?.scrollIntoView({
          behavior: shouldReduceMotion ? 'auto' : 'smooth',
          block: 'start',
        });
        window.history.pushState(null, '', href);
        setIsLeaving(false);
        return;
      }

      if (/^https?:\/\//.test(href)) {
        window.location.assign(href);
        return;
      }

      router.push(href);
    }, delay);
  }

  const sharedContent = (
    <>
      {Icon ? <Icon aria-hidden size={18} strokeWidth={1.9} /> : null}
      {children}
      {showArrow ? (
        <ArrowRight
          aria-hidden
          size={16}
          className="transition-transform duration-200 group-hover:translate-x-1"
          strokeWidth={2}
        />
      ) : null}
    </>
  );

  if (disabled) {
    return (
      <motion.span
        aria-disabled="true"
        aria-label={ariaLabel}
        className={cn(
          'group inline-flex min-h-12 items-center justify-center gap-2 rounded-2xl px-5 py-3 text-sm font-bold opacity-60 grayscale transition-all',
          className,
        )}
      >
        {sharedContent}
      </motion.span>
    );
  }

  return (
    <motion.a
      href={href}
      aria-label={ariaLabel}
      onClick={handleClick}
      className={cn(
        'group inline-flex min-h-12 items-center justify-center gap-2 rounded-2xl px-5 py-3 text-sm font-bold transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-surface',
        className,
      )}
      animate={isLeaving ? { scale: 0.97, opacity: 0.72 } : { scale: 1, opacity: 1 }}
      whileHover={shouldReduceMotion ? undefined : { y: -2 }}
      whileTap={shouldReduceMotion ? undefined : { scale: 0.97 }}
    >
      {sharedContent}
    </motion.a>
  );
}

function SectionHeader({
  eyebrow,
  title,
  description,
  center = false,
  invert = false,
}: {
  eyebrow: string;
  title: string;
  description?: string;
  center?: boolean;
  invert?: boolean;
}) {
  return (
    <motion.div
      variants={fadeUp}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.35 }}
      className={cn('max-w-3xl', center && 'mx-auto text-center')}
    >
      <span
        className={cn(
          'text-xs font-black uppercase tracking-[0.2em]',
          invert ? 'text-primary-muted' : 'text-primary',
        )}
      >
        {eyebrow}
      </span>
      <h2
        className={cn(
          'mt-3 text-3xl font-black leading-tight tracking-[-0.01em] sm:text-4xl lg:text-5xl',
          invert ? 'text-white' : 'text-on-surface',
        )}
      >
        {title}
      </h2>
      {description ? (
        <p
          className={cn(
            'mt-4 text-base leading-7 sm:text-lg',
            invert ? 'text-white/70' : 'text-gray-600',
          )}
        >
          {description}
        </p>
      ) : null}
    </motion.div>
  );
}

function FeedbackModal({
  activeModal,
  onClose,
}: {
  activeModal: ActiveModal;
  onClose: () => void;
}) {
  const [ratings, setRatings] = useState<RatingState>(INITIAL_RATINGS);
  const [comment, setComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');

  useEffect(() => {
    if (activeModal) {
      setRatings(INITIAL_RATINGS);
      setComment('');
      setStatus('idle');
      setIsSubmitting(false);
    }
  }, [activeModal]);

  function setScore(key: RatingKey, value: number) {
    setRatings((current) => ({ ...current, [key]: value }));
  }

  async function handleSubmit() {
    setIsSubmitting(true);
    setStatus('idle');

    const payload = {
      source: 'vestgo-presentation',
      anonymous: true,
      submittedAt: new Date().toISOString(),
      webhookTarget: LINKS.feedbackWebhook,
      ratings,
      labels: Object.fromEntries(
        Object.entries(ratings).map(([key, value]) => [key, value ? RATING_LABELS[value as keyof typeof RATING_LABELS] : ''])
      ),
      comment,
    };

    try {
      const response = await fetch(LINKS.feedbackWebhook, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error('Webhook returned a non-OK response');
      }

      setStatus('success');
      setRatings(INITIAL_RATINGS);
      setComment('');
    } catch {
      setStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <AnimatePresence>
      {activeModal ? (
        <motion.div
          className="fixed inset-0 z-[100] flex items-center justify-center bg-black/70 p-3 backdrop-blur-sm sm:p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          role="dialog"
          aria-modal="true"
          aria-labelledby="feedback-modal-title"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) onClose();
          }}
        >
          <motion.div
            className="max-h-[calc(100dvh-1.5rem)] w-full max-w-3xl overflow-y-auto overscroll-contain rounded-[2rem] border border-white/60 bg-[linear-gradient(180deg,rgba(255,255,255,0.99),rgba(244,248,246,0.97))] p-4 shadow-2xl sm:max-h-[calc(100dvh-2rem)] sm:p-7"
            initial={{ opacity: 0, y: 24, scale: 0.97 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 12, scale: 0.97 }}
            transition={{ duration: 0.25 }}
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs font-black uppercase tracking-[0.2em] text-primary">Feedback</p>
                <h3 id="feedback-modal-title" className="mt-2 text-2xl font-black text-on-surface">
                  Avalie nosso projeto
                </h3>
              </div>
              <button
                type="button"
                onClick={onClose}
                className="rounded-full bg-gray-100 p-2 text-gray-600 transition-colors hover:bg-gray-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
                aria-label="Fechar modal"
              >
                <X aria-hidden size={20} />
              </button>
            </div>

            <div className="mt-6 space-y-5">

              <div className="grid gap-4">
                {RATING_FIELDS.map((field) => {
                  const value = ratings[field.key];

                  return (
                    <div key={field.key} className="rounded-[1.5rem] border border-gray-200 bg-white p-4 shadow-sm sm:p-5">
                      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between sm:gap-4">
                        <div>
                          <p className="text-sm font-black text-on-surface">{field.label}</p>
                          {!value ? (
                            <p className="mt-1 text-xs font-bold uppercase tracking-[0.18em] text-gray-500">
                              Selecione uma nota
                            </p>
                          ) : null}
                        </div>
                        <div className="flex flex-wrap items-center gap-2">
                          {[1, 2, 3, 4, 5].map((score) => {
                            const active = score <= value;
                            const ratingValue = value as RatingValue;

                            return (
                              <button
                                key={score}
                                type="button"
                                onClick={() => setScore(field.key, score)}
                                className={cn(
                                  'rounded-full transition-transform hover:-translate-y-0.5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary',
                                  active && value ? RATING_STAR_STYLES[ratingValue] : 'text-gray-300',
                                )}
                                aria-label={`${field.label}: ${score} estrela${score > 1 ? 's' : ''}`}
                              >
                                <Star aria-hidden size={24} fill={active ? 'currentColor' : 'none'} />
                              </button>
                            );
                          })}
                        </div>
                      </div>
                      {value ? (
                        <p
                          className={cn(
                            'mt-3 inline-flex rounded-full border px-3 py-1 text-xs font-black uppercase tracking-[0.16em]',
                            RATING_FEEDBACK_STYLES[value as RatingValue],
                          )}
                        >
                          {value} estrela{value > 1 ? 's' : ''} · {RATING_LABELS[value as RatingValue]}
                        </p>
                      ) : null}
                    </div>
                  );
                })}
              </div>

              <label className="block rounded-[1.5rem] border border-gray-200 bg-white p-5 shadow-sm">
                <span className="text-sm font-bold text-on-surface">Opinião em texto</span>
                <textarea
                  value={comment}
                  onChange={(event) => setComment(event.target.value)}
                  rows={4}
                  className="mt-2 w-full resize-none rounded-2xl border border-gray-200 bg-surface px-4 py-3 text-sm outline-none transition focus:border-primary focus:bg-white"
                  placeholder="Escreva comentários, sugestões ou observações adicionais."
                />
              </label>

              <div className="flex flex-col gap-3 sm:flex-row sm:justify-end">
                <button
                  type="button"
                  onClick={onClose}
                  className="rounded-2xl border border-gray-200 px-5 py-3 text-sm font-bold text-on-surface transition-colors hover:bg-gray-50"
                >
                  Cancelar
                </button>
                <button
                  type="button"
                  onClick={handleSubmit}
                  disabled={isSubmitting}
                  className="inline-flex items-center justify-center gap-2 rounded-2xl bg-primary px-5 py-3 text-sm font-bold text-white shadow-lg shadow-emerald-600/20 transition-transform active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-70"
                >
                  <Send aria-hidden size={17} />
                  {isSubmitting ? 'Enviando...' : 'Enviar avaliação'}
                </button>
              </div>

              {status === 'success' ? (
                <div className="rounded-2xl bg-emerald-50 p-4 text-sm leading-6 text-emerald-900">
                  Avaliação enviada com sucesso.
                </div>
              ) : null}

              {status === 'error' ? (
                <div className="rounded-2xl bg-red-50 p-4 text-sm leading-6 text-red-900">
                  Ocorreu um erro ao enviar sua avaliação. Por favor, tente novamente.
                </div>
              ) : null}
            </div>
          </motion.div>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}

export function PresentationLanding() {
  const [activeModal, setActiveModal] = useState<ActiveModal>(null);

  return (
    <main className="min-h-screen overflow-hidden bg-surface text-on-surface">
      <FeedbackModal activeModal={activeModal} onClose={() => setActiveModal(null)} />

      <header className="sticky top-0 z-50 border-b border-gray-200/60 bg-surface/90 shadow-[0_12px_30px_-20px_rgba(15,23,42,0.35)] backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-shell items-center justify-between px-4 sm:px-6 lg:px-8">
          <a href="#links" className="flex items-center gap-3" aria-label="EcoVerse apresentação">
            <EcoVerseMark className="h-10 w-10" />
            <div>
              <p className="text-lg font-black leading-none text-primary">EcoVerse</p>
              <p className="mt-1 text-[11px] font-bold uppercase tracking-[0.2em] text-gray-500">
                FACENS
              </p>
            </div>
          </a>

          <AnimatedLink
            href={LINKS.app}
            icon={Globe}
            showArrow={false}
            className="bg-primary px-5 py-2.5 text-white shadow-lg shadow-emerald-600/20 hover:brightness-110"
          >
            Acessar app
          </AnimatedLink>
        </div>
      </header>

      <section id="links" className="bg-gradient-to-b from-primary/10 to-surface px-4 py-10 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-shell">
          <motion.div
            variants={container}
            initial="hidden"
            animate="visible"
            className="text-center"
          >
            <motion.p
              variants={fadeUp}
              className="text-xs font-black uppercase tracking-[0.22em] text-primary"
            >
              Obrigado por me escanear! :)
            </motion.p>
            <motion.h1
              variants={fadeUp}
              className="mt-3 text-4xl font-black tracking-[-0.02em] sm:text-5xl"
            >
              Links Úteis
            </motion.h1>
            <motion.p variants={fadeUp} className="mx-auto mt-4 max-w-2xl text-base text-gray-600">
              EcoVerse · Projeto UPX / FACENS
            </motion.p>
          </motion.div>

          <motion.div
            variants={container}
            initial="hidden"
            animate="visible"
            className="mt-8 grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4"
          >
            {quickLinks.map((link) => {
              const Icon = link.icon;
              const content = (
                <>
                  <Icon aria-hidden size={18} strokeWidth={1.9} />
                  <span className="flex flex-col">
                    <span className="text-base font-black">{link.label}</span>
                    <span className="text-sm font-medium text-gray-500">{link.description}</span>
                  </span>
                </>
              );

              return (
                <motion.div key={link.label} variants={fadeUp}>
                  {link.modal ? (
                    <motion.button
                      type="button"
                      onClick={() => setActiveModal(link.modal ?? null)}
                      whileHover={{ y: -2 }}
                      whileTap={{ scale: 0.97 }}
                      className="group inline-flex h-full min-h-12 w-full items-center justify-start gap-4 rounded-2xl border border-white bg-white p-5 text-left text-sm font-bold text-on-surface shadow-sm transition-all hover:-translate-y-1 hover:shadow-card-lg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-surface"
                      aria-label={link.label}
                    >
                      {content}
                    </motion.button>
                  ) : (
                    <AnimatedLink
                      href={link.href ?? '#'}
                      icon={Icon}
                      showArrow={false}
                      disabled={link.disabled}
                      className="h-full w-full justify-start gap-4 border border-white bg-white p-5 text-left text-on-surface shadow-sm hover:-translate-y-1 hover:shadow-card-lg"
                      ariaLabel={link.label}
                    >
                      <span className="flex flex-col">
                        <span className="text-base font-black">{link.label}</span>
                        <span className="text-sm font-medium text-gray-500">{link.description}</span>
                      </span>
                    </AnimatedLink>
                  )}
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>

      <TeamSection/>

      <section id="ods" className="bg-white px-4 py-16 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-shell">
          <SectionHeader
            eyebrow="ODS relacionadas"
            title="Impacto alinhado com objetivos globais"
            description="As metas abaixo reforçam o posicionamento social do EcoVerse e o propósito da solução apresentada."
          />

          <motion.div
            variants={container}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            className="mt-10 grid gap-4 md:grid-cols-2 xl:grid-cols-4"
          >
            {odsItems.map((item) => (
              <motion.article
                key={item.number}
                variants={fadeUp}
                whileHover={{ y: -4 }}
                className="relative overflow-hidden rounded-[2rem] border border-gray-200 bg-[linear-gradient(180deg,rgba(255,255,255,0.98),rgba(242,244,246,0.92))] p-6 shadow-sm"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="text-xs font-black uppercase tracking-[0.22em] text-primary">
                      ODS {item.number}
                    </p>
                    <h3 className="mt-2 text-xl font-black text-on-surface">{item.title}</h3>
                  </div>
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary-light text-lg font-black text-primary">
                    {item.number}
                  </div>
                </div>
                <p className="mt-4 text-sm leading-6 text-gray-600">{item.text}</p>
                <div
                  className="absolute -bottom-10 -right-10 h-32 w-32 rounded-full bg-primary/10"
                  aria-hidden
                />
              </motion.article>
            ))}
          </motion.div>
        </div>
      </section>

      <section className="bg-surface px-4 py-14 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-shell text-center">
          <SectionHeader
            eyebrow="Feedback e sugestões"
            title="Avalie nosso projeto"
            description="Sua opinião é muito importante. Avalie nosso projeto em poucos cliques."
            center
          />
          <div className="mt-8 flex justify-center">
            <motion.button
              type="button"
              onClick={() => setActiveModal('rating')}
              whileHover={{ y: -2 }}
              whileTap={{ scale: 0.98 }}
              className="inline-flex min-h-14 items-center justify-center gap-3 rounded-2xl bg-primary px-8 py-4 text-base font-black text-white shadow-xl shadow-emerald-600/20 transition-all hover:brightness-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
            >
              <Star aria-hidden size={21} />
              Avalie nosso projeto
            </motion.button>
          </div>
        </div>
      </section>

      <footer className="rounded-t-xl bg-primary-deeper px-4 py-10 text-center text-white sm:px-6 lg:px-8">
        <div className="mx-auto flex max-w-shell flex-col items-center gap-6">
          <div className="flex items-center gap-3">
            <EcoVerseMark className="h-10 w-10" />
            <span className="text-xl font-black text-primary-glow">EcoVerse</span>
          </div>
          <div className="flex flex-wrap justify-center gap-5 text-sm font-bold text-white/65">
            <a href={LINKS.app} className="transition-colors hover:text-white">
              Aplicação
            </a>
            <a href={LINKS.github} className="inline-flex items-center gap-1 transition-colors hover:text-white">
              GitHub
              <ExternalLink aria-hidden size={13} />
            </a>
          </div>
          <p className="text-sm text-white/45">© {new Date().getFullYear()} EcoVerse. Descartes rastreáveis com propósito.</p>
        </div>
      </footer>
    </main>
  );
}
