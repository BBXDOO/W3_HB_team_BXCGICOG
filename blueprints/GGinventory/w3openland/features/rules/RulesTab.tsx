import React, { useState, useMemo } from 'react';
import { StoryPack, RulesetPack } from '../../types';
import { Button } from '../../ui/components/Button';
import { Input, TextArea } from '../../ui/components/Input';
import { MonitorCore } from '../../ui/components/MonitorCore';
import { SplitLayout60_40 } from '../../ui/layout/SplitLayout60_40';
import { generateId } from '../../core/utils';

interface RulesTabProps {
  story: StoryPack;
  onChange: (updated: StoryPack) => void;
}

export const RulesTab: React.FC<RulesTabProps> = ({ story, onChange }) => {
  const [selectedId, setSelectedId] = useState<string | null>(story.rulesets?.[0]?.id || null);

  const selectedRule = useMemo(() => 
    (story.rulesets || []).find(r => r.id === selectedId)
  , [story.rulesets, selectedId]);

  const addRule = () => {
    const id = generateId('rule');
    const nr: RulesetPack = { id, name: 'Core Mechanics', blocks: [{ title: 'Movement', content: 'Describe rules here...' }], modifiers: [] };
    onChange({ ...story, rulesets: [...(story.rulesets || []), nr] });
    setSelectedId(id);
  };

  const updateRule = (updated: RulesetPack) => {
    const next = (story.rulesets || []).map(r => r.id === updated.id ? updated : r);
    onChange({ ...story, rulesets: next });
  };

  return (
    <SplitLayout60_40
      topLeft={
        <div className="flex flex-col h-full bg-gray-50/50">
          <div className="p-4 border-b border-gray-200 bg-white">
            <Button variant="accent" onClick={addRule}>+ NEW RULESET</Button>
          </div>
          <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-2">
            {(story.rulesets || []).map(r => (
              <button 
                key={r.id} onClick={() => setSelectedId(r.id)}
                className={`p-4 text-left text-xs font-black uppercase rounded-xl border transition-all ${selectedId === r.id ? 'bg-blue-600 border-blue-600 text-white shadow-lg' : 'bg-white border-gray-200 text-gray-500 hover:border-blue-400'}`}
              >
                {r.name}
              </button>
            ))}
            {(story.rulesets || []).length === 0 && <p className="text-center text-xs text-gray-400 py-10 uppercase font-black tracking-widest">Repository Empty</p>}
          </div>
        </div>
      }
      topRight={
        <div className="p-8 flex flex-col gap-8 overflow-y-auto h-full">
          <h2 className="text-[10px] font-black uppercase text-gray-400 tracking-[0.2em]">Rule Protocol Editor</h2>
          {selectedRule ? (
            <div className="flex flex-col gap-8 pb-12">
              <Input label="Registry Name" value={selectedRule.name} onChange={v => updateRule({...selectedRule, name: v})} />
              <div className="flex flex-col gap-6">
                {selectedRule.blocks.map((b, i) => (
                  <div key={i} className="flex flex-col gap-4 w3-card-inset p-5 bg-gray-50">
                     <div className="flex justify-between items-center">
                        <span className="text-[8px] font-black text-gray-400 uppercase tracking-widest">Block 0{i+1}</span>
                        <Button variant="ghost" className="text-red-500 p-1 h-6 w-6" onClick={() => {
                          const nb = [...selectedRule.blocks]; nb.splice(i, 1); updateRule({...selectedRule, blocks: nb});
                        }}>✕</Button>
                     </div>
                     <Input label="Sub-Protocol Title" value={b.title} onChange={v => {
                       const nb = [...selectedRule.blocks]; nb[i].title = v; updateRule({...selectedRule, blocks: nb});
                     }} />
                     <TextArea label="Protocol Content" value={b.content} onChange={v => {
                       const nb = [...selectedRule.blocks]; nb[i].content = v; updateRule({...selectedRule, blocks: nb});
                     }} />
                  </div>
                ))}
                <Button variant="secondary" onClick={() => updateRule({...selectedRule, blocks: [...selectedRule.blocks, {title:'New Rule', content:''}]})}>+ APPEND LOGIC BLOCK</Button>
              </div>
              <Button variant="danger" className="mt-8" onClick={() => {
                if (confirm('Purge ruleset?')) {
                  onChange({...story, rulesets: story.rulesets.filter(r => r.id !== selectedId)});
                  setSelectedId(null);
                }
              }}>PURGE RULESET</Button>
            </div>
          ) : (
            <p className="text-xs italic text-gray-400">Select protocol to initialize editing.</p>
          )}
        </div>
      }
      bottomMain={
        <MonitorCore 
          title="Logic Preview" 
          isEmpty={!selectedRule} 
          emptyState={{title:"No Protocol Manifest", description:"Design ecosystem rules and logic flow above.", onAction: addRule}}
        >
          {selectedRule && (
            <div className="max-w-3xl mx-auto flex flex-col gap-8">
              <h1 className="text-4xl font-black text-gray-900 tracking-tighter mb-4">{selectedRule.name}</h1>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {selectedRule.blocks.map((b, i) => (
                  <div key={i} className="flex flex-col gap-2">
                    <h4 className="text-sm font-black text-gray-900 flex items-center gap-2">
                      <span className="w-4 h-4 rounded-full bg-blue-600 text-white text-[8px] flex items-center justify-center">{i+1}</span>
                      {b.title}
                    </h4>
                    <p className="text-xs text-gray-600 leading-relaxed font-medium">{b.content}</p>
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