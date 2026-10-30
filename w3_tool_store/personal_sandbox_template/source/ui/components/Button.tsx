
import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
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
  title,
  ...buttonProps
}) => {
  const baseClasses = 'ps-button px-5 py-2.5 flex items-center justify-center gap-2 font-black transition-all active:scale-95 disabled:opacity-30 disabled:cursor-not-allowed text-[10px] uppercase tracking-[0.12em] rounded-xl clickable';
  
  const variantClasses = {
    primary: 'ps-button-primary', accent: 'ps-button-primary',
    secondary: 'ps-button-secondary', danger: 'ps-button-danger', ghost: 'ps-button-ghost'
  }[variant];

  return (
    <button
      type="button"
      {...buttonProps}
      title={title}
      className={`${baseClasses} ${variantClasses} ${className}`} 
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};
