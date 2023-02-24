import React from "react";
import {
	AppBar,
	Button,
	Toolbar,
	Typography,
} from "@mui/material";
import logo from "./CyberHireLogo.png";
import "../styles/TopBar.css";

function TopBar() {
	return (
		<AppBar position="sticky">
			<Toolbar>
				<a href="/">
					<img className="logo" src={logo} alt="CyberHire Logo" />
				</a>
				<Button variant="contained">
					<Typography>Sign-up</Typography>
				</Button>
				<Button variant="outlined">
					<Typography>Sign in</Typography>
				</Button>
			</Toolbar>
		</AppBar>
	);
}

export default TopBar;
