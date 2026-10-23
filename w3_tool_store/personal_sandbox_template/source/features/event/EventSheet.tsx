
import React, { useState } from 'react';
import { EventPack, ActionDef, OutcomeDef } from '../../types';
import { Card } from '../../ui/components/Card';
import { Button } from '../../ui/components/Button';
import { Input, TextArea, Select } from '../../ui/components/Input';
import { generateId } from '../../core/utils';

interface EventSheetProps {
  event: EventPack;
  onChange: (updated: EventPack) => void;
  onDelete: () => void;
}

export const EventSheet: React.FC<EventSheetProps> = ({ event, onChange, onDelete }) => {
  const [activeTab, setActiveTab] = useState<'actions' | 'outcomes'>('actions');

  const updateField = (path: string, val: any) => {
    const updated = { ...event };
    if (path.includes('.')) {
      const parts = path.split('.');
      let obj = updated as any;
      for (let i = 0; i < parts.length - 1; i++) obj = obj[parts[i]];
      obj[parts[parts.length - 1]] = val;
    } else {
      (updated as any)[path] = val;
    }
    onChange(updated);
  };

  const addAction = () => {
    const na: ActionDef = { id: generateId('ac'), actionType: 'Message', target: 'Self', payload: '' };
    onChange({ ...event, actions: [...event.actions, na] });
  };

  const addOutcome = () => {
    const no: OutcomeDef = { id: generateId('out'), condition: '', result: '' };
    onChange({ ...event, outcomes: [...event.outcomes, no] });
  };

  const selectedAction = event.actions.find(a => a.id === event.inspector.selectedActionId);

  return (
    <div className="p-4 flex flex-col gap-6 max-w-7xl mx-auto h-full overflow-y-auto">
      {/* A: Header */}
      <Card className="p-6 flex flex-col lg:flex-row gap-6 items-center">
        <div className="w-20 h-20 w3-card-inset flex items-center justify-center text-4xl">⚡</div>
        <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-4 w-full">
          <Input label="Event Name" value={event.name} onChange={(v) => updateField('name', v)} />
          <Input label="Event ID" value={event.eventId} onChange={(v) => updateField('eventId', v)} />
          <Select 
            label="Event Type" 
            value={event.eventType} 
            options={[
              {label: 'Special', value: 'Special'},
              {label: 'Random', value: 'Random'},
              {label: 'Quest', value: 'Quest'},
              {label: 'System', value: 'System'}
            ]}
            onChange={(v) => updateField('eventType', v)}
          />
        </div>
        <div className="flex gap-2">
          <Button variant="accent" onClick={() => {}}>SAVE</Button>
          <Button variant="danger" onClick={onDelete}>DELETE</Button>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1">
        {/* B: Trigger Panel (Left) */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest px-2">Trigger</h3>
          <Card className="p-4 flex flex-col gap-4">
            <Select 
              label="When" 
              value={event.trigger.when} 
              options={[
                {label: 'On Enter Cell', value: 'OnEnter'},
                {label: 'On Exit Cell', value: 'OnExit'},
                {label: 'On Interaction', value: 'OnInteract'},
                {label: 'Timed / Turn', value: 'OnTime'},
                {label: 'On Use Item', value: 'OnUseItem'}
              ]}
              onChange={(v) => updateField('trigger.when', v)}
            />
            <TextArea label="Condition String" value={event.trigger.condition} onChange={(v) => updateField('trigger.condition', v)} placeholder="e.g. HP > 50" />
            <div className="grid grid-cols-2 gap-2">
              <Input label="Priority" type="number" value={event.trigger.priority} onChange={(v) => updateField('trigger.priority', parseInt(v))} />
              <Input label="Cooldown" type="number" value={event.trigger.cooldown} onChange={(v) => updateField('trigger.cooldown', parseInt(v))} />
            </div>
          </Card>
        </div>

        {/* C & D: Workflow (Middle/Center) */}
        <div className="lg:col-span-8 flex flex-col gap-4">
          <div className="flex gap-2 p-1 w3-card-inset rounded-xl">
            <button 
              onClick={() => setActiveTab('actions')}
              className={`flex-1 py-2 text-xs font-bold uppercase rounded-lg transition-all ${activeTab === 'actions' ? 'w3-card text-amber-500' : 'text-gray-500'}`}
            >
              Workflow Actions ({event.actions.length})
            </button>
            <button 
              onClick={() => setActiveTab('outcomes')}
              className={`flex-1 py-2 text-xs font-bold uppercase rounded-lg transition-all ${activeTab === 'outcomes' ? 'w3-card text-amber-500' : 'text-gray-500'}`}
            >
              Logical Outcomes ({event.outcomes.length})
            </button>
          </div>

          <Card className="flex-1 p-0 overflow-hidden flex flex-col">
            {activeTab === 'actions' ? (
              <div className="flex flex-col h-full">
                <div className="flex justify-between items-center p-3 bg-white/5">
                   <span className="text-[10px] text-gray-500 uppercase font-bold tracking-tighter">Action Steps</span>
                   <Button variant="ghost" className="text-[10px] py-1" onClick={addAction}>+ ADD STEP</Button>
                </div>
                <div className="overflow-y-auto flex-1">
                   <table className="w-full text-[11px] text-left">
                     <thead className="bg-white/5 uppercase text-gray-500 border-b border-gray-800">
                       <tr>
                         <th className="p-3">Type</th>
                         <th className="p-3">Target</th>
                         <th className="p-3">Payload</th>
                         <th className="p-3 w-10"></th>
                       </tr>
                     </thead>
                     <tbody className="divide-y divide-gray-800">
                       {event.actions.map((act, idx) => (
                         <tr 
                          key={act.id} 
                          onClick={() => updateField('inspector.selectedActionId', act.id)}
                          className={`hover:bg-white/5 cursor-pointer transition-all ${event.inspector.selectedActionId === act.id ? 'bg-amber-500/5' : ''}`}
                         >
                           <td className="p-2">
                             <input className="bg-transparent w-full outline-none focus:text-amber-500" value={act.actionType} onChange={(e) => {
                               const na = [...event.actions]; na[idx].actionType = e.target.value; updateField('actions', na);
                             }} />
                           </td>
                           <td className="p-2">
                             <input className="bg-transparent w-full outline-none focus:text-amber-500" value={act.target} onChange={(e) => {
                               const na = [...event.actions]; na[idx].target = e.target.value; updateField('actions', na);
                             }} />
                           </td>
                           <td className="p-2">
                             <input className="bg-transparent w-full outline-none focus:text-amber-500" value={act.payload} onChange={(e) => {
                               const na = [...event.actions]; na[idx].payload = e.target.value; updateField('actions', na);
                             }} />
                           </td>
                           <td className="p-2">
                             <Button variant="ghost" className="text-red-500 p-1" onClick={(e) => {
                               e.stopPropagation();
                               updateField('actions', event.actions.filter(a => a.id !== act.id));
                               if (event.inspector.selectedActionId === act.id) updateField('inspector.selectedActionId', null);
                             }}>✕</Button>
                           </td>
                         </tr>
                       ))}
                       {event.actions.length === 0 && <tr><td colSpan={4} className="p-10 text-center text-gray-500 italic uppercase text-[10px] tracking-widest">No workflow steps defined.</td></tr>}
                     </tbody>
                   </table>
                </div>
              </div>
            ) : (
              <div className="flex flex-col h-full p-4">
                <div className="flex justify-between items-center mb-4">
                   <span className="text-[10px] text-gray-500 uppercase font-bold tracking-tighter">Branching Logic</span>
                   <Button variant="ghost" className="text-[10px] py-1" onClick={addOutcome}>+ ADD OUTCOME</Button>
                </div>
                <div className="flex flex-col gap-2 overflow-y-auto flex-1">
                   {event.outcomes.map((out, idx) => (
                     <div key={out.id} className="w3-card-inset p-3 flex gap-4 items-end animate-in fade-in">
                        <div className="flex-1 grid grid-cols-2 gap-4">
                          <Input label="IF CONDITION" value={out.condition} onChange={(v) => {
                            const no = [...event.outcomes]; no[idx].condition = v; updateField('outcomes', no);
                          }} placeholder="e.g. dice > 10" />
                          <Input label="THEN RESULT" value={out.result} onChange={(v) => {
                            const no = [...event.outcomes]; no[idx].result = v; updateField('outcomes', no);
                          }} placeholder="e.g. +HP 10" />
                        </div>
                        <Button variant="ghost" className="text-red-500 h-10 w-10 p-0" onClick={() => {
                          updateField('outcomes', event.outcomes.filter(o => o.id !== out.id));
                        }}>✕</Button>
                     </div>
                   ))}
                   {event.outcomes.length === 0 && <div className="text-center text-xs text-gray-600 py-10 italic">No logic outcomes defined yet.</div>}
                </div>
              </div>
            )}
          </Card>
        </div>
      </div>

      {/* E: Inspector / Simulation (Bottom) */}
      <Card className="p-4 bg-black/20 flex flex-col gap-2 mt-auto">
        <div className="flex justify-between items-center">
          <h4 className="text-[10px] font-bold text-amber-500/70 uppercase tracking-widest">Simulation Log / Debugger</h4>
          <Button variant="ghost" className="text-[10px] py-0 h-6 px-2 hover:bg-amber-500/10 text-amber-500/50">▶ RUN SIMULATION</Button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="w3-card-inset p-3 text-xs font-mono text-gray-400 min-h-[80px]">
             {selectedAction ? (
               <div className="flex flex-col gap-1">
                 <p className="text-amber-500/50 underline mb-1">SELECTED STEP: {selectedAction.id}</p>
                 <p className="flex justify-between"><span className="text-gray-500 uppercase">CMD:</span> {selectedAction.actionType}</p>
                 <p className="flex justify-between"><span className="text-gray-500 uppercase">TARGET:</span> {selectedAction.target}</p>
                 <p className="flex justify-between"><span className="text-gray-500 uppercase">DATA:</span> {selectedAction.payload}</p>
               </div>
             ) : (
               <p className="text-gray-600 italic">Select an action step to debug...</p>
             )}
          </div>
          <div className="w3-card-inset p-3 text-[10px] font-mono text-emerald-500/70 overflow-y-auto max-h-[80px]">
             {event.inspector.executionLog.length > 0 ? (
               event.inspector.executionLog.map((log, i) => <div key={i}>[{new Date().toLocaleTimeString()}] {log}</div>)
             ) : (
               <div className="text-gray-600 italic leading-tight">
                 &gt; Logic System Ready.<br/>
                 &gt; Waiting for simulation trigger...
               </div>
             )}
          </div>
        </div>
      </Card>
    </div>
  );
};
