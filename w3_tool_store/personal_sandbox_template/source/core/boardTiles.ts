import type { BoardPack, BoardTile, StoryPack } from '../types';

export function gridGeometry(style: BoardPack['gridStyle']) {
  return { gap: style === 'seamless' ? 0 : style === 'dots' ? 5 : 3, radius: style === 'seamless' ? 0 : style === 'dots' ? '50%' : 4 };
}

export function sheetRects(width: number, height: number, columns: number, rows: number, margin: number, spacing: number) {
  if (![width, height, columns, rows, margin, spacing].every(Number.isInteger) || columns < 1 || rows < 1 || columns * rows > 64 || margin < 0 || spacing < 0) throw new Error('กำหนดแถว/คอลัมน์รวมไม่เกิน 64 ชิ้น และระยะเป็นจำนวนเต็มบวกหรือศูนย์');
  const w = (width - margin * 2 - spacing * (columns - 1)) / columns;
  const h = (height - margin * 2 - spacing * (rows - 1)) / rows;
  if (w < 1 || h < 1) throw new Error('ขอบหรือช่องไฟใหญ่เกินขนาดภาพ');
  return Array.from({ length: columns * rows }, (_, i) => ({ x: margin + i % columns * (w + spacing), y: margin + Math.floor(i / columns) * (h + spacing), width: w, height: h }));
}

export function tileImage(tiles: BoardTile[], assets: StoryPack['assets'], id?: string) {
  const tile = tiles.find(item => item.id === id);
  const url = tile && assets[tile.assetId]?.dataUrl;
  return typeof url === 'string' && /^data:image\/(png|jpeg|webp|gif|svg\+xml)[;,]/i.test(url) ? url : undefined;
}

export function placeBoardTile(story: StoryPack, boardId: string, key: string, tileRefId?: string): StoryPack {
  const board = story.boards.find(item => item.boardId === boardId);
  if (!board || !/^\d+_\d+$/.test(key)) return story;
  const [x, y] = key.split('_').map(Number);
  if (x >= board.width || y >= board.height || tileRefId && !(story.boardTiles || []).some(tile => tile.id === tileRefId)) return story;
  return { ...story, boards: story.boards.map(item => item.boardId === boardId ? { ...item, cellMap: { ...item.cellMap, [key]: { ...(item.cellMap[key] || { x, y, type: 'Empty' }), tileRefId } } } : item) };
}

export function removeBoardTile(story: StoryPack, id: string): StoryPack {
  return { ...story, boardTiles: (story.boardTiles || []).filter(tile => tile.id !== id), boards: story.boards.map(board => ({ ...board, cellMap: Object.fromEntries(Object.entries(board.cellMap).map(([key, cell]) => [key, cell.tileRefId === id ? { ...cell, tileRefId: undefined } : cell])) })) };
}
