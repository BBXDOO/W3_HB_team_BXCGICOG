import assert from 'node:assert/strict';
import { createBattle, beginTurn, useAction, advancePhase } from './battle_flow_probe.mjs';

const definition = {
  elements: ['น้ำ', 'ลม'], field: ['น้ำ', 'ลม'], phases: ['หลัก', 'รอง'], startingHp: { hero: 20, foe: 20 },
  equipped: { hero: ['ice-card'], foe: [] },
  actions: [
    { id: 'ice', name: 'ธนูน้ำแข็ง', cardId: 'ice-card', phase: 'หลัก', cost: { น้ำ: 2, ลม: 3 }, effects: [{ type: 'hp', target: 'opponent', amount: -7 }] },
    { id: 'cut', name: 'ตัดลมจากสนาม', phase: 'หลัก', cost: {}, effects: [{ type: 'field', element: 'ลม', enabled: false }] },
    { id: 'guard', name: 'ตั้งรับ', phase: 'รอง', cost: {}, effects: [{ type: 'hp', target: 'self', amount: 1 }] }
  ]
};
let state = createBattle(definition, ['hero', 'foe']).state;
state = beginTurn(definition, state).state;
assert.deepEqual(state.mana.hero, { น้ำ: 2, ลม: 2 });
assert.equal(beginTurn(definition, state).ok, false);
const snapshot = JSON.stringify(state);
assert.equal(useAction(definition, state, 'ice').reason, 'มานา ลม ไม่พอ');
assert.equal(JSON.stringify(state), snapshot, 'failed cast never spends water');
state = { ...state, mana: { ...state.mana, hero: { น้ำ: 4, ลม: 5 } } };
state = useAction(definition, state, 'ice').state;
assert.deepEqual([state.mana.hero.น้ำ, state.mana.hero.ลม, state.hp.foe], [2, 2, 13]);
state = useAction(definition, state, 'cut').state;
assert.deepEqual(state.field, ['น้ำ']);
assert.equal(state.mana.hero.ลม, 2, 'field removal preserves stored mana');
state = advancePhase(definition, state).state;
assert.equal(useAction(definition, state, 'ice').ok, false);
state = useAction(definition, state, 'guard').state;
state = advancePhase(definition, state).state;
assert.equal(state.active, 'foe');
state = beginTurn(definition, state).state;
assert.deepEqual(state.mana.foe, { น้ำ: 2 });
assert.deepEqual(JSON.parse(JSON.stringify(state)), state, 'saved state can restore without replay');
assert.equal(state.log.length, 5);
const atCap = { ...state, started: false, mana: { ...state.mana, foe: { น้ำ: 9 } } };
assert.equal(beginTurn(definition, atCap).state.mana.foe.น้ำ, 10);
console.log('PASS: refill, cap boundary, atomic cost, equipped card, field change, phase, turn swap, restore');

const broken = { ...definition, actions: [{ id: 'bad', phase: 'หลัก', name: 'bad', cost: {}, effects: [{ type: 'unknown' }] }] };
assert.equal(useAction(broken, { ...state, active: 'hero', phaseIndex: 0 }, 'bad').ok, false);
assert.equal(useAction({ ...definition, equipped: { hero: [] } }, { ...state, active: 'hero', phaseIndex: 0 }, 'ice').reason, 'ยังไม่ได้ติดตั้งการ์ด');
console.log('PASS: unsupported effect and unequipped card rejected');
