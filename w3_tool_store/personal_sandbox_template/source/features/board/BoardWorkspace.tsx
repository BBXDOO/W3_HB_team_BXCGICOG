import React, { useState } from 'react';
import type { BoardPack, CellPack } from '../../types';

type ViewMode = NonNullable<BoardPack['viewMode']>;
type RecordCell = { key: string; cell: CellPack };

interface Props {
  board: BoardPack;
  selectedKey: string | null;
  zoom: number;
  onZoom: (value: number) => void;
  onSelect: (key: string) => void;
  onMode: (mode: ViewMode) => void;
  onAdd: (parentKey?: string) => void;
  onUpdate: (key: string, patch: Partial<CellPack>) => void;
  onDelete: (key: string) => void;
}

const modes: { id: ViewMode; label: string }[] = [
  { id: 'overview', label: '▦ ภาพรวม' },
  { id: 'grid', label: '▦ ตารางพิกัด' },
  { id: 'database', label: '▤ ฐานข้อมูล' },
  { id: 'mindmap', label: '◇ มายด์แมพ' }
];

const palette = ['#16a34a', '#0f9f74', '#306bd1', '#a64a9f', '#be7440', '#397d8f'];
const panel = 'rounded-xl border border-[var(--border)] bg-[var(--surface)] p-3';
const field = 'w-full rounded-lg border border-[var(--border)] bg-[var(--surface-2)] px-2 py-2 text-sm text-[var(--text)]';
const action = 'rounded-lg border border-[var(--accent)]/40 px-3 py-2 text-xs text-[var(--text)]';
const cellName = (entry: RecordCell) => entry.cell.name?.trim() || `พิกัด ${entry.cell.x}, ${entry.cell.y}`;

