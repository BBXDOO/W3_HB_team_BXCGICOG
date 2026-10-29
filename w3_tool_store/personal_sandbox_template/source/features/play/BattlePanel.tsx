import React, { useRef, useState } from 'react';
import type { BattleAction, BattleConfig, BattleEffect, StoryPack } from '../../types';
import { advanceBattle, beginTurn, newBattle, performBattleAction, type BattleProgress } from '../../core/battle';
import { generateId } from '../../core/utils';
import type { Vitals } from '../../core/eventRuntime';

interface Props { story: StoryPack; onChange: (story: StoryPack) => void; progress: BattleProgress | null; onProgress: (progress: BattleProgress) => void; vitals: Record<string, Vitals>; onVitals: (vitals: Record<string, Vitals>) => void; }
const input = 'bg-[var(--surface-2)] border border-[var(--border)] rounded-lg px-2 py-2 w-full min-w-0';
const panel = 'border border-[var(--border)] bg-[var(--surface)] rounded-xl p-3';
const num = (value: string) => value.trim() === '' ? 0 : Number(value);
export const BattlePanel: React.FC<Props> = ({ story, onChange, progress, onProgress, vitals, onVitals }) => {
  const config = story.battleConfig;
  const [editing, setEditing] = useState(false);
  const [active, setActive] = useState('');
  const [opponent, setOpponent] = useState('');
  const [message, setMessage] = useState('');
  const [hit, setHit] = useState('');
  const [busy, setBusy] = useState(false);
  const processing = useRef(false);
  const update = (next: BattleConfig) => onChange({ ...story, battleConfig: next });
  const emptyConfig = (): BattleConfig => ({ elements: [], manaPerTurn: 2, field: { name: '', elements: [] }, phases: [{ id: 'main', name: 'ช่วงหลัก' }, { id: 'followup', name: 'ช่วงถัดไป' }], actions: [] });
  const apply = (result: {ok: boolean;error?: string;progress?: BattleProgress;hitId?: string}, done = false) => {
    if (!result.ok || !result.progress) return setMessage(result.error || 'ประมวลผลไม่สำเร็จ');
    onProgress(result.progress);
    onVitals(result.progress.vitals);
    setMessage(done ? 'ฟินิท · แอคชั่นเสร็จ' : 'อัปเดตลำดับแล้ว');
    if (result.hitId) { setHit(result.hitId); window.setTimeout(() => setHit(''), 500); }
  };
  const act = (action: BattleAction) => {
    if (!config || !progress || processing.current) return;
    processing.current = true;
    setBusy(true);
    try { apply(performBattleAction(story, config, progress, action), true); }
    finally { window.setTimeout(() => { processing.current = false; setBusy(false); }, 200); }
  };
  const changeAction = (index: number, patch: Partial<BattleAction>) => {
    if (!config) return;
    update({ ...config, actions: config.actions.map((action, i) => i === index ? { ...action, ...patch } : action) });
  };
  const changeEffect = (index: number, effectIndex: number, effect: BattleEffect) => {
    if (!config) return;
    changeAction(index, { effects: config.actions[index].effects.map((old, i) => i === effectIndex ? effect : old) });
  };
  const stats = (id: string) => progress?.vitals[id] || vitals[id] || story.characters.find(c => c.id === id)?.vitals;
  const fighter = (id: string) => {
    const character = story.characters.find(c => c.id === id);
    if (!character) return null;
    const asset = character.portraitAssetId && story.assets[character.portraitAssetId];
    const values = stats(id);
    return <div className={`${panel} ${hit === id ? 'battle-hit' : ''}`} key={id}>
      <div className="flex items-center gap-3">{asset ? <img src={asset.dataUrl} alt="" className="w-14 h-14 object-cover rounded-lg" /> : <div className="w-14 h-14 rounded-lg bg-emerald-900/40 grid place-items-center text-xl">◇</div>}
        <div><b>{character.name}</b><p className="text-xs">HP {values?.hp} · MP {values?.mp} · EN {values?.en}</p><p className="text-xs text-slate-300">สถานะ: {(progress?.statuses?.[id] || character.statusEffects).join(', ') || 'ไม่มี'} · {character.innateSkill.name}</p><p className="text-xs text-slate-300">สล็อต: {character.abilitySlots.map(slot => story.cards.find(card => card.id === slot.equippedCardId)?.name || slot.name).join(', ') || 'ไม่มี'}</p><p className="text-xs text-slate-300">ACT {character.attributes.ACT} · DEF {character.attributes.DEF} · SPE {character.attributes.SPE} · CRI {character.attributes.CRI}</p><p className="text-xs text-slate-300">{Object.entries(character.capabilities).map(([key,value]) => `${key} ${value}`).join(' · ')}</p><p className="text-xs text-slate-300">ธาตุตัวละคร: {[...character.elemental.yangGroup, ...character.elemental.yinGroup].join(', ') || 'ยังไม่ระบุ'}</p></div></div>
      <p className="mt-2 text-xs text-sky-200">มานาสะสม (เพดานธาตุละ 10)</p><div className="flex flex-wrap gap-1 mt-1">{config?.elements.map(element => <span key={element} className="border border-sky-400/30 rounded px-2 py-1 text-xs">{element}: {progress?.mana[id]?.[element] || 0}/10</span>)}</div>
    </div>;
  };
  return <div className="h-full overflow-y-auto text-sm space-y-3 pb-8" aria-label="Battle">
    <div className="flex justify-between items-center"><h3 className="font-bold text-lg">⚔ Battle</h3><button className="border rounded-lg px-3 py-2" onClick={() => setEditing(!editing)}>{editing ? 'ปิดการตั้งค่า' : 'ตั้งค่าสนามและคำสั่ง'}</button></div>
    {!config && <div className={panel}><p>ยังไม่กำหนดกติกา Battle สำหรับโครงการนี้</p><button className="border rounded p-2 mt-2" onClick={() => { update(emptyConfig()); setEditing(true); }}>เริ่มกำหนด</button></div>}
    {config && editing && <section className={`${panel} space-y-4`} aria-label="กำหนด Battle">
      <p className="font-bold">กติกาของโครงการ · ระบุค่าที่ใช้จริงก่อนเริ่ม</p>
      <label className="block">พื้นที่จาก Locations<select className={input} value={config.field.locationId || ''} onChange={e => { const location = story.locations.find(l => l.locationId === e.target.value); update({ ...config, field: { ...config.field, locationId: location?.locationId, name: location?.title || config.field.name, note: location?.description || config.field.note } }); }}><option value="">ไม่ผูกพื้นที่</option>{story.locations.map(l => <option key={l.locationId} value={l.locationId}>{l.title}</option>)}</select></label>
      <label className="block">ชื่อสนาม<input className={input} value={config.field.name} onChange={e => update({ ...config, field: { ...config.field, name: e.target.value } })} /></label>
      <label className="block">เวลาในฉาก<input className={input} value={config.field.time || ''} onChange={e => update({ ...config, field: { ...config.field, time: e.target.value } })} /></label>
      <label className="block">ธาตุทั้งหมด (คั่นด้วยจุลภาค เช่น น้ำ, ลม)<input className={input} value={config.elements.join(', ')} onChange={e => { const elements = [...new Set(e.target.value.split(',').map(s => s.trim()).filter(Boolean))]; update({ ...config, elements, field: { ...config.field, elements: config.field.elements.filter(x => elements.includes(x)) } }); }} /></label>
      <label className="block">มานาที่สนามเติมต่อธาตุเมื่อเริ่มเทิร์น (สูงสุดสะสม 10)<input className={input} type="number" min="0" max="10" step="1" value={config.manaPerTurn ?? 2} onChange={e => update({ ...config, manaPerTurn: num(e.target.value) })} /></label>
      <fieldset><legend>ธาตุที่สนามเติม</legend><div className="flex flex-wrap gap-3">{config.elements.map(element => <label key={element}><input type="checkbox" checked={config.field.elements.includes(element)} onChange={e => update({ ...config, field: { ...config.field, elements: e.target.checked ? [...config.field.elements, element] : config.field.elements.filter(x => x !== element) } })} /> {element}</label>)}</div></fieldset>
      <label className="block">สภาพพื้นที่ / เวลา / โบนัส (ข้อความประกอบ)<textarea className={input} value={config.field.note || ''} onChange={e => update({ ...config, field: { ...config.field, note: e.target.value } })} /></label>
      <div><b>ลำดับช่วงในหนึ่งเทิร์น</b><p className="text-xs text-slate-300">Rule ที่ผูกกับช่วงใช้ตรวจเงื่อนไขก่อนออกจากช่วงนั้น; ไม่ผ่านจะค้างอยู่ช่วงเดิม</p><div className="space-y-2">{config.phases.map((phase, index) => <div key={phase.id} className="flex flex-wrap gap-2 items-center"><span>{index + 1}</span><input aria-label="ชื่อช่วง" className={`${input} flex-1`} value={phase.name} onChange={e => update({ ...config, phases: config.phases.map(p => p.id === phase.id ? { ...p, name: e.target.value } : p) })} /><select aria-label="เงื่อนไขก่อนออกจากช่วง" className={input} value={phase.ruleId || ''} onChange={e => update({ ...config, phases: config.phases.map(p => p.id === phase.id ? { ...p, ruleId: e.target.value || undefined } : p) })}><option value="">ไม่มีเงื่อนไข</option>{story.rulesets.map(rule => <option key={rule.id} value={rule.id}>{rule.name}</option>)}</select><button disabled={config.phases.length === 1 || config.actions.some(a => a.phaseId === phase.id)} onClick={() => update({ ...config, phases: config.phases.filter(p => p.id !== phase.id) })}>ลบ</button></div>)}</div><button className="border rounded p-2 mt-2" onClick={() => update({ ...config, phases: [...config.phases, { id: generateId('phase'), name: 'ช่วงใหม่' }] })}>+ เพิ่มช่วง</button></div>
      <div className="space-y-3"><b>คำสั่งและสูตรผลลัพธ์</b><p className="text-xs text-slate-300">จำนวนบวกเพิ่มค่า จำนวนลบลดค่า · กำหนดเป็นข้อมูล ไม่รันโค้ดจากข้อความ</p>
        {config.actions.map((action, i) => <div key={action.id} className="border border-white/15 rounded-xl p-3 space-y-2">
          <div className="flex gap-2"><input aria-label="ชื่อแอคชั่น" className={input} value={action.name} onChange={e => changeAction(i, { name: e.target.value })} /><button onClick={() => update({ ...config, actions: config.actions.filter(a => a.id !== action.id) })}>ลบ</button></div>
          <div className="grid grid-cols-2 gap-2"><label>ประเภท<select className={input} value={action.kind} onChange={e => changeAction(i, { kind: e.target.value as BattleAction['kind'] })}>{['Attack','Def','Skill','Item'].map(k => <option key={k}>{k}</option>)}</select></label><label>ช่วง<select className={input} value={action.phaseId} onChange={e => changeAction(i, { phaseId: e.target.value })}>{config.phases.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}</select></label></div>
          <label>เงื่อนไข Rules (ถ้ามี)<select className={input} value={action.ruleId || ''} onChange={e => changeAction(i, { ruleId: e.target.value || undefined })}><option value="">ไม่ใช้</option>{story.rulesets.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}</select></label>
          <label>ต้องติดตั้งการ์ด (ถ้ามี)<select className={input} value={action.sourceCardId || ''} onChange={e => changeAction(i, { sourceCardId: e.target.value || undefined })}><option value="">ไม่ใช้</option>{story.cards.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}</select></label>
          <div><b>ค่าร่ายมานา</b><div className="flex flex-wrap gap-2">{config.elements.map(element => <label key={element} className="w-24">{element}<input className={input} type="number" min="0" step="1" value={action.cost[element] || 0} onChange={e => changeAction(i, { cost: { ...action.cost, [element]: num(e.target.value) } })} /></label>)}</div></div>
          <div><b>ผลของคำสั่ง</b>{action.effects.map((effect, j) => <div key={j} className="grid grid-cols-2 md:grid-cols-5 gap-2 mt-2 items-end">
            <label>ชนิด<select className={input} value={effect.type} onChange={e => changeEffect(i, j, e.target.value === 'field' ? { type: 'field', element: config.elements[0] || '', enabled: false } : e.target.value === 'status' ? { type: 'status', target: 'opponent', status: 'ติดพิษ', enabled: true } : e.target.value === 'mana' ? { type: 'mana', target: 'opponent', element: config.elements[0] || '', amount: 0 } : { type: 'vital', target: 'opponent', stat: 'hp', amount: 0 })}><option value="vital">HP/MP/EN</option><option value="mana">มานา</option><option value="field">ธาตุสนาม</option><option value="status">สถานะ</option></select></label>
            {effect.type !== 'field' && <label>เป้าหมาย<select className={input} value={effect.target} onChange={e => changeEffect(i, j, { ...effect, target: e.target.value as 'self'|'opponent' })}><option value="opponent">อีกฝั่ง</option><option value="self">ตนเอง</option></select></label>}
            {effect.type === 'vital' && <label>ค่า<select className={input} value={effect.stat} onChange={e => changeEffect(i, j, { ...effect, stat: e.target.value as 'hp'|'mp'|'en' })}>{['hp','mp','en'].map(k => <option key={k}>{k}</option>)}</select></label>}
            {(effect.type === 'mana' || effect.type === 'field') && <label>ธาตุ<select className={input} value={effect.element} onChange={e => changeEffect(i, j, { ...effect, element: e.target.value })}>{config.elements.map(k => <option key={k}>{k}</option>)}</select></label>}
            {effect.type === 'status' && <label>ชื่อสถานะ<input className={input} value={effect.status} onChange={e => changeEffect(i, j, { ...effect, status: e.target.value })} /></label>}
            {(effect.type === 'field' || effect.type === 'status') ? <label>ผล<select className={input} value={String(effect.enabled)} onChange={e => changeEffect(i, j, { ...effect, enabled: e.target.value === 'true' })}><option value="false">ถอด / ตัด</option><option value="true">เพิ่ม / เปิด</option></select></label> : <label>จำนวน +/−<input className={input} type="number" step="1" value={effect.amount} onChange={e => changeEffect(i, j, { ...effect, amount: num(e.target.value) })} /></label>}
            {effect.type === 'vital' && <label className="col-span-2">บวกเพิ่มตามค่าตัวละคร (ตัวเลือก)<select className={input} value={effect.scale ? `${effect.scale.source}:${effect.scale.stat}` : ''} onChange={e => { const [source, stat] = e.target.value.split(':'); changeEffect(i, j, { ...effect, scale: stat ? { source: source as 'self'|'opponent', stat, multiplier: 1 } : undefined }); }}><option value="">ใช้จำนวนคงที่</option>{['self','opponent'].flatMap(source => [...['ACT','DEF','SPE','CRI'], ...story.attributeDefinitions.map(attr => attr.key)].map(stat => <option key={`${source}:${stat}`} value={`${source}:${stat}`}>{source === 'self' ? 'ผู้ใช้' : 'อีกฝั่ง'} · {stat}</option>))}</select></label>}
            {effect.type === 'vital' && effect.scale && <label>ตัวคูณ<input className={input} type="number" step="1" value={effect.scale.multiplier} onChange={e => changeEffect(i, j, { ...effect, scale: { ...effect.scale!, multiplier: num(e.target.value) } })} /></label>}
            <button className="border rounded p-2" onClick={() => changeAction(i, { effects: action.effects.filter((_, k) => k !== j) })}>ลบผล</button></div>)}<button className="border rounded p-2 mt-2" onClick={() => changeAction(i, { effects: [...action.effects, { type: 'vital', target: 'opponent', stat: 'hp', amount: 0 }] })}>+ เพิ่มผล</button></div>
        </div>)}<button className="border rounded p-2" onClick={() => update({ ...config, actions: [...config.actions, { id: generateId('battle-action'), name: 'คำสั่งใหม่', kind: 'Skill', phaseId: config.phases[0].id, cost: {}, effects: [] }] })}>+ เพิ่มคำสั่ง</button></div>
    </section>}
    {config && <><section className={panel}><p className="font-bold">สนาม: {config.field.name || 'ยังไม่ตั้งชื่อ'} · {config.field.time || 'ไม่ระบุเวลา'}</p><p className="text-xs">แหล่งเติมมานา: {(progress ? progress.fieldElements : config.field.elements).join(', ') || 'ไม่มี'} · {config.field.note || 'ไม่มีรายละเอียดพื้นที่'}</p></section>
      {!progress ? <section className={`${panel} space-y-2`}><b>เริ่มการต่อสู้หนึ่งต่อหนึ่ง</b><div className="grid grid-cols-2 gap-2"><label>ฝั่งตัวละคร<select className={input} value={active} onChange={e => setActive(e.target.value)}><option value="">เลือก</option>{story.characters.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}</select></label><label>ฝั่งศัตรู<select className={input} value={opponent} onChange={e => setOpponent(e.target.value)}><option value="">เลือก</option>{story.characters.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}</select></label></div><button className="border border-emerald-400 rounded px-3 py-2" onClick={() => apply(newBattle(story, config, active, opponent, vitals))}>สร้างสนาม</button></section> : <>
        <div className="grid grid-cols-2 gap-2">{fighter(progress.activeId)}{fighter(progress.opponentId)}</div>
        <section className={panel}><b>เทิร์น {progress.turn} · {story.characters.find(c => c.id === progress.activeId)?.name}</b><p>ช่วง: {config.phases.map((p, i) => <span key={p.id} className={`inline-block m-1 px-2 py-1 rounded ${i === progress.phaseIndex ? 'bg-emerald-700' : 'bg-white/10'}`}>{p.name}</span>)}</p>
          {!progress.started ? <button className="border rounded p-2" onClick={() => apply(beginTurn(story, config, progress))}>เริ่มเทิร์น · รับมานา</button> : <button className="border rounded p-2" onClick={() => apply(advanceBattle(story, config, progress))}>{progress.phaseIndex + 1 < config.phases.length ? 'ไปช่วงถัดไป' : 'จบเทิร์น · สลับฝั่ง'}</button>}
          <button className="ml-2 text-xs underline" onClick={() => { if (window.confirm('เริ่ม Battle ใหม่? ความคืบหน้ารอบนี้จะถูกแทนเมื่อบันทึก')) { const result = newBattle(story, config, progress.activeId, progress.opponentId, vitals); if (result.progress) onProgress(result.progress); setMessage('สร้าง Battle ใหม่แล้ว'); } }}>เริ่ม Battle ใหม่</button>
        </section><section className={panel}><b>Commands</b><div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2">{(['Attack','Def','Skill','Item'] as const).map(kind => <div key={kind}><b className="text-xs">{kind}</b>{config.actions.filter(a => a.kind === kind && a.phaseId === config.phases[progress.phaseIndex]?.id).map(action => <button disabled={!progress.started || busy} className="block w-full border border-emerald-400/40 rounded-lg p-2 text-left mt-1 disabled:opacity-40" key={action.id} onClick={() => act(action)}>{action.name}<small className="block">{Object.entries(action.cost).filter(([,n]) => Number(n) > 0).map(([e,n]) => `${e} ${n}`).join(' · ') || 'ไม่ใช้มานา'}</small>{action.sourceCardId && <small className="block text-sky-200">การ์ด: {story.cards.find(card => card.id === action.sourceCardId)?.name || 'ไม่พบ'} · โมดูล: {story.cards.find(card => card.id === action.sourceCardId)?.moduleSlots?.filter(Boolean).map(id => story.modules?.find(module => module.id === id)?.name || 'ไม่พบ').join(', ') || 'ไม่มี'}</small>}</button>)}</div>)}</div>{!config.actions.some(a => a.phaseId === config.phases[progress.phaseIndex]?.id) && <p className="text-slate-400">ช่วงนี้ยังไม่มีคำสั่งที่กำหนด</p>}</section>
        <section className={panel}><b>ประวัติการต่อสู้</b>{progress.log.map((line, i) => <p className="border-b border-white/10 py-1 text-xs" key={i}>{line}</p>)}</section>
      </>}
    </>}
    {message && <p role="status" className="text-emerald-200">{message}</p>}
  </div>;
};
