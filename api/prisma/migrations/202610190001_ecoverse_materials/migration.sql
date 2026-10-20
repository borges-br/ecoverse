-- Additive migration: legacy categories and records are preserved.
ALTER TYPE "ItemCategory" ADD VALUE IF NOT EXISTS 'BATTERIES';
ALTER TYPE "ItemCategory" ADD VALUE IF NOT EXISTS 'ELECTRONICS';
ALTER TYPE "ItemCategory" ADD VALUE IF NOT EXISTS 'LAMPS';
ALTER TYPE "ItemCategory" ADD VALUE IF NOT EXISTS 'COOKING_OIL';
