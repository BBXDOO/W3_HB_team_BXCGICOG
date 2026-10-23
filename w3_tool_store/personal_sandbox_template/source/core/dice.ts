export const rollDice = (count: number, sides: number): number[] => {
  if (!Number.isInteger(count) || count < 1 || count > 10 || ![4, 6, 8, 10, 12, 20, 100].includes(sides)) {
    throw new Error('รูปแบบลูกเต๋าไม่รองรับ');
  }
  const max = 0x100000000;
  const limit = Math.floor(max / sides) * sides;
  return Array.from({ length: count }, () => {
    const buffer = new Uint32Array(1);
    do { crypto.getRandomValues(buffer); } while (buffer[0] >= limit);
    return buffer[0] % sides + 1;
  });
};
