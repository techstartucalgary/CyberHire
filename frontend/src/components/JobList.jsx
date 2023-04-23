import React, { useEffect, useState } from "react";
import { Typography } from "@mui/material";
import "../styles/JobList.css";
import JobPost from "./JobPost";

function JobList(props) {
  const [jobs, setJobs] = useState([]);

  const getJobs = async () => {
    await fetch("https://chapi.techstartucalgary.com/job_matching/", {
      mode: "cors",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    })
      .then((response) => response.json())
      .then((data) => setJobs(data))
      .catch((error) => console.error(error));
  };

  useEffect(() => {
    getJobs();
  }, []);

  return (
    <div>
      {jobs.length > 0 ? (
        <div className="jobList">
          {jobs.map((job) => (
            <JobPost key={job.id} job={job} />
          ))}
        </div>
      ) : (
        <Typography className="noJobs">No jobs found</Typography>
      )}
    </div>
  );
}

export default JobList;
