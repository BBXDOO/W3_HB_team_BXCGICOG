export const MAX_DOCUMENT_BYTES = 4 * 1024 * 1024;
export type TextDocument = { title: string; body: string; bodyFormat: 'markdown' | 'legacy'; filename: string };
export type DocumentBridge = {
  saveText?: (name: string, contents: string, mime: string) => void;
  openExternal?: (address: string) => void;
  setWriterOpen?: (open: boolean) => void;
};
export const documentBridge = () => (window as Window & { AndroidBridge?: DocumentBridge }).AndroidBridge;

export async function readTextDocument(file: File): Promise<TextDocument> {
  if (!/\.(md|markdown|txt)$/i.test(file.name)) throw new Error('รองรับไฟล์ .md, .markdown และ .txt');
  if (file.size > MAX_DOCUMENT_BYTES) throw new Error('ไฟล์ต้องมีขนาดไม่เกิน 4 MB');
  let text: string;
  try { text = new TextDecoder('utf-8', { fatal: true }).decode(await file.arrayBuffer()); }
  catch { throw new Error('อ่านไฟล์ไม่สำเร็จ กรุณาบันทึกไฟล์เป็น UTF-8'); }
  const body = text.replace(/^\uFEFF/, '').replace(/\r\n?/g, '\n');
  if (body.includes('\u0000')) throw new Error('ไฟล์นี้ไม่ใช่ข้อความ UTF-8 ที่รองรับ');
  const title = body.match(/^#\s+(.+)$/m)?.[1]?.trim() || file.name.replace(/\.[^.]+$/, '');
  return { title, body, filename: file.name, bodyFormat: /\.(md|markdown)$/i.test(file.name) ? 'markdown' : 'legacy' };
}

export function exportTextDocument(title: string, body: string, extension: 'md' | 'txt'): 'picker' | 'download' {
  const stem = (title.trim() || 'story').replace(/[\\/:*?"<>|\u0000-\u001f]/g, '_').slice(0, 100);
  const name = `${stem}.${extension}`;
  const mime = extension === 'md' ? 'text/markdown' : 'text/plain';
  const bridge = documentBridge();
  if (bridge?.saveText) { bridge.saveText(name, body, mime); return 'picker'; }
  const url = URL.createObjectURL(new Blob([body], { type: `${mime};charset=utf-8` }));
  const anchor = document.createElement('a');
  anchor.href = url; anchor.download = name; document.body.append(anchor); anchor.click(); anchor.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 30000);
  return 'download';
}
