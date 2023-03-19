import React from "react";
import "../styles/NotFound.css";
import { Button, Typography, Box } from "@mui/material";

function NotFound() {
  return (
    <Box className="notFound">
      <Typography variant="h2">
        Error 404
        <br />
        Page Not Found
      </Typography>
      <Typography>The page you are looking for does not exist.</Typography>
      <Button variant="outlined" sx={{ marginTop: "20px" }} href="/">
        <Typography>Go Home</Typography>
      </Button>
    </Box>
  );
}

export default NotFound;
