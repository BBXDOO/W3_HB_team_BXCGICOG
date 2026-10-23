import type { EventPack } from '../types';

export type Vitals = { hp: number; mp: number; en: number };
type Stat = keyof Vitals;
export interface EventResult { ok: boolean; vitals: Vitals; log: string[]; error?: string; }

const evaluate = (expression: string, vitals: Vitals): boolean | null => {
  if (!expression.trim()) return true;
  const match = expression.trim().match(/^(HP|MP|EN)\s*(>=|<=|==|>|<)\s*(-?\d+)$/i);
  if (!match) return null;
  const value = vitals[match[1].toLowerCase() as Stat], target = Number(match[3]);
  switch (match[2]) {
    case '>': return value > target;
    case '<': return value < target;
    case '>=': return value >= target;
    case '<=': return value <= target;
    default: return value === target;
  }
};

/** Only explicit OnInteract, Message/Self, and +/- HP/MP/EN are executable. */
export const runInteraction = (event: EventPack, current: Vitals): EventResult => {
  const original = { ...current };
  const fail = (error: string): EventResult => ({ ok: false, vitals: original, log: [], error });
  if (event.trigger.when !== 'OnInteract') return fail(`Trigger ${event.trigger.when} ยังไม่รองรับการกดใช้งาน`);
  if (event.trigger.cooldown > 0) return fail('Cooldown ยังไม่รองรับในโหมดนี้');
  const allowed = evaluate(event.trigger.condition, original);
  if (allowed === null) return fail('รูปแบบเงื่อนไข Trigger ไม่รองรับ');
  if (!allowed) return fail('เงื่อนไข Trigger ไม่ผ่าน');

  const next = { ...original }, log: string[] = [];
  for (const action of event.actions) {
    if (action.actionType.toLowerCase() !== 'message' || action.target.toLowerCase() !== 'self')
      return fail(`คำสั่ง ${action.actionType}/${action.target} ยังไม่รองรับ`);
    log.push(action.payload || event.name);
  }
  for (const outcome of event.outcomes) {
    const passed = evaluate(outcome.condition, next);
    if (passed === null) return fail('รูปแบบเงื่อนไข Outcome ไม่รองรับ');
    if (!passed) continue;
    const match = outcome.result.trim().match(/^([+-])(HP|MP|EN)\s+(\d+)$/i);
    if (!match) return fail(`ผลลัพธ์ ${outcome.result || '(ว่าง)'} ยังไม่รองรับ`);
    const stat = match[2].toLowerCase() as Stat;
    next[stat] = Math.max(0, next[stat] + (match[1] === '+' ? 1 : -1) * Number(match[3]));
    log.push(`${match[1]}${match[2].toUpperCase()} ${match[3]} → ${next[stat]}`);
  }
  return { ok: true, vitals: next, log: log.length ? log : [`${event.name}: ไม่มีผลลัพธ์ที่เข้าเงื่อนไข`] };
};
