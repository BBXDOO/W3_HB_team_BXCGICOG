
import React from 'react';
import { useContentFormat } from '../../features/editor/ContentFormat';

interface InputProps {
  label?: string;
  value: string | number;
  onChange: (val: string) => void;
  placeholder?: string;
  type?: string;
  className?: string;
  richText?: boolean;
}

export const Input: React.FC<InputProps> = ({ label, value, onChange, placeholder, type = 'text', className = '' }) => {
  return (
    <div className={`flex flex-col gap-1.5 ${className}`}>
      {label && <label className="text-[10px] text-zinc-200 font-bold px-2 uppercase tracking-[0.2em]">{label}</label>}
      <div className="tactile-inset overflow-hidden">
        <input
          type={type}
          value={value ?? ''}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="px-4 py-3 text-[11px] outline-none bg-transparent text-white font-bold w-full placeholder:text-zinc-600"
        />
      </div>
    </div>
  );
};

export const TextArea: React.FC<InputProps> = ({ label, value, onChange, placeholder, className = '', richText = false }) => {
  const format = useContentFormat();
  const remember = (element: HTMLTextAreaElement) => {
    if (richText) format?.select({ element, start: element.selectionStart, end: element.selectionEnd, value: String(value ?? ''), onChange, label: label || 'เนื้อหา' });
  };
  return (
    <div className={`flex flex-col gap-1.5 ${className}`}>
      {label && <label className="text-[10px] text-zinc-200 font-bold px-2 uppercase tracking-[0.2em]">{label}</label>}
      <div className="tactile-inset overflow-hidden">
        <textarea
          value={value ?? ''}
          onChange={(e) => { onChange(e.target.value); if (richText) format?.select({ element: e.target, start: e.target.selectionStart, end: e.target.selectionEnd, value: e.target.value, onChange, label: label || 'เนื้อหา' }); }}
          onFocus={(e) => remember(e.currentTarget)}
          onSelect={(e) => remember(e.currentTarget)}
          placeholder={placeholder}
          rows={4}
          className="px-4 py-3 text-[11px] outline-none bg-transparent text-white font-medium leading-relaxed resize-none w-full placeholder:text-zinc-600"
        />
      </div>
    </div>
  );
};

export const Select: React.FC<{
  label?: string;
  value: string;
  options: { label: string; value: string }[];
  onChange: (val: string) => void;
  className?: string;
}> = ({ label, value, options, onChange, className = '' }) => {
  return (
    <div className={`flex flex-col gap-1.5 ${className}`}>
      {label && <label className="text-[10px] text-zinc-200 font-bold px-2 uppercase tracking-[0.2em]">{label}</label>}
      <div className="tactile-inset relative overflow-hidden">
        <select
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="px-4 py-3 text-[11px] outline-none bg-transparent text-white font-bold appearance-none w-full cursor-pointer"
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value} className="bg-[#1c1c1f] text-white">{opt.label}</option>
          ))}
        </select>
        <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-zinc-300 text-[10px]">▼</div>
      </div>
    </div>
  );
};
