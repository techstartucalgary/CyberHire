import React, { useState } from "react";

import "../styles/ApplicantHome.css";
import JobList from "../components/JobList";
import { Button, IconButton, Typography, Box } from "@mui/material";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import JobApply from "../components/JobApply";

function ApplicantHome() {
  const [showJobs, setShowJobs] = useState(false);
  const [appliedList, setAppliedList] = useState(false);

  const toggleJobs = () => {
    setShowJobs(!showJobs);
  };
  const toggleAppliedJobs = () => {
    setAppliedList(!appliedList);
  };

  return (
    <Box className="appHome">
      <Button variant="outlined" href="#/editProfile">
        <Typography>Update my Profile</Typography>
      </Button>

      <Box className="column" sx={{ marginTop: "20px" }}>
        <div className="row">
          <Typography align="center" variant="h5">
            Jobs For You
          </Typography>
          <IconButton className="toggleJobs" onClick={toggleJobs}>
            <ArrowDropDownIcon
              fontSize="large"
              className={showJobs ? "rotate" : ""}
            />
          </IconButton>
        </div>
        {showJobs && <JobList />}

        <div className="row">
          <Typography align="left" variant="h5">
            Pending Jobs
          </Typography>
          <IconButton className="toggleJobs" onClick={toggleAppliedJobs}>
            <ArrowDropDownIcon
              fontSize="large"
              className={appliedList ? "rotate" : ""}
            />
          </IconButton>
        </div>
        {appliedList && <JobApply />}
      </Box>
    </Box>
  );
}

export default ApplicantHome;
