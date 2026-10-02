import React, { useState, useMemo } from 'react';
import { StoryPack, StoryNode } from '../../types';
import { Card } from '../../ui/components/Card';
import { Button } from '../../ui/components/Button';
import { Input, TextArea, Select } from '../../ui/components/Input';
import { MonitorCore } from '../../ui/components/MonitorCore';
import { SplitLayout60_40 } from '../../ui/layout/SplitLayout60_40';
import { generateId } from '../../core/utils';

interface StoryTabProps {
  story: StoryPack;
  onChange: (updated: StoryPack) => void;
  toolActions?: any;
}

export const StoryTab: React.FC<StoryTabProps> = ({ story, onChange, toolActions }) => {
  const [selectedId, setSelectedId] = useState<string | null>(story.storyNodes[0]?.nodeId || null);
  const [search, setSearch] = useState('');

  const selectedNode = useMemo(() => 
    story.storyNodes.find(n => n.nodeId === selectedId)
  , [story.storyNodes, selectedId]);

  const addNode = () => {
    const id = generateId('node');
    const n: StoryNode = { nodeId: id, type: 'NarrativeBlock', title: 'New Passage', body: 'Story details...', choices: [] };
    onChange({ ...story, storyNodes: [...story.storyNodes, n] });
    setSelectedId(id);
  };

  const updateNode = (updated: StoryNode) => {
    const next = story.storyNodes.map(n => n.nodeId === updated.nodeId ? updated : n);
    onChange({ ...story, storyNodes: next });
  };

  return (
    <SplitLayout60_40
      toolActions={toolActions}
      topLeft={
        <div className="flex flex-col h-full bg-[var(--surface-2)]">
          <div className="p-3 border-b border-[var(--border)] flex flex-col gap-2">
            <Button id="tab-primary-add" variant="accent" className="h-9 text-[9px]" onClick={addNode}>+ NEW PASSAGE</Button>
            <input 
              type="text" placeholder="Search narrative..." 
              className="w-full text-[10px] p-2 bg-[var(--surface)] border border-[var(--border)] rounded-lg outline-none focus:border-blue-500 text-[var(--text)]"
              value={search} onChange={e => setSearch(e.target.value)}
            />
          </div>
          <div className="flex-1 overflow-y-auto">
            {story.storyNodes.filter(n => n.title?.toLowerCase().includes(search.toLowerCase())).map(n => (
              <button
                key={n.nodeId} onClick={() => setSelectedId(n.nodeId)}
                className={`w-full p-4 text-left border-b border-[var(--border)] transition-all clickable ${selectedId === n.nodeId ? 'bg-[var(--surface)] border-l-4 border-l-blue-600 shadow-sm' : 'hover:bg-white/5'}`}
              >
                <div className="text-[11px] font-black text-[var(--text)] leading-none mb-1.5 uppercase">{n.title || 'Untitled'}</div>
                <div className="text-[9px] text-[var(--text-dim)] font-medium truncate italic">{n.body}</div>
              </button>
            ))}
          </div>
        </div>
      }
      topRight={
        <div className="p-3 md:p-6 flex flex-col gap-4 h-full overflow-y-auto bg-[var(--surface)]">
          {selectedNode ? (
            <div className="flex flex-col gap-4 pb-12 animate-in fade-in">
              <Card className="p-4 flex flex-col gap-4">
                <div className="flex flex-col md:flex-row gap-4 items-start md:items-center">
                   <div className="w-12 h-12 md:w-16 md:h-16 w3-card-inset flex items-center justify-center text-xl md:text-2xl shrink-0">📖</div>
                   <div className="flex-1 w-full">
                      <Input label="Passage Label" value={selectedNode.title || ''} onChange={v => updateNode({...selectedNode, title: v})} />
                   </div>
                   <div className="w-full md:w-auto flex justify-end shrink-0">
                      <Button variant="danger" className="h-9 px-4 text-[9px]" onClick={() => {
                        if (confirm('Erase this node?')) {
                          onChange({...story, storyNodes: story.storyNodes.filter(n => n.nodeId !== selectedId)});
                          setSelectedId(null);
                        }
                      }}>ERASE</Button>
                   </div>
                </div>
              </Card>

              <TextArea label="Narrative Payload" className="min-h-[120px] text-[11px]" value={selectedNode.body || ''} onChange={v => updateNode({...selectedNode, body: v})} />
              
              <div className="flex flex-col gap-3">
                 <div className="flex justify-between items-center px-1">
                   <h3 className="text-[9px] font-black text-[var(--text-dim)] uppercase tracking-widest">Decision Logic</h3>
                   <Button variant="ghost" className="text-[9px] h-6 px-3" onClick={() => updateNode({...selectedNode, choices: [...(selectedNode.choices || []), {label:'Choice Path', toNodeId:''}]})}>+ LINK</Button>
                 </div>
                 <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                   {selectedNode.choices?.map((c, i) => (
                     <div key={i} className="w3-card-inset p-3 flex flex-col gap-2 rounded-xl">
                        <Input label="Player Choice" className="text-[10px]" value={c.label} onChange={v => {
                          const nc = [...selectedNode.choices!]; nc[i].label = v; updateNode({...selectedNode, choices: nc});
                        }} />
                        <Select 
                          label="Redirect to"
                          value={c.toNodeId} 
                          options={[{label:'--- Select ---', value:''}, ...story.storyNodes.map(n => ({label: n.title || '...', value: n.nodeId}))]} 
                          onChange={v => {
                            const nc = [...selectedNode.choices!]; nc[i].toNodeId = v; updateNode({...selectedNode, choices: nc});
                          }}
                        />
                        <Button variant="ghost" className="text-red-500 text-[8px] h-6 self-end" onClick={() => {
                          const nc = [...selectedNode.choices!]; nc.splice(i, 1); updateNode({...selectedNode, choices: nc});
                        }}>✕ REMOVE</Button>
                     </div>
                   ))}
                 </div>
              </div>
            </div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-center opacity-30">
               <span className="text-4xl mb-2">📖</span>
               <p className="text-[10px] font-black uppercase tracking-widest">Select nexus node</p>
            </div>
          )}
        </div>
      }
      bottomMain={
        <MonitorCore 
          title="Narrative Sync Monitor" 
          isEmpty={!selectedNode} 
          emptyState={{title:"Registry Offline", description:"Select a narrative passage above.", onAction: addNode}}
        >
          {selectedNode && (
            <div className="max-w-xl mx-auto flex flex-col gap-4 py-2 animate-in fade-in duration-700">
              <h1 className="text-2xl md:text-3xl font-black text-[var(--text)] tracking-tighter uppercase border-l-4 border-blue-600 pl-4">{selectedNode.title}</h1>
              <div className="text-sm md:text-base text-[var(--text)] leading-relaxed font-medium bg-[var(--surface)] p-5 rounded-2xl shadow-inner border border-[var(--border)] italic">
                {selectedNode.body || 'Waiting for narrative input...'}
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-2">
                {selectedNode.choices?.map((c, i) => (
                  <button key={i} onClick={() => setSelectedId(c.toNodeId)} className="p-3 text-left border border-[var(--border)] bg-[var(--surface)] rounded-xl font-black text-[var(--text)] hover:border-blue-500 transition-all text-[10px] flex items-center justify-between group">
                    <span className="truncate">{c.label}</span>
                    <span className="text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity">→</span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </MonitorCore>
      }
    />
  );
};