import React, { useEffect, useState } from 'react';
import { BattlePanel } from './BattlePanel';
import type { BattleProgress } from '../../core/battle';
import type { StoryPack, RunSection, EventPack, RuleBlock } from '../../types';
import { clearRunState, loadRunState, saveRunState } from '../../core/runState';
import { defaultRunPresentation, newRunSection, RUN_SOURCES } from '../../core/runPresentation';
import { getWorldCell } from '../../core/worldIndex';
import { generateId } from '../../core/utils';
import { runInteraction, type Vitals } from '../../core/eventRuntime';
import { rollDice } from '../../core/dice';
import { runModuleFlow, type FlowReport } from '../../core/moduleFlow';
import { evaluateRuleset, type RuleReport } from '../../core/ruleRuntime';
import { buildPlayRuleContext } from '../../core/playRuleContext';
import { changeInventory, type Inventory } from '../../core/inventory';

interface Props { story: StoryPack; onChange: (updated: StoryPack) => void; }
const box = 'rounded-xl border border-[var(--border)] bg-[var(--surface)]';
const itemStyle = 'block w-full p-3 text-left rounded-lg border border-white/10 hover:border-emerald-400/60';
const ruleText = (blocks: RuleBlock[], prefix = ''): string => blocks.map((block, index) => {
  const number = `${prefix}${index + 1}`;
  return `${number}. ${block.title}\n${block.content}${block.children?.length ? `\n${ruleText(block.children, `${number}.`)}` : ''}`;
}).join('\n\n');

