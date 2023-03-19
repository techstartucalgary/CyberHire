export interface Job {
  id: number;
  user_profile_id: number;
  title: string;
  description: string;
  location: string;
  min_salary: number;
  max_salary: number;
  skills: [
    Skill,
  ];
  owner: Owner;
}

export interface Skill {
    id: number;
    skill: string;
}

export interface Owner {
    user_id: number;
    company: string;
    first_name: string;
    last_name: string;
    profile_picture: File;
    resume: File;
}