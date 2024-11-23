import React from "react";

export const RepoCard: React.FC<React.PropsWithChildren<{
    name?: string;
    description?: string;
    url?: string;
}>> = ({ name, description, url }) => {
    return (
        <div className="border-light border-4 p-4 mb-4 mt-4 w-full rounded-xl flex flex-row justify-between items-center cursor-pointer" onClick={() => {
            if (!url) return;
            window.location.href = url;
        }}>
            {name && <h2 className="font-bold text-lg">{name}</h2>}
            {description && <p className="text-sm text-light">{description}</p>}
        </div>
    );
};