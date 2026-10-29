import React, { createContext, useContext, useState } from 'react';
import type { StoryPack, TabId } from '../../types';

type Target = { tab: TabId; id: string; label: string };
type Selection = { element: HTMLTextAreaElement; start: number; end: number; value: string; onChange: (value: string) => void; label: string };
type ContentStyle = NonNullable<StoryPack['contentStyle']>;
type ContextValue = { style: ContentStyle; setStyle: (style: ContentStyle) => void; select: (selection: Selection) => void; active: Selection | null; navigate: (tab: TabId, id: string) => void };
const Context = createContext<ContextValue | null>(null);
export const useContentFormat = () => useContext(Context);

const targets = (story: StoryPack): Target[] => [
  ...story.storyNodes.map(node => ({ tab: 'story' as const, id: node.nodeId, label: `เรื่อง · ${node.title || 'ไม่มีชื่อ'}` })),
  ...story.cards.map(card => ({ tab: 'card' as const, id: card.id, label: `การ์ด · ${card.name}` })),
  ...story.rulesets.map(rule => ({ tab: 'rule' as const, id: rule.id, label: `กฎ · ${rule.name}` })),
  ...story.boards.map(board => ({ tab: 'board' as const, id: board.boardId, label: `บอร์ด · ${board.title}` })),
  ...story.locations.map(location => ({ tab: 'location' as const, id: location.locationId, label: `สถานที่ · ${location.title}` })),
  ...story.items.map(item => ({ tab: 'item' as const, id: item.id, label: `ไอเทม · ${item.name}` }))
];

export const ContentFormatProvider: React.FC<{ story: StoryPack; onStyleChange?: (style: ContentStyle) => void; navigate: (tab: TabId, id: string) => void; children: React.ReactNode }> = ({ story, onStyleChange, navigate, children }) => {
  const [active, setActive] = useState<Selection | null>(null);
  return <Context.Provider value={{ select: setActive, active, navigate, style: story.contentStyle || {}, setStyle: style => onStyleChange?.(style) }}>{children}</Context.Provider>;
};

export const FormatPanel: React.FC<{ story: StoryPack; onClose: () => void }> = ({ story, onClose }) => {
  const context = useContentFormat();
  const [scope, setScope] = useState<'project' | 'field'>('project');
  const [size, setSize] = useState(String(story.contentStyle?.fontSize || 12));
  const [color, setColor] = useState(story.contentStyle?.color || '#e7e5df');
  const [target, setTarget] = useState('');
  const choices = targets(story);
  const entry = context?.active?.element.isConnected ? context.active : null;
  const apply = (make: (selected: string) => string) => {
    if (!entry) return;
    const { start, end, value, onChange } = entry;
    // A caret means the whole field; selecting a range remains optional.
    const from = start === end ? 0 : start, to = start === end ? value.length : end;
    const inserted = make(value.slice(from, to));
    const result = value.slice(0, from) + inserted + value.slice(to);
    onChange(result);
    context?.select({ ...entry, value: result, start: from, end: from + inserted.length });
  };
  const applySize = () => {
    if (scope === 'project') context?.setStyle({ ...context.style, fontSize: Number(size) });
    else apply(text => `[size=${size}]${text.replace(/\[size=\d+\]|\[\/size\]/g, '')}[/size]`);
  };
  return <div className="fixed inset-0 z-[9999] bg-black/75 flex items-center justify-center p-4" onClick={onClose}>
    <section role="dialog" aria-modal="true" aria-label="จัดรูปแบบเนื้อหา" className="ps-dialog ps-format-panel" onClick={e => e.stopPropagation()}>
      <div className="flex justify-between items-center"><h2 className="font-bold">ขนาดและรูปแบบตัวหนังสือ</h2><button onClick={onClose} aria-label="ปิด">✕</button></div>
      <div className="ps-format-scopes"><button type="button" aria-pressed={scope === 'project'} onClick={() => setScope('project')}>ทั้งโครงการ</button><button type="button" aria-pressed={scope === 'field'} onClick={() => setScope('field')}>ช่องที่แตะล่าสุด</button></div>
      <p className="text-xs text-[var(--text-dim)]">{scope === 'project' ? 'ปรับเนื้อหาและพรีวิวทุกหน้า ไม่ต้องเลือกหรือครอบข้อความ' : entry ? `ช่อง: ${entry.label} · ไม่ครอบข้อความจะใช้กับทั้งช่อง` : 'แตะช่องเนื้อหาที่รองรับรูปแบบก่อน แล้วเปิดเครื่องมือนี้อีกครั้ง'}</p>
      <label className="flex gap-2 items-center">ขนาด<select aria-label="ขนาดฟอนต์" className="flex-1" value={size} onChange={e => setSize(e.target.value)}>{[10,11,12,14,16,18,20,24,28,32].map(n => <option key={n} value={n}>{n}px</option>)}</select><button type="button" aria-label="ใช้ขนาดตัวหนังสือ" disabled={scope === 'field' && !entry} onClick={applySize}>ใช้ขนาด</button></label>
      <div className="flex items-center gap-2"><input aria-label="สีตัวอักษร" type="color" value={color} onChange={e => setColor(e.target.value)} /><button type="button" disabled={scope === 'field' && !entry} onClick={() => scope === 'project' ? context?.setStyle({ ...context.style, color }) : apply(text => `[color=${color}]${text}[/color]`)}>ใช้สี</button><button type="button" disabled={scope === 'field' && !entry} onClick={() => scope === 'project' ? context?.setStyle({ ...context.style, fontWeight: context.style.fontWeight === 'bold' ? 'normal' : 'bold' }) : apply(text => `**${text}**`)}>ตัวหนา</button></div>
      <div className="ps-format-sample" style={{ fontSize: Number(size), color }}>ตัวอย่าง · Build. Observe. Learn. Continue.</div>
      <button type="button" onClick={() => { context?.setStyle({}); setSize('12'); setColor('#e7e5df'); }}>คืนค่ารูปแบบโครงการ</button>
      <details className="border-t border-[var(--border)] pt-2"><summary>แทรกลิงก์ในช่องข้อความ</summary><select aria-label="ปลายทางลิงก์" value={target} onChange={e => setTarget(e.target.value)} className="w-full mt-2"><option value="">เลือกปลายทาง</option>{choices.map(t => <option key={`${t.tab}:${t.id}`} value={`${t.tab}:${t.id}`}>{t.label}</option>)}</select><button type="button" disabled={!target || !entry} onClick={() => apply(text => `[[${target}|${text || 'เปิดรายการ'}]]`)}>แทรกลิงก์</button></details>
      <p className="text-xs text-[var(--text-dim)]">รูปแบบบันทึกในโครงการและส่งออกพร้อมไฟล์สำรอง</p>
    </section>
  </div>;
};

