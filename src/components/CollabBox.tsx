import React, { useState, useEffect } from "react";

export const CollabBox: React.FC = () => {
    const [isLoading, setIsLoading] = useState(true);
    const [collabs, setCollabs] = useState<Record<string, any>[]>([]);
    const repoName = window.location.pathname.split("/")[2]; // from the url

    useEffect(() => {
        const controller = new AbortController();
        fetch('/api/getCollab', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ repoID: repoName }),
            signal: controller.signal
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                // Update the state with the server response
                setCollabs(data.collabs || []);
            })
            .catch((error) => {
                console.error("Error fetching repos:", error);
            })
            .finally(() => {
                setIsLoading(false);
            });

        return () => {
            controller.abort("unmounted"); // Abort the fetch request on component unmount
        }
    }, []);
    
    return (
        <div className="w-[100%]justify-center h-[30%] pl-2">
            <input className="w-[100%] bg-white pl-1 rounded-md"
                type="text"
                placeholder="Search"/>
            <div className="w-[100%] h-[calc(100%-30px)] bg-dark">
                <div>{isLoading ? "Loading..." : "Collaborators"}</div>
                <div className="h-[calc(100%-30px)] overflow-y-scroll" style={{
                    scrollbarWidth: "thin",
                    scrollbarColor: "#888 #333",
                }}>
                    cob
                </div>
            </div>
        </div>
    );
};