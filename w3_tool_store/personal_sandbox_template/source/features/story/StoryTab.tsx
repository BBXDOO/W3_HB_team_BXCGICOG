import { createPortal } from 'react-dom';
import { StoryWriter } from './StoryWriter';
import { MarkdownContent } from './MarkdownContent';
import { readTextDocument, type TextDocument } from '../../core/documentFiles';
import React, { useState, useMemo, useEffect, useRef } from 'react';
import { StoryPack, StoryNode } from '../../types';
import { Card } from '../../ui/components/Card';
import { Button } from '../../ui/components/Button';
import { Input, TextArea, Select } from '../../ui/components/Input';
import { MonitorCore } from '../../ui/components/MonitorCore';
import { SplitLayout60_40 } from '../../ui/layout/SplitLayout60_40';
import { generateId } from '../../core/utils';
import { RichContent } from '../editor/ContentFormat';

interface StoryTabProps {
  story: StoryPack;
  onChange: (updated: StoryPack) => void;
  toolActions?: any;
  navigationTarget?: string | null;
  onCommit?: () => boolean;
  saveState?: 'pending' | 'saved' | 'error';
}

export const StoryTab: React.FC<StoryTabProps> = ({ story, onChange, toolActions, navigationTarget, onCommit = () => true, saveState = 'saved' }) => {
  const [selectedId, setSelectedId] = useState<string | null>(story.storyNodes[0]?.nodeId || null);
  const [search, setSearch] = useState('');
  const [writerOpen, setWriterOpen] = useState(false);
  const [importDoc, setImportDoc] = useState<TextDocument | null>(null);
  const [importError, setImportError] = useState('');
  const importInput = useRef<HTMLInputElement>(null);
  useEffect(() => { if (navigationTarget && story.storyNodes.some(node => node.nodeId === navigationTarget)) setSelectedId(navigationTarget); }, [navigationTarget, story.storyNodes]);

  const selectedNode = useMemo(() => 
    story.storyNodes.find(n => n.nodeId === selectedId)
  , [story.storyNodes, selectedId]);

  const addNode = () => {
    const id = generateId('node');
    const n: StoryNode = { nodeId: id, type: 'NarrativeBlock', title: 'ตอนใหม่', body: '', bodyFormat: 'markdown', choices: [] };
    onChange({ ...story, storyNodes: [...story.storyNodes, n] });
    setSelectedId(id);
    setWriterOpen(true);
  };

  const updateNode = (updated: StoryNode) => {
    const next = story.storyNodes.map(n => n.nodeId === updated.nodeId ? updated : n);
    onChange({ ...story, storyNodes: next });
  };

  const importFile = async (file?: File) => {
    if (!file) return;
    setImportError('');
    try { setImportDoc(await readTextDocument(file)); }
    catch (error) { setImportError(error instanceof Error ? error.message : 'อ่านไฟล์ไม่สำเร็จ'); }
  };
  const finishImport = (mode: 'new' | 'append' | 'replace') => {
    if (!importDoc) return;
    if (mode === 'new' && !onCommit()) { setImportError('บันทึกโครงการไม่สำเร็จ โปรดส่งออกตอนปัจจุบันก่อนสร้างตอนใหม่'); return; }
    if (mode !== 'new' && !selectedNode) return;
    if (mode === 'replace' && selectedNode?.body && !window.confirm(`แทนที่เนื้อหา “${selectedNode.title || 'ตอนนี้'}” ด้วยไฟล์ “${importDoc.filename}” หรือไม่?`)) return;
    if (mode === 'new') {
      const imported: StoryNode = { nodeId: generateId('node'), type: 'NarrativeBlock', title: importDoc.title, body: importDoc.body, bodyFormat: importDoc.bodyFormat, choices: [] };
      onChange({ ...story, storyNodes: [...story.storyNodes, imported] }); setSelectedId(imported.nodeId);
    } else if (selectedNode) {
      updateNode({ ...selectedNode, body: mode === 'append' ? `${selectedNode.body || ''}${selectedNode.body ? '\n\n' : ''}${importDoc.body}` : importDoc.body,
        bodyFormat: mode === 'replace' ? importDoc.bodyFormat : selectedNode.bodyFormat || 'legacy' });
    }
    setImportDoc(null); setWriterOpen(true);
  };

  return (
    <>
    <input ref={importInput} aria-label="เลือกไฟล์เอกสาร Story" type="file" accept=".md,.markdown,.txt,text/markdown,text/plain" hidden onChange={e => { const file = e.target.files?.[0]; e.target.value = ''; void importFile(file); }} />
    {importError && <div role="alert" className="story-import-error">{importError}<button type="button" onClick={() => setImportError('')}>✕</button></div>}
    <SplitLayout60_40
      toolActions={toolActions}
      topLeft={
        <div className="flex flex-col h-full bg-[var(--surface-2)]">
          <div className="p-3 border-b border-[var(--border)] flex flex-col gap-2">
            <Button id="tab-primary-add" variant="accent" className="h-9 text-[9px]" onClick={addNode}>+ เขียนตอนใหม่</Button>
            <Button variant="secondary" onClick={() => importInput.current?.click()}>นำเข้า .md / .txt</Button>
            <input 
              type="text" placeholder="Search narrative..." 
              className="w-full text-[10px] p-2 bg-[var(--surface)] border border-[var(--border)] rounded-lg outline-none focus:border-blue-500 text-[var(--text)]"
              value={search} onChange={e => setSearch(e.target.value)}
            />
          </div>
          <div className="flex-1 overflow-y-auto">
            {story.storyNodes.filter(n => n.title?.toLowerCase().includes(search.toLowerCase())).map(n => (
              <button
                key={n.nodeId} onClick={() => { setSelectedId(n.nodeId); setWriterOpen(true); }}
                aria-label={`เขียน ${n.title || 'ไม่มีชื่อ'}`}
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

              <Button variant="accent" onClick={() => setWriterOpen(true)}>✎ เปิดหน้าต่างเขียนเต็มจอ</Button>
              <TextArea richText={selectedNode.bodyFormat !== 'markdown'} label="Narrative Payload" className="min-h-[120px] text-[11px]" value={selectedNode.body || ''} onChange={v => updateNode({...selectedNode, body: v})} />
              
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
                {selectedNode.bodyFormat === 'markdown' ? <MarkdownContent value={selectedNode.body || ''} /> : <RichContent value={selectedNode.body || 'Waiting for narrative input...'} />}
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
    {writerOpen && selectedNode && <StoryWriter key={selectedNode.nodeId} node={selectedNode} onChange={updateNode} onCommit={onCommit} saveState={saveState}
      onNew={addNode} onImport={() => importInput.current?.click()} onClose={() => { if (importDoc) setImportDoc(null); else setWriterOpen(false); }} />}
    {importDoc && createPortal(<div className="story-import-overlay"><section role="dialog" aria-modal="true" aria-label="นำเข้าเอกสาร Story" className="story-import-dialog">
      <header><h2>นำเข้าเอกสาร</h2><button type="button" aria-label="ปิดหน้าต่างนำเข้า" onClick={() => setImportDoc(null)}>✕</button></header>
      <p>{importDoc.filename} · {importDoc.body.length.toLocaleString()} อักขระ</p><pre>{importDoc.body.slice(0, 500)}{importDoc.body.length > 500 ? '\n…' : ''}</pre>
      <p>สร้างตอนใหม่จะเก็บเอกสารแยกจากตอนที่กำลังทำงานอยู่</p>
      <button type="button" onClick={() => finishImport('new')}>สร้างเป็นตอนใหม่</button>
      <button type="button" disabled={!selectedNode} onClick={() => finishImport('append')}>เพิ่มท้ายตอนปัจจุบัน · เก็บรูปแบบเดิม</button>
      <button type="button" disabled={!selectedNode} onClick={() => finishImport('replace')}>แทนที่เนื้อหาตอนปัจจุบัน</button>
    </section></div>, document.body)}
    </>
  );
};
