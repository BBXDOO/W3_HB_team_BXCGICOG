
import React, { useState, useMemo } from 'react';
import { StoryPack, CharacterPack, Asset, AttributeDef } from '../../types';
import { Button } from '../../ui/components/Button';
import { Input, TextArea, Select } from '../../ui/components/Input';
import { MonitorCore } from '../../ui/components/MonitorCore';
import { SplitLayout60_40 } from '../../ui/layout/SplitLayout60_40';
import { generateId, getStatusColor } from '../../core/utils';
import { Card } from '../../ui/components/Card';
import { Modal } from '../../ui/components/Modal';

interface CharactersTabProps {
  story: StoryPack;
  onChange: (updated: StoryPack) => void;
  toolActions?: any;
}

const CapabilityRow: React.FC<{ 
  label: string, 
  value: number, 
  onChange: (val: number) => void 
}> = ({ label, value, onChange }) => {
  return (
    <div className="flex items-center gap-1.5 p-1 w3-card-inset bg-[var(--surface)] border-[var(--border)] hover:border-blue-400 transition-all group">
      <div className="w-8 text-[6px] font-black text-[var(--text-dim)] uppercase tracking-tighter truncate" title={label}>{label}</div>
      <input 
        type="number" 
        value={value ?? 0} 
        onChange={(e) => onChange(parseInt(e.target.value) || 0)}
        className="w-8 bg-[var(--surface-2)] p-0.5 rounded font-black text-center text-[9px] outline-none focus:text-blue-600 transition-all text-[var(--text)]"
      />
      <div className="flex-1 h-0.5 rounded-full overflow-hidden bg-[var(--surface-2)]">
        <div 
          className="h-full rounded-full transition-all duration-700 ease-out" 
          style={{ width: `${Math.min(100, ((value || 0) / 10) * 100)}%`, backgroundColor: getStatusColor(Math.min(10, value || 0)) }}
        />
      </div>
    </div>
  );
};

