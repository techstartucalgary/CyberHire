import React, { useState } from "react";
import {
  Container,
  Typography,
  TextField,
  Button,
  Grid,
  IconButton,
  Avatar,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

function EditProfile() {
  const [profileData, setProfileData] = useState({
    firstName: "",
    lastName: "",
    profilePicture: undefined,
    resume: undefined,
  });

  function handleChange(event) {
    const { name, value } = event.target;
    setProfileData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  }

  function handleProfilePictureChange(event) {
    const selectedFile = event.target.files?.[0];
    setProfileData((prevData) => ({
      ...prevData,
      profilePicture: selectedFile,
    }));
  }

  function handleResumeChange(event) {
    const selectedFile = event.target.files?.[0];
    setProfileData((prevData) => ({
      ...prevData,
      resume: selectedFile,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const profileFormData = {
      first_name: profileData.firstName,
      last_name: profileData.lastName,
    };

    try {
      const response = await fetch(
        "https://chapi.techstartucalgary.com/users/profile/me",
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify(profileFormData),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to create profile");
      }

      const data = await response.json();
      console.log(data);

      if (profileData.profilePicture) {
        const imageFormData = new FormData();
        imageFormData.append("profile_picture", profileData.profilePicture);

        const imageResponse = await fetch(
          "https://chapi.techstartucalgary.com/users/profile/profile_picture",
          {
            method: "PATCH",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
            body: imageFormData,
          }
        );

        if (!imageResponse.ok) {
          throw new Error("Failed to update profile picture");
        }
      }

      if (profileData.resume) {
        const resumeFormData = new FormData();
        resumeFormData.append("resume", profileData.resume);

        const resumeResponse = await fetch(
          "https://chapi.techstartucalgary.com/users/profile/resume",
          {
            method: "PATCH",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
            body: resumeFormData,
          }
        );

        if (!resumeResponse.ok) {
          throw new Error("Failed to update resume");
        }
      }
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <Container maxWidth="sm">
      <Typography variant="h1" align="center" gutterBottom>
        Edit Profile
      </Typography>

      <form onSubmit={handleSubmit}>
        <Grid
          item
          xs={12}
          container
          justifyContent="center"
          style={{ marginBottom: "15px" }}
        >
          <input
            type="file"
            id="profilePicture"
            name="profilePicture"
            onChange={handleProfilePictureChange}
            style={{ display: "none" }}
          />
          <label htmlFor="profilePicture">
            <IconButton
              color="primary"
              aria-label="upload picture"
              component="span"
            >
              <Avatar
                alt="Profile Picture"
                src={
                  profileData.profilePicture
                    ? URL.createObjectURL(profileData.profilePicture)
                    : ""
                }
              />
              <span style={{ marginLeft: 10 }}>Upload Profile</span>
            </IconButton>
            <input
              id="profilePicture"
              accept="image/*"
              type="file"
              onChange={(e) => handleProfilePictureChange(e)}
              hidden
            />
          </label>
        </Grid>

        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField
              label="First Name"
              name="firstName"
              value={profileData.firstName}
              onChange={handleChange}
              fullWidth
              required
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              label="Last Name"
              name="lastName"
              value={profileData.lastName}
              onChange={handleChange}
              fullWidth
              required
            />
          </Grid>
          <Grid
            item
            xs={12}
            style={{ marginBottom: "15px", marginTop: "15px" }}
          >
            <input
              type="file"
              id="resume"
              name="resume"
              accept="application/pdf"
              onChange={handleResumeChange}
              style={{ display: "none" }}
            />
            <label htmlFor="resume">
              <Button
                variant="contained"
                color="primary"
                aria-label="upload picture"
                component="span"
                startIcon={<CloudUploadIcon />}
                fullWidth
              >
                {profileData.resume ? profileData.resume.name : "Upload Resume"}
              </Button>
            </label>
          </Grid>
          <Grid item xs={12}>
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Update
            </Button>
          </Grid>
        </Grid>
      </form>
    </Container>
  );
}
export default EditProfile;
