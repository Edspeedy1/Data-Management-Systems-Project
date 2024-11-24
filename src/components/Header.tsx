import React, { useState } from "react";

export const Header: React.FC<
	React.PropsWithChildren<{
		hasSearch?: boolean;
	}>
> = ({ hasSearch = true }) => {
	const [searchExpanded, setSearchExpanded] = useState(false);
	const [searchTerm, setSearchTerm] = useState("");

	return (
		<header className="fixed top-0 left-0 border-b-border border-b-2 bg-dark w-[100vw] h-16 flex justify-between overflow-hidden">
			<div className="flex items-center w-[75vw]"> 
				<div className="flex items-center cursor-pointer" onClick={() => window.location.href = "/home" }>
					<img src="../content/icon.png" className="mr-4 h-16" />
					<h1 className="text-3xl sm:text-5xl font-bold pb-1 sm:pb-3">Project Forge</h1>
				</div>
			</div>
			{hasSearch && (
				<div className="pr-4 justify-end flex items-center relative">
					<form
						className={`flex items-center h-12 transition-all duration-300 ${
							searchExpanded ? "w-64" : "w-0 opacity-0"
						} overflow-hidden border border-gray-400 rounded bg-white`}
						onSubmit={(e) => {
							e.preventDefault();
							setSearchExpanded(false);
							setTimeout(() => {
								window.location.href = "/search?" + searchTerm;
							}, 100);
						}}
					>
						<input
							type="text"
							className="w-full px-4 py-2 text-black outline-none"
							placeholder="Search..."
							id="searchBar"
							onFocus={() => setSearchExpanded(true)}
							onBlur={() => setSearchExpanded(false)}
							onChange={(e) => setSearchTerm(e.target.value)}
						/>
					</form>
					<button
						className="flex items-center justify-center h-16 ml-2"
						onClick={() => setSearchExpanded((prev) => !prev)}
					>
						<img src="../content/magnifying glass.svg" className="h-8" alt="Search Icon" />
					</button>
				</div>
			)}
		</header>
	);
};