
import React, { useState, useEffect } from 'react';
import { StoryPack, TabId, UITheme, CharacterPack, LocationPack, ItemPack, CardPack, EventPack, StoryNode, RulesetPack, BoardPack } from '../../types';
import { TopBar } from './TopBar';
import { LeftNav } from './LeftNav';
import { Button } from '../../ui/components/Button';
import { LocationSheet } from '../location/LocationSheet';
import { ItemSheet } from '../item/ItemSheet';
import { EventsTab } from '../events/EventsTab';
import { StoryTab } from '../story/StoryTab';
import { CharactersTab } from '../characters/CharactersTab';
import { CardsTab } from '../cards/CardsTab';
import { BoardTab } from '../board/BoardTab';
import { DashboardTab } from '../dashboard/DashboardTab';
import { RulesTab } from '../rules/RulesTab';
import { PlaytestTab } from '../play/PlaytestTab';
import { LogicAgent } from '../agent/LogicAgent';
import { SplitLayout60_40 } from '../../ui/layout/SplitLayout60_40';
import { MonitorCore } from '../../ui/components/MonitorCore';
import { generateId, deepClone } from '../../core/utils';
import { exportStory } from '../../core/storage';

interface EditorShellProps {
  story: StoryPack;
  onSave: (story: StoryPack) => void;
  onExit: () => void;
}

