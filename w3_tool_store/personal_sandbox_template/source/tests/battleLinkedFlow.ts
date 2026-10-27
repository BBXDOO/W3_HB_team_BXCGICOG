import { strict as assert } from 'node:assert';
import { advanceBattle, beginTurn, newBattle, performBattleAction, parseBattleProgress } from '../core/battle';
import { createEmptyProject } from '../core/project';
import type { CharacterPack } from '../types';

const story = createEmptyProject('test-linked', 'concept', 'ทดลอง');
assert.equal(story.battleConfig?.manaPerTurn, 2);
assert.ok(story.runPresentation?.sections.some(entry => entry.source === 'battle'));
const character = (id: string): CharacterPack => ({
  id, name: id, className: '', charType: '', vitals: { hp: 20, mp: 5, en: 5 }, capabilities: { POW: 4 },
  attributes: { ACT: 3, DEF: 2, SPE: 1, CRI: 0 }, logicSlots: {}, statusEffects: [],
  elemental: { yangGroup: [], yinGroup: [] }, innateSkill: { name: '', description: '', rarity: 0 },
  resonanceMatrix: [], abilitySlots: [{ name: 'card', equippedCardId: id === 'hero' ? 'ice' : undefined }], backgroundText: ''
});
story.characters = [character('hero'), character('foe')];
story.cards = [{ id: 'ice', name: 'น้ำแข็ง', type: 'SKILL', rarity: 'Common', grade: 'C', accessLevel: 'A',
  description: '', inputCondition: '', logicCode: '', effectResult: '', cost: 0, cooldownTurns: 0, moduleSlots: ['poison', null] }];
story.modules = [{ id: 'poison', name: 'พิษ', type: 'support', grade: 'C', description: '', parts: { A: '', B: '', C: '' },
  battleLink: { tag: 'SKILL', ruleId: 'when-strong', effects: [{ type: 'status', target: 'opponent', status: 'ติดพิษ', enabled: true }] } }];
story.rulesets = [{ id: 'when-strong', name: 'ต้องมี ACT', modifiers: [], blocks: [
  { title: 'ACT', content: '', kind: 'condition', inputKey: 'battle.self.attributes.ACT', operator: '>=', expected: '3' }
] }, { id: 'poison-gate', name: 'ติดพิษก่อนผ่าน', modifiers: [], blocks: [
  { title: 'ติดพิษ', content: '', kind: 'condition', inputKey: 'battle.opponent.status.ติดพิษ', operator: 'exists' }
] }];
const config = story.battleConfig!;
config.elements = ['น้ำ', 'ลม']; config.field.elements = ['น้ำ', 'ลม']; config.manaPerTurn = 3;
config.phases = [{ id: 'main', name: 'หลัก', ruleId: 'poison-gate' }, { id: 'end', name: 'รอง' }];
config.actions = [{ id: 'cast', name: 'ลูกศรน้ำแข็ง', kind: 'Skill', phaseId: 'main', sourceCardId: 'ice',
  cost: { น้ำ: 2, ลม: 2 }, effects: [{ type: 'vital', target: 'opponent', stat: 'hp', amount: -2,
    scale: { source: 'self', stat: 'POW', multiplier: -1 } }] }];
let state = beginTurn(story, config, newBattle(story, config, 'hero', 'foe').progress!).progress!;
assert.deepEqual(state.mana.hero, { น้ำ: 3, ลม: 3 });
assert.equal(advanceBattle(story, config, state).ok, false, 'phase rule blocks until latest state has poison');
state = performBattleAction(story, config, state, config.actions[0]).progress!;
assert.deepEqual([state.vitals.foe.hp, state.mana.hero.น้ำ], [14, 1]);
assert.deepEqual(state.statuses?.foe, ['ติดพิษ']);
assert.equal(advanceBattle(story, config, state).progress?.phaseIndex, 1);
assert.deepEqual(parseBattleProgress(JSON.parse(JSON.stringify(state))), state);
const broken = { ...config.actions[0], effects: [{ type: 'vital' as const, target: 'opponent' as const, stat: 'hp' as const, amount: 0,
  scale: { source: 'self' as const, stat: 'MISSING', multiplier: 1 } }] };
assert.equal(performBattleAction(story, config, state, broken).ok, false, 'unknown stat rejects without mutation');
story.cards[0].type = 'CORE';
const noLink = performBattleAction(story, config, { ...state, mana: { ...state.mana, hero: { น้ำ: 3, ลม: 3 } } }, config.actions[0]);
assert.equal(noLink.ok, true);
assert.deepEqual(noLink.progress?.statuses?.foe, ['ติดพิษ'], 'old status remains, mismatched module does not add another');
console.log('battle linked flow: default, character stat, rune-like module, status, rule gate, save passed');
