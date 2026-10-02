import React from 'react';
import { Button } from './Button';

interface ModalProps {
  isOpen: boolean;
  title: string;
  onClose: () => void;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({ isOpen, title, onClose, children, footer }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-black/70 backdrop-blur-md animate-in fade-in duration-200">
      <div className="w3-card w-full max-w-lg overflow-hidden flex flex-col max-h-[90vh] shadow-[0_0_50px_rgba(0,0,0,0.5)] border border-white/10">
        <div className="px-6 py-4 border-b border-white/5 bg-[var(--surface)] flex justify-between items-center">
          <h2 className="text-lg font-black text-[var(--text)] uppercase tracking-tighter">{title}</h2>
          <Button variant="ghost" className="px-2 h-8 w-8 rounded-full" onClick={onClose}>✕</Button>
        </div>
        <div className="px-6 py-6 overflow-y-auto flex-1 bg-[var(--surface-2)]">
          {children}
        </div>
        <div className="px-6 py-4 border-t border-white/5 bg-[var(--surface)] flex justify-end gap-3">
          {footer ? footer : <Button onClick={onClose}>Close Protocol</Button>}
        </div>
      </div>
    </div>
  );
};