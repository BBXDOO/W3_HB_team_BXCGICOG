
import React, { useState, useMemo, useEffect } from 'react';
import { RichContent } from '../editor/ContentFormat';
import { StoryPack, CardPack, ModulePack, Asset } from '../../types';
import { Button } from '../../ui/components/Button';
import { Input, TextArea, Select } from '../../ui/components/Input';
import { MonitorCore } from '../../ui/components/MonitorCore';
import { SplitLayout60_40 } from '../../ui/layout/SplitLayout60_40';
import { generateId } from '../../core/utils';
import { Card } from '../../ui/components/Card';

interface CardsTabProps {
  story: StoryPack;
  onChange: (updated: StoryPack) => void;
  toolActions?: any;
  navigationTarget?: string | null;
}

export const CardsTab: React.FC<CardsTabProps> = ({ story, onChange, toolActions, navigationTarget }) => {
  const [selectedId, setSelectedId] = useState<string | null>(story.cards[0]?.id || null);
  useEffect(() => { if (navigationTarget && story.cards.some(c => c.id === navigationTarget)) { setMode('cards'); setSelectedId(navigationTarget); } }, [navigationTarget]);
  const [search, setSearch] = useState('');
  const [mode, setMode] = useState<'cards' | 'modules'>('cards');
  const [selectedModuleId, setSelectedModuleId] = useState<string | null>(story.modules?.[0]?.id || null);
  const modules = story.modules || [];
  const selectedModule = modules.find(module => module.id === selectedModuleId);

  const selectedCard = useMemo(() => 
    story.cards.find(c => c.id === selectedId)
  , [story.cards, selectedId]);

  const updateCard = (updated: CardPack) => {
    onChange({ ...story, cards: story.cards.map(c => c.id === updated.id ? updated : c) });
  };
  const updateModule = (updated: ModulePack) => onChange({ ...story, modules: modules.map(module => module.id === updated.id ? updated : module) });
  const addModule = () => {
    const module: ModulePack = { id: generateId('mod'), name: 'NEW MODULE', type: 'Custom', grade: 'C', description: '', parts: { A: '', B: '', C: '' } };
    onChange({ ...story, modules: [...modules, module] }); setSelectedModuleId(module.id);
  };
  const deleteModule = (module: ModulePack) => {
    const linked = story.cards.filter(card => card.moduleSlots?.includes(module.id));
    if (!confirm(`ลบโมดูล "${module.name}"? ${linked.length ? `ระบบจะถอดออกจากการ์ด ${linked.length} ใบด้วย` : ''}`)) return;
    onChange({ ...story, modules: modules.filter(entry => entry.id !== module.id),
      cards: story.cards.map(card => ({ ...card, moduleSlots: card.moduleSlots?.map(id => id === module.id ? null : id) })) });
    setSelectedModuleId(null);
  };
  const slots = selectedCard?.moduleSlots || [null, null];
  const resizeSlots = (count: 2 | 3) => {
    if (!selectedCard) return;
    if (count === 2 && slots[2] && !confirm('ช่องที่ 3 มีโมดูลอยู่ ต้องการถอดก่อนลดเป็น 2 ช่องหรือไม่?')) return;
    updateCard({ ...selectedCard, moduleSlots: Array.from({ length: count }, (_, index) => slots[index] || null) });
  };

  const addCard = () => {
    const id = generateId('crd');
    const newCard: CardPack = {
      id,
      name: 'NEW CARD',
      type: 'SKILL',
      rarity: 'Common',
      grade: 'C',
      accessLevel: 'A',
      description: 'Module Description',
      inputCondition: '// บรรทัดแรก: กฎหรือเงื่อนไข (Input A)',
      logicCode: '// กระบวนการลอจิก: Code/f (Process B)',
      effectResult: '// ผลลัพธ์สุดท้าย: Effect (Output C)',
      cost: 0,
      cooldownTurns: 0
    };
    onChange({ ...story, cards: [...story.cards, newCard] });
    setSelectedId(id);
  };

  const handleIcon = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !selectedCard) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      const dataUrl = ev.target?.result as string;
      const assetId = generateId('ast');
      const newAsset: Asset = { id: assetId, name: file.name, dataUrl };
      onChange({
        ...story,
        assets: { ...story.assets, [assetId]: newAsset },
        cards: story.cards.map(c => c.id === selectedCard.id ? { ...c, iconAssetId: assetId } : c)
      });
    };
    reader.readAsDataURL(file);
  };

  return (
    <SplitLayout60_40
      toolActions={toolActions}
      topLeft={
        <div className="flex flex-col h-full bg-[var(--surface-2)]">
          <div className="p-3 border-b border-[var(--border)] flex flex-col gap-2">
            <div className="flex gap-2"><button onClick={() => { setMode('cards'); setSearch(''); }} className={`flex-1 p-2 text-xs rounded ${mode === 'cards' ? 'bg-emerald-700 text-white' : 'bg-black/20'}`}>การ์ด</button><button onClick={() => { setMode('modules'); setSearch(''); }} className={`flex-1 p-2 text-xs rounded ${mode === 'modules' ? 'bg-emerald-700 text-white' : 'bg-black/20'}`}>โมดูล</button></div>
            <Button variant="accent" className="h-9 text-[9px]" onClick={mode === 'cards' ? addCard : addModule}>+ สร้าง{mode === 'cards' ? 'การ์ด' : 'โมดูล'}</Button>
            <input 
              type="text" placeholder="Search module registry..." 
              className="w-full text-[10px] p-2 bg-[var(--surface)] border border-[var(--border)] rounded-lg outline-none focus:border-blue-500 text-[var(--text)]"
              value={search} onChange={e => setSearch(e.target.value)}
            />
          </div>
          <div className="flex-1 overflow-y-auto">
            {mode === 'cards' ? story.cards.filter(c => c.name.toLowerCase().includes(search.toLowerCase())).map(c => (
              <button
                key={c.id} onClick={() => setSelectedId(c.id)}
                className={`w-full p-4 text-left border-b border-[var(--border)] transition-all flex justify-between items-center ${selectedId === c.id ? 'bg-[var(--surface)] border-l-4 border-l-blue-600' : 'hover:bg-white/5'}`}
              >
                <div>
                  <div className="text-[11px] font-black text-[var(--text)] uppercase">{c.name}</div>
                  <div className="text-[8px] text-[var(--text-dim)] uppercase font-bold tracking-widest">{c.type} • GRADE {c.grade}</div>
                </div>
                <div className="text-[10px] font-black opacity-30">ACC:{c.accessLevel}</div>
              </button>
            )) : modules.filter(module => module.name.toLowerCase().includes(search.toLowerCase())).map(module => (
              <button key={module.id} onClick={() => setSelectedModuleId(module.id)} className={`w-full p-4 text-left border-b border-[var(--border)] ${selectedModuleId === module.id ? 'border-l-4 border-l-emerald-500 bg-[var(--surface)]' : ''}`}>
                <div className="text-[11px] font-black text-[var(--text)]">{module.name}</div><div className="text-[8px] text-[var(--text-dim)]">{module.type} · GRADE {module.grade}</div>
              </button>
            ))}
          </div>
        </div>
      }
      topRight={
        <div className="p-3 md:p-6 flex flex-col gap-6 h-full overflow-y-auto bg-[var(--surface)] scroll-container">
          {mode === 'modules' ? selectedModule ? (
            <div className="flex flex-col gap-4 pb-20 text-[var(--text)]">
              <h2 className="text-base font-bold text-emerald-400">แก้ไขโมดูล</h2>
              <p className="text-xs text-[var(--text-dim)]">โฟลว์ A → B → C ยังรองรับ PASS และ DISPLAY: เท่านั้น ผลเสริม Battle ด้านล่างเป็นข้อมูลที่ประมวลผลแยกเมื่อการ์ดถูกติดตั้งและใช้สกิล</p>
              <Input label="ชื่อโมดูล" value={selectedModule.name} onChange={name => updateModule({ ...selectedModule, name })} />
              <div className="grid grid-cols-2 gap-2"><Input label="ประเภท" value={selectedModule.type} onChange={type => updateModule({ ...selectedModule, type })} />
                <Input label="Grade" value={selectedModule.grade} onChange={grade => updateModule({ ...selectedModule, grade })} /></div>
              <TextArea richText label="รายละเอียด" value={selectedModule.description} onChange={description => updateModule({ ...selectedModule, description })} />
              {(['A','B','C'] as const).map(key => <TextArea key={key} label={`ส่วน ${key}`} value={selectedModule.parts?.[key] || ''} onChange={value => updateModule({ ...selectedModule, parts: { ...selectedModule.parts, [key]: value } })} />)}
              <div className="border border-emerald-400/30 rounded-xl p-3 space-y-3 text-xs">
                <b>ผลเสริมเมื่อเชื่อมกับการ์ดใน Battle</b>
                <p>ชนิดการ์ดต้องตรงกัน โมดูลเชื่อมจะเพิ่มผลให้สกิลของการ์ดที่ตัวละครติดตั้งอยู่</p>
                <label className="block">ใช้ใน Battle <input type="checkbox" checked={!!selectedModule.battleLink} onChange={e => updateModule({ ...selectedModule, battleLink: e.target.checked ? { tag: 'SKILL', effects: [] } : undefined })} /></label>
                {selectedModule.battleLink && <>
                  <label className="block">ชนิดการ์ด<select className="block w-full p-2 bg-[var(--surface-2)]" value={selectedModule.battleLink.tag} onChange={e => updateModule({ ...selectedModule, battleLink: { ...selectedModule.battleLink!, tag: e.target.value } })}>{['SKILL','PASSIVE','CORE'].map(tag => <option key={tag}>{tag}</option>)}</select></label>
                  <label className="block">Rule สำหรับเปิดผลเสริม<select className="block w-full p-2 bg-[var(--surface-2)]" value={selectedModule.battleLink.ruleId || ''} onChange={e => updateModule({ ...selectedModule, battleLink: { ...selectedModule.battleLink!, ruleId: e.target.value || undefined } })}><option value="">ไม่มีเงื่อนไขเพิ่ม</option>{story.rulesets.map(rule => <option key={rule.id} value={rule.id}>{rule.name}</option>)}</select></label>
                  {selectedModule.battleLink.effects.map((effect, index) => <div key={index} className="border p-2 rounded flex flex-wrap gap-2 items-center">
                    <select value={effect.type} onChange={e => { const type = e.target.value; const replacement = type === 'status' ? { type: 'status' as const, target: 'opponent' as const, status: 'ติดพิษ', enabled: true } : { type: 'vital' as const, target: 'opponent' as const, stat: 'hp' as const, amount: -1 }; updateModule({ ...selectedModule, battleLink: { ...selectedModule.battleLink!, effects: selectedModule.battleLink!.effects.map((item, i) => i === index ? replacement : item) } }); }}><option value="vital">HP/MP/EN</option><option value="status">สถานะ</option></select>
                    {(effect.type === 'vital' || effect.type === 'status') && <select value={effect.target} onChange={e => updateModule({ ...selectedModule, battleLink: { ...selectedModule.battleLink!, effects: selectedModule.battleLink!.effects.map((item, i) => i === index ? { ...effect, target: e.target.value as 'self'|'opponent' } : item) } })}><option value="opponent">อีกฝั่ง</option><option value="self">ตนเอง</option></select>}
                    {effect.type === 'vital' && <><select value={effect.stat} onChange={e => updateModule({ ...selectedModule, battleLink: { ...selectedModule.battleLink!, effects: selectedModule.battleLink!.effects.map((item, i) => i === index ? { ...effect, stat: e.target.value as 'hp'|'mp'|'en' } : item) } })}>{['hp','mp','en'].map(stat => <option key={stat}>{stat}</option>)}</select><input className="w-20 p-1 bg-[var(--surface-2)]" type="number" value={effect.amount} onChange={e => updateModule({ ...selectedModule, battleLink: { ...selectedModule.battleLink!, effects: selectedModule.battleLink!.effects.map((item, i) => i === index ? { ...effect, amount: Number(e.target.value) } : item) } })} /></>}
                    {effect.type === 'status' && <><input aria-label="ชื่อสถานะ" className="p-1 bg-[var(--surface-2)]" value={effect.status} onChange={e => updateModule({ ...selectedModule, battleLink: { ...selectedModule.battleLink!, effects: selectedModule.battleLink!.effects.map((item, i) => i === index ? { ...effect, status: e.target.value } : item) } })} /><select value={String(effect.enabled)} onChange={e => updateModule({ ...selectedModule, battleLink: { ...selectedModule.battleLink!, effects: selectedModule.battleLink!.effects.map((item, i) => i === index ? { ...effect, enabled: e.target.value === 'true' } : item) } })}><option value="true">เพิ่ม</option><option value="false">ถอด</option></select></>}
                    <button onClick={() => updateModule({ ...selectedModule, battleLink: { ...selectedModule.battleLink!, effects: selectedModule.battleLink!.effects.filter((_, i) => i !== index) } })}>ลบ</button>
                  </div>)}
                  <button className="border rounded p-2" onClick={() => updateModule({ ...selectedModule, battleLink: { ...selectedModule.battleLink!, effects: [...selectedModule.battleLink!.effects, { type: 'vital', target: 'opponent', stat: 'hp', amount: -1 }] } })}>+ เพิ่มผลเสริม</button>
                </>}
              </div>
              <Button variant="danger" onClick={() => deleteModule(selectedModule)}>ลบโมดูล</Button>
            </div>
          ) : <p className="text-sm text-[var(--text-dim)]">เลือกหรือสร้างโมดูล</p> : selectedCard ? (
            <div className="flex flex-col gap-6 pb-20 animate-in fade-in">
              {/* Header Editor - ถอดแบบจาก ID/Name/Type/Acc */}
              <Card className="p-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                 <Input label="Module Name" value={selectedCard.name} onChange={v => updateCard({...selectedCard, name: v})} />
                 <Select label="Type" value={selectedCard.type} options={[{label:'SKILL',value:'SKILL'},{label:'PASSIVE',value:'PASSIVE'},{label:'CORE',value:'CORE'}]} onChange={v => updateCard({...selectedCard, type: v})} />
                 <div className="grid grid-cols-2 gap-2">
                    <Input label="Grade" value={selectedCard.grade} onChange={v => updateCard({...selectedCard, grade: v})} />
                    <Select label="Access" value={selectedCard.accessLevel} options={[{label:'A',value:'A'},{label:'B',value:'B'},{label:'C',value:'C'},{label:'ALL',value:'ALL'}]} onChange={v => updateCard({...selectedCard, accessLevel: v as any})} />
                 </div>
                 <Select label="Rarity" value={selectedCard.rarity} options={[{label:'Common',value:'Common'},{label:'Rare',value:'Rare'},{label:'Epic',value:'Epic'},{label:'Legendary',value:'Legendary'}]} onChange={v => updateCard({...selectedCard, rarity: v as any})} />
              </Card>

              <Card className="p-4 flex flex-col gap-3">
                <h3 className="text-sm font-bold text-emerald-400">ประกอบโมดูลบนการ์ด</h3>
                <p className="text-xs text-[var(--text-dim)]">เลือก 2 หรือ 3 ช่อง ถอดและเปลี่ยนได้ โมดูลที่ตั้งค่าผลเสริม Battle จะทำงานเมื่อชนิดการ์ดและ Rule ตรงกัน ส่วน Grade/Access ยังไม่ตัดสินผล</p>
                <label className="text-xs text-[var(--text)]">จำนวนช่อง <select value={slots.length === 3 ? 3 : 2} onChange={e => resizeSlots(Number(e.target.value) as 2 | 3)} className="ml-2 p-2 bg-[var(--surface-2)] rounded"><option value="2">2</option><option value="3">3</option></select></label>
                {Array.from({ length: slots.length === 3 ? 3 : 2 }, (_, index) => <label key={index} className="text-xs text-[var(--text)]">ช่อง {index + 1}
                  <select value={slots[index] || ''} onChange={e => { const next = Array.from({ length: slots.length === 3 ? 3 : 2 }, (_, i) => slots[i] || null); next[index] = e.target.value || null; updateCard({ ...selectedCard, moduleSlots: next }); }} className="mt-1 block w-full p-3 bg-[var(--surface-2)] rounded border border-[var(--border)]">
                    <option value="">— ว่าง / ถอดโมดูล —</option>{modules.map(module => <option key={module.id} value={module.id}>{module.name} · {module.grade}</option>)}
                  </select>
                </label>)}
                {slots.some(id => !!id && !modules.some(module => module.id === id)) && <p className="text-amber-400 text-xs">มีโมดูลที่อ้างถึงแต่ไม่พบในคลัง</p>}
              </Card>

              {/* LOGIC BUILDER (A-B-C) - หัวใจของภาพร่าง */}
              <div className="flex flex-col gap-4">
                 <div className="flex items-center gap-2 px-1">
                    <div className="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-[10px] font-black">A</div>
                    <h3 className="text-[10px] font-black text-[var(--text-dim)] uppercase tracking-widest">Input / Rule (First Line)</h3>
                 </div>
                 <TextArea 
                    placeholder="ใส่กฎหรือเงื่อนไขบรรทัดแรกที่นี่..."
                    className="font-mono text-[11px] bg-blue-500/5"
                    value={selectedCard.inputCondition}
                    onChange={v => updateCard({...selectedCard, inputCondition: v})}
                 />

                 <div className="flex items-center gap-2 px-1">
                    <div className="w-6 h-6 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[10px] font-black">B</div>
                    <h3 className="text-[10px] font-black text-[var(--text-dim)] uppercase tracking-widest">Logic Process (Code/f)</h3>
                 </div>
                 <textarea 
                    className="w-full bg-[var(--surface-2)] text-blue-400 p-4 rounded-2xl text-[11px] font-mono min-h-[140px] outline-none border border-white/5 focus:border-blue-500/50 shadow-inner"
                    value={selectedCard.logicCode}
                    placeholder="// เขียนกระบวนการลอจิกที่นี่..."
                    onChange={e => updateCard({...selectedCard, logicCode: e.target.value})}
                 />

                 <div className="flex items-center gap-2 px-1">
                    <div className="w-6 h-6 rounded-full bg-amber-600 text-white flex items-center justify-center text-[10px] font-black">C</div>
                    <h3 className="text-[10px] font-black text-[var(--text-dim)] uppercase tracking-widest">Output / Final Effects</h3>
                 </div>
                 <TextArea 
                    placeholder="ระบุผลลัพธ์ของเอฟเฟกต์ที่นี่..."
                    className="font-mono text-[11px] bg-amber-500/5"
                    value={selectedCard.effectResult}
                    onChange={v => updateCard({...selectedCard, effectResult: v})}
                 />
              </div>

              <Button variant="danger" className="h-10 mt-4" onClick={() => {
                if(confirm('ลบการ์ดนี้? ช่องของตัวละครที่อ้างการ์ดนี้จะถูกถอดด้วย')) {
                  onChange({ ...story, cards: story.cards.filter(c => c.id !== selectedId),
                    characters: story.characters.map(character => ({ ...character,
                      logicSlots: { ...character.logicSlots,
                        slotA: character.logicSlots?.slotA === selectedId ? '' : character.logicSlots?.slotA,
                        slotB: character.logicSlots?.slotB === selectedId ? '' : character.logicSlots?.slotB,
                        slotC: character.logicSlots?.slotC === selectedId ? '' : character.logicSlots?.slotC },
                      abilitySlots: character.abilitySlots.map(slot => slot.equippedCardId === selectedId ? { ...slot, equippedCardId: undefined } : slot)
                    })) });
                  setSelectedId(null);
                }
              }}>PURGE MODULE</Button>
            </div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center opacity-20 text-center">
              <span className="text-4xl mb-4">⚡</span>
              <p className="text-[10px] font-black uppercase tracking-widest">Select module registry</p>
            </div>
          )}
        </div>
      }
      bottomMain={
        <MonitorCore title={mode === 'modules' ? 'Module Preview' : 'Card Visualizer'} isEmpty={mode === 'modules' ? !selectedModule : !selectedCard}>
          {mode === 'modules' && selectedModule && <div className="p-5 text-[var(--text)] overflow-y-auto h-full"><h2 className="text-xl font-bold">{selectedModule.name}</h2><p className="text-xs">{selectedModule.type} · Grade {selectedModule.grade}</p><p className="mt-3 whitespace-pre-wrap"><RichContent value={selectedModule.description} /></p>{(['A','B','C'] as const).map(key => <div key={key} className="mt-3 border border-[var(--border)] rounded p-3"><b>{key}</b><p className="whitespace-pre-wrap text-sm">{selectedModule.parts?.[key]}</p></div>)}</div>}
          {mode === 'cards' && selectedCard && (
            <div className="flex h-full min-h-[210px] w-full gap-2 md:gap-5 overflow-hidden">
              <div className="w-[46%] md:w-[42%] min-w-0 h-full overflow-y-auto overflow-x-hidden flex justify-start items-start pl-1 md:pl-4 py-2 scroll-container">
              {/* THE MODULE CARD (ถอดแบบจากภาพวาด) */}
              <div className="module-card-preview w-72 h-[460px] shrink-0 origin-top-left bg-[var(--surface)] border-[2px] border-[var(--border)] rounded-[40px] p-5 flex flex-col shadow-2xl relative overflow-hidden group">
                
                {/* Header (ID/Name/Type/Acc + PIC) */}
                <div className="flex gap-4 mb-4 h-24">
                   <div className="flex-1 flex flex-col justify-between py-1">
                      <div>
                        <div className="text-[8px] font-black text-blue-500 uppercase tracking-tighter">ID: {selectedCard.id.slice(-8)}</div>
                        <h4 className="text-sm font-black text-[var(--text)] leading-tight uppercase truncate">{selectedCard.name}</h4>
                      </div>
                      <div className="flex flex-col gap-1">
                        <div className="text-[8px] font-bold text-[var(--text-dim)] uppercase">TYPE: {selectedCard.type}</div>
                        <div className="text-[9px] font-black text-blue-400 uppercase">ACCESS: {selectedCard.accessLevel}</div>
                      </div>
                   </div>
                   <div className="w-20 h-20 w3-card-inset flex items-center justify-center relative overflow-hidden shrink-0 rounded-2xl border-2 border-white/5">
                      {selectedCard.iconAssetId ? (
                        <img src={story.assets[selectedCard.iconAssetId]?.dataUrl} className="w-full h-full object-cover" />
                      ) : <span className="text-2xl opacity-10 font-black">PIC</span>}
                      <input type="file" className="absolute inset-0 opacity-0 cursor-pointer" onChange={handleIcon} />
                      {/* Grade Badge - ตามภาพร่าง */}
                      <div className="absolute top-0 right-0 bg-blue-600 text-white font-black text-[10px] w-7 h-7 flex items-center justify-center rounded-bl-xl shadow-lg border-l border-b border-white/20">{selectedCard.grade}</div>
                   </div>
                </div>

                {/* Input A (บรรทัดแรก/กฎ) */}
                <div className="mb-3 p-3 bg-blue-500/10 border border-blue-500/20 rounded-xl">
                   <p className="text-[9px] font-mono text-blue-400 italic leading-tight">
                     {selectedCard.inputCondition || '// Rule Logic A'}
                   </p>
                </div>

                {/* Process B (Code Block) */}
                <div className="flex-1 w3-card-inset bg-[var(--surface-2)] rounded-2xl p-4 mb-3 border border-white/5 font-mono text-[10px] text-emerald-400 overflow-hidden relative shadow-inner">
                   <div className="absolute top-2 right-3 text-[7px] text-white/10 font-black tracking-widest uppercase">PROCESS_B</div>
                   <div className="whitespace-pre-wrap leading-relaxed opacity-80">
                     {selectedCard.logicCode || '// Processing...'}
                   </div>
                </div>

                {/* Output C (Effect Area) */}
                <div className="h-20 w3-card-inset bg-amber-500/5 rounded-2xl p-3 border border-amber-500/10 font-mono text-[9px] text-amber-500 overflow-hidden relative">
                   <div className="absolute top-2 right-3 text-[7px] text-amber-500/20 font-black uppercase">EFFECT_C</div>
                   <p className="leading-relaxed opacity-90">{selectedCard.effectResult || '// Final Output'}</p>
                </div>

                {/* Bottom Bar */}
                <div className="mt-3 flex justify-between items-center px-1">
                   <div className="text-[9px] font-black text-[var(--text-dim)] uppercase tracking-widest">{selectedCard.rarity}</div>
                   <div className="flex gap-1">
                      <div className="w-1.5 h-1.5 rounded-full bg-blue-500"></div>
                      <div className="w-1.5 h-1.5 rounded-full bg-blue-500/20"></div>
                   </div>
                </div>
              </div>
              </div>
              <div className="flex-1 min-w-0 h-full overflow-y-auto py-2 pr-1 md:pr-4 scroll-container" aria-label="ชุดคำสั่งโมดูล A B C">
                {([
                  ['A', selectedCard.inputCondition, 'text-blue-400', 'border-blue-500/30'],
                  ['B', selectedCard.logicCode, 'text-emerald-400', 'border-emerald-500/30'],
                  ['C', selectedCard.effectResult, 'text-amber-400', 'border-amber-500/30']
                ] as const).map(([part, commands, color, border]) => (
                  <div key={part} className={`mb-2 rounded-xl border ${border} bg-[var(--surface)] p-2 md:p-3`}>
                    <div className={`text-xs font-black ${color}`}>{part}</div>
                    <pre className="mt-1 whitespace-pre-wrap break-words font-mono text-[10px] md:text-xs leading-relaxed text-[var(--text)]">{commands || '—'}</pre>
                  </div>
                ))}
              </div>
            </div>
          )}
        </MonitorCore>
      }
    />
  );
};
