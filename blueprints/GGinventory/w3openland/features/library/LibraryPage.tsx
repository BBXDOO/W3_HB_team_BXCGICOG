
import React, { useState, useEffect, useRef } from 'react';
import { Button } from '../../ui/components/Button';
import { Card } from '../../ui/components/Card';
import { StoryIndexItem, getStoryIndex, deleteStory, importStory, saveStory } from '../../core/storage';
import { formatDate } from '../../core/utils';
import { Modal } from '../../ui/components/Modal';

interface LibraryPageProps {
  onOpenStory: (id: string) => void;
  onNewStory: () => void;
  canInstall?: boolean;
}

export const LibraryPage: React.FC<LibraryPageProps> = ({ onOpenStory, onNewStory }) => {
  const [index, setIndex] = useState<StoryIndexItem[]>([]);
  const [showHelp, setShowHelp] = useState(false);
  const [showExportModal, setShowExportModal] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    setIndex(getStoryIndex());
  }, []);

  const refreshIndex = () => setIndex(getStoryIndex());

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const story = await importStory(file);
    if (story) {
      saveStory(story);
      refreshIndex();
      alert(`กู้คืนจักรวาล "${story.title}" เรียบร้อยแล้วครับเพื่อน!`);
    }
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="min-h-screen p-6 md:p-16 max-w-7xl mx-auto overflow-y-auto bg-[#121214] scroll-container pb-60 relative">
      
      <header className="flex flex-col md:flex-row justify-between items-start md:items-end gap-10 mb-20 pb-12 relative z-10 border-b border-white/5">
        <div className="animate-in fade-in slide-in-from-left duration-700">
          <h1 className="text-5xl md:text-7xl font-black text-white tracking-tighter mb-4 uppercase italic leading-none glow-text">W3.REGISTRY</h1>
          <div className="flex items-center gap-4">
             <div className="w-12 h-1 bg-[#ea580c] shadow-[0_0_15px_#ea580c]"></div>
             <p className="text-[#ea580c] font-black uppercase tracking-[0.6em] text-[10px]">Physical Ecosystem Archive</p>
          </div>
        </div>
        <div className="flex flex-wrap gap-4 w-full md:w-auto animate-in fade-in slide-in-from-right duration-700">
          <input type="file" ref={fileInputRef} className="hidden" accept=".json" onChange={handleImport} />
          
          <button 
            onClick={() => setShowExportModal(true)}
            className="h-14 px-6 tactile-raised flex items-center gap-2 text-amber-400 hover:text-amber-300 font-black text-[10px] uppercase tracking-wider transition-all border border-amber-500/30 hover:border-amber-500/60 shadow-[0_0_15px_rgba(245,158,11,0.15)] hover:scale-105 active:scale-95"
          >
            📦 SOURCE CODE (.ZIP)
          </button>

          <Button variant="ghost" onClick={() => fileInputRef.current?.click()} className="h-14 px-8 tactile-raised text-zinc-300 font-black text-[10px] hover:text-white transition-all border border-white/5">
            📤 IMPORT REPOSITORY
          </Button>
          <Button variant="accent" onClick={onNewStory} className="h-14 md:h-16 px-12 text-[11px] font-black rounded-3xl shadow-2xl hover:scale-105 active:scale-95 transition-all">
            + INITIALIZE NEW CORE
          </Button>
        </div>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10 relative z-10">
        {index.map((item, idx) => (
          <div 
            key={item.storyId} 
            onClick={() => onOpenStory(item.storyId)}
            className="group cursor-pointer relative animate-in fade-in zoom-in duration-500"
            style={{ animationDelay: `${idx * 100}ms` }}
          >
            <Card className="p-8 relative h-[340px] flex flex-col justify-between transition-all duration-300 group-hover:-translate-y-2 overflow-hidden border border-white/10 shadow-2xl">
              <div className="flex justify-between items-start z-10">
                <div className="flex flex-col gap-1.5">
                   <span className="text-[9px] font-black text-emerald-400 uppercase tracking-[0.3em] bg-emerald-400/10 px-4 py-1.5 rounded-full border border-emerald-400/20 w-fit shadow-inner">VERIFIED_ACTIVE</span>
                </div>
                <button 
                  className="opacity-0 group-hover:opacity-100 text-red-500 transition-all p-2 bg-black/40 rounded-xl hover:bg-red-500 hover:text-white" 
                  onClick={(e) => { e.stopPropagation(); if(confirm('ต้องการลบ "จักรวาล" ชิ้นนี้ใช่หรือไม่?')) { deleteStory(item.storyId); refreshIndex(); } }}
                >
                  ✕
                </button>
              </div>

              <div className="flex-1 flex flex-col justify-center py-6 z-10">
                <h3 className="text-2xl font-black text-white tracking-tighter leading-tight group-hover:text-[#ea580c] transition-colors uppercase italic break-all line-clamp-3">
                  {item.title || 'UNNAMED_ENTITY'}
                </h3>
                <div className="flex flex-col gap-2 mt-6">
                  <p className="text-[9px] text-zinc-400 font-black uppercase tracking-[0.2em]">UID: <span className="text-zinc-300">{item.storyId.slice(-12)}</span></p>
                  <p className="text-[9px] text-emerald-500/80 font-black uppercase tracking-[0.2em]">STORAGE: <span className="text-emerald-400">STABLE_SSD</span></p>
                </div>
              </div>

              <div className="pt-6 border-t border-white/10 flex justify-between items-end z-10">
                <div className="flex flex-col">
                   <span className="text-[8px] text-zinc-400 font-black uppercase tracking-[0.3em] mb-1">Last Revision</span>
                   <span className="text-[10px] text-white font-bold">{formatDate(item.updatedAt)}</span>
                </div>
                <div className="w-12 h-12 tactile-raised flex items-center justify-center text-[#ea580c] group-hover:bg-[#ea580c] group-hover:text-white transition-all duration-300 shadow-xl border border-white/10">
                   <span className="text-xl font-black">→</span>
                </div>
              </div>
            </Card>
          </div>
        ))}

        <button 
          className="h-[340px] tactile-inset border-2 border-dashed border-white/10 flex flex-col items-center justify-center gap-6 group hover:bg-white/5 transition-all animate-in fade-in"
          onClick={onNewStory}
          style={{ animationDelay: `${index.length * 100}ms` }}
        >
          <div className="w-16 h-16 tactile-raised flex items-center justify-center text-3xl text-zinc-400 group-hover:text-[#ea580c] transition-all duration-500 border border-white/5">＋</div>
          <div className="flex flex-col items-center gap-1">
            <span className="text-[11px] font-black text-zinc-300 uppercase tracking-[0.4em] group-hover:text-white">Add Memory Block</span>
            <span className="text-[8px] text-zinc-500 font-bold uppercase tracking-[0.2em]">Initialize fresh ecosystem</span>
          </div>
        </button>
      </section>

      <footer className="mt-40 border-t border-white/10 pt-12 flex flex-col items-center gap-6 opacity-40 hover:opacity-100 transition-opacity duration-1000">
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

      <Modal isOpen={showExportModal} title="📦 DOWNLOAD SOURCE CODE & BUILD APP" onClose={() => setShowExportModal(false)}>
        <div className="flex flex-col gap-6 py-2 text-zinc-300 max-h-[75vh] overflow-y-auto scroll-container pr-2">
           <div className="p-6 tactile-inset border border-amber-500/20 bg-amber-500/5 rounded-2xl flex flex-col items-center text-center gap-3">
              <span className="text-4xl">⚡</span>
              <h3 className="text-base font-black text-white uppercase tracking-wider">ดาวน์โหลดซอร์สโค้ดฉบับสมบูรณ์ (.ZIP)</h3>
              <p className="text-xs text-zinc-300 max-w-md">
                ไฟล์ ZIP บรรจุโค้ดทั้งหมด (React 19, TypeScript, Vite, Tailwind CSS, Features ทั้งหมด) พร้อมไฟล์ตั้งค่าและ README ภาษาไทย
              </p>
              
              <a 
                href="/w3-idp-studio-source.zip" 
                download="w3-idp-studio-source.zip"
                className="mt-2 w-full py-4 px-6 bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-400 hover:to-orange-500 text-black font-black text-xs rounded-xl shadow-[0_0_20px_rgba(245,158,11,0.4)] hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-3 text-center uppercase tracking-widest"
              >
                <span>💾 คลิกเพื่อดาวน์โหลด w3-idp-studio-source.zip</span>
              </a>
           </div>

           <section className="space-y-4">
              <h4 className="text-xs font-black uppercase text-amber-400 tracking-widest flex items-center gap-2">
                <span>1️⃣</span> วิธีรันบนเครื่องของคุณ (Localhost)
              </h4>
              <div className="p-4 tactile-inset font-mono text-[11px] text-zinc-300 space-y-2 border border-white/5 rounded-xl">
                 <p className="text-zinc-500"># 1. แตกไฟล์ zip แล้วเข้าไปในโฟลเดอร์</p>
                 <p className="text-emerald-400 font-bold">cd w3-idp-studio</p>
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
                ใช้ <strong className="text-white">Electron</strong> ครอบเว็บแอปเพื่อรันเป็นแอปเดสก์ท็อป ดูคู่มือฉบับเต็มได้ในไฟล์ <code className="text-amber-400">README.md</code> ใน ZIP
              </p>
           </section>

           <section className="space-y-4 border-t border-white/10 pt-4">
              <h4 className="text-xs font-black uppercase text-emerald-400 tracking-widest flex items-center gap-2">
                <span>📱</span> หรือติดตั้งเป็น PWA บนโทรศัพท์/คอมพิวเตอร์ได้ทันที!
              </h4>
              <p className="text-[11px] text-zinc-300 leading-relaxed">
                ระบบนี้เป็น <strong className="text-emerald-400">Progressive Web App (PWA)</strong> ในตัว: เพียงเปิด URL เว็บนี้ในโทรศัพท์ แล้วกด <span className="text-white font-bold">"เพิ่มลงในหน้าจอหลัก" (Add to Home screen)</span> จะได้ไอคอนแอปบนหน้าจอที่เปิดใช้งานได้เต็มจอและ Offline ได้ทันทีโดยไม่ต้องเขียนโค้ดเพิ่มครับ!
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
