import sqlite3

def run_data_profile(db_path):
	if (not db_path.exists()):
		print(f"⚠️ Database file does not exist: {db_path}")
		return
	print("\n--- 🔍 DATA QUALITY REPORT ---")
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	cursor.execute("SELECT COUNT(*) FROM jobs")
	total_jobs = cursor.fetchone()[0]
	print(f"📈Total Reecords: {total_jobs}")

	cursor.execute("SELECT COUNT(*) FROM jobs WHERE job_title IS NULL OR job_title = ''")
	null_job_titles = cursor.fetchone()[0]

	cursor.execute("SELECT COUNT(*) FROM jobs WHERE company IS NULL OR company = ''")
	null_companies = cursor.fetchone()[0]

	cursor.execute("SELECT COUNT(*) FROM jobs WHERE description IS NULL OR description = ''")
	null_descriptions = cursor.fetchone()[0]	

	print(f"❓ Missing Values -> Job Title: {null_job_titles}, Company: {null_companies}, Description: {null_descriptions}")

	cursor.execute("SELECT AVG(LENGTH(description)) FROM jobs")
	avg_description_length = cursor.fetchone()[0]
	print(f"📝 Avg Description Length: {int(avg_description_length)} chars")

	cursor.execute("SELECT source_id, job_title, LENGTH(description) As description_length FROM jobs ORDER BY LENGTH(description) ASC LIMIT 1")
	min_desc_record = cursor.fetchone()
	print(f"⚠️  Shortest Description: {min_desc_record[2]} chars\n  ↳ source_id: {min_desc_record[0]} | job_title: {min_desc_record[1]}")

	cursor.execute("SELECT source_id, job_title, LENGTH(description) As description_length FROM jobs ORDER BY LENGTH(description) DESC LIMIT 1")
	max_desc_record = cursor.fetchone()
	print(f"✅ Longest Description: {max_desc_record[2]} chars\n  ↳ source_id: {max_desc_record[0]} | job_title: {max_desc_record[1]}")
