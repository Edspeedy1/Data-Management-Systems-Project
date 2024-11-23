import React, { ReactNode } from 'react';

type SplitProps = {
    left: ReactNode;
    right: ReactNode;
};

export const SplitVertical: React.FC<SplitProps> = ({ left, right }) => {
    return (
        <div className="flex flex-col sm:flex-row w-full gap-16 justify-around">
            {left}
            {right}
        </div>
    );
};
