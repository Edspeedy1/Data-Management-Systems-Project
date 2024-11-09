import React from 'react';
import { BackdropTriangles } from '../components/BackdropTriangles';
import { ContentBox } from '../components/ContentBox';
import { SplitVertical } from '../components/SplitVertical';
import { MouseBubble } from '../components/MouseBubble';

const Home: React.FC = () => {
	return (
		<div className="bg-primary w-[100vw] h-[100vh] flex flex-col items-center p-12">
			<BackdropTriangles />
			<div style={{ zIndex: 1 }}>
				<MouseBubble blur="almostMedium">
					<SplitVertical
						left={
							<ContentBox bgColor="dark" hasBorder>
								<div className="text-center w-[60vw] lg:h-[85vh] lg:w-[40vw]">
									<h1 className="text-5xl font-bold">Side 1</h1>
								</div>
							</ContentBox>
						}
						right={
							<ContentBox bgColor="dark" hasBorder>
								<div className="text-center w-[60vw] lg:h-[85vh] lg:w-[40vw]">
									<h1 className="text-5xl font-bold">Side 2</h1>
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