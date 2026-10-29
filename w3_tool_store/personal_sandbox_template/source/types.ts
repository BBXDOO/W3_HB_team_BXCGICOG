
export type UITheme = 'darkNavy' | 'softLight' | 'deepForest' | 'nightBlue' | 'aubergine' | 'custom';
export type ActiveMode = 'EDITOR' | 'PLAYMODE' | 'PLAYGROUND' | 'FREELAND';
export type ProjectKind = 'library' | 'bookcraft' | 'concept';
export type RunSource = 'story' | 'board' | 'cards' | 'characters' | 'items' | 'locations' | 'rules' | 'events' | 'battle' | 'special';
export interface RunSection { id: string; source: RunSource; label: string; icon: string; visible: boolean; }
export interface RunPresentation {
  sections: RunSection[];
  sectionsMigrated?: boolean;
  backgroundColor?: string;
  backgroundAssetId?: string;
}
export type TabId = 'home' | 'story' | 'character' | 'board' | 'location' | 'item' | 'event' | 'rule' | 'commonPlay' | 'play' | 'card';

export interface AttributeDef {
  key: string; // e.g., 'STR'
  label: string; // e.g., 'Strength'
  defaultValue: number;
}

export interface StoryPack {
  storyId: string;
  title: string;
  author?: string; 
  version?: string; 
  description?: string;
  sourceUrl?: string; 
  logoAssetId?: string;
  createdAt: number;
  updatedAt: number;
  uiTheme: UITheme;
  contentStyle?: { fontSize?: number; color?: string; fontWeight?: 'normal' | 'bold' };
  themeColor?: string;
  themeAssetId?: string;
  workspaceAssetId?: string;
  activeMode: ActiveMode;
  projectKind?: ProjectKind; // Older projects remain unclassified until the owner chooses.
  runPresentation?: RunPresentation;
  battleConfig?: BattleConfig;
  
  attributeDefinitions: AttributeDef[]; // Global stats schema
  characters: CharacterPack[];
  boards: BoardPack[];
  locations: LocationPack[];
  cards: CardPack[];
  modules?: ModulePack[]; // Independent module registry; older projects have none.
  items: ItemPack[];
  events: EventPack[];
  rulesets: RulesetPack[];
  commonPlay?: CommonPlayCommand[];
  storyNodes: StoryNode[];
  assets: Record<string, Asset>;
}

/** Rules are authored per project; runtime values live only in RunState. */
export interface BattleConfig {
  elements: string[];
  manaPerTurn?: number; // Default 2. Project-local and editable.
  field: { name: string; locationId?: string; elements: string[]; time?: string; note?: string };
  phases: { id: string; name: string; ruleId?: string }[];
  actions: BattleAction[];
}
export interface BattleAction {
  id: string;
  name: string;
  kind: 'Attack' | 'Def' | 'Skill' | 'Item';
  phaseId: string;
  sourceCardId?: string;
  ruleId?: string;
  cost: Record<string, number>;
  effects: BattleEffect[];
}
export interface BattleScale { stat: string; source: 'self' | 'opponent'; multiplier: number }
export type BattleEffect =
  | { type: 'vital'; target: 'self' | 'opponent'; stat: 'hp' | 'mp' | 'en'; amount: number; scale?: BattleScale }
  | { type: 'mana'; target: 'self' | 'opponent'; element: string; amount: number }
  | { type: 'field'; element: string; enabled: boolean }
  | { type: 'status'; target: 'self' | 'opponent'; status: string; enabled: boolean };

export interface CharacterPack {
  id: string;
  name: string;
  className: string;
  charType: string;
  portraitAssetId?: string;
  vitals: { hp: number; mp: number; en: number; };
  capabilities: Record<string, number>; // Dynamic stats mapped by key
  attributes: { ACT: number; DEF: number; SPE: number; CRI: number; };
  
  logicSlots: {
    slotA?: string;
    slotB?: string;
    slotC?: string;
    totalResult?: string;
  };

  statusEffects: string[];
  elemental: {
    yangGroup: ('E' | 'F' | 'L')[];
    yinGroup: ('R' | 'W' | 'D')[];
  };
  
  innateSkill: {
    name: string;
    description: string;
    rarity: number;
  };

  resonanceMatrix: number[][];
  abilitySlots: { name: string; equippedCardId?: string }[];
  backgroundText: string;
}

