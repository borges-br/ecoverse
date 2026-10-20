import { z } from 'zod';
import { ConflictError } from './errors';

export const DISPOSAL_CATEGORIES = ['BATTERIES', 'ELECTRONICS', 'LAMPS', 'COOKING_OIL'] as const;
export const disposalItemSchema = z.object({
  name: z.string().trim().min(2).max(120),
  category: z.enum(DISPOSAL_CATEGORIES),
  quantity: z.coerce.number().finite().positive().max(1000),
  // Retained for wire compatibility. Condition no longer changes eco points.
  condition: z.enum(['EXCELLENT', 'GOOD']).optional().default('GOOD'),
  description: z.string().trim().max(600).optional(),
}).superRefine((item, ctx) => {
  if (item.category !== 'COOKING_OIL' && !Number.isInteger(item.quantity)) {
    ctx.addIssue({ code: z.ZodIssueCode.custom, path: ['quantity'], message: 'Informe uma quantidade inteira em unidades.' });
  }
  if (item.category === 'COOKING_OIL' && Math.abs(item.quantity * 100 - Math.round(item.quantity * 100)) > 1e-7) {
    ctx.addIssue({ code: z.ZodIssueCode.custom, path: ['quantity'], message: 'Informe litros com até duas casas decimais.' });
  }
});
export const createDisposalSchema = z.object({
  collectionPointId: z.string().min(1), notes: z.string().trim().max(600).optional(), scheduledAt: z.string().datetime().optional(),
  items: z.array(disposalItemSchema).min(1).max(20),
  packages: z.array(z.object({ type: z.enum(['BAG','BOX']), size: z.enum(['SMALL','MEDIUM','LARGE']), quantity: z.coerce.number().int().min(1).max(50) })).max(20).optional().default([]),
});

/** Empty acceptedCategories is not an implicit permit to receive every residue. */
export function assertMaterialsAccepted(items: ReadonlyArray<{ category: string }>, acceptedCategories: readonly string[]) {
  if (items.some(item => !acceptedCategories.includes(item.category))) {
    throw new ConflictError('O ponto não recebe todos os materiais deste descarte. Escolha outro ponto ou ajuste os materiais.');
  }
}
export function isEcoDisposal(items: ReadonlyArray<{ category: string }>) {
  return items.length > 0 && items.every(item => (DISPOSAL_CATEGORIES as readonly string[]).includes(item.category));
}
