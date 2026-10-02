
import React, { useState, useMemo } from 'react';
import { StoryPack, EventPack, ActionDef, OutcomeDef, Asset } from '../../types';
import { Button } from '../../ui/components/Button';
import { Input, TextArea, Select } from '../../ui/components/Input';
import { MonitorCore } from '../../ui/components/MonitorCore';
import { SplitLayout60_40 } from '../../ui/layout/SplitLayout60_40';
import { generateId } from '../../core/utils';
import { Card } from '../../ui/components/Card';

interface EventsTabProps {
  story: StoryPack;
  onChange: (updated: StoryPack) => void;
  toolActions?: any;
}

export const EventsTab: React.FC<EventsTabProps> = ({ story, onChange, toolActions }) => {
  const [selectedId, setSelectedId] = useState<string | null>(story.events[0]?.id || null);

  const selectedEvent = useMemo(() => 
    story.events.find(e => e.id === selectedId)
  , [story.events, selectedId]);

  const addEvent = () => {
    const id = generateId('evt');
    const newEv: EventPack = {
      id,
      eventId: id,
      name: 'New Nexus Event',
      eventType: 'Special',
      areaRule: '',
      trigger: { when: 'OnInteract', condition: '', priority: 1, cooldown: 0 },
      actions: [],
      outcomes: [],
      inspector: { selectedActionId: null, executionLog: [] }
    };
    onChange({ ...story, events: [...story.events, newEv] });
    setSelectedId(id);
  };

  const updateEvent = (updated: Partial<EventPack>) => {
    if (!selectedEvent) return;
    onChange({ ...story, events: story.events.map(e => e.id === selectedEvent.id ? { ...e, ...updated } : e) });
  };

  const handleIconUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !selectedEvent) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      const dataUrl = ev.target?.result as string;
      const assetId = generateId('ast');
      const newAsset: Asset = { id: assetId, name: file.name, dataUrl };
      onChange({
        ...story,
        assets: { ...story.assets, [assetId]: newAsset },
        events: story.events.map(evnt => evnt.id === selectedEvent.id ? { ...evnt, iconAssetId: assetId } : evnt)
      });
    };
    reader.readAsDataURL(file);
  };

  const boardOptions = [{label: '--- No Board ---', value: ''}, ...story.boards.map(b => ({ label: b.title, value: b.boardId }))];

  return (
    <SplitLayout60_40
      toolActions={toolActions}
      topLeft={
        /* (2) รายชื่อ Event ฝั่งซ้าย */
        <div className="flex flex-col h-full bg-gray-50/10">
          <div className="p-3 border-b border-[var(--border)]">
            <Button id="tab-primary-add" variant="accent" className="w-full h-10 text-[9px]" onClick={addEvent}>+ NEW NEXUS EVENT</Button>
          </div>
          <div className="flex-1 overflow-y-auto scroll-container">
            {story.events.map((e, idx) => (
              <button 
                key={e.id} onClick={() => setSelectedId(e.id)}
                className={`w-full p-4 text-left border-b border-[var(--border)] transition-all clickable flex gap-4 items-center ${selectedId === e.id ? 'bg-[var(--surface)] border-l-4 border-l-blue-600 shadow-sm' : 'hover:bg-gray-200/5'}`}
              >
                <span className="text-[10px] font-black text-gray-500 opacity-30">{String(idx + 1).padStart(2, '0')}.</span>
                <div className="flex-1 truncate">
                  <div className="text-[11px] font-black text-[var(--text)] uppercase truncate">{e.name}</div>
                  <div className="text-[7px] text-[var(--text-dim)] uppercase font-bold tracking-[0.2em] mt-0.5">{e.trigger.when}</div>
                </div>
              </button>
            ))}
          </div>
        </div>
      }
      topRight={
        <div className="p-3 md:p-6 flex flex-col gap-6 overflow-y-auto h-full bg-[var(--surface)] scroll-container pb-32">
          {selectedEvent ? (
            <div className="flex flex-col gap-6 animate-in fade-in">
              {/* (1) Header Section: Icon (Custom) + 2-Tier Name/Type */}
              <Card className="p-5 flex flex-col gap-5 w-full bg-[var(--surface-2)] border-blue-500/10 shadow-xl">
                <div className="flex flex-col md:flex-row gap-6 items-start">
                  {/* Custom Icon Box */}
                  <div className="w-24 h-24 md:w-28 md:h-28 w3-card-inset flex items-center justify-center relative overflow-hidden shrink-0 border-2 border-white/5 bg-black/20 group cursor-pointer">
                    {selectedEvent.iconAssetId ? (
                      <img src={story.assets[selectedEvent.iconAssetId]?.dataUrl} className="w-full h-full object-cover p-1" />
                    ) : (
                      <span className="text-4xl opacity-10 font-black group-hover:opacity-30 transition-opacity">⚡</span>
                    )}
                    <input type="file" className="absolute inset-0 opacity-0 cursor-pointer" onChange={handleIconUpload} accept="image/*" />
                    <div className="absolute inset-0 bg-blue-600/0 group-hover:bg-blue-600/10 transition-colors pointer-events-none"></div>
                  </div>
                  
                  {/* Name/Type 2-Tier Fields */}
                  <div className="flex-1 flex flex-col gap-4 w-full">
                    <div className="w-full">
                      <Input label="Event Identity (Name)" value={selectedEvent.name} onChange={v => updateEvent({name: v})} className="text-lg" />
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <Select label="Execution Type" value={selectedEvent.eventType} options={[{label:'Special',value:'Special'},{label:'Random',value:'Random'},{label:'Story/Main',value:'System'}]} onChange={v => updateEvent({eventType: v})} />
                      <div className="flex items-end h-full">
                         <Button variant="danger" className="h-10 w-full text-[9px]" onClick={() => { if (confirm('Purge this signal?')) { onChange({...story, events: story.events.filter(e => e.id !== selectedId)}); setSelectedId(null); } }}>PURGE SIGNAL</Button>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>

              {/* (6) Rule of Area / Spatial Link */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card className="p-4 flex flex-col gap-3 bg-blue-600/5 border-blue-500/20 h-full">
                   <h3 className="text-[9px] font-black text-blue-500 uppercase tracking-[0.3em] px-1">Rule of Area / พิกัดลักษณะการทำงาน</h3>
                   <TextArea 
                     value={selectedEvent.areaRule} 
                     onChange={v => updateEvent({areaRule: v})} 
                     placeholder="ระบุกฎพื้นที่หรือลักษณะการทำงานเฉพาะของพิกัดนี้..."
                     className="text-[11px] flex-1 min-h-[100px]"
                   />
                </Card>

                {/* Spatial Anchor (New Section to solve "where to refer") */}
                <Card className="p-4 flex flex-col gap-3 bg-emerald-600/5 border-emerald-500/20 h-full">
                   <h3 className="text-[9px] font-black text-emerald-500 uppercase tracking-[0.3em] px-1">Spatial Anchor / การอ้างอิงพิกัดพื้นที่</h3>
                   <div className="flex flex-col gap-4">
                      <Select label="Target Board" value={selectedEvent.targetBoardId || ''} options={boardOptions} onChange={v => updateEvent({targetBoardId: v})} />
                      <div className="grid grid-cols-2 gap-3">
                         <Input label="Coordinate X" type="number" value={selectedEvent.targetX || 0} onChange={v => updateEvent({targetX: parseInt(v) || 0})} />
                         <Input label="Coordinate Y" type="number" value={selectedEvent.targetY || 0} onChange={v => updateEvent({targetY: parseInt(v) || 0})} />
                      </div>
                      <p className="text-[8px] text-gray-500 italic mt-auto">ระบุบอร์ดและพิกัดที่ต้องการให้เหตุการณ์นี้เกิดขึ้นบนแผนที่ครับ</p>
                   </div>
                </Card>
              </div>

              {/* (3) Middle Section: Workflow Pipeline */}
              <div className="flex flex-col gap-4">
                <div className="flex justify-between items-center px-1">
                  <h3 className="text-[10px] font-black text-gray-400 uppercase tracking-[0.4em]">Workflow Pipeline (Logic Connections)</h3>
                  <Button variant="ghost" className="text-[9px] h-7 px-4 border border-white/10" onClick={() => {
                    const na: ActionDef = { id: generateId('act'), actionType: 'Message', target: 'Self', payload: '' };
                    updateEvent({actions: [...selectedEvent.actions, na]});
                  }}>+ ADD PIPELINE STEP</Button>
                </div>
                
                <div className="flex flex-col gap-4 relative p-2">
                   {selectedEvent.actions.map((act, i) => (
                    <div key={act.id} className="flex gap-4 items-start animate-in slide-in-from-left-4" style={{ animationDelay: `${i * 100}ms` }}>
                       <div className="w-16 h-16 shrink-0 w3-card-inset flex items-center justify-center text-xl bg-black border-white/5 relative z-10 shadow-lg">
                          <span className="font-black text-blue-500 opacity-40 text-sm">#{i + 1}</span>
                       </div>
                       <Card className="flex-1 p-4 bg-white/5 border-white/5 grid grid-cols-1 md:grid-cols-3 gap-3 relative">
                          <Input label="Process" value={act.actionType} onChange={v => {
                            const na = [...selectedEvent.actions]; na[i].actionType = v; updateEvent({actions: na});
                          }} />
                          <Input label="Target" value={act.target} onChange={v => {
                            const na = [...selectedEvent.actions]; na[i].target = v; updateEvent({actions: na});
                          }} />
                          <Input label="Data/Log" value={act.payload} onChange={v => {
                            const na = [...selectedEvent.actions]; na[i].payload = v; updateEvent({actions: na});
                          }} />
                          <button 
                            className="absolute -top-1 -right-1 w-5 h-5 bg-red-600 text-white rounded-full flex items-center justify-center text-[10px] shadow-lg opacity-0 group-hover:opacity-100 transition-opacity"
                            onClick={() => updateEvent({actions: selectedEvent.actions.filter(a => a.id !== act.id)})}
                          >✕</button>
                       </Card>
                    </div>
                   ))}

                   {selectedEvent.actions.length === 0 && (
                     <div className="py-20 text-center opacity-10 border-2 border-dashed border-white/5 rounded-[40px]">
                        <p className="text-[12px] font-black uppercase tracking-[0.5em]">No logical steps defined</p>
                     </div>
                   )}
                </div>
              </div>
            </div>
          ) : <div className="p-20 text-center text-[11px] italic opacity-20 uppercase font-black tracking-widest">Select nexus signal from registry.</div>}
        </div>
      }
      bottomMain={
        /* (4) Event Monitor: Terminal Output */
        <MonitorCore 
          title="NEXUS EVENT MONITOR TERMINAL" 
          isEmpty={!selectedEvent} 
        >
          {selectedEvent && (
            <div className="max-w-4xl mx-auto flex flex-col gap-6 animate-in fade-in duration-700 h-full p-2">
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white/5 p-4 rounded-3xl border border-white/10">
                 <div className="flex items-center gap-4">
                   <div className="w-12 h-12 bg-blue-600/20 rounded-xl flex items-center justify-center shrink-0 border border-blue-600/20 overflow-hidden">
                      {selectedEvent.iconAssetId ? (
                        <img src={story.assets[selectedEvent.iconAssetId]?.dataUrl} className="w-full h-full object-cover p-1" />
                      ) : <span className="text-xl">⚡</span>}
                   </div>
                   <div>
                      <h1 className="text-2xl font-black text-white tracking-tighter uppercase">{selectedEvent.name}</h1>
                      <div className="flex gap-3 mt-1">
                        <span className="px-3 py-0.5 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full text-[8px] font-black uppercase tracking-widest">SPATIAL: {selectedEvent.targetBoardId ? 'ANCHORED' : 'FLOATING'}</span>
                        <span className="px-3 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-[8px] font-black uppercase tracking-widest">LOC: {selectedEvent.targetX || 0}, {selectedEvent.targetY || 0}</span>
                      </div>
                   </div>
                 </div>
                 <div className="text-right flex flex-col items-end">
                    <span className="text-[7px] text-gray-500 font-black uppercase tracking-[0.4em] mb-1">Local Area Rule</span>
                    <p className="text-[9px] text-blue-500/80 font-medium italic max-w-xs truncate">{selectedEvent.areaRule || "Global parameters applied"}</p>
                 </div>
              </div>

              <div className="flex-1 p-6 w3-card-inset bg-[#050505] text-emerald-400 font-mono text-[10px] md:text-[11px] rounded-[32px] shadow-inner border border-white/5 overflow-y-auto scroll-container">
                <div className="mb-4 opacity-40 border-b border-emerald-900/30 pb-2 uppercase tracking-widest">EVENT_PIPELINE_INIT_V0.7</div>
                <div className="flex flex-col gap-1.5">
                  {selectedEvent.actions.length > 0 ? selectedEvent.actions.map((act, i) => (
                    <div key={i} className="flex gap-4">
                      <span className="text-emerald-900 shrink-0">[{String(i+1).padStart(2, '0')}]</span>
                      <span className="text-blue-400">&gt; EXECUTE_{act.actionType.toUpperCase()}</span>
                      <span className="text-gray-600">TARGET:</span>
                      <span className="text-white">"{act.target}"</span>
                      <span className="text-gray-600">DATA:</span>
                      <span className="text-emerald-500/70">"{act.payload}"</span>
                    </div>
                  )) : <div className="opacity-20">&gt; NO_LOGICAL_STEPS_QUEUED</div>}
                </div>
                <div className="animate-pulse mt-8 flex items-center gap-3">
                   <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full"></div>
                   <span className="opacity-60">SYSTEM_READY: LISTENING FOR TRIGGER_SIGNAL...</span>
                </div>
              </div>
            </div>
          )}
        </MonitorCore>
      }
    />
  );
};
