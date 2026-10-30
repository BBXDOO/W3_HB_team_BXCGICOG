
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
import { CommonPlayTab } from '../common/CommonPlayTab';
import { PlaytestTab } from '../play/PlaytestTab';
import { ContentFormatProvider, FormatPanel, RichContent } from './ContentFormat';
import { AppCommands } from './AppCommands';
import { SplitLayout60_40 } from '../../ui/layout/SplitLayout60_40';
import { MonitorCore } from '../../ui/components/MonitorCore';
import { generateId, deepClone } from '../../core/utils';
import { exportStory } from '../../core/storage';

interface EditorShellProps {
  story: StoryPack;
  onSave: (story: StoryPack) => boolean;
  onExit: () => void;
}

export const EditorShell: React.FC<EditorShellProps> = ({ story: initialStory, onSave, onExit }) => {
  const [story, setStory] = useState<StoryPack>(initialStory);
  const [navigationCollapsed, setNavigationCollapsed] = useState(false);
  const [activeTab, setActiveTab] = useState<TabId>('home');
  const [isDirty, setIsDirty] = useState(false);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [isFormatOpen, setIsFormatOpen] = useState(false);
  const [isCommandOpen, setIsCommandOpen] = useState(false);
  const [navigationTarget, setNavigationTarget] = useState<string | null>(null);
  const [showSaveToast, setShowSaveToast] = useState(false);
  const [saveError, setSaveError] = useState(false);
  const [backgroundImage, setBackgroundImage] = useState(() => {
    try { return localStorage.getItem('w3.personal.background-image') || ''; } catch { return ''; }
  });

  // Existing projects may carry the older forest palette. Move each project
  // once to the new default; a theme chosen afterwards remains the user's choice.
  useEffect(() => {
    const key = `w3.personal.instrument-theme.${initialStory.storyId}`;
    try {
      if (localStorage.getItem(key)) return;
      if (initialStory.uiTheme !== 'darkNavy') {
        const migrated = { ...initialStory, uiTheme: 'darkNavy' as UITheme };
        if (!onSave(migrated)) return;
        setStory(migrated);
      }
      localStorage.setItem(key, '1');
    } catch { /* The app remains usable when preference storage is unavailable. */ }
  }, [initialStory, onSave]);

  useEffect(() => {
    const theme = story.uiTheme || 'darkNavy';
    const classes = ['theme-light', 'theme-forest', 'theme-night-blue', 'theme-aubergine', 'theme-custom', 'theme-image'];
    document.body.classList.remove(...classes);
    const themeClass = {
      softLight: 'theme-light', deepForest: 'theme-forest',
      nightBlue: 'theme-night-blue', aubergine: 'theme-aubergine', custom: 'theme-custom'
    }[theme];
    if (themeClass) document.body.classList.add(themeClass);
    if (story.uiTheme === 'custom' && /^#[0-9a-f]{6}$/i.test(story.themeColor || '')) document.body.style.setProperty('--custom-theme-color', story.themeColor!);
    else document.body.style.removeProperty('--custom-theme-color');
    return () => { document.body.classList.remove(...classes); document.body.style.removeProperty('--custom-theme-color'); };
  }, [story.uiTheme, story.themeColor]);

  useEffect(() => {
    const image = story.workspaceAssetId && story.assets[story.workspaceAssetId]?.dataUrl
      || backgroundImage || story.themeAssetId && story.assets[story.themeAssetId]?.dataUrl;
    if (image) document.body.style.setProperty('--personal-bg-image', `url("${image}")`);
    else document.body.style.removeProperty('--personal-bg-image');
    return () => { document.body.style.removeProperty('--personal-bg-image'); };
  }, [backgroundImage, story.workspaceAssetId, story.themeAssetId, story.assets]);

  const updateStory = (newStory: StoryPack) => {
    setStory({ ...newStory, updatedAt: Date.now() });
    setIsDirty(true);
    setSaveError(false);
  };

  useEffect(() => {
    if (!isDirty) return;
    const timer = window.setTimeout(() => {
      if (onSave(story)) { setIsDirty(false); setSaveError(false); }
      else setSaveError(true);
    }, 2000);
    return () => window.clearTimeout(timer);
  }, [story, isDirty, onSave]);

  useEffect(() => {
    const saveOnLeave = () => {
      if (isDirty) onSave(story);
    };
    window.addEventListener('pagehide', saveOnLeave);
    return () => window.removeEventListener('pagehide', saveOnLeave);
  }, [story, isDirty, onSave]);

  const toggleTheme = () => {
    const nextTheme: UITheme = story.uiTheme === 'darkNavy' ? 'deepForest' : 'darkNavy';
    updateStory({ ...story, uiTheme: nextTheme });
  };

  const chooseBackgroundImage = (file: File) => {
    if (!file.type.startsWith('image/') || file.size > 15 * 1024 * 1024) {
      alert('กรุณาเลือกรูปภาพขนาดไม่เกิน 15 MB'); return;
    }
    const objectUrl = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => {
      const scale = Math.min(1, 2048 / Math.max(img.width, img.height));
      const canvas = document.createElement('canvas');
      canvas.width = Math.max(1, Math.round(img.width * scale));
      canvas.height = Math.max(1, Math.round(img.height * scale));
      canvas.getContext('2d')?.drawImage(img, 0, 0, canvas.width, canvas.height);
      URL.revokeObjectURL(objectUrl);
      try {
        const data = canvas.toDataURL('image/jpeg', 0.86);
        const assetId = generateId('workspace');
        const next = { ...story, assets: { ...story.assets, [assetId]: { id: assetId, name: file.name, dataUrl: data } }, workspaceAssetId: assetId };
        if (!onSave(next)) throw new Error('storage full');
        setStory(next);
        setIsDirty(false);
        localStorage.removeItem('w3.personal.background-image');
        setBackgroundImage('');
      } catch { alert('พื้นที่เก็บข้อมูลภาพไม่พอ กรุณาเลือกรูปที่เล็กลง'); }
    };
    img.onerror = () => { URL.revokeObjectURL(objectUrl); alert('อ่านรูปภาพไม่สำเร็จ'); };
    img.src = objectUrl;
  };

  const clearBackgroundImage = () => {
    try { localStorage.removeItem('w3.personal.background-image'); } catch { /* optional image */ }
    setBackgroundImage('');
    updateStory({ ...story, workspaceAssetId: undefined, themeAssetId: undefined });
  };

  const handleSave = (): boolean => {
    if (!onSave(story)) { setSaveError(true); return false; }
    setIsDirty(false);
    setSaveError(false);
    setShowSaveToast(true);
    setTimeout(() => setShowSaveToast(false), 4000);
    return true;
  };

  const handleExit = () => {
    if (!onSave(story)) { setSaveError(true); return; }
    onExit();
  };

  const handleContextualAdd = () => {
    if (activeTab === 'story') {
      const add = document.getElementById('tab-primary-add') as HTMLButtonElement | null;
      if (add) { add.click(); return; }
    }
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
        const newCard: CardPack = { id: generateId('crd'), name: 'NEW CARD', type: 'SKILL', rarity: 'Common', grade: 'C', accessLevel: 'A', description: '', inputCondition: '', logicCode: '', effectResult: '', cost: 0, cooldownTurns: 0 };
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
        const newNode: StoryNode = { nodeId: generateId('node'), type: 'NarrativeBlock', title: 'ตอนใหม่', body: '', bodyFormat: 'markdown', choices: [] };
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
    onToggleAgent: () => setIsFormatOpen(!isFormatOpen),
    onToggleCommands: () => setIsCommandOpen(!isCommandOpen),
    isAgentOpen: isFormatOpen
  };

  const renderTabContent = () => {
    const commonProps = { story, onChange: updateStory, toolActions };

    switch (activeTab) {
      case 'home': return <DashboardTab {...commonProps} />;
      case 'story': return <StoryTab {...commonProps} navigationTarget={navigationTarget} onCommit={handleSave} saveState={saveError ? 'error' : isDirty ? 'pending' : 'saved'} />;
      case 'character': return <CharactersTab {...commonProps} />;
      case 'board': return <BoardTab {...commonProps} navigationTarget={navigationTarget} />;
      case 'rule': return <RulesTab {...commonProps} navigationTarget={navigationTarget} />;
      case 'commonPlay': return <CommonPlayTab {...commonProps} />;
      case 'card': return <CardsTab {...commonProps} navigationTarget={navigationTarget} />;
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
            bottomMain={<MonitorCore title="Location Telemetry" isEmpty={!selectedLoc}>{selectedLoc && <div className="p-10 flex flex-col gap-4 animate-in fade-in"><h2 className="text-5xl font-black uppercase border-l-8 border-blue-600 pl-8 leading-none text-[var(--text)]">{selectedLoc.title}</h2><p className="mt-4 text-xl text-[var(--text-dim)] font-medium max-w-2xl leading-relaxed"><RichContent value={selectedLoc.description || 'System awaiting data input...'} /></p></div>}</MonitorCore>}
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
    <ContentFormatProvider story={story} onStyleChange={style => updateStory({ ...story, contentStyle: style })} navigate={(tab, id) => { setNavigationTarget(id); setActiveTab(tab); if (tab === 'location' || tab === 'item') setSelectedId(id); }}>
    <div className={`editor-shell h-screen flex flex-col overflow-hidden bg-[var(--bg)] ${navigationCollapsed ? 'nav-collapsed' : ''} ${story.workspaceAssetId || backgroundImage || story.themeAssetId ? 'has-workspace-image' : ''}`} style={{ '--content-font-size': `${story.contentStyle?.fontSize || 12}px`, '--content-color': story.contentStyle?.color || 'var(--text)', '--content-weight': story.contentStyle?.fontWeight || 'normal' } as React.CSSProperties}>
      <TopBar 
        navigationCollapsed={navigationCollapsed}
        onToggleNavigation={() => setNavigationCollapsed(!navigationCollapsed)}
        story={story} 
        isDirty={isDirty} 
        onSave={handleSave} 
        onUndo={() => {}} 
        onExport={() => exportStory(story)} 
        onExit={handleExit} 
        onToggleTheme={toggleTheme}
        currentTheme={story.uiTheme || 'darkNavy'}
        onSelectTheme={(theme) => updateStory({ ...story, uiTheme: theme })}
        customThemeColor={story.themeColor || '#368a77'}
        onSelectCustomColor={(color) => updateStory({ ...story, uiTheme: 'custom', themeColor: color })}
        onChooseBackgroundImage={chooseBackgroundImage}
        onClearBackgroundImage={clearBackgroundImage}
        hasBackgroundImage={Boolean(story.workspaceAssetId || backgroundImage || story.themeAssetId)}
      />
      
      <div className="workspace-stage"><div className="editor-upper flex flex-1 min-h-0 overflow-hidden relative">
        <LeftNav 
          activeTab={activeTab} 
          onTabChange={(t) => { setActiveTab(t); setSelectedId(null); setNavigationTarget(null); }} 
          onToggleFormat={() => setIsFormatOpen(!isFormatOpen)}
          isFormatOpen={isFormatOpen}
          isDirty={isDirty}
          onSave={handleSave}
        />
        <main className="flex-1 overflow-hidden relative">
          {renderTabContent()}
        </main>
      </div><div id="workspace-preview-host" /></div>

      {isFormatOpen && <FormatPanel story={story} onClose={() => setIsFormatOpen(false)} />}
      {isCommandOpen && <AppCommands story={story} activeTab={activeTab} onAdd={handleContextualAdd} onSave={handleSave} onExport={() => exportStory(story)} onClose={() => setIsCommandOpen(false)} />}

      {saveError && <div role="alert" className="absolute bottom-4 right-4 z-50 max-w-sm rounded-xl bg-red-950 border border-red-400 p-4 text-sm text-white shadow-2xl">
        บันทึกไม่สำเร็จ ข้อมูลที่แก้ยังอยู่ในหน้านี้ โปรดส่งออกสำเนาโครงการหรือตรวจพื้นที่เก็บข้อมูล แล้วกดบันทึกอีกครั้ง
        <button className="block mt-2 underline" onClick={() => exportStory(story)}>ส่งออกสำเนา JSON</button>
      </div>}
      {showSaveToast && (
        <div className="fixed bottom-12 left-1/2 -translate-x-1/2 px-10 py-5 bg-[#22C55E] text-white rounded-[32px] font-black text-xs uppercase tracking-[0.3em] shadow-[0_20px_50px_rgba(34,197,94,0.5)] z-[100] animate-save flex items-center gap-5 border border-white/20 backdrop-blur-md">
          <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center text-xl">💾</div>
          <span>บันทึกหัวใจของโปรเจกต์ลงเครื่องแล้วครับเพื่อน</span>
        </div>
      )}
    </div>
    </ContentFormatProvider>
  );
};
