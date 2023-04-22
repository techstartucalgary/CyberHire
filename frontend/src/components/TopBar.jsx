import React from "react";
import { AppBar, Button, Toolbar, Typography, Grid } from "@mui/material";
import logo from "../img/CyberHireLogo.png";
import "../styles/TopBar.css";

function TopBar() {
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
            <a href="/" className="logoLink">
              <img className="logo" src={logo} alt="CyberHire Logo" />
            </a>
          </Grid>
          <Grid item className="buttonContainer" xs={1}>
            <Button variant="contained" className="signup" href="#/signup">
              <Typography>Sign-up</Typography>
            </Button>
            <Button variant="outlined" className="signin" href="#/signin">
              <Typography>Sign in</Typography>
            </Button>
          </Grid>
        </Grid>
      </Toolbar>
    </AppBar>
  );
}

export default TopBar;
