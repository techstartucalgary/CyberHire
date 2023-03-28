import React, { useEffect, useState } from "react";
import {
	TextField,
	Button,
	Grid,
	FormControlLabel,
	Checkbox,
	Typography,
	Link,
} from "@mui/material";

const SignUpPage = () => {
	const [username, setUserName] = useState("");
	const [usernameError, setUserNameError] = useState("");

	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [passwordError, setPasswordError] = useState("");
	const [is_recruiter, setRecommendedByRecruiter] = useState(false);
	const [formValid, setFormValid] = useState(false);

	useEffect(() => {
		setFormValid(!usernameError && !passwordError);
	}, [usernameError, passwordError]);

	const handleUserNameChange = (
		event: React.ChangeEvent<HTMLInputElement>
	) => {
		setUserName(event.target.value);
		if (event.target.value.length < 5) {
			setUserNameError("Username must be at least 5 characters");
		} else {
			setUserNameError("");
		}
	};

	const handleEmailChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setEmail(event.target.value);
	};

	const handlePasswordChange = (
		event: React.ChangeEvent<HTMLInputElement>
	) => {
		setPassword(event.target.value);
		if (event.target.value.length < 8) {
			setPasswordError("Password must be atleast 8 characters");
		} else {
			setPasswordError("");
		}
	};

	const handleRecommendedByRecruiterChange = (
		event: React.ChangeEvent<HTMLInputElement>
	) => {
		setRecommendedByRecruiter(event.target.checked);
	};

	const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
		event.preventDefault();

		try {
			const response = await fetch(
				"https://chapi.techstartucalgary.com/users/",
				{
					method: "POST",
					mode: "cors",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						username,
						email,
						password,
						is_recruiter,
					}),
				}
			);
			if (response.ok) {
				const data = await response.json();
				console.log(data);
			} else if (response.status === 400) {
				throw new Error("Username already exists");
			} else {
				throw new Error("Signup failed");
			}
		} catch (error) {
			console.error(error);
		}
		setUserName("");
		setEmail("");
		setPassword("");
		setRecommendedByRecruiter(false);
	};

	return (
		<Grid
			container
			justifyContent="center"
			alignItems="center"
			style={{ height: "100vh" }}
		>
			<Grid item xs={10} sm={8} md={6} lg={4}>
				<Typography
					variant="h4"
					align="center"
					sx={{
						mb: { xs: 2, sm: 4 },
						fontSize: { xs: "2rem", sm: "3rem", md: "4rem" },
					}}
				>
					CyberHire Signup Page
				</Typography>

				<form onSubmit={handleSubmit}>
					<TextField
						label="Username"
						variant="outlined"
						fullWidth
						margin="normal"
						value={username}
						onChange={handleUserNameChange}
						required
						error={!!usernameError}
						helperText={usernameError}
					/>

					<TextField
						label="Email"
						variant="outlined"
						fullWidth
						margin="normal"
						type="email"
						value={email}
						onChange={handleEmailChange}
						required
					/>
					<TextField
						label="Password"
						variant="outlined"
						fullWidth
						margin="normal"
						type="password"
						value={password}
						onChange={handlePasswordChange}
						required
						error={!!passwordError}
						helperText={passwordError}
					/>
					<FormControlLabel
						control={
							<Checkbox
								checked={is_recruiter}
								onChange={handleRecommendedByRecruiterChange}
							/>
						}
						label="Were you recommended by a recruiter?"
					/>
					<Button
						type="submit"
						variant="contained"
						color="primary"
						fullWidth
						disabled={!formValid}
					>
						Sign Up
					</Button>
					<Grid container justifyContent="flex-end">
						<Grid item>
							<Typography>
								Already have an account?
								<Link
									href="#/signin"
									variant="body2"
								>
									Sign In
								</Link>
							</Typography>
						</Grid>
					</Grid>
				</form>
			</Grid>
		</Grid>
	);
};

export default SignUpPage;
