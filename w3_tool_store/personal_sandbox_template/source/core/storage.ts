import { summarizeProject, type ProjectSummary } from './projectSummary';

import { StoryPack, CharacterPack, ItemPack, EventPack, AttributeDef, ProjectKind } from '../types';
import { clearRunState, loadRunState, parseRunState, saveRunState, type RunState } from './runState';

const INDEX_KEY = 'w3idp.story.index';
const STORY_PREFIX = 'w3idp.story.';

export interface StoryIndexItem extends ProjectSummary {
  storyId: string;
  title: string;
  updatedAt: number;
  projectKind?: ProjectKind;
}

export interface ImportedBackup { story: StoryPack; runState: RunState | null; }
const BACKUP_FORMAT = 'w3-personal-backup';

export const buildBackup = (story: StoryPack): { format: string; version: number; project: StoryPack; runState: RunState | null } => ({
  format: BACKUP_FORMAT, version: 1, project: story, runState: loadRunState(story.storyId)
});

export const parseBackup = (raw: unknown): ImportedBackup | null => {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return null;
  const data = raw as Record<string, unknown>;
  const wrapped = data.format === BACKUP_FORMAT;
  if (data.format !== undefined && !wrapped) return null;
  if (wrapped && data.version !== 1) return null;
  const project = wrapped ? data.project : data;
  if (!project || typeof project !== 'object' || Array.isArray(project)) return null;
  const candidate = project as Record<string, unknown>;
  if (typeof candidate.storyId !== 'string' || !candidate.storyId.trim() || candidate.storyId === 'index' ||
      typeof candidate.title !== 'string' || !Array.isArray(candidate.characters) ||
      !Array.isArray(candidate.boards) || !Array.isArray(candidate.storyNodes)) return null;
  const progress = wrapped ? data.runState : null;
  const runState = progress == null ? null : parseRunState(progress, candidate.storyId);
  if (progress != null && !runState) return null;
  return { story: migrateStory(project), runState };
};

// Exported to allow consistent default attributes when creating new story packs
export const DEFAULT_ATTRIBUTES: AttributeDef[] = [
  { key: 'STR', label: 'Strength', defaultValue: 5 },
  { key: 'DEX', label: 'Dexterity', defaultValue: 5 },
  { key: 'INT', label: 'Intelligence', defaultValue: 5 },
  { key: 'TEC', label: 'Technique', defaultValue: 5 },
  { key: 'KNO', label: 'Knowledge', defaultValue: 5 },
  { key: 'VIS', label: 'Vision', defaultValue: 5 },
  { key: 'TOL', label: 'Tolerance', defaultValue: 5 },
  { key: 'POW', label: 'Power', defaultValue: 5 },
  { key: 'ESN', label: 'Essence', defaultValue: 5 },
  { key: 'LOC', label: 'Luck', defaultValue: 5 }
];

const migrateStory = (data: any): StoryPack => {
  const attributeDefinitions = (data.attributeDefinitions || DEFAULT_ATTRIBUTES)
    .map((attribute: AttributeDef) => ({ ...attribute }));

  const migrateCharacter = (c: any): CharacterPack => {
    const capabilities: Record<string, number> = {};
    attributeDefinitions.forEach((attr: AttributeDef) => {
      capabilities[attr.key] = c.capabilities?.[attr.key] ?? attr.defaultValue;
    });

    return {
      ...c,
      vitals: { hp: 100, mp: 100, en: 100, ...(c.vitals || {}) },
      capabilities,
      attributes: { ACT: 10, DEF: 10, SPE: 10, CRI: 5, ...(c.attributes || {}) },
      logicSlots: { slotA: '', slotB: '', slotC: '', totalResult: '', ...(c.logicSlots || {}) },
      statusEffects: c.statusEffects || [],
      elemental: { yangGroup: [], yinGroup: [] , ...(c.elemental || {}) },
      innateSkill: { name: 'Innate Skill', description: '', rarity: 3, ...(c.innateSkill || {}) },
      resonanceMatrix: c.resonanceMatrix || Array(5).fill(0).map(() => Array(5).fill(0)),
      abilitySlots: c.abilitySlots || [{ name: 'Slot 1' }],
      backgroundText: c.backgroundText || ''
    };
  };

  return {
    ...data,
    attributeDefinitions,
    characters: (data.characters || []).map(migrateCharacter),
    boards: data.boards || [],
    locations: data.locations || [],
    cards: data.cards || [],
    modules: data.modules || [],
    items: (data.items || []).map((i: any) => ({
      ...i,
      properties: { stackable: true, maxStack: 99, ...(i.properties || {}) },
      usage: { useType: 'Instant', cooldown: 0, consumeOnUse: true, ...(i.usage || {}) },
      effects: i.effects || [],
      inspector: { selectedEffectId: null, executionLog: [], ...(i.inspector || {}) }
    })),
    events: (data.events || []).map((e: any) => ({
      ...e,
      areaRule: e.areaRule || '',
      trigger: { when: 'OnInteract', condition: '', priority: 1, cooldown: 0, ...(e.trigger || {}) },
      actions: e.actions || [],
      outcomes: e.outcomes || [],
      inspector: { selectedActionId: null, executionLog: [], ...(e.inspector || {}) }
    })),
    rulesets: data.rulesets || [],
    commonPlay: data.commonPlay || [],
    storyNodes: data.storyNodes || [],
    assets: data.assets || {},
    uiTheme: data.uiTheme || 'darkNavy',
    title: data.title || 'Untitled Project',
    updatedAt: data.updatedAt || Date.now(),
    createdAt: data.createdAt || Date.now()
  };
};

