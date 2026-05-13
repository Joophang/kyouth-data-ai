## Project Description

This project builds a local data engineering pipeline that extracts raw job data from source files, processes the data into a clean structured format, and loads the final records into a SQLite relational database named `jobs.db`.

The pipeline is divided into three stages:

1. **Bronze** — Extract HTML content from raw `.mhtml` files in `0_source`.
2. **Silver** — Parse the extracted `.html` files and convert job listings into structured `.json` files.
3. **Gold** — Load the cleaned JSON records into a SQLite database.

The goal is to create a reproducible local pipeline that can transform unstructured job posting data into a queryable database.



## Setup instructions
### Prerequisites

Make sure the following tools are installed:

- Python 3.12 or above
- `uv` package manager
- Git

### Install uv

On macOS or Linux:

run:
	```curl -LsSf https://astral.sh/uv/install.sh | sh```

###  Set up Python environment
1. From the project root directory, run:
	```uv python install```.
2. Initialize the project if it has not been initialized:
	```uv init```.
3. Create a virtual environment:
	```uv venv```.
4. Activate the virtual environment:
	```source .venv/bin/activate```.

### Install dependencies
Install the required packages:
	```uv add bs4 ruff pydantic```

## Usage

1. Run Bronze stage:
	```python main.py ingest```.
This reads .mhtml files from 0_source and writes extracted .html files into the Bronze output folder.

2. Run Silver stage:
	```python main.py process```.
This reads extracted .html files and creates structured .json job listing files.

3. Run Gold stage:
	```python main.py load```.
This reads the cleaned JSON files and loads them into ```jobs.db```

4. Run all stages:
	```python main.py all```.
This executes the full pipeline:

---

### Module 1: The Extractor — Medallion & Lakehouses

Keeping the original raw HTML files is useful because it gives us a source of truth. If the processing logic is wrong, we can fix the parser and rerun the pipeline without needing to collect the data again.

It also makes debugging easier. For example, if a job title or company name is missing in the JSON output, we can inspect the original HTML to check whether the field was missing from the source file or whether our extraction logic failed.

### Module 2: Treatment Plant — ETL vs ELT & Scale

Cloud systems often prefer ELT because raw data can be loaded first and transformed later using scalable warehouse tools like Snowflake or BigQuery. This keeps the original data available and allows teams to apply different transformations for different use cases.

Processing files sequentially becomes slow when the dataset grows because each file is handled one at a time. Distributed processing tools like Apache Spark solve this by splitting work across many machines or workers, allowing large datasets to be processed much faster.

### Module 3: The Blueprint & The Vault — Storage & Contracts

If an important field like `job_title` disappears, the pipeline should fail early or skip the invalid record with a clear warning. Silently inserting `null` values can damage the quality of the database and cause dashboards or reports to show incorrect results.

Failing early helps catch data problems before they spread downstream. `INSERT OR IGNORE` helps prevent duplicate records by ignoring rows with the same primary key, such as the same `source_id`, making the load step safer to rerun.

### Module 4: The QA Inspector & Orchestrator — Orchestration & DAGs

If `processor.py` crashes halfway, only some HTML files may be converted into JSON. This creates a partial output, so the next stage may load incomplete data unless the output folder is cleaned or the failed step is rerun properly.

Orchestration tools like Airflow are more reliable because they track task status, dependencies, retries, logs, and schedules. Instead of manually remembering what failed, the orchestrator knows which task failed and can retry or stop the pipeline safely.