export interface CardPack {
  id: string;
  name: string;
  type: string;
  rarity: 'Common' | 'Rare' | 'Epic' | 'Legendary';
  grade: string;
  accessLevel: 'A' | 'B' | 'C' | 'ALL';
  iconAssetId?: string;
  description: string;
  inputCondition: string;
  logicCode: string;
  effectResult: string;
  cost: number;
  cooldownTurns: number;
  moduleSlots?: (string | null)[]; // 2 or 3 references to project modules; no automatic effect execution.
}

export interface ModulePack {
  id: string;
  name: string;
  type: string;
  grade: string;
  description: string;
  parts: { A: string; B: string; C: string };
  battleLink?: { tag: string; ruleId?: string; effects: BattleEffect[] };
}

export interface BoardPack {
  boardId: string;
  title: string;
  width: number;
  height: number;
  viewMode?: 'overview' | 'grid' | 'database' | 'mindmap';
  gridStyle?: 'tiles' | 'dots';
  cellSize?: number;
  showCoordinates?: boolean;
  bgAssetId?: string;
  cellMap: Record<string, CellPack>; 
  explored: Record<string, boolean>;
  visionRangeDefault: number;
  movementPerTurnDefault: number;
}

export interface CellPack {
  x: number;
  y: number;
  name?: string;
  desc?: string;
  markerColor?: string;
  markerIcon?: string;
  locationRefId?: string;
  eventRefs?: string[];
  parentKey?: string;
  type?: 'Empty' | 'Location' | 'Encounter' | 'SafeZone';
}

export interface RulesetPack {
  id: string;
  name: string;
  blocks: RuleBlock[];
  modifiers: { key: string; value: string }[];
}

export interface CommonPlayCommand {
  id: string; // Stable project-local reference, independent of display name.
  name: string;
  description: string;
  inputKeys: string[];
}

export interface RuleBlock {
  id?: string; // Older flat blocks have no ID; retain them when loading.
  title: string;
  content: string;
  kind?: 'reference' | 'condition';
  children?: RuleBlock[];
  inputKey?: string; // Key in a supplied context; no project-specific meaning.
  operator?: '==' | '!=' | '>' | '>=' | '<' | '<=' | 'exists';
  expected?: string;
  commandRef?: string; // Reserved reference to a future Common Play command.
}

export interface LocationPack {
  locationId: string;
  title: string;
  zone?: string;
  areaProfile: {
    type?: 'Indoor' | 'Outdoor' | 'Dungeon' | 'City';
    threat?: number;
    access?: 'Public' | 'Restricted';
    timeRule?: 'Any' | 'Day' | 'Night';
  };
  description?: string;
  triggers: TriggerPack[];
  loot: LootPack[];
  eventRefs: string[];
  imageAssetId?: string;
}

export interface EffectDef { id: string; condition: string; effect: string; target: string; }

export interface ItemPack {
  id: string;
  itemId: string;
  name: string;
  category: string;
  rarity: string;
  properties: {
    stackable?: boolean;
    maxStack?: number;
    weight?: number;
    value?: number;
    tradable?: boolean;
    description?: string;
  };
  description: string;
  iconAssetId?: string;
  usage: { useType: string; cooldown: number; consumeOnUse: boolean; };
  effects: EffectDef[];
  inspector: { selectedEffectId: string | null; executionLog: string[]; };
  linkedEvents: string[];
  linkedLocations: string[];
}

export interface ActionDef { id: string; actionType: string; target: string; payload: string; }
export interface OutcomeDef { id: string; condition: string; result: string; }

export interface EventPack {
  id: string;
  eventId: string;
  name: string;
  eventType: string;
  iconAssetId?: string; // New: Custom Icon
  targetBoardId?: string; // Spatial Ref: Board
  targetX?: number; // Spatial Ref: X
  targetY?: number; // Spatial Ref: Y
  areaRule: string; // Rule of Area (6)
  trigger: { when: string; condition: string; priority: number; cooldown: number; };
  actions: ActionDef[];
  outcomes: OutcomeDef[];
  inspector: { selectedActionId: string | null; executionLog: string[]; };
}

export interface TriggerPack { id: string; when: 'enter' | 'click'; condition?: string; effect?: string; }
export interface LootPack { id: string; itemRefId: string; chance: number; amount: number; }

export interface StoryNode {
  nodeId: string;
  type: 'NarrativeBlock' | 'ChoiceNode' | 'EventHook';
  title?: string;
  body?: string;
  imageAssetId?: string;
  choices?: { label: string; toNodeId: string }[];
}

export interface Asset { id: string; name: string; dataUrl: string; }
