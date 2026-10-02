
import React, { useState, useMemo, useEffect } from 'react';
import { StoryPack, CharacterPack, CardPack, ItemPack, LocationPack } from '../../types';
import { Button } from '../../ui/components/Button';
import { Card } from '../../ui/components/Card';
import { getStatusColor } from '../../core/utils';
import { saveStory, getStory } from '../../core/storage';

interface PlaytestTabProps {
  story: StoryPack;
  onChange: (updated: StoryPack) => void;
  toolActions?: any;
}

type PlayView = 'story' | 'inventory' | 'character' | 'cards';

export const PlaytestTab: React.FC<PlaytestTabProps> = ({ story, onChange, toolActions }) => {
  const [activeView, setActiveView] = useState<PlayView>('story');
  const [activeCharId, setActiveCharId] = useState<string | null>(story.characters[0]?.id || null);
  const [logs, setLogs] = useState<{msg: string, type: 'system' | 'narrative' | 'combat' | 'item'}[]>([]);
  const [currentNodeIdx, setCurrentNodeIdx] = useState(0);
  const [isBooting, setIsBooting] = useState(true);
  const [bootProgress, setBootProgress] = useState(0);
  const [notification, setNotification] = useState<string | null>(null);
  const [isGlitching, setIsGlitching] = useState(false);

  const activeChar = useMemo(() => story.characters.find(c => c.id === activeCharId), [story.characters, activeCharId]);
  const activeNode = story.storyNodes[currentNodeIdx] || null;

  // Cinematic Boot Sequence
  useEffect(() => {
    const timer = setInterval(() => {
      setBootProgress(prev => {
        if (prev >= 100) {
          clearInterval(timer);
          setTimeout(() => setIsBooting(false), 800);
          return 100;
        }
        return prev + 4;
      });
    }, 30); 
    
    addLog(`NEXUS_OS: Loading universe [${story.title}]...`, 'system');
    addLog('INIT_HARDWARE: Secure isolation link established.', 'system');
    
    return () => clearInterval(timer);
  }, [story.storyId]);

  const addLog = (msg: string, type: 'system' | 'narrative' | 'combat' | 'item' = 'system') => {
    setLogs(prev => [{ msg, type }, ...prev].slice(0, 50));
  };

  const showNotify = (msg: string) => {
    setNotification(msg);
    setTimeout(() => setNotification(null), 2000);
  };

  const triggerGlitch = (view: PlayView) => {
    setIsGlitching(true);
    setActiveView(view);
    addLog(`VIEW_SWITCH: Switched to ${view.toUpperCase()} module.`, 'system');
    setTimeout(() => setIsGlitching(false), 200);
  };

  const handleChoice = (label: string, nextNodeId: string) => {
    addLog(`DECISION: "${label}"`, 'narrative');
    const nextIdx = story.storyNodes.findIndex(n => n.nodeId === nextNodeId);
    if (nextIdx !== -1) {
      setCurrentNodeIdx(nextIdx);
    } else {
      addLog('ERR_LINK: Destination node unreachable.', 'system');
    }
  };

  const simulateUseItem = (item: ItemPack) => {
    addLog(`ACTION_INV: Triggered [${item.name}] usage logic.`, 'item');
    addLog(`RESULT: Execution type [${item.usage.useType}] confirmed.`, 'system');
    showNotify(`USED: ${item.name}`);
  };

  const simulateCardTrigger = (card: CardPack) => {
    addLog(`MODULE_EXEC: Processing [${card.name}] logic...`, 'combat');
    addLog(`OUTPUT_BUFFER: ${card.effectResult}`, 'combat');
    showNotify(`ACTIVE: ${card.name}`);
  };

  const handleSave = () => {
    saveStory(story);
    addLog('STORY_STATE: Current universe progress archived.', 'system');
    showNotify('ECOSYSTEM SAVED');
  };

  const handleLoad = () => {
    // Re-fetch only this specific story from storage to "refresh"
    const refreshed = getStory(story.storyId);
    if (refreshed) {
      onChange(refreshed);
      addLog('STORY_STATE: Synced with latest archive.', 'system');
      showNotify('RESTORING STATE');
    }
  };

  if (isBooting) {
    return (
      <div className="h-full w-full bg-[#020408] flex flex-col items-center justify-center gap-8 font-mono relative overflow-hidden">
        <div className="scanline opacity-20"></div>
        <div className="flex flex-col items-center z-10">
          <div className="text-blue-500 text-7xl mb-6 animate-pulse drop-shadow-[0_0_20px_rgba(59,130,246,0.5)]">📡</div>
          <h1 className="text-white text-xs font-black tracking-[0.6em] uppercase mb-2">Simulating Universe</h1>
          <p className="text-blue-400 text-lg font-black uppercase tracking-tighter glow-text border-y border-blue-500/20 px-8 py-2 mb-1">{story.title}</p>
          <p className="text-gray-600 text-[8px] uppercase tracking-widest mt-2">Isolation Mode: Active (W3.IDP-CORE)</p>
        </div>
        <div className="w-72 h-1.5 bg-white/5 rounded-full overflow-hidden border border-white/10 relative">
          <div className="h-full bg-blue-600 transition-all duration-300 shadow-[0_0_15px_#2563EB]" style={{ width: `${bootProgress}%` }} />
        </div>
        <div className="text-blue-500/50 text-[9px] uppercase font-black tracking-[0.3em] animate-pulse">
          {bootProgress < 30 ? 'Indexing Registry...' : bootProgress < 70 ? `Loading [${story.characters.length}] Entities...` : 'Synchronizing Logic Pipeline...'}
        </div>
      </div>
    );
  }

  return (
    <div className="h-full w-full bg-[#020408] flex flex-col overflow-hidden relative text-white font-['Anuphan']">
      
      {/* NOTIFICATION OVERLAY */}
      {notification && (
        <div className="absolute inset-0 z-[100] flex items-center justify-center pointer-events-none">
          <div className="bg-blue-600/20 backdrop-blur-xl border-2 border-blue-500/50 px-10 py-6 rounded-[32px] animate-in zoom-in duration-300 shadow-[0_0_50px_rgba(37,99,235,0.3)]">
            <span className="text-sm font-black text-blue-400 uppercase tracking-[0.5em] glow-text text-center">{notification}</span>
          </div>
        </div>
      )}

      {/* TOP BAR */}
      <header className="h-14 shrink-0 border-b border-white/5 bg-black/60 flex items-center justify-between px-6 z-20 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 flicker shadow-[0_0_15px_#10B981]"></div>
          <div className="flex flex-col">
            <span className="text-[10px] font-black uppercase tracking-[0.3em] text-white glow-text truncate max-w-[200px]">{story.title}</span>
            <span className="text-[7px] text-gray-500 font-bold tracking-widest uppercase">Live Simulation Node</span>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="ghost" className="h-9 text-[9px] border border-white/5 hover:bg-white/10 px-4 rounded-xl" onClick={handleSave}>SAVE</Button>
          <Button variant="ghost" className="h-9 text-[9px] border border-white/5 hover:bg-white/10 px-4 rounded-xl" onClick={handleLoad}>LOAD</Button>
          <div className="w-px h-5 bg-white/10 mx-1"></div>
          <Button variant="accent" className="h-10 text-[9px] px-6 rounded-2xl shadow-lg border-2 border-white/10" onClick={() => {setCurrentNodeIdx(0); showNotify('RETURNED TO START');}}>Reset Sequence</Button>
        </div>
      </header>

      {/* MAIN PLAY AREA */}
      <main className="flex-1 flex overflow-hidden p-3 md:p-6 gap-3 md:gap-6">
        
        {/* LEFT COLUMN: MONITOR 1 & 2 */}
        <div className="flex-[7] flex flex-col gap-3 md:gap-6 overflow-hidden">
          
          {/* MONITOR 1 (Dynamic Viewport) */}
          <div className={`flex-[6.5] w3-card-inset bg-black border-2 border-blue-500/20 rounded-[40px] overflow-hidden relative flex flex-col shadow-[0_0_60px_rgba(37,99,235,0.08)] ${isGlitching ? 'glitch-active' : ''}`}>
             <div className="scanline"></div>
             <div className="absolute top-6 left-8 z-10 flex items-center gap-3">
                <span className="text-[9px] font-black text-blue-500 uppercase tracking-widest bg-blue-500/10 px-3 py-1 rounded-full border border-blue-500/20">Monitor 1: {activeView.toUpperCase()}</span>
             </div>
             
             <div className="flex-1 p-8 md:p-14 flex flex-col items-center justify-center text-center overflow-y-auto scroll-container relative z-10">
                
                {/* 1. STORY VIEW */}
                {activeView === 'story' && (
                  activeNode ? (
                    <div className="animate-in fade-in slide-in-from-bottom-8 duration-1000 max-w-3xl">
                      <h2 className="text-3xl md:text-5xl font-black mb-8 uppercase tracking-tighter leading-tight text-white glow-text">{activeNode.title}</h2>
                      <p className="text-base md:text-xl font-medium leading-relaxed text-gray-400 italic mb-12">"{activeNode.body}"</p>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {activeNode.choices?.map((choice, i) => (
                          <button key={i} className="h-14 rounded-3xl border border-white/10 bg-white/5 hover:bg-blue-600 hover:text-white transition-all text-[11px] font-black uppercase tracking-widest shadow-xl active:scale-95 group overflow-hidden relative" onClick={() => handleChoice(choice.label, choice.toNodeId)}>
                            <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                            {choice.label}
                          </button>
                        ))}
                      </div>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center gap-6 opacity-40">
                      <div className="text-6xl flicker">📖</div>
                      <div className="flex flex-col gap-2 items-center">
                        <span className="text-xs font-black uppercase tracking-widest text-blue-400">Sequence End</span>
                        <p className="text-[10px] text-gray-500">โปรดกลับไปสร้างเนื้อเรื่องในหน้า Story เพื่อจำลองต่อครับ</p>
                      </div>
                    </div>
                  )
                )}

                {/* 2. INVENTORY VIEW */}
                {activeView === 'inventory' && (
                  story.items.length > 0 ? (
                    <div className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4 w-full h-full overflow-y-auto p-4 scroll-container animate-in zoom-in duration-500">
                      {story.items.map(item => (
                        <div 
                          key={item.id} 
                          onClick={() => simulateUseItem(item)}
                          className="aspect-square w3-card-inset flex flex-col items-center justify-center p-3 border-white/5 hover:border-blue-500 hover:bg-blue-600/10 transition-all cursor-pointer bg-white/5 group active:scale-90"
                        >
                          <span className="text-3xl mb-2 group-hover:scale-110 transition-transform">🎒</span>
                          <span className="text-[8px] font-black uppercase text-center text-gray-400 group-hover:text-blue-400 truncate w-full">{item.name}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="flex flex-col items-center gap-6 opacity-40">
                      <div className="text-6xl flicker">🎒</div>
                      <div className="flex flex-col gap-2 items-center">
                        <span className="text-xs font-black uppercase tracking-widest text-blue-400">Inventory Purged</span>
                        <p className="text-[10px] text-gray-500">จักรวาลนี้ยังไม่มีการนิยามไอเทมครับ</p>
                      </div>
                    </div>
                  )
                )}

                {/* 3. CHARACTER VIEW */}
                {activeView === 'character' && (
                   activeChar ? (
                     <div className="max-w-xl w-full flex flex-col gap-8 animate-in fade-in duration-500">
                        <div className="flex items-center gap-6">
                           <div className="w-24 h-24 bg-blue-600/10 border-2 border-blue-500/20 rounded-[40px] flex items-center justify-center text-5xl relative overflow-hidden group">
                              <div className="absolute inset-0 bg-blue-600/5 flicker"></div>
                              👤
                           </div>
                           <div className="text-left">
                              <h2 className="text-4xl font-black uppercase tracking-tighter text-white glow-text">{activeChar.name}</h2>
                              <span className="text-xs text-blue-500 font-black uppercase tracking-[0.3em]">{activeChar.className}</span>
                           </div>
                        </div>
                        <div className="grid grid-cols-2 gap-6 text-left">
                           <div className="space-y-4">
                              <div className="flex justify-between items-end"><span className="text-[10px] font-black text-gray-500 uppercase tracking-widest">Integrity</span><span className="text-xl font-black text-red-500">{activeChar.vitals.hp}%</span></div>
                              <div className="h-2 bg-white/5 rounded-full overflow-hidden p-0.5 border border-white/5"><div className="h-full bg-red-600 rounded-full shadow-[0_0_15px_#EF4444]" style={{width: `${activeChar.vitals.hp}%`}} /></div>
                           </div>
                           <div className="space-y-4">
                              <div className="flex justify-between items-end"><span className="text-[10px] font-black text-gray-500 uppercase tracking-widest">Energy Core</span><span className="text-xl font-black text-emerald-500">{activeChar.vitals.en}%</span></div>
                              <div className="h-2 bg-white/5 rounded-full overflow-hidden p-0.5 border border-white/5"><div className="h-full bg-emerald-600 rounded-full shadow-[0_0_15px_#10B981]" style={{width: `${activeChar.vitals.en}%`}} /></div>
                           </div>
                        </div>
                     </div>
                   ) : (
                    <div className="flex flex-col items-center gap-6 opacity-40">
                      <div className="text-6xl flicker">👥</div>
                      <div className="flex flex-col gap-2 items-center">
                        <span className="text-xs font-black uppercase tracking-widest text-blue-400">Soul Sync Error</span>
                        <p className="text-[10px] text-gray-500">ไม่พบตัวละครในโปรเจกต์นี้ครับ</p>
                      </div>
                    </div>
                   )
                )}

                {/* 4. CARDS VIEW */}
                {activeView === 'cards' && (
                  story.cards.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full h-full overflow-y-auto p-4 scroll-container animate-in slide-in-from-right-8 duration-500">
                      {story.cards.map(card => (
                        <div 
                          key={card.id} 
                          onClick={() => simulateCardTrigger(card)}
                          className="w3-card-inset p-5 flex flex-col gap-3 border-white/5 bg-white/5 hover:bg-emerald-500/10 hover:border-emerald-500/20 transition-all cursor-pointer group active:scale-95"
                        >
                          <div className="flex justify-between items-center">
                            <span className="text-[11px] font-black uppercase text-gray-300 group-hover:text-emerald-400 transition-colors">{card.name}</span>
                            <span className="text-[9px] bg-white/10 text-white px-2 py-0.5 rounded font-black group-hover:bg-emerald-500 group-hover:text-black transition-all">{card.grade}</span>
                          </div>
                          <p className="text-[10px] text-gray-500 text-left line-clamp-3 group-hover:text-gray-300 transition-colors italic">"{card.description}"</p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="flex flex-col items-center gap-6 opacity-40">
                      <div className="text-6xl flicker">⚡</div>
                      <div className="flex flex-col gap-2 items-center">
                        <span className="text-xs font-black uppercase tracking-widest text-blue-400">Logic Modules Empty</span>
                        <p className="text-[10px] text-gray-500">ยังไม่มีการ์ดลอจิกถูกนิยามในจักรวาลนี้ครับ</p>
                      </div>
                    </div>
                  )
                )}
             </div>
          </div>

          {/* MONITOR 2 (Link Console) */}
          <div className="flex-[3.5] w3-card-inset bg-[#020408] border border-white/5 rounded-[40px] overflow-hidden flex flex-col relative shadow-inner">
             <div className="scanline opacity-30"></div>
             <div className="absolute top-5 left-8 z-10 flex items-center gap-3">
                <span className="text-[8px] font-black text-gray-500 uppercase tracking-widest">Monitor 2: Link_Console</span>
             </div>
             <div className="flex-1 p-6 pt-12 overflow-y-auto scroll-container font-mono text-[10px] md:text-[11px] relative z-10">
                {logs.map((log, i) => (
                  <div key={i} className={`mb-2 flex gap-4 animate-in fade-in slide-in-from-left-4 duration-500 ${
                    log.type === 'narrative' ? 'text-blue-400' : 
                    log.type === 'combat' ? 'text-emerald-400 font-black' : 
                    log.type === 'item' ? 'text-amber-400' : 
                    'text-gray-600'}`}>
                    <span className="opacity-30 shrink-0">[{new Date().toLocaleTimeString([], {hour12: false})}]</span>
                    <span className="flex-1 leading-relaxed">&gt; {log.msg}</span>
                  </div>
                ))}
                {logs.length === 0 && <div className="text-center py-20 opacity-10 uppercase text-[9px] font-black tracking-[0.5em] flicker">Signal Idle...</div>}
             </div>
          </div>
        </div>

        {/* RIGHT COLUMN: STATUS (3 & 4) */}
        <div className="flex-[3] flex flex-col gap-3 md:gap-6 overflow-hidden">
           <div className="flex-[5.5] w3-card bg-black/60 border border-white/5 rounded-[40px] p-6 flex flex-col gap-5 overflow-hidden relative shadow-2xl">
              <div className="absolute top-5 right-8 text-[8px] font-black text-white/10 uppercase tracking-widest">SEC_03</div>
              {activeChar ? (
                <div className="flex flex-col h-full animate-in slide-in-from-right-8 duration-700">
                  <div className="flex items-center gap-5 mb-8">
                    <div className="w-16 h-16 md:w-20 md:h-20 rounded-[32px] bg-blue-600/10 border border-blue-500/20 flex items-center justify-center text-3xl shadow-lg relative overflow-hidden group">
                       <div className="absolute inset-0 bg-blue-500/5 flicker"></div>
                       👤
                    </div>
                    <div>
                      <h3 className="text-xl font-black uppercase tracking-tighter leading-none glow-text">{activeChar.name}</h3>
                      <span className="text-[10px] text-blue-500 font-black tracking-widest uppercase mt-2 block opacity-80">{activeChar.className}</span>
                    </div>
                  </div>
                  <div className="space-y-6">
                    <div className="space-y-2">
                       <div className="flex justify-between text-[9px] font-black uppercase tracking-widest text-red-500/80"><span>Integrity</span><span>{activeChar.vitals.hp}%</span></div>
                       <div className="h-2 bg-white/5 rounded-full overflow-hidden p-0.5"><div className="h-full bg-red-600 rounded-full shadow-[0_0_10px_#EF4444]" style={{width: `${activeChar.vitals.hp}%`}} /></div>
                    </div>
                    <div className="space-y-2">
                       <div className="flex justify-between text-[9px] font-black uppercase tracking-widest text-emerald-500/80"><span>Energy</span><span>{activeChar.vitals.en}%</span></div>
                       <div className="h-2 bg-white/5 rounded-full overflow-hidden p-0.5"><div className="h-full bg-emerald-600 rounded-full shadow-[0_0_15px_#10B981]" style={{width: `${activeChar.vitals.en}%`}} /></div>
                    </div>
                    <div className="mt-10 pt-8 border-t border-white/5">
                       <span className="text-[8px] font-black text-gray-500 uppercase tracking-[0.4em] block mb-4 text-center">Logic Buffer Output</span>
                       <div className="w3-card-inset h-16 bg-blue-600/5 border border-blue-600/10 rounded-[20px] flex items-center justify-center px-4 shadow-inner">
                          <span className="text-[10px] font-black text-blue-400 uppercase tracking-[0.2em] flicker">{activeChar.logicSlots?.totalResult || 'LINK_READY'}</span>
                       </div>
                    </div>
                  </div>
                </div>
              ) : <div className="h-full flex items-center justify-center opacity-10 uppercase text-[9px] font-black tracking-widest flicker">Soul Offline</div>}
           </div>

           <div className="flex-[4.5] w3-card-inset bg-white/5 border border-white/5 rounded-[40px] p-6 flex flex-col gap-4 relative overflow-hidden shadow-inner">
              <div className="absolute top-5 right-8 text-[8px] font-black text-white/10 uppercase tracking-widest">SEC_04</div>
              <div className="flex items-center gap-4 mb-2">
                 <div className="w-10 h-10 rounded-2xl bg-amber-500/10 flex items-center justify-center text-xl shadow-inner border border-amber-500/10 flicker">🏰</div>
                 <h4 className="text-[11px] font-black uppercase text-amber-500 tracking-widest">Environmental Status</h4>
              </div>
              <div className="flex-1 overflow-y-auto scroll-container flex flex-col gap-4">
                 <div className="p-4 bg-black/40 rounded-[24px] border border-white/5 shadow-inner">
                    <p className="text-[10px] text-gray-400 leading-relaxed italic font-medium">
                      "Analyzing isolated context for universe [${story.title}]... Ambient mana and logic density are within local safe parameters."
                    </p>
                 </div>
              </div>
           </div>
        </div>
      </main>

      {/* BOTTOM NAV */}
      <footer className="h-20 shrink-0 bg-black/80 border-t border-white/5 px-8 flex items-center justify-center gap-4 md:gap-16 z-20 backdrop-blur-xl relative">
        <div className="absolute top-0 inset-x-0 h-[1px] bg-gradient-to-r from-transparent via-blue-500/20 to-transparent"></div>
        {[
          {id: 'story', label: 'Story', icon: '📝'},
          {id: 'inventory', label: 'Inventory', icon: '🎒'},
          {id: 'character', label: 'Status', icon: '👥'},
          {id: 'cards', label: 'Cards', icon: '⚡'}
        ].map(tab => (
          <button 
            key={tab.id}
            onClick={() => triggerGlitch(tab.id as PlayView)}
            className={`flex flex-col items-center gap-2 transition-all px-6 py-2 rounded-[24px] relative group ${activeView === tab.id ? 'text-blue-400 scale-110' : 'text-gray-500 hover:text-white opacity-40 hover:opacity-100'}`}
          >
            {activeView === tab.id && (
              <div className="absolute inset-0 bg-blue-600/10 rounded-[24px] border border-blue-500/20 shadow-[0_0_20px_rgba(37,99,235,0.1)] animate-in zoom-in duration-300"></div>
            )}
            <span className="text-2xl relative z-10 group-active:scale-90 transition-transform">{tab.icon}</span>
            <span className="text-[9px] font-black uppercase tracking-widest relative z-10">{tab.label}</span>
          </button>
        ))}
      </footer>

      {/* OVERLAYS */}
      <div className="absolute inset-0 pointer-events-none opacity-[0.05] bg-[url('https://grainy-gradients.vercel.app/noise.svg')] mix-blend-overlay"></div>
    </div>
  );
};
