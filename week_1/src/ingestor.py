import email.message
import quopri

def ingest_all_mhtml(input_dir, output_dir):
	if (not input_dir.exists()):
		print(f"⚠️ Input directory does not exist: {input_dir}")
		return
	if (not output_dir.exists()):
		output_dir.mkdir(parents=True)
	print("🥉 Bronze:...")
	
	# iterate through all mhtml files
	for file in input_dir.glob("*.mhtml"):
		with open(file, "r") as f:
			has_html = False

			# convert email file to email message object
			msg = email.message_from_file(f)
			
			# iterate through the parts of email
			for part in msg.walk():
				# decode html content and write to output directory
				if part.get_content_type() == "text/html":
					has_html = True
					payload = part.get_payload(decode=True)
					html = payload.decode("utf-8", errors="replace")

					output_file = output_dir / (file.stem + ".html")
					with open(output_file, "w") as out_f:
						out_f.write(html)
					break
			
			if has_html:
				print(f"✅ Extracted: {file.name}")
			else:
				print(f"⚠️ No HTML content found in: {file.name}")

	total = len(list(input_dir.glob("*.mhtml")))
	extracted_count = len(list(output_dir.glob("*.html")))
	print("\n📊 Bronze Summary:")
	print(f"Total: {total} | Extracted: {extracted_count} | Failed: {total - extracted_count}")
