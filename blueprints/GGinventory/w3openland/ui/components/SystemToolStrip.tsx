
import React from 'react';
import { getStatusColor, SPECIAL_STATUS } from '../../core/utils';

interface SystemToolStripProps {
  onSearch?: () => void;
  onAdd?: () => void;
  onExport?: () => void;
  onToggleTheme?: () => void;
  onToggleAgent?: () => void;
  isAgentOpen?: boolean;
}

export const SystemToolStrip: React.FC<SystemToolStripProps> = ({ 
  onSearch, onAdd, onExport, onToggleTheme, onToggleAgent, isAgentOpen 
}) => {
  return (
    <div className="h-full flex flex-col gap-6 p-2 md:p-3 overflow-y-auto overflow-x-hidden items-center">
      
      {/* Utility Actions */}
      <div className="flex flex-col gap-3 w-full">
        <button onClick={onSearch} className="w-full aspect-square w3-card-inset flex items-center justify-center text-[11px] clickable hover:text-blue-500 transition-all border-white/5" title="Search">🔍</button>
        <button onClick={onAdd} className="w-full aspect-square w3-card-inset text-emerald-500 flex items-center justify-center text-lg clickable hover:bg-emerald-500/10 transition-all border-white/5" title="Add">+</button>
        <button onClick={onExport} className="w-full aspect-square w3-card-inset flex items-center justify-center text-[11px] clickable hover:text-blue-500 transition-all border-white/5" title="Export">📤</button>
      </div>

      <div className="mt-auto flex flex-col gap-3 w-full pb-4">
        {/* Special Status Icons (Small circular indicators) */}
        <div className="flex flex-col gap-2 border-t border-white/5 pt-6 items-center">
           {Object.entries(SPECIAL_STATUS).map(([key, info]) => (
            <div 
              key={key} 
              className="w-2 h-2 rounded-full border border-white/10" 
              style={{ backgroundColor: info.color }}
              title={info.label}
            />
          ))}
        </div>

        <button 
          onClick={onToggleAgent} 
          className={`w-full aspect-square rounded-2xl transition-all flex items-center justify-center text-xl clickable border-2 
            ${isAgentOpen ? 'bg-blue-600 border-blue-400 text-white shadow-lg animate-pulse' : 'bg-[var(--surface)] border-white/10 text-gray-500 hover:text-white'}
          `} 
          title="Nexus Agent"
        >
          🧠
        </button>
      </div>
    </div>
  );
};
