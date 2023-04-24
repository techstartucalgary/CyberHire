// import React, { useState, useEffect } from "react";
// import {
//   Typography,
//   Box,
//   Grid,
//   Card,
//   CardContent,
// } from "@mui/material";

// function RecruiterApplicantsPage() {
//   const [jobs, setJobs] = useState([]);
//   const [selectedJob, setSelectedJob] = useState(null);

//   useEffect(() => {
//     fetchJobs();
//   }, []);

//   const fetchJobs = async () => {
//     const response = await fetch(
//         "https://chapi.techstartucalgary.com/jobs/me",
//         {
//           method: "GET",
//           mode: "cors",
//           headers: {
//             "Content-Type": "application/json",
//             Authorization: `Bearer ${localStorage.getItem("access_token")}`,
//           },
//         },
//       );
//     if (response.ok) {
//       const data = await response.json();
//       console.log('Fetched jobs:', data); // Add this line to print the fetched data
//       setJobs(data);
//     } else {
//       console.error("Failed to fetch jobs:", response.statusText);
//     }
//   };
  

//   const handleJobSelection = (job) => {
//     setSelectedJob(job);
//   };

//   return (
//     <Box className="applicantsPage">
//       <Typography variant="h5" textAlign="center" sx={{ marginTop: "20px" }}>
//         Select a Job
//       </Typography>

//       <Box sx={{ flexGrow: 1, marginTop: "20px" }}>
//         <Grid container spacing={2}>
//           {Array.isArray(jobs) && jobs.length === 0 ? (
//             <Typography color="text.secondary" sx={{ marginTop: "20px" }}>
//               No jobs posted
//             </Typography>
//           ) : (
//             Array.isArray(jobs) &&
//             jobs.map((job) => (
//               <Grid item xs={12} md={6} key={job.id}>
//                 <Card
//                   className="jobContainer"
//                   onClick={() => handleJobSelection(job)}
//                 >
//                   <CardContent className="CardContent">
//                     <Typography
//                       className="jobTitle"
//                       variant="h5"
//                       component="div"
//                     >
//                       {job.title}
//                     </Typography>
//                     <Typography
//                       className="jobCompany"
//                       sx={{ mb: 1.5 }}
//                       color="text.secondary"
//                     >
//                       {job.company_name}
//                     </Typography>
//                     <Typography
//                       className="jobLocation"
//                       sx={{ mb: 1.5 }}
//                       color="text.secondary"
//                     >
//                       {job.location}
//                     </Typography>
//                   </CardContent>
//                 </Card>
//               </Grid>
//             ))
//           )}
//         </Grid>
//       </Box>
//     </Box>
//   );
// }

// export default RecruiterApplicantsPage;


// import React, { useState, useEffect } from "react";
// import {
//   Typography,
//   Box,
//   Grid,
//   Card,
//   CardContent,
//   TextField,
//   List,
//   ListItem,
//   ListItemText,
// } from "@mui/material";

// function RecruiterApplicantsPage() {
//   const [jobs, setJobs] = useState([]);
//   const [selectedJob, setSelectedJob] = useState(null);
//   const [searchText, setSearchText] = useState("");

//   useEffect(() => {
//     fetchJobs();
//   }, []);

//   const fetchJobs = async () => {
//     const response = await fetch("https://chapi.techstartucalgary.com/jobs/me", {
//       method: "GET",
//       mode: "cors",
//       headers: {
//         "Content-Type": "application/json",
//         Authorization: `Bearer ${localStorage.getItem("access_token")}`,
//       },
//     });
//     if (response.ok) {
//       const data = await response.json();
//       console.log("Fetched jobs:", data);
//       setJobs(data);
//     } else {
//       console.error("Failed to fetch jobs:", response.statusText);
//     }
//   };

//   const handleJobSelection = (job) => {
//     setSelectedJob(job);
//   };

//   const handleSearchTextChange = (e) => {
//     setSearchText(e.target.value);
//   };

//   const filteredJobs = jobs.filter((job) =>
//     job.title.toLowerCase().includes(searchText.toLowerCase())
//   );

//   return (
//     <Box className="applicantsPage">
//       <Grid container spacing={2}>
//         <Grid item xs={12} md={6}>
//           <TextField
//             fullWidth
//             variant="outlined"
//             label="Search Jobs"
//             value={searchText}
//             onChange={handleSearchTextChange}
//             sx={{ marginBottom: "20px" }}
//           />
//           <Box
//             className="jobList"
//             sx={{
//               maxHeight: "500px",
//               overflowY: "scroll",
//               border: "1px solid lightgray",
//               borderRadius: "4px",
//               padding: "8px",
//             }}
//           >
//             <List>
//               {filteredJobs.map((job) => (
//                 <ListItem
//                   key={job.id}
//                   button
//                   onClick={() => handleJobSelection(job)}
//                 >
//                   <ListItemText primary={job.title} />
//                 </ListItem>
//               ))}
//             </List>
//           </Box>
//         </Grid>
//         <Grid item xs={12} md={6}>
//           {selectedJob ? (
//             <Card>
//               <CardContent>
//                 <Typography variant="h5" component="div">
//                   {selectedJob.title}
//                 </Typography>
//                 <Typography sx={{ mb: 1.5 }} color="text.secondary">
//                   {selectedJob.company_name}
//                 </Typography>
//                 <Typography sx={{ mb: 1.5 }} color="text.secondary">
//                   {selectedJob.location}
//                 </Typography>
//               </CardContent>
//             </Card>
//           ) : (
//             <Typography color="text.secondary">
//               Select a job to see its details
//             </Typography>
//           )}
//         </Grid>
//       </Grid>
//     </Box>
//   );
// }

