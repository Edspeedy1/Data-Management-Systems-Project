import React from "react";
import { ContentBox } from "../components/ContentBox";
import { MouseBubble } from "../components/MouseBubble";
import { LoginInputs } from "../components/LoginInputs";

const Login: React.FC = () => {
	return (
		<div className="bg-primary w-[100vw] h-[100vh] flex flex-col items-center p-12">
			<ContentBox bgColor="secondary" hasBorder>
				<div className="h-[80vh] w-[80vw] flex justify-center">
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
	);
};

export default Login;
