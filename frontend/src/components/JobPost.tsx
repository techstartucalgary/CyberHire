import React from "react";
import { AppBar, Button, Toolbar, Typography, Grid } from "@mui/material";
import logo from "./CyberHireLogo.png";
import "../styles/JobPost.css";

function JobPost(props: any) {
  return (
    <div className="jobContainer">
      <Typography className="jobTitle">{props.job.title}</Typography>
      <Typography className="jobCompany">{props.job.company}</Typography>
      <Typography className="jobLocation">{props.job.location}</Typography>
      {props.job?.salary && (
        <Typography className="jobSalary">${props.job.salary}</Typography>
      )}
      {props.job?.description && (
        <div className="descContainer">
          <Typography className="jobDescription">
            {props.job.description}
          </Typography>
        </div>
      )}
      <Button variant="contained" className="applyButton">
        <Typography>Apply</Typography>
      </Button>
    </div>
  );
}

export default JobPost;
