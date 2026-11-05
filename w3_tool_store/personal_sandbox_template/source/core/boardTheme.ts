import type { BoardPack, BoardTableTheme } from '../types';

export const BOARD_TABLE_THEMES: Record<string, { label: string; colors: BoardTableTheme }> = {
  instrument: { label: 'ดำเทา', colors: { background: '#191a1d', empty: '#30293e', grid: '#63596e', text: '#f3f0f7', selection: '#f59e0b' } },
  paper: { label: 'กระดาษ', colors: { background: '#f4efe3', empty: '#fffdf7', grid: '#a69b85', text: '#29251e', selection: '#2563eb' } },
  forest: { label: 'เขียวป่า', colors: { background: '#10261d', empty: '#244735', grid: '#6b9b7d', text: '#eefbf1', selection: '#facc15' } },
  ocean: { label: 'น้ำเงิน', colors: { background: '#102136', empty: '#203e5b', grid: '#6c9aba', text: '#eef6ff', selection: '#38bdf8' } },
};

// Imported projects can contain old or incomplete settings. Resolve each color
// independently and keep appearance separate from the data/marker colors.
export function boardTableTheme(board: BoardPack): BoardTableTheme {
  const fallback = BOARD_TABLE_THEMES.instrument.colors;
  return Object.fromEntries(Object.entries(fallback).map(([key, color]) => [key,
    /^#[0-9a-f]{6}$/i.test(board.tableTheme?.[key] || '') ? board.tableTheme![key] : color
  ])) as unknown as BoardTableTheme;
}
