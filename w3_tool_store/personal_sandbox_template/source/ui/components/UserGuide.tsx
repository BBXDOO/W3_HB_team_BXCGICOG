import React, { lazy, Suspense, useState } from 'react';
import guide from '../../docs/คู่มือใช้งานภาษาไทย.md?raw';
import { APP_VERSION_CODE } from '../../core/appVersion';

const MarkdownContent = lazy(() => import('../../features/story/MarkdownRenderer').then(module => ({ default: module.MarkdownContent })));

export const UserGuide: React.FC = () => {
  const [query, setQuery] = useState('');
  const sections = guide.split(/(?=^## )/m);
  const filtered = sections.filter(section => section.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase()));
  return <div className="user-guide flex flex-col min-h-0 flex-1">
    <label className="p-3 border-b border-white/10 text-sm">คู่มือที่มากับแอป v{APP_VERSION_CODE}
      <input type="search" aria-label="ค้นหาในคู่มือ" placeholder="ค้นหาชื่อเมนูหรือสิ่งที่ต้องการทำ" value={query} onChange={event => setQuery(event.target.value)}
        className="w-full mt-2 p-2 rounded-lg bg-[var(--surface-2)] text-[var(--text)] border border-[var(--border)]" />
    </label>
    <div className="p-4 overflow-y-auto min-h-0 flex-1 text-sm leading-7">
      {filtered.length ? <Suspense fallback={<p>กำลังเปิดคู่มือ…</p>}><MarkdownContent value={filtered.join('\n')} /></Suspense> : <p role="status">ไม่พบหัวข้อ ลองใช้ชื่อเมนูหรือคำอื่น</p>}
    </div>
  </div>;
};
