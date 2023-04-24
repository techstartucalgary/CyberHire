import React, { useState, useEffect } from "react";
import {
  AppBar,
  Button,
  Toolbar,
  Typography,
  Grid,
  Menu,
  MenuItem,
  Avatar,
} from "@mui/material";
import logo from "../img/CyberHireLogo.png";
import "../styles/TopBar.css";

function TopBar() {
  const [username, setUsername] = useState("");
  const [profilePicture, setProfilePicture] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isRecruiter, setIsRecruiter] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);

  useEffect(() => {
    async function fetchData() {
      if (localStorage.getItem("access_token") !== null) {
        await fetch("https://chapi.techstartucalgary.com/users/me/", {
          mode: "cors",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        }).then((response) => {
          if (response.status === 200) {
            response.json().then((data) => {
              setIsLoggedIn(true);
              setUsername(data.username);
              setIsRecruiter(data.is_recruiter);
              fetch(
                "https://chapi.techstartucalgary.com/users/profile/me/profile_picture",
                {
                  mode: "cors",
                  headers: {
                    Authorization: `Bearer ${localStorage.getItem(
                      "access_token",
                    )}`,
                  },
                },
              ).then((response) => {
                if (response.status === 200) {
                  response.blob().then((blob) => {
                    const imageURL = URL.createObjectURL(blob);
                    console.log(imageURL);
                    setProfilePicture(imageURL);
                  });
                }
              });
            });
          }
        });
      }
    }
    fetchData();
  }, [localStorage.getItem("access_token")]);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleNavigate = (page) => {
    handleClose();
    if (page === "signout") {
      localStorage.removeItem("access_token");
      localStorage.removeItem("is_recruiter");
      window.location.href = `#/signin/`;
      window.location.reload();
    } else if (page === "dashboard") {
      var dashboard = isRecruiter ? "#/recruiterHome/" : "#/app/";
      window.location.href = `${dashboard}`;
    } else if (page === "edit") {
      window.location.href = `#/editProfile/`;
    }
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar position="sticky">
      <Toolbar className="topBar">
        <Grid container spacing={0} columns={3} alignItems="center">
          <Grid item xs={0} md={1} />
          <Grid
            className="logoContainer"
            item
            xs={2}
            md={1}
            alignItems="center"
          >
            <a href="/">
              <img className="logo" src={logo} alt="CyberHire Logo" />
            </a>
          </Grid>
          <Grid item className="buttonContainer" xs={1}>
            {!isLoggedIn ? (
              <>
                <Button variant="contained" className="signup" href="#/signup">
                  <Typography>Sign-up</Typography>
                </Button>
                <Button variant="outlined" className="signin" href="#/signin">
                  <Typography>Sign in</Typography>
                </Button>
              </>
            ) : (
              <>
                <Button onClick={handleMenu}>
                  {profilePicture && (
                    <Avatar
                      className="avatar"
                      alt="Profile Picture"
                      src={profilePicture}
                    />
                  )}
                  {username}
                </Button>
                <Menu
                  id="menu-appbar"
                  anchorEl={anchorEl}
                  anchorOrigin={{
                    vertical: "top",
                    horizontal: "right",
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: "top",
                    horizontal: "right",
                  }}
                  open={Boolean(anchorEl)}
                  onClose={handleClose}
                >
                  <MenuItem onClick={() => handleNavigate("dashboard")}>
                    Dashboard
                  </MenuItem>
                  <MenuItem onClick={() => handleNavigate("edit")}>
                    Edit Profile
                  </MenuItem>
                  <MenuItem onClick={() => handleNavigate("signout")}>
                    Sign Out
                  </MenuItem>
                </Menu>
              </>
            )}
          </Grid>
        </Grid>
      </Toolbar>
    </AppBar>
  );
}

export default TopBar;
