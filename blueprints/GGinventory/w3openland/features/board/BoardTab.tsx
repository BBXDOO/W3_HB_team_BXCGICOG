
import React, { useState, useMemo, useEffect, useRef } from 'react';
import { StoryPack, BoardPack, CellPack, Asset } from '../../types';
import { Button } from '../../ui/components/Button';
import { Input, TextArea, Select } from '../../ui/components/Input';
import { MonitorCore } from '../../ui/components/MonitorCore';
import { SplitLayout60_40 } from '../../ui/layout/SplitLayout60_40';
import { generateId } from '../../core/utils';
import { Card } from '../../ui/components/Card';
import { Modal } from '../../ui/components/Modal';

interface BoardTabProps {
  story: StoryPack;
  onChange: (updated: StoryPack) => void;
  toolActions?: any;
}

const PRESET_COLORS = [
  '#EF4444', '#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899', '#F8FAFC', '#1e293b'
];

const PRESET_ICONS = [
  '🏰', '⚔️', '🛡️', '💎', '💀', '🗝️', '📜', '🌋', '⛺', '🌳', '🏠', '✨', '🌊', '🌾', '🔥', '🌀'
];

export const BoardTab: React.FC<BoardTabProps> = ({ story, onChange, toolActions }) => {
  const [selectedBoardId, setSelectedBoardId] = useState<string | null>(story.boards[0]?.boardId || null);
  const [selectedKey, setSelectedKey] = useState<string | null>(null);
  const [isColorPickerOpen, setIsColorPickerOpen] = useState(false);
  const [tempColor, setTempColor] = useState<string>('#3B82F6');
  const [tempIcon, setTempIcon] = useState<string>('🏰');
  const [zoom, setZoom] = useState(48); 
  
  const [wInput, setWInput] = useState('12');
  const [hInput, setHInput] = useState('12');

  const customColorInputRef = useRef<HTMLInputElement>(null);

  const activeBoard = useMemo(() => 
    story.boards.find(b => b.boardId === selectedBoardId)
  , [story.boards, selectedBoardId]);

  useEffect(() => {
    if (activeBoard) {
      setWInput(activeBoard.width.toString());
      setHInput(activeBoard.height.toString());
    }
  }, [selectedBoardId]);

  const getCell = (x: number, y: number): CellPack => {
    const key = `${x}_${y}`;
    return activeBoard?.cellMap[key] || { x, y, type: 'Empty' };
  };

  const selectedCell = useMemo(() => {
    if (!selectedKey || !activeBoard) return null;
    const [x, y] = selectedKey.split('_').map(Number);
    return getCell(x, y);
  }, [selectedKey, activeBoard]);

  const addBoard = () => {
    const id = generateId('brd');
    const b: BoardPack = { 
      boardId: id, title: 'NEW ECOSYSTEM AREA', width: 12, height: 12, cellMap: {}, 
      explored: {}, visionRangeDefault: 2, movementPerTurnDefault: 2 
    };
    onChange({ ...story, boards: [...story.boards, b] });
    setSelectedBoardId(id);
    setSelectedKey(null);
  };

  const updateCell = (x: number, y: number, updated: Partial<CellPack>) => {
    if (!activeBoard) return;
    const key = `${x}_${y}`;
    const nextMap = { ...activeBoard.cellMap };
    nextMap[key] = { ...getCell(x, y), ...updated };
    
    const updatedBoards = story.boards.map(b => 
      b.boardId === activeBoard.boardId ? { ...b, cellMap: nextMap } : b
    );
    onChange({ ...story, boards: updatedBoards });
  };

  const handleResize = () => {
    if (!activeBoard) return;
    const w = Math.min(50, Math.max(1, parseInt(wInput) || 12));
    const h = Math.min(50, Math.max(1, parseInt(hInput) || 12));
    
    const updatedBoards = story.boards.map(b => 
      b.boardId === activeBoard.boardId ? { ...b, width: w, height: h } : b
    );
    setSelectedKey(null);
    onChange({ ...story, boards: updatedBoards });
    alert(`ปรับขนาดอาณาจักรเป็น ${w}x${h} แล้วครับ`);
  };

  const handleOpenColorPicker = () => {
    if (!selectedCell) return;
    setTempColor(selectedCell.markerColor || '#3B82F6');
    setTempIcon(selectedCell.markerIcon || '');
    setIsColorPickerOpen(true);
  };

  const handleConfirmColor = () => {
    if (selectedCell) {
      updateCell(selectedCell.x, selectedCell.y, { 
        markerColor: tempColor,
        markerIcon: tempIcon
      });
    }
    setIsColorPickerOpen(false);
  };

  return (
    <>
      <SplitLayout60_40
        toolActions={toolActions}
        topLeft={
          <div className="p-4 flex flex-col gap-6 bg-[var(--surface-2)] h-full overflow-y-auto w-full scroll-container pb-20">
            <Button variant="accent" onClick={addBoard} className="h-14 text-[10px] font-black border-2 border-white/10 shadow-xl rounded-[24px] active:scale-95 transition-all">
              + สร้างพื้นที่อาณาจักรใหม่
            </Button>
            
            <div className="flex flex-col gap-2">
               <label className="text-[9px] text-gray-500 font-black uppercase tracking-widest px-1">เลือกพื้นที่ที่ต้องการแก้ไข</label>
               <Select 
                  value={selectedBoardId || ''} 
                  options={[{label:'--- เลือกพื้นที่ ---', value:''}, ...story.boards.map(b => ({ label: b.title, value: b.boardId }))]} 
                  onChange={id => setSelectedBoardId(id)}
                  className="h-12"
                />
            </div>

            {activeBoard && (
              <div className="flex flex-col gap-4 mt-2 border-t border-white/5 pt-6 animate-in fade-in slide-in-from-left-2">
                <Input label="ชื่อพื้นที่/อาณาจักร" value={activeBoard.title} onChange={v => onChange({...story, boards: story.boards.map(b => b.boardId === activeBoard.boardId ? {...b, title: v} : b)})} />
                <div className="grid grid-cols-2 gap-4">
                  <Input label="Width (Cells)" type="number" value={wInput} onChange={setWInput} />
                  <Input label="Height (Cells)" type="number" value={hInput} onChange={setHInput} />
                </div>
                <Button variant="primary" className="h-12 text-[10px] font-black rounded-xl border border-white/10 shadow-lg" onClick={handleResize}>
                  อัปเดตขนาดตาราง
                </Button>
                <Button variant="danger" className="h-10 text-[9px] mt-4 opacity-50 hover:opacity-100" onClick={() => {
                   if(confirm('ลบพื้นที่นี้ใช่หรือไม่?')) {
                     onChange({...story, boards: story.boards.filter(b => b.boardId !== activeBoard.boardId)});
                     setSelectedBoardId(story.boards.find(b => b.boardId !== activeBoard.boardId)?.boardId || null);
                   }
                }}>ลบพื้นที่นี้</Button>
              </div>
            )}
          </div>
        }
        topRight={
          <div className="p-4 flex flex-col gap-6 overflow-y-auto h-full w-full bg-[var(--surface)] scroll-container pb-24">
            {selectedCell ? (
              <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-right-4 duration-300">
                 <div className="flex justify-between items-center px-1">
                    <h3 className="text-[10px] font-black text-blue-500 uppercase tracking-[0.3em]">Coordinate Trace: {selectedCell.x}, {selectedCell.y}</h3>
                 </div>
                 <Card className="p-6 flex flex-col gap-6 bg-[var(--surface-2)] border-white/5 rounded-[40px] shadow-2xl relative overflow-hidden">
                    <div className="grid grid-cols-2 gap-5">
                      <Select label="Entity Type" value={selectedCell.type || 'Empty'} options={[{label:'Empty Cell',value:'Empty'},{label:'Location Hub',value:'Location'},{label:'Encounter Point',value:'Encounter'},{label:'Neutral Zone',value:'SafeZone'}]} onChange={v => updateCell(selectedCell.x, selectedCell.y, {type:v as any})} />
                      <div className="flex flex-col gap-1">
                         <label className="text-[9px] text-gray-500 font-black px-1 uppercase tracking-widest">Visual Skin</label>
                         <button 
                           onClick={handleOpenColorPicker} 
                           className="h-14 w-full rounded-[20px] border-2 flex items-center justify-center transition-all shadow-xl active:scale-90 group relative overflow-hidden" 
                           style={{ 
                             backgroundColor: selectedCell.markerColor || '#1e293b',
                             borderColor: 'rgba(255,255,255,0.1)'
                           }}
                         >
                           <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                           <span className="text-3xl drop-shadow-lg select-none relative z-10">
                            {selectedCell.markerIcon || (
                                selectedCell.type === 'Location' ? '🏰' : 
                                selectedCell.type === 'Encounter' ? '⚔️' : 
                                selectedCell.type === 'SafeZone' ? '🛡️' : '🎨'
                            )}
                           </span>
                         </button>
                      </div>
                    </div>
                    <Input label="Display Label" placeholder="ชื่อเรียกพิกัดนี้..." value={selectedCell.name || ''} onChange={v => updateCell(selectedCell.x, selectedCell.y, {name:v})} />
                    <TextArea label="Atmospheric Log" className="text-[11px] min-h-[140px]" value={selectedCell.desc || ''} onChange={v => updateCell(selectedCell.x, selectedCell.y, {desc:v})} />
                 </Card>
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center opacity-20 text-center py-20">
                 <div className="text-7xl mb-6">🎯</div>
                 <p className="text-[12px] font-black uppercase tracking-[0.4em] leading-relaxed">เลือกช่องพิกัดบนแผนที่<br/>เพื่อเริ่มกำหนดรายละเอียดครับ</p>
              </div>
            )}
          </div>
        }
        bottomMain={
          <MonitorCore title="WORLD GRID NAVIGATOR" modeLabel="RENDER_V0.5" isEmpty={!activeBoard}>
            {activeBoard && (
              <div className="flex-1 flex flex-col items-center gap-8 py-10 h-full overflow-hidden">
                <div className="relative overflow-auto max-w-full w-full w3-card-inset border-2 border-white/5 rounded-[48px] p-8 md:p-20 bg-[#050810] shadow-[inset_0_0_100px_rgba(0,0,0,1)] scroll-container h-full flex items-center justify-center">
                  <div className="inline-block" key={`grid-brd-${activeBoard.boardId}-${activeBoard.width}-${activeBoard.height}`}>
                    <div 
                      className="grid shadow-[0_40px_100px_rgba(0,0,0,0.8)] transition-all bg-white/5" 
                      style={{ 
                        gridTemplateColumns: `repeat(${activeBoard.width}, ${zoom}px)`,
                        gap: '1px' 
                      }}
                    >
                      {Array.from({ length: activeBoard.height * activeBoard.width }).map((_, i) => {
                          const x = i % activeBoard.width;
                          const y = Math.floor(i / activeBoard.width);
                          const key = `${x}_${y}`;
                          const cell = getCell(x, y);
                          const isSelected = selectedKey === key;
                          
                          const cellBgColor = isSelected ? (cell.markerColor || '#3B82F6') : (cell.markerColor || '#0B1220');

                          return (
                            <div 
                              key={key} 
                              onClick={() => setSelectedKey(key)} 
                              className={`
                                flex items-center justify-center transition-all cursor-pointer relative
                                ${isSelected ? 'z-20 scale-125 shadow-2xl ring-2 ring-white/50' : 'hover:brightness-150 border border-white/5'}
                              `} 
                              style={{ 
                                width: `${zoom}px`, 
                                height: `${zoom}px`, 
                                fontSize: `${zoom * 0.6}px`, 
                                backgroundColor: cellBgColor
                              }}
                            >
                              <span className="drop-shadow-lg select-none relative z-10 transition-transform hover:scale-110">
                                {cell.markerIcon !== undefined && cell.markerIcon !== '' ? cell.markerIcon : (
                                  cell.markerIcon === '' ? '' : (
                                    cell.type === 'Location' ? '🏰' : 
                                    cell.type === 'Encounter' ? '⚔️' : 
                                    cell.type === 'SafeZone' ? '🛡️' : ''
                                  )
                                )}
                              </span>
                              
                              {isSelected && (
                                <div className="absolute inset-0 bg-white/10 animate-pulse z-0" />
                              )}
                            </div>
                          );
                      })}
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center gap-6 w-full max-w-md bg-black/80 px-10 py-5 rounded-full border border-white/10 shadow-2xl backdrop-blur-2xl">
                   <span className="text-[10px] font-black text-gray-500 uppercase tracking-widest shrink-0">Scale:</span>
                   <input 
                     type="range" min="24" max="140" value={zoom} 
                     onChange={(e) => setZoom(parseInt(e.target.value))} 
                     className="flex-1 h-1.5 bg-gray-800 rounded-full appearance-none accent-blue-600 cursor-pointer" 
                   />
                   <span className="text-[11px] font-mono font-black text-blue-500 w-12 text-right">{zoom}px</span>
                </div>
              </div>
            )}
          </MonitorCore>
        }
      />

      <Modal 
        isOpen={isColorPickerOpen} 
        title="Cell Skin Configuration" 
        onClose={() => setIsColorPickerOpen(false)} 
        footer={
          <div className="flex gap-4 w-full">
            <Button variant="secondary" className="flex-1 h-16 rounded-[28px] font-black uppercase text-[11px]" onClick={() => setIsColorPickerOpen(false)}>ยกเลิก</Button>
            <Button variant="accent" className="flex-1 h-16 rounded-[28px] font-black uppercase text-[11px] shadow-2xl border-2 border-white/20" onClick={handleConfirmColor}>ยืนยันการเปลี่ยนแปลง</Button>
          </div>
        }
      >
        <div className="flex flex-col gap-10 py-4 scroll-container overflow-y-auto max-h-[60vh]">
          {/* ICON SELECTOR */}
          <div className="flex flex-col gap-4">
            <label className="text-[10px] font-black text-blue-500 uppercase px-1 tracking-[0.4em]">Signature Icon</label>
            <div className="grid grid-cols-5 gap-3 p-6 bg-black/40 rounded-[32px] border border-white/5">
              {/* CLEAR ICON BUTTON - AS REQUESTED BY USER SKETCH */}
              <button 
                onClick={() => setTempIcon('')} 
                className={`aspect-square rounded-[20px] bg-red-600/10 border-2 transition-all flex items-center justify-center text-2xl active:scale-90 ${tempIcon === '' ? 'border-red-500 shadow-xl scale-110 bg-red-600/20' : 'border-white/5 opacity-40 hover:opacity-100'}`}
                title="ไม่แสดง Icon (ใส)"
              >
                ❌
              </button>

              {PRESET_ICONS.map((icon, i) => (
                <button 
                  key={i} 
                  onClick={() => setTempIcon(icon)} 
                  className={`aspect-square rounded-[20px] bg-[var(--surface)] border-2 transition-all flex items-center justify-center text-2xl active:scale-90 ${tempIcon === icon ? 'border-blue-500 bg-blue-500/20 shadow-xl scale-110' : 'border-white/5 opacity-40 hover:opacity-100'}`}
                >
                  {icon}
                </button>
              ))}
            </div>
          </div>

          {/* COLOR SELECTOR (PRESETS) */}
          <div className="flex flex-col gap-4">
            <label className="text-[10px] font-black text-blue-500 uppercase px-1 tracking-[0.4em]">Color Tint</label>
            <div className="grid grid-cols-8 gap-3 p-6 bg-black/40 rounded-[32px] border border-white/5">
              {PRESET_COLORS.map((c, i) => (
                <button 
                  key={i} 
                  onClick={() => setTempColor(c)} 
                  className={`aspect-square rounded-xl border-[4px] transition-all active:scale-90 ${tempColor === c ? 'border-white scale-110 shadow-xl' : 'border-transparent opacity-60'}`} 
                  style={{ backgroundColor: c }} 
                />
              ))}
            </div>
          </div>

          {/* CUSTOM COLOR SELECTOR */}
          <div className="flex flex-col gap-4">
             <div className="flex items-center justify-between px-1">
                <label className="text-[10px] font-black text-gray-500 uppercase tracking-[0.4em]">Custom Palette</label>
                <div className="text-[11px] font-mono text-blue-500 font-black tracking-tighter">{tempColor.toUpperCase()}</div>
             </div>
             
             <div className="flex items-center gap-6 bg-black/60 p-6 rounded-[40px] border border-white/5 shadow-inner">
                <button 
                  onClick={() => customColorInputRef.current?.click()}
                  className="flex-1 h-28 bg-[var(--surface-2)] rounded-[32px] border-2 border-dashed border-white/10 flex flex-col items-center justify-center gap-2 hover:bg-white/5 transition-all group active:scale-95"
                >
                  <span className="text-4xl group-hover:rotate-12 transition-transform">🎨</span>
                  <span className="text-[9px] font-black text-white/40 uppercase tracking-widest">Open Color Picker</span>
                  <input 
                    type="color" 
                    ref={customColorInputRef}
                    className="hidden" 
                    value={tempColor} 
                    onChange={(e) => setTempColor(e.target.value)} 
                  />
                </button>

                <div className="flex flex-col items-center gap-3">
                   <div 
                      className="w-24 h-24 rounded-full border-[6px] border-white shadow-2xl transition-all duration-500"
                      style={{ backgroundColor: tempColor }}
                   />
                   <span className="text-[8px] font-black text-white/20 uppercase">PREVIEW</span>
                </div>
             </div>
          </div>
        </div>
      </Modal>
    </>
  );
};
