import React, { useState } from "react";

import "../styles/ApplicantHome.css";
import JobList from "../components/JobList";
import { Button, Container, IconButton, Typography, Box } from "@mui/material";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import JobApply from "../components/JobApply";

function ApplicantHome() {
  const [showJobs, setShowJobs] = useState(false);
  const [appliedList, setAppliedList] = useState(false)

  const toggleJobs = () => {
    setShowJobs(!showJobs);
  };
  const toggleAppliedJobs = () => {
    setAppliedList(!appliedList)
  }

  return (
    <Box className="appHome">
      <Button variant="outlined" href="#/editProfile">
        <Typography>Update my Profile</Typography>
      </Button>

      <Container className="row" sx={{ marginTop: "20px" }}>
        <Typography align="center" variant="h5">
          Job List
        </Typography>
        
        <IconButton className="toggleJobs" onClick={toggleJobs}>
          <ArrowDropDownIcon
            fontSize="large"
            className={showJobs ? "rotate" : ""}
          />
        </IconButton>

        <Typography align = "left" variant="h5">
          Applied Jobs
        </Typography>
        <IconButton className="toggleJobs" onClick={toggleAppliedJobs}>
          <ArrowDropDownIcon
            fontSize="large"
            className={showJobs ? "rotate" : ""}
          />
        </IconButton>
      </Container>

      {showJobs && <JobList />}
      {appliedList && <JobApply />}
    </Box>
  );
}

export default ApplicantHome;
