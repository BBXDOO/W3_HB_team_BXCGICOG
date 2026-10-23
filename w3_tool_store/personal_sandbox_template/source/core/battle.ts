import type { BattleAction, BattleConfig, BattleEffect, StoryPack } from '../types';
import { evaluateRuleset } from './ruleRuntime';
import type { Vitals } from './eventRuntime';

export interface BattleProgress {
  turn: number;
  phaseIndex: number;
  activeId: string;
  opponentId: string;
  fieldElements: string[];
  mana: Record<string, Record<string, number>>;
  vitals: Record<string, Vitals>;
  log: string[];
  started: boolean;
}
export interface BattleResult { ok: boolean; error?: string; progress?: BattleProgress; hitId?: string; line?: string }
const safe = (value: unknown): value is number => typeof value === 'number' && Number.isSafeInteger(value) && Math.abs(value) <= 99999;
const idSafe = (id: string) => !!id && !['__proto__', 'constructor', 'prototype'].includes(id);
const vitalsFor = (story: StoryPack, progress: BattleProgress, id: string): Vitals | undefined =>
  progress.vitals[id] || story.characters.find(entry => entry.id === id)?.vitals;
const nameFor = (story: StoryPack, id: string) => story.characters.find(entry => entry.id === id)?.name || id;

export const validBattleConfig = (config: BattleConfig): boolean =>
  !!config && Array.isArray(config.elements) && config.elements.every(id => typeof id === 'string' && idSafe(id)) &&
  Array.isArray(config.field?.elements) && config.field.elements.every(id => config.elements.includes(id)) &&
  Array.isArray(config.phases) && config.phases.length > 0 && config.phases.every(p => p && idSafe(p.id) && typeof p.name === 'string') &&
  new Set(config.phases.map(p => p.id)).size === config.phases.length &&
  Array.isArray(config.actions) && config.actions.every(a => a && idSafe(a.id) && typeof a.name === 'string' &&
    ['Attack', 'Def', 'Skill', 'Item'].includes(a.kind) && config.phases.some(p => p.id === a.phaseId) &&
    a.cost && typeof a.cost === 'object' && !Array.isArray(a.cost) &&
    Object.entries(a.cost).every(([element, amount]) => config.elements.includes(element) && safe(amount) && amount >= 0) &&
    Array.isArray(a.effects) && a.effects.every(effect => validateEffect(config, effect))) &&
  new Set(config.actions.map(a => a.id)).size === config.actions.length;

const validateEffect = (config: BattleConfig, effect: BattleEffect): boolean => {
  if (!effect || !['self', 'opponent'].includes((effect as { target?: string }).target || 'self')) return false;
  if (effect.type === 'vital') return ['hp', 'mp', 'en'].includes(effect.stat) && safe(effect.amount) && ['self', 'opponent'].includes(effect.target);
  if (effect.type === 'mana') return config.elements.includes(effect.element) && safe(effect.amount) && ['self', 'opponent'].includes(effect.target);
  if (effect.type === 'field') return config.elements.includes(effect.element) && typeof effect.enabled === 'boolean';
  return false;
};

export const newBattle = (story: StoryPack, config: BattleConfig, activeId: string, opponentId: string, initialVitals: Record<string, Vitals> = {}): BattleResult => {
  if (!validBattleConfig(config) || !config.actions.length) return { ok: false, error: 'กำหนดสนาม ช่วง และแอคชั่นให้ถูกต้องก่อน' };
  if (activeId === opponentId || !story.characters.some(c => c.id === activeId) || !story.characters.some(c => c.id === opponentId))
    return { ok: false, error: 'เลือกผู้ต่อสู้สองตัวที่ต่างกัน' };
  return { ok: true, progress: { turn: 1, phaseIndex: 0, activeId, opponentId, fieldElements: [...config.field.elements],
    mana: { [activeId]: {}, [opponentId]: {} }, vitals: Object.fromEntries([activeId, opponentId].filter(id => initialVitals[id]).map(id => [id, { ...initialVitals[id] }])), log: [], started: false } };
};

