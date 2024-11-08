import React from "react";
import { ContentBox } from "../components/ContentBox";
import { MouseBubble } from "../components/MouseBubble";
import { LoginInputs } from "../components/LoginInputs";
import { BackdropTriangles } from "../components/BackdropTriangles";

const Login: React.FC = () => {
	return (
		<div className="bg-primary w-[100vw] h-[100vh] flex flex-col items-center p-12 overflow-hidden">
			<BackdropTriangles />
			<div style={{ zIndex: 1 }}>
				<ContentBox bgColor="secondary" hasBorder>
					<div className="h-[70vh] w-[60vw] flex justify-center">
						<MouseBubble>
							<div className="mt-20">
								<ContentBox bgColor="light" hasBorder>
									<div className="text-center w-[60vw] lg:h-[300px] lg:w-[20vw]">
										<h1 className="text-3xl font-bold">Login</h1>
										<LoginInputs />
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

export default Login;
