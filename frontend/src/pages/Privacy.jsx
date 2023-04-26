import { Box, List, ListItem, Typography } from "@mui/material";
import React from "react";
import "../styles/privacy.css";

<link
  rel="stylesheet"
  href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
/>;

function PrivacyPolicy() {
  return (
    <Box className="textBox">
      <Typography variant="h1" color="primary" mb={"10%"}>
        Privacy Policy.
      </Typography>
      <Typography variant="h5" mb={"10%"}>
        This Privacy Policy sets out how CyberHire (the "Website"), collects,
        uses, and protects any personal information that you provide to us.
        <br />
        We are committed to ensuring that your privacy is protected. Should we
        ask you to provide certain information by which you can be identified
        when using this Website, then you can be assured that it will only be
        used in accordance with this Privacy Policy.
        <br />
        <br />
        We may collect the following personal information:
        <br />
        <List>
          <ListItem>First and last name</ListItem>
          <ListItem>Email address</ListItem>
          <ListItem>Resume</ListItem>
        </List>
        We use this personal information to:
        <br />
        <List>
          <ListItem>Facilitate the job search and application process</ListItem>
          <ListItem>Communicate with you regarding job opportunities</ListItem>
          <ListItem>Improve our Website and services</ListItem>
          <ListItem>
            Allow recruiters on our platform to view your resume and contact you
            about job opportunities
          </ListItem>
        </List>
        <br />
        We will not sell, distribute or lease your personal information to third
        parties unless we have your permission or are required by law to do so.
        <br />
        We store your personal information on Amazon Relational Database Service
        (RDS). Your personal information is stored on servers that are part of
        the Amazon Web Services (AWS) infrastructure and are subject to AWS
        privacy standards. AWS has achieved internationally recognized
        certifications and accreditations for compliance with privacy assurance
        frameworks, such as ISO 27017 for cloud security, ISO 27701 for privacy
        information management, and ISO 27018 for cloud privacy.
        <br />
        We take the security of your data very seriously, and have implemented
        strict access controls and monitoring mechanisms to ensure that only
        authorized personnel have access to personal information.
        <br />
        You have the right to access your personal information and request that
        it be corrected or deleted. You may also make a complaint about our
        handling of your personal information. To exercise these rights, please
        contact our Privacy Compliance Officer at{" "}
        <a href="mailto:cyberhiretsu+privacy@gmail.com">
          cyberhiretsu+privacy@gmail.com
        </a>
        . We will fulfill your request within 30 days.
        <br />
        We may update this Privacy Policy from time to time by updating this
        page. You should check this page from time to time to ensure that you
        are happy with any changes.
        <br />
        This Privacy Policy is compliant with Canada's Personal Information
        Protection and Electronic Documents Act (PIPEDA).
        <br />
        By using our Website, you consent to our collection, use, and storage of
        your personal information as described in this Privacy Policy. If you
        have any questions or concerns, please contact our Privacy Compliance
        Officer at{" "}
        <a href="mailto:cyberhiretsu+privacy@gmail.com">
          cyberhiretsu+privacy@gmail.com
        </a>
        .
      </Typography>
    </Box>
  );
}

export default PrivacyPolicy;
