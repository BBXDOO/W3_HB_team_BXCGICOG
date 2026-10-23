
import { CharacterPack } from '../types';

/**
 * Rule Engine v0.1
 * Supports basic strings like "+HP 2", "-EN 1", "ADD_NOTE('foo')"
 */
export const applyOutcome = (character: CharacterPack, outcomeStr: string): CharacterPack => {
  // Fix: CharacterPack uses 'vitals' instead of 'statsCompact'
  const newChar = { ...character, vitals: { ...character.vitals } };
  const parts = outcomeStr.trim().split(' ');
  
  if (parts.length < 2) return newChar;
  
  const action = parts[0]; // "+HP", "-MP", etc
  const value = parseInt(parts[1], 10);
  
  switch (action.toUpperCase()) {
    case '+HP': newChar.vitals.hp += value; break;
    case '-HP': newChar.vitals.hp -= value; break;
    case '+MP': newChar.vitals.mp += value; break;
    case '-MP': newChar.vitals.mp -= value; break;
    case '+EN': newChar.vitals.en += value; break;
    case '-EN': newChar.vitals.en -= value; break;
    case 'ADD_NOTE':
      const note = outcomeStr.match(/'([^']+)'/)?.[1] || outcomeStr.match(/"([^"]+)"/)?.[1];
      // Fix: CharacterPack uses 'backgroundText' instead of 'notes'
      if (note) newChar.backgroundText = (newChar.backgroundText ? newChar.backgroundText + '\n' : '') + note;
      break;
  }
  
  return newChar;
};

export const checkCondition = (character: CharacterPack, conditionStr: string): boolean => {
  if (!conditionStr) return true;
  
  // Example: "HP > 0"
  const hpMatch = conditionStr.match(/HP\s*([><=]+)\s*(\d+)/i);
  if (hpMatch) {
    const op = hpMatch[1];
    const val = parseInt(hpMatch[2], 10);
    // Fix: CharacterPack uses 'vitals' instead of 'statsCompact'
    const charVal = character.vitals.hp;
    if (op === '>') return charVal > val;
    if (op === '<') return charVal < val;
    if (op === '>=') return charVal >= val;
    if (op === '<=') return charVal <= val;
    if (op === '==') return charVal === val;
  }
  
  return true;
};