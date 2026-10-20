'use client';

import { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { HOME_FAQ_ITEMS } from '@/lib/faq';

export function HomeFaq() {
  const [faq, setFaq] = useState<number | null>(null);
  return <section id="duvidas" className="eco-container eco-faq"><div><h2>Dúvidas</h2></div><div className="eco-faq-list">{HOME_FAQ_ITEMS.map((item, index) => <div key={item.id} className="eco-faq-item"><h3><button onClick={() => setFaq(faq === index ? null : index)} aria-expanded={faq === index} aria-controls={`faq-${item.id}`}>{item.question}<ChevronDown size={18} /></button></h3><div id={`faq-${item.id}`} hidden={faq !== index}><p>{item.answer}</p></div></div>)}</div></section>;
}
