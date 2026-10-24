
import React from 'react';
import { TabId } from '../../types';
import { NavIcon } from '../../ui/components/NavIcon';

interface LeftNavProps {
  activeTab: TabId;
  onTabChange: (tab: TabId) => void;
  onToggleFormat: () => void;
  isFormatOpen: boolean;
  isDirty?: boolean;
  onSave?: () => void;
}

export const LeftNav: React.FC<LeftNavProps> = ({ 
  activeTab, 
  onTabChange, 
  onToggleFormat,
  isFormatOpen,
  isDirty,
  onSave
}) => {
  const tabs: { id: TabId; label: string }[] = [
    { id: 'home', label: 'Home' },
    { id: 'story', label: 'Story' },
    { id: 'character', label: 'Characters' },
    { id: 'card', label: 'Cards' },
    { id: 'board', label: 'Board' },
    { id: 'location', label: 'Locations' },
    { id: 'item', label: 'Items' },
    { id: 'event', label: 'Events' },
    { id: 'rule', label: 'Rules' },
    { id: 'commonPlay', label: 'Common Play' },
    { id: 'play', label: 'Playtest' },
  ];

  return (
    <nav className="w-14 md:w-64 border-r border-[#426a59]/50 flex flex-col bg-[#101813] overflow-hidden z-40 transition-all shadow-[10px_0_30px_rgba(0,0,0,0.3)]">
      <div className="p-6 md:p-8 hidden md:block border-b border-white/10 bg-[#18231c]">
        <h1 className="text-xl font-black text-white tracking-tighter italic glow-text">PERSONAL SANDBOX</h1>
        <div className="h-1 w-12 bg-[#65ad8d] mt-2"></div>
      </div>
      
      <div className="flex-1 pt-4 md:pt-4 overflow-y-auto scroll-container px-3 flex flex-col gap-3">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`
              w-full flex flex-col md:flex-row items-center gap-1 md:gap-4 px-2 md:px-5 py-3 md:py-4 transition-all relative rounded-2xl group
              ${activeTab === tab.id 
                ? 'border border-[#65ad8d]/40 border-l-4 border-l-[#65ad8d] text-white font-black shadow-lg bg-[#284236]' 
                : 'text-zinc-300 hover:text-white hover:bg-white/5'
              }
            `}
          >
            <span className={`transition-all duration-300 ${activeTab === tab.id ? 'text-[#9ed3b5]' : 'text-[#d5d8d4] opacity-80 group-hover:opacity-100'}`}>
              <NavIcon name={tab.id} />
            </span>
            <span className="text-[8px] md:text-[10px] uppercase font-black tracking-[0.2em] md:block hidden">
              {tab.label}
            </span>
          </button>
        ))}

        <div className="mt-4 pt-4 border-t border-white/10">
           <button
            onClick={onToggleFormat}
            aria-label="จัดรูปแบบเนื้อหา"
            className={`
              w-full flex flex-col md:flex-row items-center gap-1 md:gap-4 px-2 md:px-5 py-4 transition-all rounded-2xl group
              ${isFormatOpen ? 'bg-[#284236] text-[#9ed3b5] border border-[#65ad8d]/40' : 'text-zinc-300 hover:text-white hover:bg-white/5'}
            `}
          >
            <NavIcon name="ai" className={isFormatOpen ? 'animate-pulse' : 'opacity-70 group-hover:opacity-100'} />
            <span className="text-[8px] md:text-[10px] uppercase font-black tracking-[0.2em] md:block hidden">
              FONT EDIT
            </span>
          </button>
        </div>
      </div>
      
      <div className="mt-auto p-4 md:p-6 flex flex-col gap-4 border-t border-white/10 bg-[#18231c]">
        {isDirty && (
          <button 
            onClick={onSave}
            className="w-full py-4 bg-[#28755f] text-white rounded-[20px] text-[10px] font-black uppercase tracking-[0.2em] shadow-2xl hover:bg-[#348b70] transition-all active:scale-95 border border-white/20"
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
