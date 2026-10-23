import type { ItemPack } from '../types';

export type Inventory = Record<string, Record<string, number>>;
export interface InventoryResult { ok: boolean; inventory: Inventory; error?: string; quantity?: number }

/** Adjusts ownership only for registered items. Item definitions are never modified. */
export const changeInventory = (inventory: Inventory, items: ItemPack[], ownerId: string, itemId: string, delta: number): InventoryResult => {
  if (!ownerId || ['__proto__', 'constructor', 'prototype'].includes(ownerId) || ['__proto__', 'constructor', 'prototype'].includes(itemId))
    return { ok: false, inventory, error: 'เจ้าของหรือ ID ไอเทมไม่ถูกต้อง' };
  const item = items.find(entry => entry.id === itemId);
  if (!item) return { ok: false, inventory, error: 'ไม่พบไอเทมในทะเบียนโครงการ' };
  if (!Number.isSafeInteger(delta) || delta === 0) return { ok: false, inventory, error: 'จำนวนที่ปรับต้องเป็นจำนวนเต็มที่ไม่ใช่ศูนย์' };
  const current = inventory[ownerId]?.[itemId] || 0;
  if (!Number.isSafeInteger(current) || current < 0) return { ok: false, inventory, error: 'จำนวนเดิมไม่ถูกต้อง' };
  const next = current + delta;
  if (!Number.isSafeInteger(next) || next < 0) return { ok: false, inventory, error: 'จำนวนไอเทมไม่เพียงพอ' };
  const max = item.properties.maxStack;
  if (delta > 0 && (!item.properties.stackable && next > 1 || max !== undefined && next > max))
    return { ok: false, inventory, error: 'เกินจำนวนที่ไอเทมกำหนด' };
  const owned = { ...(inventory[ownerId] || {}) };
  if (next === 0) delete owned[itemId]; else owned[itemId] = next;
  return { ok: true, inventory: { ...inventory, [ownerId]: owned }, quantity: next };
};
