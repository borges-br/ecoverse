'use client';
import { useState, useMemo } from 'react';
import {
  HelpCircle, Search, ChevronDown, ChevronUp,
  MessageCircle, Mail, FileText, ShieldCheck, ExternalLink,
} from 'lucide-react';

import { FAQ_ITEMS, FAQ_CATEGORIES, normalizeFaqSearch, type FaqItem } from '@/lib/faq';

// Contact channels are shown only when an actual destination is configured.
const supportEmail = process.env.NEXT_PUBLIC_SUPPORT_EMAIL?.trim();
const supportWhatsApp = process.env.NEXT_PUBLIC_SUPPORT_WHATSAPP?.replace(/\D/g, '');

function AccordionItem({ item }: { item: FaqItem }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="border-b border-gray-100 last:border-0 dark:border-white/10">
      <button
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        aria-controls={`answer-${item.id}`}
        className="w-full flex items-start justify-between gap-3 py-4 text-left"
      >
        <p className={`text-sm leading-snug pr-2 ${open ? 'font-bold text-primary-deeper dark:text-primary-muted' : 'font-semibold text-on-surface dark:text-gray-100'}`}>
          {item.question}
        </p>
        <div className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center transition-colors ${
          open ? 'bg-primary text-white' : 'bg-surface text-gray-400 dark:bg-white/10 dark:text-gray-500'
        }`}>
          {open ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
        </div>
      </button>

      {open && (
        <div id={`answer-${item.id}`} className="pb-4">
          <p className="text-sm text-gray-500 leading-relaxed dark:text-gray-400">{item.answer}</p>
        </div>
      )}
    </div>
  );
}

export default function SuportePage() {
  const [search, setSearch] = useState('');
  const [activeCategory, setActiveCategory] = useState('Todas');

  const filtered = useMemo(() => {
    const q = normalizeFaqSearch(search);
    return FAQ_ITEMS.filter((item) => {
      const matchCategory = activeCategory === 'Todas' || item.category === activeCategory;
      const matchSearch =
        !q ||
        normalizeFaqSearch(item.question).includes(q) ||
        normalizeFaqSearch(item.answer).includes(q);
      return matchCategory && matchSearch;
    });
  }, [search, activeCategory]);

  // Agrupar por categoria para exibição
  const grouped = useMemo(() => {
    const map = new Map<string, FaqItem[]>();
    for (const item of filtered) {
      if (!map.has(item.category)) map.set(item.category, []);
      map.get(item.category)!.push(item);
    }
    return Array.from(map.entries());
  }, [filtered]);

  return (
    <div className="vg-dark-fix pb-2">
      {/* ── Header ── */}
      <section className="px-5 pt-6 pb-4">
        <p className="text-[11px] font-semibold tracking-widest text-gray-400 uppercase mb-1">
          Ajuda
        </p>
        <h1 className="text-3xl font-bold text-primary-deeper dark:text-white">Dúvidas frequentes</h1>
        <p className="text-sm text-gray-400 mt-1 dark:text-gray-500">Entrega, QR, acompanhamento e conta.</p>
      </section>

      {/* ── Busca ── */}
      <section className="px-5 mb-4">
        <div className="flex items-center gap-3 bg-white border border-gray-200 rounded-2xl px-4 py-3 focus-within:border-primary transition-colors dark:border-white/10 dark:bg-surface-inkSoft dark:focus-within:border-primary-muted">
          <Search size={16} className="text-gray-300 flex-shrink-0 dark:text-gray-600" />
          <input
            type="text"
            placeholder="Buscar perguntas…"
            aria-label="Buscar dúvidas"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 text-sm outline-none placeholder:text-gray-300 bg-transparent dark:text-gray-100 dark:placeholder:text-gray-600"
          />
        </div>
      </section>

      {/* ── Filtros de categoria ── */}
      <section className="mb-5">
        <div className="flex gap-2 overflow-x-auto px-5 pb-1 scrollbar-hide">
          {FAQ_CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              aria-pressed={activeCategory === cat}
              className={`flex-shrink-0 text-xs font-semibold px-4 py-2 rounded-xl transition-all ${
                activeCategory === cat
                  ? 'bg-primary-deeper text-white'
                  : 'bg-white text-gray-500 border border-gray-200 dark:border-white/10 dark:bg-surface-inkSoft dark:text-gray-300'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </section>

      {/* ── FAQ Accordion ── */}
      <section className="px-5 mb-6">
        {filtered.length === 0 ? (
          <div className="text-center py-12">
            <HelpCircle size={32} className="text-gray-200 mx-auto mb-3 dark:text-gray-600" />
            <p className="text-sm font-semibold text-gray-400 dark:text-gray-500">Nenhuma pergunta encontrada</p>
            <p className="text-xs text-gray-300 mt-1 dark:text-gray-600">Tente outra palavra ou categoria.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {grouped.map(([category, items]) => (
              <div key={category}>
                {activeCategory === 'Todas' && (
                  <p className="text-[11px] font-semibold tracking-widest text-gray-400 uppercase mb-2">
                    {category}
                  </p>
                )}
                <div className="bg-white rounded-2xl shadow-card px-4 dark:bg-surface-inkSoft dark:shadow-none">
                  {items.map((item) => (
                    <AccordionItem key={item.id} item={item} />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* ── Fale conosco ── */}
      <section className="px-5 mb-5">
        <div className="bg-primary-deeper rounded-3xl p-5 text-white">
          <p className="font-bold text-base mb-1">Ainda tem dúvidas?</p>
          <p className="text-xs text-primary-muted mb-4 leading-relaxed">
            Para condições de entrega, consulte o perfil do ponto escolhido.
          </p>
          <div className="flex gap-2">
            {supportWhatsApp && <a
              href={`https://wa.me/${supportWhatsApp}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 flex items-center justify-center gap-2 bg-[#25D366] text-white text-xs font-bold py-3 rounded-xl hover:opacity-90 transition-opacity active:scale-95"
            >
              <MessageCircle size={14} />
              WhatsApp
            </a>}
            {supportEmail && <a
              href={`mailto:${supportEmail}`}
              className="flex-1 flex items-center justify-center gap-2 bg-primary text-white text-xs font-bold py-3 rounded-xl hover:bg-primary-dark transition-colors active:scale-95"
            >
              <Mail size={14} />
              E-mail
            </a>}
            {!supportEmail && !supportWhatsApp && <a href="/mapa" className="text-sm font-semibold underline underline-offset-4">Consultar pontos da rede</a>}
          </div>
        </div>
      </section>

      {/* ── Links úteis ── */}
      <section className="px-5 mb-4">
        <p className="text-[11px] font-semibold tracking-widest text-gray-400 uppercase mb-3">
          Links úteis
        </p>
        <div className="bg-white rounded-2xl shadow-card divide-y divide-gray-100 overflow-hidden dark:divide-white/10 dark:bg-surface-inkSoft dark:shadow-none">
          {[
            { icon: ShieldCheck, label: 'Privacidade e segurança', href: '/perfil/privacidade', external: false },
            { icon: FileText, label: 'Guia de materiais', href: '/materiais', external: false },
            { icon: ExternalLink, label: 'Sobre o EcoVerse', href: '/sobre', external: false },
          ].map(({ icon: Icon, label, href, external }) => (
            <a
              key={label}
              href={href}
              target={external ? '_blank' : undefined}
              rel={external ? 'noopener noreferrer' : undefined}
              className="flex items-center gap-3 px-5 py-4 hover:bg-surface transition-colors dark:hover:bg-white/5"
            >
              <div className="w-8 h-8 bg-surface rounded-lg flex items-center justify-center flex-shrink-0 dark:bg-white/10">
                <Icon size={15} className="text-gray-500 dark:text-gray-300" />
              </div>
              <span className="flex-1 text-sm text-on-surface dark:text-gray-100">{label}</span>
              <ExternalLink size={13} className="text-gray-300 dark:text-gray-600" />
            </a>
          ))}
        </div>
      </section>
    </div>
  );
}
