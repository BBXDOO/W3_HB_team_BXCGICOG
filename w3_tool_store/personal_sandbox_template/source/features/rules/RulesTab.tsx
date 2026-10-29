import React, { useState, useEffect } from 'react';
import type { StoryPack, RulesetPack, RuleBlock } from '../../types';
import { Button } from '../../ui/components/Button';
import { Input, TextArea } from '../../ui/components/Input';
import { MonitorCore } from '../../ui/components/MonitorCore';
import { SplitLayout60_40 } from '../../ui/layout/SplitLayout60_40';
import { generateId } from '../../core/utils';
import { evaluateRuleset, type RuleReport } from '../../core/ruleRuntime';
import { RichContent } from '../editor/ContentFormat';

interface Props { story: StoryPack; onChange: (updated: StoryPack) => void; navigationTarget?: string | null; }
const newBlock = (): RuleBlock => ({ id: generateId('ruleblock'), title: 'ข้อใหม่', content: '', kind: 'reference', children: [] });
const updateAt = (blocks: RuleBlock[], path: number[], change: (block: RuleBlock) => RuleBlock): RuleBlock[] =>
  blocks.map((block, index) => index !== path[0] ? block : path.length === 1 ? change(block) :
    { ...block, children: updateAt(block.children || [], path.slice(1), change) });
const removeAt = (blocks: RuleBlock[], path: number[]): RuleBlock[] => path.length === 1
  ? blocks.filter((_, index) => index !== path[0])
  : blocks.map((block, index) => index === path[0]
    ? { ...block, children: removeAt(block.children || [], path.slice(1)) } : block);

