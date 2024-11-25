import React, { useState, useEffect } from "react";

export const RepoFiles: React.FC<React.PropsWithChildren<{
    sharedState: boolean
}>> = (sharedState) => {
    const [isLoading, setIsLoading] = useState(true);
    const [files, setFiles] = useState<{ name: string }[]>([]);
    const repoName = window.location.pathname.split("/")[2]; // from the url

    useEffect(() => {
        const controller = new AbortController();
        fetch('/api/getFileNames', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ repoID: repoName }),
            signal: controller.signal
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("fileNames",data);
                // Update the state with the server response
                setFiles(data.fileNames || []);
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
    }, [sharedState]);

    return (
        <div className="flex flex-wrap gap-2 w-full h-full justify-center">
            {isLoading ? (
                <p className="animate-pulse">Loading...</p>
            ) : (
                files.map((file, index) => (
                    <div key={index} className="bg-dark w-32 h-32 flex items-center justify-center rounded">
                        <a href={`../api/download/${repoName}/${file.name}`} download>
                            {file.name}
                        </a>
                    </div>
                ))
            )}
        </div>
    );    
};