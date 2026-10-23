import type { StoryPack, BoardPack, CellPack, EventPack, LocationPack } from '../types';

/** Read-only view of authored world data. No triggers or free-text rules are executed here. */
export interface WorldCellView {
  board: BoardPack;
  cell: CellPack;
  location: LocationPack | null;
  events: EventPack[];
  missingLocationRef: boolean;
  missingEventRefs: string[];
}

export const getWorldCell = (
  story: StoryPack, boardId: string, x: number, y: number
): WorldCellView | null => {
  const board = story.boards.find(b => b.boardId === boardId);
  if (!board || !Number.isInteger(x) || !Number.isInteger(y) ||
      x < 0 || y < 0 || x >= board.width || y >= board.height) return null;

  const cell = board.cellMap[`${x}_${y}`] || { x, y, type: 'Empty' as const };
  const location = cell.locationRefId
    ? story.locations.find(l => l.locationId === cell.locationRefId) || null : null;
  const byId = new Map(story.events.map(e => [e.id, e]));
  const byEventId = new Map(story.events.map(e => [e.eventId, e]));
  const referenced = (cell.eventRefs || []).map(id => byId.get(id) || byEventId.get(id));
  const anchored = story.events.filter(e => e.targetBoardId === boardId &&
    e.targetX === x && e.targetY === y);
  const events = [...new Map([...referenced.filter((e): e is EventPack => !!e), ...anchored]
    .map(e => [e.id, e])).values()];

  return {
    board, cell, location, events,
    missingLocationRef: !!cell.locationRefId && !location,
    missingEventRefs: (cell.eventRefs || []).filter(id => !byId.has(id) && !byEventId.has(id))
  };
};