// export default RecruiterApplicantsPage;



// import React, { useState, useEffect } from "react";
// import {
//   Typography,
//   Box,
//   Grid,
//   Card,
//   CardContent,
//   TextField,
//   List,
//   ListItem,
//   ListItemText,
// } from "@mui/material";
// import "../styles/RecruiterApplicant.css";



// function RecruiterApplicantsPage() {
//   const [jobs, setJobs] = useState([]);
//   const [selectedJob, setSelectedJob] = useState(null);
//   const [searchText, setSearchText] = useState("");

//   useEffect(() => {
//     fetchJobs();
//   }, []);

//   const fetchJobs = async () => {
//     const response = await fetch("https://chapi.techstartucalgary.com/jobs/me", {
//       method: "GET",
//       mode: "cors",
//       headers: {
//         "Content-Type": "application/json",
//         Authorization: `Bearer ${localStorage.getItem("access_token")}`,
//       },
//     });
//     if (response.ok) {
//       const data = await response.json();
//       console.log("Fetched jobs:", data);
//       setJobs(data);
//     } else {
//       console.error("Failed to fetch jobs:", response.statusText);
//     }
//   };

//   const handleJobSelection = (job) => {
//     setSelectedJob(job);
//   };

//   const handleSearchTextChange = (e) => {
//     setSearchText(e.target.value);
//   };

//   const filteredJobs = jobs.filter((job) =>
//     job.title.toLowerCase().includes(searchText.toLowerCase())
//   );

//   return (
//     <Box className="applicantsPage">
//       <Grid container className="mainGrid">
//         <Grid item xs={12} md={4} className="leftContainer">
//           <TextField
//             fullWidth
//             variant="outlined"
//             label="Search Jobs"
//             value={searchText}
//             onChange={handleSearchTextChange}
//             className="searchBar"
//           />
//           <Box className="jobList">
//             <List>
//               {filteredJobs.map((job) => (
//                 <ListItem
//                   key={job.id}
//                   button
//                   onClick={() => handleJobSelection(job)}
//                   className="jobListItem"
//                 >
//                   <ListItemText primary={job.title} />
//                 </ListItem>
//               ))}
//             </List>
//           </Box>
//         </Grid>
//         <Grid item xs={12} md={8} className="rightContainer">
//           {selectedJob ? (
//             <Card>
//               <CardContent>
//                 <Typography variant="h5" component="div">
//                   {selectedJob.title}
//                 </Typography>
//                 <Typography sx={{ mb: 1.5 }} color="text.secondary">
//                   {selectedJob.company_name}
//                 </Typography>
//                 <Typography sx={{ mb: 1.5 }} color="text.secondary">
//                   {selectedJob.location}
//                 </Typography>
//               </CardContent>
//             </Card>
//           ) : (
//             <Typography color="text.secondary">
//               Select a job to see its details
//             </Typography>
//           )}
//         </Grid>
//       </Grid>
//     </Box>
//   );
// }

// export default RecruiterApplicantsPage;











import React, { useState, useEffect } from "react";
import {
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  TextField,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import "../styles/RecruiterApplicant.css";

function RecruiterApplicantsPage() {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [searchText, setSearchText] = useState("");

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    const response = await fetch("https://chapi.techstartucalgary.com/jobs/me", {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    });
    if (response.ok) {
      const data = await response.json();
      console.log("Fetched jobs:", data);
      setJobs(data);
    } else {
      console.error("Failed to fetch jobs:", response.statusText);
    }
  };

  const handleJobSelection = (job) => {
    setSelectedJob(job);
  };

  const handleSearchTextChange = (e) => {
    setSearchText(e.target.value);
  };

  const filteredJobs = jobs.filter((job) =>
    job.title.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
    <Box className="applicantsPage">
      <Grid container className="mainGrid">
        <Grid item xs={12} md={4} className="leftContainer">
          <TextField
            fullWidth
            variant="outlined"
            label="Search Jobs"
            value={searchText}
            onChange={handleSearchTextChange}
            className="searchBar"
          />
          <Box className="jobList">
            <List>
              {filteredJobs.map((job) => (
                <ListItem
                  key={job.id}
                  button
                  onClick={() => handleJobSelection(job)}
                  className="jobListItem"
                >
                  <ListItemText primary={job.title} />
                </ListItem>
              ))}
            </List>
          </Box>
        </Grid>
        <Grid item xs={12} md={8} className="rightContainer">
          {selectedJob ? (
            <Card>
              <CardContent>
                <Typography variant="h5" component="div">
                  {selectedJob.title}
                </Typography>
                <Typography sx={{ mb: 1.5 }} color="text.secondary">
                  {selectedJob.company_name}
                </Typography>
                <Typography sx={{ mb: 1.5 }} color="text.secondary">
                  {selectedJob.location}
                </Typography>
              </CardContent>
            </Card>
          ) : (
            <Typography color="text.secondary">
              Select a job to see its details
            </Typography>
          )}
        </Grid>
      </Grid>
    </Box>
  );
}

export default RecruiterApplicantsPage;
