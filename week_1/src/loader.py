import sqlite3
import json

def load_all_jsons(input_dir, output_dir):
	if (not input_dir.exists()):
		print(f"⚠️ Input directory does not exist: {input_dir}")
		return
	if (not output_dir.exists()):
		output_dir.mkdir(parents=True)

	print("\n🥇 Gold:...")
	
	db_path = output_dir / "jobs.db"

	# always delete old DB first
	if db_path.exists():
		db_path.unlink()

	# create db file
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()

	# create table
	cursor.execute(
	"""
	CREATE TABLE if NOT EXISTS jobs (
		source_id TEXT PRIMARY KEY,
		job_title TEXT,
		company TEXT,
		description TEXT,
		tech_stack TEXT)
	""")

	conn.commit()

	inserted_count = 0
	for file in input_dir.glob("*.json"):
		with open(file, "r", encoding="utf-8") as f:
			job_data = json.load(f)

			cursor.execute(
				"""
				INSERT OR IGNORE INTO jobs (source_id, job_title, company, description)
				VALUES (?, ?, ?, ?)
				""",
				(
					job_data["source_id"],
					job_data["job_title"],
					job_data["company"],
					job_data["description"]
				)
			)
			if cursor.rowcount == 1:
				print(f"✅ Inserted: {file.name}")
				inserted_count += 1
			else:
				print(f"⚠️ Skipped (duplicate): {file.name}")

	conn.commit()
	conn.close()

	total = len(list(input_dir.glob("*.json")))
	print("\n📊 Gold Summary:")
	print(f"Total: {total} | Inserted: {inserted_count} | Skipped: {total - inserted_count}")


