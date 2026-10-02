
import React from 'react';
import { TabId } from '../../types';

interface LeftNavProps {
  activeTab: TabId;
  onTabChange: (tab: TabId) => void;
  onToggleAgent: () => void;
  isAgentOpen: boolean;
  isDirty?: boolean;
  onSave?: () => void;
}

export const LeftNav: React.FC<LeftNavProps> = ({ 
  activeTab, 
  onTabChange, 
  onToggleAgent, 
  isAgentOpen,
  isDirty,
  onSave
}) => {
  const tabs: { id: TabId; label: string; icon: string }[] = [
    { id: 'home', label: 'Home', icon: '🏠' },
    { id: 'story', label: 'Story', icon: '📝' },
    { id: 'character', label: 'Characters', icon: '👥' },
    { id: 'card', label: 'Cards', icon: '⚡' },
    { id: 'board', label: 'Board', icon: '🗺️' },
    { id: 'location', label: 'Locations', icon: '🏰' },
    { id: 'item', label: 'Items', icon: '🎒' },
    { id: 'event', label: 'Events', icon: '⚡' },
    { id: 'rule', label: 'Rules', icon: '⚖️' },
    { id: 'play', label: 'Playtest', icon: '🎮' },
  ];

  return (
    <nav className="w-14 md:w-64 border-r border-black/40 flex flex-col bg-[#121214] overflow-hidden z-40 transition-all shadow-[10px_0_30px_rgba(0,0,0,0.5)]">
      <div className="p-6 md:p-8 hidden md:block border-b border-white/5 bg-[#161618]">
        <h1 className="text-2xl font-black text-white tracking-tighter italic glow-text">W3.IDP</h1>
        <div className="h-1 w-12 bg-[#ea580c] mt-2 shadow-[0_0_15px_#ea580c]"></div>
      </div>
      
      <div className="flex-1 pt-4 md:pt-4 overflow-y-auto scroll-container px-3 flex flex-col gap-3">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`
              w-full flex flex-col md:flex-row items-center gap-1 md:gap-4 px-2 md:px-5 py-3 md:py-4 transition-all relative rounded-2xl group
              ${activeTab === tab.id 
                ? 'tactile-raised border-l-4 border-l-[#ea580c] text-white font-black shadow-lg bg-[#27272a]' 
                : 'text-zinc-300 hover:text-white hover:bg-white/5'
              }
            `}
          >
            <span className={`text-base md:text-lg transition-all duration-300 ${activeTab === tab.id ? 'scale-110' : 'opacity-80 grayscale group-hover:grayscale-0 group-hover:opacity-100'}`}>
              {tab.icon}
            </span>
            <span className="text-[8px] md:text-[10px] uppercase font-black tracking-[0.2em] md:block hidden">
              {tab.label}
            </span>
          </button>
        ))}

        <div className="mt-4 pt-4 border-t border-white/10">
           <button
            onClick={onToggleAgent}
            className={`
              w-full flex flex-col md:flex-row items-center gap-1 md:gap-4 px-2 md:px-5 py-4 transition-all rounded-2xl group
              ${isAgentOpen ? 'tactile-raised bg-blue-900/20 text-blue-400 border border-blue-500/30' : 'text-zinc-300 hover:text-white hover:bg-white/5'}
            `}
          >
            <span className={`text-xl md:text-2xl transition-all ${isAgentOpen ? 'animate-pulse' : 'grayscale opacity-70 group-hover:opacity-100'}`}>🧠</span>
            <span className="text-[8px] md:text-[10px] uppercase font-black tracking-[0.2em] md:block hidden">
              NEXUS AI
            </span>
          </button>
        </div>
      </div>
      
      <div className="mt-auto p-4 md:p-6 flex flex-col gap-4 border-t border-white/5 bg-[#161618]">
        {isDirty && (
          <button 
            onClick={onSave}
            className="w-full py-4 bg-[#ea580c] text-white rounded-[20px] text-[10px] font-black uppercase tracking-[0.2em] shadow-2xl hover:bg-[#f97316] transition-all active:scale-95 border border-white/20"
          >
            💾 COMMIT CHANGES
          </button>
        )}
        
        <div className="tactile-inset p-3 text-[8px] md:text-[9px] text-zinc-200 uppercase font-black tracking-[0.4em] text-center border border-white/10 shadow-lg">
          ENGINE_V0.5.TACTILE
        </div>
      </div>
    </nav>
  );
};
