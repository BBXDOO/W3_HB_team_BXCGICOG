
import { StoryPack, CharacterPack, ItemPack, EventPack, AttributeDef } from '../types';

const INDEX_KEY = 'w3idp.story.index';
const STORY_PREFIX = 'w3idp.story.';

export interface StoryIndexItem {
  storyId: string;
  title: string;
  updatedAt: number;
}

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
  const attributeDefinitions = data.attributeDefinitions || DEFAULT_ATTRIBUTES;

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
  return raw ? JSON.parse(raw) : [];
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
  const updatedStory = { ...story, updatedAt: Date.now() };
  localStorage.setItem(`${STORY_PREFIX}${story.storyId}`, JSON.stringify(updatedStory));
  
  const index = getStoryIndex();
  const existingIndex = index.findIndex(i => i.storyId === story.storyId);
  const newItem = { storyId: story.storyId, title: story.title, updatedAt: updatedStory.updatedAt };
  
  if (existingIndex > -1) {
    index[existingIndex] = newItem;
  } else {
    index.push(newItem);
  }
  
  saveStoryIndex(index);
};

export const deleteStory = (storyId: string) => {
  localStorage.removeItem(`${STORY_PREFIX}${storyId}`);
  const index = getStoryIndex().filter(i => i.storyId !== storyId);
  saveStoryIndex(index);
};

export const exportStory = (story: StoryPack) => {
  const dataStr = JSON.stringify(story, null, 2);
  const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
  const exportFileDefaultName = `${story.title.replace(/\s+/g, '_')}_pack.json`;
  const linkElement = document.createElement('a');
  linkElement.setAttribute('href', dataUri);
  linkElement.setAttribute('download', exportFileDefaultName);
  linkElement.click();
};

export const importStory = async (file: File): Promise<StoryPack | null> => {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const json = JSON.parse(e.target?.result as string);
        resolve(migrateStory(json));
      } catch (err) {
        alert('Error parsing JSON.');
        resolve(null);
      }
    };
    reader.readAsText(file);
  });
};
