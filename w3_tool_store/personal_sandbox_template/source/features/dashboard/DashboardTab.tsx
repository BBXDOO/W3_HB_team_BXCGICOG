import { summarizeProject, normalizeProgress, projectStatusLabels } from '../../core/projectSummary';
import type { ProjectStatus } from '../../types';
import { ProjectIdentityCard } from '../../ui/components/ProjectIdentityCard';
import { Acknowledgements } from '../../ui/components/Acknowledgements';

import React, { useState } from 'react';
import { StoryPack, UITheme, Asset } from '../../types';
import { Button } from '../../ui/components/Button';
import { MonitorCore } from '../../ui/components/MonitorCore';
import { SplitLayout60_40 } from '../../ui/layout/SplitLayout60_40';
import { generateId, SPECIAL_STATUS } from '../../core/utils';
import { Input, TextArea, Select } from '../../ui/components/Input';

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
              <div className="bg-[var(--surface)] p-5 border border-[var(--border)] flex items-center justify-between shadow-2xl rounded-2xl relative overflow-hidden group">
                <div className="absolute inset-0 bg-blue-500/5 animate-pulse"></div>
                <div className="flex flex-col relative z-10">
                  <span className="text-[14px] font-black text-white uppercase tracking-tighter flex items-center gap-2">
                    {SPECIAL_STATUS.EXODUS.icon} {saveStatus}
                  </span>
                  <span className="text-[8px] text-blue-400 uppercase font-black mt-1">ข้อมูลโครงการบนเครื่องนี้</span>
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
               <div className="p-4 bg-[var(--surface)] border border-[var(--border)] rounded-2xl">
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
        <div className="ps-dashboard-editor p-4 md:p-8 flex flex-col gap-5 overflow-y-auto h-full bg-[var(--surface)] scroll-container pb-24">
          <div className="flex flex-col gap-4 animate-in fade-in duration-500">
            <div className="ps-project-heading"><label>01 / โครงการ</label><span>PROJECT</span></div>
            <input 
              type="text"
              value={story.title || ''}
              onChange={e => onChange({...story, title: e.target.value})}
              className="w-full bg-transparent border-b-2 border-[var(--border)] py-3 text-2xl md:text-4xl font-black text-[var(--text)] outline-none focus:border-[var(--accent)] transition-all uppercase tracking-tighter"
              placeholder="PROJECT_ID_NULL"
            />
          </div>

          <div className="animate-in fade-in duration-600">
             <Button variant="accent" className="w-full h-12 md:h-14 text-xs md:text-sm font-black uppercase tracking-[0.16em] border border-white/10 transition-transform active:scale-95" onClick={handleManualSave}>
               บันทึกโครงการ
             </Button>
          </div>

          <div className="flex flex-col gap-5 animate-in fade-in duration-700">
            <TextArea 
              label="รายละเอียด / จุดมุ่งหมาย"
              value={story.description || ''}
              onChange={v => onChange({...story, description: v})}
              className="w-full text-base md:text-lg font-medium leading-relaxed"
              placeholder="ระบุจุดมุ่งหมายหรือเรื่องราวของระบบนิเวศนี้..."
            />
          </div>
          <section className="project-meta-editor" aria-label="ข้อมูลและความคืบหน้าโครงการ">
            <div className="grid grid-cols-2 gap-3"><Input label="เวอร์ชันโครงการ" value={story.version || ''} onChange={version => onChange({ ...story, version })} /><Select label="สถานะโครงการ" value={story.projectStatus || ''} options={[{ label: 'ยังไม่ระบุ', value: '' }, ...Object.entries(projectStatusLabels).map(([value, label]) => ({ value, label }))]} onChange={value => onChange({ ...story, projectStatus: value ? value as ProjectStatus : undefined })} /></div>
            <label className="project-progress-control">ความคืบหน้าที่คุณกำหนด (0–100%)<div><input aria-label="ปรับความคืบหน้าโครงการ" type="range" min="0" max="100" value={normalizeProgress(story.projectProgress) ?? 0} onChange={e => onChange({ ...story, projectProgress: Number(e.target.value) })} /><input aria-label="เปอร์เซ็นต์ความคืบหน้าโครงการ" type="number" min="0" max="100" placeholder="—" value={normalizeProgress(story.projectProgress) ?? ''} onChange={e => onChange({ ...story, projectProgress: e.target.value === '' ? undefined : normalizeProgress(Number(e.target.value)) })} /></div></label>
          </section>
          <section aria-label="สรุปโครงการ" className="ps-stat-grid grid grid-cols-2 gap-3 mt-1">
            <div className="ps-stat-tile"><span>01 / ตัวละคร</span><strong>{story.characters.length}</strong></div>
            <div className="ps-stat-tile"><span>02 / การ์ด</span><strong>{story.cards.length}</strong></div>
            <div className="ps-stat-tile"><span>03 / เหตุการณ์</span><strong>{story.events.length}</strong></div>
            <div className="ps-stat-tile"><span>04 / บอร์ด</span><strong>{story.boards.length}</strong></div>
          </section>
        </div>
      }
      bottomMain={
        <MonitorCore title="Project Overview" modeLabel="STUDIO_VIEW" isEmpty={false}>
          <div className="project-overview-detail">
            <div className="project-logo-control"><label title="เปลี่ยนรูปโครงการ"><span>{story.logoAssetId ? <img src={story.assets[story.logoAssetId]?.dataUrl} alt="รูปโครงการ" /> : '◇'}</span><input aria-label="เปลี่ยนรูปโครงการ" type="file" accept="image/*" onChange={handleLogoUpload} /></label><span>PROJECT PROFILE / BBX19 WORKSPACE</span></div>
            <ProjectIdentityCard project={{ ...story, ...summarizeProject(story) }} description={story.description} />
            <Acknowledgements />
          </div>

        </MonitorCore>
      }
    />
  );
};
