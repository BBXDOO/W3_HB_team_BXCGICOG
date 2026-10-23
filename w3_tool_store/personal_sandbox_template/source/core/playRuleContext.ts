import type { StoryPack } from '../types';
import type { RuleContext } from './ruleRuntime';

export interface PlayRuleSelection {
  boardId?: string | null; cellKey?: string | null; characterId?: string | null;
  nodeId?: string | null; recordId?: string | null;
  vitals?: Record<string, { hp: number; mp: number; en: number }>;
}

/** Snapshot of currently selected project data; absent sources remain absent. */
export const buildPlayRuleContext = (story: StoryPack, selection: PlayRuleSelection): RuleContext => {
  const context: RuleContext = { project: { id: story.storyId, kind: story.projectKind || null } };
  const board = story.boards.find(entry => entry.boardId === selection.boardId);
  if (board) context.board = { id: board.boardId, title: board.title, width: board.width, height: board.height };
  if (board && selection.cellKey) {
    const [x, y] = selection.cellKey.split('_').map(Number);
    if (Number.isInteger(x) && Number.isInteger(y) && x >= 0 && y >= 0 && x < board.width && y < board.height) {
      const cell = board.cellMap[selection.cellKey];
      context.cell = { x, y, ...(cell ? { name: cell.name || '', type: cell.type || '', locationRefId: cell.locationRefId || '' } : {}) };
      const location = story.locations.find(entry => entry.locationId === cell?.locationRefId);
      if (location) context.location = { id: location.locationId, title: location.title, zone: location.zone || '', type: location.areaProfile.type || '', threat: location.areaProfile.threat ?? 0 };
    }
  }
  const character = story.characters.find(entry => entry.id === selection.characterId);
  if (character) context.character = { id: character.id, name: character.name, className: character.className,
    ...character.capabilities, ...character.attributes, ...(selection.vitals?.[character.id] || character.vitals) };
  const node = story.storyNodes.find(entry => entry.nodeId === selection.nodeId);
  if (node) context.story = { id: node.nodeId, title: node.title || '', type: node.type };
  const item = story.items.find(entry => entry.id === selection.recordId);
  if (item) context.item = { id: item.id, name: item.name, category: item.category, rarity: item.rarity };
  const card = story.cards.find(entry => entry.id === selection.recordId);
  if (card) context.card = { id: card.id, name: card.name, type: card.type, rarity: card.rarity, grade: card.grade };
  const event = story.events.find(entry => entry.id === selection.recordId);
  if (event) context.event = { id: event.id, name: event.name, type: event.eventType };
  const selectedLocation = story.locations.find(entry => entry.locationId === selection.recordId);
  if (selectedLocation) context.location = { id: selectedLocation.locationId, title: selectedLocation.title, zone: selectedLocation.zone || '', type: selectedLocation.areaProfile.type || '', threat: selectedLocation.areaProfile.threat ?? 0 };
  return context;
};
