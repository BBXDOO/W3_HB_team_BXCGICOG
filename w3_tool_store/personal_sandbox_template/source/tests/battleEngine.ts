import { strict as assert } from 'node:assert';
import { advanceBattle, beginTurn, newBattle, parseBattleProgress, performBattleAction } from '../core/battle';
import { parseRunState } from '../core/runState';
import type { BattleConfig, StoryPack } from '../types';
const config: BattleConfig = { elements: ['น้ำ', 'ลม'], field: { name: 'สนาม', elements: ['น้ำ','ลม'] }, phases: [{ id: 'main', name: 'หลัก' }, { id: 'next', name: 'รอง' }], actions: [
  { id: 'ice', name: 'ธนูน้ำแข็ง', kind: 'Skill', phaseId: 'main', cost: { น้ำ: 2, ลม: 3 }, effects: [{type: 'vital', target: 'opponent', stat: 'hp', amount: -7}] },
  { id: 'cut', name: 'ตัดลม', kind: 'Skill', phaseId: 'main', cost: {}, effects: [{ type: 'field', element: 'ลม', enabled: false }] }
] };
const fighter = (id: string) => ({ id, name: id, vitals: { hp: 20, mp: 5, en: 5 }, abilitySlots: [] });
const story = { storyId: 'test', characters: [fighter('a'), fighter('b')], rulesets: [], commonPlay: [] } as unknown as StoryPack;
let state = newBattle(story, config, 'a', 'b').progress!;
assert.equal(beginTurn(story, config, state).progress!.mana.a['น้ำ'], 2);
state = beginTurn(story, config, state).progress!;
assert.equal(beginTurn(story, config, state).ok, false, 'start cannot refill twice');
let blocked = performBattleAction(story, config, state, config.actions[0]);
assert.equal(blocked.ok, false, 'wind shortage rejects whole action');
assert.equal(state.mana.a['น้ำ'], 2, 'water remains unchanged on rejection');
state = { ...state, mana: { ...state.mana, a: { น้ำ: 4, ลม: 5 } } };
let result = performBattleAction(story, config, state, config.actions[0]);
assert.equal(result.ok, true);
assert.deepEqual([result.progress!.mana.a['น้ำ'], result.progress!.mana.a['ลม'], result.progress!.vitals.b.hp], [2, 2, 13]);
state = result.progress!;
state = performBattleAction(story, config, state, config.actions[1]).progress!;
assert.deepEqual(state.fieldElements, ['น้ำ']);
assert.equal(state.mana.a['ลม'], 2, 'cutting field does not erase accumulated mana');
state = advanceBattle(story, config, state).progress!;
assert.equal(state.phaseIndex, 1);
assert.equal(performBattleAction(story, config, state, config.actions[0]).ok, false, 'wrong phase');
state = advanceBattle(story, config, state).progress!;
assert.equal(state.activeId, 'b');
assert.equal(state.started, false);
state = beginTurn(story, config, state).progress!;
assert.deepEqual(state.mana.b, { น้ำ: 2 }, 'cut element does not replenish next turn');
const snapshot = JSON.parse(JSON.stringify(state));
assert.deepEqual(parseBattleProgress(snapshot), state);
assert.deepEqual(parseRunState({version: 1, storyId:'test', currentNodeId:null, activeCharacterId:null, savedAt:1, battle:snapshot}, 'test')?.battle, state);
assert.equal(parseBattleProgress({ ...snapshot, mana: { a: { น้ำ: -1 } } }), null);
console.log('battle engine: costs, atomic failure, field, phases, save/restore passed');