export const BoardWorkspace: React.FC<Props> = ({ board, selectedKey, zoom, onZoom, onSelect, onMode, onAdd, onUpdate, onDelete }) => {
  const [query, setQuery] = useState('');
  const [sortBy, setSortBy] = useState<'coordinate' | 'name'>('coordinate');
  const mode = board.viewMode || 'overview';
  const records: RecordCell[] = (Object.entries(board.cellMap) as [string, CellPack][])
    .filter(([, cell]) => cell.name || cell.desc || cell.markerColor || cell.markerIcon || (cell.type && cell.type !== 'Empty'))
    .map(([key, cell]) => ({ key, cell }))
    .filter(({ cell }) => cell.x < board.width && cell.y < board.height)
    .sort((a, b) => a.cell.y - b.cell.y || a.cell.x - b.cell.x);
  const selected = selectedKey ? records.find(entry => entry.key === selectedKey) : undefined;
  const filtered = records.filter(entry => `${cellName(entry)} ${entry.cell.desc || ''}`.toLowerCase().includes(query.toLowerCase()))
    .sort((a, b) => sortBy === 'name' ? cellName(a).localeCompare(cellName(b), 'th') : a.cell.y - b.cell.y || a.cell.x - b.cell.x);
  const types = ['Location', 'Encounter', 'SafeZone', 'Empty'] as const;
  const typeCounts = types.map(type => ({ type, count: records.filter(entry => (entry.cell.type || 'Empty') === type).length }));
  const roots = records.filter(entry => !entry.cell.parentKey || !records.some(other => other.key === entry.cell.parentKey));
  const descendantOf = (key: string, possibleParent: string): boolean => {
    const visited = new Set<string>();
    let cursor: string | undefined = possibleParent;
    while (cursor && !visited.has(cursor)) {
      if (cursor === key) return true;
      visited.add(cursor);
      cursor = records.find(entry => entry.key === cursor)?.cell.parentKey;
    }
    return false;
  };
  const renderNode = (entry: RecordCell, ancestors: Set<string>): React.ReactNode => {
    if (ancestors.has(entry.key)) return null;
    const next = new Set(ancestors).add(entry.key);
    return <div key={entry.key} className="border-l border-emerald-500/30 pl-3 mt-2">
      <button type="button" onClick={() => onSelect(entry.key)} className={`w-full text-left rounded-lg border p-2 text-xs ${selectedKey === entry.key ? 'border-[var(--accent)] bg-[var(--accent)]/15' : 'border-white/10 bg-white/5'}`}>
        <span className="mr-2">{entry.cell.markerIcon || '◇'}</span>{cellName(entry)}
      </button>
      {records.filter(child => child.cell.parentKey === entry.key).map(child => renderNode(child, next))}
    </div>;
  };

  return <div className="board-workspace h-full min-h-[260px] flex flex-col gap-2 text-white" aria-label="พื้นที่ข้อมูลบอร์ด">
    <div className="flex items-center gap-1 overflow-x-auto shrink-0 pb-1" aria-label="รูปแบบการแสดงข้อมูล">
      {modes.map(option => <button key={option.id} type="button" onClick={() => onMode(option.id)} aria-pressed={mode === option.id}
        className={`shrink-0 rounded-lg px-3 py-2 text-xs ${mode === option.id ? 'bg-[var(--accent)] text-[#0b0912] font-bold' : 'bg-white/5 text-slate-300'}`}>{option.label}</button>)}
    </div>
    <div className="board-workspace-columns flex-1 min-h-0 grid gap-2" style={{ gridTemplateColumns: 'minmax(0, 1.15fr) minmax(0, .85fr)' }}>
      <section className={`${panel} min-w-0 min-h-0 flex flex-col overflow-hidden`} aria-label="ภาพรวมข้อมูล">
        <div className="flex items-center justify-between gap-2 pb-2 text-xs"><strong>{mode === 'overview' ? 'ภาพรวมพื้นที่' : mode === 'grid' ? 'ตารางพิกัด' : mode === 'database' ? 'รายการข้อมูล' : 'ความสัมพันธ์'}</strong><span className="text-emerald-300">{records.length} รายการ</span></div>
        {mode === 'database' && <div className="flex gap-1 mb-2"><input className={`${field} min-w-0`} type="search" placeholder="ค้นหาข้อมูล" value={query} onChange={event => setQuery(event.target.value)} /><select aria-label="เรียงรายการ" className={`${field} w-24 shrink-0`} value={sortBy} onChange={event => setSortBy(event.target.value as 'coordinate' | 'name')}><option value="coordinate">พิกัด</option><option value="name">ชื่อ</option></select></div>}
        <div className="flex-1 min-h-0 overflow-auto rounded-lg bg-[#0a1114] p-2 scroll-container">
          {mode === 'grid' && <div className="grid w-max" style={{ gridTemplateColumns: `repeat(${board.width}, ${zoom}px)`, gap: 1 }}>
            {Array.from({ length: board.width * board.height }, (_, index) => {
              const x = index % board.width, y = Math.floor(index / board.width), key = `${x}_${y}`;
              const cell = board.cellMap[key];
              return <button key={key} type="button" title={cell?.name || `พิกัด ${x}, ${y}`} onClick={() => onSelect(key)}
                className={`border border-white/10 flex items-center justify-center ${selectedKey === key ? 'ring-2 ring-white' : ''}`}
                style={{ width: zoom, height: zoom, background: cell?.markerColor || '#142334', fontSize: zoom * .5 }}>{cell?.markerIcon || ''}</button>;
            })}
          </div>}
          {mode === 'overview' && (records.length ? <div className="grid grid-cols-3 auto-rows-[68px] gap-1">
            {records.map((entry, index) => <button key={entry.key} type="button" onClick={() => onSelect(entry.key)}
              className={`min-w-0 rounded-md p-2 text-left text-xs flex flex-col justify-between ${selectedKey === entry.key ? 'ring-2 ring-white' : ''}`}
              style={{ gridColumn: index % 5 === 0 ? 'span 2' : undefined, background: entry.cell.markerColor || palette[index % palette.length] }}>
              <span className="truncate font-bold">{entry.cell.markerIcon} {cellName(entry)}</span><small className="opacity-80">{entry.cell.x}, {entry.cell.y}</small>
            </button>)}</div> : <div className="h-full flex flex-col items-center justify-center gap-3 text-center text-xs text-slate-300">ยังไม่มีข้อมูลในพื้นที่นี้<button className={action} onClick={() => onAdd()}>+ เพิ่มรายการแรก</button></div>)}
          {mode === 'database' && (filtered.length ? filtered.map(entry => <button key={entry.key} type="button" onClick={() => onSelect(entry.key)}
            className={`w-full flex justify-between gap-2 border-b border-white/10 px-2 py-3 text-left text-xs ${selectedKey === entry.key ? 'bg-emerald-900/40' : ''}`}><span className="truncate">{entry.cell.markerIcon} {cellName(entry)}</span><span className="text-slate-400 shrink-0">{entry.cell.x},{entry.cell.y}</span></button>) : <p className="p-3 text-xs text-slate-400">ไม่พบรายการ</p>)}
          {mode === 'mindmap' && (records.length ? roots.map(entry => renderNode(entry, new Set())) : <p className="p-3 text-xs text-slate-400">เพิ่มหัวข้อเพื่อเริ่มมายด์แมพ</p>)}
        </div>
        {mode === 'grid' && <label className="flex items-center gap-2 text-xs pt-2">ขนาดช่อง <input type="range" min="24" max="100" value={zoom} onChange={event => onZoom(Number(event.target.value))} className="min-w-0 flex-1 accent-emerald-500" />{zoom}px</label>}
      </section>
      <aside className={`${panel} min-w-0 min-h-0 overflow-y-auto scroll-container space-y-3 text-xs`} aria-label="รายละเอียดและเครื่องมือ">
        <div><strong className="text-emerald-200">{selected ? cellName(selected) : selectedKey ? `พิกัด ${selectedKey.replace('_', ', ')}` : 'เครื่องมือ'}</strong><p className="text-slate-400 mt-1">{mode === 'mindmap' ? 'จัดหัวข้อและความเชื่อมโยง' : mode === 'database' ? 'ค้นหาและแก้ข้อมูล' : 'เลือกช่องหรือรายการเพื่อดูรายละเอียด'}</p></div>
        <button className={`${action} w-full`} onClick={() => onAdd(mode === 'mindmap' ? selectedKey || undefined : undefined)}>+ {mode === 'mindmap' && selectedKey ? 'เพิ่มหัวข้อย่อย' : 'เพิ่มรายการ'}</button>
        {mode === 'overview' && <div className="grid grid-cols-2 gap-1" aria-label="สรุปข้อมูล"><div className="rounded-lg bg-emerald-950/60 p-2"><span className="text-slate-400">รายการ</span><strong className="block text-lg">{records.length}</strong></div><div className="rounded-lg bg-emerald-950/60 p-2"><span className="text-slate-400">ช่องทั้งหมด</span><strong className="block text-lg">{board.width * board.height}</strong></div></div>}
        {mode === 'overview' && <div className="space-y-1" aria-label="ประเภทข้อมูล">{typeCounts.filter(item => item.count).map(item => <div key={item.type} className="flex items-center gap-2"><span className="w-16 truncate text-slate-300">{item.type}</span><div className="h-2 flex-1 rounded bg-white/10"><div className="h-full rounded bg-emerald-500" style={{ width: `${item.count / Math.max(records.length, 1) * 100}%` }} /></div><span>{item.count}</span></div>)}</div>}
        {mode === 'database' && <p className="text-slate-400">แสดง {filtered.length} จาก {records.length} รายการ · ค้นหาและเรียงจากแผงซ้าย</p>}
        {mode === 'mindmap' && <p className="text-slate-400">หัวข้อหลัก {roots.length} · แตะหัวข้อแล้วเพิ่มหัวข้อย่อยหรือเปลี่ยนหัวข้อแม่</p>}
        {mode === 'grid' && <p className="text-slate-400">แตะช่องในตารางเพื่อกำหนดชนิด สี และไอคอนในส่วนแก้ไขด้านบน</p>}
        {selectedKey && <>
          <label className="block">ชื่อ<input className={`${field} mt-1`} value={selected?.cell.name || ''} onChange={event => onUpdate(selectedKey, { name: event.target.value })} placeholder="ตั้งชื่อรายการ" /></label>
          <label className="block">รายละเอียด<textarea className={`${field} mt-1 min-h-20 resize-y`} value={selected?.cell.desc || ''} onChange={event => onUpdate(selectedKey, { desc: event.target.value })} placeholder="บันทึกข้อมูล" /></label>
          {mode === 'mindmap' && <label className="block">เชื่อมจากหัวข้อแม่<select className={`${field} mt-1`} value={selected?.cell.parentKey || ''} onChange={event => onUpdate(selectedKey, { parentKey: event.target.value || undefined })}>
            <option value="">หัวข้อหลัก</option>{records.filter(entry => entry.key !== selectedKey && !descendantOf(selectedKey, entry.key)).map(entry => <option key={entry.key} value={entry.key}>{cellName(entry)}</option>)}
          </select></label>}
          <button className="text-rose-300 border border-rose-400/30 rounded-lg px-3 py-2" onClick={() => { if (window.confirm('ลบข้อมูลในช่องนี้?')) onDelete(selectedKey); }}>ลบรายการนี้</button>
        </>}
        <div className="border-t border-white/10 pt-2 text-slate-400">พื้นที่ {board.width} × {board.height} ช่อง<br />ข้อมูล {records.length} รายการ<br />เลือกโหมดด้านบนเพื่อเปลี่ยนวิธีดูข้อมูล</div>
      </aside>
    </div>
  </div>;
};
