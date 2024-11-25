import React, { useState } from "react";
import { DragAndDrop } from "./DragAndDrop";

export const UploadFiles: React.FC<React.PropsWithChildren<{
    setSharedState: React.Dispatch<React.SetStateAction<boolean>>
}>> = (setSharedState) => {
    const [files, setFiles] = useState<File[]>([]);

    return (
        <div className="w-full h-[20%]">
            <DragAndDrop files={files} setFiles={setFiles} onUpload={() => {}} />
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4" onClick={() => {
                setSharedState.setSharedState(true);
                setTimeout(() => {
                    setSharedState.setSharedState(false);
                }, 2);
                const formData = new FormData();
                const reponame = window.location.pathname.split("/")[2];
                formData.append("repoID", reponame); // Add repoID to the form data
        
                if (files.length !== 0) {
                    files.forEach((file) => {
                        formData.append("files", file); // Add files
                    });
                }
            
                console.log("Uploading files:", reponame);
        
                fetch("/api/UploadFile", {
                    method: "POST",
                    body: formData,
                })
                    .then((response) => {
                        return response.json()
                    })
                    .then((data) => {
                        if (data.success) {
                            console.log("uploaded Files", data);
                        } else {
                            console.error("Error uploading files:", data);
                        }
                    })
            }}>Upload</button>
        </div>
    );
};