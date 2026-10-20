import { Battery, Monitor, Lightbulb, Droplets } from 'lucide-react';
import type { ItemCategory } from './api';
export const MATERIALS = [
  { id: 'BATTERIES', label: 'Pilhas e baterias', short: 'Pilhas', icon: Battery, unit: 'un.', hint: 'Pilhas e baterias portáteis', detail: 'O tipo de bateria faz diferença. Confira as restrições do ponto e confirme o recebimento de itens danificados antes de levar.', tone: 'sage' },
  { id: 'ELECTRONICS', label: 'Eletrônicos', short: 'Eletrônicos', icon: Monitor, unit: 'un.', hint: 'Aparelhos e componentes eletrônicos', detail: 'Verifique quais aparelhos o ponto recebe, seus limites de tamanho e as condições de entrega. Cuide dos seus dados pessoais antes de entregar dispositivos.', tone: 'blue' },
  { id: 'LAMPS', label: 'Lâmpadas', short: 'Lâmpadas', icon: Lightbulb, unit: 'un.', hint: 'Tipos aceitos conforme cada ponto', detail: 'LED, fluorescentes e outros tipos podem ter destinos diferentes. Consulte o ponto sobre o tipo, o estado e as condições de recebimento.', tone: 'sage' },
  { id: 'COOKING_OIL', label: 'Óleo de cozinha', short: 'Óleo', icon: Droplets, unit: 'L', hint: 'Óleo de cozinha usado, em litros', detail: 'Consulte as condições de acondicionamento e a quantidade aceita pelo ponto. Esta categoria é exclusiva para óleo de cozinha; não inclui óleo lubrificante.', tone: 'amber' },
] as const;
export type MaterialCategory = typeof MATERIALS[number]['id'];
export function isMaterialCategory(value: unknown): value is MaterialCategory { return MATERIALS.some(m => m.id === value); }
export const MATERIAL_LABELS: Record<ItemCategory, string> = {
  BATTERIES: 'Pilhas e baterias', ELECTRONICS: 'Eletrônicos', LAMPS: 'Lâmpadas', COOKING_OIL: 'Óleo de cozinha',
  CLOTHING: 'Roupas (legado)', SHOES: 'Calçados (legado)', ACCESSORIES: 'Acessórios (legado)', BAGS: 'Bolsas (legado)', TOYS: 'Brinquedos (legado)', FOOD: 'Alimentos (legado)', OTHER: 'Outros (legado)',
};
export function formatMaterialQuantity(item: { quantity: number; category: string }) { return `${new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 2 }).format(item.quantity)} ${item.category === 'COOKING_OIL' ? 'L' : 'un.'}`; }
