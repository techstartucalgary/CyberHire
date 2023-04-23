import React, { useEffect, useState } from 'react';
import {
  Button,
  Typography,
  Dialog,
  DialogTitle,
  TextField,
  Slider,
  FormControlLabel,
  Switch,
  Autocomplete,
} from '@mui/material';

import '../styles/Modal.css';

const skills = [
  'Python',
'Java',
'SQL',
'JavaScript',
'C++',
'C#',
'C',
];

function CreateJobModal(props) {
  const [isEditing, setIsEditing] = useState(false);
  const [showSalary, setShowSalary] = useState(false);
  const [salary, setSalary] = useState([0, 0]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState('');
  const [company_name, setCompanyName] = useState('');
  const [showGenericError, setShowGenericError] = useState(false);

  const [selectedSkills, setSelectedSkills] = useState([]);

  useEffect(() => {
    if (props.job) {
      setIsEditing(true);
      setTitle(props.job.title);
      setDescription(props.job.description);
      setLocation(props.job.location);
      setCompanyName(props.job.company_name);
      if (props.job.min_salary) {
        setShowSalary(true);
        setSalary([props.job.min_salary, props.job.max_salary]);
      }
    }
  }, [props]);

  const handleSalaryChange = (e, newValue) => {
    setSalary(newValue);
  };

  const handleSkillSelection = (event, value) => {
    setSelectedSkills(value);
  };

  const submitJobSkills = async (jobId, skills) => {
    await fetch(`https://chapi.techstartucalgary.com/jobs/skills/${jobId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: JSON.stringify(skills.map((skill) => ({ skill }))),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Skills update failed');
        }
      })
      .catch((error) => {
        console.error(error);
      });
  };
  

  const submitNewJob = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const min_salary = salary[0];
    const max_salary = salary[1];
    const title = formData.get('title');
    const description = formData.get('description');
    const location = formData.get('location');
    const company_name = formData.get('company_name');
    const data = {
      title,
      description,
      location,
      min_salary,
      max_salary,
      company_name,
      skills: selectedSkills.map((skill) => ({ skill })),
    };

    if (isEditing) {
      await fetch(`https://chapi.techstartucalgary.com/jobs/${props.job.id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify(data),
      })
        .then(async (response) => {
          if (!response.ok) {
            if (response.status === 401) {
              window.location.href = '#/signin';
            } else {
              setShowGenericError(true);
            }
            throw new Error('Job creation failed');
          }
          await submitJobSkills(props.job.id, selectedSkills);
          cancelModal();
        })
        .catch((error) => {
          console.error(error);
        });
    } else {
      await fetch('https://chapi.techstartucalgary.com/jobs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify(data),
      })
        .then(async (response) => {
          if (!response.ok) {
            if (response.status === 401) {
              window.location.href = '#/signin';
            } else {
              setShowGenericError(true)
            }
            throw new Error('Job creation failed');
          }
          const jobData = await response.json();
          await submitJobSkills(jobData.id, selectedSkills);
          props.closeModal();
        })
        .catch((error) => {
          console.error(error);
        });
    }
  };

  
  const formatCurrency = (num) => {
  return num.toLocaleString('en-US', {
  style: 'currency',
  currency: 'CAD',
  maximumFractionDigits: 0,
  });
  };
  
  const cancelModal = () => {
  setTitle('');
  setDescription('');
  setLocation('');
  setCompanyName('');
  setShowSalary(false);
  setShowGenericError(false);
  setSalary([0, 0]);
  setIsEditing(false);
  props.closeModal();
  };

  return (
    <Dialog open={props.open} fullWidth>
    <DialogTitle>
  {isEditing ? 'Update Existing Job' : 'Create New Job'}
</DialogTitle>

    <form id="jobForm" className="form" onSubmit={submitNewJob}>
    <TextField
    name="title"
    label="Job Title"
    onChange={(e) => setTitle(e.target.value)}
    value={title}
    required
    />
    <TextField
    name="description"
    label="Job Description"
    onChange={(e) => setDescription(e.target.value)}
    value={description}
    multiline
    required
    />
    <TextField
    name="location"
    label="Location"
    onChange={(e) => setLocation(e.target.value)}
    value={location}
    required
    />
    <Autocomplete
    multiple
    options={skills}
    value={selectedSkills}
    onChange={handleSkillSelection}
    renderInput={(params) => (
    <TextField
    {...params}
    label="Required Skills"
    variant="outlined"
    />
    )}
    />
    <TextField
    name="company_name"
    label="Company Name"
    onChange={(e) => setCompanyName(e.target.value)}
    value={company_name}
    required
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
      {showGenericError && (
        <Typography color="error">
          There was an error creating your job. Please try again.
        </Typography>
      )}
    </div>
    <div className="row right-align button-container">
      <Button variant="outlined" onClick={cancelModal}>
        Cancel
      </Button>
      <Button type="submit" variant="contained">
        {isEditing ? `Update Job` : `Post Job`}
      </Button>
    </div>
  </form>
</Dialog>
);

  
}

export default CreateJobModal;
