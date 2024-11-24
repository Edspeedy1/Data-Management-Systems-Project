import React, { useEffect, useState } from "react";
import { ToggleSlider } from "react-toggle-slider";

export const ToggleBox: React.FC<React.PropsWithChildren<{ api?: string }>> = ({
    children,
    api,
}) => {
    const [isOpen, setIsOpen] = useState(false);
    const [loading, setLoading] = useState(true); // Add a loading state

    const changed = (newState: boolean) => {
        if (api) {
            fetch('/api/' + api, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    repoID: window.location.pathname.split("/")[2],
                    isPublic: newState,
                    get: false,
                }),
            })
                .then((response) => response.json())
                .then((data) => {
                    console.log("Server response:", data);
                    // Optionally synchronize the toggle state with the server response
                })
                .catch((error) => {
                    console.error("Error updating state:", error);
                });
        }
    };

    useEffect(() => {
        if (api === "repoPublic") {
            fetch('/api/repoPublic', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    repoID: window.location.pathname.split("/")[2],
                    isPublic: isOpen,
                    get: true,
                }),
            })
                .then((response) => response.json())
                .then((data) => {
                    console.log("Initial state from server:", data);
                    setIsOpen(data.isPublic); // Synchronize state with the server
                })
                .catch((error) => {
                    console.error("Error fetching initial state:", error);
                })
                .finally(() => {
                    setLoading(false); // Mark loading as complete
                });
        }
    }, [api]);

    const toggle = () => {
        const newState = !isOpen;
        setIsOpen(newState); // Update state locally
        changed(newState); // Sync with the server
    };

    if (loading) {
        return <div>Loading...</div>; // Optionally render a loader
    }

    return (
        <div
            className="flex flex-row items-center justify-between w-full cursor-pointer pl-4 pr-4 mt-2"
            onClick={toggle}
        >
            {children}
            <ToggleSlider active={isOpen} />
        </div>
    );
};
