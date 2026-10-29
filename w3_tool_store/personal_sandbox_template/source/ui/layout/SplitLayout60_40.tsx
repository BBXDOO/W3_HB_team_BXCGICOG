import { NavIcon } from '../components/NavIcon';
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
    isAgentOpen?: boolean;
  };
  children?: React.ReactNode;
}

const LAYOUT_KEY = 'w3.personal.preview-height-v6';
const MIN_PREVIEW = 10;
const MAX_PREVIEW = 65;
const DEFAULT_PREVIEW = 28;
const maxPreview = (mobileMax: number) => window.matchMedia('(max-width: 767px)').matches ? mobileMax : MAX_PREVIEW;

function initialPreviewHeight(key: string, defaultHeight: number, mobileMax: number): number {
  try {
    const saved = Number(localStorage.getItem(key));
    if (saved >= MIN_PREVIEW && saved <= maxPreview(mobileMax)) return saved;
  } catch {
    // The layout remains usable when storage is unavailable.
  }
  return defaultHeight;
}

export const SplitLayout60_40: React.FC<SplitLayout60_40Props> = ({
  topLeft,
  topRight,
  bottomMain,
  previewKey = LAYOUT_KEY,
  defaultPreview = DEFAULT_PREVIEW,
  mobileMaxPreview = 35,
  showTools = true,
  toolActions,
  children
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const dragging = useRef(false);
  const [previewHeight, setPreviewHeight] = useState(() => initialPreviewHeight(previewKey, defaultPreview, mobileMaxPreview));
  const [listOpen, setListOpen] = useState(false);
  const [workspaceHeight, setWorkspaceHeight] = useState(0);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const measure = () => setWorkspaceHeight(container.getBoundingClientRect().height);
    measure();
    const observer = new ResizeObserver(measure);
    observer.observe(container);
    return () => observer.disconnect();
  }, []);

  const outputHeight = Math.max(0, (workspaceHeight - 22) * previewHeight / 100);

  const setHeight = (height: number) => {
    const next = Math.max(MIN_PREVIEW, Math.min(maxPreview(mobileMaxPreview), Math.round(height)));
    setPreviewHeight(next);
    try { localStorage.setItem(previewKey, String(next)); } catch { /* optional preference */ }
  };

  const moveHandle = (clientY: number) => {
    const bounds = containerRef.current?.getBoundingClientRect();
    if (!bounds) return;
    setHeight(100 - (clientY - bounds.top) / bounds.height * 100);
  };

  return (
    <div
      ref={containerRef}
      className="workspace-layout h-full w-full bg-[var(--bg)] overflow-hidden"
      style={{ gridTemplateRows: workspaceHeight ? `minmax(0, ${Math.max(0, workspaceHeight - outputHeight - 22)}px) 22px minmax(0, ${outputHeight}px)` : `${100 - previewHeight}% 22px ${previewHeight}%` }}
    >
      <section className="workspace-region flex flex-col md:flex-row min-h-0 overflow-hidden" aria-label="พื้นที่แก้ไข">
        <button type="button" className="workspace-list-toggle" aria-expanded={listOpen} aria-controls="workspace-list" onClick={() => setListOpen(open => !open)}>☰ รายการ / เพิ่ม</button>
        {listOpen && <button type="button" className="workspace-list-backdrop" aria-label="ปิดรายการ" onClick={() => setListOpen(false)} />}
        <div id="workspace-list" className={`workspace-list ${listOpen ? 'workspace-list-open' : ''} h-[40%] md:h-full md:flex-[3.5] min-w-0 min-h-0 overflow-y-auto scroll-container`} onClick={event => {
          if ((event.target as HTMLElement).closest('button')) setListOpen(false);
        }}>
          <div className="workspace-list-header">
            <span>รายการ / เพิ่ม</span>
            <button type="button" aria-label="ปิดหน้าต่างรายการ" onClick={() => setListOpen(false)}>✕ ปิด</button>
          </div>
          {topLeft}
        </div>
        <div className="workspace-detail h-[60%] md:h-full md:flex-[6.5] min-w-0 min-h-0 overflow-y-auto scroll-container">
          {topRight}
        </div>
      </section>
      <div aria-hidden="true" />
      <div aria-hidden="true" />

      <div className="workspace-divider workspace-divider-wide flex items-center justify-center"
        style={{ bottom: `${outputHeight + 6}px` }}>
        <button
          type="button"
          className="workspace-drag-handle"
          role="separator"
          aria-label="ปรับขนาดพื้นที่ผลลัพธ์"
          aria-orientation="horizontal"
          aria-valuemin={MIN_PREVIEW}
          aria-valuemax={maxPreview(mobileMaxPreview)}
          aria-valuenow={previewHeight}
          title="ลากเพื่อปรับขนาดผลลัพธ์ • แตะสองครั้งเพื่อคืนค่าเดิม"
          onPointerDown={(event) => {
            dragging.current = true;
            event.currentTarget.setPointerCapture(event.pointerId);
          }}
          onPointerMove={(event) => { if (dragging.current) moveHandle(event.clientY); }}
          onPointerUp={(event) => {
            if (dragging.current) moveHandle(event.clientY);
            dragging.current = false;
          }}
          onPointerCancel={() => { dragging.current = false; }}
          onDoubleClick={() => setHeight(defaultPreview)}
          onKeyDown={(event) => {
            if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
              event.preventDefault();
              setHeight(previewHeight + (event.key === 'ArrowUp' ? 5 : -5));
            }
          }}
        ><span /></button>
      </div>

      <section className="workspace-output workspace-output-wide min-h-0 flex flex-col overflow-hidden"
        style={{ height: `${outputHeight}px` }} aria-label="พื้นที่แสดงผล">
        {showTools && toolActions && (toolActions.onSearch || toolActions.onAdd || toolActions.onExport || toolActions.onToggleAgent) && (
          <div className="workspace-output-actions flex items-center gap-2 px-3 py-1 border-b border-[var(--border)] bg-[var(--surface-2)] shrink-0" aria-label="เครื่องมือพื้นที่แสดงผล">
            {toolActions.onSearch && <button type="button" onClick={toolActions.onSearch} aria-label="ค้นหา" className="workspace-action"><NavIcon name="search" /></button>}
            {toolActions.onAdd && <button type="button" onClick={toolActions.onAdd} aria-label="เพิ่มรายการ" className="workspace-action"><NavIcon name="add" /></button>}
            {toolActions.onExport && <button type="button" onClick={toolActions.onExport} aria-label="ส่งออก" className="workspace-action"><NavIcon name="export" /></button>}
            {toolActions.onToggleAgent && <button type="button" onClick={toolActions.onToggleAgent} aria-label="เปิดหรือปิดผู้ช่วย" className="workspace-action ml-auto"><NavIcon name="ai" /></button>}
          </div>
        )}
        <div className="flex-1 w-full min-w-0 min-h-0 overflow-y-auto scroll-container relative">
          <div className="min-h-full w-full">{bottomMain}</div>
        </div>
      </section>
      {children}
    </div>
  );
};
