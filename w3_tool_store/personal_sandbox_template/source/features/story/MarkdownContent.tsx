import React, { lazy, Suspense } from 'react';
const Renderer = lazy(() => import('./MarkdownRenderer').then(module => ({ default: module.MarkdownContent })));
export const MarkdownContent: React.FC<{ value: string }> = props => <Suspense fallback={<p role="status">กำลังจัดรูปแบบเอกสาร…</p>}><Renderer {...props} /></Suspense>;
