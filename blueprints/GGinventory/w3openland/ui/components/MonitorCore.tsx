
import React from 'react';

interface MonitorCoreProps {
  title: string;
  modeLabel?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  emptyState?: {
    title: string;
    description: string;
    actionLabel?: string;
    onAction?: () => void;
  };
  isEmpty?: boolean;
}

export const MonitorCore: React.FC<MonitorCoreProps> = ({ 
  title, 
  modeLabel = 'PREVIEW', 
  children, 
  footer,
  emptyState,
  isEmpty 
}) => {
  return (
    <div className="h-full w-full p-2 md:p-3 flex flex-col overflow-hidden">
      <div className="tactile-raised flex flex-col h-full overflow-hidden bg-[#0d0d0f] shadow-[0_30px_60px_rgba(0,0,0,0.6)] relative border border-white/5">
        {/* Header */}
        <div className="p-4 border-b border-black/40 bg-[#161618] flex justify-between items-center relative z-10 shadow-md">
          <div className="flex items-center gap-4">
            <div className="w-2 h-2 rounded-full bg-[#c2410c] shadow-[0_0_10px_#c2410c]"></div>
            <h2 className="text-[9px] md:text-[10px] font-black uppercase tracking-[0.4em] text-zinc-300">{title}</h2>
            <span className="px-3 py-0.5 rounded-full text-[8px] font-black bg-[#c2410c]/20 text-[#ea580c] border border-[#c2410c]/40">
              {modeLabel}
            </span>
          </div>
        </div>

        {/* Content Viewport */}
        <div className="flex-1 overflow-y-auto overflow-x-hidden p-6 relative z-10 scroll-container">
          {isEmpty && emptyState ? (
            <div className="h-full flex flex-col items-center justify-center text-center p-4">
              <div className="text-5xl mb-6 opacity-40">⚙️</div>
              <h3 className="text-sm font-black text-zinc-300 uppercase tracking-[0.4em] mb-2">{emptyState.title}</h3>
              <p className="text-[11px] text-zinc-400 mb-8 max-w-md leading-relaxed italic">{emptyState.description}</p>
              {emptyState.onAction && (
                <button 
                  onClick={emptyState.onAction}
                  className="px-8 py-3 bg-[#c2410c] text-white text-[10px] font-black uppercase tracking-[0.3em] rounded-2xl shadow-xl hover:bg-[#ea580c] transition-all"
                >
                  {emptyState.actionLabel || '+ INITIALIZE'}
                </button>
              )}
            </div>
          ) : (
            <div className="w-full h-full relative">
              {children}
            </div>
          )}
        </div>

        {/* Footer */}
        {footer && (
          <div className="h-14 px-8 bg-[#161618] border-t border-black/40 flex items-center justify-between shrink-0 relative z-10">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
};
