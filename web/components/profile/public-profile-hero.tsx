'use client';

import Link from 'next/link';
import { Camera, CheckCircle2, Loader2, MailWarning, Pencil, Send } from 'lucide-react';
import { LevelRing } from '@/components/profile/level-ring';
import type { DonorGamificationResponse } from '@/lib/api';

type PublicProfileHeroProps = {
  name: string; email: string; emailVerifiedAt: string | null;
  avatarUrl: string | null; initials: string;
  level: DonorGamificationResponse['level'] | null; levelName: string;
  streakMonths: number; points: number;
  pointsBreakdown: DonorGamificationResponse['pointsBreakdown'] | null;
  donationsCount: number; completedCount: number; itemsCount: number;
  showPrivateEmail: boolean; showSettingsLink: boolean;
  avatarUploading: boolean; emailVerificationSending: boolean;
  emailVerificationMessage: string | null; emailVerificationError: string | null;
  onAvatarFileSelected: (file: File | null | undefined) => void;
  onResendEmailVerification: () => void;
  loading?: boolean;
};

export function PublicProfileHero(props: PublicProfileHeroProps) {
  const { name, email, emailVerifiedAt, avatarUrl, initials, level, levelName,
    streakMonths, points, donationsCount, completedCount, itemsCount,
    showPrivateEmail, showSettingsLink, avatarUploading, emailVerificationSending,
    emailVerificationMessage, emailVerificationError, onAvatarFileSelected,
    onResendEmailVerification, loading = false } = props;

  return <header className="eco-profile-head">
    <div className="eco-profile-identity">
      <div className="eco-profile-avatar">
        {avatarUrl ? <img src={avatarUrl} alt=""/> : <span>{initials || '?'}</span>}
        <label className="eco-avatar-edit" aria-label="Alterar foto">
          {avatarUploading ? <Loader2 size={13} className="animate-spin"/> : <Camera size={13}/>}
          <input type="file" accept="image/png,image/jpeg,image/webp" className="sr-only" disabled={avatarUploading}
            onChange={event => { onAvatarFileSelected(event.target.files?.[0] ?? null); event.target.value = ''; }}/>
        </label>
      </div>
      <div className="eco-profile-name">
        <h1>{name}</h1>
        {showPrivateEmail && <p>{email}</p>}
      </div>
      {showSettingsLink && <Link href="/configuracoes/perfil" className="eco-icon-action" aria-label="Editar perfil"><Pencil size={17}/></Link>}
    </div>

    {showPrivateEmail && <div className="eco-profile-verification">
      {emailVerifiedAt ? <span><CheckCircle2 size={13}/> E-mail confirmado</span> : <>
        <span className="eco-verification-pending"><MailWarning size={13}/> Confirme seu e-mail</span>
        <button type="button" onClick={onResendEmailVerification} disabled={emailVerificationSending}>
          {emailVerificationSending ? <Loader2 size={13} className="animate-spin"/> : <Send size={12}/>}
          {emailVerificationSending ? 'Enviando…' : 'Reenviar'}
        </button>
      </>}
    </div>}
    {emailVerificationMessage && <p className="eco-profile-feedback" role="status">{emailVerificationMessage}</p>}
    {emailVerificationError && <p className="eco-profile-feedback is-error" role="alert">{emailVerificationError}</p>}

    <dl className="eco-profile-stats">
      {[{value:donationsCount,label:'Descartes'}, {value:completedCount,label:'Concluídos'}, {value:itemsCount,label:'Materiais'}].map(stat =>
        <div key={stat.label}><dt>{stat.label}</dt><dd>{loading ? '—' : stat.value.toLocaleString('pt-BR')}</dd></div>
      )}
    </dl>

    <div className="eco-profile-level">
      {loading ? <p role="status">Carregando pontos…</p> : <>
      <LevelRing points={points} level={level} levelName={levelName} compact/>
      <div>
        <p className="eco-level-caption">Nível {level?.currentLevel ?? 1} de {level?.totalLevels ?? 30}</p>
        <h2>{level?.name ?? levelName}</h2>
        <p><strong>{points.toLocaleString('pt-BR')} pontos</strong>{streakMonths > 0 && <span> · {streakMonths} {streakMonths === 1 ? 'mês ativo' : 'meses ativos'}</span>}</p>
        <small>{level?.lockedUntilFirstDonation ? 'Confirme a primeira entrega para avançar.' : level && level.pointsToNextLevel > 0 ? `${level.pointsToNextLevel} pontos para o próximo nível` : 'Consulte suas conquistas abaixo.'}</small>
      </div>
      </>}
    </div>
  </header>;
}
