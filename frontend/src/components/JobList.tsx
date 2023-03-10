import React, { useEffect, useState } from "react";
import { Typography } from "@mui/material";
import "../styles/JobList.css";
import JobPost from "./JobPost";

interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  salary?: string;
  description?: string;
}

const jobs = [
  {
    id: 0,
    title: "Software Engineer",
    company: "Google",
    location: "Mountain View, CA",
    salary: "100,000",
    description: "This is a description of the job",
  },
  {
    id: 1,
    title: "Software Engineer",
    company: "Google",
    location: "Mountain View, CA",
    description: "This is a description",
  },
  {
    id: 2,
    title: "Software Engineer",
    company: "Google",
    location: "Mountain View, CA",
    salary: "100,000",
  },
  {
    id: 3,
    title: "Software Engineer",
    company: "Google",
    location: "Mountain View, CA",
    salary: "100,000",
  },
];

function JobList(props: any) {
  // const [jobs, setJobs] = useState<Job[]>([]);

  // const getJobs = async () => {
  //   await fetch("https://chapi.techstartucalgary.com/jobs")
  //     .then((response) => response.json())
  //     .then((data) => setJobs(data))
  //     .catch((error) => console.error(error));
  // };

  // useEffect(() => {
  //   getJobs();
  // }, []);

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
