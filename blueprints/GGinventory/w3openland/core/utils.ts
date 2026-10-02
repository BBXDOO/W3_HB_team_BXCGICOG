
export const generateId = (prefix: string = '') => {
  return `${prefix}${Date.now()}_${Math.floor(Math.random() * 10000)}`;
};

export const deepClone = <T,>(obj: T): T => {
  return JSON.parse(JSON.stringify(obj));
};

export const formatDate = (timestamp: number): string => {
  return new Date(timestamp).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

/**
 * W3 Studio Status Color System (v0.5)
 * 10-Level Granular Scale (Based on User Sketch)
 */
export const getStatusColor = (level: number): string => {
  const L = Math.max(0, Math.min(10, Math.round(level)));
  const colors = [
    '#111827', // 0: Black (Void)
    '#EF4444', // 1: Deep Red (Critical)
    '#F87171', // 2: Light Red (Danger)
    '#F97316', // 3: Deep Orange
    '#FB923C', // 4: Orange
    '#FACC15', // 5: Yellow
    '#EAB308', // 6: Deep Yellow
    '#A3E635', // 7: Lime
    '#4ADE80', // 8: Light Green
    '#22C55E', // 9: Green
    '#15803D'  // 10: Deep Green (Max)
  ];
  return colors[L] || colors[0];
};

/**
 * Special Status Overlays (Requested by User)
 * Purple, Black, White, Blue + EXODUS (Gold/Cyan)
 */
export const SPECIAL_STATUS = {
  MYSTIC: { color: '#A855F7', label: 'MYSTIC', icon: '🔮' },
  CURSE: { color: '#111827', label: 'CURSE', icon: '💀' },
  BLESS: { color: '#F1F5F9', label: 'BLESS', icon: '✨' },
  TECH: { color: '#3B82F6', label: 'TECH', icon: '⚙️' },
  EXODUS: { color: '#FCD34D', label: 'EXODUS', icon: '🕊️' } // Added Exodus Protocol
};
