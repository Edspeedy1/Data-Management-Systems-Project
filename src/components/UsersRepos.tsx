import React, { useEffect, useState } from "react";
import { RepoCard } from "../components/RepoCard";

export const UsersRepos: React.FC = () => {
    // State to hold the fetched repos
    const [repos, setRepos] = useState<
        { name: string; description: string; url: string }[]
    >([]);
    const [isLoading, setIsLoading] = useState(true);

    // Fetch data from the server on component mount
    useEffect(() => {
        const controller = new AbortController();
        fetch('/api/getUsersRepos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: "" }),
            signal: controller.signal
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                // Update the state with the server response
                setRepos(data.repos || []);
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
    }, []); // Empty dependency array means this runs once on mount

    // Render RepoCard for each item in repos
    return (
        <div className="text-center w-full h-[calc(100vh-200px)] overflow-y-scroll" style={{
            scrollbarWidth: "thin",
            scrollbarColor: "#888 #333",
        }}>
            {isLoading ? (
                <p className="animate-pulse mt-10">Loading repositories...</p>
            ) : repos.length > 0 ? (
                repos.map((repo, index) => (
                    <RepoCard
                        key={index}
                        name={repo.name}
                        description={repo.description}
                        url={repo.url}
                    />
                ))
            ) : (
                <p className="mt-10">No repositories found.</p>
            )}
        </div>
    );
};
