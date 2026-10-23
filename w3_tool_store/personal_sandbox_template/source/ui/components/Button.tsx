
import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
  variant?: 'primary' | 'secondary' | 'accent' | 'danger' | 'ghost';
  disabled?: boolean;
  title?: string;
}

export const Button: React.FC<ButtonProps> = ({ 
  children, 
  onClick, 
  className = '', 
  variant = 'secondary', 
  disabled,
  title
}) => {
  const baseClasses = 'px-5 py-2.5 flex items-center justify-center gap-2 font-black transition-all active:scale-95 disabled:opacity-30 disabled:cursor-not-allowed text-[10px] uppercase tracking-[0.2em] rounded-2xl clickable';
  
  let variantClasses = '';
  // Reference Image: Primary (Orange)
  if (variant === 'accent' || variant === 'primary') {
    variantClasses = 'bg-[#c2410c] text-white shadow-[-2px_-2px_6px_rgba(255,255,255,0.05),4px 4px 10px rgba(0,0,0,0.4)] hover:bg-[#ea580c] border border-white/5';
  }
  // Reference Image: Secondary (Green)
  else if (variant === 'secondary') {
    variantClasses = 'bg-[#15803d] text-white shadow-[-2px_-2px_6px_rgba(255,255,255,0.05),4px 4px 10px rgba(0,0,0,0.4)] hover:bg-[#16a34a] border border-white/5';
  }
  else if (variant === 'danger') {
    variantClasses = 'bg-red-900/40 text-red-400 border border-red-500/20 shadow-inner hover:bg-red-900/60';
  }
  else if (variant === 'ghost') {
    variantClasses = 'bg-transparent text-gray-500 hover:text-white shadow-none hover:bg-white/5';
  }
  // Default/Subtle
  else {
    variantClasses = 'bg-[#27272a] text-gray-300 shadow-[-2px_-2px_6px_rgba(255,255,255,0.05),4px 4px 10px rgba(0,0,0,0.4)] hover:bg-[#3f3f46] border border-white/5';
  }

  return (
    <button 
      title={title}
      className={`${baseClasses} ${variantClasses} ${className}`} 
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};
