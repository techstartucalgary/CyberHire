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

  const handleUserNameChange = (event) => {
    setUserName(event.target.value);
    if (event.target.value.length < 5) {
      setUserNameError("Username must be at least 5 characters");
    } else {
      setUserNameError("");
    }
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
    if (event.target.value.length < 8) {
      setPasswordError("Password must be atleast 8 characters");
    } else {
      setPasswordError("");
    }
  };

  const handleRecommendedByRecruiterChange = (event) => {
    setRecommendedByRecruiter(event.target.checked);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      await fetch("https://chapi.techstartucalgary.com/users/", {
        method: "POST",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          email,
          password,
          is_recruiter,
        }),
      }).then((response) => {
        if (response.ok) {
          fetch("https://chapi.techstartucalgary.com/token", {
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
                throw new Error("API Error: ", response.status);
              }
              return response.json();
            })
            .then((data) => {
              localStorage.setItem("access_token", data.access_token);
              if (is_recruiter) {
                window.location.href = "#/recruiterHome";
              } else {
                window.location.href = "#/app";
              }
            })
            .catch((error) => console.error(error));
        } else if (response.status === 400) {
          throw new Error("Username already exists");
        } else {
          throw new Error("Signup failed");
        }
      });
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
            label="Would you like to sign up as a recruiter?"
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
                <Link href="#/signin" variant="body2">
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
