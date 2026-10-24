
import React, { useState, useEffect, useRef } from 'react';
import { Button } from '../../ui/components/Button';
import { Card } from '../../ui/components/Card';
import { StoryIndexItem, getStoryIndex, deleteStory, importStory, restoreBackup } from '../../core/storage';
import { formatDate } from '../../core/utils';
import { Modal } from '../../ui/components/Modal';
import type { ProjectKind } from '../../types';

const PROJECT_KINDS: { id: ProjectKind; label: string; description: string }[] = [
  { id: 'library', label: 'Library', description: 'เอกสาร คู่มือ เรื่องเล่า และข้อมูลที่จัดเก็บ' },
  { id: 'bookcraft', label: 'BG – Bookcraft', description: 'เกม บอร์ด การ์ด และหนังสือโต้ตอบ' },
  { id: 'concept', label: 'Concept mind map', description: 'ข้อมูลและแผนที่ที่เชื่อมด้วยเงื่อนไข' }
];

const kindLabel = (kind?: ProjectKind) =>
  PROJECT_KINDS.find(option => option.id === kind)?.label || 'ยังไม่กำหนดโหมด';

interface LibraryPageProps {
  onOpenStory: (id: string) => void;
  onNewStory: (kind: ProjectKind, title: string) => void;
  canInstall?: boolean;
}

