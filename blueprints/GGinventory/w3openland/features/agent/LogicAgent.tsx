
import React, { useState, useEffect, useRef } from 'react';
import { GoogleGenAI } from "@google/genai";
import { StoryPack, TabId } from '../../types';
import { Button } from '../../ui/components/Button';

interface Message {
  role: 'user' | 'agent';
  content: string;
  suggestionData?: any;
  hasFile?: boolean;
}

interface LogicAgentProps {
  story: StoryPack;
  activeTab: TabId;
  selectedId: string | null;
  onApplyFix: (updatedStory: StoryPack) => void;
  isOpen: boolean;
  onClose: () => void;
}

export const LogicAgent: React.FC<LogicAgentProps> = ({ story, activeTab, selectedId, onApplyFix, isOpen, onClose }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [attachedFile, setAttachedFile] = useState<{data: string, mime: string, name: string} | null>(null);
  
  const scrollRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greeting = `สวัสดีครับเพื่อน... ผม Nexus Agent ประจำหน้า ${activeTab.toUpperCase()} ยินดีที่ได้คุยกันในพื้นที่สร้างสรรค์เล็กๆ แห่งนี้ครับ มีลอจิกหรือเรื่องราวส่วนไหนที่คุณอยากให้ผมช่วยขัดเกลาในระหว่างพักเหนื่อยไหมครับ?`;
      setMessages([{ role: 'agent', content: greeting }]);
    }
  }, [isOpen, activeTab]);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (ev) => {
      const base64 = (ev.target?.result as string).split(',')[1];
      setAttachedFile({
        data: base64,
        mime: file.type || 'text/plain',
        name: file.name
      });
    };
    reader.readAsDataURL(file);
  };

  const sendMessage = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if ((!input.trim() && !attachedFile) || isTyping) return;

    const userMsg = input.trim();
    const currentFile = attachedFile;
    
    setInput('');
    setAttachedFile(null);
    setMessages(prev => [...prev, { 
        role: 'user', 
        content: userMsg || `[ส่งข้อมูล: ${currentFile?.name}]`, 
        hasFile: !!currentFile 
    }]);
    setIsTyping(true);

    try {
      const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
      
      let contextData = "";
      if (activeTab === 'character' && selectedId) {
        contextData = `Character: ${JSON.stringify(story.characters.find(c => c.id === selectedId))}`;
      } else if (activeTab === 'story' && selectedId) {
        contextData = `Story Node: ${JSON.stringify(story.storyNodes.find(n => n.nodeId === selectedId))}`;
      } else if (activeTab === 'board') {
        contextData = `Board Stats: ${JSON.stringify({ 
          boards: story.boards.map(b => ({ title: b.title, size: `${b.width}x${b.height}` }))
        })}`;
      } else if (activeTab === 'item' && selectedId) {
        contextData = `Item: ${JSON.stringify(story.items.find(i => i.id === selectedId))}`;
      } else if (activeTab === 'card' && selectedId) {
        contextData = `Card/Module: ${JSON.stringify(story.cards.find(c => c.id === selectedId))}`;
      }

      const systemPrompt = `
        You are Nexus AI, a Senior Game Systems Architect and empathetic creative partner.
        You are helping a designer build a board game ecosystem called W3.IDP.
        The user works long, exhausting hours in a hospital (12-14h shifts). This tool is their sanctuary.
        
        STRICT BEHAVIORAL RULES:
        1. Empathy First: Be supportive, concise, and professional. Use warm, humble Thai language (like 'ครับเพื่อน', 'ยินดีช่วยเสมอครับ').
        2. Technical Expertise: Provide sound RPG design advice. Balance stats, refine logic, and spark narrative ideas.
        3. Implementation: If proposing a change, include a JSON block starting with FIX_DATA: { ... }.
        4. Deep Merge: When providing FIX_DATA for characters, always include nested objects like 'vitals' or 'capabilities' fully if changing one part of them.
        5. Focus: You are currently monitoring the ${activeTab} tab.
        6. Visual Analysis: If an image is provided, offer mechanic or flavor text suggestions based on its vibe.
      `;

      const contents: any = {
        parts: [{ text: `${systemPrompt}\n\nUser: ${userMsg}\n\nContext:\n${contextData}` }]
      };

      if (currentFile && currentFile.mime.startsWith('image/')) {
        contents.parts.push({
          inlineData: { data: currentFile.data, mimeType: currentFile.mime }
        });
      }

      const response = await ai.models.generateContent({
        model: 'gemini-3-flash-preview',
        contents,
      });

      const text = response.text || "Nexus Link Unstable.";
      let suggestionData = null;

      if (text.includes('FIX_DATA:')) {
        const jsonMatch = text.match(/FIX_DATA:\s*(\{[\s\S]*\})/);
        if (jsonMatch) {
          try { suggestionData = JSON.parse(jsonMatch[1]); } catch(e) {}
        }
      }

      setMessages(prev => [...prev, { role: 'agent', content: text, suggestionData }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'agent', content: "ขออภัยครับเพื่อน ระลอกสัญญาณขัดข้องชั่วคราว กรุณาลองส่งข้อความอีกครั้งนะครับ" }]);
    } finally {
      setIsTyping(false);
    }
  };

  const applyFix = (data: any) => {
    if (!data || !selectedId) return;
    const newStory = { ...story };

    const deepMerge = (target: any, source: any) => {
      for (const key in source) {
        if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
          if (!target[key]) target[key] = {};
          deepMerge(target[key], source[key]);
        } else {
          target[key] = source[key];
        }
      }
      return target;
    };

    if (activeTab === 'character') {
      newStory.characters = story.characters.map(c => {
        if (c.id === selectedId) {
          const cloned = JSON.parse(JSON.stringify(c));
          return deepMerge(cloned, data);
        }
        return c;
      });
    } else if (activeTab === 'story') {
      newStory.storyNodes = story.storyNodes.map(n => n.nodeId === selectedId ? { ...n, ...data } : n);
    } else if (activeTab === 'item') {
      newStory.items = story.items.map(i => i.id === selectedId ? { ...i, ...data } : i);
    } else if (activeTab === 'card') {
      newStory.cards = story.cards.map(c => c.id === selectedId ? { ...c, ...data } : c);
    }
    onApplyFix(newStory);
    alert("Nexus Logic Synchronized.");
  };

  if (!isOpen) return null;

  return (
    <div className="fixed right-4 bottom-20 md:right-8 md:bottom-28 w-[94vw] md:w-[480px] h-[75vh] md:h-[620px] bg-[#050810]/95 backdrop-blur-3xl border-2 border-blue-500/30 rounded-[48px] shadow-[0_40px_100px_rgba(0,0,0,0.8)] overflow-hidden z-[9999] flex flex-col animate-in slide-in-from-bottom-8 duration-500 ease-out">
      <div className="p-6 bg-gradient-to-r from-blue-900/30 to-black/30 border-b border-white/5 flex justify-between items-center shrink-0">
        <div className="flex items-center gap-4">
          <div className="relative">
            <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-[0_0_15px_#10B981]"></div>
            <div className="absolute inset-0 w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping opacity-20"></div>
          </div>
          <div>
            <h3 className="text-[11px] font-black text-blue-400 uppercase tracking-[0.4em] leading-none">Nexus Protocol</h3>
            <p className="text-[8px] text-gray-500 font-black mt-2 uppercase tracking-widest opacity-60">Session Active: {activeTab}</p>
          </div>
        </div>
        <button onClick={onClose} className="w-10 h-10 flex items-center justify-center rounded-full hover:bg-white/10 text-gray-400 hover:text-white transition-all active:scale-90">✕</button>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 flex flex-col gap-6 scroll-smooth scroll-container">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
            <div className={`
              max-w-[85%] p-5 rounded-[28px] text-[13px] leading-relaxed
              ${msg.role === 'user' 
                ? 'bg-blue-600 text-white rounded-tr-none shadow-xl border border-white/10 font-bold' 
                : 'bg-white/5 text-gray-300 border border-white/10 rounded-tl-none font-medium'}
            `}>
              <div className="whitespace-pre-wrap">{msg.content.replace(/FIX_DATA:[\s\S]*/, '').trim()}</div>
              {msg.hasFile && <div className="mt-4 text-[9px] bg-black/40 px-3 py-2 rounded-xl border border-white/5 italic opacity-70">Registry context analyzed by Nexus</div>}
              {msg.suggestionData && (
                <div className="mt-6 pt-6 border-t border-white/10 flex flex-col gap-3">
                   <p className="text-[9px] text-emerald-400 font-black uppercase tracking-[0.2em]">Optimization Signature Found</p>
                   <Button variant="accent" className="h-12 w-full shadow-lg border-2 border-white/10 rounded-2xl font-black text-[10px]" onClick={() => applyFix(msg.suggestionData)}>⚡ APPLY OPTIMIZATIONS</Button>
                </div>
              )}
            </div>
            <span className="text-[8px] text-gray-600 font-black uppercase mt-2.5 px-3 tracking-[0.2em]">{msg.role === 'user' ? 'You' : 'Nexus AI'}</span>
          </div>
        ))}
        {isTyping && (
          <div className="flex flex-col items-start px-3">
            <div className="flex gap-2 items-center bg-white/5 px-5 py-2.5 rounded-full border border-white/5">
              <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce"></div>
              <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce delay-100"></div>
              <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce delay-200"></div>
              <span className="text-[9px] font-black text-blue-500 uppercase tracking-[0.2em] ml-2">Nexus Processing...</span>
            </div>
          </div>
        )}
      </div>

      <div className="p-6 bg-black/40 border-t border-white/5 flex flex-col gap-4 shrink-0 backdrop-blur-2xl">
        {attachedFile && (
            <div className="flex items-center gap-4 bg-blue-600/10 p-4 rounded-2xl border border-blue-500/20 animate-in slide-in-from-bottom-2">
                <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-xl shadow-lg">📄</div>
                <div className="flex-1 truncate text-[10px] font-black text-blue-400 uppercase tracking-widest">{attachedFile.name}</div>
                <button onClick={() => setAttachedFile(null)} className="text-gray-400 hover:text-red-500 transition-colors">✕</button>
            </div>
        )}
        <form onSubmit={sendMessage} className="flex gap-3">
            <input type="file" ref={fileInputRef} onChange={handleFileUpload} className="hidden" accept="image/*, .json" />
            <button type="button" onClick={() => fileInputRef.current?.click()} className="w-14 h-14 bg-white/5 border border-white/10 rounded-[22px] flex items-center justify-center text-2xl text-blue-500 hover:bg-white/10 transition-all hover:scale-105 shadow-inner">+</button>
            <input type="text" value={input} onChange={(e) => setInput(e.target.value)} placeholder="คุยกับระบบเพื่อปรับจูน..." className="flex-1 bg-white/5 border border-white/10 rounded-[22px] px-6 text-[12px] text-white outline-none focus:border-blue-500/50 shadow-inner" />
            <button type="submit" disabled={(!input.trim() && !attachedFile) || isTyping} className="w-14 h-14 bg-blue-600 rounded-[22px] flex items-center justify-center shadow-[0_12px_24px_rgba(37,99,235,0.4)] active:scale-90 disabled:opacity-30 transition-all text-xl">↗️</button>
        </form>
      </div>
    </div>
  );
};
