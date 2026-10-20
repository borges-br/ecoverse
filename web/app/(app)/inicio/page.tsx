import Link from 'next/link';
import {
  AlertCircle,
  ArrowRight,
  Building2,
  CalendarDays,
  CheckCircle2,
  ClipboardList,
  Clock3,
  ExternalLink,
  Map,
  Package,
  QrCode,
  ShieldCheck,
  Truck,
  Search,
  Calendar,
  Eye,
  Camera,
  Check,
  TrendingUp,
  TrendingDown,
  MapPin,
  type LucideIcon,
} from 'lucide-react';
import { DonorHome } from '@/components/dashboard/donor-home';
import { OperationalHomeScanButton } from '@/components/dashboard/operational-home-scan-button';
import { StatusActionPanel } from '@/components/donations/status-action-panel';
import { PickupRequestsPanel } from '@/components/operations/pickup-requests-panel';
import { auth } from '@/lib/auth';
import {
  getAdminProfiles,
  getMyGamification,
  getMyPartnerships,
  getMyProfile,
  getNearbyPoints,
  getNotifications,
  getOperationalDonations,
  getPickupRequests,
  getUserDonations,
  type AdminProfileRecord,
  type DonationRecord,
  type DonationStatus,
  type DonorGamificationResponse,
  type MyProfile,
  type NotificationRecord,
  type OperationalDonationListResponse,
  type PartnershipRecord,
  type PickupRequestRecord,
} from '@/lib/api';
import { formatDayMonthLabel } from '@/lib/date-time';

const PROFILE_STATE_LABELS: Record<string, string> = {
  DRAFT: 'Rascunho',
  PENDING: 'Pendente',
  ACTIVE: 'Ativo',
  VERIFIED: 'Verificado',
};

const ROLE_LABELS: Record<string, string> = {
  DONOR: 'Participante',
  COLLECTION_POINT: 'Ponto de Coleta',
  NGO: 'Operador parceiro',
  ADMIN: 'Administrador',
};

const STATUS_META: Record<DonationStatus, { label: string; tone: string }> = {
  PENDING: { label: 'Pendente', tone: 'bg-amber-50 text-amber-700' },
  AT_POINT: { label: 'No ponto', tone: 'bg-blue-50 text-blue-700' },
  IN_TRANSIT: { label: 'Em trânsito', tone: 'bg-indigo-50 text-indigo-700' },
  DELIVERED: { label: 'Entregue', tone: 'bg-primary-light text-primary' },
  DISTRIBUTED: { label: 'Finalizado', tone: 'bg-emerald-50 text-emerald-700' },
  CANCELLED: { label: 'Cancelada', tone: 'bg-red-50 text-red-600' },
};

const NEXT_ACTION_LABELS: Partial<Record<DonationStatus, string>> = {
  AT_POINT: 'Confirmar recebimento',
  IN_TRANSIT: 'Enviar paro operador',
  DELIVERED: 'Confirmar entrega',
  DISTRIBUTED: 'Marcar processamento',
};

const GOVERNANCE_NOTIFICATION_TYPES = new Set([
  'PROFILE_APPROVAL_REQUIRED',
  'PROFILE_REVISION_PENDING',
]);

type OperationalPeriod = 'today' | '7d' | '30d' | 'all';

const OPERATIONAL_PERIOD_OPTIONS: Array<{
  value: OperationalPeriod;
  label: string;
  summary: string;
}> = [
  { value: 'today', label: 'Hoje', summary: 'Atualizadas hoje' },
  { value: '7d', label: '7 dias', summary: 'Últimos 7 dias' },
  { value: '30d', label: '30 dias', summary: 'Últimos 30 dias' },
  { value: 'all', label: 'Tudo', summary: 'Todo o histórico' },
];

function getOperationalPeriod(value: string | string[] | undefined): OperationalPeriod {
  const candidate = Array.isArray(value) ? value[0] : value;

  if (
    candidate === 'today' ||
    candidate === '7d' ||
    candidate === '30d' ||
    candidate === 'all'
  ) {
    return candidate;
  }

  return '7d';
}

function getOperationalPeriodSummary(period: OperationalPeriod) {
  return OPERATIONAL_PERIOD_OPTIONS.find((option) => option.value === period)?.summary ?? 'Recorte atual';
}

function formatDateLabel(input: string) {
  return formatDayMonthLabel(input);
}

function getOperationPartnerLabel(role: string, donation: DonationRecord) {
  if (role === 'COLLECTION_POINT') {
    return donation.ngo?.organizationName ?? donation.ngo?.name ?? 'Operador destino pendente';
  }

  if (role === 'NGO') {
    return (
      donation.collectionPoint?.organizationName ??
      donation.collectionPoint?.name ??
      'Ponto de origem pendente'
    );
  }

  return `${donation.collectionPoint?.organizationName ?? donation.collectionPoint?.name ?? 'Origem'} -> ${
    donation.ngo?.organizationName ?? donation.ngo?.name ?? 'Destino'
  }`;
}

function getNextActionLabel(donation: DonationRecord) {
  const nextStatus = donation.allowedNextStatuses[0];

  return nextStatus ? NEXT_ACTION_LABELS[nextStatus] ?? STATUS_META[nextStatus].label : null;
}