export const PlaytestTab: React.FC<Props> = ({ story, onChange }) => {
  const presentation = story.runPresentation || defaultRunPresentation(story.projectKind);
  // Older projects keep their customized sections and receive the new views once.
  const sections = [...(presentation.sections || []), ...(presentation.sectionsMigrated ? [] : (['battle', 'special'] as const))
    .filter(source => !(presentation.sections || []).some(entry => entry.source === source))
    .map(source => newRunSection(source, `built-in-${source}`))];
  const visible = sections.filter(section => section.visible);
  const [sectionId, setSectionId] = useState<string | null>(null);
  const [configOpen, setConfigOpen] = useState(false);
  const [nodeId, setNodeId] = useState<string | null>(story.storyNodes[0]?.nodeId || null);
  const [characterId, setCharacterId] = useState<string | null>(story.characters[0]?.id || null);
  const [boardId, setBoardId] = useState<string | null>(story.boards[0]?.boardId || null);
  const [cellKey, setCellKey] = useState<string | null>(null);
  const [recordId, setRecordId] = useState<string | null>(null);
  const [contextRecordId, setContextRecordId] = useState<string | null>(null);
  const [notice, setNotice] = useState('');
  const [vitals, setVitals] = useState<Record<string, Vitals>>({});
  const [eventLog, setEventLog] = useState<string[]>([]);
  const [positions, setPositions] = useState<Record<string, { boardId: string; x: number; y: number }>>({});
  const [diceLog, setDiceLog] = useState<string[]>([]);
  const [diceOpen, setDiceOpen] = useState(false);
  const [inventory, setInventory] = useState<Inventory>({});
  const [battleTurn, setBattleTurn] = useState(1);
  const [battleLog, setBattleLog] = useState<string[]>([]);
  const [battleProgress, setBattleProgress] = useState<BattleProgress | null>(null);
  const [specialId, setSpecialId] = useState<string | null>(null);
  const [diceCount, setDiceCount] = useState(1);
  const [diceSides, setDiceSides] = useState(6);
  const [flowReport, setFlowReport] = useState<{ cardId: string; report: FlowReport } | null>(null);
  const [ruleReport, setRuleReport] = useState<{ ruleId: string; report: RuleReport; context: Record<string, unknown> } | null>(null);

  useEffect(() => {
    setSectionId(null); setNodeId(story.storyNodes[0]?.nodeId || null);
    setCharacterId(story.characters[0]?.id || null); setBoardId(story.boards[0]?.boardId || null);
    setCellKey(null); setRecordId(null); setContextRecordId(null); setVitals({}); setEventLog([]); setPositions({}); setDiceLog([]); setInventory({}); setFlowReport(null); setRuleReport(null); setBattleTurn(1); setBattleLog([]); setBattleProgress(null); setSpecialId(null);
  }, [story.storyId]);

  const section = visible.find(entry => entry.id === sectionId) || visible[0];
  const node = story.storyNodes.find(entry => entry.nodeId === nodeId) || story.storyNodes[0];
  const board = story.boards.find(entry => entry.boardId === boardId) || story.boards[0];
  const activePosition = characterId ? positions[characterId] : undefined;
  const activeName = story.characters.find(character => character.id === characterId)?.name || story.characters[0]?.name;
  const updateSections = (entries: RunSection[]) => onChange({ ...story, runPresentation: { ...presentation, sections: entries, sectionsMigrated: true } });
  const editSection = (id: string, change: Partial<RunSection>) => updateSections(sections.map(entry => entry.id === id ? { ...entry, ...change } : entry));
  const move = (index: number, step: number) => {
    const next = [...sections], target = index + step;
    if (target < 0 || target >= next.length) return;
    [next[index], next[target]] = [next[target], next[index]];
    updateSections(next);
  };
  const save = () => setNotice(saveRunState({ version: 1, storyId: story.storyId, currentNodeId: node?.nodeId || null,
    activeCharacterId: characterId, characterVitals: vitals, positions, diceLog, eventLog, inventory, battleTurn, battleLog, battle: battleProgress || undefined, savedAt: Date.now() }) ? 'บันทึกความคืบหน้าแล้ว' : 'บันทึกไม่สำเร็จ');
  const load = () => {
    const saved = loadRunState(story.storyId);
    if (!saved) return setNotice('ยังไม่มีความคืบหน้าที่บันทึกไว้');
    setNodeId(story.storyNodes.some(entry => entry.nodeId === saved.currentNodeId) ? saved.currentNodeId : story.storyNodes[0]?.nodeId || null);
    setCharacterId(story.characters.some(entry => entry.id === saved.activeCharacterId) ? saved.activeCharacterId : story.characters[0]?.id || null);
    setVitals(Object.fromEntries(Object.entries(saved.characterVitals || {}).filter(([id, value]) =>
      story.characters.some(character => character.id === id) && value &&
      ['hp','mp','en'].every(key => Number.isFinite(value[key as keyof Vitals])))));
    setPositions(Object.fromEntries(Object.entries(saved.positions || {}).filter(([id, position]) =>
      story.characters.some(character => character.id === id) && position &&
      story.boards.some(entry => entry.boardId === position.boardId && Number.isInteger(position.x) && Number.isInteger(position.y) &&
        position.x >= 0 && position.y >= 0 && position.x < entry.width && position.y < entry.height))));
    setDiceLog((saved.diceLog || []).slice(0, 20));
    setEventLog((saved.eventLog || []).slice(0, 20));
    setBattleTurn(saved.battleTurn || 1);
    setBattleLog((saved.battleLog || []).slice(0, 20));
    setBattleProgress(saved.battle && story.battleConfig && story.characters.some(c => c.id === saved.battle!.activeId) && story.characters.some(c => c.id === saved.battle!.opponentId) && saved.battle.phaseIndex < story.battleConfig.phases.length ? saved.battle : null);
    setInventory(Object.fromEntries(Object.entries(saved.inventory || {}).filter(([owner]) => owner === '@project' || story.characters.some(character => character.id === owner)).map(([owner, owned]) =>
      [owner, Object.fromEntries(Object.entries(owned).filter(([id]) => story.items.some(item => item.id === id)))])));
    setNotice('โหลดความคืบหน้าแล้ว');
  };
  const reset = () => {
    if (!clearRunState(story.storyId)) return setNotice('ลบความคืบหน้าไม่สำเร็จ');
    setNodeId(story.storyNodes[0]?.nodeId || null);
    setCharacterId(story.characters[0]?.id || null); setVitals({}); setEventLog([]); setPositions({}); setDiceLog([]); setInventory({}); setBattleTurn(1); setBattleLog([]); setBattleProgress(null); setNotice('เริ่มจากต้นแล้ว');
  };
  const adjustItem = (itemId: string, delta: number) => {
    const owner = characterId && story.characters.some(character => character.id === characterId) ? characterId : '@project';
    const result = changeInventory(inventory, story.items, owner, itemId, delta);
    if (!result.ok) return setNotice(result.error || 'ปรับจำนวนไม่สำเร็จ');
    setInventory(result.inventory);
    setNotice(`ปรับจำนวนไอเทมแล้ว: ${result.quantity} · กดบันทึกจุดอ่านเพื่อเก็บผล`);
  };
  const execute = (event: EventPack) => {
    const character = story.characters.find(entry => entry.id === characterId) || story.characters[0];
    if (!character) return setNotice('ต้องมีตัวละครก่อนใช้อีเวนต์');
    const result = runInteraction(event, vitals[character.id] || character.vitals);
    if (!result.ok) return setNotice(`${event.name}: ${result.error}`);
    setVitals(previous => ({...previous, [character.id]: result.vitals}));
    setEventLog(previous => [...result.log.map(line => `${event.name}: ${line}`), ...previous].slice(0, 20));
    setNotice(`${event.name}: ทำงานแล้ว — กดบันทึกจุดอ่านเพื่อเก็บผล`);
  };
  const roll = () => {
    try {
      const values = rollDice(diceCount, diceSides);
      const line = `${new Date().toLocaleTimeString('th-TH')} · ${diceCount}d${diceSides}: ${values.join(' + ')} = ${values.reduce((sum, value) => sum + value, 0)}`;
      setDiceLog(previous => [line, ...previous].slice(0, 20));
      setNotice('ทอยลูกเต๋าแล้ว — กดบันทึกจุดอ่านเพื่อเก็บประวัติ');
    } catch {
      setNotice('ไม่สามารถสุ่มลูกเต๋าบนอุปกรณ์นี้');
    }
  };
  const empty = <p className="text-slate-400 text-sm p-8">ยังไม่มีข้อมูลในส่วนนี้ เพิ่มได้จากหน้าแก้ไขโครงการ</p>;
  const renderContent = () => {
    if (!section) return empty;
    if (section.source === 'battle') return <BattlePanel story={story} onChange={onChange} progress={battleProgress} onProgress={setBattleProgress} vitals={vitals} onVitals={setVitals} />;
    if (section.source === 'special') {
      const entries = [...story.storyNodes.filter(entry => entry.type === 'EventHook').map(entry => ({ id: `node:${entry.nodeId}`, name: entry.title || 'ฉากพิเศษ', kind: 'ฉาก', body: entry.body || '', image: entry.imageAssetId, event: undefined as EventPack | undefined })),
        ...story.events.filter(entry => ['Special', 'System'].includes(entry.eventType)).map(entry => ({ id: `event:${entry.id}`, name: entry.name, kind: 'อีเวนต์', body: [entry.areaRule, ...entry.actions.filter(action => action.actionType.toLowerCase() === 'message').map(action => action.payload)].filter(Boolean).join('\n\n'), image: entry.iconAssetId, event: entry }))];
      const selected = entries.find(entry => entry.id === specialId) || entries[0];
      return entries.length ? <div className="h-full min-h-0 grid md:grid-cols-[200px_1fr] gap-3"><nav className={`${box} p-2 overflow-y-auto space-y-2`}>{entries.map(entry => <button key={entry.id} className={`${itemStyle} ${selected.id === entry.id ? 'border-emerald-400' : ''}`} onClick={() => setSpecialId(entry.id)}><small className="text-emerald-300">{entry.kind}</small><span className="block">{entry.name}</span></button>)}</nav><article className={`${box} p-5 overflow-y-auto`}>
        {selected.image && story.assets[selected.image] && <img src={story.assets[selected.image].dataUrl} alt="" className="max-h-52 w-full object-contain rounded-lg mb-4" />}<small className="text-emerald-300">{selected.kind}</small><h3 className="text-2xl font-bold mb-4">{selected.name}</h3><p className="whitespace-pre-wrap leading-7">{selected.body || 'ยังไม่มีเนื้อหา'}</p>
        {selected.event && <div className="border-t border-white/10 mt-6 pt-4"><p className="text-xs text-slate-300 mb-3">ผลอีเวนต์ใช้ตัวละครที่เลือกใน Playtest · รองรับ OnInteract, Message/Self และผล HP/MP/EN ตามเงื่อนไขเท่านั้น</p><button onClick={() => execute(selected.event!)} className="p-2 rounded border border-emerald-400/50">โต้ตอบกับอีเวนต์</button></div>}
      </article></div> : <p className="text-slate-400 p-8">ยังไม่มีฉาก EventHook หรืออีเวนต์ชนิด Special / Story เพิ่มได้จากหน้า Story และ Events</p>;
    }
    if (section.source === 'story') return story.storyNodes.length ? <div className="grid md:grid-cols-[200px_1fr] gap-3 h-full min-h-0">
      <div className={`${box} overflow-y-auto p-2 space-y-2`}>{story.storyNodes.map(entry =>
        <button key={entry.nodeId} className={`${itemStyle} ${node?.nodeId === entry.nodeId ? 'border-emerald-400' : ''}`} onClick={() => setNodeId(entry.nodeId)}>{entry.title || 'ไม่มีชื่อหัวข้อ'}</button>)}</div>
      <article className={`${box} overflow-y-auto p-5`}><h2 className="text-2xl font-bold mb-4">{node?.title}</h2><p className="whitespace-pre-wrap leading-7">{node?.body}</p>
        <div className="grid gap-2 mt-6">{node?.choices?.map((choice, index) => <button key={index} className={itemStyle} onClick={() => {
          if (story.storyNodes.some(entry => entry.nodeId === choice.toNodeId)) setNodeId(choice.toNodeId);
          else setNotice('ปลายทางของตัวเลือกยังไม่มี');
        }}>{choice.label} →</button>)}</div></article>
    </div> : empty;

    if (section.source === 'board') return board ? <div className="grid lg:grid-cols-[minmax(0,1fr)_250px] gap-3 h-full min-h-0">
      <div className={`${box} p-3 flex flex-col min-h-0`}><select aria-label="เลือกบอร์ด" value={board.boardId} onChange={e => { setBoardId(e.target.value); setCellKey(null); }} className="bg-[#0b1512] border border-white/20 p-2 mb-3 rounded max-w-full self-start">
        {story.boards.map(entry => <option key={entry.boardId} value={entry.boardId}>{entry.title}</option>)}</select>
        <div className="flex-1 min-h-0 overflow-auto bg-[#0b1415] p-3 rounded-lg touch-pan-x touch-pan-y"><div className="grid w-max" style={{ gridTemplateColumns: `repeat(${board.width}, 48px)` }}>
          {Array.from({ length: board.width * board.height }, (_, index) => {
            const x = index % board.width, y = Math.floor(index / board.width), key = `${x}_${y}`, cell = board.cellMap[key];
            const occupants = story.characters.filter(character => positions[character.id]?.boardId === board.boardId && positions[character.id]?.x === x && positions[character.id]?.y === y);
            return <button key={key} aria-label={`พิกัด ${x}, ${y}${occupants.length ? ` มีตัวละคร ${occupants.map(c => c.name).join(', ')}` : ''}`} title={cell?.name || key} onClick={() => setCellKey(key)}
              className={`w-12 h-12 border border-white/10 text-lg relative ${cellKey === key ? 'outline outline-2 outline-sky-400 z-10' : ''}`}
              style={{ backgroundColor: cell?.markerColor || '#16252b' }}>{cell?.markerIcon || (cell?.type === 'Location' ? '⌖' : cell?.type === 'Encounter' ? '⚡' : '')}{occupants.length > 0 && <span className="absolute right-0 bottom-0 w-3 h-3 rounded-full bg-emerald-400 animate-pulse ring-2 ring-black" />}</button>;
          })}</div></div></div>
      <aside className={`${box} p-4 overflow-y-auto text-sm`}>
        {cellKey ? (() => { const [x, y] = cellKey.split('_').map(Number), view = getWorldCell(story, board.boardId, x, y);
          return view ? <div className="space-y-3"><h2 className="font-bold text-lg">{view.cell.name || `พิกัด ${x}, ${y}`}</h2><p className="whitespace-pre-wrap">{view.cell.desc || 'ยังไม่มีรายละเอียด'}</p>
            <div className="border-t border-white/10 pt-3"><b>ตำแหน่งตัวละคร</b><p className="text-xs text-slate-300">{story.characters.filter(character => positions[character.id]?.boardId === board.boardId && positions[character.id]?.x === x && positions[character.id]?.y === y).map(character => character.name).join(', ') || 'ไม่มีตัวละครในช่องนี้'}</p>
              {story.characters.length > 0 && <><select aria-label="เลือกตัวละครที่จะวาง" value={characterId || story.characters[0].id} onChange={e => setCharacterId(e.target.value)} className="mt-2 w-full p-2 bg-[#0b1512] rounded border border-white/20">{story.characters.map(character => <option key={character.id} value={character.id}>{character.name}</option>)}</select>
                <button className="mt-2 border border-emerald-400/40 rounded px-2 py-2" onClick={() => { const id = characterId || story.characters[0].id; setPositions(previous => ({ ...previous, [id]: { boardId: board.boardId, x, y } })); setNotice('วางตัวละครแล้ว — กดบันทึกจุดอ่านเพื่อเก็บตำแหน่ง'); }}>วาง/ย้ายตัวละครมาที่นี่</button>
                {positions[characterId || story.characters[0].id]?.boardId === board.boardId && positions[characterId || story.characters[0].id]?.x === x && positions[characterId || story.characters[0].id]?.y === y && <button className="ml-2 text-xs underline" onClick={() => { const id = characterId || story.characters[0].id; setPositions(previous => { const next = { ...previous }; delete next[id]; return next; }); }}>นำออกจากบอร์ด</button>}</>}</div>
            {view.location && <div className="border-t border-white/10 pt-3"><b>{view.location.title}</b><p>{view.location.description}</p></div>}
            {view.events.length > 0 && <div className="border-t border-white/10 pt-3"><b>อีเวนต์ที่อ้างถึง</b>{view.events.map(event => <div key={event.id} className="mt-2 flex gap-2 items-center"><span>{event.name}</span><button className="border border-emerald-400/40 rounded px-2 py-1" onClick={() => execute(event)}>โต้ตอบ</button></div>)}</div>}
            {(view.missingLocationRef || view.missingEventRefs.length > 0) && <p className="text-amber-300">มีลิงก์ที่หาปลายทางไม่พบ</p>}</div> : empty; })() : <p>แตะช่องเพื่อดูรายละเอียด</p>}
      </aside></div> : empty;

    const records: { id: string; title: string; detail: string }[] = section.source === 'cards'
      ? story.cards.map(card => ({ id: card.id, title: card.name, detail: `${card.description}\n\nโมดูลที่ประกอบ: ${card.moduleSlots?.length ? card.moduleSlots.map((id, index) => `${index + 1}. ${id ? (story.modules || []).find(module => module.id === id)?.name || 'ไม่พบโมดูล' : 'ว่าง'}`).join(' · ') : 'ยังไม่ประกอบ'}\n\nข้อความ A/B/C เดิม: ${card.inputCondition} / ${card.logicCode} / ${card.effectResult}` }))
      : section.source === 'characters' ? story.characters.map(character => ({ id: character.id, title: character.name, detail: `${character.className}\nHP ${vitals[character.id]?.hp ?? character.vitals.hp} · MP ${vitals[character.id]?.mp ?? character.vitals.mp} · EN ${vitals[character.id]?.en ?? character.vitals.en}\n\n${character.backgroundText}` }))
      : section.source === 'items' ? story.items.map(item => ({ id: item.id, title: item.name, detail: item.description }))
      : section.source === 'locations' ? story.locations.map(location => ({ id: location.locationId, title: location.title, detail: location.description || '' }))
      : section.source === 'rules' ? story.rulesets.map(rule => ({ id: rule.id, title: rule.name, detail: ruleText(rule.blocks) }))
      : story.events.map(event => ({ id: event.id, title: event.name, detail: `${event.areaRule}\n\n${event.actions.map(action => `${action.actionType}: ${action.payload}`).join('\n')}` }));
    if (!records.length) return empty;
    const selected = records.find(record => record.id === recordId) || records[0];
    return <div className="grid md:grid-cols-[200px_1fr] gap-3 h-full min-h-0"><div className={`${box} overflow-y-auto p-2 space-y-2`}>
      {records.map(record => <button key={record.id} className={`${itemStyle} ${selected.id === record.id ? 'border-emerald-400' : ''}`} onClick={() => { setRecordId(record.id); setFlowReport(null); setRuleReport(null); if (section.source === 'characters') setCharacterId(record.id); if (['items','cards','events','locations'].includes(section.source)) setContextRecordId(record.id); }}>{record.title || 'ไม่มีชื่อ'}</button>)}
      </div><article className={`${box} overflow-y-auto p-5`}><h2 className="text-2xl font-bold mb-4">{selected.title}</h2><p className="whitespace-pre-wrap leading-7">{selected.detail || 'ยังไม่มีรายละเอียด'}</p>
      {section.source === 'cards' && <div className="mt-6 border-t border-white/10 pt-4"><button className="border border-emerald-400/50 rounded px-3 py-2 text-sm" onClick={() => { const card = story.cards.find(entry => entry.id === selected.id); if (card) setFlowReport({ cardId: card.id, report: runModuleFlow(card, story.modules || []) }); }}>ลองเดินโฟลว A → B → C</button>
        {flowReport?.cardId === selected.id && <div role="status" className="mt-3 text-sm space-y-1"><b className={flowReport.report.status === 'DISPLAY' ? 'text-emerald-300' : 'text-amber-300'}>{flowReport.report.status}</b>
          {flowReport.report.trace.map((line, index) => <p key={index} className="whitespace-pre-wrap">{line}</p>)}
          {flowReport.report.reason && <p>{flowReport.report.reason}</p>}
          {flowReport.report.output && <p className="font-bold">ผลแสดง: {flowReport.report.output}</p>}</div>}
      </div>}
      {section.source === 'items' && <div className="mt-6 border-t border-white/10 pt-4 text-sm space-y-2"><p>ช่องเก็บของ: {activeName || 'โครงการ'} · จำนวน {inventory[characterId || '@project']?.[selected.id] || 0}</p>
        <div className="flex gap-2"><button className="border border-emerald-400/50 rounded px-3 py-2" onClick={() => adjustItem(selected.id, 1)}>หยิบ +1</button>
          <button className="border border-amber-400/50 rounded px-3 py-2" onClick={() => adjustItem(selected.id, -1)}>นำออก −1</button></div>
        <p className="text-slate-400">ใช้เฉพาะไอเทมที่ลงทะเบียนแล้ว การใช้เอฟเฟกต์ของไอเทมยังไม่รองรับ</p></div>}
      {section.source === 'rules' && <div className="mt-6 border-t border-white/10 pt-4 text-sm space-y-2"><p className="text-slate-300">ตรวจข้อมูลที่เลือกใน Playtest ณ เวลาที่กด รวมถึงบอร์ด ช่อง ตัวละคร สถานะล่าสุด และรายการไอเทม/การ์ด/อีเวนต์/สถานที่ที่แตะล่าสุด หากมีอยู่</p>
        <button className="border border-emerald-400/50 rounded px-3 py-2" onClick={() => { const rule = story.rulesets.find(entry => entry.id === selected.id); if (!rule) return;
          const context = buildPlayRuleContext(story, { boardId, cellKey, characterId, nodeId, recordId: contextRecordId, vitals });
          setRuleReport({ ruleId: rule.id, report: evaluateRuleset(rule, context, story.commonPlay || []), context });
        }}>ตรวจ Rules กับบริบทปัจจุบัน</button>
        {ruleReport?.ruleId === selected.id && <div role="status" className="rounded-lg border border-white/10 p-3 space-y-2"><b>ผลตรวจ: {ruleReport.report.status}</b>
          <details><summary>ข้อมูลที่ส่งเข้ากฎ</summary><pre className="whitespace-pre-wrap break-all text-xs">{JSON.stringify(ruleReport.context, null, 2)}</pre></details>
          {ruleReport.report.trace.map(entry => <p key={entry.path}>{entry.path} {entry.title}: {entry.status} — {entry.message}{entry.commandRef ? ` · อ้างอิง ${entry.commandRef} (ยังไม่รัน)` : ''}</p>)}
        </div>}</div>}
      {section.source === 'events' && <div className="mt-8"><p className="text-amber-200 text-xs mb-2">การกดโต้ตอบรองรับเฉพาะคำสั่งที่ระบุไว้ในหน้า Events</p><button className="border border-emerald-400/40 rounded px-3 py-2" onClick={() => { const event = story.events.find(entry => entry.id === selected.id); if (event) execute(event); }}>โต้ตอบกับอีเวนต์</button></div>}</article></div>;
  };

  return <div className="h-full min-h-0 flex flex-col text-slate-100 relative" style={{ backgroundColor: presentation.backgroundColor || '#111a18',
    backgroundImage: presentation.backgroundAssetId && story.assets[presentation.backgroundAssetId] ? `linear-gradient(#07120ccc,#07120cdd),url(${story.assets[presentation.backgroundAssetId].dataUrl})` : undefined,
    backgroundSize: 'cover', backgroundPosition: 'center' }}>
    <header className="p-3 flex flex-wrap justify-between items-center gap-2 border-b border-white/10 bg-[#0b1613]/90"><div><h1 className="font-bold text-lg">{story.title}</h1><p className="text-xs text-emerald-200/70">{story.projectKind || 'โครงการเดิม'} · โหมดใช้งาน</p>{activePosition && <p className="text-xs text-emerald-300">● {activeName}: {story.boards.find(entry => entry.boardId === activePosition.boardId)?.title || 'บอร์ด'} ({activePosition.x}, {activePosition.y})</p>}</div>
      <div className="flex flex-wrap gap-2 text-xs"><button className={`${box} px-3 py-2`} onClick={() => setDiceOpen(value => !value)}>🎲 ลูกเต๋า</button><button className={`${box} px-3 py-2`} onClick={save}>บันทึกจุดอ่าน</button><button className={`${box} px-3 py-2`} onClick={load}>เปิดจุดอ่าน</button><button className={`${box} px-3 py-2`} onClick={reset}>เริ่มใหม่</button><button className="border border-emerald-400/40 rounded-xl px-3 py-2" onClick={() => setConfigOpen(true)}>ตั้งค่าหน้าใช้งาน</button></div></header>
    {diceOpen && <section aria-label="เครื่องมือลูกเต๋า" className="p-3 border-b border-white/10 bg-[#10221b] text-xs flex flex-wrap items-center gap-3">
      <label>จำนวน <input type="number" min="1" max="10" value={diceCount} onChange={e => setDiceCount(Number(e.target.value))} className="ml-2 w-14 p-2 rounded bg-black/30" /></label>
      <label>ชนิด <select value={diceSides} onChange={e => setDiceSides(Number(e.target.value))} className="ml-2 p-2 rounded bg-black/30">{[4,6,8,10,12,20,100].map(sides => <option key={sides} value={sides}>d{sides}</option>)}</select></label>
      <button className="p-2 rounded border border-emerald-400/50" onClick={roll}>ทอย</button>
      <div className="max-h-20 overflow-y-auto min-w-[180px] flex-1" aria-live="polite">{diceLog.length ? diceLog.slice(0,3).map((line, index) => <p key={index}>{line}</p>) : 'ยังไม่มีผลทอย'}</div>
    </section>}
    <div className="flex-1 min-h-0 min-w-0 flex flex-col md:flex-row"><nav aria-label="รายการใช้งาน" className="w-full min-w-0 max-w-full md:w-44 shrink-0 flex md:flex-col overflow-x-auto md:overflow-y-auto gap-1 p-2 border-b md:border-b-0 md:border-r border-white/10 bg-[#0b1513]/90" style={{ WebkitOverflowScrolling: 'touch' }}>
      {visible.map(entry => <button key={entry.id} onClick={() => { setSectionId(entry.id); setRecordId(null); }} className={`shrink-0 flex items-center gap-2 text-left rounded-xl p-3 text-sm ${section?.id === entry.id ? 'bg-[var(--accent)]/25 border border-[var(--accent)]/40' : 'hover:bg-white/5'}`}><span className="text-xl w-6 text-center">{entry.icon}</span>{entry.label}</button>)}
    </nav><main className="flex-1 min-h-0 min-w-0 flex flex-col p-3 gap-3"><h2 className="text-sm font-bold text-emerald-200">{section?.label || 'รายการใช้งาน'}</h2><div className="flex-1 min-h-0">{renderContent()}</div>{notice && <p role="status" className="text-xs text-emerald-200">{notice}</p>}{eventLog.length > 0 && <div className="max-h-20 overflow-y-auto text-xs text-slate-300 border-t border-white/10 pt-1" aria-label="ผลอีเวนต์">{eventLog.slice(0,3).map((line,index) => <p key={index}>{line}</p>)}</div>}</main></div>
    {configOpen && <div className="absolute inset-0 z-30 bg-black/75 p-3 flex items-center justify-center"><section className={`${box} w-full max-w-xl max-h-[85vh] overflow-y-auto p-5 shadow-2xl`} aria-label="ตั้งค่าหน้าใช้งาน">
      <div className="flex justify-between"><h2 className="font-bold text-lg">รายการของโครงการนี้</h2><button onClick={() => setConfigOpen(false)}>ปิด ✕</button></div><p className="text-xs text-slate-300 my-3">ชื่อ ไอคอน ลำดับ และภาพของโครงการนี้</p>
      <div className="space-y-2">{sections.map((entry, index) => <div key={entry.id} className="grid grid-cols-[40px_1fr_auto] gap-2 items-center border border-white/10 rounded-xl p-2">
        <input aria-label="ไอคอน" value={entry.icon} maxLength={3} onChange={e => editSection(entry.id, { icon: e.target.value })} className="w-full p-2 bg-black/30 rounded" />
        <div><input aria-label="ชื่อรายการ" value={entry.label} onChange={e => editSection(entry.id, { label: e.target.value })} className="w-full p-2 bg-black/30 rounded" /><small className="text-slate-400">ข้อมูลจาก {RUN_SOURCES.find(option => option.source === entry.source)?.label}</small></div>
        <div className="flex flex-col text-xs gap-1"><button aria-label="เลื่อนขึ้น" onClick={() => move(index, -1)}>↑</button><button aria-label="เลื่อนลง" onClick={() => move(index, 1)}>↓</button><label><input type="checkbox" checked={entry.visible} onChange={e => editSection(entry.id, { visible: e.target.checked })} /> แสดง</label><button aria-label={`ลบรายการ ${entry.label}`} className="text-rose-300 p-1" onClick={() => { if (window.confirm(`ลบรายการ ${entry.label} จากหน้าใช้งาน? ข้อมูลต้นฉบับของโครงการจะยังอยู่`)) updateSections(sections.filter(item => item.id !== entry.id)); }}>ลบ</button></div>
      </div>)}</div><div className="mt-4 flex flex-wrap gap-2">{RUN_SOURCES.map(option => <button key={option.source} className="px-2 py-1 border border-white/15 rounded text-xs" onClick={() => updateSections([...sections, newRunSection(option.source, generateId('section'))])}>+ {option.label}</button>)}</div>
      <div className="mt-5 pt-4 border-t border-white/10 flex flex-wrap items-center gap-4"><label className="text-xs">สีพื้นหลัง <input type="color" value={presentation.backgroundColor || '#111a18'} onChange={e => onChange({ ...story, runPresentation: { ...presentation, backgroundColor: e.target.value } })} /></label>
        <label className="text-xs">ภาพพื้นหลัง <input type="file" accept="image/*" className="block text-xs max-w-[200px]" onChange={e => { const file = e.target.files?.[0]; if (!file) return; if (file.size > 500_000) return setNotice('ภาพต้องไม่เกิน 500 KB'); const reader = new FileReader(); reader.onload = () => { if (typeof reader.result !== 'string') return; const id = generateId('bg'); onChange({ ...story, assets: { ...story.assets, [id]: { id, name: file.name, dataUrl: reader.result } }, runPresentation: { ...presentation, backgroundAssetId: id } }); }; reader.readAsDataURL(file); }} /></label>
        {presentation.backgroundAssetId && <button className="text-xs underline" onClick={() => onChange({ ...story, runPresentation: { ...presentation, backgroundAssetId: undefined } })}>เอาภาพออก</button>}</div>
    </section></div>}
  </div>;
};
