import type { ProjectStatus, StoryPack } from '../types';

export interface ProjectSummary {
  version?: string;
  author?: string;
  createdAt?: number;
  projectStatus?: ProjectStatus;
  projectProgress?: number;
  recordCount?: number;
  summaryVersion?: 1;
}
export const projectStatusLabels: Record<ProjectStatus, string> = {
  draft: 'เริ่มต้น', active: 'กำลังพัฒนา', paused: 'พักไว้', complete: 'เสร็จแล้ว'
};
export const normalizeProgress = (value: unknown): number | undefined =>
  typeof value === 'number' && Number.isFinite(value) ? Math.max(0, Math.min(100, Math.round(value))) : undefined;

export const summarizeProject = (story: StoryPack): ProjectSummary => ({
  summaryVersion: 1, version: story.version, author: story.author, createdAt: story.createdAt,
  projectStatus: story.projectStatus && projectStatusLabels[story.projectStatus] ? story.projectStatus : undefined,
  projectProgress: normalizeProgress(story.projectProgress),
  recordCount: [story.characters, story.boards, story.locations, story.cards, story.modules, story.items,
    story.events, story.rulesets, story.commonPlay, story.storyNodes].reduce((sum, items) => sum + (items?.length || 0), 0)
});
