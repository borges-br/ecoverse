-- Separate migration so added enum values are committed before use.
-- Existing integer quantities convert exactly; cooking oil is declared in L.
ALTER TABLE "donation_items" ALTER COLUMN "quantity" TYPE DOUBLE PRECISION USING "quantity"::DOUBLE PRECISION;
ALTER TABLE "donation_items" ALTER COLUMN "category" SET DEFAULT 'BATTERIES';
