import React from 'react';
import assert from 'node:assert/strict';
import { renderToStaticMarkup } from 'react-dom/server';
import { BoardWorkspace } from '../features/board/BoardWorkspace';
import { boardTableTheme, BOARD_TABLE_THEMES } from '../core/boardTheme';
import { createEmptyProject } from '../core/project';
import { saveStory, getStory, buildBackup, parseBackup } from '../core/storage';
import type { BoardPack } from '../types';

const memory = new Map<string, string>();
(globalThis as any).localStorage = { getItem: (key: string) => memory.get(key) ?? null, setItem: (key: string, value: string) => memory.set(key, value), removeItem: (key: string) => memory.delete(key) };
const board: BoardPack = { boardId: 'one', title: 'ตารางหนึ่ง', width: 2, height: 2, viewMode: 'grid', cellMap: { '0_0': { x: 0, y: 0, name: 'ข้อมูล', markerColor: '#ff0000' } }, explored: {}, visionRangeDefault: 2, movementPerTurnDefault: 2 };
assert.deepEqual(boardTableTheme(board), BOARD_TABLE_THEMES.instrument.colors);
const story = createEmptyProject('theme-test', 'library', 'ทดสอบ');
story.boards = [{ ...board, tableTheme: { ...BOARD_TABLE_THEMES.paper.colors } }, { ...board, boardId: 'two' }];
assert.equal(saveStory(story), true);
assert.deepEqual(getStory(story.storyId)?.boards[0].tableTheme, BOARD_TABLE_THEMES.paper.colors);
const restored = parseBackup(JSON.parse(JSON.stringify(buildBackup(story))))!.story;
assert.deepEqual(restored.boards[0].tableTheme, BOARD_TABLE_THEMES.paper.colors);
assert.equal(restored.boards[1].tableTheme, undefined);
assert.equal(restored.uiTheme, story.uiTheme);
assert.equal(restored.boards[0].cellMap['0_0'].markerColor, '#ff0000');
assert.equal(boardTableTheme({ ...board, tableTheme: { ...BOARD_TABLE_THEMES.paper.colors, grid: 'invalid' } }).grid, BOARD_TABLE_THEMES.instrument.colors.grid);
const render = (data: BoardPack) => renderToStaticMarkup(<BoardWorkspace board={data} selectedKey="0_0" zoom={22} onZoom={() => {}} onAppearance={() => {}} onSelect={() => {}} onMode={() => {}} onAdd={() => {}} onUpdate={() => {}} onDelete={() => {}} />);
const grid = render(restored.boards[0]);
assert.ok(grid.includes('ธีมเฉพาะตาราง'));
assert.ok(grid.includes('--table-text:#29251e'));
assert.ok(grid.includes('background:#ff0000')); // Existing marker retains its data color.
for (const viewMode of ['overview', 'database', 'mindmap'] as const) {
  const html = render({ ...restored.boards[0], viewMode });
  assert.ok(!html.includes('ธีมเฉพาะตาราง'));
  assert.ok(!html.includes('--table-text:'));
}
console.log('Board themes: old projects, persistence, JSON round trip, per-board isolation, markers, invalid values and view scoping passed');
