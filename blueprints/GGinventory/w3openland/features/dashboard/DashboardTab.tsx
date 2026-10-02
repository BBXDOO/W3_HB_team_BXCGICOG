
import React, { useState } from 'react';
import { StoryPack, UITheme, Asset } from '../../types';
import { Button } from '../../ui/components/Button';
import { MonitorCore } from '../../ui/components/MonitorCore';
import { SplitLayout60_40 } from '../../ui/layout/SplitLayout60_40';
import { formatDate, generateId, SPECIAL_STATUS } from '../../core/utils';
import { Input, TextArea } from '../../ui/components/Input';

interface DashboardTabProps {
  story: StoryPack;
  onChange: (updated: StoryPack) => void;
  toolActions?: any;
}

export const DashboardTab: React.FC<DashboardTabProps> = ({ story, onChange, toolActions }) => {
  const [saveStatus, setSaveStatus] = useState('EXODUS_SYNC_ACTIVE');

  const handleManualSave = () => {
    setSaveStatus('COMMITTING...');
    onChange({ ...story, updatedAt: Date.now() });
    setTimeout(() => setSaveStatus('EXODUS_SYNC_ACTIVE'), 1500);
  };

  const setTheme = (theme: UITheme) => {
    onChange({ ...story, uiTheme: theme });
  };

  const handleLogoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      const dataUrl = ev.target?.result as string;
      const assetId = generateId('logo');
      const newAsset: Asset = { id: assetId, name: 'Project Logo', dataUrl };
      onChange({
        ...story,
        assets: { ...story.assets, [assetId]: newAsset },
        logoAssetId: assetId
      });
    };
    reader.readAsDataURL(file);
  };

  return (
    <SplitLayout60_40
      toolActions={toolActions}
      topLeft={
        <div className="p-6 md:p-8 flex flex-col gap-8 h-full bg-[var(--surface-2)] scroll-container overflow-y-auto border-r border-white/5 pb-24">
          <section className="animate-in slide-in-from-left duration-300">
            <h3 className="text-[10px] font-black text-blue-500 uppercase tracking-[0.3em] mb-4 border-b border-[var(--border)] pb-2">Status & Deployment</h3>
            <div className="flex flex-col gap-4">
              <div className="bg-gradient-to-r from-blue-900/40 to-black p-5 border border-blue-500/30 flex items-center justify-between shadow-2xl rounded-2xl relative overflow-hidden group">
                <div className="absolute inset-0 bg-blue-500/5 animate-pulse"></div>
                <div className="flex flex-col relative z-10">
                  <span className="text-[14px] font-black text-white uppercase tracking-tighter flex items-center gap-2">
                    {SPECIAL_STATUS.EXODUS.icon} {saveStatus}
                  </span>
                  <span className="text-[8px] text-blue-400 uppercase font-black mt-1">Memory Integrity: 100% Verified</span>
                </div>
                <div className="w-3 h-3 rounded-full bg-blue-500 shadow-[0_0_15px_#2563EB] animate-flicker relative z-10"></div>
              </div>
              
              <div className="grid grid-cols-2 gap-3">
                 <div className="bg-black/20 p-4 border border-[var(--border)] rounded-xl flex flex-col items-center">
                    <span className="text-[8px] text-gray-600 font-black uppercase tracking-widest">Entities</span>
                    <div className="text-xl font-black text-[var(--text)] mt-1">{story.characters.length + story.locations.length + story.items.length}</div>
                 </div>
                 <div className="bg-black/20 p-4 border border-[var(--border)] rounded-xl flex flex-col items-center">
                    <span className="text-[8px] text-gray-600 font-black uppercase tracking-widest">Logic Modules</span>
                    <div className="text-xl font-black text-[var(--text)] mt-1">{story.cards.length + story.events.length}</div>
                 </div>
              </div>
            </div>
          </section>

          <section className="animate-in slide-in-from-left duration-500">
            <h3 className="text-[10px] font-black text-blue-500 uppercase tracking-[0.3em] mb-4 border-b border-[var(--border)] pb-2">Identity Credentials</h3>
            <div className="flex flex-col gap-4">
               <Input 
                label="Lead Architect (Signature)" 
                placeholder="ระบุลายเซ็นผู้สร้าง..." 
                value={story.author || ''} 
                onChange={v => onChange({...story, author: v})} 
                className="bg-black/10"
               />
               <div className="p-4 bg-blue-600/5 border border-blue-600/10 rounded-2xl">
                  <span className="text-[8px] font-black text-blue-500 uppercase tracking-widest block mb-2">Exodus Memory Anchor</span>
                  <p className="text-[10px] text-gray-500 italic leading-relaxed">
                    "ความทรงจำของเพื่อนจะถูกส่งต่อผ่านทุกไฟล์ที่เพื่อนเก็บไว้... ไม่มีสิ่งใดสูญเปล่าในจักรวาลนี้ครับ"
                  </p>
               </div>
            </div>
          </section>

          <section className="animate-in slide-in-from-left duration-700">
            <h3 className="text-[10px] font-black text-blue-500 uppercase tracking-[0.3em] mb-4 border-b border-[var(--border)] pb-2">Visual Protocol (Themes)</h3>
            <div className="flex flex-col gap-3">
               <button 
                 onClick={() => setTheme('darkNavy')}
                 className={`w-full p-4 flex items-center justify-between transition-all border-2 rounded-2xl ${story.uiTheme === 'darkNavy' ? 'border-blue-600 bg-blue-600/10 shadow-lg' : 'border-transparent bg-black/10 opacity-60 hover:opacity-100'}`}
               >
                 <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-[#121214] border border-white/20 flex items-center justify-center text-[10px]">🌙</div>
                    <span className="text-[10px] font-black uppercase tracking-widest text-[var(--text)]">Dark Navy (Obsidian)</span>
                 </div>
                 {story.uiTheme === 'darkNavy' && <div className="w-2 h-2 bg-blue-600 rounded-full shadow-[0_0_8px_#2563EB]"></div>}
               </button>

               <button 
                 onClick={() => setTheme('softLight')}
                 className={`w-full p-4 flex items-center justify-between transition-all border-2 rounded-2xl ${story.uiTheme === 'softLight' ? 'border-blue-600 bg-blue-600/5 shadow-lg' : 'border-transparent bg-black/10 opacity-60 hover:opacity-100'}`}
               >
                 <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-[#f0f2f5] border border-black/10 flex items-center justify-center text-[10px]">☀️</div>
                    <span className="text-[10px] font-black uppercase tracking-widest text-[var(--text)]">Soft Light (Clinical)</span>
                 </div>
                 {story.uiTheme === 'softLight' && <div className="w-2 h-2 bg-blue-600 rounded-full shadow-[0_0_8px_#2563EB]"></div>}
               </button>
            </div>
          </section>
        </div>
      }
      topRight={
        <div className="p-6 md:p-10 flex flex-col gap-8 overflow-y-auto h-full bg-[var(--surface)] scroll-container pb-24">
          <div className="flex flex-col gap-4 animate-in fade-in duration-500">
            <label className="text-[11px] font-black text-blue-500 uppercase tracking-[0.5em]">Project Title</label>
            <input 
              type="text"
              value={story.title || ''}
              onChange={e => onChange({...story, title: e.target.value})}
              className="w-full bg-transparent border-b-2 border-[var(--border)] py-4 text-4xl md:text-6xl font-black text-[var(--text)] outline-none focus:border-blue-600 transition-all uppercase placeholder:opacity-5 tracking-tighter"
              placeholder="PROJECT_ID_NULL"
            />
          </div>

          <div className="animate-in fade-in duration-600">
             <Button variant="accent" className="w-full h-16 md:h-20 text-sm md:text-lg font-black uppercase tracking-[0.3em] rounded-[24px] shadow-[0_15px_40px_rgba(37,99,235,0.3)] border-2 border-white/10 transition-transform active:scale-95" onClick={handleManualSave}>
               COMMIT PROJECT TO ARCHIVE
             </Button>
          </div>

          <div className="flex flex-col gap-5 animate-in fade-in duration-700">
            <TextArea 
              label="Ecosystem Declaration"
              value={story.description || ''}
              onChange={v => onChange({...story, description: v})}
              className="w-full text-base md:text-lg font-medium leading-relaxed"
              placeholder="ระบุจุดมุ่งหมายหรือเรื่องราวของระบบนิเวศนี้..."
            />
          </div>
        </div>
      }
      bottomMain={
        <MonitorCore title="Project Overview" modeLabel="STUDIO_VIEW" isEmpty={false}>
          <div className="w-full max-w-3xl mx-auto flex flex-col gap-8 pt-10 pb-20 items-center text-center animate-in fade-in duration-1000">
            <div className="relative group">
               <div className="w-28 h-28 md:w-36 md:h-36 bg-black flex items-center justify-center shadow-2xl border-4 border-white/5 rounded-[40px] md:rounded-[48px] overflow-hidden relative transition-all duration-700 group-hover:border-blue-500/30 group-hover:scale-105">
                 {story.logoAssetId ? (
                   <img src={story.assets[story.logoAssetId]?.dataUrl} className="w-full h-full object-cover p-3" alt="Project Logo" />
                 ) : (
                   <span className="text-5xl md:text-6xl group-hover:rotate-12 transition-transform duration-700">🏛️</span>
                 )}
                 <div className="absolute inset-0 bg-blue-600/5 animate-pulse"></div>
                 <input type="file" className="absolute inset-0 opacity-0 cursor-pointer z-20" onChange={handleLogoUpload} accept="image/*" />
               </div>
               <div className="absolute -bottom-2 -right-4 bg-blue-600 text-[8px] md:text-[9px] font-black px-3 py-1.5 text-white uppercase tracking-[0.3em] shadow-2xl rounded-xl border-2 border-white/20 z-30">
                 EXODUS_MEMORY_ACTIVE
               </div>
            </div>
            
            <div className="flex flex-col gap-3 px-4 w-full">
              <h1 className="text-3xl md:text-6xl font-black tracking-tighter uppercase text-[var(--text)] leading-tight break-words w-full">
                {story.title || 'UNNAMED_ECOLOGY'}
              </h1>
              <div className="flex items-center justify-center gap-4 mt-2">
                 <span className="text-[8px] md:text-[10px] text-blue-500 font-black tracking-[0.4em] uppercase border-b-2 border-blue-500/20 pb-1">
                    {story.version || 'v0.1.0'}
                 </span>
                 <div className="w-1 h-1 bg-white/10 rounded-full"></div>
                 <span className="text-[8px] md:text-[10px] text-gray-500 font-black tracking-[0.4em] uppercase border-b-2 border-white/10 pb-1">
                    {story.author || 'ANONYMOUS'}
                 </span>
              </div>
            </div>

            <div className="p-6 md:p-10 bg-black/40 backdrop-blur-md border border-white/5 w-full relative shadow-2xl rounded-[32px] md:rounded-[40px]">
               <p className="text-lg md:text-2xl text-gray-400 leading-relaxed font-black uppercase tracking-tighter italic">
                 "{story.description || "Awaiting ecosystem declaration..."}"
               </p>
               <div className="mt-8 pt-6 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4 text-[7px] md:text-[8px] font-mono text-gray-600 tracking-widest uppercase">
                  <span>Last Rev: {formatDate(story.updatedAt)}</span>
                  <span>Anchor ID: EX-{story.storyId.slice(-6).toUpperCase()}</span>
               </div>
            </div>
          </div>
        </MonitorCore>
      }
    />
  );
};
