import { NavIcon } from '../components/NavIcon';
import { createPortal } from 'react-dom';
import React, { useEffect, useRef, useState } from 'react';

interface SplitLayout60_40Props {
  topLeft: React.ReactNode;
  topRight: React.ReactNode;
  bottomMain: React.ReactNode;
  previewKey?: string;
  defaultPreview?: number;
  mobileMaxPreview?: number;
  showTools?: boolean;
  toolActions?: {
    onSearch?: () => void;
    onAdd?: () => void;
    onExport?: () => void;
    onToggleTheme?: () => void;
    onToggleAgent?: () => void;
    onToggleCommands?: () => void;
    isAgentOpen?: boolean;
  };
  children?: React.ReactNode;
}


const MIN_PREVIEW = 12;
const MAX_PREVIEW = 70;
const DEFAULT_PREVIEW = 36;

export const SplitLayout60_40: React.FC<SplitLayout60_40Props> = ({
  topLeft, topRight, bottomMain, previewKey = 'w3.personal.preview-height-v7',
  defaultPreview = DEFAULT_PREVIEW, showTools = true, toolActions, children
}) => {
  const [host, setHost] = useState<HTMLElement | null>(null);
  const [stageHeight, setStageHeight] = useState(600);
  const [listOpen, setListOpen] = useState(false);
  const [previewHeight, setPreviewHeight] = useState(() => {
    try { const n = Number(localStorage.getItem(previewKey)); if (n >= MIN_PREVIEW && n <= MAX_PREVIEW) return n; } catch {}
    return defaultPreview;
  });
  const dragging = useRef(false);
  useEffect(() => {
    const target = document.getElementById('workspace-preview-host');
    setHost(target);
    const stage = target?.parentElement;
    if (!stage) return;
    const measure = () => setStageHeight(stage.getBoundingClientRect().height);
    measure();
    const observer = new ResizeObserver(measure);
    observer.observe(stage);
    return () => observer.disconnect();
  }, []);
  const setHeight = (height: number) => {
    const value = Math.max(MIN_PREVIEW, Math.min(MAX_PREVIEW, Math.round(height)));
    setPreviewHeight(value);
    try { localStorage.setItem(previewKey, String(value)); } catch {}
  };
  const moveHandle = (y: number) => {
    const bounds = host?.parentElement?.getBoundingClientRect();
    if (bounds) setHeight((bounds.bottom - y) / bounds.height * 100);
  };
  const preview = <div className="workspace-preview-shell" style={{ height: Math.round(stageHeight * previewHeight / 100) }}>
    <div className="workspace-divider">
      <button type="button" className="workspace-drag-handle" role="separator" aria-label="ปรับขนาดพื้นที่ผลลัพธ์"
        aria-orientation="horizontal" aria-valuemin={MIN_PREVIEW} aria-valuemax={MAX_PREVIEW} aria-valuenow={previewHeight}
        onPointerDown={e => { dragging.current = true; e.currentTarget.setPointerCapture(e.pointerId); }}
        onPointerMove={e => { if (dragging.current) moveHandle(e.clientY); }}
        onPointerUp={e => { if (dragging.current) moveHandle(e.clientY); dragging.current = false; }}
        onPointerCancel={() => { dragging.current = false; }} onDoubleClick={() => setHeight(defaultPreview)}
        onKeyDown={e => { if (['ArrowUp', 'ArrowDown'].includes(e.key)) { e.preventDefault(); setHeight(previewHeight + (e.key === 'ArrowUp' ? 5 : -5)); } }}
        title="ลากขึ้นลงเพื่อปรับพื้นที่ผลลัพธ์"><span /></button>
    </div>
    <section className="workspace-output" aria-label="พื้นที่แสดงผล">
      {showTools && toolActions && <div className="workspace-output-actions" aria-label="เครื่องมือพื้นที่แสดงผล">
        {toolActions.onSearch && <button type="button" onClick={toolActions.onSearch} aria-label="ค้นหา" className="workspace-action"><NavIcon name="search" /></button>}
        {toolActions.onAdd && <button type="button" onClick={toolActions.onAdd} aria-label="เพิ่มรายการ" className="workspace-action"><NavIcon name="add" /></button>}
        {toolActions.onExport && <button type="button" onClick={toolActions.onExport} aria-label="ส่งออก" className="workspace-action"><NavIcon name="export" /></button>}
        {toolActions.onToggleCommands && <button type="button" onClick={toolActions.onToggleCommands} aria-label="คำสั่งและคู่มือ" className="workspace-action"><NavIcon name="commonPlay" /></button>}
        {toolActions.onToggleAgent && <button type="button" onClick={toolActions.onToggleAgent} aria-label="เปิดหรือปิดผู้ช่วย" title="ขนาดและรูปแบบตัวหนังสือ" className="workspace-action ml-auto"><NavIcon name="ai" /></button>}
      </div>}
      <div className="workspace-output-content scroll-container">{bottomMain}</div>
    </section>
  </div>;
  return <div className="workspace-layout">
    <section className={`workspace-region ${listOpen ? 'workspace-show-list' : ''}`} aria-label="พื้นที่แก้ไข">
      <div className="workspace-toolbar"><span>EDITOR</span><button type="button" className="workspace-list-toggle" aria-expanded={listOpen} aria-controls="workspace-list" onClick={() => setListOpen(!listOpen)}>{listOpen ? 'กลับพื้นที่แก้ไข' : '☰ รายการ / เพิ่ม'}</button></div>
      <div className="workspace-panels">
        <div id="workspace-list" className="workspace-list">
          <div className="workspace-list-header"><span>รายการ / เพิ่ม</span><button type="button" aria-label="ปิดหน้าต่างรายการ" onClick={() => setListOpen(false)}>✕ ปิด</button></div>
          <div className="workspace-list-body scroll-container" onClick={e => { const b = (e.target as HTMLElement).closest('button'); if (b && !b.closest('[role="dialog"]')) setListOpen(false); }}>{topLeft}</div>
        </div>
        <div className="workspace-detail scroll-container">{topRight}</div>
      </div>
    </section>
    {host ? createPortal(preview, host) : preview}
    {children}
  </div>;
};
