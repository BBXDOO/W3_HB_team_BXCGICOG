import React from 'react';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import rehypeSanitize from 'rehype-sanitize';
import { documentBridge } from '../../core/documentFiles';

type AstNode = { type: string; tagName?: string; value?: string; properties?: Record<string, unknown>; children?: AstNode[] };
const textOf = (node: AstNode): string => node.value || node.children?.map(textOf).join('') || '';
function headingIds() {
  return (tree: AstNode) => {
    const seen = new Map<string, number>();
    const walk = (node: AstNode) => {
      if (/^h[1-6]$/.test(node.tagName || '')) {
        const slug = textOf(node).toLowerCase().normalize('NFKC').replace(/[^\p{L}\p{N}\s_-]/gu, '').trim().replace(/\s+/g, '-') || 'section';
        const n = seen.get(slug) || 0; seen.set(slug, n + 1);
        node.properties = { ...node.properties, id: `story-heading-${slug}${n ? `-${n}` : ''}` };
      }
      node.children?.forEach(walk);
    };
    walk(tree);
  };
}

export const MarkdownContent: React.FC<{ value: string }> = ({ value }) => <div className="markdown-content">
  <Markdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw, rehypeSanitize, headingIds]} components={{
    img: ({ alt }) => <span className="markdown-image-placeholder">ภาพ: {alt || 'ไม่มีคำบรรยาย'} · ยังไม่ได้แนบไฟล์ภาพ</span>,
    input: ({ checked }) => <input type="checkbox" checked={!!checked} disabled readOnly />,
    a: ({ node: _node, href, children, ...props }) => <a {...props} href={href} target={href?.startsWith('#') ? undefined : '_blank'} rel="noopener noreferrer" onClick={event => {
      if (href?.startsWith('#')) {
        event.preventDefault();
        let slug = href.slice(1); try { slug = decodeURIComponent(slug); } catch {}
        const root = event.currentTarget.closest('.markdown-content');
        const target = Array.from(root?.querySelectorAll('[id]') || []).find(item => item.id === slug || item.id === `story-heading-${slug}` || item.id === `user-content-${slug}`);
        target?.scrollIntoView({ block: 'start', behavior: 'smooth' });
      } else if (href && /^(https?:|mailto:)/i.test(href) && documentBridge()?.openExternal) {
        event.preventDefault(); documentBridge()!.openExternal!(href);
      }
    }}>{children}</a>
  }}>{value}</Markdown>
</div>;
