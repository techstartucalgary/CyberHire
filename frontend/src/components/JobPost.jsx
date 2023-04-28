import React from "react";
import { useState } from "react";
import { Button, Typography } from "@mui/material";
import { Label } from "../components/RecruiterApplicantsComponents";

import "../styles/JobPost.css";

function JobPost(props) {
  const [apply, setApply] = useState(false);

  const formatCurrency = (num) => {
    return num.toLocaleString("en-US", {
      style: "currency",
      currency: "CAD",
      maximumFractionDigits: 0,
    });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "SUBMITTED":
        return "success";
      case "UNDER REVIEW":
        return "info";
      case "UNDERGOING FURTHER SCREENING":
        return "warning";
      case "REJECTED":
        return "error";
      case "OFFER SENT":
        return "offerSent";
      default:
        return "secondary";
    }
  };

  const applyHandler = async () => {
    setApply(true);
    try {
      const response = await fetch(
        `https://chapi.techstartucalgary.com/applications/${props.job.id}`,
        {
          method: "POST",
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        },
      );
      if (response.ok) {
        alert("Job was succesful");
        setApply(false);
        window.location.reload();
      } else {
        throw new Error("Job application failed. Please try again later");
      }
    } catch (error) {
      console.error(error);
      alert(error.message);
      setApply(false);
    }
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
      {props.job.skills.map((skill) => {
        return (
          <Typography className="jobSkill" key={skill.id}>
            {skill.skill}
          </Typography>
        );
      })}
      {!props.disabled ? (
        <Button
          variant="contained"
          href=""
          className="applyButton"
          disabled={apply}
          onClick={applyHandler}
        >
          {apply ? (
            <Typography>Applying...</Typography>
          ) : (
            <Typography>Apply</Typography>
          )}
        </Button>
      ) : (
        <Label color={getStatusColor(props.status)}>{props.status}</Label>
      )}
    </div>
  );
}

export default JobPost;
