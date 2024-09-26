import React from 'react'

interface BadgeProps {
  children: React.ReactNode
  variant?: 'default' | 'secondary'
}

export function Badge({ children, variant = 'default' }: BadgeProps) {
  const baseClasses = 'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold'
  const variantClasses = variant === 'secondary' 
    ? 'bg-secondary text-secondary-foreground' 
    : 'bg-primary text-primary-foreground'

  return (
    <span className={`${baseClasses} ${variantClasses}`}>
      {children}
    </span>
  )
}