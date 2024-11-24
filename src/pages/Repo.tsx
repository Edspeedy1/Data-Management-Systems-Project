import React from "react";
import { BackdropTriangles } from "../components/BackdropTriangles";
import { ContentBox } from "../components/ContentBox";
import { Header } from "../components/Header";
import { MouseBubble } from "../components/MouseBubble";
import { Spacer } from "../components/Spacer";

const Repo: React.FC = () => {
    const repoName = window.location.pathname.split("/")[2];

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
                                        <h1 className="text-xl font-bold">Description</h1>
                                        <Spacer space={20}/>
                                        <div className="text-xl font-bold h-[calc(100%-100px)] overflow-y-auto" style={{
                                            scrollbarWidth: "thin",
                                            scrollbarColor: "#888 #333",
                                        }}>
                                            <p>Itterations</p>
                                        </div>
                                    </div>
                                    <div className="w-[100%]">
                                        <p>Files</p>
                                    </div>
                                    <div className="w-[20%] border-dark border-l-4"> 
                                        <p>Settings</p>
                                        <p>search Bar</p>
                                        <p>Collaborators -</p>
                                        <p>upload Files</p>
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