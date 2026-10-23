import React, { useState } from 'react';
import type { CommonPlayCommand, StoryPack } from '../../types';
import { generateId } from '../../core/utils';
import { SplitLayout60_40 } from '../../ui/layout/SplitLayout60_40';
import { MonitorCore } from '../../ui/components/MonitorCore';
import { Button } from '../../ui/components/Button';
import { Input, TextArea } from '../../ui/components/Input';

interface Props { story: StoryPack; onChange: (story: StoryPack) => void }

export const CommonPlayTab: React.FC<Props> = ({ story, onChange }) => {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const commands = story.commonPlay || [];
  const selected = commands.find(entry => entry.id === selectedId) || commands[0];
  const update = (command: CommonPlayCommand) => onChange({ ...story, commonPlay: commands.map(entry => entry.id === command.id ? command : entry) });
  const add = () => {
    const command = { id: generateId('cmd'), name: 'คำสั่งใหม่', description: '', inputKeys: [] };
    onChange({ ...story, commonPlay: [...commands, command] }); setSelectedId(command.id);
  };
  return <SplitLayout60_40
    topLeft={<div className="h-full p-3 flex flex-col gap-3 bg-[var(--surface-2)]"><Button variant="accent" onClick={add}>+ เพิ่มรายการคำสั่ง</Button>
      <div className="overflow-y-auto space-y-2">{commands.map(entry => <button key={entry.id} className={`w-full text-left rounded-lg p-3 ${selected?.id === entry.id ? 'bg-emerald-800/50' : 'bg-white/5'}`} onClick={() => setSelectedId(entry.id)}>{entry.name}</button>)}</div></div>}
    topRight={<div className="h-full overflow-y-auto p-4 md:p-6 text-slate-100 space-y-4"><h2 className="text-emerald-300 font-bold">COMMON PLAY</h2>
      <p className="text-sm text-slate-300">ทะเบียนคำสั่งของโครงการนี้ ID ใช้อ้างอิงจาก Rules ได้ ชื่อและคำอธิบายปรับเองได้ ยังไม่รันคำสั่งหรือเปลี่ยนข้อมูล</p>
      {selected ? <><p className="text-xs break-all">ID: <code>{selected.id}</code></p>
        <Input label="ชื่อแสดง" value={selected.name} onChange={name => update({ ...selected, name })} />
        <TextArea label="คำอธิบาย/แนวทาง (ยังไม่รัน)" value={selected.description} onChange={description => update({ ...selected, description })} />
        <label className="block text-sm">ชื่อ input ที่ต้องมี คั่นด้วยจุลภาค<input key={selected.id} aria-label="ชื่อ input ที่ต้องมี" className="block w-full mt-1 bg-[#0b1512] rounded p-2" defaultValue={selected.inputKeys.join(', ')} onBlur={e => { const inputKeys = e.target.value.split(',').map(key => key.trim()).filter(Boolean); if (inputKeys.join(',') !== selected.inputKeys.join(',')) update({ ...selected, inputKeys }); }} /></label>
        <Button variant="danger" onClick={() => { if (confirm('ลบรายการคำสั่งนี้? กฎที่อ้าง ID นี้จะหาปลายทางไม่พบ')) { onChange({ ...story, commonPlay: commands.filter(entry => entry.id !== selected.id) }); setSelectedId(null); } }}>ลบรายการ</Button>
      </> : <p>ยังไม่มีรายการคำสั่ง</p>}</div>}
    bottomMain={<MonitorCore title="Common Play Registry" isEmpty={!selected}>{selected && <div className="p-5 text-slate-100"><b>{selected.name}</b><p className="text-xs break-all text-emerald-300">{selected.id}</p><p className="whitespace-pre-wrap mt-3">{selected.description}</p><p className="text-xs mt-3">INPUT: {selected.inputKeys.join(', ') || 'ยังไม่ระบุ'}</p><p className="text-amber-300 text-xs mt-3">สถานะ: นิยามไว้ · ยังไม่มีตัวประมวลผล</p></div>}</MonitorCore>}
  />;
};