export const RulesTab: React.FC<Props> = ({ story, onChange, navigationTarget }) => {
  const [selectedId, setSelectedId] = useState<string | null>(story.rulesets?.[0]?.id || null);
  const [contextText, setContextText] = useState('{}');
  const [report, setReport] = useState<RuleReport | null>(null);
  const [contextError, setContextError] = useState('');
  useEffect(() => { if (navigationTarget && story.rulesets.some(rule => rule.id === navigationTarget)) setSelectedId(navigationTarget); }, [navigationTarget, story.rulesets]);
  const selected = story.rulesets.find(rule => rule.id === selectedId);
  const update = (rule: RulesetPack) => onChange({ ...story, rulesets: story.rulesets.map(item => item.id === rule.id ? rule : item) });
  const add = () => {
    const rule: RulesetPack = { id: generateId('rule'), name: 'กฎใหม่', blocks: [], modifiers: [] };
    onChange({ ...story, rulesets: [...story.rulesets, rule] }); setSelectedId(rule.id);
  };
  const editBlock = (path: number[], change: (block: RuleBlock) => RuleBlock) => {
    if (selected) update({ ...selected, blocks: updateAt(selected.blocks, path, change) });
  };
  const inspect = () => {
    if (!selected) return;
    try {
      const parsed: unknown = JSON.parse(contextText);
      if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) throw new Error('บริบทต้องเป็น JSON object');
      setReport(evaluateRuleset(selected, parsed as Record<string, unknown>, story.commonPlay || [])); setContextError('');
    } catch (error) { setReport(null); setContextError(error instanceof Error ? error.message : 'อ่านบริบทไม่ได้'); }
  };
  const renderEditor = (blocks: RuleBlock[], prefix = '', parent: number[] = []): React.ReactNode => blocks.map((block, index) => {
    const path = [...parent, index], number = `${prefix}${index + 1}`;
    return <div key={block.id || number} className="border-l-2 border-emerald-500/40 pl-3 mt-3 space-y-2">
      <div className="flex items-center gap-2"><span className="text-xs font-bold text-emerald-300">{number}</span>
        <input aria-label={`ชื่อข้อ ${number}`} value={block.title} onChange={e => editBlock(path, old => ({ ...old, title: e.target.value }))} className="flex-1 min-w-0 rounded bg-black/30 p-2 text-sm" />
        <button className="text-xs text-red-300" aria-label={`ลบข้อ ${number}`} onClick={() => selected && update({ ...selected, blocks: removeAt(selected.blocks, path) })}>ลบ</button></div>
      <label className="block text-xs text-slate-300">ประเภท
        <select value={block.kind || 'reference'} onChange={e => editBlock(path, old => ({ ...old, kind: e.target.value as RuleBlock['kind'] }))} className="ml-2 rounded bg-[var(--surface-2)] p-2">
          <option value="reference">คำอธิบาย/อ้างอิง</option><option value="condition">เงื่อนไขที่นิยามไว้ (ยังไม่รัน)</option>
        </select></label>
      <TextArea richText={block.kind !== 'condition'} label="เนื้อหา (เขียน Markdown ได้)" value={block.content} onChange={value => editBlock(path, old => ({ ...old, content: value }))} />
      {block.kind === 'condition' && <div className="grid grid-cols-2 gap-2 rounded-lg border border-emerald-500/20 p-2">
        <Input label="ชื่อ input เช่น area.type" value={block.inputKey || ''} onChange={value => editBlock(path, old => ({ ...old, inputKey: value }))} />
        <label className="text-xs">เปรียบเทียบ<select className="block w-full bg-[var(--surface-2)] p-2 rounded" value={block.operator || ''} onChange={e => editBlock(path, old => ({ ...old, operator: e.target.value as RuleBlock['operator'] }))}>
          <option value="">เลือก</option>{['exists','==','!=','>','>=','<','<='].map(op => <option key={op} value={op}>{op}</option>)}
        </select></label>
        {block.operator !== 'exists' && <Input label="ค่าที่เทียบ" value={block.expected || ''} onChange={value => editBlock(path, old => ({ ...old, expected: value }))} />}
        <Input label="อ้างอิงคำสั่ง Common Play (ยังไม่รัน)" value={block.commandRef || ''} onChange={value => editBlock(path, old => ({ ...old, commandRef: value }))} />
      </div>}
      <button className="text-xs text-emerald-300 border border-emerald-600/40 px-3 py-2 rounded" onClick={() => editBlock(path, old => ({ ...old, children: [...(old.children || []), newBlock()] }))}>+ เพิ่มข้อย่อยใต้ {number}</button>
      {renderEditor(block.children || [], `${number}.`, path)}
    </div>;
  });
  const renderPreview = (blocks: RuleBlock[], prefix = ''): React.ReactNode => blocks.map((block, index) => {
    const number = `${prefix}${index + 1}`;
    return <div key={block.id || number} className="border-l border-emerald-600/40 pl-4 mt-3">
      <h3 className="font-bold text-emerald-200">{number}. {block.title}</h3>
      <p className="text-[11px] text-slate-400">{block.kind === 'condition' ? 'เงื่อนไขที่นิยามไว้ · ยังไม่รัน' : 'คำอธิบาย/อ้างอิง'}</p>
      <p className="whitespace-pre-wrap text-sm mt-2"><RichContent value={block.content} /></p>{renderPreview(block.children || [], `${number}.`)}
    </div>;
  });
  return <SplitLayout60_40
    topLeft={<div className="h-full flex flex-col bg-[var(--surface-2)] p-3 gap-3"><Button variant="accent" onClick={add}>+ NEW RULESET</Button>
      <div className="overflow-y-auto space-y-2">{story.rulesets.map(rule => <button key={rule.id} onClick={() => { setSelectedId(rule.id); setReport(null); setContextError(''); }} className={`w-full text-left rounded-lg p-3 text-sm ${selected?.id === rule.id ? 'bg-emerald-800/50' : 'bg-white/5'}`}>{rule.name}</button>)}</div></div>}
    topRight={<div className="h-full overflow-y-auto p-4 md:p-6 text-slate-100"><h2 className="text-xs font-bold tracking-widest text-emerald-300">RULE PROTOCOL EDITOR</h2>
      {selected ? <div className="space-y-5 mt-5 pb-16"><Input label="ชื่อชุดกฎ" value={selected.name} onChange={value => update({ ...selected, name: value })} />
        <p className="text-xs text-slate-400">ข้อย่อยเรียงเป็นทรี ข้อแบบคำอธิบายไม่ถูกประมวลผล ข้อแบบเงื่อนไขตรวจ input จากบริบทที่ส่งเข้ามาได้ โดยยังไม่เรียกคำสั่งหรือเปลี่ยนสถานะ</p>
        {renderEditor(selected.blocks)}<Button variant="secondary" onClick={() => update({ ...selected, blocks: [...selected.blocks, newBlock()] })}>+ เพิ่มข้อหลัก</Button>
        <section className="rounded-xl border border-emerald-500/30 p-3 space-y-2"><h3 className="font-bold text-emerald-200">ทดลองตรวจบริบท</h3>
          <TextArea label="ข้อมูลเข้า JSON (ตั้งชื่อเองได้ ไม่บันทึกในโครงการ)" value={contextText} onChange={value => { setContextText(value); setReport(null); }} />
          <Button variant="secondary" onClick={inspect}>ตรวจเงื่อนไข</Button>
          {contextError && <p role="alert" className="text-red-300">ERROR: {contextError}</p>}
          {report && <div role="status" className="text-sm space-y-1"><b>{report.status}</b>{report.trace.map(entry => <p key={entry.path}>{entry.path} {entry.title}: {entry.status} — {entry.message}{entry.commandRef ? ` · อ้างอิง ${entry.commandRef} (ยังไม่รัน)` : ''}</p>)}</div>}
        </section>
        <Button variant="danger" onClick={() => { if (confirm('ลบชุดกฎนี้?')) { onChange({ ...story, rulesets: story.rulesets.filter(rule => rule.id !== selected.id) }); setSelectedId(null); } }}>ลบชุดกฎ</Button>
      </div> : <p className="mt-6 text-sm text-slate-400">เลือกหรือเพิ่มชุดกฎ</p>}</div>}
    bottomMain={<MonitorCore title="Rule Tree Preview" isEmpty={!selected}>{selected && <div className="p-5 text-slate-100 overflow-y-auto h-full"><h2 className="text-xl font-bold">{selected.name}</h2>{renderPreview(selected.blocks)}</div>}</MonitorCore>}
  />;
};
