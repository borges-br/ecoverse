const test = require('node:test');
const assert = require('node:assert/strict');
const { createDisposalSchema, assertMaterialsAccepted } = require('../dist/shared/disposal');
const { calculateDonationPointsBreakdown } = require('../dist/shared/donation-points');
const body = (category, quantity) => ({ collectionPointId:'test-point', items:[{name:'Material de teste',category,quantity}] });

test('oil accepts decimal litres while countable materials require whole units', () => {
  assert.equal(createDisposalSchema.parse(body('COOKING_OIL',1.25)).items[0].quantity,1.25);
  assert.equal(createDisposalSchema.safeParse(body('COOKING_OIL',1.234)).success,false);
  assert.equal(createDisposalSchema.safeParse(body('BATTERIES',1.5)).success,false);
  for (const qty of [0,-1,NaN,Infinity,1001]) assert.equal(createDisposalSchema.safeParse(body('LAMPS',qty)).success,false);
});
test('new registrations reject legacy and excluded categories', () => {
  for (const category of ['CLOTHING','OTHER','MEDICINE','SYRINGE']) assert.equal(createDisposalSchema.safeParse(body(category,1)).success,false);
});
test('point acceptance must include every material; empty is not universal acceptance', () => {
  assert.doesNotThrow(() => assertMaterialsAccepted([{category:'BATTERIES'}],['BATTERIES']));
  assert.throws(() => assertMaterialsAccepted([{category:'BATTERIES'}],[]),{statusCode:409});
  assert.throws(() => assertMaterialsAccepted([{category:'BATTERIES'},{category:'LAMPS'}],['BATTERIES']),{statusCode:409});
});
test('eco participation is confirmed once and is independent of volume, diversity and condition', () => {
  const small=[{category:'BATTERIES',quantity:1,condition:'GOOD'}];
  const large=[{category:'BATTERIES',quantity:100,condition:'EXCELLENT'},{category:'COOKING_OIL',quantity:12.5,condition:'GOOD'}];
  for (const items of [small,large]) {
    for (const status of ['PENDING','CANCELLED']) assert.equal(calculateDonationPointsBreakdown({items,status}).pointsForCurrentStatus,0);
    for (const status of ['AT_POINT','IN_TRANSIT','DELIVERED','DISTRIBUTED']) {
      const result=calculateDonationPointsBreakdown({items,status});assert.equal(result.pointsForCurrentStatus,10);assert.equal(result.conditionBonus,0);assert.equal(result.distributionBonus,0);
    }
  }
});
test('historical donation calculations remain compatible', () => {
  const result=calculateDonationPointsBreakdown({items:[{category:'CLOTHING',quantity:2,condition:'EXCELLENT'}],status:'DISTRIBUTED'});
  assert.equal(result.pointsForCurrentStatus,40);
});
