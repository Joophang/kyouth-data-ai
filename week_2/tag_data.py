import os
import sqlite3
import time
from dotenv import load_dotenv
from prompt_model import prompt_model

BATCH_SIZE = 5
RETRY_LIMIT = 3
RETRY_DELAY = 3  # seconds

def build_prompt(jobs):
	prompt = """
	Extract the technical skills / tech stack from each job description.

	Return ONLY this format:
	<job_id>: skill1, skill2, skill3

	Example:
	12345: Python, SQL, Git
	67890: Java, Spring Boot, REST API

	Rules:
	- One line per job
	- Do not include explanation
	- Do not use bullet points
	- Use comma-separated values only
	- If no technical skill is found, write: General IT
	"""
	
	for source_id, description in jobs:
		prompt += f"\nsource_id: {source_id}\n"
		prompt += f"description: {description}\n"

	return prompt

def parse_response(response_text):
	results = {}

	for line in response_text.splitlines():
		if ":" not in line:
			continue

		source_id, tech_stack = line.split(":", 1)
		source_id = source_id.strip()
		tech_stack = tech_stack.strip()

		if source_id and tech_stack:
			results[source_id] = tech_stack
	
	return results
	
def tag_data(db_url: str):
	load_dotenv()  # Load environment variables from .env file
	try:
		conn = sqlite3.connect(db_url)
		cursor = conn.cursor()

		# reset
		cursor.execute("UPDATE jobs SET tech_stack = NULL")
		conn.commit()

		while True:

			cursor.execute("""
					SELECT source_id, description FROM jobs WHERE tech_stack IS NULL OR tech_stack = '' LIMIT ?
					""", (BATCH_SIZE,))
			
			jobs = cursor.fetchall()

			if not jobs:
				print("No jobs found that require tagging.")
				break

			prompt = build_prompt(jobs)
			success = False
			
			for attempt in range(1, RETRY_LIMIT + 1):
				try:
					response_text = prompt_model( "gemini-2.5-flash", prompt)

					if (
						not response_text
						or "Error:" in response_text
						or "An error occurred" in response_text
						or "429" in response_text
						or "quota" in response_text.lower()
					):
						print(f"[Batch] Attempt {attempt}: failed: {response_text}")
						time.sleep(RETRY_DELAY)
						continue

					parsed_response = parse_response(response_text)

					if len(parsed_response) != len(jobs):
						print(f"[Batch] Attempt {attempt}: Mismatch in number of responses. Expected {len(jobs)}, got {len(parsed_response)}. Response: {response_text}")
						time.sleep(RETRY_DELAY)
						continue

					for source_id, _ in jobs:
						source_id_str = str(source_id)
						tech_stack = parsed_response.get(source_id_str, "")

						if tech_stack:
							cursor.execute("""
								UPDATE jobs SET tech_stack = ? WHERE source_id = ?
							""", (tech_stack, source_id))
							print(f"Analyzed job {source_id}: {tech_stack}")

					conn.commit()
					success = True
					break

				except Exception as e:
					print(f"[Batch] Attemp {attempt} failed: {str(e)}")
					time.sleep(RETRY_DELAY)
			
			if not success:
				print("Skipping failed batch")
				break

	except Exception as e:
		print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    tag_data("jobs_d1.db")	

	