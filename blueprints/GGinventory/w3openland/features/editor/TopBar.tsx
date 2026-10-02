
import React, { useState, useEffect } from 'react';
import { Button } from '../../ui/components/Button';
import { StoryPack } from '../../types';

interface TopBarProps {
  story: StoryPack;
  isDirty: boolean;
  onSave: () => void;
  onExport: () => void;
  onExit: () => void;
  onUndo: () => void;
  onToggleTheme?: () => void;
}

export const TopBar: React.FC<TopBarProps> = ({ story, isDirty, onSave, onExport, onExit, onUndo, onToggleTheme }) => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

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
    <header className="h-16 border-b border-black/60 px-6 flex items-center justify-between bg-[#161618] z-50 shadow-2xl relative">
      <div className="flex items-center gap-6">
        <button onClick={onExit} className="text-2xl font-black text-white tracking-tighter uppercase italic glow-text hover:scale-105 transition-transform">W3.IDP</button>
        <div className="w-px h-8 bg-white/10"></div>
        <div className="flex flex-col">
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-400 shadow-[0_0_12px_#34d399]' : 'bg-amber-400 shadow-[0_0_12px_#fbbf24]'}`}></div>
            <span className="text-[9px] font-black uppercase tracking-[0.2em] text-zinc-200">
              {isOnline ? 'SYSTEM_STABLE' : 'ISOLATED_SYNC'}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="hidden md:flex flex-col items-end mr-2">
           <span className="text-[8px] font-black text-zinc-400 uppercase tracking-widest mb-0.5">Memory Status</span>
           <span className={`text-[10px] font-black ${isDirty ? 'text-[#fb923c] animate-pulse' : 'text-emerald-400'}`}>
             {isDirty ? 'PENDING_COMMIT' : 'ALL_SYNCHRONIZED'}
           </span>
        </div>
        <a 
          href="/w3-idp-studio-source.zip" 
          download="w3-idp-studio-source.zip"
          className="hidden sm:flex h-11 px-4 tactile-raised items-center gap-2 text-amber-400 hover:text-amber-300 font-black text-[9px] uppercase tracking-wider border border-amber-500/20 hover:border-amber-500/40 rounded-xl transition-all"
          title="ดาวน์โหลด Source Code โปรเจกต์ (.ZIP)"
        >
          <span>📦</span>
          <span>ZIP SOURCE</span>
        </a>
        <button 
          onClick={onToggleTheme} 
          className="w-10 h-10 tactile-raised flex items-center justify-center text-sm opacity-90 hover:opacity-100 hover:scale-110 transition-all border border-white/5"
          title="Toggle Protocol Theme"
        >
          🌓
        </button>
        <Button 
          variant={isDirty ? 'accent' : 'secondary'} 
          className={`h-11 px-8 text-[10px] font-black border border-white/20 shadow-xl ${isDirty ? 'animate-pulse' : ''}`} 
          onClick={onSave}
        >
          {isDirty ? '💾 COMMIT' : '✅ SYNCED'}
        </Button>
      </div>
    </header>
  );
};
