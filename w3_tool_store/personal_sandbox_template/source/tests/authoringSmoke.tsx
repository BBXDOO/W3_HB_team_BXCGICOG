import React from 'react';
import { renderToString } from 'react-dom/server';
import assert from 'node:assert/strict';
import { createEmptyProject } from '../core/project';
import { getWorldCell } from '../core/worldIndex';
import { buildPlayRuleContext } from '../core/playRuleContext';
import { evaluateRuleset } from '../core/ruleRuntime';
import { runModuleFlow } from '../core/moduleFlow';
import { runInteraction } from '../core/eventRuntime';
import { buildBackup, parseBackup, getStory, saveStory } from '../core/storage';
import { changeInventory } from '../core/inventory';
import { parseRunState, saveRunState, loadRunState } from '../core/runState';
import { DashboardTab } from '../features/dashboard/DashboardTab';
import { StoryTab } from '../features/story/StoryTab';
import { CharactersTab } from '../features/characters/CharactersTab';
import { CardsTab } from '../features/cards/CardsTab';
import { BoardTab } from '../features/board/BoardTab';
import { LocationSheet } from '../features/location/LocationSheet';
import { ItemSheet } from '../features/item/ItemSheet';
import { EventsTab } from '../features/events/EventsTab';
import { RulesTab } from '../features/rules/RulesTab';
import { CommonPlayTab } from '../features/common/CommonPlayTab';
import { PlaytestTab } from '../features/play/PlaytestTab';

const memory = new Map<string, string>();
(globalThis as any).localStorage = {
  getItem: (key: string) => memory.get(key) ?? null,
  setItem: (key: string, value: string) => { memory.set(key, value); },
  removeItem: (key: string) => { memory.delete(key); }
};

const story = createEmptyProject('sample-1', 'bookcraft', 'เมืองทดสอบ');
story.storyNodes.push({ nodeId: 'main-1', type: 'NarrativeBlock', title: 'MEP-1 บันทึก', body: 'ค้นพบคู่มือ', choices: [{ label: 'อ่านต่อ', toNodeId: 'sub-1' }] },
  { nodeId: 'sub-1', type: 'NarrativeBlock', title: 'SEP_1.0', body: 'ตอนย่อย', choices: [] });
story.characters.push({ id: 'char-1', name: 'นักสำรวจ', className: 'ผู้เรียน', charType: 'NPC',
  vitals: { hp: 80, mp: 10, en: 9 }, capabilities: { INT: 4, STR: 5, DEX: 5 }, attributes: { ACT: 1, DEF: 1, SPE: 1, CRI: 1 },
  logicSlots: {}, statusEffects: [], elemental: { yangGroup: [], yinGroup: [] },
  innateSkill: { name: 'สังเกต', description: 'อ่านบันทึก', rarity: 1 }, resonanceMatrix: [], abilitySlots: [], backgroundText: 'ผู้ค้นหา' });
story.boards.push({ boardId: 'board-1', title: 'ประเทศไทย', width: 3, height: 3, cellMap: {
  '1_1': { x: 1, y: 1, name: 'หอสมุด', type: 'Location', locationRefId: 'loc-1', eventRefs: ['event-1'] }
}, explored: {}, visionRangeDefault: 2, movementPerTurnDefault: 2 });
story.locations.push({ locationId: 'loc-1', title: 'หอสมุด', zone: 'เมือง', areaProfile: { type: 'City', threat: 0, access: 'Public', timeRule: 'Any' },
  description: 'แหล่งบันทึก', triggers: [], loot: [{ id: 'loot-1', itemRefId: 'item-1', chance: 100, amount: 1 }], eventRefs: ['event-1'] });
story.items.push({ id: 'item-1', itemId: 'book-1', name: 'คู่มือ', category: 'KeyItem', rarity: 'Common', properties: { stackable: false },
  description: 'หนังสือความรู้', usage: { useType: 'Instant', cooldown: 0, consumeOnUse: false }, effects: [],
  inspector: { selectedEffectId: null, executionLog: [] }, linkedEvents: ['event-1'], linkedLocations: ['loc-1'] });
story.events.push({ id: 'event-1', eventId: 'evt-1', name: 'พบคู่มือ', eventType: 'Special', targetBoardId: 'board-1', targetX: 1, targetY: 1,
  areaRule: 'ในหอสมุด', trigger: { when: 'OnInteract', condition: 'HP >= 1', priority: 1, cooldown: 0 },
  actions: [{ id: 'a', actionType: 'Message', target: 'Self', payload: 'พบคู่มือ' }],
  outcomes: [{ id: 'o', condition: 'HP >= 1', result: '+HP 1' }], inspector: { selectedActionId: null, executionLog: [] } });
story.modules = [{ id: 'mod-1', name: 'ค้นพบ', type: 'Skill', grade: 'A', description: '', parts: { A: 'PASS', B: '', C: 'DISPLAY: พบคู่มือ' } },
  { id: 'mod-2', name: 'อ่านข้อความ', type: 'Skill', grade: 'A', description: '', parts: { A: 'PASS', B: '', C: 'DISPLAY: อ่านจบ' } }];
