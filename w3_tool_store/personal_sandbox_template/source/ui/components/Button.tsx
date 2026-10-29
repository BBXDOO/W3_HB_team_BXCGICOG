
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
  const baseClasses = 'ps-button px-5 py-2.5 flex items-center justify-center gap-2 font-black transition-all active:scale-95 disabled:opacity-30 disabled:cursor-not-allowed text-[10px] uppercase tracking-[0.12em] rounded-xl clickable';
  
  let variantClasses = '';
  // Reference Image: Primary (Orange)
  if (variant === 'accent' || variant === 'primary') {
    variantClasses = 'ps-button-primary bg-[#a277f4] text-[#0b0912] hover:bg-[#bb99ff] border border-white/10';
  }
  // Reference Image: Secondary (Green)
  else if (variant === 'secondary') {
    variantClasses = 'ps-button-secondary bg-[#292239] text-[#e3d1ff] hover:bg-[#392b50] border border-[#a277f4]/30';
  }
  else if (variant === 'danger') {
    variantClasses = 'bg-[#3c1d22] text-[#ff897a] border border-[#f24d35]/30 hover:bg-[#4a2328]';
  }
  else if (variant === 'ghost') {
    variantClasses = 'bg-transparent text-[#bdb5cb] hover:text-white shadow-none hover:bg-white/5';
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
