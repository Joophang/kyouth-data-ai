# AI-Powered Job Tagging & Skill Gap Analysis

## Project Overview

This project implements a mini AI-assisted data processing pipeline using Python and SQLite.

The system consists of two major components:

1. **Job Tech Stack Tagging**
   - Reads job descriptions from a SQLite database
   - Uses Google Gemini models to extract technical skills
   - Stores the extracted skills into the `tech_stack` column

2. **Skill Gap Analysis**
   - Reads a transformed resume text file
   - Compares resume skills against job market skills from the database
   - Identifies missing technical skills (skill gaps) deterministically

The project focuses on:
- AI-assisted extraction
- Deterministic skill comparison
- Structured data processing
- Error handling and resilience



# Setup Instructions

## Prerequisites

- Python 3.12+
- uv package manager
- Google AI Studio API Key
- SQLite3

---

## Install uv

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

## Install Dependencies
```uv add google-generativeai python-dotenv pydantic```

## Environment Variables
Create a .env file at the project root:
```GOOGLE_API_KEY=your_api_key_here```

## Generate Gemini API Key
Create a free API key from:
https://aistudio.google.com/app/apikey

# Usage
### Part 1 — Prompt Model Testing
Run:
```uv run prompt_model.py```

### Part 2 — Job Tech Stack Tagging
Rn: 
```uv run tag_data.py```
The script:
Reads job descriptions from SQLite
Sends batch prompts to Gemini
Updates the tech_stack column

### Part 3 — Skill Gap Analysis
Run: 
```uv run find_skill_gaps.py```
The script:
Reads skills from tagged jobs
Reads resume text
Compares skills deterministically
Returns missing technical skills


# API/ Function Reference
1. ```prompt_model(model: str, prompt: str) -> str```
- Prompts a Gemini model and returns a text response.
- Input: model(Gemini model name), prompt(Input prompt)
- Output: Generated response text

2. ```tag_data(db_url: str)```
- Extracts technical skills from job descriptions and updates the SQLite database
- Input: db_url(Path to SQLite database)
- Output: Updates tech_stack column in database.

3. ```find_skill_gaps(input_file_path: str, db_url: str) -> SkillGapResult```
- Determines missing technical skills from a resume.
- Input: input_file_path(Path to transformed resume text), db_url(SQLite database path)
- Output: A list of skills

# Data / Assumptions
## Database Schema
The project uses a SQLite database containing a jobs table
Example schema:
```
CREATE TABLE jobs (
    source_id TEXT PRIMARY KEY,
    job_title TEXT,
    company TEXT,
    description TEXT,
    tech_stack TEXT
);
```

## Input assumptions
### Resume
Resume is already transformed into plain text
Technical skills appear explicitly in text
Resume uses English terminology

### Job Skills
tech_stack contains comma-separated technical skills
Skills are AI-generated from job descriptions

# Data Flow
```
Job Descriptions
        ↓
Gemini Skill Extraction
        ↓
SQLite tech_stack column
        ↓
Resume Skill Matching
        ↓
Skill Gap Analysis
```

## Testing
### Testing Methods
The system was tested using:
- Multiple job descriptions
- Empty database cases
- API quota failures
- Invalid responses from Gemini

## Validation
### Determination
The final skill gap comparison uses:
- lowercase normalization
- Regex matching
- Python set operations
- sorted outputs
- This ensures consistent outputs across runs.

## Error Handling
The system handles:
- API failures
- Missing API keys
- Empty responses
- Invalid AI outputs
- Database errors
- without crashing

## Limitations
### AI Tagging Accuracy
Gemini-generated tech stacks may:
- miss niche skills
- generate inconsistent naming
- over-generalize skills

## Regex-Based Resume Matching
The deterministic matching approach:
- only matches known skills
- cannot infer semantic equivalents

## Free Tier API Limits
Gemini free-tier quotas may:
- throttle requests
- delay responses
- return quota exceeded errors

# Architecture Reflection
## Design Choices

The project separates:
- AI extraction (tag_data.py)
- deterministic analysis (find_skill_gaps.py)
This improves modularity and reliability.

SQLite was chosen because:
- lightweight
- simple local setup
- sufficient for structured storage
Pydantic was used to enforce structured outputs.

## Trade-offs
### Determinism vs AI Flexibility
The project prioritizes deterministic outputs over fully AI-driven reasoning.
Instead of using LLMs for skill gap analysis directly, Python set comparison and Regex matching were used to ensure stable outputs.
This reduces hallucination risk and inconsistent results.

## Improvements
Given more time, improvements could include:
skill synonym normalization
MCP-based database interaction
semantic embedding similarity
benchmarking and profiling
better prompt optimization
caching repeated AI responses
larger skill taxonomy database
asynchronous batch processing



