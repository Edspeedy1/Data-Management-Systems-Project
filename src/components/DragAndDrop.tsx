import React from "react";

interface DragAndDropProps {
    setFiles: (files: File[]) => void; // Callback to update parent's file state
    files: File[]; // Pass current files from parent
    onUpload: () => void;
}

export const DragAndDrop: React.FC<DragAndDropProps> = ({ files, setFiles, onUpload }) => {

    const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        const newFiles = Array.from(e.dataTransfer.files);
        setFiles([...files, ...newFiles]); // Update parent state
        onUpload();
    };

    const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            const newFiles = Array.from(e.target.files);
            setFiles([...files, ...newFiles]); // Update parent state
            onUpload();
        }
    };

	// Prevent the default behavior for drag-over
	const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
		e.preventDefault();
	};

	// Render the file names
    const renderFiles = () => {
        const maxVisible = 2; // Limit to 2 files
        const visibleFiles = files.slice(0, maxVisible); // Take only the first 2 files
    
        return (
            <>
                {visibleFiles.map((file, index) => (
                    <li key={index} className="text-gray-700">
                        {file.webkitRelativePath || file.name}
                    </li>
                ))}
                {files.length > maxVisible && (
                    <li className="text-gray-500">...</li>
                )}
            </>
        );
    };
        
	return (
		<div className="w-full flex flex-col items-center justify-center space-y-4">
			<div
				className="p-4 border-2 border-dashed border-gray-400 flex flex-col items-center justify-center bg-gray-100 cursor-pointer"
				onDrop={handleDrop}
				onDragOver={handleDragOver}
			>
				<button className="text-2xl font-bold absolute top-[60%] right-4" onClick={() => setFiles([])}>X</button>
				<ul className="w-1/2 bg-white border rounded p-2 ">
					{files.length > 0 ? (
						renderFiles()
					) : (
						<li className="text-gray-500">No files selected</li>
					)}
				</ul>
				<input
					type="file"
					multiple
					className="hidden"
					id="file-input"
					onChange={handleFileInput}
				/>
				<label
					htmlFor="file-input"
					className="p-2 bg-blue-500 text-white rounded cursor-pointer"
				>
					Select Files
				</label>
			</div>
		</div>
	);
};