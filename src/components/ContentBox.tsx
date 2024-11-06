import React from 'react';

const colorClasses: Record<string, string> = {
    secondary: 'bg-secondary',
    black: 'bg-black',
    dark: 'bg-dark',
    light: 'bg-light',
};

export const ContentBox: React.FC<React.PropsWithChildren<{
    bgColor?: string;
    hasBorder?: boolean;
}>> = ({ children, bgColor, hasBorder }) => {
    const bgClass = colorClasses[bgColor ?? ''] || '';

    if (hasBorder) {
        return (
            <div className={`text-center h-fit w-fit border-border border-2 p-2 ${bgClass}`}>
                {children}
            </div>
        );
    }

    return (
        <div className={`text-center h-fit w-fit border-none p-2 ${bgClass}`}>
            {children}
        </div>
    );
};