/** Begin once per turn. Loading a saved turn never calls this automatically. */
export const beginTurn = (story: StoryPack, config: BattleConfig, current: BattleProgress): BattleResult => {
  if (!validBattleConfig(config) || current.started || !vitalsFor(story, current, current.activeId)) return { ok: false, error: 'เริ่มเทิร์นนี้แล้วหรือข้อมูลผู้เล่นไม่ครบ' };
  const mana = { ...current.mana, [current.activeId]: { ...(current.mana[current.activeId] || {}) } };
  const changes: string[] = [];
  for (const element of current.fieldElements) {
    if (!config.elements.includes(element)) return { ok: false, error: `ธาตุในสนามไม่รู้จัก: ${element}` };
    const before = mana[current.activeId][element] || 0;
    mana[current.activeId][element] = Math.min(10, before + 2);
    changes.push(`${element} ${before}→${mana[current.activeId][element]}`);
  }
  const line = `เทิร์น ${current.turn} · ${nameFor(story, current.activeId)} รับมานาจากสนาม: ${changes.join(', ') || 'ไม่มี'}`;
  return { ok: true, progress: { ...current, mana, started: true, log: [line, ...current.log].slice(0, 30) }, line };
};

/** Validate everything before returning one immutable state transition. */
export const performBattleAction = (story: StoryPack, config: BattleConfig, current: BattleProgress, action: BattleAction): BattleResult => {
  if (!validBattleConfig(config) || !config.actions.some(a => a.id === action.id)) return { ok: false, error: 'ไม่พบแอคชั่นที่กำหนดในโปรเจกต์' };
  if (!action.effects.length || action.effects.some(effect => effect.type !== 'field' && effect.amount === 0))
    return { ok: false, error: 'แอคชั่นนี้ยังไม่กำหนดผลหรือจำนวนที่ใช้จริง' };
  if (!current.started || config.phases[current.phaseIndex]?.id !== action.phaseId) return { ok: false, error: 'แอคชั่นนี้ใช้ไม่ได้ในช่วงปัจจุบัน' };
  if (!vitalsFor(story, current, current.activeId) || !vitalsFor(story, current, current.opponentId)) return { ok: false, error: 'ไม่พบผู้ต่อสู้' };
  if (action.sourceCardId && !story.characters.find(c => c.id === current.activeId)?.abilitySlots.some(slot => slot.equippedCardId === action.sourceCardId))
    return { ok: false, error: 'ตัวละครยังไม่ได้ติดตั้งการ์ดของแอคชั่นนี้' };
  for (const [element, amount] of Object.entries(action.cost)) {
    if ((current.mana[current.activeId]?.[element] || 0) < amount) return { ok: false, error: `มานา ${element} ไม่พอ (ต้องการ ${amount})` };
  }
  if (action.ruleId) {
    const rule = story.rulesets.find(r => r.id === action.ruleId);
    if (!rule) return { ok: false, error: 'ไม่พบ Rules ที่อ้างอิง' };
    const report = evaluateRuleset(rule, { battle: { turn: current.turn, phase: config.phases[current.phaseIndex].id,
      self: { vitals: vitalsFor(story, current, current.activeId), mana: current.mana[current.activeId] || {} },
      opponent: { vitals: vitalsFor(story, current, current.opponentId), mana: current.mana[current.opponentId] || {} },
      field: { elements: current.fieldElements } } }, story.commonPlay || []);
    if (report.status !== 'PASS') return { ok: false, error: `Rules ${report.status}: ${report.trace.find(t => t.status !== 'PASS')?.message || 'ไม่มีเงื่อนไขที่ประเมินได้'}` };
  }
  const mana = Object.fromEntries(Object.entries(current.mana).map(([id, values]) => [id, { ...values }]));
  const vitals = { ...current.vitals };
  let fieldElements = [...current.fieldElements];
  const changes: string[] = [];
  let hitId: string | undefined;
  const actor = current.activeId;
  const target = current.opponentId;
  for (const [element, amount] of Object.entries(action.cost)) {
    const before = mana[actor][element] || 0;
    mana[actor][element] = before - amount;
    if (amount) changes.push(`${nameFor(story, actor)} มานา ${element} ${before}→${mana[actor][element]}`);
  }
  for (const effect of action.effects) {
    const id = effect.type === 'field' ? '' : effect.target === 'self' ? actor : target;
    if (effect.type === 'field') {
      const had = fieldElements.includes(effect.element);
      fieldElements = effect.enabled ? [...new Set([...fieldElements, effect.element])] : fieldElements.filter(e => e !== effect.element);
      changes.push(`สนาม ${effect.element}: ${had ? 'มี' : 'ไม่มี'}→${effect.enabled ? 'มี' : 'ไม่มี'}`);
    } else if (effect.type === 'mana') {
      const before = mana[id]?.[effect.element] || 0;
      mana[id] = { ...(mana[id] || {}), [effect.element]: Math.min(10, Math.max(0, before + effect.amount)) };
      changes.push(`${nameFor(story, id)} มานา ${effect.element} ${before}→${mana[id][effect.element]}`);
      if (before !== mana[id][effect.element]) hitId = id;
    } else {
      const beforeVitals = vitalsFor(story, { ...current, vitals }, id)!;
      const before = beforeVitals[effect.stat];
      vitals[id] = { ...beforeVitals, [effect.stat]: Math.max(0, before + effect.amount) };
      changes.push(`${nameFor(story, id)} ${effect.stat.toUpperCase()} ${before}→${vitals[id][effect.stat]}`);
      if (before !== vitals[id][effect.stat]) hitId = id;
    }
  }
  const line = `เทิร์น ${current.turn} · ${nameFor(story, actor)} ใช้ ${action.name}: ${changes.join(' · ')}`;
  return { ok: true, progress: { ...current, mana, vitals, fieldElements, log: [line, ...current.log].slice(0, 30) }, hitId, line };
};

