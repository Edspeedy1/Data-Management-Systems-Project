import React from 'react';

export const BlurOverlay: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
    return (
        <div className="absolute inset-4 backdrop-blur-lg flex items-center justify-center">
            {children}
        </div>
    );
};