function getPickupPartnerName(role: string, pickupRequest: PickupRequestRecord) {
  if (role === 'COLLECTION_POINT') {
    return pickupRequest.ngo.organizationName ?? pickupRequest.ngo.name;
  }

  return pickupRequest.collectionPoint.organizationName ?? pickupRequest.collectionPoint.name;
}

function getUpcomingPickup(pickupRequests: PickupRequestRecord[]) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const activeRequests = pickupRequests
    .filter((pickupRequest) => pickupRequest.status !== 'REJECTED')
    .filter((pickupRequest) => {
      if (!pickupRequest.requestedDate) {
        return true;
      }

      return new Date(pickupRequest.requestedDate).getTime() >= today.getTime();
    })
    .sort((left, right) => {
      const leftDate = left.requestedDate ?? left.createdAt;
      const rightDate = right.requestedDate ?? right.createdAt;

      return new Date(leftDate).getTime() - new Date(rightDate).getTime();
    });

  return activeRequests[0] ?? null;
}

function OperationalHome({
  firstName,
  role,
  profile,
  partnerships,
  pickupRequests,
  operationQueue,
  operationMeta,
  accessToken,
  period,
  hasDataError,
}: {
  firstName: string;
  role: string;
  profile: MyProfile | null;
  partnerships: PartnershipRecord[];
  pickupRequests: PickupRequestRecord[];
  operationQueue: DonationRecord[];
  operationMeta: OperationalDonationListResponse['meta'] | null;
  accessToken: string;
  period: OperationalPeriod;
  hasDataError: boolean;
}) {
  const roleLabel = ROLE_LABELS[role] ?? role;
  const organizationName = profile?.organizationName ?? profile?.name ?? 'Organização';
  const profileStateLabel = PROFILE_STATE_LABELS[profile?.publicProfileState ?? 'DRAFT'] ?? 'Rascunho';
  
  const completion = profile?.profileCompletion;
  const completionPercent =
    completion && completion.totalItems > 0
      ? Math.round((completion.completedItems / completion.totalItems) * 100)
      : null;
  const isVerified = Boolean(profile?.verifiedAt || profile?.publicProfileState === 'VERIFIED');
  const activePartnership = partnerships.find(
    (partnership) => partnership.status === 'ACTIVE' && partnership.isActive,
  );
  const activePartnerName = activePartnership
    ? role === 'COLLECTION_POINT'
      ? activePartnership.ngo.organizationName ?? activePartnership.ngo.name
      : activePartnership.collectionPoint.organizationName ?? activePartnership.collectionPoint.name
    : null;
  const pendingPickupRequests = pickupRequests.filter(
    (pickupRequest) => pickupRequest.status === 'PENDING',
  );
  const actionableOperations = operationQueue.filter(
    (donation) => donation.allowedNextStatuses.length > 0,
  );
  const nextAction = actionableOperations[0] ?? null;
  
  const statusCounts = operationMeta?.statusCounts ?? {};
  const countFor = (status: DonationStatus) => (operationMeta ? statusCounts[status] ?? 0 : null);
  
  const pendingCount = countFor('PENDING') ?? 0;
  const atPointCount = (role === 'NGO' ? countFor('DELIVERED') : countFor('AT_POINT')) ?? 0;
  const inTransitCount = countFor('IN_TRANSIT') ?? 0;
  const deliveredCount = (role === 'NGO' ? countFor('DISTRIBUTED') : countFor('DELIVERED')) ?? 0;
  
  const totalCount = pendingCount + atPointCount + inTransitCount + deliveredCount;
  const pendingPct = totalCount > 0 ? (pendingCount / totalCount) * 100 : 25;
  const atPointPct = totalCount > 0 ? (atPointCount / totalCount) * 100 : 25;
  const inTransitPct = totalCount > 0 ? (inTransitCount / totalCount) * 100 : 25;
  const deliveredPct = totalCount > 0 ? (deliveredCount / totalCount) * 100 : 25;

  const upcomingPickup = getUpcomingPickup(pickupRequests);
  const pickupTimeWindow =
    upcomingPickup?.timeWindowStart && upcomingPickup.timeWindowEnd
      ? `${upcomingPickup.timeWindowStart} - ${upcomingPickup.timeWindowEnd}`
      : null;

  const getDonationsForStage = (stageStatus: DonationStatus) => {
    const targetStatuses = new Set<DonationStatus>();
    if (stageStatus === 'PENDING') targetStatuses.add('PENDING');
    else if (stageStatus === 'AT_POINT') {
      if (role === 'NGO') targetStatuses.add('DELIVERED');
      else targetStatuses.add('AT_POINT');
    } else if (stageStatus === 'IN_TRANSIT') {
      targetStatuses.add('IN_TRANSIT');
    } else if (stageStatus === 'DELIVERED') {
      if (role === 'NGO') targetStatuses.add('DISTRIBUTED');
      else targetStatuses.add('DELIVERED');
    }
    return operationQueue.filter(d => targetStatuses.has(d.status));
  };

  const getPeriodDateRangeLabel = () => {
    const end = new Date();
    const start = new Date();
    start.setDate(end.getDate() - 6);
    const months = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
    const startDay = start.getDate();
    const endDay = end.getDate();
    const startMonth = months[start.getMonth()];
    const endMonth = months[end.getMonth()];
    
    if (start.getMonth() === end.getMonth()) {
      return `${startDay}-${endDay} ${endMonth}`;
    }
    return `${startDay} ${startMonth} - ${endDay} ${endMonth}`;
  };

  const dateRangeLabel = getPeriodDateRangeLabel();

  function Sparkline({ color }: { color: string }) {
    const path = "M 5 20 Q 20 4, 35 17 T 65 6 T 95 12";
    return (
      <svg className="w-16 h-6 overflow-visible" viewBox="0 0 100 20" fill="none">
        <path
          d={path}
          stroke={color}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    );
  }

  const getPickupDateParts = (dateString?: string | null) => {
    if (!dateString) return { month: 'MAI', day: '22' };
    const date = new Date(dateString);
    const months = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'];
    return {
      month: months[date.getMonth()],
      day: String(date.getDate()),
    };
  };

  const { month: pickupMonth, day: pickupDay } = getPickupDateParts(upcomingPickup?.requestedDate);

  const operationalStageCards = [
    {
      status: 'PENDING' as DonationStatus,
      label: 'PENDENTES',
      hint: role === 'COLLECTION_POINT' ? 'aguardando recebimento' : 'aguardando origem',
      icon: AlertCircle,
      color: '#f59e0b',
      textClass: 'text-amber-500',
      bgClass: 'bg-amber-500',
      cardBgClass: 'bg-amber-50/50 border-amber-100',
      itemBgClass: 'bg-amber-50 text-amber-900 border-amber-100/50',
      trend: '+3',
      isTrendUp: true,
      donations: getDonationsForStage('PENDING'),
      count: pendingCount,
    },
    {
      status: (role === 'NGO' ? 'DELIVERED' : 'AT_POINT') as DonationStatus,
      label: 'NO PONTO',
      hint: role === 'NGO' ? 'para conferir ou processar' : 'prontas para enviar',
      color: '#3b82f6',
      textClass: 'text-blue-500',
      bgClass: 'bg-blue-500',
      cardBgClass: 'bg-blue-50/50 border-blue-100',
      itemBgClass: 'bg-blue-50 text-blue-950 border-blue-100/50',
      trend: '+1',
      isTrendUp: true,
      donations: getDonationsForStage('AT_POINT'),
      count: atPointCount,
    },
    {
      status: 'IN_TRANSIT' as DonationStatus,
      label: 'EM TRÂNSITO',
      hint: 'com o operador',
      color: '#6366f1',
      textClass: 'text-indigo-500',
      bgClass: 'bg-[#6366f1]',
      cardBgClass: 'bg-indigo-50/50 border-indigo-100',
      itemBgClass: 'bg-indigo-50 text-indigo-900 border-indigo-100/50',
      trend: '0',
      isTrendUp: false,
      donations: getDonationsForStage('IN_TRANSIT'),
      count: inTransitCount,
    },
    {
      status: (role === 'NGO' ? 'DISTRIBUTED' : 'DELIVERED') as DonationStatus,
      label: 'ENTREGUES',
      hint: role === 'NGO' ? 'ciclo social concluído' : 'no recorte',
      color: '#0d9488',
      textClass: 'text-teal-600',
      bgClass: 'bg-[#0d9488]',
      cardBgClass: 'bg-teal-50/50 border-teal-100',
      itemBgClass: 'bg-teal-50 text-teal-900 border-teal-100/50',
      trend: '+12',
      isTrendUp: true,
      donations: getDonationsForStage('DELIVERED'),
      count: deliveredCount,
    },
  ];

  function ColetasProgressBar() {
    return (
      <div className="w-full h-2.5 bg-gray-200/60 rounded-full overflow-hidden flex">
        <div className="h-full bg-amber-500 transition-all duration-500" style={{ width: `${pendingPct}%` }} title={`Pendentes: ${pendingCount}`} />
        <div className="h-full bg-blue-500 transition-all duration-500" style={{ width: `${atPointPct}%` }} title={`No Ponto: ${atPointCount}`} />
        <div className="h-full bg-indigo-500 transition-all duration-500" style={{ width: `${inTransitPct}%` }} title={`Em Trânsito: ${inTransitCount}`} />
        <div className="h-full bg-teal-600 transition-all duration-500" style={{ width: `${deliveredPct}%` }} title={`Entregues: ${deliveredCount}`} />
      </div>
    );
  }

  const ScanCard = ({ isMobile }: { isMobile: boolean }) => (
    <div className={`relative overflow-hidden rounded-3xl bg-[#004d40] text-white p-5 lg:p-6 shadow-sm ${isMobile ? 'md:hidden mt-4' : 'hidden md:block h-full'}`}>
      <div className="relative z-10 flex flex-col justify-between h-full min-h-[160px] lg:min-h-[190px]">
        <div className="flex items-center justify-between">
          <div className="flex items-center justify-center h-10 w-10 rounded-xl bg-white/10 border border-white/10">
            <QrCode size={20} className="text-white" />
          </div>
          <span className="text-[10px] font-black uppercase tracking-[0.2em] text-white/50">RECEBER DOAÇÃO</span>
        </div>
        
        <div className="mt-4">
          <h3 className="text-2xl lg:text-3xl font-black tracking-tight leading-tight">Escanear QR<br />do descarte</h3>
        </div>
        
        <div className="mt-6 flex items-center gap-3">
          {isMobile ? (
            <OperationalHomeScanButton accessToken={accessToken} className="w-full border-none bg-transparent p-0">
              <div className="w-full flex items-center justify-center gap-2 bg-white/15 hover:bg-white/25 backdrop-blur-md border border-white/20 text-white rounded-full py-3.5 text-sm font-bold shadow-sm transition-all">
                <Camera size={16} />
                <span>Toque para abrir a câmera</span>
              </div>
            </OperationalHomeScanButton>
          ) : (
            <OperationalHomeScanButton accessToken={accessToken} className="w-auto border-none bg-transparent p-0">
              <div className="flex items-center gap-2 bg-white/10 hover:bg-white/20 border border-white/20 text-white rounded-xl px-4 py-2 text-sm font-bold shadow-sm transition-all">
                <Camera size={16} />
                <span>Câmera</span>
                <kbd className="h-5 px-1.5 flex items-center justify-center text-[10px] font-bold bg-white/10 border border-white/10 rounded text-white/50 ml-1">E</kbd>
              </div>
            </OperationalHomeScanButton>
          )}
        </div>
      </div>
      
      {/* Background Graphic Corner Target */}
      <svg className="absolute right-4 top-1/2 -translate-y-1/2 w-32 h-32 opacity-15 text-white pointer-events-none" viewBox="0 0 100 100" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M10 30 V10 H30" strokeLinecap="round" />
        <path d="M70 10 H90 V30" strokeLinecap="round" />
        <path d="M90 70 V90 H70" strokeLinecap="round" />
        <path d="M30 90 H10 V70" strokeLinecap="round" />
        <rect x="25" y="25" width="50" height="50" rx="8" strokeDasharray="4 4" />
      </svg>
    </div>
  );

  const NextActionCard = ({ isMobile }: { isMobile: boolean }) => (
    <div className={`bg-white rounded-3xl border border-gray-100 p-5 lg:p-6 shadow-sm ${isMobile ? 'md:hidden mt-4' : 'hidden md:block h-full'}`}>
      <div className="flex items-start justify-between gap-4">
        <div className="inline-flex items-center gap-1.5 rounded-full bg-amber-50 border border-amber-100/60 px-3 py-1 text-xs font-bold text-amber-700">
          <AlertCircle size={13} />
          <span>PRÓXIMA AÇÃO RECOMENDADA</span>
        </div>
        <div className="flex items-center gap-3">
          {nextAction && isMobile && (
            <span className="text-xs font-bold text-gray-400">+ 6 aguardando</span>
          )}
          <Link href="/operacoes?actionableOnly=true" className="text-xs font-bold text-[#006a62] hover:underline flex items-center gap-0.5">
            <span>Ver fila</span>
            <ArrowRight size={13} />
          </Link>
        </div>
      </div>

      {nextAction ? (
        <div className="mt-5 space-y-4">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-base font-black text-gray-900 tracking-tight">{nextAction.code}</span>
            <span className={`rounded-full px-2.5 py-0.5 text-[11px] font-bold ${STATUS_META[nextAction.status].tone}`}>
              {STATUS_META[nextAction.status].label}
            </span>
          </div>
          
          <div>
            <h4 className="text-2xl font-black text-gray-950 tracking-tight leading-snug">{nextAction.itemLabel}</h4>
          </div>

          <div className="flex flex-wrap items-center gap-4 text-xs font-bold text-gray-400">
            <div className="flex items-center gap-1.5">
              <Package size={14} className="text-gray-300" />
              <span>{nextAction.itemCount} item(ns)</span>
            </div>
            <div className="flex items-center gap-1.5">
              <Calendar size={14} className="text-gray-300" />
              <span>{formatDateLabel(nextAction.updatedAt)}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <MapPin size={14} className="text-gray-300" />
              <span>{getOperationPartnerLabel(role, nextAction)}</span>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3 pt-2">
            <StatusActionPanel compact donation={nextAction} />
            <Link
              href={`/rastreio/${nextAction.id}`}
              className="inline-flex h-11 items-center justify-center rounded-full border border-gray-200 bg-white hover:bg-gray-50 px-5 text-xs font-bold text-gray-700 shadow-sm transition-all"
            >
              Detalhes
            </Link>
          </div>
        </div>
      ) : (
        <div className="mt-6 rounded-2xl bg-gray-50 border border-gray-100 p-5 text-center">
          <p className="text-sm font-bold text-gray-500">Nenhum descarte exige ação no momento.</p>
          <p className="mt-1 text-xs text-gray-400 font-semibold">{getOperationalPeriodSummary(period)}</p>
        </div>
      )}
    </div>
  );

  const AgendaCard = () => (
    <div className="bg-white rounded-3xl border border-gray-100 p-5 lg:p-6 shadow-sm">
      <div className="flex items-center justify-between gap-4 mb-5">
        <h3 className="text-xs font-black uppercase tracking-[0.2em] text-gray-400">AGENDA</h3>
        <Link href="/operacoes" className="text-xs font-bold text-[#006a62] hover:underline flex items-center gap-0.5">
          <span>Ver todas</span>
          <ArrowRight size={13} />
        </Link>
      </div>

      {upcomingPickup ? (
        <div className="flex items-start gap-4">
          <div className="flex flex-col items-center justify-center bg-gray-100 dark:bg-white/5 rounded-2xl w-14 h-14 font-black flex-shrink-0 text-gray-500">
            <span className="text-[10px] uppercase font-bold tracking-wider text-gray-400">{pickupMonth}</span>
            <span className="text-xl -mt-1 text-gray-800">{pickupDay}</span>
          </div>
          <div className="min-w-0 flex-1">
            <h4 className="text-base font-black text-gray-900 leading-tight">
              Retirada com {getPickupPartnerName(role, upcomingPickup)}
            </h4>
            <div className="flex flex-wrap items-center gap-3 text-xs font-bold text-gray-400 mt-1.5">
              <div className="flex items-center gap-1">
                <Clock3 size={13} className="text-gray-300" />
                <span>{pickupTimeWindow ?? 'Horário pendente'}</span>
              </div>
              <div className="flex items-center gap-1">
                <Package size={13} className="text-gray-300" />
                <span>14 item(ns)</span>
              </div>
            </div>
            {pendingPickupRequests.length > 0 && (
              <div className="inline-flex items-center gap-1.5 rounded-full bg-amber-50 border border-amber-100/50 px-2.5 py-0.5 text-[10px] font-bold text-amber-700 mt-2">
                <AlertCircle size={10} />
                <span>{pendingPickupRequests.length} solicitação(ões) para responder</span>
              </div>
            )}
          </div>
          <div className="flex-shrink-0">
            <Link
              href="/operacoes"
              className="inline-flex items-center justify-center bg-[#004d40] hover:bg-[#003d33] text-white rounded-full px-4 py-2 text-xs font-bold transition-all shadow-sm gap-1"
            >
              <span>Preparar</span>
              <ArrowRight size={12} />
            </Link>
          </div>
        </div>
      ) : (
        <div className="rounded-2xl bg-gray-50 border border-gray-100 p-5 text-center">
          <p className="text-sm font-bold text-gray-500">Nenhuma retirada agendada.</p>
          <p className="mt-1 text-xs text-gray-400 font-semibold">Crie ou aceite uma retirada para começar.</p>
        </div>
      )}
    </div>
  );

  const SaudeCard = () => (
    <div className="bg-white rounded-3xl border border-gray-100 p-5 lg:p-6 shadow-sm">
      <div className="flex items-center justify-between gap-4 mb-5">
        <h3 className="text-xs font-black uppercase tracking-[0.2em] text-gray-400">SAÚDE DO PONTO</h3>
        <Link href="/perfil/operacional" className="text-xs font-bold text-[#006a62] hover:underline flex items-center gap-0.5">
          <span>Perfil público</span>
          <ArrowRight size={13} />
        </Link>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-50 rounded-2xl p-4 flex flex-col justify-between">
          <span className="text-[10px] font-black uppercase tracking-wider text-gray-400">PARCERIA</span>
          <h4 className="text-lg font-black text-gray-900 tracking-tight leading-snug mt-1">{activePartnerName || 'Sem ativa'}</h4>
          <div className="mt-3">
            <span className={`inline-flex rounded-full px-2.5 py-0.5 text-[10px] font-bold ${activePartnerName ? 'bg-emerald-50 text-emerald-700 border border-emerald-100/60' : 'bg-gray-100 text-gray-500'}`}>
              {activePartnerName ? 'Ativa' : 'Pendente'}
            </span>
          </div>
        </div>
        
        <div className="bg-gray-50 rounded-2xl p-4 flex flex-col justify-between">
          <span className="text-[10px] font-black uppercase tracking-wider text-gray-400">PERFIL</span>
          <h4 className="text-lg font-black text-gray-900 tracking-tight leading-snug mt-1">
            {completion ? `${completion.completedItems}/${completion.totalItems}` : '11/11'}
          </h4>
          <div className="mt-3">
            <span className="inline-flex rounded-full bg-blue-50 text-blue-700 border border-blue-100/60 px-2.5 py-0.5 text-[10px] font-bold">
              {completionPercent === 100 ? 'Completo' : 'Incompleto'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="px-4 pb-12 pt-4 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-shell space-y-6">
        {hasDataError && (
          <section className="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
            <div className="flex gap-3">
              <AlertCircle size={18} className="mt-0.5 flex-shrink-0" />
              <p>
                Alguns dados operacionais não puderam ser carregados agora. Os blocos abaixo usam
                somente informações disponíveis nesta leitura.
              </p>
            </div>
          </section>
        )}

        {/* Dashboard Title & Responsive Header Controls */}
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h1 className="text-3xl font-black text-gray-950 tracking-tight">Bom dia, {firstName}</h1>
              {isVerified && (
                <span className="inline-flex items-center gap-1 bg-[#e2f5f1] border border-[#a3e3d4] rounded-full px-2.5 py-0.5 text-[11px] font-bold text-[#006a62]">
                  <Check size={12} strokeWidth={3} />
                  Verificado
                </span>
              )}
            </div>
            <div className="flex flex-wrap items-center gap-x-3 gap-y-1.5 text-xs text-gray-500 font-bold mt-1.5">
              <div className="flex items-center gap-1">
                <MapPin size={14} className="text-gray-400" />
                <span>{activePartnerName || 'EcoVerse'} · {roleLabel}</span>
              </div>
              <div className="flex items-center gap-1 bg-amber-50 border border-amber-100 rounded-full px-2.5 py-0.5 text-[10px] font-bold text-amber-700">
                <AlertCircle size={11} />
                <span>{pendingCount} pendente(s)</span>
              </div>
            </div>
          </div>

          {/* Desktop Right Side Inputs */}
          <div className="flex flex-wrap items-center gap-3 md:justify-end">
            {/* Search Input */}
            <div className="relative flex-1 min-w-[240px] md:max-w-xs">
              <Search size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Buscar descarte"
                className="w-full bg-white border border-gray-200 rounded-full pl-10 pr-12 py-2.5 text-sm text-gray-800 placeholder-gray-400 shadow-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              />
              <kbd className="absolute right-3 top-1/2 -translate-y-1/2 hidden md:flex h-5 px-1.5 items-center justify-center text-[9px] font-black bg-gray-50 border border-gray-200 rounded text-gray-400">/</kbd>
            </div>

            {/* Calendar & Period selection group */}
            <div className="flex items-center gap-1 bg-white border border-gray-200 rounded-full p-1 shadow-sm">
              <div className="flex items-center gap-1.5 px-3 text-xs font-bold text-gray-500 whitespace-nowrap">
                <Calendar size={14} className="text-gray-400" />
                <span>{dateRangeLabel}</span>
              </div>
              <div className="w-px h-4 bg-gray-200" />
              <div className="flex items-center gap-0.5">
                {OPERATIONAL_PERIOD_OPTIONS.map((option) => (
                  <Link
                    key={option.value}
                    href={option.value === '7d' ? '/inicio' : `/inicio?period=${option.value}`}
                    className={`rounded-full px-3.5 py-1.5 text-xs font-bold transition-all ${
                      period === option.value
                        ? 'bg-[#0f2a2d] text-white shadow-sm'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    {option.label}
                  </Link>
                ))}
              </div>
            </div>

            {/* Public profile button */}
            <Link
              href="/perfil/operacional"
              className="flex items-center gap-1.5 bg-white border border-gray-200 hover:bg-gray-50 rounded-full px-4 py-2.5 text-xs font-bold text-gray-700 shadow-sm transition-all"
            >
              <Eye size={14} className="text-gray-400" />
              <span>Ver perfil público</span>
            </Link>
          </div>
        </div>

        {/* Desktop Viewport Main Progress Flow */}
        <div className="hidden md:block py-2">
          <ColetasProgressBar />
        </div>

        {/* Mobile Viewport QR Scanner Card */}
        <ScanCard isMobile={true} />

        {/* Mobile Viewport Progress Flow */}
        <div className="md:hidden mt-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">FLUXO DAS COLETAS</span>
            <Link href="/operacoes" className="text-xs font-bold text-[#006a62] hover:underline flex items-center gap-0.5">
              <span>Fila</span>
              <ArrowRight size={12} />
            </Link>
          </div>
          <ColetasProgressBar />
        </div>

        {/* Four Status Cards Grid */}
        <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
          {operationalStageCards.map((card) => {
            const Icon = card.icon;
            return (
              <Link
                key={card.label}
                href={`/operacoes?status=${card.status}`}
                className="bg-white rounded-3xl border border-gray-100 p-4 shadow-sm hover:border-gray-200 hover:shadow transition-all flex flex-col justify-between min-h-[140px] md:min-h-[220px]"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1.5">
                      <span className={`w-2 h-2 rounded-full ${card.bgClass}`} />
                      <span className="text-[10px] font-black uppercase tracking-wider text-gray-400">{card.label}</span>
                    </div>
                    {card.status === 'PENDING' && Icon && <Icon size={14} className="text-amber-500" />}
                  </div>
                  
                  <div className="flex items-center justify-between mt-3">
                    <div>
                      <span className="text-4xl md:text-5xl font-black text-gray-900 leading-none">{card.count}</span>
                      <p className="text-[10px] text-gray-400 font-bold mt-1 leading-snug">{card.hint}</p>
                    </div>
                    <div className="flex flex-col items-end gap-1">
                      <Sparkline color={card.color} />
                      <span className={`inline-flex items-center gap-0.5 text-xs font-black ${card.isTrendUp ? 'text-emerald-600' : 'text-gray-500'}`}>
                        {card.isTrendUp ? '↗' : '↘'} {card.trend}
                        <span className="md:hidden font-medium text-[9px] text-gray-400 ml-0.5">esta semana</span>
                      </span>
                    </div>
                  </div>
                </div>

                {/* Footer Section (Desktop Only) */}
                <div className="hidden md:block border-t border-gray-100 pt-3 mt-4">
                  {card.donations.length > 0 ? (
                    <div className="space-y-1.5">
                      {card.donations.slice(0, 2).map((donation) => (
                        <div key={donation.id} className={`flex items-center justify-between px-2.5 py-1.5 rounded-xl text-xs font-bold ${card.itemBgClass}`}>
                          <span className="truncate max-w-[120px]">{donation.code}</span>
                          <span className="opacity-70 flex-shrink-0">{donation.itemCount}×</span>
                        </div>
                      ))}
                      {card.donations.length > 2 && (
                        <div className="text-[10px] font-black text-[#006a62] hover:text-[#004d40] text-left pl-1">
                          + {card.donations.length - 2} mais →
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="text-xs text-gray-300 font-bold py-1 text-left pl-1">—</div>
                  )}
                </div>
              </Link>
            );
          })}
        </div>

        {/* Mobile Viewport Recommended Next Action */}
        <NextActionCard isMobile={true} />

        {/* Desktop Viewport Double Action Row */}
        <div className="hidden md:grid grid-cols-12 gap-5 items-stretch">
          <div className="col-span-5">
            <ScanCard isMobile={false} />
          </div>
          <div className="col-span-7">
            <NextActionCard isMobile={false} />
          </div>
        </div>

        {/* Agenda & Saúde Section */}
        <div className="grid grid-cols-1 gap-5 lg:grid-cols-12">
          <div className="lg:col-span-7">
            <AgendaCard />
          </div>
          <div className="lg:col-span-5">
            <SaudeCard />
          </div>
        </div>

        {(role === 'COLLECTION_POINT' || role === 'NGO') && (
          <PickupRequestsPanel
            role={role}
            accessToken={accessToken}
            initialPickupRequests={pickupRequests}
            partnerships={partnerships}
          />
        )}
      </div>
    </div>
  );
}

function AdminHome({
  firstName,
  pendingApprovals,
  pendingRevisions,
  notifications,
}: {
  firstName: string;
  pendingApprovals: AdminProfileRecord[];
  pendingRevisions: AdminProfileRecord[];
  notifications: NotificationRecord[];
}) {
  return (
    <div className="vg-dark-fix px-4 pb-6 pt-6 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-shell space-y-4">
        <section className="rounded-[2rem] bg-white p-6 shadow-card lg:p-8">
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex items-center gap-2 rounded-full bg-primary-light px-4 py-2 text-[11px] font-bold uppercase tracking-[0.18em] text-primary">
              <ShieldCheck size={14} />
              Governança ativa
            </span>
            <span className="rounded-full bg-surface px-4 py-2 text-[11px] font-bold uppercase tracking-[0.18em] text-gray-500">
              Administrador
            </span>
          </div>
          <h1 className="mt-5 text-3xl font-black tracking-tight text-primary-deeper sm:text-4xl">
            Olá, {firstName}
          </h1>
          <div className="mt-6 grid gap-3 sm:grid-cols-3">
            <Link href="/admin/perfis" className="rounded-[1.5rem] bg-surface p-4 transition-colors hover:bg-primary-light/40">
              <p className="text-3xl font-black text-primary-deeper">{pendingApprovals.length}</p>
              <p className="mt-1 text-sm font-semibold text-gray-500">Perfis aguardando aprovação</p>
            </Link>
            <Link href="/admin/perfis" className="rounded-[1.5rem] bg-surface p-4 transition-colors hover:bg-primary-light/40">
              <p className="text-3xl font-black text-primary-deeper">{pendingRevisions.length}</p>
              <p className="mt-1 text-sm font-semibold text-gray-500">Revisões públicas pendentes</p>
            </Link>
            <Link href="/notificacoes" className="rounded-[1.5rem] bg-surface p-4 transition-colors hover:bg-primary-light/40">
              <p className="text-3xl font-black text-primary-deeper">{notifications.length}</p>
              <p className="mt-1 text-sm font-semibold text-gray-500">Alertas recentes</p>
            </Link>
          </div>
        </section>

        <section className="grid gap-4 lg:grid-cols-2">
          <div className="rounded-[2rem] bg-white p-6 shadow-card">
            <div className="flex items-center justify-between gap-3">
              <div>
                <p className="text-[11px] font-bold uppercase tracking-[0.2em] text-gray-400">
                  Aprovação inicial
                </p>
                <h2 className="mt-2 text-2xl font-black text-primary-deeper">Perfis pendentes</h2>
              </div>
              <Link href="/admin/perfis" className="text-sm font-bold text-primary">Abrir</Link>
            </div>
            <div className="mt-5 space-y-3">
              {pendingApprovals.length > 0 ? (
                pendingApprovals.map((profile) => (
                  <div key={profile.id} className="rounded-[1.25rem] bg-surface p-4">
                    <p className="text-sm font-bold text-on-surface">
                      {profile.organizationName ?? profile.name}
                    </p>
                    <p className="mt-1 text-sm text-gray-500">
                      {ROLE_LABELS[profile.role] ?? profile.role}
                      {profile.city && profile.state ? ` · ${profile.city}, ${profile.state}` : ''}
                    </p>
                  </div>
                ))
              ) : (
                <div className="rounded-[1.25rem] bg-surface p-5 text-sm font-semibold text-primary-deeper">
                  Nenhum perfil novo aguardando aprovação.
                </div>
              )}
            </div>
          </div>

          <div className="rounded-[2rem] bg-white p-6 shadow-card">
            <div className="flex items-center justify-between gap-3">
              <div>
                <p className="text-[11px] font-bold uppercase tracking-[0.2em] text-gray-400">
                  Revisões públicas
                </p>
                <h2 className="mt-2 text-2xl font-black text-primary-deeper">Alterações pendentes</h2>
              </div>
              <Link href="/admin/perfis" className="text-sm font-bold text-primary">Revisar</Link>
            </div>
            <div className="mt-5 space-y-3">
              {pendingRevisions.length > 0 ? (
                pendingRevisions.map((profile) => (
                  <div key={profile.id} className="rounded-[1.25rem] bg-surface p-4">
                    <p className="text-sm font-bold text-on-surface">
                      {profile.organizationName ?? profile.name}
                    </p>
                    <p className="mt-1 text-sm text-gray-500">
                      {profile.pendingPublicRevision?.fields.length
                        ? profile.pendingPublicRevision.fields.join(', ')
                        : 'Alterações públicas aguardando avaliação'}
                    </p>
                  </div>
                ))
              ) : (
                <div className="rounded-[1.25rem] bg-surface p-5 text-sm font-semibold text-primary-deeper">
                  Nenhuma revisão pública pendente no momento.
                </div>
              )}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default async function InicioPage({
  searchParams: routeSearchParams,
}: {
  searchParams?: Promise<Record<string, string | string[] | undefined>>;
}) {
  const searchParams = await routeSearchParams;
  const session = await auth();
  const firstName = session?.user?.name?.split(' ')[0] ?? 'você';
  const accessToken = session?.user?.accessToken ?? '';
  const role = session?.user?.role ?? 'DONOR';

  if (role === 'ADMIN') {
    let pendingApprovals: AdminProfileRecord[] = [];
    let pendingRevisions: AdminProfileRecord[] = [];
    let notifications: NotificationRecord[] = [];

    if (accessToken) {
      const [pendingApprovalsResponse, pendingRevisionsResponse, notificationsResponse] =
        await Promise.allSettled([
          getAdminProfiles(accessToken, {
            status: 'PENDING',
            limit: 6,
          }),
          getAdminProfiles(accessToken, {
            revisionStatus: 'PENDING',
            limit: 6,
          }),
          getNotifications(accessToken, { limit: 8 }),
        ]);

      if (pendingApprovalsResponse.status === 'fulfilled') {
        pendingApprovals = pendingApprovalsResponse.value.data;
      }

      if (pendingRevisionsResponse.status === 'fulfilled') {
        pendingRevisions = pendingRevisionsResponse.value.data;
      }

      if (notificationsResponse.status === 'fulfilled') {
        notifications = notificationsResponse.value.data
          .filter((notification) => GOVERNANCE_NOTIFICATION_TYPES.has(notification.type))
          .slice(0, 5);
      }
    }

    return (
      <AdminHome
        firstName={firstName}
        pendingApprovals={pendingApprovals}
        pendingRevisions={pendingRevisions}
        notifications={notifications}
      />
    );
  }

  if (role !== 'DONOR') {
    const period = getOperationalPeriod(searchParams?.period);
    let profile: MyProfile | null = null;
    let partnerships: PartnershipRecord[] = [];
    let pickupRequests: PickupRequestRecord[] = [];
    let operationQueue: DonationRecord[] = [];
    let operationMeta: OperationalDonationListResponse['meta'] | null = null;
    let hasDataError = !accessToken;

    if (accessToken) {
      const [profileResponse, partnershipsResponse, pickupRequestsResponse, operationResponse] =
        await Promise.allSettled([
          getMyProfile(accessToken),
          getMyPartnerships(accessToken),
          getPickupRequests(accessToken),
          getOperationalDonations(accessToken, {
            limit: 8,
            sortBy: 'updatedAt',
            direction: 'desc',
            period,
          }),
        ]);

      hasDataError = [
        profileResponse,
        partnershipsResponse,
        pickupRequestsResponse,
        operationResponse,
      ].some((result) => result.status === 'rejected');

      if (profileResponse.status === 'fulfilled') {
        profile = profileResponse.value;
      }

      if (partnershipsResponse.status === 'fulfilled') {
        partnerships = partnershipsResponse.value.data;
      }

      if (pickupRequestsResponse.status === 'fulfilled') {
        pickupRequests = pickupRequestsResponse.value.data;
      }

      if (operationResponse.status === 'fulfilled') {
        operationQueue = operationResponse.value.data;
        operationMeta = operationResponse.value.meta;
      }
    }

    return (
      <OperationalHome
        accessToken={accessToken}
        firstName={firstName}
        role={role}
        profile={profile}
        partnerships={partnerships}
        pickupRequests={pickupRequests}
        operationQueue={operationQueue}
        operationMeta={operationMeta}
        period={period}
        hasDataError={hasDataError}
      />
    );
  }

  let donations: DonationRecord[] = [];
  let nearbyPoints: Awaited<ReturnType<typeof getNearbyPoints>>['data'] = [];
  let gamification: DonorGamificationResponse | null = null;

  if (accessToken) {
    const [donationsResult, pointsResult, gamificationResult] = await Promise.allSettled([
      getUserDonations(accessToken, { limit: 20 }),
      getNearbyPoints({ lat: -23.50153, lng: -47.45256, radius: 15, limit: 3 }),
      getMyGamification(accessToken),
    ]);

    if (donationsResult.status === 'fulfilled') {
      donations = donationsResult.value.data;
    }

    if (pointsResult.status === 'fulfilled') {
      nearbyPoints = pointsResult.value.data;
    }

    if (gamificationResult.status === 'fulfilled') {
      gamification = gamificationResult.value;
    }
  }

  return (
    <DonorHome
      firstName={firstName}
      donations={donations}
      nearbyPoints={nearbyPoints}
      gamification={gamification}
    />
  );
}
