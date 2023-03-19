import React from "react";
import { Button, Typography } from "@mui/material";

import "../styles/JobPost.css";
import { Skill } from "../interfaces/interfaces";

function JobPost(props: any) {
  const formatCurrency = (num: number) => {
    return num.toLocaleString("en-US", {
      style: "currency",
      currency: "CAD",
      maximumFractionDigits: 0,
    });
  };

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
      {props.job.skills.map((skill: Skill) => {
        return (
          <Typography className="jobSkill" key={skill.id}>
            {skill.skill}
          </Typography>
        );
      })}
      <Button variant="contained" className="applyButton">
        <Typography>Apply</Typography>
      </Button>
    </div>
  );
}

export default JobPost;
