
export type UITheme = 'darkNavy' | 'softLight';
export type ActiveMode = 'EDITOR' | 'PLAYMODE' | 'PLAYGROUND' | 'FREELAND';
export type TabId = 'home' | 'story' | 'character' | 'board' | 'location' | 'item' | 'event' | 'rule' | 'play' | 'card';

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
  activeMode: ActiveMode;
  
  attributeDefinitions: AttributeDef[]; // Global stats schema
  characters: CharacterPack[];
  boards: BoardPack[];
  locations: LocationPack[];
  cards: CardPack[];
  items: ItemPack[];
  events: EventPack[];
  rulesets: RulesetPack[];
  storyNodes: StoryNode[];
  assets: Record<string, Asset>;
}

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
}

export interface BoardPack {
  boardId: string;
  title: string;
  width: number;
  height: number;
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
  type?: 'Empty' | 'Location' | 'Encounter' | 'SafeZone';
}

export interface RulesetPack {
  id: string;
  name: string;
  blocks: { title: string; content: string }[];
  modifiers: { key: string; value: string }[];
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
