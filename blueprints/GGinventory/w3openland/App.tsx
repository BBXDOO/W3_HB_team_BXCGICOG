
import React, { useState, useEffect } from 'react';
import { StoryPack, ActiveMode } from './types';
import { getStory, saveStory, getStoryIndex, DEFAULT_ATTRIBUTES } from './core/storage';
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

  // ระบบ Auto-save: บันทึกข้อมูลลง LocalStorage อัตโนมัติเมื่อมีการเปลี่ยนแปลง (Debounce 2s)
  useEffect(() => {
    if (currentStory) {
      const timer = setTimeout(() => {
        saveStory(currentStory);
        console.log('W3: Auto-saved to local repository');
      }, 2000); 
      return () => clearTimeout(timer);
    }
  }, [currentStory]);

  // ระบบ Safety Save: บันทึกทันทีก่อนปิด Tab หรือ Browser
  useEffect(() => {
    const handleUnload = () => {
      if (currentStory) {
        saveStory(currentStory);
      }
    };
    window.addEventListener('beforeunload', handleUnload);
    window.addEventListener('pagehide', handleUnload);
    return () => {
      window.removeEventListener('beforeunload', handleUnload);
      window.removeEventListener('pagehide', handleUnload);
    };
  }, [currentStory]);

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

  const handleNewStory = () => {
    const id = generateId('st');
    const newPack: StoryPack = {
      storyId: id,
      title: 'PROJECT_NEW_MONUMENT',
      author: 'ARCHITECT',
      version: 'v0.1.0',
      description: 'ระบุคำประกาศของระบบนิเวศนี้...',
      createdAt: Date.now(),
      updatedAt: Date.now(),
      uiTheme: 'darkNavy',
      activeMode: 'EDITOR',
      // Fix: Add required attributeDefinitions from default schema
      attributeDefinitions: DEFAULT_ATTRIBUTES,
      characters: [],
      boards: [],
      locations: [],
      cards: [],
      items: [],
      events: [],
      rulesets: [],
      storyNodes: [],
      assets: {}
    };
    saveStory(newPack);
    setActiveStoryId(id);
  };

  const handleSave = (updated: StoryPack) => {
    saveStory(updated);
    setCurrentStory(updated);
  };

  const handleExit = () => {
    if (currentStory) saveStory(currentStory);
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
