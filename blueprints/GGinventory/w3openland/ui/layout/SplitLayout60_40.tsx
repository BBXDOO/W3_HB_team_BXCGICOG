
import React from 'react';
import { SystemToolStrip } from '../components/SystemToolStrip';

interface SplitLayout60_40Props {
  topLeft: React.ReactNode;
  topRight: React.ReactNode;
  bottomMain: React.ReactNode;
  showTools?: boolean;
  toolActions?: {
    onSearch?: () => void;
    onAdd?: () => void;
    onExport?: () => void;
    onToggleTheme?: () => void;
    onToggleAgent?: () => void;
    isAgentOpen?: boolean;
  };
  children?: React.ReactNode;
}

export const SplitLayout60_40: React.FC<SplitLayout60_40Props> = ({ 
  topLeft, 
  topRight, 
  bottomMain, 
  showTools = true,
  toolActions,
  children
}) => {
  return (
    <div className="h-full w-full flex flex-col bg-[var(--bg)] overflow-hidden">
      {/* 
        TOP SECTION
        Selection Pane (Left) and Detail Pane (Right)
      */}
      <div className="flex-[6] flex flex-col md:flex-row border-b border-[var(--border)] min-h-0 overflow-hidden">
        {/* Selection Pane */}
        <div className="h-[40%] md:h-full md:flex-[3.5] border-b md:border-b-0 md:border-r border-[var(--border)] bg-[var(--surface-2)] scroll-container min-w-0">
          {topLeft}
        </div>
        
        {/* Detail Pane */}
        <div className="h-[60%] md:h-full md:flex-[6.5] bg-[var(--surface)] scroll-container min-w-0">
          <div className="h-full">
            {topRight}
          </div>
        </div>
      </div>

      {/* 
        BOTTOM SECTION
        Monitor Area and Tool Strip
      */}
      <div className="flex-[4] flex min-h-0 overflow-hidden bg-[var(--surface)]">
        
        {/* Tool Strip: MOVED FROM RIGHT TO LEFT AS REQUESTED */}
        {showTools && (
          <div className="w-[50px] md:w-[60px] border-r border-[var(--border)] bg-[var(--surface-2)] flex flex-col shrink-0">
            <SystemToolStrip {...toolActions} />
          </div>
        )}

        {/* Monitor Area */}
        <div className="flex-1 scroll-container relative w-full">
          <div className="min-h-full w-full">
            {bottomMain}
          </div>
        </div>

      </div>

      {children}
    </div>
  );
}