const tokenPattern = /(\*\*[\s\S]+?\*\*|\[size=(?:10|11|12|14|16|18|20|24|28|32)\][\s\S]+?\[\/size\]|\[color=#[0-9a-fA-F]{6}\][\s\S]+?\[\/color\]|\[\[(?:story|card|rule|board|location|item):[^|\]]+\|[^\]]+\]\])/g;
const renderTokens = (value: string, navigate?: (tab: TabId, id: string) => void, depth = 0): React.ReactNode[] => {
  if (depth > 5) return [value];
  const output: React.ReactNode[] = [];
  let position = 0, match: RegExpExecArray | null;
  const pattern = new RegExp(tokenPattern.source, 'g');
  while ((match = pattern.exec(value))) {
    if (match.index > position) output.push(value.slice(position, match.index));
    const token = match[0], key = match.index;
    if (token.startsWith('**')) output.push(<strong key={key}>{renderTokens(token.slice(2, -2), navigate, depth + 1)}</strong>);
    else if (token.startsWith('[size=')) {
      const close = token.indexOf(']');
      output.push(<span key={key} style={{ fontSize: Number(token.slice(6, close)) }}>{renderTokens(token.slice(close + 1, -7), navigate, depth + 1)}</span>);
    } else if (token.startsWith('[color=')) output.push(<span key={key} style={{ color: token.slice(7, 14) }}>{renderTokens(token.slice(15, -8), navigate, depth + 1)}</span>);
    else {
      const separator = token.indexOf('|'), address = token.slice(2, separator), divider = address.indexOf(':');
      const tab = address.slice(0, divider) as TabId, id = address.slice(divider + 1), label = token.slice(separator + 1, -2);
      output.push(<button key={key} type="button" className="text-sky-300 underline underline-offset-2" onClick={() => navigate?.(tab, id)}>{label}</button>);
    }
    position = match.index + token.length;
  }
  if (position < value.length) output.push(value.slice(position));
  return output;
};

export const RichContent: React.FC<{ value: string; className?: string }> = ({ value, className }) => {
  const context = useContentFormat();
  return <span className={`ps-content ${className || ''}`} style={{ whiteSpace: 'pre-wrap' }}>{renderTokens(value, context?.navigate)}</span>;
};
