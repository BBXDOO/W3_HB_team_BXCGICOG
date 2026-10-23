import React from 'react';
import { LocationPack, TriggerPack, LootPack } from '../../types';
import { Button } from '../../ui/components/Button';
import { Input, TextArea, Select } from '../../ui/components/Input';
import { Card } from '../../ui/components/Card';
import { generateId } from '../../core/utils';

interface LocationSheetProps {
  location: LocationPack;
  onChange: (updated: LocationPack) => void;
  onDelete: () => void;
}

export const LocationSheet: React.FC<LocationSheetProps> = ({ location, onChange, onDelete }) => {
  const updateField = (path: string, val: any) => {
    const updated = { ...location };
    if (path.includes('.')) {
      const [p1, p2] = path.split('.');
      (updated as any)[p1][p2] = val;
    } else {
      (updated as any)[path] = val;
    }
    onChange(updated);
  };

  const addTrigger = () => {
    const newTrig: TriggerPack = { id: generateId('tr'), when: 'enter', condition: '', effect: '' };
    onChange({ ...location, triggers: [...location.triggers, newTrig] });
  };

  const addLoot = () => {
    const newLoot: LootPack = { id: generateId('lt'), itemRefId: '', chance: 50, amount: 1 };
    onChange({ ...location, loot: [...location.loot, newLoot] });
  };

  return (
    <div className="flex flex-col gap-4 p-3 md:p-6 w-full">
      {/* Header - Fixed Overlap Bug with more compact structure */}
      <Card className="p-4 flex flex-col gap-4 w-full">
        <div className="flex flex-col md:flex-row gap-4 items-start md:items-center">
          <div className="w-14 h-14 md:w-20 md:h-20 w3-card-inset flex-shrink-0 flex items-center justify-center text-2xl md:text-4xl">
            {location.imageAssetId ? '🖼️' : '🏰'}
          </div>
          <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-3 w-full">
            <Input label="Label" value={location.title} onChange={(v) => updateField('title', v)} />
            <Input label="Zone" value={location.zone || ''} onChange={(v) => updateField('zone', v)} />
          </div>
          <div className="w-full md:w-auto flex justify-end shrink-0">
            <Button variant="danger" className="w-full md:w-auto h-10 px-6 text-[9px]" onClick={onDelete}>PURGE</Button>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 w-full">
        {/* Left: Profile */}
        <div className="lg:col-span-4 flex flex-col gap-4">
          <h3 className="text-[9px] font-black opacity-50 uppercase tracking-[0.2em] px-1">Environmental Profile</h3>
          <Card className="p-4 flex flex-col gap-5">
            <Select 
              label="Archetype" 
              value={location.areaProfile.type || 'Outdoor'} 
              options={[
                {label: 'Indoor', value: 'Indoor'},
                {label: 'Outdoor', value: 'Outdoor'},
                {label: 'Dungeon', value: 'Dungeon'},
                {label: 'City', value: 'City'}
              ]}
              onChange={(v) => updateField('areaProfile.type', v)}
            />
            <div className="grid grid-cols-2 gap-3">
               <Input label="Threat" type="number" value={location.areaProfile.threat || 0} onChange={(v) => updateField('areaProfile.threat', parseInt(v))} />
               <Select 
                label="Clearance" 
                value={location.areaProfile.access || 'Public'} 
                options={[{label: 'Public', value: 'Public'}, {label: 'Restricted', value: 'Restricted'}]}
                onChange={(v) => updateField('areaProfile.access', v)}
              />
            </div>
            <Select 
              label="Temporal" 
              value={location.areaProfile.timeRule || 'Any'} 
              options={[{label: 'Any', value: 'Any'}, {label: 'Day Cycle', value: 'Day'}, {label: 'Night Cycle', value: 'Night'}]}
              onChange={(v) => updateField('areaProfile.timeRule', v)}
            />
            <TextArea label="Overview" className="text-[11px]" value={location.description || ''} onChange={(v) => updateField('description', v)} />
          </Card>
        </div>

        {/* Middle: Triggers & Loot */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          <div className="flex flex-col gap-3">
            <div className="flex justify-between items-center px-1">
              <h3 className="text-[9px] font-black opacity-50 uppercase tracking-[0.2em]">Active Triggers</h3>
              <Button variant="ghost" className="text-[9px] py-1 font-black" onClick={addTrigger}>+ NEW ARRAY</Button>
            </div>
            <Card className="p-0 overflow-hidden border-gray-100">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-[10px]">
                  <thead className="bg-gray-50/50 uppercase opacity-50 font-black tracking-widest border-b border-gray-200">
                    <tr>
                      <th className="p-3">Hook</th>
                      <th className="p-3">Cond</th>
                      <th className="p-3">Exec</th>
                      <th className="p-3 w-8"></th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100/10">
                    {location.triggers.map((trig, idx) => (
                      <tr key={trig.id} className="hover:bg-gray-50/5 transition-colors">
                        <td className="p-2">
                          <select 
                            className="bg-transparent outline-none w-full font-bold clickable"
                            value={trig.when}
                            onChange={(e) => {
                              const nt = [...location.triggers];
                              nt[idx].when = e.target.value as any;
                              updateField('triggers', nt);
                            }}
                          >
                            <option value="enter">Entry</option>
                            <option value="click">Click</option>
                          </select>
                        </td>
                        <td className="p-2">
                          <input 
                            className="bg-transparent outline-none w-full font-medium clickable" 
                            value={trig.condition} 
                            placeholder="..."
                            onChange={(e) => {
                              const nt = [...location.triggers];
                              nt[idx].condition = e.target.value;
                              updateField('triggers', nt);
                            }}
                          />
                        </td>
                        <td className="p-2">
                          <input 
                            className="bg-transparent outline-none w-full font-medium clickable" 
                            value={trig.effect} 
                            placeholder="..."
                            onChange={(e) => {
                              const nt = [...location.triggers];
                              nt[idx].effect = e.target.value;
                              updateField('triggers', nt);
                            }}
                          />
                        </td>
                        <td className="p-2 text-right">
                          <Button variant="ghost" className="px-1 text-red-500 clickable" onClick={() => {
                            updateField('triggers', location.triggers.filter(t => t.id !== trig.id));
                          }}>✕</Button>
                        </td>
                      </tr>
                    ))}
                    {location.triggers.length === 0 && (
                      <tr><td colSpan={4} className="p-8 text-center opacity-30 italic font-medium uppercase tracking-widest">Protocol Null</td></tr>
                    )}
                  </tbody>
                </table>
              </div>
            </Card>
          </div>

          <div className="flex flex-col gap-3">
            <div className="flex justify-between items-center px-1">
              <h3 className="text-[9px] font-black opacity-50 uppercase tracking-[0.2em]">Loot Distribution</h3>
              <Button variant="ghost" className="text-[9px] py-1 font-black" onClick={addLoot}>+ NEW SLOT</Button>
            </div>
            <Card className="p-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
               {location.loot.map((loot, idx) => (
                 <div key={loot.id} className="w3-card-inset p-3 flex gap-3 items-center">
                   <div className="flex-1 flex flex-col gap-2">
                      <Input value={loot.itemRefId} className="text-[10px]" onChange={(v) => {
                        const nl = [...location.loot]; nl[idx].itemRefId = v; updateField('loot', nl);
                      }} placeholder="Item ID..." />
                      <div className="flex gap-2">
                        <Input type="number" label="%" value={loot.chance} onChange={(v) => {
                          const nl = [...location.loot]; nl[idx].chance = parseInt(v); updateField('loot', nl);
                        }} />
                        <Input type="number" label="Qty" value={loot.amount} onChange={(v) => {
                          const nl = [...location.loot]; nl[idx].amount = parseInt(v); updateField('loot', nl);
                        }} />
                      </div>
                   </div>
                   <Button variant="ghost" className="text-red-500 px-1 self-start clickable" onClick={() => {
                     updateField('loot', location.loot.filter(l => l.id !== loot.id));
                   }}>✕</Button>
                 </div>
               ))}
               {location.loot.length === 0 && (
                 <div className="col-span-full py-6 text-center opacity-30 font-black uppercase tracking-widest text-[9px]">Manifest Null</div>
               )}
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};