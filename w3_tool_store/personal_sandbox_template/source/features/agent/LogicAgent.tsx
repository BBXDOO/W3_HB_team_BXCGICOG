import React from 'react';
import { StoryPack, TabId } from '../../types';

interface LogicAgentProps {
  story: StoryPack;
  activeTab: TabId;
  selectedId: string | null;
  onApplyFix: (updatedStory: StoryPack) => void;
  isOpen: boolean;
  onClose: () => void;
}

export const LogicAgent: React.FC<LogicAgentProps> = ({ activeTab, isOpen, onClose }) => {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-[9999] bg-black/70 flex items-center justify-center p-4" role="presentation" onClick={onClose}>
      <section role="dialog" aria-modal="true" aria-label="Nexus AI" className="w-full max-w-md rounded-3xl border border-emerald-500/30 bg-[#18231c] p-6 text-zinc-100 shadow-2xl" onClick={e => e.stopPropagation()}>
        <h2 className="text-lg font-bold text-emerald-300">Nexus AI</h2>
        <p className="mt-3 text-sm leading-7">โหมดออฟไลน์กำลังทำงาน หน้านี้ ({activeTab}) ยังไม่ได้เชื่อมผู้ช่วย AI ภายนอก จึงไม่มีการส่งเนื้อหาโครงการหรือไฟล์ออกจากเครื่อง</p>
        <p className="mt-3 text-sm text-zinc-400">สามารถเพิ่มช่องทางเชื่อมต่อที่เลือกเปิดเองได้ในภายหลัง</p>
        <button type="button" onClick={onClose} className="mt-6 rounded-xl bg-emerald-700 px-5 py-3 text-sm font-bold">ปิด</button>
      </section>
    </div>
  );
};
