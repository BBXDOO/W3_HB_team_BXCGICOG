import React, { useState } from 'react';
import type { StoryPack, TabId } from '../../types';
import guide from '../../docs/คู่มือใช้งานภาษาไทย.md?raw';

interface Props {
  story: StoryPack;
  activeTab: TabId;
  onAdd: () => void;
  onSave: () => boolean;
  onExport: () => void;
  onClose: () => void;
}

export const AppCommands: React.FC<Props> = ({ story, activeTab, onAdd, onSave, onExport, onClose }) => {
  const [tab, setTab] = useState<'commands' | 'manual'>('commands');
  const [result, setResult] = useState('');
  const [command, setCommand] = useState('summary');
  const count = story.storyNodes.length + story.cards.length + story.characters.length + story.boards.length + story.locations.length + story.items.length + story.events.length + story.rulesets.length;
  const run = () => {
    if (command === 'summary') setResult(`โครงการ: ${story.title}\nเรื่อง ${story.storyNodes.length} · การ์ด ${story.cards.length} · ตัวละคร ${story.characters.length}\nบอร์ด ${story.boards.length} · สถานที่ ${story.locations.length} · ไอเทม ${story.items.length}\nอีเวนต์ ${story.events.length} · ชุดกฎ ${story.rulesets.length}\nรวม ${count} รายการ`);
    else if (command === 'add') {
      if (!['story', 'card', 'character', 'board', 'location', 'item', 'event', 'rule'].includes(activeTab)) return setResult('หน้านี้ยังไม่มีคำสั่งเพิ่มรายการ');
      onAdd(); setResult(`ส่งคำสั่งเพิ่มรายการในหน้า ${activeTab} แล้ว ตรวจรายการในหน้านั้นเพื่อดูผล`);
    } else if (command === 'save') setResult(onSave() ? 'บันทึกโครงการลงเครื่องสำเร็จ' : 'บันทึกไม่สำเร็จ กรุณาส่งออกสำเนาหรือตรวจพื้นที่เก็บข้อมูล');
    else if (command === 'export') { onExport(); setResult('เปิดหน้าบันทึกไฟล์ JSON แล้ว การส่งออกจะเสร็จเมื่อเลือกตำแหน่งและยืนยันบันทึก'); }
  };
  return <div className="fixed inset-0 z-[9999] bg-black/75 flex items-center justify-center p-4" onClick={onClose}>
    <section role="dialog" aria-modal="true" aria-label="คำสั่งและคู่มือแอป" className="w-full max-w-xl max-h-[85vh] flex flex-col rounded-2xl border border-emerald-500/40 bg-[var(--surface)] text-white shadow-2xl" onClick={event => event.stopPropagation()}>
      <div className="flex items-center justify-between border-b border-white/10 p-4"><h2 className="font-bold text-emerald-200">คำสั่งและคู่มือ Sandbox</h2><button aria-label="ปิด" onClick={onClose}>✕</button></div>
      <div className="flex gap-2 p-3 border-b border-white/10"><button className={`rounded-lg px-4 py-2 text-sm ${tab === 'commands' ? 'bg-emerald-700' : 'bg-white/10'}`} onClick={() => setTab('commands')}>คำสั่ง</button><button className={`rounded-lg px-4 py-2 text-sm ${tab === 'manual' ? 'bg-emerald-700' : 'bg-white/10'}`} onClick={() => setTab('manual')}>คู่มือ</button></div>
      {tab === 'manual' ? <div className="overflow-y-auto p-4 whitespace-pre-wrap text-sm leading-7">{guide}</div> : <div className="overflow-y-auto p-4 space-y-4 text-sm">
        <p className="text-slate-300">เลือกงานที่แอปรองรับและดูผลด้านล่าง คำสั่งเหล่านี้ทำงานกับโครงการที่เปิดอยู่</p>
        <label className="block">เลือกคำสั่ง<select className="mt-2 w-full rounded-lg border border-white/15 bg-[var(--surface-2)] p-3" value={command} onChange={event => { setCommand(event.target.value); setResult(''); }}>
          <option value="summary">สรุปจำนวนข้อมูลในโครงการ</option><option value="add">เพิ่มรายการในหน้าปัจจุบัน</option><option value="save">บันทึกโครงการลงเครื่อง</option><option value="export">ส่งออกสำเนา JSON</option>
        </select></label>
        <p className="text-slate-400">{command === 'summary' ? 'อ่านจำนวนรายการจากข้อมูลปัจจุบัน' : command === 'add' ? `เพิ่มรายการในหน้า ${activeTab} หากหน้านั้นรองรับ` : command === 'save' ? 'บันทึกข้อมูลที่แก้ไขบนเครื่องนี้' : 'เปิดตัวเลือกบันทึกไฟล์สำรอง'}</p>
        <button className="w-full rounded-lg bg-emerald-700 p-3 font-bold" onClick={run}>ทำคำสั่ง</button>
        {result && <pre role="status" className="whitespace-pre-wrap rounded-lg border border-emerald-500/30 bg-black/30 p-3 font-sans leading-6">{result}</pre>}
        <p className="text-xs text-slate-400">การรัน npm หรือเครื่องมือใน W3 ยังไม่ได้เชื่อมกับแอปนี้</p>
      </div>}
    </section>
  </div>;
};
