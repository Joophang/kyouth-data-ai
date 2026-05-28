from pydantic import BaseModel
from typing import List
import sqlite3
import re

class SkillGapResult(BaseModel):
	gaps: List[str]

# Define skill aliases for normalization
SKILL_ALIASES = {
    "c/c++": "c/c++",
    "c++": "c/c++",
    "c": "c/c++",
    "javascript": "javascript",
    "js": "javascript",
    "typescript": "typescript",
    "ts": "typescript",
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "mysql": "mysql",
    "sql": "sql",
}

def normalize_skill(skill: str) -> str:
	skill = skill.strip().lower()
	return SKILL_ALIASES.get(skill, skill)

def get_required_skills(db_url: str) -> set[str]:
	conn = sqlite3.connect(db_url)
	cursor = conn.cursor()

	# fetch all non-empty tech_stack values from the jobs table
	cursor.execute("SELECT tech_stack FROM jobs WHERE tech_stack IS NOT NULL AND tech_stack != ''")

	rows = cursor.fetchall()

	skills = set()

	# normalize and collect unique skills from the tech_stack values
	for row in rows:
		tech_stack = row[0]
		for skill in tech_stack.split(","):
			skill = normalize_skill(skill)
			if skill:
				skills.add(skill)
	
	conn.close()
	return skills

def get_resume_skills(resume_txt: str, required_skills: set[str]) -> set[str]:
	# read the resume content from the input file
		content = resume_txt.lower()

		resume_skills = set()

		# use regex to find the section of the technical skills
		match = re.search(
			r"technical skills\s*:?\s*(.*?)(\n\s*(education|experience|projects|work experience|certifications|languages)\s*:|\Z)",
			content,
			re.DOTALL
		)

		# if the technical skills section is found, extract and normalize the skills
		if match:
			skills_section = match.group(1)

			for skill in skills_section.split(","):
				skill = normalize_skill(skill)

				if skill in required_skills:
					resume_skills.add(skill)

		return resume_skills

def find_skill_gaps(resume_txt: str, db_url: str) -> SkillGapResult:
	try:
		required_skills = get_required_skills(db_url)
		resume_skills = get_resume_skills(resume_txt, required_skills)
		gaps = sorted(required_skills - resume_skills)
		print(f"Required skills: {gaps}")
		return SkillGapResult(gaps=gaps)
	
	except Exception as e:
		print(f"An error occurred: {str(e)}")
		return SkillGapResult(gaps=[])
	