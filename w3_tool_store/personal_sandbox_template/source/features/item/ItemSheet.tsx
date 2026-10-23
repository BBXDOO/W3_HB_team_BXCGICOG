import React, { useState } from 'react';
import { ItemPack, EffectDef } from '../../types';
import { Card } from '../../ui/components/Card';
import { Button } from '../../ui/components/Button';
import { Input, TextArea, Select } from '../../ui/components/Input';
import { generateId } from '../../core/utils';

interface ItemSheetProps {
  item: ItemPack;
  onChange: (updated: ItemPack) => void;
  onDelete: () => void;
}

export const ItemSheet: React.FC<ItemSheetProps> = ({ item, onChange, onDelete }) => {
  const [activeTab, setActiveTab] = useState<'usage' | 'effects' | 'relations'>('usage');

  const updateField = (path: string, val: any) => {
    const updated = { ...item };
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

  const addEffect = () => {
    const newEffect: EffectDef = { id: generateId('eff'), condition: '', effect: '', target: 'User' };
    onChange({ ...item, effects: [...item.effects, newEffect] });
  };

  return (
    <div className="p-3 md:p-6 flex flex-col gap-4 w-full h-full overflow-y-auto">
      {/* A: Header - Optimized like LocationSheet */}
      <Card className="p-4 flex flex-col gap-4 w-full">
        <div className="flex flex-col md:flex-row gap-4 items-start md:items-center">
          <div className="w-14 h-14 md:w-20 md:h-20 w3-card-inset flex items-center justify-center text-2xl md:text-4xl shrink-0">🎒</div>
          <div className="flex-1 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 w-full">
            <Input label="Label" value={item.name} onChange={(v) => updateField('name', v)} />
            <Input label="Asset ID" value={item.itemId} onChange={(v) => updateField('itemId', v)} />
            <Select 
              label="Type" 
              value={item.category} 
              options={[
                {label: 'Consumable', value: 'Consumable'},
                {label: 'Key Item', value: 'KeyItem'},
                {label: 'Weapon', value: 'Weapon'},
                {label: 'Material', value: 'Material'}
              ]}
              onChange={(v) => updateField('category', v)}
            />
            <Select 
              label="Rarity" 
              value={item.rarity} 
              options={[
                {label: 'Common', value: 'Common'},
                {label: 'Rare', value: 'Rare'},
                {label: 'Epic', value: 'Epic'},
                {label: 'Legendary', value: 'Legendary'}
              ]}
              onChange={(v) => updateField('rarity', v)}
            />
          </div>
          <div className="w-full md:w-auto flex justify-end shrink-0">
            <Button variant="danger" className="w-full md:w-auto h-10 px-6 text-[9px]" onClick={onDelete}>PURGE</Button>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 w-full">
        {/* B: Properties Panel (Left) */}
        <div className="lg:col-span-3 flex flex-col gap-3">
          <h3 className="text-[9px] font-black opacity-50 uppercase tracking-[0.2em] px-1">Properties</h3>
          <Card className="p-4 flex flex-col gap-4">
            <div className="flex items-center justify-between p-2 w3-card-inset rounded-lg">
              <span className="text-[10px] font-black uppercase text-gray-400">Stackable</span>
              <input 
                type="checkbox" 
                checked={item.properties.stackable} 
                onChange={(e) => updateField('properties.stackable', e.target.checked)} 
              />
            </div>
            <div className="grid grid-cols-2 gap-2">
              <Input label="Max Stack" type="number" value={item.properties.maxStack} onChange={(v) => updateField('properties.maxStack', parseInt(v))} />
              <Input label="Weight" type="number" value={item.properties.weight} onChange={(v) => updateField('properties.weight', parseFloat(v))} />
            </div>
            <TextArea label="Description" className="text-[10px]" value={item.properties.description} onChange={(v) => updateField('properties.description', v)} />
          </Card>
        </div>

        {/* C: Usage / Effects (Middle) */}
        <div className="lg:col-span-9 flex flex-col gap-3">
          <div className="flex gap-2 p-1 w3-card-inset rounded-xl">
            <button 
              onClick={() => setActiveTab('usage')}
              className={`flex-1 py-1.5 text-[9px] font-black uppercase rounded-lg transition-all ${activeTab === 'usage' ? 'bg-[var(--surface)] text-blue-600 shadow-sm' : 'text-gray-500'}`}
            >
              Usage Logic
            </button>
            <button 
              onClick={() => setActiveTab('effects')}
              className={`flex-1 py-1.5 text-[9px] font-black uppercase rounded-lg transition-all ${activeTab === 'effects' ? 'bg-[var(--surface)] text-blue-600 shadow-sm' : 'text-gray-500'}`}
            >
              Effects ({item.effects.length})
            </button>
          </div>

          <Card className="p-4 min-h-[160px]">
            {activeTab === 'usage' && (
              <div className="flex flex-col gap-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                   <Select 
                    label="Use Type" 
                    value={item.usage.useType} 
                    options={[{label: 'Instant', value: 'Instant'}, {label: 'Equip', value: 'Equip'}, {label: 'Passive', value: 'Passive'}]}
                    onChange={(v) => updateField('usage.useType', v)}
                  />
                  <Input label="Cooldown (Turns)" type="number" value={item.usage.cooldown} onChange={(v) => updateField('usage.cooldown', parseInt(v))} />
                </div>
                <div className="flex items-center justify-between p-3 w3-card-inset rounded-lg">
                  <span className="text-[10px] font-black uppercase text-gray-400">Consume on use</span>
                  <input type="checkbox" checked={item.usage.consumeOnUse} onChange={(e) => updateField('usage.consumeOnUse', e.target.checked)} />
                </div>
              </div>
            )}

            {activeTab === 'effects' && (
              <div className="flex flex-col gap-3">
                <div className="flex justify-between items-center px-1">
                   <span className="text-[9px] text-gray-500 uppercase font-black tracking-tighter">Logic Pipeline</span>
                   <Button variant="ghost" className="text-[9px] py-1" onClick={addEffect}>+ ADD EFFECT</Button>
                </div>
                <div className="flex flex-col gap-2">
                  {item.effects.map((eff, idx) => (
                    <div key={eff.id} className="w3-card-inset p-2 flex gap-2 items-center">
                      <div className="flex-1 grid grid-cols-3 gap-2">
                        <Input value={eff.condition} placeholder="Condition" onChange={(v) => {
                          const ne = [...item.effects]; ne[idx].condition = v; updateField('effects', ne);
                        }} />
                        <Input value={eff.effect} placeholder="Effect" onChange={(v) => {
                          const ne = [...item.effects]; ne[idx].effect = v; updateField('effects', ne);
                        }} />
                        <Input value={eff.target} placeholder="Target" onChange={(v) => {
                          const ne = [...item.effects]; ne[idx].target = v; updateField('effects', ne);
                        }} />
                      </div>
                      <Button variant="ghost" className="text-red-500 p-1" onClick={() => {
                        updateField('effects', item.effects.filter(ex => ex.id !== eff.id));
                      }}>✕</Button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};