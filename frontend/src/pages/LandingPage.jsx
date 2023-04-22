import React from "react";

import { Box, Button } from "@mui/material";
import HiringVector from "../img/HiringVector.png";
import vector1 from "../img/LPVector1.png";
import vector2 from "../img/LPVector2.png";
import vector3 from "../img/LPVector3.png";
import findJob from "../img/findJob.png";
import "../styles/LandingPage.css";

const LandingPage = () => {
  return (
    <div>
      <img src={vector1} alt="" />

      <Box className="findJob">
        <img src={findJob} alt="Find Jobs Stress Free!" />
        <Button
          className="button-1"
          variant="contained"
          sx={{ color: "black", backgroundColor: "#f9e393" }}
          href="#/signup"
        >
          Get Started
        </Button>
      </Box>

      <img src={HiringVector} alt="" />

      <div className="design">
        <img className="image" src={vector2} alt="" />
        <img className="image" src={vector3} alt="" />
      </div>
    </div>
  );
};

export default LandingPage;
