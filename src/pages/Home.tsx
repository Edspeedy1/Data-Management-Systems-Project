import React from 'react';
import { Header } from '../components/Header';
import { BackdropTriangles } from '../components/BackdropTriangles';
import { ContentBox } from '../components/ContentBox';
import { SplitVertical } from '../components/SplitVertical';
import { MouseBubble } from '../components/MouseBubble';
import { Spacer } from '../components/Spacer';
import { HomePageButtons } from '../components/HomePageButtons';
import { UsersRepos } from '../components/UsersRepos';


const Home: React.FC = () => {
	return (
		<div className="bg-primary w-[100vw] h-[100vh] flex flex-col items-center p-12">
			<BackdropTriangles />
			<div style={{ zIndex: 1 }}>
				<MouseBubble blur="almostMedium">
					<Header hasSearch/>
					<Spacer space={40}/>
					<SplitVertical
						left={
							<ContentBox bgColor="dark" hasBorder>
								<div className="text-center w-[60vw] lg:h-[85vh] lg:w-[40vw]">
									<h1 className="text-5xl font-bold mb-4">My Repos</h1>
									<UsersRepos />
								</div>
							</ContentBox>
						}
						right={
							<ContentBox bgColor="dark" hasBorder>
								<div className="text-center w-[60vw] lg:h-[85vh] lg:w-[40vw]">
									<h1 className="text-5xl font-bold mb-4">Buttons</h1>
									<HomePageButtons />
								</div>
							</ContentBox>
						}
					/>
				</MouseBubble>
			</div>
		</div>
	);
};

export default Home;