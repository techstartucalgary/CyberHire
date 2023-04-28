import React, { useState, useEffect } from "react";
import {
  Box,
  Container,
  Table,
  TableBody,
  TableCell,
  TableRow,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
} from "@mui/material";
import {
  Label,
  Iconify,
  Scrollbar,
  UserListHead,
  UserListToolbar,
} from "../components/RecruiterApplicantsComponents";
import defaultProfile from "../img/defaultProfile.jpg";
import GetAppIcon from "@mui/icons-material/GetApp";

const RecruiterApplicantsPage = () => {
  const [filterName, setFilterName] = useState("");
  const [applicants, setApplicants] = useState([]);
  const [jobIds, setJobIds] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogData, setDialogData] = useState({});

  const [resumeURL, setResumeURL] = useState("");
  const [open, setOpen] = useState(false);

  const [profilePictures, setProfilePictures] = useState({});

  useEffect(() => {
    fetchJobs();
  }, []);

  useEffect(() => {
    if (jobIds.length > 0) {
      jobIds.forEach((jobId) => {
        fetchApplicants(jobId);
      });
    }
  }, [jobIds]);

  const fetchJobs = async () => {
    try {
      const response = await fetch(
        "https://chapi.techstartucalgary.com/jobs/me",
        {
          method: "GET",
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        },
      );

      if (response.ok) {
        const data = await response.json();
        const jobIds = data.map((job) => job.id);
        setJobIds(jobIds);
      } else {
        console.error("Failed to fetch jobs for the recruiter");
      }
    } catch (error) {
      console.error(error);
    }
  };

  const fetchApplicants = async (jobId) => {
    try {
      const idsToFetch = jobId ? [jobId] : jobIds;
      let allApplicants = [];

      for (const id of idsToFetch) {
        const response = await fetch(
          `https://chapi.techstartucalgary.com/applications/${id}`,
          {
            method: "GET",
            mode: "cors",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          },
        );

        if (response.status === 404) {
          setApplicants([]);
        } else {
          const data = await response.json();

          // had to check if data is an array or not for error checking
          if (Array.isArray(data)) {
            const applicantsWithProfilePictures = await Promise.all(
              data.map(async (applicant) => {
                const profilePictureUrl = await fetchProfilePicture(
                  applicant.user_profile_id,
                );
                return { ...applicant, profile_picture: profilePictureUrl };
              }),
            );
            allApplicants = [
              ...allApplicants,
              ...applicantsWithProfilePictures,
            ];
          } else {
            setApplicants([]);
            console.error("Fetched data is not an array:", data);
          }
        }
      }

      setApplicants(allApplicants);
    } catch (error) {
      console.error(error);
    }
  };

  const handleDownloadClick = async (userId) => {
    const endpoint = `https://chapi.techstartucalgary.com/users/profile/${userId}/resume`;

    try {
      const response = await fetch(endpoint, {
        method: "GET",
        headers: {
          "Content-Type": "application/pdf",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch resume");
      }

      const blob = await response.blob();
      const objectURL = URL.createObjectURL(blob);
      setResumeURL(objectURL);
      setOpen(true);
    } catch (error) {
      console.error(error);
    }
  };

  const handleClose = () => {
    setOpen(false);
  };

  const fetchProfilePicture = async (userId) => {
    try {
      const response = await fetch(
        `https://chapi.techstartucalgary.com/users/profile/${userId}/profile_picture`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        },
      );

      if (response.ok) {
        const data = await response.blob();
        return URL.createObjectURL(data);
      } else {
        console.error("Failed to fetch profile picture");
        return defaultProfile;
      }
    } catch (error) {
      console.error(error);
      return defaultProfile;
    }
  };

  const handleFilterByName = (event) => {
    setFilterName(event.target.value);
  };

  const filteredApplicants = applicants.filter((applicant) =>
    `${applicant.applicant.first_name} ${applicant.applicant.last_name}`
      .toLowerCase()
      .includes(filterName.toLowerCase()),
  );

  const handleDialogOpen = (row) => {
    setDialogData(row);
    setDialogOpen(true);
  };

  const handleDialogClose = () => {
    setDialogOpen(false);
  };

  const handleUpdateStatus = async () => {
    try {
      const response = await fetch(
        `https://chapi.techstartucalgary.com/applications/${dialogData.job.id}_${dialogData.user_profile_id}/`,
        {
          method: "PATCH",
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify({
            new_status: dialogData.application_status.status,
            rejection_feedback: dialogData.application_status.feedback,
          }),
        },
      );

      if (response.ok) {
        fetchApplicants();
        handleDialogClose();
      } else {
        console.error("Failed to update the status");
      }
    } catch (error) {
      console.error(error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "SUBMITTED":
        return "success";
      case "UNDER REVIEW":
        return "info";
      case "UNDERGOING FURTHER SCREENING":
        return "warning";
      case "REJECTED":
        return "error";
      case "OFFER SENT":
        return "offerSent";
      default:
        return "secondary";
    }
  };

  return (
    <Container maxWidth="lg">
      <Box
        sx={{
          pb: 5,
          minHeight: "100px",
          borderRadius: "10px", // Testing - For now added inline styling
          boxShadow: 1,
          bgcolor: "background.page",
          marginTop: "30px",
        }}
      >
        <UserListToolbar
          filterName={filterName}
          onFilterName={handleFilterByName}
        />

        <Scrollbar>
          {filteredApplicants.length > 0 ? (
            <Table>
              <UserListHead
                order="asc"
                orderBy="name"
                headLabel={[
                  { id: "name", label: "Name", alignRight: false },
                  { id: "role", label: "Role", alignRight: false },
                  { id: "status", label: "Status", alignRight: false },
                  { id: "resume", label: "Resume", alignRight: false },
                  { id: "action", label: "Action", alignRight: false },
                ]}
                rowCount={filteredApplicants.length}
                onRequestSort={() => {}}
              />
              <TableBody>
                {filteredApplicants.map((row) => (
                  <TableRow key={row.user_profile_id} tabIndex={-1}>
                    <TableCell component="th" scope="row" padding="none">
                      <img
                        src={row.profile_picture || defaultProfile}
                        alt={""}
                        style={{
                          borderRadius: "50%",
                          width: "35px",
                          height: "35px",
                          marginRight: "8px",
                          marginLeft: "8px",
                          verticalAlign: "middle",
                        }}
                      />
                    </TableCell>
                    <TableCell component="th" scope="row" padding="none">
                      <Typography
                        variant="body1"
                        sx={{
                          margin: 0,
                          fontWeight: 600,
                          lineHeight: 1.57142,
                          fontSize: "0.875rem",
                          fontFamily: "Public Sans, sans-serif",
                          overflow: "hidden",
                          textOverflow: "ellipsis",
                          whiteSpace: "nowrap",
                          marginLeft: "8px",
                        }}
                      >
                        {`${row.applicant.first_name} ${row.applicant.last_name}`}
                      </Typography>
                    </TableCell>

                    <TableCell>{row.job.title}</TableCell>
                    <TableCell>
                      {/* <Label
                        color={
                          row.application_status.status === "SUBMITTED"
                            ? "success"
                            : "error"
                        }
                      >
                        {row.application_status.status}
                      </Label> */}
                      <Label
                        color={getStatusColor(row.application_status.status)}
                      >
                        {row.application_status.status}
                      </Label>
                    </TableCell>

                    <TableCell>
                      <Button
                        variant="outlined"
                        onClick={() => handleDownloadClick(row.user_profile_id)}
                        startIcon={<GetAppIcon />}
                        sx={{
                          whiteSpace: "nowrap",
                          overflow: "hidden",
                          textOverflow: "ellipsis",
                          bgcolor: "primary.main",
                          color: "white",
                          fontSize: "14px",
                          marginLeft: "6px",
                          marginRight: "0px",
                          fontWeight: "bold",
                          "&:hover": {
                            bgcolor: "primary.dark",
                          },
                        }}
                      ></Button>
                    </TableCell>

                    {/* </TableCell> */}
                    <TableCell>
                      <Button
                        variant="outlined"
                        onClick={() => handleDialogOpen(row)}
                        sx={{
                          whiteSpace: "nowrap",
                          overflow: "hidden",
                          textOverflow: "ellipsis",
                          border: "2px solid grey",
                          borderRadius: "4px",
                          color: "grey",
                          fontWeight: "bold",
                          padding: "6px 12px",
                          transition: "background-color 0.3s",
                          "&:hover": {
                            // backgroundColor: "#4CAF50",
                            backgroundColor: "primary.dark",
                            color: "#fff",
                          },
                        }}
                      >
                        Update Status
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <Box
              sx={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                height: 400,
              }}
            >
              <Iconify
                icon="ic:round-announcement"
                sx={{ color: "text.secondary", width: 80, height: 80 }}
              />
              <Typography variant="h5" sx={{ mt: 2, mb: 0.5 }}>
                Sorry, no applications found.
              </Typography>
            </Box>
          )}
        </Scrollbar>
      </Box>

      <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
        <DialogTitle>Resume</DialogTitle>
        <DialogContent>
          <iframe
            src={resumeURL}
            title="Resume"
            width="100%"
            height="600px"
          ></iframe>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Close</Button>
        </DialogActions>
      </Dialog>

      <Dialog
        open={dialogOpen}
        onClose={handleDialogClose}
        maxWidth="xs"
        fullWidth
      >
        <DialogTitle>Update Application Status</DialogTitle>
        <DialogContent>
          <FormControl fullWidth variant="outlined" sx={{ mb: 2 }}>
            <InputLabel>Status</InputLabel>
            <Select
              value={dialogData.application_status?.status || ""}
              onChange={(e) =>
                setDialogData({
                  ...dialogData,
                  application_status: {
                    ...dialogData.application_status,
                    status: e.target.value,
                  },
                })
              }
              label="Status"
            >
              <MenuItem value="SUBMITTED">SUBMITTED</MenuItem>
              <MenuItem value="UNDER REVIEW">UNDER REVIEW</MenuItem>
              <MenuItem value="UNDERGOING FURTHER SCREENING">
                UNDERGOING FURTHER SCREENING
              </MenuItem>
              <MenuItem value="REJECTED">REJECTED</MenuItem>
              <MenuItem value="OFFER SENT">OFFER SENT</MenuItem>
            </Select>
          </FormControl>
          <TextField
            fullWidth
            label="Rejection Feedback"
            variant="outlined"
            multiline
            rows={4}
            value={dialogData.application_status?.feedback || ""}
            onChange={(e) =>
              setDialogData({
                ...dialogData,
                application_status: {
                  ...dialogData.application_status,
                  feedback: e.target.value,
                },
              })
            }
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose}>Cancel</Button>
          <Button onClick={handleUpdateStatus} variant="contained">
            Update Status
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default RecruiterApplicantsPage;
