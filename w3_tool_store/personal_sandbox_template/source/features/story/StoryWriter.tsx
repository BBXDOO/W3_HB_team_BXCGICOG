import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import type { StoryNode } from '../../types';
import { documentBridge, exportTextDocument } from '../../core/documentFiles';
import { RichContent } from '../editor/ContentFormat';
import { MarkdownContent } from './MarkdownContent';

type Snapshot = { body: string; bodyFormat?: StoryNode['bodyFormat'] };
type Props = {
  node: StoryNode; onChange: (node: StoryNode) => void; onClose: () => void;
  onCommit: () => boolean; onImport: () => void; onNew: () => void;
  saveState: 'pending' | 'saved' | 'error';
};
export const StoryWriter: React.FC<Props> = ({ node, onChange, onClose, onCommit, onImport, onNew, saveState }) => {
  const editor = useRef<HTMLTextAreaElement>(null);
  const [view, setView] = useState<'write' | 'split' | 'preview'>('write');
  const [findOpen, setFindOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [replacement, setReplacement] = useState('');
  const [notice, setNotice] = useState('');
  useEffect(() => { if (!notice || saveState === 'error') return; const timer = window.setTimeout(() => setNotice(''), 4500); return () => window.clearTimeout(timer); }, [notice, saveState]);
  const [fontSize, setFontSize] = useState(() => { try { return Math.max(11, Math.min(24, Number(localStorage.getItem('w3.story-writer.font')) || 14)); } catch { return 14; } });
  const history = useRef<{ past: Snapshot[]; future: Snapshot[]; lastEdit: number }>({ past: [], future: [], lastEdit: 0 });
  const latest = useRef({ body: node.body || '', node, onChange });
  latest.current = { body: node.body || '', node, onChange };
  const body = node.body || '';
  const format = node.bodyFormat || 'legacy';
  const seenBody = useRef(body);
  const seenFormat = useRef(node.bodyFormat);
  const internalNext = useRef<Snapshot | null>(null);
  const [, forceHistory] = useState(0);
  const remember = (text: string, bodyFormat = node.bodyFormat) => {
    const past = history.current.past;
    if (past.at(-1)?.body !== text || past.at(-1)?.bodyFormat !== bodyFormat) past.push({ body: text, bodyFormat });
    while (past.length > 20 || past.reduce((n, value) => n + value.body.length, 0) > 2_000_000) past.shift();
  };
  useEffect(() => {
    if ((body !== seenBody.current || node.bodyFormat !== seenFormat.current) && !(internalNext.current?.body === body && internalNext.current?.bodyFormat === node.bodyFormat)) {
      remember(seenBody.current, seenFormat.current); history.current.future = []; history.current.lastEdit = 0; forceHistory(n => n + 1);
    }
    seenBody.current = body; seenFormat.current = node.bodyFormat; internalNext.current = null;
  }, [body, node.bodyFormat]);
  const changeBody = (text: string, separate = false) => {
    internalNext.current = { body: text, bodyFormat: node.bodyFormat };
    const now = Date.now();
    if (separate || now - history.current.lastEdit > 700) remember(latest.current.body);
    history.current.lastEdit = now; history.current.future = [];
    onChange({ ...node, body: text });
  };
  const undo = () => {
    const previous = history.current.past.pop(); if (previous === undefined) return;
    history.current.future.push({ body, bodyFormat: node.bodyFormat }); history.current.lastEdit = 0;
    internalNext.current = previous; onChange({ ...node, body: previous.body, bodyFormat: previous.bodyFormat });
  };
  const redo = () => {
    const next = history.current.future.pop(); if (next === undefined) return;
    remember(body); history.current.lastEdit = 0; internalNext.current = next; onChange({ ...node, body: next.body, bodyFormat: next.bodyFormat });
  };
  const save = () => { const ok = onCommit(); setNotice(ok ? 'บันทึกลงเครื่องแล้ว' : 'บันทึกไม่สำเร็จ โปรดส่งออกสำเนาก่อนปิด'); return ok; };
  const close = () => { if (onCommit()) onClose(); else setNotice('บันทึกไม่สำเร็จ ยังเปิดต้นฉบับไว้ให้ส่งออกได้'); };
  const closeRef = useRef(close); closeRef.current = close;
  useEffect(() => {
    documentBridge()?.setWriterOpen?.(true);
    const back = () => closeRef.current();
    const escape = (e: KeyboardEvent) => { if (e.key === 'Escape') back(); };
    window.addEventListener('w3-story-back', back); window.addEventListener('keydown', escape);
    return () => { documentBridge()?.setWriterOpen?.(false); window.removeEventListener('w3-story-back', back); window.removeEventListener('keydown', escape); };
  }, []);
  const resizeFont = (delta: number) => { const n = Math.max(11, Math.min(24, fontSize + delta)); setFontSize(n); try { localStorage.setItem('w3.story-writer.font', String(n)); } catch {} };
  const insert = (before: string, after = '', fallback = 'ข้อความ', line = false) => {
    const area = editor.current; const start = area?.selectionStart ?? body.length, end = area?.selectionEnd ?? start;
    const from = line ? body.lastIndexOf('\n', start - 1) + 1 : start;
    const selected = body.slice(from, end) || fallback;
    const value = before + selected + after;
    changeBody(body.slice(0, from) + value + body.slice(end), true);
    setView(view === 'preview' ? 'write' : view);
    requestAnimationFrame(() => { editor.current?.focus(); editor.current?.setSelectionRange(from + before.length, from + before.length + selected.length); });
  };
  const findNext = () => {
    if (!query) return;
    const at = body.indexOf(query, editor.current?.selectionEnd || 0);
    const found = at < 0 ? body.indexOf(query) : at;
    if (found < 0) { setNotice('ไม่พบข้อความที่ค้นหา'); return; }
    setView(view === 'preview' ? 'write' : view);
    requestAnimationFrame(() => { editor.current?.focus(); editor.current?.setSelectionRange(found, found + query.length); });
    setNotice(`พบข้อความที่ตำแหน่ง ${found + 1}`);
  };
  const replace = (all: boolean) => {
    if (!query) return;
    if (all) { const pieces = body.split(query); if (pieces.length === 1) { setNotice('ไม่พบข้อความที่ค้นหา'); return; } changeBody(pieces.join(replacement), true); setNotice(`แทนที่ ${pieces.length - 1} แห่ง`); }
    else { const area = editor.current; const start = area?.selectionStart || 0, end = area?.selectionEnd || 0; if (body.slice(start, end) !== query) { findNext(); return; } changeBody(body.slice(0, start) + replacement + body.slice(end), true); setNotice('แทนที่ข้อความที่เลือกแล้ว'); }
  };
  const exportFile = (extension: 'md' | 'txt') => { try { const route = exportTextDocument(node.title || 'story', body, extension); setNotice(route === 'picker' ? 'เปิดหน้าบันทึกไฟล์แล้ว เลือกโฟลเดอร์และยืนยันบันทึก' : 'ส่งไฟล์ให้เบราว์เซอร์ดาวน์โหลดแล้ว'); } catch { setNotice('เปิดหน้าส่งออกไม่สำเร็จ ต้นฉบับยังอยู่ในหน้าต่างนี้'); } };
  const toolbar: [string, string, () => void][] = [
    ['ตัวหนา', 'B', () => insert('**', '**')], ['ตัวเอียง', 'I', () => insert('*', '*')],
    ['ขีดฆ่า', 'S̶', () => insert('~~', '~~')], ['หัวข้อ', 'H2', () => insert('## ', '', 'หัวข้อ', true)],
    ['รายการหัวข้อ', '• รายการ', () => insert('- ', '', 'รายการ', true)], ['รายการลำดับ', '1.', () => insert('1. ', '', 'รายการ', true)],
    ['เช็กลิสต์', '☑', () => insert('- [ ] ', '', 'รายการ', true)], ['อ้างอิงข้อความ', '❯', () => insert('> ', '', 'ข้อความ', true)],
    ['แทรกลิงก์', 'ลิงก์', () => insert('[', '](https://example.com)', 'ชื่อเว็บไซต์')],
    ['บล็อกโค้ด', '</>', () => insert('\n```text\n', '\n```\n', 'ข้อความหรือโค้ด')],
    ['ตาราง', 'ตาราง', () => insert('\n| หัวข้อ | รายละเอียด |\n| --- | --- |\n| ', ' | ข้อมูล |\n', 'รายการ')],
    ['ส่วนพับได้', 'พับ', () => insert('\n<details>\n<summary>หัวข้อ</summary>\n\n', '\n\n</details>\n', 'เนื้อหา')]
  ];
  return createPortal(<div className="story-writer" role="dialog" aria-modal="true" aria-label="หน้าต่างเขียน Story เต็มจอ" style={{ '--writer-font-size': `${fontSize}px` } as React.CSSProperties}>
    <header className="story-writer-header"><button type="button" onClick={close} aria-label="กลับรายการ Story">← Story</button><input aria-label="ชื่อเอกสาร Story" value={node.title || ''} onChange={e => onChange({ ...node, title: e.target.value })} placeholder="ชื่อเรื่อง / เอกสาร" /><button type="button" onClick={save}>บันทึก</button></header>
    <div className="story-writer-actions">
      <div className="story-writer-modes">{([['write','เขียน'],['split','เขียน + พรีวิว'],['preview','พรีวิว']] as const).map(([mode, label]) => <button type="button" key={mode} aria-pressed={view === mode} onClick={() => setView(mode)}>{label}</button>)}</div>
      <select aria-label="รูปแบบเอกสาร" value={format} onChange={e => onChange({ ...node, bodyFormat: e.target.value as StoryNode['bodyFormat'] })}><option value="markdown">Markdown / GitHub</option><option value="legacy">ข้อความเดิม</option></select>
      <button type="button" onClick={() => { if (onCommit()) onNew(); else setNotice('บันทึกตอนปัจจุบันไม่สำเร็จ โปรดส่งออกสำเนาก่อนสร้างตอนใหม่'); }}>+ ตอนใหม่</button><button type="button" onClick={onImport}>นำเข้าไฟล์</button><button type="button" onClick={() => exportFile('md')}>ส่งออก .md</button><button type="button" onClick={() => exportFile('txt')}>ส่งออก .txt</button>
      <button type="button" onClick={() => setFindOpen(!findOpen)} aria-expanded={findOpen}>ค้นหา / แทนที่</button>
      <button type="button" onClick={undo} disabled={!history.current.past.length} aria-label="เลิกทำ">↶</button><button type="button" onClick={redo} disabled={!history.current.future.length} aria-label="ทำซ้ำ">↷</button>
      <button type="button" onClick={() => resizeFont(-1)} aria-label="ลดขนาดตัวหนังสือเขียน">A−</button><button type="button" onClick={() => resizeFont(1)} aria-label="เพิ่มขนาดตัวหนังสือเขียน">A+</button>
    </div>
    {format === 'markdown' && <div className="story-writing-tools" aria-label="เครื่องมือเขียน Markdown">{toolbar.map(([title, label, action]) => <button type="button" key={title} title={title} aria-label={title} onMouseDown={e => e.preventDefault()} onClick={action}>{label}</button>)}</div>}
    {findOpen && <div className="story-writer-find"><input aria-label="ค้นหาในเอกสาร" placeholder="ค้นหา (ตรงตัวพิมพ์)" value={query} onChange={e => setQuery(e.target.value)} /><input aria-label="ข้อความแทนที่" placeholder="แทนที่ด้วย" value={replacement} onChange={e => setReplacement(e.target.value)} /><button type="button" onClick={findNext} disabled={!query}>ถัดไป</button><button type="button" onClick={() => replace(false)} disabled={!query}>แทนที่</button><button type="button" onClick={() => replace(true)} disabled={!query}>ทั้งหมด</button></div>}
    <main className={`story-writer-panes story-writer-${view}`}>
      {view !== 'preview' && <textarea ref={editor} aria-label="ต้นฉบับ Story" spellCheck={false} value={body} onChange={e => changeBody(e.target.value)} placeholder="เขียนเนื้อเรื่อง วางข้อมูล หรือเริ่มด้วย # หัวข้อ Markdown" onKeyDown={e => {
        if (!(e.ctrlKey || e.metaKey)) return;
        const key = e.key.toLowerCase();
        if (['s','b','i','z','y'].includes(key)) e.preventDefault();
        if (key === 's') save(); else if (key === 'b') insert('**','**'); else if (key === 'i') insert('*','*'); else if (key === 'z') e.shiftKey ? redo() : undo(); else if (key === 'y') redo();
      }} />}
      {view !== 'write' && <section className="story-writer-preview scroll-container" aria-label="พรีวิวเอกสาร">{format === 'markdown' ? <MarkdownContent value={body} /> : <RichContent value={body} />}</section>}
    </main>
    <footer className="story-writer-footer"><span>{body.split('\n').length} บรรทัด · {body.length.toLocaleString()} อักขระ · {fontSize}px</span><span role="status" className={saveState === 'error' ? 'story-writer-error' : ''}>{saveState === 'error' ? 'บันทึกไม่สำเร็จ · ส่งออกสำเนาได้' : saveState === 'pending' ? 'กำลังรอบันทึกอัตโนมัติ…' : 'บันทึกลงเครื่องแล้ว'}</span></footer>
    {notice && <div role="status" className="story-writer-notice" onClick={() => setNotice('')}>{notice}<button type="button" aria-label="ปิดข้อความแจ้งผล" onClick={() => setNotice('')}>✕</button></div>}
  </div>, document.body);
};
