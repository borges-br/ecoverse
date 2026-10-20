'use client';

import Image from 'next/image';
import { Github, Linkedin, Plus } from 'lucide-react';
import { useRef, useState, type KeyboardEvent } from 'react';
import { ECOVERSE_TEAM, type TeamMember } from '@/lib/team';

/** Photo accordion adapted from the supplied reference; works with touch and keyboard. */
export default function TailwindImageAccordion({ items = ECOVERSE_TEAM }: { items?: TeamMember[] }) {
  const [activeId, setActiveId] = useState(items[0]?.id);
  const buttons = useRef<Array<HTMLButtonElement | null>>([]);

  function moveFocus(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    let next: number;
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % items.length;
    else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index - 1 + items.length) % items.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = items.length - 1;
    else return;
    event.preventDefault();
    buttons.current[next]?.focus();
  }

  return <div className="eco-team-accordion">
    {items.map((member, index) => <article key={member.id} className="eco-team-card" data-active={activeId === member.id}
      onMouseEnter={() => setActiveId(member.id)} onFocus={() => setActiveId(member.id)}>
      <button type="button" className="eco-team-portrait" ref={node => { buttons.current[index] = node; }}
        aria-label={`Destacar foto de ${member.name}`} aria-pressed={activeId === member.id}
        onClick={() => setActiveId(member.id)} onKeyDown={event => moveFocus(event, index)}>
        <Image src={member.photo} alt={`Retrato de ${member.name}`} fill
          sizes="(max-width: 767px) 100vw, (max-width: 1200px) 50vw, 600px"
          style={{ objectPosition: member.objectPosition }} />
        <span className="eco-team-caption">
          <span className="eco-team-name">{member.name}</span>
        </span>
        <span className="eco-team-expand" aria-hidden="true"><Plus size={16}/></span>
      </button>
      {(member.github || member.linkedin) && <div className="eco-team-socials">
        {member.linkedin && <a href={member.linkedin} target="_blank" rel="noopener noreferrer" aria-label={`LinkedIn de ${member.name}`}><Linkedin size={17}/></a>}
        {member.github && <a href={member.github} target="_blank" rel="noopener noreferrer" aria-label={`GitHub de ${member.name}`}><Github size={17}/></a>}
      </div>}
    </article>)}
  </div>;
}
