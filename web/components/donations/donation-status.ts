import {
  CheckCircle,
  Clock,
  Package,
  Truck,
  XCircle,
  type LucideIcon,
} from 'lucide-react';
import type { DonationStatus } from '@/lib/api';
import { formatDateTimeLabel } from '@/lib/date-time';

export const DONATION_STATUS_ORDER: DonationStatus[] = [
  'PENDING',
  'AT_POINT',
  'IN_TRANSIT',
  'DELIVERED',
  'DISTRIBUTED',
];

export const DONATION_STATUS_CONFIG: Record<
  DonationStatus,
  {
    label: string;
    description: string;
    color: string;
    bg: string;
    icon: LucideIcon;
  }
> = {
  PENDING: {
    label: 'Aguardando entrega',
    description: 'Descarte registrado. Aguardando entrega no ponto de coleta.',
    color: 'text-amber-600',
    bg: 'bg-amber-50',
    icon: Clock,
  },
  AT_POINT: {
    label: 'No ponto',
    description: 'Item recebido no ponto de coleta e aguardando o próximo passo.',
    color: 'text-blue-600',
    bg: 'bg-blue-50',
    icon: Package,
  },
  IN_TRANSIT: {
    label: 'Em trânsito',
    description: 'O descarte está em deslocamento para o parceiro responsável.',
    color: 'text-indigo-600',
    bg: 'bg-indigo-50',
    icon: Truck,
  },
  DELIVERED: {
    label: 'Recebido no destino',
    description: 'Recebimento confirmado pelo operador no destino parceiro.',
    color: 'text-primary',
    bg: 'bg-primary-light',
    icon: CheckCircle,
  },
  DISTRIBUTED: {
    label: 'Processamento informado',
    description: 'O parceiro informou o encerramento do processamento. Este registro não é um certificado de reciclagem.',
    color: 'text-emerald-600',
    bg: 'bg-emerald-50',
    icon: CheckCircle,
  },
  CANCELLED: {
    label: 'Cancelado',
    description: 'Este descarte foi cancelado.',
    color: 'text-red-500',
    bg: 'bg-red-50',
    icon: XCircle,
  },
};

export const DONATION_STATUS_ACTIONS: Record<
  DonationStatus,
  { label: string; description: string }
> = {
  PENDING: {
    label: 'Aguardando recebimento',
    description: 'O descarte foi registrado e ainda não iniciou o fluxo operacional.',
  },
  AT_POINT: {
    label: 'Receber no ponto',
    description: 'Recebimento registrado no ponto parceiro.',
  },
  IN_TRANSIT: {
    label: 'Vincular a carga & despachar',
    description: 'Envio para a operador parceiro confirmado.',
  },
  DELIVERED: {
    label: 'Confirmar recebimento',
    description: 'Recebimento confirmado pela operador parceiro.',
  },
  DISTRIBUTED: {
    label: 'Informar processamento',
    description: 'Processamento informado pelo operador.',
  },
  CANCELLED: {
    label: 'Cancelar descarte',
    description: 'Descarte cancelado antes da coleta.',
  },
};

export function formatDonationDateLabel(input: string) {
  return formatDateTimeLabel(input);
}
