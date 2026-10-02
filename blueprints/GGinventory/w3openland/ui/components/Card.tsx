
import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  inset?: boolean;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({ children, className = '', inset = false, onClick }) => {
  return (
    <div 
      className={`${inset ? 'tactile-inset' : 'tactile-raised'} ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  );
};
