import React, { useState, useEffect } from 'react';

export const MouseBubble: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

    // Track mouse movement
    useEffect(() => {
        const handleMouseMove = (event: MouseEvent) => {
            setMousePosition({ x: event.clientX, y: event.clientY });
        };

        const handleTouchMove = (event: TouchEvent) => {
            const touch = event.touches[0]; // Get the first touch point
            setMousePosition({ x: touch.clientX, y: touch.clientY });
        };

        window.addEventListener('mousemove', handleMouseMove);
        window.addEventListener('touchmove', handleTouchMove);

        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('touchmove', handleTouchMove);
        };
    }, []);

    return (
        <div className="relative">
            {/* Background effect */}
            <div
                className="fixed inset-0 backdrop-blur-lg w-[100vw] h-[100vh] top-0 left-0"
                style={{
                    maskImage: `radial-gradient(circle at ${mousePosition.x}px ${mousePosition.y}px, transparent 180px, black 350px)`,
                    WebkitMaskImage: `radial-gradient(circle at ${mousePosition.x}px ${mousePosition.y}px, transparent 180px, black 350px)`,
                    pointerEvents: 'none', // This ensures the mask effect doesn't block interaction with children
                }}
            ></div>

            {/* Content (children) */}
            <div className="relative z-10">
                {children}
            </div>
        </div>
    );
};
