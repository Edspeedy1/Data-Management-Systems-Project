import React, { ReactNode } from 'react';

type SplitProps = {
    left: ReactNode;
    right: ReactNode;
};

export const SplitVertical: React.FC<SplitProps> = ({ left, right }) => {
    return (
        <div className="flex flex-row w-full h-full gap-16">
            {left}
            {right}
        </div>
    );
};
