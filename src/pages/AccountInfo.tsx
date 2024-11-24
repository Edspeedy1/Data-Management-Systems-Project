import React, { useState } from "react";
import { Header } from "../components/Header";
import { BackdropTriangles } from "../components/BackdropTriangles";
import { ContentBox } from "../components/ContentBox";
import { MouseBubble } from "../components/MouseBubble";
import { Spacer } from "../components/Spacer";

const AccountInfo: React.FC = () => {
    const [username, setUsername] = useState("");
    const [numberOfRepos, setNumberOfRepos] = useState("");

    React.useEffect(() => {
        const fetchUsername = async () => {
            try {
                const response = await fetch("/api/getUsername", { method: "POST" });
                const data = await response.json();
                setUsername(data.username);
            } catch (error) {
                console.error("Error fetching username:", error);
            }
        };

        fetchUsername();
    }, []);

    React.useEffect(() => {
        const fetchNumberOfRepos = async () => {
            try {
                const response = await fetch("/api/getNumberOfRepos", { method: "POST" });
                const data = await response.json();  
                setNumberOfRepos(data.number);
                console.log(data);
            } catch (error) {
                console.error("Error fetching number of repos:", error);
            }
        };

        fetchNumberOfRepos();
    }, []);

	return (
		<div className="bg-primary w-[100vw] h-[100vh] flex flex-col items-center p-12">
			<BackdropTriangles />
			<div style={{ zIndex: 1 }}>
				<Spacer space={40} />
				<ContentBox bgColor="secondary">
					<MouseBubble blur="almostMedium">
						<Header hasSearch />
                        <ContentBox bgColor="dark" hasBorder>
                            <div className="text-center w-[60vw] lg:h-[85vh] lg:w-[40vw]">
                                <h1 className="text-5xl font-bold mb-4">Account Info</h1>
                                <p className="text-2xl mt-4">Username: {username}</p>
                                <p className="text-2xl mt-8">Number of Repos: {numberOfRepos}</p>
                            </div>
                        </ContentBox>
					</MouseBubble>
				</ContentBox>
			</div>
		</div>
	);
};

export default AccountInfo;
