
import React, { useState, useEffect } from 'react';
import { StoryPack, ProjectKind } from './types';
import { getStory, saveStory } from './core/storage';
import { createEmptyProject } from './core/project';
import { generateId } from './core/utils';
import { LibraryPage } from './features/library/LibraryPage';
import { EditorShell } from './features/editor/EditorShell';

const App: React.FC = () => {
  const [activeStoryId, setActiveStoryId] = useState<string | null>(null);
  const [view, setView] = useState<'LIBRARY' | 'EDITOR'>('LIBRARY');
  const [currentStory, setCurrentStory] = useState<StoryPack | null>(null);
  const [canInstall, setCanInstall] = useState(false);

  useEffect(() => {
    const handleInstallReady = () => setCanInstall(true);
    window.addEventListener('pwa-install-ready', handleInstallReady);
    
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setCanInstall(false);
    }

    return () => window.removeEventListener('pwa-install-ready', handleInstallReady);
  }, []);

  useEffect(() => {
    if (activeStoryId) {
      const story = getStory(activeStoryId);
      if (story) {
        setCurrentStory(story);
        setView('EDITOR');
      }
    }
  }, [activeStoryId]);

  const handleOpenStory = (id: string) => {
    setActiveStoryId(id);
  };

  const handleNewStory = (projectKind: ProjectKind, title: string) => {
    const id = generateId('st');
    const newPack = createEmptyProject(id, projectKind, title);
    if (!saveStory(newPack)) {
      alert('สร้างโครงการไม่สำเร็จ โปรดตรวจพื้นที่เก็บข้อมูลในเครื่อง');
      return;
    }
    setActiveStoryId(id);
  };

  const handleSave = (updated: StoryPack) => {
    if (!saveStory(updated)) return false;
    setCurrentStory(updated);
    return true;
  };

  const handleExit = () => {
    setActiveStoryId(null);
    setCurrentStory(null);
    setView('LIBRARY');
  };

  if (view === 'EDITOR' && currentStory) {
    return (
      <EditorShell 
        story={currentStory} 
        onSave={handleSave} 
        onExit={handleExit} 
      />
    );
  }

  return (
    <LibraryPage 
      onOpenStory={handleOpenStory} 
      onNewStory={handleNewStory} 
      canInstall={canInstall}
    />
  );
};

export default App;