export const CharactersTab: React.FC<CharactersTabProps> = ({ story, onChange, toolActions }) => {
  const [selectedId, setSelectedId] = useState<string | null>(story.characters[0]?.id || null);
  const [search, setSearch] = useState('');
  const [isManageStatsOpen, setIsManageStatsOpen] = useState(false);

  const selectedChar = useMemo(() => 
    story.characters.find(c => c.id === selectedId)
  , [story.characters, selectedId]);

  const addChar = () => {
    const id = generateId('chr');
    const capabilities: Record<string, number> = {};
    story.attributeDefinitions.forEach(a => capabilities[a.key] = a.defaultValue);

    const newChar: CharacterPack = {
      id, name: 'New Soul', className: 'Novice', charType: 'NPC',
      vitals: { hp: 100, mp: 100, en: 100 },
      capabilities,
      attributes: { ACT: 10, DEF: 10, SPE: 10, CRI: 5 },
      logicSlots: { slotA: '', slotB: '', slotC: '', totalResult: '' },
      statusEffects: [],
      elemental: { yangGroup: [], yinGroup: [] },
      innateSkill: { name: 'New Skill', description: '', rarity: 3 },
      resonanceMatrix: Array(5).fill(0).map(() => Array(5).fill(0)),
      abilitySlots: [{ name: 'Slot 1' }], backgroundText: ''
    };
    onChange({ ...story, characters: [...story.characters, newChar] });
    setSelectedId(id);
  };

  const updateChar = (updated: Partial<CharacterPack>) => {
    if (!selectedChar) return;
    onChange({ ...story, characters: story.characters.map(c => c.id === selectedChar.id ? { ...c, ...updated } : c) });
  };

  const addAttribute = () => {
    const newAttr: AttributeDef = { key: 'NEW', label: 'New Stat', defaultValue: 0 };
    const nextSchema = [...story.attributeDefinitions, newAttr];
    
    // Update all characters to include this new stat
    const nextChars = story.characters.map(c => ({
      ...c,
      capabilities: { ...c.capabilities, [newAttr.key]: newAttr.defaultValue }
    }));

    onChange({ ...story, attributeDefinitions: nextSchema, characters: nextChars });
  };

  const updateAttribute = (index: number, updated: AttributeDef) => {
    const oldKey = story.attributeDefinitions[index].key;
    const nextSchema = [...story.attributeDefinitions];
    nextSchema[index] = updated;

    // If key changed, update all characters
    let nextChars = story.characters;
    if (oldKey !== updated.key) {
      nextChars = story.characters.map(c => {
        const nextCaps = { ...c.capabilities };
        nextCaps[updated.key] = nextCaps[oldKey] ?? updated.defaultValue;
        delete nextCaps[oldKey];
        return { ...c, capabilities: nextCaps };
      });
    }

    onChange({ ...story, attributeDefinitions: nextSchema, characters: nextChars });
  };

  const deleteAttribute = (index: number) => {
    const key = story.attributeDefinitions[index].key;
    const nextSchema = story.attributeDefinitions.filter((_, i) => i !== index);
    const nextChars = story.characters.map(c => {
      const nextCaps = { ...c.capabilities };
      delete nextCaps[key];
      return { ...c, capabilities: nextCaps };
    });
    onChange({ ...story, attributeDefinitions: nextSchema, characters: nextChars });
  };

  const handlePortrait = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !selectedChar) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      const dataUrl = ev.target?.result as string;
      const assetId = generateId('ast');
      const newAsset: Asset = { id: assetId, name: file.name, dataUrl };
      onChange({
        ...story,
        assets: { ...story.assets, [assetId]: newAsset },
        characters: story.characters.map(c => c.id === selectedChar.id ? { ...c, portraitAssetId: assetId } : c)
      });
    };
    reader.readAsDataURL(file);
  };

  const cardOptions = [{label: '--- No Card ---', value: ''}, ...story.cards.map(c => ({ label: c.name, value: c.id }))];

  return (
    <>
      <SplitLayout60_40
        toolActions={toolActions}
        showTools={false}
        topLeft={
          <div className="flex flex-col h-full bg-[var(--surface-2)]">
            <div className="p-2 border-b border-[var(--border)] flex flex-col gap-1.5">
              <Button id="tab-primary-add" variant="accent" onClick={addChar} className="h-8 text-[9px]">+ INITIALIZE SOUL</Button>
              <input 
                type="text" placeholder="Search registry..." 
                className="w-full text-[9px] p-1.5 bg-[var(--surface)] border border-[var(--border)] rounded outline-none focus:border-blue-500 text-[var(--text)]"
                value={search} onChange={e => setSearch(e.target.value)}
              />
            </div>
            <div className="flex-1 overflow-y-auto scroll-container">
              {story.characters.filter(c => c.name.toLowerCase().includes(search.toLowerCase())).map(c => (
                <button
                  key={c.id} onClick={() => setSelectedId(c.id)}
                  className={`w-full p-2.5 text-left border-b border-[var(--border)] transition-all clickable ${selectedId === c.id ? 'bg-[var(--surface)] border-l-4 border-l-blue-600 shadow-sm' : 'hover:bg-white/5'}`}
                >
                  <div className="text-[10px] font-black text-[var(--text)] uppercase">{c.name}</div>
                  <div className="text-[7px] text-[var(--text-dim)] uppercase font-black tracking-widest">{c.className}</div>
                </button>
              ))}
            </div>
          </div>
        }
        topRight={
          <div className="p-3 md:p-6 flex flex-col gap-6 overflow-y-auto h-full bg-[var(--surface)] scroll-container">
            {selectedChar ? (
              <div className="flex flex-col gap-5 animate-in fade-in pb-20">
                <Card className="p-3 flex flex-col gap-3">
                   <div className="flex flex-col md:flex-row gap-3 items-start md:items-center">
                      <div className="w-12 h-12 w3-card-inset flex items-center justify-center text-xl shrink-0">👤</div>
                      <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-2 w-full">
                         <Input label="Name" value={selectedChar.name} onChange={v => updateChar({name: v})} />
                         <Input label="Role" value={selectedChar.className} onChange={v => updateChar({className: v})} />
                      </div>
                      <Button variant="danger" className="h-8 px-3 text-[8px]" onClick={() => { if (confirm('Purge soul?')) { onChange({...story, characters: story.characters.filter(c => c.id !== selectedId)}); setSelectedId(null); } }}>PURGE</Button>
                   </div>
                </Card>

                <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
                   <div className="flex flex-col gap-2">
                      <h3 className="text-[9px] font-black text-blue-500 uppercase tracking-widest px-1">Logic Modules</h3>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                        <Select label="A" value={selectedChar.logicSlots?.slotA || ''} options={cardOptions} onChange={v => updateChar({logicSlots: {...selectedChar.logicSlots, slotA: v}})} />
                        <Select label="B" value={selectedChar.logicSlots?.slotB || ''} options={cardOptions} onChange={v => updateChar({logicSlots: {...selectedChar.logicSlots, slotB: v}})} />
                        <Select label="C" value={selectedChar.logicSlots?.slotC || ''} options={cardOptions} onChange={v => updateChar({logicSlots: {...selectedChar.logicSlots, slotC: v}})} />
                      </div>
                      <Input label="Output Preview" value={selectedChar.logicSlots?.totalResult || ''} onChange={v => updateChar({logicSlots: {...selectedChar.logicSlots, totalResult: v}})} />
                   </div>
                   <div className="flex flex-col gap-2">
                      <h3 className="text-[9px] font-black text-blue-500 uppercase tracking-widest px-1">Elements & History</h3>
                      <div className="w3-card p-3 flex flex-col gap-3 bg-black/5">
                        <div className="flex gap-1 justify-center">
                            {['E', 'F', 'L'].map(e => (
                               <button key={e} onClick={() => {
                                 const cur = selectedChar.elemental?.yangGroup || [];
                                 updateChar({elemental: {...selectedChar.elemental, yangGroup: cur.includes(e as any) ? cur.filter(x => x !== e) : [...cur, e as any]}});
                               }} className={`w-7 h-7 rounded-lg text-[10px] font-black ${selectedChar.elemental?.yangGroup?.includes(e as any) ? 'bg-amber-500 text-black' : 'bg-white/5 opacity-30'}`}>{e}</button>
                            ))}
                            <div className="w-4"></div>
                            {['R', 'W', 'D'].map(e => (
                               <button key={e} onClick={() => {
                                 const cur = selectedChar.elemental?.yinGroup || [];
                                 updateChar({elemental: {...selectedChar.elemental, yinGroup: cur.includes(e as any) ? cur.filter(x => x !== e) : [...cur, e as any]}});
                               }} className={`w-7 h-7 rounded-lg text-[10px] font-black ${selectedChar.elemental?.yinGroup?.includes(e as any) ? 'bg-blue-500 text-white' : 'bg-white/5 opacity-30'}`}>{e}</button>
                            ))}
                        </div>
                        <TextArea label="Biography" className="text-[9px]" value={selectedChar.backgroundText || ''} onChange={v => updateChar({backgroundText: v})} />
                      </div>
                   </div>
                </section>

                <Card className="p-2">
                   <div className="flex justify-between items-center px-1 mb-2">
                      <h3 className="text-[9px] font-black text-blue-500 uppercase tracking-widest">Capabilities Matrix</h3>
                      <Button variant="ghost" onClick={() => setIsManageStatsOpen(true)} className="h-6 px-2 text-[7px] border border-blue-500/20 text-blue-400">+ MANAGE SCHEMA</Button>
                   </div>
                   <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-1.5 max-h-60 overflow-y-auto scroll-container pr-1">
                      {story.attributeDefinitions.map((attr) => (
                        <CapabilityRow 
                          key={attr.key} 
                          label={attr.key} 
                          value={selectedChar.capabilities[attr.key] ?? 0} 
                          onChange={(v) => updateChar({capabilities: {...selectedChar.capabilities, [attr.key]: v}})} 
                        />
                      ))}
                   </div>
                </Card>
              </div>
            ) : <p className="text-[9px] italic text-[var(--text-dim)] p-10 text-center uppercase font-black">Select manifest</p>}
          </div>
        }
        bottomMain={
          <MonitorCore title="Soul Data Terminal (v0.7 Dynamic Stats)" isEmpty={!selectedChar}>
            {selectedChar && (
              <div className="w-full h-full flex flex-col md:flex-row gap-3 p-1.5 md:p-3 animate-in fade-in overflow-y-auto overflow-x-hidden scroll-container">
                <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-3">
                   <div className="lg:col-span-7 flex flex-col gap-2.5">
                      <div className="flex justify-between items-center bg-white/5 p-2 rounded-2xl border border-white/5">
                         <div>
                            <h2 className="text-xl font-black text-[var(--text)] tracking-tighter uppercase leading-none">{selectedChar.name}</h2>
                            <div className="text-[8px] text-blue-500 font-black tracking-[0.2em] mt-1 uppercase">{selectedChar.className}</div>
                         </div>
                         <div className="flex gap-1.5">
                            <div className="bg-red-600/10 px-2 py-1 rounded-lg border border-red-500/10 text-center"><span className="text-[9px] font-black text-white">{selectedChar.vitals?.hp || 0} <span className="text-[6px] text-red-500">HP</span></span></div>
                            <div className="bg-emerald-600/10 px-2 py-1 rounded-lg border border-emerald-500/10 text-center"><span className="text-[9px] font-black text-white">{selectedChar.vitals?.en || 0} <span className="text-[6px] text-emerald-500">EN</span></span></div>
                         </div>
                      </div>

                      <div className="w3-card-inset bg-black/40 p-2 border border-white/5 rounded-2xl">
                         <div className="text-[7px] font-black text-gray-600 uppercase tracking-widest px-1 mb-2">Attribute Grid</div>
                         <div className="grid grid-cols-4 md:grid-cols-5 gap-1.5">
                            {story.attributeDefinitions.map(attr => (
                               <div key={attr.key} className="flex flex-col bg-white/5 p-1 rounded border border-white/5">
                                  <span className="text-[6px] font-black text-gray-500 uppercase">{attr.key}</span>
                                  <span className="text-[10px] font-black text-blue-400">{selectedChar.capabilities[attr.key] || 0}</span>
                               </div>
                            ))}
                         </div>
                      </div>

                      <div className="w3-card-inset h-8 bg-emerald-600/5 border border-emerald-600/10 rounded-xl flex items-center px-4">
                         <span className="text-[6px] text-gray-500 font-black mr-2 uppercase tracking-tighter shrink-0">Output:</span>
                         <span className="text-[9px] font-black text-emerald-400 uppercase tracking-widest truncate">{selectedChar.logicSlots?.totalResult || '>> READY'}</span>
                      </div>
                   </div>

                   <div className="lg:col-span-5 flex flex-col gap-2.5">
                      <div className="flex gap-2.5 h-24 shrink-0">
                         <div className="w-24 h-24 bg-[var(--surface-2)] rounded-[32px] border-2 border-white/5 relative overflow-hidden shrink-0 shadow-lg group">
                            {selectedChar.portraitAssetId ? (
                               <img src={story.assets[selectedChar.portraitAssetId]?.dataUrl} className="w-full h-full object-cover p-1" />
                            ) : <span className="absolute inset-0 flex items-center justify-center text-xl opacity-10">👤</span>}
                            <input type="file" className="absolute inset-0 opacity-0 cursor-pointer" onChange={handlePortrait} accept="image/*" />
                         </div>
                         <div className="flex-1 w3-card-inset bg-white/5 p-2 rounded-2xl border border-white/5 flex flex-col gap-1 overflow-hidden">
                            <span className="text-[7px] font-black text-gray-500 uppercase tracking-widest">History</span>
                            <p className="text-[9px] leading-tight text-gray-400 font-medium italic overflow-y-auto scroll-container">
                               {selectedChar.backgroundText || "Awaiting registry data..."}
                            </p>
                         </div>
                      </div>

                      <div className="w3-card-inset bg-gradient-to-br from-blue-900/30 to-black p-3 rounded-[32px] border border-blue-500/20 flex flex-col gap-1.5 flex-1 shadow-xl">
                         <div className="flex items-center gap-2">
                            <div className="w-6 h-6 rounded-lg bg-blue-600 flex items-center justify-center shadow-lg text-[10px]">⚡</div>
                            <h4 className="text-[11px] font-black text-white uppercase tracking-tighter truncate">{selectedChar.innateSkill?.name || 'MASTER_SKILL'}</h4>
                         </div>
                         <p className="text-[9px] text-blue-400/80 font-medium leading-tight italic line-clamp-3">
                            "{selectedChar.innateSkill?.description || 'No description found.'}"
                         </p>
                      </div>
                   </div>
                </div>
              </div>
            )}
          </MonitorCore>
        }
      />

      <Modal isOpen={isManageStatsOpen} title="Manage Global Attributes" onClose={() => setIsManageStatsOpen(false)}>
        <div className="flex flex-col gap-4 py-2 scroll-container max-h-[60vh] overflow-y-auto">
          <p className="text-[10px] text-gray-400 italic mb-2">กำหนดชื่อสถานะที่ใช้ในทั้งโปรเจกต์ที่นี่ครับ ตัวแปรเหล่านี้จะปรากฏในตัวละครทุกตัว</p>
          {story.attributeDefinitions.map((attr, idx) => (
            <div key={idx} className="flex gap-2 items-end bg-white/5 p-3 rounded-2xl border border-white/5">
              <Input label="ตัวย่อ (KEY)" value={attr.key} className="flex-[2]" onChange={v => updateAttribute(idx, {...attr, key: v.toUpperCase().replace(/\s/g, '')})} />
              <Input label="ชื่อเต็ม (NAME)" value={attr.label} className="flex-[3]" onChange={v => updateAttribute(idx, {...attr, label: v})} />
              <Input label="ค่าเริ่มต้น" type="number" value={attr.defaultValue} className="flex-[1.5]" onChange={v => updateAttribute(idx, {...attr, defaultValue: parseInt(v) || 0})} />
              <Button variant="danger" className="h-10 w-10 px-0" onClick={() => deleteAttribute(idx)}>✕</Button>
            </div>
          ))}
          <Button variant="accent" onClick={addAttribute} className="h-12 mt-4 font-black uppercase tracking-widest text-[10px] shadow-lg">+ ADD NEW STATUS PARAMETER</Button>
        </div>
      </Modal>
    </>
  );
};
