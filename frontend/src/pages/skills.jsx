import React, { useState } from "react";
import { Autocomplete } from "@mui/material";
import { Typography, TextField, Button } from "@mui/material";

const skills = [
  "JavaScript",
  "TypeScript",
  "React",
  "Angular",
  "Vue.js",
  "Node.js",
  "Express.js",
  "Django",
  "Flask",
  "Python",
  "Java",
  "C#",
  "PHP",
  "Ruby",
  "Swift",
];

function SkillsSelector() {
  const [selectedSkills, setSelectedSkills] = useState([]);

  const handleSkillSelection = (event, value) => {
    setSelectedSkills(value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch(
        "https://chapi.techstartucalgary.com/users/profile/me/skills",
        {
          method: "POST",
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify(selectedSkills.map((skill) => ({ skill }))),
        },
      );
      console.log(response);
      const data = await response.json();
      if (response.ok) {
        window.location.href = "#/app";
      }
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ margin: "40px", marginTop: "60px" }}>
      <Typography variant="h3" align="center" gutterBottom>
        Choose Skills
      </Typography>
      <Autocomplete
        multiple
        options={skills}
        value={selectedSkills}
        onChange={handleSkillSelection}
        renderInput={(params) => (
          <TextField {...params} label="Choose Skills" variant="outlined" />
        )}
      />
      <Button
        style={{ marginTop: "30px" }}
        type="submit"
        variant="contained"
        color="primary"
        fullWidth
        onClick={handleSubmit}
      >
        Add Your Skills
      </Button>
    </div>
  );
}

export default SkillsSelector;

// import React, { useState, useEffect } from "react";

// const App = () => {
//   const [profilePictureDataUrl, setProfilePictureDataUrl] = useState(null);

//   useEffect(() => {
//     const fetchProfilePicture = async () => {
//       try {
//         const response = await fetch(
//           "https://chapi.techstartucalgary.com/users/profile/171/profile_picture",
//           {
//             method: "GET",
//             headers: {
//               "Content-Type": "application/json",
//               Authorization: `Bearer ${localStorage.getItem("access_token")}`,
//             },
//           },
//         );

//         if (!response.ok) {
//           throw new Error(`Failed to fetch profile picture for user: ${171}`);
//         }

//         const dataUrl = await response.text();
//         setProfilePictureDataUrl(dataUrl);
//       } catch (error) {
//         console.error(`Failed to fetch profile picture for user: 171`);
//         setProfilePictureDataUrl(null);
//       }
//     };

//     fetchProfilePicture();
//   }, []);

//   return (
//     <div>
//       {profilePictureDataUrl ? (
//         <img src={profilePictureDataUrl} alt="Profile Picture" />
//       ) : (
//         <p>Profile picture not available</p>
//       )}
//     </div>
//   );
// };

// export default App;

// import React, { useState } from 'react';
// import { Button, Dialog, DialogTitle, DialogContent } from '@mui/material';

// function DownloadResumeButton() {
//   const [open, setOpen] = useState(false);
//   const [resumeURL, setResumeURL] = useState(null);

//   const userId = 171;
//   const endpoint = `https://chapi.techstartucalgary.com/users/profile/${userId}/resume`;

//   const handleDownloadClick = async () => {
//     try {
//       const response = await fetch(endpoint, {
//         method: 'GET',
//         headers: {
//           'Content-Type': 'application/pdf',
//           Authorization: `Bearer ${localStorage.getItem('access_token')}`,
//         },
//       });

//       if (!response.ok) {
//         throw new Error('Failed to fetch resume');
//       }

//       const blob = await response.blob();
//       const objectURL = URL.createObjectURL(blob);
//       setResumeURL(objectURL);
//       setOpen(true);
//     } catch (error) {
//       console.error(error);
//     }
//   };

//   const handleClose = () => {
//     setOpen(false);
//   };

//   return (
//     <>
//       <Button variant="contained" color="primary" onClick={handleDownloadClick}>
//         Download Resume
//       </Button>
//       <Dialog
//         open={open}
//         onClose={handleClose}
//         maxWidth="md"
//         fullWidth
//         PaperProps={{
//           style: {
//             height: '90%',
//             overflow: 'hidden',
//           },
//         }}
//       >
//         <DialogTitle>Resume</DialogTitle>
//         <DialogContent>
//           {resumeURL && (
//             <iframe
//               src={resumeURL}
//               title="Resume"
//               width="100%"
//               height="100%"
//               style={{ border: 'none' }}
//             ></iframe>
//           )}
//         </DialogContent>
//       </Dialog>
//     </>
//   );
// }

// export default DownloadResumeButton;
