import type { ProjectKind, RunPresentation, RunSection, RunSource } from '../types';

export const RUN_SOURCES: { source: RunSource; label: string; icon: string }[] = [
  { source: 'story', label: 'เนื้อหา', icon: '▤' },
  { source: 'board', label: 'แผนที่', icon: '▦' },
  { source: 'cards', label: 'การ์ด', icon: '◇' },
  { source: 'characters', label: 'ตัวละคร', icon: '♙' },
  { source: 'items', label: 'ไอเทม', icon: '▣' },
  { source: 'locations', label: 'โลเกชั่น', icon: '⌖' },
  { source: 'rules', label: 'กฎ', icon: '☷' },
  { source: 'events', label: 'อีเวนต์', icon: '⚡' },
  { source: 'battle', label: 'Battle', icon: '⚔' },
  { source: 'special', label: 'เรื่องพิเศษ', icon: '✦' }
];

const preset: Record<ProjectKind, RunSource[]> = {
  library: ['story', 'rules', 'locations', 'items', 'battle'],
  bookcraft: ['story', 'board', 'cards', 'characters', 'items', 'events', 'battle', 'special'],
  concept: ['story', 'board', 'locations', 'events', 'rules', 'battle']
};

export const newRunSection = (source: RunSource, id: string): RunSection => {
  const option = RUN_SOURCES.find(item => item.source === source)!;
  return { id, source, label: option.label, icon: option.icon, visible: true };
};

export const defaultRunPresentation = (kind?: ProjectKind): RunPresentation => ({
  sections: (preset[kind || 'bookcraft']).map((source, index) => newRunSection(source, `${source}-${index}`)),
  backgroundColor: '#111a18'
});