export const getStoryIndex = (): StoryIndexItem[] => {
  const raw = localStorage.getItem(INDEX_KEY);
  if (!raw) return [];
  try {
    const index: unknown = JSON.parse(raw);
    return Array.isArray(index) ? index : [];
  } catch {
    return [];
  }
};

export const saveStoryIndex = (index: StoryIndexItem[]) => {
  localStorage.setItem(INDEX_KEY, JSON.stringify(index));
};

export const getStory = (storyId: string): StoryPack | null => {
  const raw = localStorage.getItem(`${STORY_PREFIX}${storyId}`);
  if (!raw) return null;
  try {
    const data = JSON.parse(raw);
    return migrateStory(data);
  } catch (e) {
    console.error("Corruption detected in storage", e);
    return null;
  }
};

export const saveStory = (story: StoryPack) => {
  const key = `${STORY_PREFIX}${story.storyId}`;
  let previous: string | null = null;
  try {
    previous = localStorage.getItem(key);
    const rawIndex = localStorage.getItem(INDEX_KEY);
    const parsed: unknown = rawIndex ? JSON.parse(rawIndex) : [];
    if (!Array.isArray(parsed)) return false;
    const index = [...parsed] as StoryIndexItem[];
    const updatedStory = { ...story, updatedAt: Date.now() };
    const existingIndex = index.findIndex(i => i.storyId === story.storyId);
    const newItem = { storyId: story.storyId, title: story.title, updatedAt: updatedStory.updatedAt,
      projectKind: story.projectKind, ...summarizeProject(story) };
    if (existingIndex > -1) index[existingIndex] = newItem;
    else index.push(newItem);
    localStorage.setItem(key, JSON.stringify(updatedStory));
    try {
      localStorage.setItem(INDEX_KEY, JSON.stringify(index));
    } catch {
      if (previous === null) localStorage.removeItem(key);
      else localStorage.setItem(key, previous);
      return false;
    }
    return true;
  } catch {
    return false;
  }
};

export const deleteStory = (storyId: string) => {
  localStorage.removeItem(`${STORY_PREFIX}${storyId}`);
  clearRunState(storyId);
  const index = getStoryIndex().filter(i => i.storyId !== storyId);
  saveStoryIndex(index);
};

export const exportStory = (story: StoryPack) => {
  const progress = buildBackup(story);
  if (localStorage.getItem(`w3.personal.run.${story.storyId}`) !== null && !progress.runState) {
    alert('จุดเล่นที่เก็บไว้มีปัญหา จึงยังไม่ส่งออกไฟล์ที่อาจขาดข้อมูล');
    return;
  }
  const json = JSON.stringify(progress, null, 2);
  const exportFileDefaultName = `${story.title.replace(/\s+/g, '_')}_pack.json`;
  const androidBridge = (window as Window & { AndroidBridge?: { saveJson(name: string, contents: string): void } }).AndroidBridge;
  if (location.hostname === 'appassets.androidplatform.net' && androidBridge) {
    androidBridge.saveJson(exportFileDefaultName, json);
    return;
  }
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const linkElement = document.createElement('a');
  linkElement.setAttribute('href', url);
  linkElement.setAttribute('download', exportFileDefaultName);
  document.body.appendChild(linkElement);
  linkElement.click();
  linkElement.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 60_000);
};

export const importStory = async (file: File): Promise<ImportedBackup | null> => {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const json = JSON.parse(e.target?.result as string);
        const backup = parseBackup(json);
        if (!backup) alert('ไฟล์สำรองไม่ถูกต้อง หรือจุดเล่นไม่ตรงกับโครงการ');
        resolve(backup);
      } catch (err) {
        alert('Error parsing JSON.');
        resolve(null);
      }
    };
    reader.onerror = () => resolve(null);
    reader.readAsText(file);
  });
};

/** Restore authoring data and progress together; roll both back if storage runs out. */
export const restoreBackup = (backup: ImportedBackup): boolean => {
  const id = backup.story.storyId;
  if (backup.runState && !parseRunState(backup.runState, id)) return false;
  const keys = [`${STORY_PREFIX}${id}`, INDEX_KEY, `w3.personal.run.${id}`];
  try {
    const previous = keys.map(key => localStorage.getItem(key));
    if (!saveStory(backup.story)) return false;
    if (backup.runState ? saveRunState(backup.runState) : clearRunState(id)) return true;
    // Remove the new story first to free room for the prior copy.
    localStorage.removeItem(keys[0]);
    keys.forEach((key, index) => { if (previous[index] === null) localStorage.removeItem(key); else localStorage.setItem(key, previous[index]!); });
    return false;
  } catch {
    return false;
  }
};
