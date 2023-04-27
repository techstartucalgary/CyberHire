import React from "react";
import { Button, Typography } from "@mui/material";

import "../styles/JobPost.css";

function JobPost(props) {
  const formatCurrency = (num) => {
    return num.toLocaleString("en-US", {
      style: "currency",
      currency: "CAD",
      maximumFractionDigits: 0,
    });
  };

  const  applyHandler = async (job) => {
    const response = await fetch(`https://chapi.techstartucalgary.com/applications/${props.job.id}`, {
      method: "POST",
      headers: {
        'Content-Type' : 'application/json',
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    })
    const data = await response.json()
    console.log(data)
  }


  return (
    <div className="jobContainer">
      <Typography className="jobTitle">{props.job.title}</Typography>
      <Typography className="jobCompany">{props.job.owner.company}</Typography>
      <Typography className="jobLocation">{props.job.location}</Typography>
      {props.job?.min_salary && (
        <Typography className="jobSalary">
          {formatCurrency(props.job.min_salary)} -{" "}
          {formatCurrency(props.job.max_salary)}
        </Typography>
      )}
      {props.job?.description && (
        <div className="descContainer">
          <Typography className="jobDescription">
            {props.job.description}
          </Typography>
        </div>
      )}
      {props.job.skills.map((skill) => {
        return (
          <Typography className="jobSkill" key={skill.id}>
            {skill.skill}
          </Typography>
        );
      })}
      <Button variant="contained" onClick={applyHandler} className="applyButton">
        <Typography>Apply</Typography>
      </Button>
    </div>
  );
}

export default JobPost;