export const advanceBattle = (story: StoryPack, config: BattleConfig, current: BattleProgress): BattleResult => {
  if (!current.started || !validBattleConfig(config)) return { ok: false, error: 'เริ่มเทิร์นก่อนเดินช่วง' };
  if (current.phaseIndex + 1 < config.phases.length) return { ok: true, progress: { ...current, phaseIndex: current.phaseIndex + 1 } };
  const line = `จบเทิร์น ${current.turn} · ต่อไป ${nameFor(story, current.opponentId)}`;
  return { ok: true, progress: { ...current, turn: current.turn + 1, phaseIndex: 0, activeId: current.opponentId,
    opponentId: current.activeId, started: false, log: [line, ...current.log].slice(0, 30) }, line };
};

export const parseBattleProgress = (raw: unknown): BattleProgress | null => {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return null;
  const p = raw as BattleProgress;
  if (!Number.isSafeInteger(p.turn) || p.turn < 1 || !Number.isSafeInteger(p.phaseIndex) || p.phaseIndex < 0 ||
      !idSafe(p.activeId) || !idSafe(p.opponentId) || p.activeId === p.opponentId || typeof p.started !== 'boolean' ||
      !Array.isArray(p.fieldElements) || !p.fieldElements.every(idSafe) || !Array.isArray(p.log) || !p.log.every(line => typeof line === 'string') ||
      !p.mana || typeof p.mana !== 'object' || Array.isArray(p.mana) || !p.vitals || typeof p.vitals !== 'object' || Array.isArray(p.vitals)) return null;
  if (!Object.entries(p.mana).every(([id, amounts]) => idSafe(id) && amounts && typeof amounts === 'object' && !Array.isArray(amounts) &&
    Object.entries(amounts).every(([element, amount]) => idSafe(element) && safe(amount) && amount >= 0 && amount <= 10))) return null;
  if (!Object.entries(p.vitals).every(([id, values]) => idSafe(id) && values && ['hp', 'mp', 'en'].every(key => safe(values[key as keyof Vitals]) && values[key as keyof Vitals] >= 0))) return null;
  return p;
};
