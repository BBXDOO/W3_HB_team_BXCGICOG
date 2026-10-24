import React, { createContext, useContext, useState } from 'react';
import type { StoryPack, TabId } from '../../types';

type Target = { tab: TabId; id: string; label: string };
type Selection = { element: HTMLTextAreaElement; start: number; end: number; value: string; onChange: (value: string) => void; label: string };
type ContextValue = { select: (selection: Selection) => void; active: Selection | null; navigate: (tab: TabId, id: string) => void };
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

export const ContentFormatProvider: React.FC<{ story: StoryPack; navigate: (tab: TabId, id: string) => void; children: React.ReactNode }> = ({ story, navigate, children }) => {
  const [active, setActive] = useState<Selection | null>(null);
  return <Context.Provider value={{ select: setActive, active, navigate }}>{children}</Context.Provider>;
};

export const FormatPanel: React.FC<{ story: StoryPack; onClose: () => void }> = ({ story, onClose }) => {
  const context = useContentFormat();
  const [size, setSize] = useState('18');
  const [color, setColor] = useState('#65ad8d');
  const [target, setTarget] = useState('');
  const choices = targets(story);
  const apply = (make: (selected: string) => string) => {
    const entry = context?.active;
    if (!entry || !entry.element.isConnected) return;
    const { element, start, end, value, onChange } = entry;
    const inserted = make(value.slice(start, end) || 'ข้อความ');
    const result = value.slice(0, start) + inserted + value.slice(end);
    onChange(result);
    context.select({ ...entry, value: result, start: start + inserted.length, end: start + inserted.length });
    requestAnimationFrame(() => { element.focus(); element.setSelectionRange(start + inserted.length, start + inserted.length); });
  };
  return <div className="fixed inset-0 z-[9999] bg-black/75 flex items-center justify-center p-4" onClick={onClose}>
    <section role="dialog" aria-modal="true" aria-label="จัดรูปแบบเนื้อหา" className="w-full max-w-md max-h-[85vh] overflow-y-auto rounded-2xl border border-emerald-500/40 bg-[#18231c] p-4 text-white space-y-4" onClick={event => event.stopPropagation()}>
      <div className="flex justify-between items-center"><h2 className="font-bold text-emerald-200">จัดรูปแบบเนื้อหา</h2><button onClick={onClose} aria-label="ปิด">✕</button></div>
      <p className="text-xs text-slate-300">{context?.active?.element.isConnected ? `ช่องที่เลือก: ${context.active.label} · เลือกข้อความในช่องก่อนกดเครื่องมือ` : 'แตะช่องเนื้อหาที่ต้องการก่อน แล้วกลับมากดปุ่มหุ่นยนต์'}</p>
      <div className="grid grid-cols-2 gap-2"><button disabled={!context?.active?.element.isConnected} className="rounded-lg border border-white/20 p-3 disabled:opacity-40" onClick={() => apply(text => `**${text}**`)}><b>ตัวหนา</b></button>
        <div className="flex gap-1"><select aria-label="ขนาดฟอนต์" className="min-w-0 flex-1 rounded-lg bg-[#0c1512]" value={size} onChange={event => setSize(event.target.value)}>{[12,14,16,18,20,24,28,32].map(n => <option key={n} value={n}>{n}px</option>)}</select><button disabled={!context?.active?.element.isConnected} className="rounded-lg border border-white/20 px-2 disabled:opacity-40" onClick={() => apply(text => `[size=${size}]${text}[/size]`)}>ใช้</button></div>
        <div className="flex gap-1"><input aria-label="สีตัวอักษร" type="color" className="h-11 w-14" value={color} onChange={event => setColor(event.target.value)} /><button disabled={!context?.active?.element.isConnected} className="flex-1 rounded-lg border border-white/20 disabled:opacity-40" onClick={() => apply(text => `[color=${color}]${text}[/color]`)}>ใช้สี</button></div></div>
      <div className="border-t border-white/10 pt-3 space-y-2"><label className="text-xs">ลิงก์ไปยังรายการในโครงการนี้</label><select value={target} onChange={event => setTarget(event.target.value)} className="w-full rounded-lg bg-[#0c1512] p-3 text-sm"><option value="">เลือกปลายทาง</option>{choices.map(entry => <option key={`${entry.tab}:${entry.id}`} value={`${entry.tab}:${entry.id}`}>{entry.label}</option>)}</select>
        <button disabled={!target || !context?.active?.element.isConnected} className="w-full rounded-lg bg-emerald-700 p-3 text-sm disabled:opacity-40" onClick={() => apply(text => `[[${target}|${text}]]`)}>แทรกลิงก์</button></div>
      <p className="text-xs text-slate-400">รูปแบบจะอยู่ในไฟล์สำรองโครงการด้วย ลิงก์จะใช้ได้ตราบที่รายการปลายทางยังอยู่</p>
    </section>
  </div>;
};

const tokenPattern = /(\*\*[\s\S]+?\*\*|\[size=(?:12|14|16|18|20|24|28|32)\][\s\S]+?\[\/size\]|\[color=#[0-9a-fA-F]{6}\][\s\S]+?\[\/color\]|\[\[(?:story|card|rule|board|location|item):[^|\]]+\|[^\]]+\]\])/g;
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
  return <span className={className} style={{ whiteSpace: 'pre-wrap' }}>{renderTokens(value, context?.navigate)}</span>;
};
