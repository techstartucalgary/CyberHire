import React, { useState } from "react";

import "../styles/RecruiterHome.css";
import CreateJobModal from "../components/CreateJobModal";
import { Button, Container, Typography, Box } from "@mui/material";

function RecruiterHome() {
  const [showCreateJobModal, setShowCreateJobModal] = useState(false);

  const showModal = () => {
    setShowCreateJobModal(true);
  };

  return (
    <Box className="appHome">
      <Button variant="outlined" onClick={showModal}>
        <Typography>Post New Job</Typography>
      </Button>

      <Container className="row" sx={{ marginTop: "20px" }}>
        <Typography>Your Job Listings</Typography>
      </Container>

      <CreateJobModal open={showCreateJobModal} />
    </Box>
  );
}

export default RecruiterHome;