export const LibraryPage: React.FC<LibraryPageProps> = ({ onOpenStory, onNewStory }) => {
  const [index, setIndex] = useState<StoryIndexItem[]>([]);
  const [showHelp, setShowHelp] = useState(false);
  const [showExportModal, setShowExportModal] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newKind, setNewKind] = useState<ProjectKind>('library');
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    setIndex(getStoryIndex());
  }, []);

  const refreshIndex = () => setIndex(getStoryIndex());

  const createProject = () => {
    if (!newTitle.trim()) return;
    onNewStory(newKind, newTitle.trim());
    setShowCreate(false);
    setNewTitle('');
  };

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const backup = await importStory(file);
    if (backup) {
      const existing = getStoryIndex().some(item => item.storyId === backup.story.storyId);
      if (existing && !confirm(`มีโครงการ "${backup.story.title}" ที่ใช้รหัสเดียวกันอยู่แล้ว การกู้คืนนี้จะแทนที่ข้อมูลโครงการและจุดเล่นเดิม ต้องการดำเนินการหรือไม่?`)) {
        if (fileInputRef.current) fileInputRef.current.value = '';
        return;
      }
      if (!restoreBackup(backup)) {
        alert('กู้คืนไม่สำเร็จ โปรดตรวจพื้นที่เก็บข้อมูลในเครื่องและเก็บไฟล์สำรองไว้');
        return;
      }
      refreshIndex();
      alert(`กู้คืนโครงการ "${backup.story.title}"${backup.runState ? ' พร้อมจุดเล่น' : ' (ไฟล์นี้ไม่มีจุดเล่น)'} เรียบร้อยแล้ว`);
    }
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="library-page h-screen w-full p-4 md:p-12 max-w-7xl mx-auto overflow-y-auto bg-[#121214] scroll-container pb-20 relative">
      
      <header className="flex flex-col md:flex-row justify-between items-start md:items-end gap-5 mb-6 pb-6 relative z-10 border-b border-white/5">
        <div className="animate-in fade-in slide-in-from-left duration-700">
          <h1 className="text-3xl md:text-5xl font-black text-white tracking-tighter mb-3 uppercase italic leading-none glow-text">PERSONAL SANDBOX</h1>
          <div className="flex items-center gap-4">
             <div className="w-12 h-1 bg-[#ea580c] shadow-[0_0_15px_#ea580c]"></div>
             <p className="text-[#ea580c] font-black uppercase tracking-[0.3em] text-[10px]">คลังโครงการส่วนตัว</p>
          </div>
        </div>
        <div className="flex flex-wrap gap-2 w-full md:w-auto animate-in fade-in slide-in-from-right duration-700">
          <input type="file" ref={fileInputRef} className="hidden" accept=".json" onChange={handleImport} />
          
          <button 
            onClick={() => setShowExportModal(true)}
            className="h-11 px-4 tactile-raised flex items-center gap-2 text-amber-400 hover:text-amber-300 font-black text-[10px] uppercase tracking-wider transition-all border border-amber-500/30 hover:border-amber-500/60 shadow-[0_0_15px_rgba(245,158,11,0.15)] active:scale-95"
          >
            📦 วิธีสำรองและติดตั้ง
          </button>

          <Button variant="ghost" onClick={() => fileInputRef.current?.click()} className="h-11 px-4 tactile-raised text-zinc-300 font-black text-[10px] hover:text-white transition-all border border-white/5">
            📤 นำเข้า JSON
          </Button>
          <Button variant="accent" onClick={() => setShowCreate(true)} className="h-11 px-5 text-[11px] font-black rounded-xl shadow-2xl active:scale-95 transition-all">
            + INITIALIZE NEW CORE
          </Button>
        </div>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-5 relative z-10" aria-label="โครงการทั้งหมด">
        {index.map((item, idx) => (
          <div 
            key={item.storyId} 
            onClick={() => onOpenStory(item.storyId)}
            className="group cursor-pointer relative animate-in fade-in zoom-in duration-500"
            style={{ animationDelay: `${idx * 100}ms` }}
          >
            <Card className="library-project-card p-4 relative min-h-[170px] flex flex-col justify-between overflow-hidden border border-white/10 shadow-xl">
              <div className="flex justify-between items-start gap-2 z-10">
                <span className="text-[9px] font-black text-emerald-300 uppercase tracking-[0.1em] bg-emerald-400/10 px-3 py-1 rounded-full border border-emerald-400/20 w-fit">{kindLabel(item.projectKind)}</span>
                <button 
                  type="button" aria-label={`ลบโครงการ ${item.title}`} className="text-red-300/70 transition-all px-2 py-1 bg-black/30 rounded-lg hover:bg-red-500 hover:text-white" 
                  onClick={(e) => { e.stopPropagation(); if(confirm('ต้องการลบ "จักรวาล" ชิ้นนี้ใช่หรือไม่?')) { deleteStory(item.storyId); refreshIndex(); } }}
                >
                  ✕
                </button>
              </div>

              <div className="flex-1 flex flex-col justify-center py-3 z-10">
                <h3 className="text-xl font-black text-white tracking-tight leading-tight group-hover:text-[#ea580c] transition-colors uppercase italic break-words line-clamp-2">
                  {item.title || 'UNNAMED_ENTITY'}
                </h3>
                <p className="text-[9px] text-zinc-400 font-bold uppercase tracking-[0.1em] mt-2">ID: {item.storyId.slice(-12)}</p>
              </div>

              <div className="pt-2 border-t border-white/10 flex justify-between items-center z-10">
                <div className="flex flex-col">
                   <span className="text-[8px] text-zinc-400 font-black uppercase tracking-[0.15em]">แก้ไขล่าสุด</span>
                   <span className="text-[10px] text-white font-bold">{formatDate(item.updatedAt)}</span>
                </div>
                <div className="w-9 h-9 tactile-raised flex items-center justify-center text-[#ea580c] group-hover:bg-[#ea580c] group-hover:text-white transition-all duration-300 border border-white/10" aria-hidden="true">
                   <span className="text-lg font-black">→</span>
                </div>
              </div>
            </Card>
          </div>
        ))}

        <button 
          className="min-h-[110px] tactile-inset border-2 border-dashed border-white/10 flex items-center justify-center gap-3 group hover:bg-white/5 transition-all animate-in fade-in"
          onClick={() => setShowCreate(true)}
          style={{ animationDelay: `${index.length * 100}ms` }}
        >
          <div className="w-10 h-10 tactile-raised flex items-center justify-center text-xl text-zinc-400 group-hover:text-[#ea580c] transition-all duration-500 border border-white/5">＋</div>
          <div className="flex flex-col items-center gap-1">
            <span className="text-[11px] font-black text-zinc-300 uppercase tracking-[0.4em] group-hover:text-white">Add Memory Block</span>
            <span className="text-[8px] text-zinc-500 font-bold uppercase tracking-[0.2em]">Initialize fresh ecosystem</span>
          </div>
        </button>
      </section>

      <footer className="mt-10 border-t border-white/10 pt-6 flex flex-col items-center gap-4 opacity-40 hover:opacity-100 transition-opacity duration-1000">
         <div className="flex items-center gap-6">
            <div className="w-12 h-[1px] bg-zinc-800"></div>
            <span className="text-[9px] font-black text-zinc-400 uppercase tracking-[0.8em]">Nexus Physical Link Established</span>
            <div className="w-12 h-[1px] bg-zinc-800"></div>
         </div>
         <div className="flex flex-col items-center gap-2">
            <p className="text-[10px] font-medium italic text-zinc-300">"ดูแลตัวเองนะครับเพื่อน ระบบพร้อมทำงานเสมอครับ"</p>
            <p className="text-[8px] font-black uppercase tracking-[0.4em] text-[#ea580c] mt-2">— Nexus Studio Engine v0.5</p>
         </div>
      </footer>

      <Modal isOpen={showCreate} title="สร้างโครงการใหม่" onClose={() => setShowCreate(false)} footer={
        <>
          <Button variant="ghost" onClick={() => setShowCreate(false)}>ยกเลิก</Button>
          <Button variant="accent" onClick={createProject} disabled={!newTitle.trim()}>สร้างโครงการ</Button>
        </>
      }>
        <div className="flex flex-col gap-5 text-[var(--text)]">
          <label className="flex flex-col gap-2 text-sm font-bold">
            ชื่อโครงการ
            <input autoFocus value={newTitle} onChange={e => setNewTitle(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') createProject(); }}
              placeholder="ตั้งชื่อให้ตรงกับเนื้อหาที่จะเก็บ" maxLength={120}
              className="w-full rounded-xl p-3 bg-[var(--surface)] border border-[var(--border)] text-[var(--text)]" />
          </label>
          <div className="flex flex-col gap-2">
            <p className="text-sm font-bold">โหมดการใช้งาน</p>
            {PROJECT_KINDS.map(option => (
              <button key={option.id} type="button" onClick={() => setNewKind(option.id)}
                aria-pressed={newKind === option.id}
                className={`text-left rounded-xl p-4 border transition-colors ${newKind === option.id ? 'border-emerald-500 bg-emerald-500/10' : 'border-[var(--border)] bg-[var(--surface)]'}`}>
                <span className="block font-bold">{option.label}</span>
                <span className="block text-xs text-[var(--text-dim)] mt-1">{option.description}</span>
              </button>
            ))}
          </div>
          <p className="text-xs text-[var(--text-dim)]">การเลือกนี้ระบุประเภทโครงการ หน้าการอ่านและเล่นเฉพาะโหมดจะเพิ่มในขั้นถัดไป</p>
        </div>
      </Modal>

      <Modal isOpen={showHelp} title="Nexus Registry Protocol" onClose={() => setShowHelp(false)}>
        <div className="flex flex-col gap-8 py-4 text-zinc-300 font-medium">
           <section>
              <h4 className="text-white font-black text-xs uppercase mb-3 border-l-4 border-[#ea580c] pl-4 tracking-widest">Data Persistence</h4>
              <p className="text-[11px] leading-relaxed">
                ข้อมูลทุกอย่างถูกเก็บไว้ในระดับ Browser Storage ของเพื่อนครับ เพื่อความปลอดภัยสูงสุด แนะนำให้กด EXPORT เก็บไว้เป็นระยะนะครับ
              </p>
           </section>
           <div className="p-6 tactile-inset italic text-[11px] text-center text-[#ea580c] uppercase font-black tracking-[0.3em] bg-black/40">
              "Efficiency is physical. Integrity is digital."
           </div>
        </div>
      </Modal>

      <Modal isOpen={showExportModal} title="📦 สำรองข้อมูลและติดตั้ง" onClose={() => setShowExportModal(false)}>
        <div className="flex flex-col gap-6 py-2 text-zinc-300 max-h-[75vh] overflow-y-auto scroll-container pr-2">
           <p className="text-sm leading-7">ใน Playtest กดบันทึกจุดอ่านก่อน แล้วกด EXPORT DATA ภายในโครงการ ไฟล์ JSON จะรวมข้อมูลโครงการและจุดเล่นล่าสุดที่บันทึกไว้ นำเข้าจากหน้าแรกเพื่อกู้คืนทั้งสองส่วน ไฟล์ JSON รุ่นเก่าที่ยังไม่มีจุดเล่นยังใช้ได้ ซอร์สโค้ดและแอปติดตั้งจะจัดส่งแยกต่างหาก</p>
           <section className="space-y-4">
              <h4 className="text-xs font-black uppercase text-amber-400 tracking-widest flex items-center gap-2">
                <span>1️⃣</span> วิธีรันบนเครื่องของคุณ (Localhost)
              </h4>
              <div className="p-4 tactile-inset font-mono text-[11px] text-zinc-300 space-y-2 border border-white/5 rounded-xl">
                 <p className="text-zinc-500"># 1. แตกไฟล์ zip แล้วเข้าไปในโฟลเดอร์</p>
                 <p className="text-emerald-400 font-bold">cd w3-personal-sandbox</p>
                 <p className="text-zinc-500 mt-2"># 2. ติดตั้งแพ็กเกจ (ใช้ Node.js 18+)</p>
                 <p className="text-emerald-400 font-bold">npm install</p>
                 <p className="text-zinc-500 mt-2"># 3. รันเซิร์ฟเวอร์จำลอง</p>
                 <p className="text-emerald-400 font-bold">npm run dev</p>
              </div>
           </section>

           <section className="space-y-4">
              <h4 className="text-xs font-black uppercase text-amber-400 tracking-widest flex items-center gap-2">
                <span>2️⃣</span> วิธีแปลงเป็นแอปมือถือ (Android APK / iOS)
              </h4>
              <p className="text-[11px] text-zinc-400 leading-relaxed">
                ใช้เครื่องมือยอดนิยม <strong className="text-white">Capacitor</strong> เพื่อแปลงเว็บแอปนี้เป็น Native App ได้ในไม่กี่คำสั่ง:
              </p>
              <div className="p-4 tactile-inset font-mono text-[11px] text-zinc-300 space-y-2 border border-white/5 rounded-xl">
                 <p className="text-zinc-500"># บิลด์เว็บโค้ดก่อน</p>
                 <p className="text-emerald-400 font-bold">npm run build</p>
                 <p className="text-zinc-500 mt-2"># ติดตั้ง Capacitor</p>
                 <p className="text-emerald-400 font-bold">npm install @capacitor/core @capacitor/cli</p>
                 <p className="text-emerald-400 font-bold">npx cap init "W3 Studio" "com.w3.studio" --web-dir dist</p>
                 <p className="text-zinc-500 mt-2"># สำหรับ Android (เปิดใน Android Studio เพื่อสร้าง APK)</p>
                 <p className="text-emerald-400 font-bold">npm install @capacitor/android && npx cap add android</p>
                 <p className="text-emerald-400 font-bold">npx cap open android</p>
              </div>
           </section>

           <section className="space-y-4">
              <h4 className="text-xs font-black uppercase text-amber-400 tracking-widest flex items-center gap-2">
                <span>3️⃣</span> วิธีแปลงเป็นโปรแกรมคอมพิวเตอร์ (.exe / .dmg)
              </h4>
              <p className="text-[11px] text-zinc-400 leading-relaxed">
                ใช้ <strong className="text-white">Electron</strong> ครอบเว็บแอปเพื่อรันเป็นแอปเดสก์ท็อป ดูคู่มือฉบับเต็มได้ในไฟล์ <code className="text-amber-400">README.md</code> ที่มาพร้อมซอร์สโค้ด
              </p>
           </section>

           <section className="space-y-4 border-t border-white/10 pt-4">
              <h4 className="text-xs font-black uppercase text-emerald-400 tracking-widest flex items-center gap-2">
                <span>📱</span> หรือติดตั้งเป็น PWA บนโทรศัพท์/คอมพิวเตอร์ได้ทันที!
              </h4>
              <p className="text-[11px] text-zinc-300 leading-relaxed">
                ระบบนี้รองรับ <strong className="text-emerald-400">Progressive Web App (PWA)</strong> เมื่อเปิดผ่าน localhost หรือเว็บที่รองรับ ให้เลือก <span className="text-white font-bold">"เพิ่มลงในหน้าจอหลัก"</span> ในเบราว์เซอร์เพื่อทดลองใช้งานแบบหน้าต่างแอป การใช้งานแบบไม่ต่อเน็ตขึ้นกับการติดตั้งและแคชที่อุปกรณ์สร้างสำเร็จ โปรดทดสอบหลังเปิดใช้งานครั้งแรก
              </p>
           </section>
        </div>
      </Modal>

      {index.length === 0 && (
        <div className="mt-40 text-center opacity-20 flex flex-col items-center animate-pulse">
            <h2 className="text-6xl font-black mb-4 tracking-tighter italic text-white">VOID_EMPTY</h2>
            <p className="font-black uppercase tracking-[0.8em] text-[11px] text-zinc-400">Awaiting Core Initialization</p>
        </div>
      )}
    </div>
  );
};
