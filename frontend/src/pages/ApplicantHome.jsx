import React, { useState } from "react";

import "../styles/ApplicantHome.css";
import JobList from "../components/JobList";
import { Button, Container, IconButton, Typography, Box } from "@mui/material";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";

function ApplicantHome() {
  const [showJobs, setShowJobs] = useState(false);

  const toggleJobs = () => {
    setShowJobs(!showJobs);
  };

  return (
    <Box className="appHome">
      <Button variant="outlined">
        <Typography>Update my Profile</Typography>
      </Button>

      <Container className="row" sx={{ marginTop: "20px" }}>
        <Typography>Job List</Typography>
        <IconButton className="toggleJobs" onClick={toggleJobs}>
          <ArrowDropDownIcon className={showJobs ? "rotate" : ""} />
        </IconButton>
      </Container>

      {showJobs && <JobList />}
    </Box>
  );
}

export default ApplicantHome;
