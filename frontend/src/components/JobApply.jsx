import React, { useState } from 'react'
import { useEffect } from 'react';
import {  Typography } from "@mui/material";
import JobPost from './JobPost';

const JobApply = () => {

    const [appliedJobs, setAppliedJobs] = useState([]);

    const getAplliedJobs = async () => {
        await fetch("https://chapi.techstartucalgary.com/applications/me", {
            mode: "cors",
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
        })
        .then((response) => response.json())
        .then((data) => setAppliedJobs(data))
        .catch((error) => console.error(error))
    }

    useEffect(() => {
        getAplliedJobs()
    },[])




  return (
    <div>
        {appliedJobs.length > 0 ? (
            <div>
                <Typography>Applied Jobs</Typography>
                {appliedJobs.map((appliedJob) => (
                    <JobPost
                     key = {appliedJob.id}
                     job = {appliedJob.job}
                     disabled = {true}
                    
                    
                    />
                )) }

            </div>
        ):(

            <Typography>No found Job</Typography>
        )}

    </div>
  )
}

export default JobApply