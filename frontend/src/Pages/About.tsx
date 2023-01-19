import React from "react";
import logo from "../logo.svg";
import "../App.css";

function About() {
	return (
		<div className="App">
			<header className="App-header">
				<img src={logo} className="App-logo" alt="logo" />
			</header>
			<h1>
				<title>About Our Company</title>
				<link></link>
			</h1>

			<h2>Our Story</h2>
			<p>
				{" "}
				CyberHire was kickstarted by a group of 6 multidisciplinary
				individuals from the University of Calgary Tech Start club for
				university students. Our team's vision originated from sharing
				the pain of the job seeking experience, which motivated us to
				make the process more intuitive and stress free for everyone
				else. We'll be starting out with the focus of marketing towards
				tech students due to one of our main competitive advantages
				being primarily a group of tech concentration students. However
				we do have a focus of expanding into other concentrations and
				niches of the job market once our website has seen an
				significant amount of impact within our initial target market.
			</p>
			<h2>Our Team</h2>
			<div className="team-member">
				<img src="/public/team-member-1.jpg" alt="Team Member 1"></img>
				<h3>Ben Schmidt</h3>
				<p>Project Manager</p>
			</div>
			<div className="team-member">
				<img src="/public/team-member-2.jpg" alt="Team Member 2"></img>
				<h3>Ana Garza </h3>
				<p> Junior Frontend Developer</p>
			</div>
			<div className="team-member">
				<img src="/public/team-member-3.jpg" alt="Team Member 3"></img>
				<h3>Suhaib Tariq </h3>
				<p>Developer</p>
			</div>
			<div className="team-member">
				<img src="/public/team-member-4.jpg" alt="Team Member 4"></img>
				<h3>Ling Lee</h3>
				<p>Fullstack Developer</p>
			</div>
			<div className="team-member">
				<img src="/public/team-member-5.jpg" alt="Team Member 4"></img>
				<h3>Bernard Aire</h3>
				<p>Frontend Developer</p>
			</div>
			<div className="team-member">
				<img src="/public/team-member-6.jpg" alt="Team Member 4"></img>
				<h3>Etta Liu</h3>
				<p>Business Strategist & Frontend Developer</p>
			</div>

			<footer>
				<p>Copyright 2022 CyberHire</p>
			</footer>
		</div>
	);
}

export default About;
