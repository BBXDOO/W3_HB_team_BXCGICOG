import type { ProjectKind, StoryPack } from '../types';
import { DEFAULT_ATTRIBUTES } from './storage';
import { defaultRunPresentation } from './runPresentation';

/** Each invocation creates fresh collections and attribute definitions. */
export const createEmptyProject = (storyId: string, projectKind: ProjectKind, title: string): StoryPack => {
  const now = Date.now();
  return {
    storyId,
    title: title.trim(),
    author: 'ARCHITECT',
    version: 'v0.1.0',
    projectStatus: 'draft',
    projectProgress: 0,
    description: '',
    createdAt: now,
    updatedAt: now,
    uiTheme: 'darkNavy',
    activeMode: 'EDITOR',
    projectKind,
    runPresentation: defaultRunPresentation(projectKind),
    battleConfig: {
      elements: [], manaPerTurn: 2, field: { name: '', elements: [] },
      phases: [{ id: 'main', name: 'ช่วงหลัก' }, { id: 'followup', name: 'ช่วงถัดไป' }], actions: []
    },
    attributeDefinitions: DEFAULT_ATTRIBUTES.map(attribute => ({ ...attribute })),
    characters: [], boards: [], locations: [], cards: [], modules: [], items: [],
    events: [], rulesets: [], commonPlay: [], storyNodes: [], assets: {}
  };
};
