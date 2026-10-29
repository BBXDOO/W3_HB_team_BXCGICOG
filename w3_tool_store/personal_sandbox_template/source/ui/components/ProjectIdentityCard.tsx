import React from 'react';
import type { ProjectSummary } from '../../core/projectSummary';
import { normalizeProgress, projectStatusLabels } from '../../core/projectSummary';
import { formatDate } from '../../core/utils';

export const ProjectIdentityCard: React.FC<{ project: ProjectSummary & { storyId: string; title: string; updatedAt?: number }; description?: string }> = ({ project, description }) => {
  const progress = normalizeProgress(project.projectProgress);
  return <div className="project-identity-card">
    <div className="project-terminal-line"><span className="project-terminal-dots" aria-hidden="true"><i /><i /><i /></span><span>PROJECT / IDENTITY</span><span className="project-status">{project.projectStatus ? projectStatusLabels[project.projectStatus] || 'ยังไม่ระบุสถานะ' : 'ยังไม่ระบุสถานะ'}</span></div>
    <h3 className="project-identity-title"><span aria-hidden="true">{'< '}</span>{project.title}<span aria-hidden="true">{' />'}</span></h3>
    <dl className="project-identity-meta"><div><dt>ID</dt><dd>{project.storyId}</dd></div><div><dt>VERSION</dt><dd>{project.version || '—'}</dd></div><div><dt>AUTHOR</dt><dd>{project.author || '—'}</dd></div><div><dt>รายการหลัก</dt><dd>{project.recordCount ?? '—'}</dd></div></dl>
    {description && <p className="project-identity-description">{description}</p>}
    <div className="project-progress-label"><span>ความคืบหน้า · กำหนดเอง</span><strong>{progress === undefined ? 'ยังไม่กำหนด' : `${progress}%`}</strong></div>
    {progress === undefined ? <div className="project-progress-track" aria-hidden="true" /> : <div className="project-progress-track" role="progressbar" aria-label="ความคืบหน้าโครงการ" aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress}><span style={{ width: `${progress}%` }} /></div>}
    <div className="project-identity-dates"><span>สร้าง {project.createdAt ? formatDate(project.createdAt) : '—'}</span><span>แก้ไข {formatDate(project.updatedAt || project.createdAt || 0)}</span></div>
  </div>;
};
