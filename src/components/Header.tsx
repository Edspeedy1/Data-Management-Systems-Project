import React from "react";

export const Header: React.FC<
	React.PropsWithChildren<{
		hasSearch?: boolean;
	}>
> = ({ hasSearch = true }) => {
	return (
		<header className="fixed top-0 left-0 border-b-border border-b-2 bg-dark w-[100vw] h-16 flex justify-between overflow-hidden">
			<div className="flex items-center w-[75vw]"> 
				<img src="../content/icon.png" className="mr-4 h-16" />
				<h1 className="text-3xl sm:text-5xl font-bold pb-1 sm:pb-3">Project Forge</h1>
			</div>
			{hasSearch && (
				<div className="pr-4 justify-end flex">
					<button className="flex h-16" onClick={() => {
                        // do something
                    }}>
						<h1 className="text-5xl hidden sm:block">Search</h1>
						<img src="../content/magnifying glass.svg" className="ml-2 h-16" />
					</button>
				</div>
			)}
		</header>
	);
};
