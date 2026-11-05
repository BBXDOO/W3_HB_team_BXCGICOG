import React, { useState, useEffect } from 'react';
import type { StoryPack } from '../../types';
import { generateId } from '../../core/utils';
import { removeBoardTile, sheetRects, tileImage } from '../../core/boardTiles';

interface Props { story: StoryPack; onChange: (story: StoryPack) => void; brush: string | null; onBrush: (id: string | null) => void; }
export const TileLibrary: React.FC<Props> = ({ story, onChange, brush, onBrush }) => {
  const [image, setImage] = useState<HTMLImageElement | null>(null);
  const [name, setName] = useState('ชิ้นเลโก้');
  const [columns, setColumns] = useState(1), [rows, setRows] = useState(1);
  const [margin, setMargin] = useState(0), [spacing, setSpacing] = useState(0);
  const [drafts, setDrafts] = useState<string[]>([]), [chosen, setChosen] = useState<number[]>([]);
  const [notice, setNotice] = useState(''), [busy, setBusy] = useState(false);
  const tiles = story.boardTiles || [];
  useEffect(() => () => { if (image) URL.revokeObjectURL(image.src); }, [image]);
  const load = async (file?: File) => {
    if (!file) return;
    setNotice(''); setDrafts([]); setChosen([]); setImage(null); setBusy(true);
    const url = URL.createObjectURL(file);
    try {
      if (!/^image\/(png|jpeg|webp|gif)$/.test(file.type) || file.size > 8 * 1024 * 1024) throw new Error('ใช้ PNG/JPG/WebP/GIF ไม่เกิน 8 MB');
      const img = new Image(); img.src = url; await img.decode();
      if (img.naturalWidth * img.naturalHeight > 16000000) throw new Error('ภาพใหญ่เกิน 16 ล้านพิกเซล กรุณาย่อก่อน');
      setImage(img); setName(file.name.replace(/\.[^.]+$/, '')); setColumns(1); setRows(1); setMargin(0); setSpacing(0);
    } catch (e) { URL.revokeObjectURL(url); setNotice(e instanceof Error ? e.message : 'เปิดภาพไม่สำเร็จ'); }
    finally { setBusy(false); }
  };
  const slice = () => {
    if (!image) return;
    try {
      const rects = sheetRects(image.naturalWidth, image.naturalHeight, columns, rows, margin, spacing);
      const canvas = document.createElement('canvas'); canvas.width = canvas.height = 96;
      const context = canvas.getContext('2d'); if (!context) throw new Error('เครื่องนี้ไม่พร้อมตัดภาพ');
      const images = rects.map(rect => {
        context.clearRect(0, 0, 96, 96);
        context.drawImage(image, rect.x, rect.y, rect.width, rect.height, 0, 0, 96, 96);
        return canvas.toDataURL('image/png');
      });
      setDrafts(images); setChosen(images.map((_, index) => index)); setNotice('แตะชิ้นเพื่อเลือก/ไม่เลือก แล้วกดเพิ่มเข้าคลัง');
    } catch (e) { setDrafts([]); setChosen([]); setNotice(e instanceof Error ? e.message : 'ตัดภาพไม่ได้'); }
  };
  const add = () => {
    if (!chosen.length) return;
    const assets = { ...story.assets }, added = chosen.map((index, n) => {
      const id = `${generateId('tile')}_${n}`, assetId = `board_tile_${id}`;
      const title = `${name.trim() || 'ชิ้นเลโก้'} ${index + 1}`;
      assets[assetId] = { id: assetId, name: title, dataUrl: drafts[index] };
      return { id, assetId, name: title };
    });
    onChange({ ...story, assets, boardTiles: [...tiles, ...added] }); onBrush(added[0].id);
    setImage(null); setDrafts([]); setChosen([]); setNotice(`เพิ่ม ${added.length} ชิ้นแล้ว เลือกชิ้นแล้วแตะช่องเพื่อวาง กดบันทึกเพื่อเก็บโครงการ`);
  };
  return <details className="board-tile-library"><summary>▦ คลังเลโก้ · {tiles.length} ชิ้น</summary><div className="board-tile-library-body">
    <p>เลือกชิ้นแล้วแตะช่องเพื่อวางซ้ำ ใช้กริดชิดสำหรับต่อภาพ เลือก “เลือกช่อง” เมื่อต้องการแก้ข้อมูลตามปกติ</p>
    <div className="flex gap-2 flex-wrap"><button type="button" aria-pressed={brush === null} onClick={() => onBrush(null)}>เลือกช่อง</button><button type="button" aria-pressed={brush === '__erase'} onClick={() => onBrush('__erase')}>ลบชิ้นในช่อง</button></div>
    {brush && <p role="status">{brush === '__erase' ? 'โหมดลบชิ้น: แตะช่องเพื่อลบเฉพาะภาพ' : `พร้อมวาง: ${tiles.find(tile => tile.id === brush)?.name || 'เลือกชิ้นอีกครั้ง'}`}</p>}
    <div className="board-tile-palette">{tiles.map(tile => <div key={tile.id}><button type="button" title={tile.name} aria-label={`เลือกเลโก้ ${tile.name}`} aria-pressed={brush === tile.id} onClick={() => onBrush(tile.id)}><img src={tileImage(tiles, story.assets, tile.id)} alt={tile.name} /><span>{tile.name}</span></button><button type="button" aria-label={`ลบจากคลัง ${tile.name}`} onClick={() => {
      if (confirm(`ลบ ${tile.name} จากคลังและทุกช่องที่ใช้ชิ้นนี้? ข้อความและสีช่องยังอยู่`)) { onChange(removeBoardTile(story, tile.id)); if (brush === tile.id) onBrush(null); }
    }}>ลบจากคลัง</button></div>)}</div>
    <label>นำเข้ารูปเดี่ยว / แผ่นรวมหลายชิ้น<input type="file" accept="image/png,image/jpeg,image/webp,image/gif" disabled={busy} onChange={event => { void load(event.target.files?.[0]); event.target.value = ''; }} /></label>
    {image && <div className="space-y-2"><img className="tile-sheet-preview" src={image.src} alt="ต้นฉบับแผ่นเลโก้" />
      <label>ชื่อชุด<input value={name} onChange={event => setName(event.target.value)} /></label>
      <div className="grid grid-cols-2 gap-2">{([['คอลัมน์', columns, setColumns], ['แถว', rows, setRows], ['ขอบนอก (px)', margin, setMargin], ['ช่องไฟ (px)', spacing, setSpacing]] as const).map(([label, value, set]) => <label key={label}>{label}<input type="number" min={label === 'คอลัมน์' || label === 'แถว' ? 1 : 0} step="1" value={value} onChange={event => { set(Number(event.target.value)); setDrafts([]); setChosen([]); }} /></label>)}</div>
      <p>รูปเดี่ยวใช้ 1 × 1 แผ่นรวมต้องเป็นตารางสม่ำเสมอ รวมไม่เกิน 64 ชิ้น ปรับขอบและช่องไฟเพื่อตัดเส้นคั่นออก ภาพข้อความหรือหลายขนาดอาจต้องครอปจากเครื่องก่อน</p>
      <button type="button" onClick={slice}>ดูตัวอย่างชิ้น</button><button type="button" onClick={() => { setImage(null); setDrafts([]); setChosen([]); }}>ยกเลิกนำเข้า</button>
    </div>}
    {drafts.length > 0 && <div><div className="board-tile-palette">{drafts.map((url, i) => <button type="button" key={i} aria-label={`ชิ้นตัวอย่าง ${i + 1}`} aria-pressed={chosen.includes(i)} onClick={() => setChosen(current => current.includes(i) ? current.filter(n => n !== i) : [...current, i])}><img src={url} alt={`ชิ้น ${i + 1}`} /><span>{i + 1} {chosen.includes(i) ? '✓' : ''}</span></button>)}</div><button type="button" disabled={!chosen.length} onClick={add}>เพิ่ม {chosen.length} ชิ้นเข้าคลัง</button></div>}
    {notice && <p role="status">{notice}</p>}
  </div></details>;
};
