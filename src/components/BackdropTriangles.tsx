import React, { useEffect, useRef } from "react";

export const BackdropTriangles: React.FC = () => {
    const canvasRef = useRef<HTMLCanvasElement | null>(null);
    const triangleSize = 120;
    const height = Math.sqrt(3) / 2 * triangleSize;

    // Define colors to transition between
    const color1 = "#8c3800";
    const color2 = "#773100";

    // Function to interpolate between two colors
    const interpolateColor = (color1: string, color2: string, factor: number) => {
        const c1 = parseInt(color1.slice(1), 16);
        const c2 = parseInt(color2.slice(1), 16);
        const r = Math.round(((c1 >> 16) * (1 - factor)) + ((c2 >> 16) * factor));
        const g = Math.round((((c1 >> 8) & 0x00ff) * (1 - factor)) + (((c2 >> 8) & 0x00ff) * factor));
        const b = Math.round(((c1 & 0x0000ff) * (1 - factor)) + ((c2 & 0x0000ff) * factor));
        return `#${(r << 16 | g << 8 | b).toString(16).padStart(6, '0')}`;
    };

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        // Store triangle data
        const triangles = [] as { x: number, y: number, flip: boolean, color: string, targetColor: string, transitionFactor: number }[];
        var ix = 0;
        var iy = 0;
        for (let y = -triangleSize; y < canvas.height; y += height) {
            iy += 1;
            for (let x = -triangleSize; x < canvas.width; x += triangleSize / 2) {
                ix += 1;
                const flip = (ix + iy) % 2 === 0;
                triangles.push({
                    x,
                    y,
                    flip: flip,
                    color: Math.random() > 0.5 ? color1 : color2,
                    targetColor: Math.random() > 0.5 ? color1 : color2,
                    transitionFactor: Math.random(), // a random number between 0 and 1
                });
            }
        }

        // Draws a single triangle
        const drawTriangle = (x: number, y: number, color: string, flip: boolean) => {
            ctx.beginPath();
            if (flip) {
                ctx.moveTo(x, y);
                ctx.lineTo(x + triangleSize, y);
                ctx.lineTo(x + triangleSize / 2, y + height);
            } else {
                ctx.moveTo(x + triangleSize / 2, y);
                ctx.lineTo(x, y + height);
                ctx.lineTo(x + triangleSize, y + height);
            }
            ctx.closePath();
            ctx.fillStyle = color;
            ctx.fill();
        };

        // Update and redraw triangles with smooth color transitions
        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            triangles.forEach((triangle) => {
                // Gradually increase transition factor for smooth color change
                triangle.transitionFactor += 0.005;
                if (triangle.transitionFactor >= 1) {
                    triangle.transitionFactor = 0;
                    triangle.color = triangle.targetColor;
                    triangle.targetColor = triangle.targetColor === color1 ? color2 : color1;
                }
                const currentColor = interpolateColor(triangle.color, triangle.targetColor, triangle.transitionFactor);
                drawTriangle(triangle.x, triangle.y, currentColor, triangle.flip);
            });

            requestAnimationFrame(animate);
        };

        // Start animation
        animate();

        // Update canvas dimensions and redraw triangles on resize
        const handleResize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        
        window.addEventListener("resize", handleResize);

        return () => {
            window.removeEventListener("resize", handleResize);
        };
    }, [triangleSize, height, color1, color2]);

    return <canvas ref={canvasRef} width="600" height="600" style={{position: 'absolute', top: 0, left: 0, zIndex: 1}}></canvas>;
};
