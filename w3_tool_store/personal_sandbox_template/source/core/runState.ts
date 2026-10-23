/** Play progress is separate from the editable StoryPack. */
import type { Inventory } from './inventory';
import { parseBattleProgress, type BattleProgress } from './battle';
export interface RunState {
  version: 1;
  storyId: string;
  currentNodeId: string | null;
  activeCharacterId: string | null;
  savedAt: number;
  characterVitals?: Record<string, { hp: number; mp: number; en: number }>;
  positions?: Record<string, { boardId: string; x: number; y: number }>;
  diceLog?: string[];
  eventLog?: string[];
  inventory?: Inventory;
  battleTurn?: number;
  battleLog?: string[];
  battle?: BattleProgress;
}

const runKey = (storyId: string) => `w3.personal.run.${storyId}`;

export const parseRunState = (state: unknown, storyId: string): RunState | null => {
  if (!state || typeof state !== 'object') return null;
  const value = state as Partial<RunState>;
  if (value.version !== 1 || value.storyId !== storyId ||
      (value.currentNodeId !== null && typeof value.currentNodeId !== 'string') ||
      (value.activeCharacterId !== null && typeof value.activeCharacterId !== 'string') ||
      typeof value.savedAt !== 'number' || !Number.isFinite(value.savedAt) ||
      (value.characterVitals !== undefined && (typeof value.characterVitals !== 'object' || value.characterVitals === null || Array.isArray(value.characterVitals))) ||
      (value.positions !== undefined && (typeof value.positions !== 'object' || value.positions === null || Array.isArray(value.positions))) ||
      (value.diceLog !== undefined && (!Array.isArray(value.diceLog) || !value.diceLog.every(line => typeof line === 'string'))) ||
      (value.eventLog !== undefined && (!Array.isArray(value.eventLog) || !value.eventLog.every(line => typeof line === 'string'))) ||
      (value.battleTurn !== undefined && (!Number.isSafeInteger(value.battleTurn) || value.battleTurn < 1)) ||
      (value.battleLog !== undefined && (!Array.isArray(value.battleLog) || !value.battleLog.every(line => typeof line === 'string')))) return null;
  if (value.battle !== undefined && !parseBattleProgress(value.battle)) return null;
  if (value.inventory !== undefined && (typeof value.inventory !== 'object' || value.inventory === null || Array.isArray(value.inventory) ||
      !Object.entries(value.inventory).every(([owner, items]) => owner && owner !== '__proto__' && owner !== 'constructor' && owner !== 'prototype' &&
        items && typeof items === 'object' && !Array.isArray(items) && Object.entries(items).every(([id, quantity]) =>
          id && id !== '__proto__' && id !== 'constructor' && id !== 'prototype' && Number.isSafeInteger(quantity) && quantity > 0)))) return null;
  if (value.characterVitals && !Object.values(value.characterVitals).every(vitals =>
    vitals && typeof vitals === 'object' &&
    ['hp', 'mp', 'en'].every(key => Number.isFinite(vitals[key as keyof typeof vitals])))) return null;
  if (value.positions && !Object.values(value.positions).every(position =>
    position && typeof position.boardId === 'string' &&
    Number.isInteger(position.x) && Number.isInteger(position.y))) return null;
  return value as RunState;
};

export const loadRunState = (storyId: string): RunState | null => {
  try {
    const raw = localStorage.getItem(runKey(storyId));
    if (!raw) return null;
    return parseRunState(JSON.parse(raw), storyId);
  } catch {
    return null;
  }
};

export const saveRunState = (state: RunState): boolean => {
  try {
    localStorage.setItem(runKey(state.storyId), JSON.stringify(state));
    return true;
  } catch {
    return false;
  }
};

export const clearRunState = (storyId: string): boolean => {
  try { localStorage.removeItem(runKey(storyId)); return true; }
  catch { return false; }
};