story.cards.push({ id: 'card-1', name: 'อ่านคู่มือ', type: 'SKILL', rarity: 'Common', grade: 'C', accessLevel: 'ALL', description: 'การ์ดอ่าน',
  inputCondition: '', logicCode: '', effectResult: '', cost: 0, cooldownTurns: 0, moduleSlots: ['mod-1', 'mod-2'] });
story.commonPlay = [{ id: 'cmd-1', name: 'เพิ่มความรู้', description: 'ตัวอย่างคำสั่งที่ยังไม่รัน', inputKeys: ['character.INT'] }];
story.rulesets.push({ id: 'rule-1', name: 'คู่มือ', modifiers: [], blocks: [
  { id: 'block-1', title: 'อ่านได้', content: 'ตรวจข้อมูลจริง', kind: 'condition', inputKey: 'character.INT', operator: '>', expected: '3', commandRef: 'cmd-1' }
] });

const noChange = () => {};
const props = { story, onChange: noChange };
const pages: [string, React.ReactElement, string][] = [
  ['Home', <DashboardTab {...props} />, 'เมืองทดสอบ'],
  ['Story', <StoryTab {...props} />, 'MEP-1'],
  ['Characters', <CharactersTab {...props} />, 'นักสำรวจ'],
  ['Cards', <CardsTab {...props} />, 'อ่านคู่มือ'],
  ['Board', <BoardTab {...props} />, 'ประเทศไทย'],
  ['Locations', <LocationSheet location={story.locations[0]} onChange={noChange} onDelete={noChange} />, 'หอสมุด'],
  ['Items', <ItemSheet item={story.items[0]} onChange={noChange} onDelete={noChange} />, 'คู่มือ'],
  ['Events', <EventsTab {...props} />, 'พบคู่มือ'],
  ['Rules', <RulesTab {...props} />, 'คู่มือ'],
  ['Common Play', <CommonPlayTab {...props} />, 'เพิ่มความรู้'],
  ['Playtest', <PlaytestTab {...props} />, 'เมืองทดสอบ']
];

for (const [page, element, expected] of pages) {
  const html = renderToString(element);
  assert.ok(html.includes(expected), `${page}: missing ${expected}`);
  console.log(`${page}: rendered sample content`);
}

const cell = getWorldCell(story, 'board-1', 1, 1);
assert.equal(cell?.location?.locationId, 'loc-1');
assert.equal(cell?.events[0]?.id, 'event-1');
assert.equal(story.items.find(item => item.id === story.locations[0].loot[0].itemRefId)?.name, 'คู่มือ');
const context = buildPlayRuleContext(story, { boardId: 'board-1', cellKey: '1_1', characterId: 'char-1' });
assert.equal((context.character as any).INT, 4);
assert.equal(evaluateRuleset(story.rulesets[0], context, story.commonPlay).status, 'UNKNOWN'); // Defined, no executor yet.
assert.equal(runModuleFlow(story.cards[0], story.modules).output, 'อ่านจบ');
assert.equal(runInteraction(story.events[0], story.characters[0].vitals).vitals.hp, 81);
assert.equal(saveStory(story), true);
assert.equal(getStory(story.storyId)?.commonPlay?.[0].id, 'cmd-1');
assert.equal(parseBackup(buildBackup(story))?.story.items[0].id, 'item-1');
const acquired = changeInventory({}, story.items, 'char-1', 'item-1', 1);
assert.equal(acquired.ok, true); assert.equal(acquired.inventory['char-1']['item-1'], 1);
assert.equal(changeInventory(acquired.inventory, story.items, 'char-1', 'missing', 1).ok, false);
assert.equal(changeInventory(acquired.inventory, story.items, 'char-1', 'item-1', 1).ok, false); // Not stackable.
assert.equal(changeInventory({}, story.items, 'char-1', 'item-1', -1).ok, false);
assert.equal(changeInventory(acquired.inventory, story.items, 'char-1', 'item-1', -1).quantity, 0);
const progress = { version: 1 as const, storyId: story.storyId, currentNodeId: null, activeCharacterId: 'char-1', savedAt: Date.now(), inventory: acquired.inventory };
assert.equal(saveRunState(progress), true);
assert.equal(loadRunState(story.storyId)?.inventory?.['char-1']['item-1'], 1);
assert.equal(parseRunState({ ...progress, inventory: { 'char-1': { 'item-1': -2 } } }, story.storyId), null);
assert.equal(parseBackup(buildBackup(story))?.runState?.inventory?.['char-1']['item-1'], 1);
const blank = createEmptyProject('sample-2', 'library', 'ฐานใหม่');
assert.equal(blank.items.length, 0); assert.equal(blank.commonPlay?.length, 0);
console.log('Cross-page links, explicit runtimes, inventory, persistence, backup and isolation: passed');
