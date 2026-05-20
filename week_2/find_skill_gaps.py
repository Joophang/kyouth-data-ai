from pydantic import BaseModel
from typing import List
import sqlite3
import re

class SkillGapResult(BaseModel):
	gaps: List[str]

def get_required_skills(db_url: str) -> set[str]:
	conn = sqlite3.connect(db_url)
	cursor = conn.cursor()

	cursor.execute("SELECT tech_stack FROM jobs WHERE tech_stack IS NOT NULL AND tech_stack != ''")

	rows = cursor.fetchall()

	skills = set()

	for row in rows:
		tech_stack = row[0]
		for skill in tech_stack.split(","):
			if skill.strip():
				skills.add(skill.strip().lower())
	
	conn.close()
	return skills

def get_resume_skills(input_file_path: str, required_skills: set[str]) -> set[str]:
	with open(input_file_path, "r", encoding="utf-8") as file:
		content = file.read().lower()

		resume_skills = set()

		for skill in required_skills:
			pattern = r"\b" + re.escape(skill) + r"\b"

			if re.search(pattern, content):
				resume_skills.add(skill)

			if "c/c++" in content:
				resume_skills.add("c/c++")
				resume_skills.add("c")
				resume_skills.add("c++")
		
		return resume_skills

def find_skill_gaps(input_file_path: str, db_url: str) -> SkillGapResult:
	try:
		required_skills = get_required_skills(db_url)
		resume_skills = get_resume_skills(input_file_path, required_skills)
		gaps = sorted(required_skills - resume_skills)
		return SkillGapResult(gaps=gaps)
	
	except Exception as e:
		print(f"An error occurred: {str(e)}")
		return SkillGapResult(gaps=[])
	
if __name__ == "__main__":
	db_url = "jobs_d1.db"
	input_file_path = "resume_d3.txt"

	result = find_skill_gaps(input_file_path, db_url)

	print("Skill Gaps:")
	for gap in result.gaps:
		print(f"- {gap}")

