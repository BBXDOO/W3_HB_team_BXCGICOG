
import React, { useState, useEffect } from 'react';
import { Button } from '../../ui/components/Button';
import { StoryPack, UITheme } from '../../types';
import guide from '../../docs/คู่มือใช้งานภาษาไทย.md?raw';

interface TopBarProps {
  navigationCollapsed: boolean;
  onToggleNavigation: () => void;
  story: StoryPack;
  isDirty: boolean;
  onSave: () => void;
  onExport: () => void;
  onExit: () => void;
  onUndo: () => void;
  onToggleTheme?: () => void;
  currentTheme: UITheme;
  onSelectTheme: (theme: UITheme) => void;
  customThemeColor: string;
  onSelectCustomColor: (color: string) => void;
  onChooseBackgroundImage: (file: File) => void;
  onClearBackgroundImage: () => void;
  hasBackgroundImage: boolean;
}

export const TopBar: React.FC<TopBarProps> = ({ navigationCollapsed, onToggleNavigation, story, isDirty, onSave, onExport, onExit, onUndo, currentTheme, onSelectTheme, customThemeColor, onSelectCustomColor, onChooseBackgroundImage, onClearBackgroundImage, hasBackgroundImage }) => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [guideOpen, setGuideOpen] = useState(false);
  const [appearanceOpen, setAppearanceOpen] = useState(false);

  useEffect(() => {
    const handleStatus = () => setIsOnline(navigator.onLine);
    window.addEventListener('online', handleStatus);
    window.addEventListener('offline', handleStatus);
    return () => {
      window.removeEventListener('online', handleStatus);
      window.removeEventListener('offline', handleStatus);
    };
  }, []);

  return (
    <header className="ps-topbar h-16 border-b px-2 md:px-6 flex items-center justify-between gap-2 z-50 relative">
      <div className="ps-brand-group">
        <button type="button" aria-label="ย่อหรือขยายเมนู" aria-expanded={!navigationCollapsed} onClick={onToggleNavigation} className="ps-menu-toggle">☰</button>
        <button onClick={onExit} className="ps-brand" title="กลับไปคลังโครงการ"><span className="ps-brand-long">PERSONAL </span>SANDBOX<small>WORKSPACE / 0.50</small></button>
        <div className="hidden md:block w-px h-8 bg-white/10"></div>
        <div className="hidden md:flex flex-col">
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-400 shadow-[0_0_12px_#34d399]' : 'bg-amber-400 shadow-[0_0_12px_#fbbf24]'}`}></div>
            <span className="text-[9px] font-black uppercase tracking-[0.2em] text-zinc-200">
              {isOnline ? 'SYSTEM_STABLE' : 'ISOLATED_SYNC'}
            </span>
          </div>
        </div>
      </div>
      {guideOpen && <div className="fixed inset-0 z-[9999] bg-black/80 p-3 md:p-8 flex items-center justify-center" onClick={() => setGuideOpen(false)}>
        <section role="dialog" aria-modal="true" aria-label="คู่มือภาษาไทย" className="ps-dialog max-w-3xl w-full max-h-[85vh] flex flex-col text-slate-100 rounded-2xl border shadow-2xl" onClick={event => event.stopPropagation()}>
          <div className="p-4 border-b border-white/10 flex items-center justify-between"><h2 className="font-bold">คู่มือภาษาไทย</h2><button onClick={() => setGuideOpen(false)} className="p-2">ปิด ✕</button></div>
          <div className="p-5 overflow-y-auto whitespace-pre-wrap text-sm leading-7">{guide}</div>
        </section>
      </div>}

      <div className="ps-topbar-actions shrink-0">
        <button type="button" onClick={() => setGuideOpen(true)} className="text-xs border border-emerald-500/30 text-emerald-200 rounded-xl p-2" title="คู่มือภาษาไทย"><span>?<span className="ps-control-label"> คู่มือ</span></span></button>
        <button id="w3-check-update" type="button" aria-label="ตรวจอัปเดตแอป" onClick={() => {
          const bridge = (window as unknown as { AndroidBridge?: { checkUpdate?: () => void } }).AndroidBridge;
          if (bridge?.checkUpdate) bridge.checkUpdate();
          else alert('ปุ่มอัปเดตใช้ได้ในแอป Android');
        }}>↑<span className="ps-control-label"> อัปเดต</span></button>
        <div className="hidden md:flex flex-col items-end mr-2">
           <span className="text-[8px] font-black text-zinc-400 uppercase tracking-widest mb-0.5">Memory Status</span>
           <span className={`text-[10px] font-black ${isDirty ? 'text-[#9ed3b5] animate-pulse' : 'text-emerald-400'}`}>
             {isDirty ? 'PENDING_COMMIT' : 'ALL_SYNCHRONIZED'}
           </span>
        </div>
        <button type="button" onClick={onExport} className="flex h-11 px-2 md:px-4 tactile-raised items-center gap-2 text-amber-400 font-black text-[9px] uppercase tracking-wider border border-amber-500/20 rounded-xl" title="สำรองโครงการพร้อมจุดเล่นล่าสุดที่บันทึกเป็น JSON" aria-label="สำรองโครงการและจุดเล่น"><span>⇧<span className="ps-control-label"> ส่งออก</span></span></button>
        <button type="button" onClick={() => setAppearanceOpen(true)}
          className="flex w-10 h-10 tactile-raised items-center justify-center text-sm border border-white/5"
          title="สีและภาพพื้นหลัง" aria-label="เลือกสีและภาพพื้นหลัง">ธีม</button>
        <Button 
          variant={isDirty ? 'accent' : 'secondary'} 
          className={`h-11 px-3 md:px-8 text-[10px] font-black border border-white/20 shadow-xl ${isDirty ? 'animate-pulse' : ''}`} 
          onClick={onSave}
        >
          {isDirty ? 'บันทึก' : '✓'}
        </Button>
      </div>
      {appearanceOpen && <div className="fixed inset-0 z-[9999] bg-black/75 flex items-center justify-center p-4" onClick={() => setAppearanceOpen(false)}>
        <section role="dialog" aria-modal="true" aria-label="สีและภาพพื้นหลัง" className="ps-dialog w-full max-w-sm rounded-2xl p-5 border text-white shadow-2xl" onClick={event => event.stopPropagation()}>
          <div className="flex justify-between items-center mb-4"><h2 className="font-bold">ธีมและภาพพื้นที่ทำงาน</h2><button type="button" onClick={() => setAppearanceOpen(false)} aria-label="ปิด">✕</button></div>
          <p className="text-xs text-slate-300 mb-2">แตะสีเพื่อเลือกธีมของทุกหน้า</p><div className="grid grid-cols-4 gap-3">
            {([
              ['darkNavy', 'ดำเทา Instrument', '#222326'],
              ['deepForest', 'เขียวป่า', '#17342a'],
              ['nightBlue', 'น้ำเงินกลางคืน', '#182b41'],
              ['aubergine', 'ม่วงหม่น', '#352535'],
              ['softLight', 'สว่างนวล', '#e3e8e2']
            ] as [UITheme, string, string][]).map(([theme, label, color]) => (
              <button type="button" key={theme} onClick={() => onSelectTheme(theme)} aria-label={label} aria-pressed={currentTheme === theme} title={label}
                className={`h-14 rounded-xl border-4 ${currentTheme === theme ? 'border-white ring-2 ring-emerald-400' : 'border-white/20'}`} style={{ backgroundColor: color, color: theme === 'softLight' ? '#10251d' : '#fff' }}>{currentTheme === theme ? '✓' : ''}</button>
            ))}
          </div>
          <label className="flex items-center justify-between mt-4 text-sm">สีที่กำหนดเอง <input type="color" value={currentTheme === 'custom' ? customThemeColor : '#368a77'} onChange={e => onSelectCustomColor(e.target.value)} className="w-16 h-11 rounded cursor-pointer" aria-label="เลือกสีธีมที่กำหนดเอง" /></label>
          <label className="block mt-4 p-3 text-center rounded-xl border border-dashed border-white/40 cursor-pointer">เลือกรูปจากเครื่องเป็นพื้นพื้นที่ทำงาน
            <input className="sr-only" type="file" accept="image/*" onChange={e => { const file = e.target.files?.[0]; if (file) onChooseBackgroundImage(file); e.target.value = ''; }} />
          </label>
          {hasBackgroundImage && <button type="button" className="mt-3 w-full p-2 text-amber-200" onClick={onClearBackgroundImage}>ลบรูปพื้นหลัง</button>}
          <p className="mt-3 text-xs text-slate-300">ภาพเก็บในโครงการและอยู่ในไฟล์สำรอง JSON เมนูใช้สีที่เลือกด้านบน</p>
        </section>
      </div>}
    </header>
  );
};
