import React, { useState } from "react";
import clsx from "clsx";

export const LoginInputs: React.FC = () => {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [isActive, setIsActive] = useState(false);

	// Use effect to track changes in username and password and update the button state immediately
	React.useEffect(() => {
		if (username.trim() && password.trim()) {
			setIsActive(true);
		} else {
			setIsActive(false);
		}
	}, [username, password]); // Effect runs when username or password changes

	// Handlers for input changes
	const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setUsername(e.target.value);
	};

	const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setPassword(e.target.value);
	};

	function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
		if (!username || !password || !isActive) {
			return;
		}
		fetch("/api/login", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ username, password }),
		})
			.then((response) => response.json())
			.then((data) => {
				if (data.success) {
					console.log("redirecting...");
					window.location.href = "/home";
				}
			});
	}

	return (
		<form className="h-[30vh] lg:w-[20vw] flex flex-col justify-center items-center" onSubmit={handleSubmit}>
			<input
				type="text"
				name="username"
				id="username"
				placeholder="username"
				onChange={handleUsernameChange}
				className="p-2 border-2 border-black mt-4 mb-4"
			/>
			<input
				type="password"
				name="password"
				id="password"
				placeholder="password"
				onChange={handlePasswordChange}
				className="p-2 border-2 border-black mt-4 mb-4"
			/>
			<button
				className={
                    clsx(
                        "p-2 border-2 border-black mt-4 mb-4",
                        isActive ? "bg-dark text-white" : "bg-light text-black"
                    )}
				type="submit"
				disabled={!isActive}
			> Submit </button>
		</form>
	);
};
