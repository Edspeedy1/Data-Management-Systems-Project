import React, { useState } from "react";
import { ToggleSlider }  from "react-toggle-slider";

export const ToggleBox: React.FC<React.PropsWithChildren<{
    api?: string;
}>> = ({ children, api }) => {
    const [isOpen, setIsOpen] = useState(false);

    const changed = () => {
        if (api) {
            fetch('/api/' + api, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ value: isOpen }),
            })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    // Update the state with the server response
                })
                .catch((error) => {
                    console.error("Error fetching repos:", error);
                })
        }
    };

    return (
        <div className="flex flex-row items-center justify-between w-full cursor-pointer pl-4 pr-4 mt-2" onClick={() => {changed();setIsOpen(!isOpen)}}>
            {children}
            <ToggleSlider active={isOpen} />
        </div>
    );
};