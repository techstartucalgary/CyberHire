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
        }
      );
      console.log(response);
      const data = await response.json();
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
