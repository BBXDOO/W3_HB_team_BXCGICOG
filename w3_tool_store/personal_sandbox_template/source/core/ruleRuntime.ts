import type { CommonPlayCommand, RuleBlock, RulesetPack } from '../types';

export type RuleStatus = 'PASS' | 'FAIL' | 'UNKNOWN' | 'ERROR';
export interface RuleTrace { path: string; title: string; status: RuleStatus; message: string; commandRef?: string }
export interface RuleReport { status: RuleStatus; trace: RuleTrace[] }
export type RuleContext = Record<string, unknown>;

const lookup = (context: RuleContext, key: string): { found: boolean; value?: unknown } => {
  if (!key || key.split('.').some(part => !part || part === '__proto__' || part === 'constructor' || part === 'prototype')) return { found: false };
  let value: unknown = context;
  for (const part of key.split('.')) {
    if (value === null || typeof value !== 'object' || Array.isArray(value) || !Object.prototype.hasOwnProperty.call(value, part)) return { found: false };
    value = (value as Record<string, unknown>)[part];
  }
  return { found: true, value };
};

/** Evaluates declared inputs only. Never interprets prose or executes command references. */
export const evaluateRuleset = (ruleset: RulesetPack, context: RuleContext, commands: CommonPlayCommand[] = []): RuleReport => {
  const trace: RuleTrace[] = [];
  const visit = (blocks: RuleBlock[], prefix = '') => blocks.forEach((block, index) => {
    const path = `${prefix}${index + 1}`;
    if (block.kind === 'condition') {
      const key = block.inputKey?.trim() || '';
      const op = block.operator;
      const found = lookup(context, key);
      let status: RuleStatus = 'UNKNOWN', message = '';
      if (!key || !op || !['exists','==','!=','>','>=','<','<='].includes(op)) { status = 'ERROR'; message = 'ยังไม่กำหนด input หรือการเปรียบเทียบที่รองรับ'; }
      else if (!found.found) message = `ไม่พบ input: ${key}`;
      else if (op === 'exists') { status = 'PASS'; message = `พบ ${key}`; }
      else {
        const actual = found.value;
        const expected = block.expected ?? '';
        if (typeof actual !== 'string' && typeof actual !== 'number' && typeof actual !== 'boolean') {
          status = 'UNKNOWN'; message = `${key} ไม่ใช่ค่าพื้นฐานที่เปรียบเทียบได้`;
        } else if (['>', '>=', '<', '<='].includes(op) && (typeof actual !== 'number' || !Number.isFinite(actual) || !Number.isFinite(Number(expected)) || !expected.trim())) {
          status = 'ERROR'; message = 'การเปรียบเทียบลำดับต้องใช้ตัวเลข';
        } else {
          const target: string | number | boolean = typeof actual === 'number' ? Number(expected) : typeof actual === 'boolean' ? expected === 'true' : expected;
          if (typeof actual === 'boolean' && expected !== 'true' && expected !== 'false') { status = 'ERROR'; message = 'ค่า boolean ต้องเป็น true หรือ false'; }
          else {
            const passed = op === '==' ? actual === target : op === '!=' ? actual !== target : op === '>' ? (actual as number) > (target as number) : op === '>=' ? (actual as number) >= (target as number) : op === '<' ? (actual as number) < (target as number) : (actual as number) <= (target as number);
            status = passed ? 'PASS' : 'FAIL'; message = `${key} ${op} ${expected}: ${passed ? 'ผ่าน' : 'ไม่ผ่าน'}`;
          }
        }
      }
      const commandRef = status === 'PASS' ? block.commandRef?.trim() || undefined : undefined;
      if (commandRef) {
        const command = commands.find(entry => entry.id === commandRef);
        if (!command) { status = 'ERROR'; message += ` · ไม่พบคำสั่ง ID ${commandRef}`; }
        else {
          const missing = (command.inputKeys || []).filter(input => !lookup(context, input).found);
          status = 'UNKNOWN';
          message += missing.length ? ` · คำสั่ง ${command.name} ขาด input: ${missing.join(', ')}` : ` · พบคำสั่ง ${command.name} แต่ยังไม่มีตัวประมวลผล`;
        }
      }
      trace.push({ path, title: block.title, status, message, commandRef });
    }
    visit(block.children || [], `${path}.`);
  });
  visit(ruleset.blocks);
  const conditions = trace.map(entry => entry.status);
  return { status: conditions.includes('ERROR') ? 'ERROR' : conditions.includes('UNKNOWN') ? 'UNKNOWN' : conditions.includes('FAIL') ? 'FAIL' : conditions.length ? 'PASS' : 'UNKNOWN', trace };
};
