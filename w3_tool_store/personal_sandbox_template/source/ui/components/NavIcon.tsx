import React from 'react';
import { TabId } from '../../types';

const paths: Record<TabId | 'ai' | 'search' | 'add' | 'export', React.ReactNode> = {
  search: <><circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/></>,
  add: <path d="M12 4v16M4 12h16"/>,
  export: <><path d="M12 16V3m-5 5 5-5 5 5M4 14v7h16v-7"/></>,
  home: <><path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><path d="M9 21v-7h6v7"/></>,
  story: <><path d="M4 4h11l5 5v11H4z"/><path d="M15 4v5h5M7 13h10M7 17h8"/></>,
  character: <><circle cx="9" cy="8" r="3"/><path d="M3 20v-2a6 6 0 0 1 12 0v2zM17 6a3 3 0 0 1 0 6M18 15a5 5 0 0 1 3 5"/></>,
  card: <><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18m-14 6h5"/></>,
  board: <><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18M15 3v18M3 9h18M3 15h18"/></>,
  location: <><path d="M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0z"/><circle cx="12" cy="10" r="2.5"/></>,
  item: <><path d="M3 8h18v12H3zM8 8V6a4 4 0 0 1 8 0v2M3 13h18"/></>,
  event: <><path d="m13 2-9 12h7l-1 8 10-12h-7z"/></>,
  rule: <><path d="M12 3v18M5 7h14M5 7l-3 6h6zM19 7l-3 6h6zM8 21h8"/></>,
  commonPlay: <><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9h10M7 13h6M7 17h4"/></>,
  play: <><rect x="3" y="7" width="18" height="12" rx="5"/><path d="M7 13h5m-2.5-2.5v5M16 12h.01M18 15h.01"/></>,
  ai: <><circle cx="12" cy="12" r="8"/><path d="M9 9h.01M15 9h.01M8 14c2 3 6 3 8 0M12 4V2M4 12H2M22 12h-2"/></>
};

export const NavIcon: React.FC<{ name: TabId | 'ai' | 'search' | 'add' | 'export'; className?: string }> = ({ name, className }) => (
  <svg className={className} viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    {paths[name]}
  </svg>
);