export const EditorShell: React.FC<EditorShellProps> = ({ story: initialStory, onSave, onExit }) => {
  const [story, setStory] = useState<StoryPack>(initialStory);
  const [activeTab, setActiveTab] = useState<TabId>('home');
  const [isDirty, setIsDirty] = useState(false);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [isAgentOpen, setIsAgentOpen] = useState(false);
  const [showSaveToast, setShowSaveToast] = useState(false);

  useEffect(() => {
    const theme = story.uiTheme || 'darkNavy';
    if (theme === 'softLight') {
      document.body.classList.add('theme-light');
    } else {
      document.body.classList.remove('theme-light');
    }
  }, [story.uiTheme]);

  const updateStory = (newStory: StoryPack) => {
    setStory(newStory);
    setIsDirty(true);
  };

  const toggleTheme = () => {
    const nextTheme: UITheme = story.uiTheme === 'darkNavy' ? 'softLight' : 'darkNavy';
    updateStory({ ...story, uiTheme: nextTheme });
  };

  const handleSave = () => {
    onSave(story);
    setIsDirty(false);
    setShowSaveToast(true);
    setTimeout(() => setShowSaveToast(false), 4000);
  };

  const handleContextualAdd = () => {
    const id = generateId();
    let updatedStory = { ...story };

    switch (activeTab) {
      case 'character':
        const newChar: CharacterPack = {
          id: generateId('chr'), name: 'New Unit', className: 'Novice', charType: 'NPC',
          vitals: { hp: 100, mp: 100, en: 100 },
          capabilities: { STR: 5, DEX: 5, INT: 5, TEC: 5, KNO: 5, VIS: 5, TOL: 5, POW: 5, ESN: 5, LOC: 5 },
          attributes: { ACT: 10, DEF: 10, SPE: 10, CRI: 5 },
          logicSlots: { slotA: '', slotB: '', slotC: '', totalResult: '' },
          statusEffects: [],
          elemental: { yangGroup: [], yinGroup: [] },
          innateSkill: { name: 'Innate Skill', description: '', rarity: 3 },
          resonanceMatrix: Array(5).fill(0).map(() => Array(5).fill(0)),
          abilitySlots: [{ name: 'Slot 1' }], backgroundText: ''
        };
        updatedStory.characters = [...story.characters, newChar];
        setSelectedId(newChar.id);
        break;
      case 'location':
        const newLoc: LocationPack = { locationId: generateId('loc'), title: 'New Sector', areaProfile: { type: 'Outdoor', threat: 0, access: 'Public', timeRule: 'Any' }, triggers: [], loot: [], eventRefs: [] };
        updatedStory.locations = [...story.locations, newLoc];
        setSelectedId(newLoc.locationId);
        break;
      case 'item':
        const newItem: ItemPack = { id: generateId('itm'), itemId: 'i' + Date.now(), name: 'New Asset', category: 'Consumable', rarity: 'Common', properties: { stackable: true, maxStack: 99 }, description: '', usage: { useType: 'Instant', cooldown: 0, consumeOnUse: true }, effects: [], inspector: { selectedEffectId: null, executionLog: [] }, linkedEvents: [], linkedLocations: [] };
        updatedStory.items = [...story.items, newItem];
        setSelectedId(newItem.id);
        break;
      case 'card':
        const newCard: CardPack = { id: generateId('crd'), name: 'NEW MODULE', type: 'SKILL', rarity: 'Common', grade: 'C', accessLevel: 'A', description: '', inputCondition: '', logicCode: '', effectResult: '', cost: 0, cooldownTurns: 0 };
        updatedStory.cards = [...story.cards, newCard];
        setSelectedId(newCard.id);
        break;
      case 'event':
        // Fix: Add required areaRule property to the new EventPack object
        const newEv: EventPack = { id: generateId('evt'), eventId: id, name: 'New Logic Trigger', eventType: 'Special', areaRule: '', trigger: { when: 'OnInteract', condition: '', priority: 1, cooldown: 0 }, actions: [], outcomes: [], inspector: { selectedActionId: null, executionLog: [] } };
        updatedStory.events = [...story.events, newEv];
        setSelectedId(newEv.id);
        break;
      case 'story':
        const newNode: StoryNode = { nodeId: generateId('node'), type: 'NarrativeBlock', title: 'New Narrative Point', body: '', choices: [] };
        updatedStory.storyNodes = [...story.storyNodes, newNode];
        setSelectedId(newNode.nodeId);
        break;
      case 'rule':
        const newRule: RulesetPack = { id: generateId('rule'), name: 'New System Protocol', blocks: [{title:'Rules Block', content:''}], modifiers: [] };
        updatedStory.rulesets = [...(story.rulesets || []), newRule];
        setSelectedId(newRule.id);
        break;
      case 'board':
        const newBoard: BoardPack = { boardId: generateId('brd'), title: 'NEW WORLD', width: 12, height: 12, cellMap: {}, explored: {}, visionRangeDefault: 2, movementPerTurnDefault: 2 };
        updatedStory.boards = [...story.boards, newBoard];
        // Fix: Replace non-existent setSelectedBoardId with setSelectedId as suggested by compiler error message
        setSelectedId(newBoard.boardId);
        break;
      default:
        return;
    }
    updateStory(updatedStory);
  };

  const toolActions = {
    onSearch: () => alert("Nexus Search is indexing the registry... (Coming soon)"),
    onAdd: handleContextualAdd,
    onExport: () => exportStory(story),
    onToggleTheme: toggleTheme,
    onToggleAgent: () => setIsAgentOpen(!isAgentOpen),
    isAgentOpen
  };

  const renderTabContent = () => {
    const commonProps = { story, onChange: updateStory, toolActions };

    switch (activeTab) {
      case 'home': return <DashboardTab {...commonProps} />;
      case 'story': return <StoryTab {...commonProps} />;
      case 'character': return <CharactersTab {...commonProps} />;
      case 'board': return <BoardTab {...commonProps} />;
      case 'rule': return <RulesTab {...commonProps} />;
      case 'card': return <CardsTab {...commonProps} />;
      case 'event': return <EventsTab {...commonProps} />;
      case 'play': return <PlaytestTab {...commonProps} />;
      
      case 'location':
        const selectedLoc = story.locations.find(l => l.locationId === selectedId);
        return (
          <SplitLayout60_40
            toolActions={toolActions}
            topLeft={<div className="flex flex-col h-full overflow-y-auto scroll-container">
              <div className="p-4 border-b border-[var(--border)]">
                 <Button variant="accent" className="w-full h-11 rounded-xl font-black uppercase text-[10px]" onClick={handleContextualAdd}>+ NEW SECTOR</Button>
              </div>
              <div className="flex-1">
                {story.locations.map(loc => (
                  <button key={loc.locationId} onClick={() => setSelectedId(loc.locationId)} className={`w-full p-5 text-left border-b border-[var(--border)] transition-all ${selectedId === loc.locationId ? 'bg-[var(--surface)] border-l-4 border-l-blue-600' : 'hover:bg-black/5'}`}>
                    <div className="text-sm font-black text-[var(--text)] uppercase truncate">{loc.title}</div>
                    <div className="text-[9px] text-[var(--text-dim)] uppercase font-black tracking-widest mt-1">{loc.zone || 'UNDEFINED'}</div>
                  </button>
                ))}
                {story.locations.length === 0 && <div className="p-10 text-center text-[10px] opacity-20 font-black uppercase tracking-widest italic">Sector List Empty</div>}
              </div>
            </div>}
            topRight={<div className="overflow-y-auto h-full scroll-container">{selectedLoc ? <LocationSheet location={selectedLoc} onChange={(updated) => updateStory({ ...story, locations: story.locations.map(l => l.locationId === updated.locationId ? updated : l) })} onDelete={() => { updateStory({ ...story, locations: story.locations.filter(l => l.locationId !== selectedLoc.locationId) }); setSelectedId(null); }} /> : <div className="p-20 text-center text-[11px] italic opacity-20 uppercase font-black tracking-widest">Select Sector Registry</div>}</div>}
            bottomMain={<MonitorCore title="Location Telemetry" isEmpty={!selectedLoc}>{selectedLoc && <div className="p-10 flex flex-col gap-4 animate-in fade-in"><h2 className="text-5xl font-black uppercase border-l-8 border-blue-600 pl-8 leading-none text-[var(--text)]">{selectedLoc.title}</h2><p className="mt-4 text-xl text-[var(--text-dim)] font-medium max-w-2xl leading-relaxed">{selectedLoc.description || 'System awaiting data input...'}</p></div>}</MonitorCore>}
          />
        );

      case 'item':
        const selectedItem = story.items.find(i => i.id === selectedId);
        return (
          <SplitLayout60_40
            toolActions={toolActions}
            topLeft={<div className="flex flex-col h-full overflow-y-auto scroll-container">
              <div className="p-4 border-b border-[var(--border)]">
                <Button variant="accent" className="w-full h-11 rounded-xl font-black uppercase text-[10px]" onClick={handleContextualAdd}>+ NEW ASSET</Button>
              </div>
              <div className="flex-1">
                {story.items.map(item => (
                  <button key={item.id} onClick={() => setSelectedId(item.id)} className={`w-full p-5 text-left border-b border-[var(--border)] transition-all ${selectedId === item.id ? 'bg-[var(--surface)] border-l-4 border-l-blue-600' : 'hover:bg-black/5'}`}>
                    <div className="text-sm font-black text-[var(--text)] uppercase truncate">{item.name}</div>
                    <div className="text-[9px] text-[var(--text-dim)] uppercase font-black tracking-widest mt-1">{item.category} • {item.rarity}</div>
                  </button>
                ))}
                {story.items.length === 0 && <div className="p-10 text-center text-[10px] opacity-20 font-black uppercase tracking-widest italic">Asset List Empty</div>}
              </div>
            </div>}
            topRight={<div className="overflow-y-auto h-full scroll-container">{selectedItem ? <ItemSheet item={selectedItem as any} onChange={(updated) => updateStory({ ...story, items: story.items.map(i => i.id === updated.id ? updated : i) })} onDelete={() => { updateStory({ ...story, items: story.items.filter(i => i.id !== selectedItem.id) }); setSelectedId(null); }} /> : <div className="p-20 text-center text-[11px] italic opacity-20 uppercase font-black tracking-widest">Select Asset Registry</div>}</div>}
            bottomMain={<MonitorCore title="Asset Manifest View" isEmpty={!selectedItem}>{selectedItem && <div className="p-10 flex gap-10 items-center animate-in fade-in"><div className="w-32 h-32 w3-card-inset flex items-center justify-center text-6xl shadow-2xl rounded-[40px] border-2 border-white/5">🎒</div><div><h2 className="text-5xl font-black uppercase leading-none text-[var(--text)]">{selectedItem.name}</h2><p className="text-xl text-[var(--text-dim)] mt-6 font-medium max-w-xl">{selectedItem.description || 'Manifest awaiting description...'}</p></div></div>}</MonitorCore>}
          />
        );

      default:
        return null;
    }
  };

  return (
    <div className="h-screen flex flex-col overflow-hidden bg-[var(--bg)]">
      <TopBar 
        story={story} 
        isDirty={isDirty} 
        onSave={handleSave} 
        onUndo={() => {}} 
        onExport={() => exportStory(story)} 
        onExit={onExit} 
        onToggleTheme={toggleTheme}
      />
      
      <div className="flex flex-1 overflow-hidden relative">
        <LeftNav 
          activeTab={activeTab} 
          onTabChange={(t) => { setActiveTab(t); setSelectedId(null); }} 
          onToggleAgent={() => setIsAgentOpen(!isAgentOpen)}
          isAgentOpen={isAgentOpen}
          isDirty={isDirty}
          onSave={handleSave}
        />
        <main className="flex-1 overflow-hidden relative">
          {renderTabContent()}
        </main>
      </div>

      <LogicAgent 
        story={story} 
        activeTab={activeTab} 
        selectedId={selectedId} 
        onApplyFix={updateStory} 
        isOpen={isAgentOpen}
        onClose={() => setIsAgentOpen(false)}
      />

      {showSaveToast && (
        <div className="fixed bottom-12 left-1/2 -translate-x-1/2 px-10 py-5 bg-[#22C55E] text-white rounded-[32px] font-black text-xs uppercase tracking-[0.3em] shadow-[0_20px_50px_rgba(34,197,94,0.5)] z-[100] animate-save flex items-center gap-5 border border-white/20 backdrop-blur-md">
          <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center text-xl">💾</div>
          <span>บันทึกหัวใจของโปรเจกต์ลงเครื่องแล้วครับเพื่อน</span>
        </div>
      )}
    </div>
  );
};
