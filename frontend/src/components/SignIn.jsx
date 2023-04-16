import React, { useState } from "react";
import { TextField, Button, Grid, Typography, Link } from "@mui/material";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  //const [usernameError, setUsernameError] = useState('');
  //const [passwordError, setPasswordError] = useState('');
  const [errorMessage, setErrorMessage] = useState("");

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
    //setUsernameError('');
    setErrorMessage("");
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
    //setPasswordError('');
    setErrorMessage("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!username) {
      setErrorMessage("Username is required");
      return;
    }
    if (!password) {
      setErrorMessage("Password is required");
      return;
    }

    await fetch("https://chapi.techstartucalgary.com/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        grant_type: "password",
        username,
        password,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          if (response.status === 401) {
            setErrorMessage("Invalid username or password");
          } else {
            throw new Error("Login failed");
          }
        }
        setUsername("");
        setPassword("");
        return response.json();
      })
      .then((data) => {
        localStorage.setItem("access_token", data.access_token);
        fetch("https://chapi.techstartucalgary.com/users/me/", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("API Error: ", response.status);
            }
            return response.json();
          })
          .then((data) => {
            if (data.is_recruiter) {
              window.location.href = "#/app";
            } else {
              window.location.href = "#/recruiter";
            }
          });
      })
      .catch((error) => console.error(error));

    //setUsername('');
    //setPassword('');
  };

  return (
    <>
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
            CyberHire SignIn Page
          </Typography>

          <form onSubmit={handleSubmit}>
            <TextField
              label="Username"
              variant="outlined"
              type="text"
              fullWidth
              margin="normal"
              value={username}
              onChange={handleUsernameChange}
              error={!!errorMessage}
              helperText={errorMessage}
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
              error={!!errorMessage}
              helperText={errorMessage}
              required
            />
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Log In
            </Button>
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Typography>
                  Don't have an account?
                  <Link href="#/signup" variant="body2">
                    Sign up
                  </Link>
                </Typography>
              </Grid>
            </Grid>
          </form>
        </Grid>
      </Grid>
    </>
  );
};

export default LoginPage;
