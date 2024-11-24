import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Repo from "../pages/Repo";
import AccountIngo from "../pages/AccountInfo";
import CreateRepo from "../pages/CreateRepo";
import UploadFiles from "../pages/UploadFiles";
import SearchPage from "../pages/SearchPage";

const AppRoutes: React.FC = () => {
	return (
		<Router>
			<Routes>
				<Route path="/" element={<Login />} />
				<Route path="/login" element={<Login />} />
				<Route path="/home" element={<Home />} />
				<Route path="/repo" element={<Repo />} />
				<Route path="/createRepo" element={<CreateRepo />} />
				<Route path="/uploadFiles" element={<UploadFiles />} />
				<Route path="/accountInfo" element={<AccountIngo />} />
				<Route path="/search" element={<SearchPage />} />
			</Routes>
		</Router>
	);
};

export default AppRoutes;
