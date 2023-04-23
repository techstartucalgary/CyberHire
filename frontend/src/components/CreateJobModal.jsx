import React, { useState } from "react";
import {
  Button,
  Typography,
  Dialog,
  DialogTitle,
  TextField,
  Slider,
  FormControlLabel,
  Switch,
} from "@mui/material";

import "../styles/Modal.css";

function CreateJobModal(props) {
  const [showSalary, setShowSalary] = useState(false);
  const [salary, setSalary] = useState([0, 0]);
  // const [showGenericError, setShowGenericError] = useState(false);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const [company_name, setCompanyName] = useState(""); //  added Company Name in order to Get Job Posted by Recruiter

  const handleSalaryChange = (e, newValue) => {
    setSalary(newValue);
  };

  const submitNewJob = async () => {
    try {
      const response = await fetch("https://chapi.techstartucalgary.com/jobs", {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify({
          title,
          location,
          description,
          min_salary: salary[0],
          max_salary: salary[1],
          company_name, // added company name 
        }),
      });

      if (!response.ok) {
        throw new Error("Job creation failed");
      }

      props.closeModal();
    } catch (error) {
      console.error(error);
    }
  };

  const formatCurrency = (num) => {
    return num.toLocaleString("en-US", {
      style: "currency",
      currency: "CAD",
      maximumFractionDigits: 0,
    });
  };

  return (
    <Dialog open={props.open} fullWidth>
      <DialogTitle>Create New Job</DialogTitle>
      <form className="form" onSubmit={(e) => e.preventDefault()}>
        <TextField
          name="title"
          label="Job Title"
          required
          onChange={(e) => setTitle(e.target.value)}
        />
        <TextField
          name="description"
          label="Job Description"
          multiline
          required
          onChange={(e) => setDescription(e.target.value)}
        />
        <TextField
          name="location"
          label="Location"
          required
          onChange={(e) => setLocation(e.target.value)}
        />
        <TextField
          name="company_name"
          label="Company Name"
          required
          onChange={(e) => setCompanyName(e.target.value)} 
        />
        <FormControlLabel
          control={
            <Switch
              checked={showSalary}
              onChange={(e) => setShowSalary(e.target.checked)}
            />
          }
          label="Include Salary?"
        />

        {showSalary && (
          <div>
            <Typography>Salary Range</Typography>
            <Slider
              value={salary}
              onChange={handleSalaryChange}
              min={0}
              max={1000000}
              step={5000}
              valueLabelFormat={formatCurrency}
              valueLabelDisplay="on"
            />
          </div>
        )}
        <div className="row right-align">
         (
            <Typography color="error">
              There was an error creating your job. Please try again.
            </Typography>
          )
        </div>
        <div className="row right-align button-container">
        <Button variant="outlined" onClick={(e) => {e.preventDefault(); props.closeModal();}}>

            Cancel
          </Button>
            <Button
              variant="contained"
              color="primary"
              type="submit"
              onClick={submitNewJob}
              disabled={!title || !description || !location || !company_name} // Disable the button if any of these fields are empty
            >
              Create Job
            </Button>

        </div>
      </form>
    </Dialog>
  );
}

export default CreateJobModal;
