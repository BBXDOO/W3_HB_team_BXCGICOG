import type { CardPack, ModulePack } from '../types';

export type FlowStatus = 'DISPLAY' | 'UNKNOWN' | 'ERROR';
export interface FlowReport { status: FlowStatus; trace: string[]; output?: string; reason?: string; }

/** Small, read-only flow runner. Unknown text never becomes executable JavaScript. */
export const runModuleFlow = (card: CardPack, modules: ModulePack[]): FlowReport => {
  const slots = card.moduleSlots;
  const trace: string[] = [];
  if (!slots?.length) return { status: 'UNKNOWN', trace, reason: 'การ์ดยังไม่ประกอบโมดูล' };
  if (![2, 3].includes(slots.length)) return { status: 'ERROR', trace, reason: 'จำนวนช่องต้องเป็น 2 หรือ 3' };
  let output: string | undefined;
  for (let index = 0; index < slots.length; index++) {
    const id = slots[index];
    if (!id) return { status: 'UNKNOWN', trace, reason: `ช่อง ${index + 1} ยังว่าง` };
    const module = modules.find(entry => entry.id === id);
    if (!module) return { status: 'ERROR', trace, reason: `ช่อง ${index + 1} อ้างโมดูลที่ไม่พบ (${id})` };
    let hasInstruction = false;
    for (const part of ['A', 'B', 'C'] as const) {
      const raw = module.parts?.[part]?.trim() || '';
      if (!raw) continue;
      hasInstruction = true;
      const step = `ช่อง ${index + 1} · ${module.name} · ${part}`;
      if (/^PASS$/i.test(raw)) {
        trace.push(`${step}: PASS`);
      } else if (/^DISPLAY\s*:/i.test(raw)) {
        const content = raw.replace(/^DISPLAY\s*:/i, '').trim();
        if (!content) return { status: 'ERROR', trace, reason: `${step}: DISPLAY ไม่มีข้อความ` };
        output = content;
        trace.push(`${step}: DISPLAY → ${content}`);
      } else {
        return { status: 'UNKNOWN', trace, reason: `${step}: ไม่รู้จักลอจิค “${raw.slice(0, 80)}”` };
      }
    }
    if (!hasInstruction) return { status: 'UNKNOWN', trace, reason: `ช่อง ${index + 1} · ${module.name}: ยังไม่มีลอจิค A/B/C` };
  }
  if (!output) return { status: 'UNKNOWN', trace, reason: 'เดินครบแล้ว แต่ไม่มีผลลัพธ์ DISPLAY ให้ใช้' };
  return { status: 'DISPLAY', trace, output };
};
