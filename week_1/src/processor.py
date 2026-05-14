from bs4 import BeautifulSoup
from pydantic import BaseModel
import json

class JobListing(BaseModel):
	source_id: str
	job_title: str
	description: str
	company: str

def process_all_html(input_dir, output_dir):
	if (not input_dir.exists()):
		print(f"⚠️ Input directory does not exist: {input_dir}")
		return
	if (not output_dir.exists()):
		output_dir.mkdir(parents=True)

	# clean output directory
	for file in output_dir.iterdir():
		if file.is_file():
			file.unlink()

	print("\n🥈 Silver:...")

	total = 0
	processed_count = 0

	for file in input_dir.glob("*.html"):

		with open(file, "r", encoding="utf-8") as f:
			total += 1
			soup = BeautifulSoup(f, "html.parser")

			source_id_tag = soup.find("meta", property="og:url")
			if source_id_tag:
				source_id_url = source_id_tag.get("content", "")
				source_id = source_id_url.rstrip("/").split("/")[-1]
				if not source_id:
					print(f"⚠️  Missing source_id in: {file.name}");
					continue

			else:
				print(f"⚠️  Missing source_id in: {file.name}")
				continue

			job_title_tag = soup.find(attrs = {"data-automation": "job-detail-title"})
			if job_title_tag:
				job_title = job_title_tag.get_text(separator=" ", strip=True)
				if not job_title:
					print(f"⚠️  Missing job title in: {file.name}");
					continue
				# print(job_title)
			else:
				print(f"⚠️  Missing job title in: {file.name}")
				continue

			# description_tag = soup.find("meta", attrs={"property": "og:description"})
			description_tag = soup.find(attrs = {"data-automation": "jobAdDetails"})
			if description_tag:
				description = description_tag.get_text(separator=" ", strip=True)
				if not description:
					print(f"⚠️  Missing description in: {file.name}");
					continue
			else:
				print(f"⚠️  Missing description in: {file.name}")
				continue

			company_tag = soup.find(attrs = {"data-automation": "advertiser-name"})
			if company_tag:
				company = company_tag.get_text(separator=" ", strip=True)
				if not company:
					print(f"⚠️  Missing company in: {file.name}");
					continue
			else:
				print(f"⚠️  Missing company in: {file.name}")
				continue

			processed_count += 1

			job = JobListing(
				source_id=source_id,
				job_title=job_title,
				description=description,
				company=company
			)

			output_file = output_dir / (file.stem + ".json")

			with open(output_file, "w", encoding="utf-8") as out_f:
				json.dump(job.model_dump(), out_f, ensure_ascii=False, indent=4)
			# print(f"✅ Processed: {file.name}")

	print("\n📊 Silver Summary:")
	print(f"Total: {total} | Processed: {processed_count} | Skipped: {total - processed_count}")
