
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
    { id: 'home', label: 'หน้าแรก' },
    { id: 'story', label: 'เรื่องราว' },
    { id: 'character', label: 'ตัวละคร' },
    { id: 'card', label: 'การ์ด' },
    { id: 'board', label: 'บอร์ด' },
    { id: 'location', label: 'สถานที่' },
    { id: 'item', label: 'ไอเทม' },
    { id: 'event', label: 'เหตุการณ์' },
    { id: 'rule', label: 'กฎ' },
    { id: 'commonPlay', label: 'คำสั่ง' },
    { id: 'play', label: 'ทดลอง' },
  ];

  return (
    <nav className="ps-nav w-14 md:w-64 border-r flex flex-col overflow-hidden z-40 transition-all">
      <div className="p-6 md:p-8 hidden md:block border-b border-white/10">
        <h1 className="text-xl font-black text-white tracking-tighter italic glow-text">PERSONAL SANDBOX</h1>
        <div className="h-1 w-12 bg-[var(--accent)] mt-2"></div>
      </div>
      
      <div className="flex-1 pt-4 md:pt-4 overflow-y-auto scroll-container px-3 flex flex-col gap-3">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            title={tab.label}
            aria-label={tab.label}
            aria-current={activeTab === tab.id ? 'page' : undefined}
            onClick={() => onTabChange(tab.id)}
            className={`
              w-full flex flex-col md:flex-row items-center gap-1 md:gap-4 px-2 md:px-5 py-3 md:py-4 transition-all relative rounded-2xl group
              ${activeTab === tab.id 
                ? 'ps-nav-active border border-l-4 text-white font-black shadow-lg' 
                : 'text-zinc-300 hover:text-white hover:bg-white/5'
              }
            `}
          >
            <span className={`transition-all duration-300 ${activeTab === tab.id ? 'text-[var(--accent)]' : 'text-[#bfc0ce] opacity-80 group-hover:opacity-100'}`}>
              <NavIcon name={tab.id} />
            </span>
            <span className="ps-nav-label">
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
              ${isFormatOpen ? 'ps-nav-active text-[var(--accent)] border' : 'text-zinc-300 hover:text-white hover:bg-white/5'}
            `}
          >
            <NavIcon name="ai" className={isFormatOpen ? 'animate-pulse' : 'opacity-70 group-hover:opacity-100'} />
            <span className="ps-nav-label">
              รูปแบบ
            </span>
          </button>
        </div>
      </div>
      
      <div className="mt-auto p-4 md:p-6 flex flex-col gap-4 border-t border-white/10">
        {isDirty && (
          <button 
            onClick={onSave}
            className="w-full py-4 bg-[var(--accent)] text-white rounded-[20px] text-[10px] font-black uppercase tracking-[0.2em] shadow-2xl hover:brightness-110 transition-all active:scale-95 border border-white/20"
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
