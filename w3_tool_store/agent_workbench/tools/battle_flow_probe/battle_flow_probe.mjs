// Isolated Battle flow experiment for W3 Agent Workbench. No app imports or writes.
const MAX_MANA = 10;
const integer = n => Number.isSafeInteger(n) && n >= 0;
const copy = value => structuredClone(value);
const reject = reason => ({ ok: false, reason });

export function createBattle(definition, actorIds) {
  if (!Array.isArray(definition.phases) || !definition.phases.length ||
      new Set(definition.phases).size !== definition.phases.length ||
      !Array.isArray(definition.elements) || new Set(definition.elements).size !== definition.elements.length ||
      actorIds.length !== 2 || actorIds[0] === actorIds[1] ||
      !definition.field.every(element => definition.elements.includes(element))) {
    return reject('ข้อมูลสนาม ผู้ต่อสู้ หรือเฟสไม่ครบ');
  }
  return { ok: true, state: { turn: 1, phaseIndex: 0, active: actorIds[0], opponent: actorIds[1],
    started: false, field: [...definition.field], mana: Object.fromEntries(actorIds.map(id => [id, {}])),
    hp: Object.fromEntries(actorIds.map(id => [id, definition.startingHp[id]])), log: [] } };
}

export function beginTurn(definition, state) {
  if (state.started) return reject('เทิร์นนี้เริ่มแล้ว');
  const next = copy(state);
  for (const element of next.field) {
    if (!definition.elements.includes(element)) return reject(`ธาตุไม่รู้จัก: ${element}`);
    const current = next.mana[next.active][element] || 0;
    next.mana[next.active][element] = Math.min(MAX_MANA, current + 2);
  }
  next.started = true;
  next.log.push(`T${next.turn} ${next.active} รับมานา: ${next.field.join(', ') || 'ไม่มี'}`);
  return { ok: true, state: next };
}

export function useAction(definition, state, actionId) {
  const action = definition.actions.find(item => item.id === actionId);
  if (!state.started || !action || action.phase !== definition.phases[state.phaseIndex]) return reject('ใช้แอคชั่นในเฟสนี้ไม่ได้');
  if (action.cardId && !definition.equipped[state.active]?.includes(action.cardId)) return reject('ยังไม่ได้ติดตั้งการ์ด');
  if (!Array.isArray(action.effects) || !action.effects.length) return reject('ยังไม่กำหนดผล');
  for (const [element, cost] of Object.entries(action.cost || {})) {
    if (!definition.elements.includes(element) || !integer(cost)) return reject('ค่าร่ายไม่ถูกต้อง');
    if ((state.mana[state.active][element] || 0) < cost) return reject(`มานา ${element} ไม่พอ`);
  }
  for (const effect of action.effects) {
    if (effect.type === 'hp' && (!['self', 'opponent'].includes(effect.target) || !Number.isSafeInteger(effect.amount))) return reject('ผล HP ไม่ถูกต้อง');
    if (effect.type === 'field' && (!definition.elements.includes(effect.element) || typeof effect.enabled !== 'boolean')) return reject('ผลสนามไม่ถูกต้อง');
    if (!['hp', 'field'].includes(effect.type)) return reject('ชนิดผลยังไม่รองรับ');
  }
  // All checks precede mutation; failure returns no replacement state.
  const next = copy(state);
  for (const [element, cost] of Object.entries(action.cost || {})) next.mana[next.active][element] -= cost;
  const before = copy({ mana: state.mana[state.active], hp: state.hp, field: state.field });
  for (const effect of action.effects) {
    if (effect.type === 'hp') {
      const target = effect.target === 'self' ? next.active : next.opponent;
      next.hp[target] = Math.max(0, next.hp[target] + effect.amount);
    } else if (effect.enabled) next.field = [...new Set([...next.field, effect.element])];
    else next.field = next.field.filter(element => element !== effect.element);
  }
  next.log.push(`T${next.turn}/${definition.phases[next.phaseIndex]} ${next.active} ใช้ ${action.name}: ${JSON.stringify(before)} → ${JSON.stringify({ mana: next.mana[next.active], hp: next.hp, field: next.field })}`);
  return { ok: true, state: next, signal: 'ฟินิท · แอคชั่นเสร็จ' };
}

export function advancePhase(definition, state) {
  if (!state.started) return reject('ต้องเริ่มเทิร์นก่อน');
  const next = copy(state);
  if (next.phaseIndex + 1 < definition.phases.length) next.phaseIndex++;
  else {
    next.turn++;
    next.phaseIndex = 0;
    [next.active, next.opponent] = [next.opponent, next.active];
    next.started = false;
  }
  return { ok: true, state: next };
}
