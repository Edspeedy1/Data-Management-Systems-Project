import React, { useState } from "react";
import clsx from "clsx";

import { MouseBubble } from "../components/MouseBubble";
import { Header } from "../components/Header";
import { Spacer } from "../components/Spacer";
import { SplitVertical } from "../components/SplitVertical";
import { ContentBox } from "../components/ContentBox";
import { BackdropTriangles } from "../components/BackdropTriangles";
import { DragAndDrop } from "../components/DragAndDrop";



const CreateRepo: React.FC = () => {
    const [reponame, setRepoName] = useState("");
    const [description, setDescription] = useState("");
    const [isActive, setIsActive] = useState(false);
    const [files, setFiles] = useState<File[]>([]);
    
    React.useEffect(() => {
        if (reponame.trim()) {
            setIsActive(true);
        } else {
            setIsActive(false);
        }
    }, [reponame, description]);
    
    const handleUpload = async () => {

    };
    
    function apiCreateRepo() {
        if (!reponame || !isActive) {
            return;
        }
    
        const formData = new FormData();
        formData.append("repoID", reponame); // Add repoID to the form data
        formData.append("description", description || ""); // Add description

        if (files.length !== 0) {
            files.forEach((file) => {
                formData.append("files", file); // Add files
            });
        }
    
        console.log("Creating repo:", reponame);

        fetch("/api/createRepo", {
            method: "POST",
            body: formData,
        })
            .then((response) => {
                console.log("got response");
                console.log(response.headers);
                return response.json()
            })
            .then((data) => {
                if (data.success) {
                    console.log("Repo created successfully:", data);
                } else {
                    console.error("Failed to create repo:", data);
                }
            })
            .catch((error) => {
                console.error("Error creating repo:", error);
            });
    }
    

    const repoNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setRepoName(e.target.value);
    }

    const descriptionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setDescription(e.target.value);
    }
    
	return (
		<div className="bg-primary w-[100vw] h-[100vh] flex flex-col items-center p-12">
			<BackdropTriangles />
			<div style={{ zIndex: 1 }}>
				<Spacer space={40} />
				<ContentBox bgColor="secondary" hasBorder>
					<div className="lg:p-[100px] p-4">
						<MouseBubble blur="md">
							<Header hasSearch />
							<ContentBox bgColor="light" hasBorder>
								<div className="text-center w-[70vw] h-[80vh] lg:h-[550px] lg:w-[50vw]">
									<SplitVertical left={
                                        <div className="text-center w-full">
                                            <Spacer space={40} />
                                            <h1 className="text-3xl font-bold">Repo Name</h1>
                                            <Spacer space={20} />
                                            <input type="text" onChange={repoNameChange} className="border-2 border-border rounded-xl p-2 w-[90%]" placeholder="Repo Name" />
                                        </div>
                                    } right={
                                        <div className="text-center w-full">
                                            <div className="lg:block hidden">
                                                <Spacer space={40} />
                                            </div>
                                            <h1 className="text-3xl font-bold">Repo Description</h1>
                                            <Spacer space={20} />
                                            <input type="text" onChange={descriptionChange} className="border-2 border-border rounded-xl p-2 w-[90%]" placeholder="Description (optional)" />
                                        </div>
                                    } />
                                    <div className="lg:block hidden">
                                        <Spacer space={30} />
                                    </div>
                                    <Spacer space={50} />
                                    <DragAndDrop files={files} setFiles={setFiles} onUpload={handleUpload}>
                                    </DragAndDrop>
                                    <div className="absolute bottom-4 text-center w-full -ml-2">
                                        <button 
                                            onClick={() => apiCreateRepo()} 
                                            className={
                                                clsx(
                                                    "text-3xl font-bold m-3 pt-4 pb-4 p-2 bg-dark text-white rounded-xl lg:w-[calc(50%-40px)] cursor-pointer",
                                                    isActive ? "" : "opacity-50"
                                                )
                                            }
                                            >Create Repo</button>
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

export default CreateRepo;
