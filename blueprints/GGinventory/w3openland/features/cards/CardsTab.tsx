
import React, { useState, useMemo } from 'react';
import { StoryPack, CardPack, Asset } from '../../types';
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
}

export const CardsTab: React.FC<CardsTabProps> = ({ story, onChange, toolActions }) => {
  const [selectedId, setSelectedId] = useState<string | null>(story.cards[0]?.id || null);
  const [search, setSearch] = useState('');

  const selectedCard = useMemo(() => 
    story.cards.find(c => c.id === selectedId)
  , [story.cards, selectedId]);

  const updateCard = (updated: CardPack) => {
    onChange({ ...story, cards: story.cards.map(c => c.id === updated.id ? updated : c) });
  };

  const addCard = () => {
    const id = generateId('crd');
    const newCard: CardPack = {
      id,
      name: 'NEW MODULE',
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
            <Button variant="accent" className="h-9 text-[9px]" onClick={addCard}>+ INITIALIZE MODULE</Button>
            <input 
              type="text" placeholder="Search module registry..." 
              className="w-full text-[10px] p-2 bg-[var(--surface)] border border-[var(--border)] rounded-lg outline-none focus:border-blue-500 text-[var(--text)]"
              value={search} onChange={e => setSearch(e.target.value)}
            />
          </div>
          <div className="flex-1 overflow-y-auto">
            {story.cards.filter(c => c.name.toLowerCase().includes(search.toLowerCase())).map(c => (
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
            ))}
          </div>
        </div>
      }
      topRight={
        <div className="p-3 md:p-6 flex flex-col gap-6 h-full overflow-y-auto bg-[var(--surface)] scroll-container">
          {selectedCard ? (
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
                    className="w-full bg-[#050505] text-blue-400 p-4 rounded-2xl text-[11px] font-mono min-h-[140px] outline-none border border-white/5 focus:border-blue-500/50 shadow-inner"
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
                if(confirm('Purge module?')) {
                  onChange({...story, cards: story.cards.filter(c => c.id !== selectedId)});
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
        <MonitorCore title="Module Visualizer (Sketch Based)" isEmpty={!selectedCard}>
          {selectedCard && (
            <div className="flex items-center justify-center py-6 h-full">
              {/* THE MODULE CARD (ถอดแบบจากภาพวาด) */}
              <div className="w-72 h-[460px] bg-[var(--surface)] border-[2px] border-[var(--border)] rounded-[40px] p-5 flex flex-col shadow-2xl relative overflow-hidden group">
                
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
                <div className="flex-1 w3-card-inset bg-[#050505] rounded-2xl p-4 mb-3 border border-white/5 font-mono text-[10px] text-emerald-400 overflow-hidden relative shadow-inner">
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
          )}
        </MonitorCore>
      }
    />
  );
};
