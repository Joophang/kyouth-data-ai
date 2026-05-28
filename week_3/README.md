# Week 3 Full-Stack AI Chat Application

## Project Overview

This project is a containerized full-stack chat application. It consists of:

* A frontend service that displays a chat page, accepts user messages, supports PDF upload, converts PDF content into text, and sends the data to the backend.
* A backend service built with FastAPI that exposes a `POST /chat` endpoint.
* AI model integration using the Week 2 `prompt_model()` function.
* Docker and Docker Compose for containerizing and running both services together.

The goal of this project is to connect a frontend chat interface to a backend AI service and run both services in separate Docker containers.

---

## Setup Instructions

### Prerequisites

Make sure the following are installed:

* Docker
* Docker Compose
* Git

Optional for local development without Docker:

* Python 3.14+
* `uv`

---

## Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
BACKEND_URL=http://localhost:8000/chat
```

Do not commit your real `.env` file.

A `.env.example` file is provided as a template.

---

## Running with Docker Compose

From the project root, run:

```bash
docker compose up --build
```

This will build and start both services:

* Frontend: `http://localhost:8080`
* Backend: `http://localhost:8000`

Open the frontend in your browser:

```text
http://localhost:8080
```

---

## Manual Setup with uv

If running manually without Docker:

### Backend

```bash
cd backend
uv sync
uv run uvicorn --app-dir src main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
uv sync
uv run uvicorn --app-dir src main:app --reload --port 8080
```

---

## Usage

1. Open the frontend page.
2. Type a message into the chat input.
3. Optionally upload a PDF file.
4. Click Send.
5. The frontend converts the PDF into text and sends the user message and PDF text to the backend.
6. The backend passes the combined prompt to the Week 2 AI function.
7. The chatbot response is displayed in the chat history.

Example input:

```text
Can you help improve my resume?
```

Example JSON sent to backend:

```json
{
  "message": "Can you help improve my resume?",
  "pdf_text": "Extracted resume text here..."
}
```

Example backend response:

```json
{
  "reply": "Here are some suggestions to improve your resume..."
}
```

---

## API / Function Reference

### Backend API

#### `POST /chat`

Receives a JSON request from the frontend and returns an AI-generated response.

Request body:

```json
{
  "message": "User message",
  "pdf_text": "Extracted PDF text"
}
```

Response body:

```json
{
  "reply": "AI response"
}
```

The backend calls:

```python
prompt_model(model="gemini-2.5-flash-lite", prompt=full_prompt)
```

where `full_prompt` combines the user message and extracted PDF text.

---

## Frontend Key Functions

### `addMessage(text, sender)`

Adds a message bubble to the chat history.

### `readPdfAsText(file)`

Reads the uploaded PDF and extracts text from it using PDF parsing logic in the frontend.

### Form submit handler

Handles the chat form submission, creates a JSON payload, sends it to the backend using `fetch()`, and displays the backend response.

---

## Docker Service Interaction

The project uses Docker Compose with two services:

* `frontend`
* `backend`

Both services run in the same Docker bridge network.

The frontend is accessed from the browser at:

```text
http://localhost:8080
```

The backend is exposed at:

```text
http://localhost:8000
```

The frontend sends chat requests to the backend `/chat` endpoint.

---

## Data / Assumptions

The system sends data between frontend and backend using JSON.

Expected request format:

```json
{
  "message": "string",
  "pdf_text": "string"
}
```

Assumptions:

* The user message is plain text.
* Uploaded files are PDF files.
* PDF text extraction may not work perfectly for scanned/image-based PDFs.
* Large PDFs may produce long prompts and may slow down the AI response.
* The Week 2 AI function is already implemented and available to the backend.
* The backend requires a valid `GOOGLE_API_KEY` if using Gemini.

Data flow:

1. User enters a message and uploads a PDF.
2. Frontend extracts text from the PDF.
3. Frontend sends JSON to the backend.
4. Backend combines message and PDF text into a prompt.
5. Backend calls the Week 2 AI model function.
6. Backend returns the AI response.
7. Frontend displays the response in the chat UI.

---

## Testing

### Backend Test with curl

Run:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Help me improve my resume","pdf_text":"Python Docker FastAPI"}'
```

Expected response:

```json
{
  "reply": "..."
}
```

### Frontend Test

1. Run the project using Docker Compose.
2. Open:

```text
http://localhost:8080
```

3. Send a normal text message.
4. Confirm that the chatbot displays a response.
5. Upload a PDF and send a message.
6. Confirm that the backend receives both the message and extracted PDF text.

### Docker Communication Test

To confirm containers are running:

```bash
docker compose ps
```

To view logs:

```bash
docker compose logs frontend
docker compose logs backend
```

The frontend should successfully send requests to the backend `/chat` endpoint.

---

## Limitations

* Chat history is only displayed in the browser and is not saved to a database.
* No user authentication is implemented.
* PDF extraction may fail or return incomplete text for scanned PDFs.
* Large PDF files may create very long prompts.
* AI responses depend on the model and may not always be fully accurate.
* The current UI is simple and does not include advanced loading states, retry logic, or persistent sessions.
* Error handling is basic and mainly returns a simple backend error message.

---

## Architecture Reflection

### Design Choices

This project uses a frontend/backend separation to keep the user interface and AI processing logic independent. The frontend focuses on collecting user input, handling PDF upload, and displaying chat messages. The backend focuses on processing the request and calling the Week 2 AI function.

Each service is containerized separately using Docker. This makes the project easier to run consistently across different machines because dependencies are isolated inside containers.

Docker Compose is used to run both services together with one command. It also creates a shared bridge network so the services can communicate.

### Trade-offs

The design prioritizes simplicity and ease of deployment. Docker Compose makes it easy to start the full application, but the system is still relatively simple.

The frontend uses basic HTML, Bootstrap, and JavaScript instead of a full frontend framework. This keeps the project easier to understand but limits advanced UI features.

The backend directly calls the AI function from Week 2. This keeps integration simple, but it does not include advanced queueing, caching, or request management.

### Improvements

With more time, I would improve the project by:

* Adding a database to save chat history.
* Improving PDF extraction for scanned documents using OCR.
* Adding user authentication.
* Improving frontend UI with loading indicators and better error messages.
* Adding automated tests.
* Deploying the services to a cloud platform.
* Using a more structured frontend framework such as React.
