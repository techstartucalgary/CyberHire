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
  const [showGenericError, setShowGenericError] = useState(false);

  const handleSalaryChange = (e, newValue) => {
    setSalary(newValue);
  };

  const submitNewJob = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const min_salary = salary[0];
    const max_salary = salary[1];
    const title = formData.get("title");
    const description = formData.get("description");
    const location = formData.get("location");
    const data = {
      title,
      description,
      location,
      min_salary,
      max_salary,
    };

    await fetch("https://chapi.techstartucalgary.com/jobs", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (!response.ok) {
          if (response.status === 401) {
            window.location.href = "#/signin";
          } else {
            setShowGenericError(true);
          }
          throw new Error("Job creation failed");
        }
        props.closeModal();
      })
      .catch((error) => {
        console.error(error);
      });
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
      <form className="form" onSubmit={submitNewJob}>
        <TextField name="title" label="Job Title" required />
        <TextField
          name="description"
          label="Job Description"
          multiline
          required
        />
        <TextField name="location" label="Location" required />
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
          {showGenericError && (
            <Typography color="error">
              There was an error creating your job. Please try again.
            </Typography>
          )}
        </div>
        <div className="row right-align button-container">
          <Button variant="outlined" onClick={props.closeModal}>
            Cancel
          </Button>
          <Button type="submit" variant="contained">
            Post Job
          </Button>
        </div>
      </form>
    </Dialog>
  );
}

export default CreateJobModal;
