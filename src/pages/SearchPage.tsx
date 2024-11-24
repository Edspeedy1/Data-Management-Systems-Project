import React from "react";
import { BackdropTriangles } from "../components/BackdropTriangles";
import { ContentBox } from "../components/ContentBox";
import { Header } from "../components/Header";
import { MouseBubble } from "../components/MouseBubble";
import { Spacer } from "../components/Spacer";
import { SearchResults } from "../components/SearchResults";

const SearchPage: React.FC = () => {
	return (
		<div className="bg-primary w-[100vw] h-[100vh] flex flex-col items-center p-12">
			<BackdropTriangles />
			<div style={{ zIndex: 1 }}>
				<Spacer space={50} />
				<ContentBox bgColor="secondary" hasBorder>
					<div className="h-[81vh] w-[61vw] flex justify-center">
						<MouseBubble blur="almostMedium">
							<Header />
							<div className="border-black border-2">
								<ContentBox bgColor="dark">
									<div className="text-center w-[60vw] h-[80vh] -m-2">
										<h1 className="text-5xl font-bold">Search: {window.location.search.replace("?", " ").replace("%20", " ")}</h1>
                                        <SearchResults />
									</div>
								</ContentBox>
							</div>
						</MouseBubble>
					</div>
				</ContentBox>
			</div>
		</div>
	);
};

export default SearchPage;
