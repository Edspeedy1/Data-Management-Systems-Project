import React from "react";

export const Spacer: React.FC<React.PropsWithChildren<{
    space?: number;
}>> = ({ space = 0 }) => {
    return <div style={{ height: space }} />;
}