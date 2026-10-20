import { DonationItemCondition, DonationStatus, ItemCategory } from '@prisma/client';

/**
 * EcoVerse: 10 points per confirmed participation, independent of quantities.
 * The following rules apply only to historical donation categories:
 * - Each item is worth 10 pts on AT_POINT confirmation.
 * - Items in EXCELLENT condition add +5 pts each on AT_POINT.
 * - Subtotal is multiplied by a category-diversity multiplier.
 * - Multiple unique categories on a single donation increase the multiplier.
 * - DISTRIBUTED status adds a +5 per item bonus, no multiplier.
 * - PENDING and CANCELLED award no real points.
 * - Seasonal campaign multipliers are intentionally not applied here yet.
 */

export const CONFIRMED_DONATION_STATUSES: DonationStatus[] = [
  DonationStatus.AT_POINT,
  DonationStatus.IN_TRANSIT,
  DonationStatus.DELIVERED,
  DonationStatus.DISTRIBUTED,
];

export const POINTS_PER_ITEM_CONFIRMED = 10;
export const POINTS_PER_EXCELLENT_ITEM_BONUS = 5;
export const POINTS_PER_ITEM_DISTRIBUTED_BONUS = 5;

export function isConfirmedDonationStatus(status: DonationStatus) {
  return CONFIRMED_DONATION_STATUSES.includes(status);
}

export function getCategoryMultiplier(uniqueCategories: number) {
  if (uniqueCategories <= 1) return 1.0;
  if (uniqueCategories === 2) return 1.1;
  if (uniqueCategories === 3) return 1.2;
  if (uniqueCategories === 4) return 1.4;
  return 1.8;
}

export type DonationPointsItemInput = {
  category: ItemCategory;
  quantity: number;
  condition: DonationItemCondition;
};

export type DonationPointsBreakdown = {
  totalItems: number;
  excellentItems: number;
  uniqueCategories: number;
  categoryMultiplier: number;
  seasonalMultiplier: number;
  confirmationBase: number;
  conditionBonus: number;
  confirmationPoints: number;
  distributionBonus: number;
  totalPotentialPoints: number;
  pointsForCurrentStatus: number;
};

export type CalculateDonationPointsInput = {
  items: DonationPointsItemInput[];
  status: DonationStatus;
};

export function calculateDonationPointsBreakdown(
  input: CalculateDonationPointsInput,
): DonationPointsBreakdown {
  const items = input.items ?? [];
  // EcoVerse rewards a confirmed participation, independent of volume,
  // conservation and variety. Historical donation formulas stay readable.
  const ecoCategories = ['BATTERIES','ELECTRONICS','LAMPS','COOKING_OIL'];
  if (items.length > 0 && items.every(item => ecoCategories.includes(item.category))) {
    return { totalItems: items.filter(item => item.category !== 'COOKING_OIL').reduce((sum,item) => sum + item.quantity,0), excellentItems:0, uniqueCategories:new Set(items.map(item => item.category)).size, categoryMultiplier:1, seasonalMultiplier:1, confirmationBase:10, conditionBonus:0, confirmationPoints:10, distributionBonus:0, totalPotentialPoints:10, pointsForCurrentStatus: ['AT_POINT','IN_TRANSIT','DELIVERED','DISTRIBUTED'].includes(input.status) ? 10 : 0 };
  }

  const totalItems = items.reduce((sum, item) => sum + Math.max(0, item.quantity), 0);
  const excellentItems = items
    .filter((item) => item.condition === DonationItemCondition.EXCELLENT)
    .reduce((sum, item) => sum + Math.max(0, item.quantity), 0);
  const uniqueCategories = new Set(items.map((item) => item.category)).size;
  const categoryMultiplier = getCategoryMultiplier(uniqueCategories);
  const seasonalMultiplier = 1;

  const confirmationBase = totalItems * POINTS_PER_ITEM_CONFIRMED;
  const conditionBonus = excellentItems * POINTS_PER_EXCELLENT_ITEM_BONUS;
  const confirmationSubtotal = confirmationBase + conditionBonus;
  const confirmationPoints = Math.round(confirmationSubtotal * categoryMultiplier);
  const distributionBonus = totalItems * POINTS_PER_ITEM_DISTRIBUTED_BONUS;
  const totalPotentialPoints = confirmationPoints + distributionBonus;

  let pointsForCurrentStatus = 0;
  switch (input.status) {
    case DonationStatus.PENDING:
    case DonationStatus.CANCELLED:
      pointsForCurrentStatus = 0;
      break;
    case DonationStatus.AT_POINT:
    case DonationStatus.IN_TRANSIT:
    case DonationStatus.DELIVERED:
      pointsForCurrentStatus = confirmationPoints;
      break;
    case DonationStatus.DISTRIBUTED:
      pointsForCurrentStatus = totalPotentialPoints;
      break;
  }

  return {
    totalItems,
    excellentItems,
    uniqueCategories,
    categoryMultiplier,
    seasonalMultiplier,
    confirmationBase,
    conditionBonus,
    confirmationPoints,
    distributionBonus,
    totalPotentialPoints,
    pointsForCurrentStatus,
  };
}

export function buildConfirmationLedgerKey(donationId: string) {
  return `donation:${donationId}:confirmed-at-point`;
}

export function buildDistributionLedgerKey(donationId: string) {
  return `donation:${donationId}:distributed`;
}
