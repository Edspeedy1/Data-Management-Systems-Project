import React, { useEffect, useState } from "react";
import { BackdropTriangles } from "../components/BackdropTriangles";
import { ContentBox } from "../components/ContentBox";
import { Header } from "../components/Header";
import { MouseBubble } from "../components/MouseBubble";
import { Spacer } from "../components/Spacer";
import { SettingsDropDown } from "../components/SettingsDropDown";
import { CollabBox } from "../components/CollabBox";
import { UploadFiles } from "../components/UploadFiles";

const Repo: React.FC = () => {
    const repoName = window.location.pathname.split("/")[2];

    const [isLoadingDesc, setIsLoadingDesc] = useState(true);
    const [description, setDescription] = useState("");

    useEffect(() => {
        const controller = new AbortController();
        fetch('/api/getRepoDescription', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ repoID: repoName }),
            signal: controller.signal
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                setDescription(data.description || '');
            })
            .catch((error) => {
                console.error("Error fetching repos:", error);
            })
            .finally(() => {
                setIsLoadingDesc(false);
            });

        return () => {
            controller.abort("unmounted"); // Abort the fetch request on component unmount
        }
    }, []);

    return (
        <div className="bg-primary w-[100vw] h-[100vh] flex flex-col items-center p-12">
			<BackdropTriangles />
			<div style={{ zIndex: 1 }}>
				<Spacer space={40} />
				<ContentBox bgColor="secondary" hasBorder>
					<div className="p-2">
						<MouseBubble blur="md">
							<Header hasSearch />
							<ContentBox bgColor="light" hasBorder>
								<div className="text-center w-[80vw] h-[80vh] flex justify-center">
									<div className="w-[35%] overflow-hidden border-dark border-r-4">
                                        <button className="left-4 absolute">
                                            <img src="../content/download-svgrepo-com.svg" className="h-8" alt="Search Icon" />
                                        </button>
                                        <h1 className="text-3xl font-bold pl-12 pr-12">{repoName.replace(/%20/g, " ")}</h1>
                                        <Spacer space={20}/>
                                        <h1 className="text-xl font-bold">{isLoadingDesc ? "Loading..." : description}</h1>
                                        <Spacer space={20}/>
                                        <div className="text-xl font-bold h-[calc(100%-100px)] overflow-y-auto" style={{
                                            scrollbarWidth: "thin",
                                            scrollbarColor: "#888 #333",
                                        }}>
                                        </div>
                                    </div>
                                    <div className="w-[100%]">
                                        <p>Files</p>
                                    </div>
                                    <div className="w-[20%] border-dark border-l-4"> 
                                        <SettingsDropDown />
                                        <CollabBox />
                                        <UploadFiles />
                                    </div>
								</div>
							</ContentBox>
						</MouseBubble>
					</div>
				</ContentBox>
			</div>
		</div>
	);
};

export default Repo;