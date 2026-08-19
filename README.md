# CV Screener

This is a small project I built to try out generating fake CVs with AI and
then chatting with them using RAG (retrieval-augmented generation).

Basically it does 3 things:

1. Generates fake candidate CVs (text + photo + PDF) using an LLM.
2. Loads those CV PDFs, splits them into chunks, and stores them in a local
   vector database (Chroma).
3. Lets you ask questions like "who knows Python?" and it searches the CVs
   and answers based only on what's actually in them.

You can use it either from the terminal, or with a simple web page
(React frontend + FastAPI backend).

## Folder structure

```
CV-Screener/
├── .env                # your API keys and settings (not committed)
├── .env.example        # example of what .env should look like
├── backend/             # python code
│   ├── app/
│   │   ├── api/          # FastAPI app
│   │   ├── core/          # logging
│   │   ├── generation/    # generates fake CVs
│   │   ├── ingestion/     # loads PDFs into the vector db
│   │   ├── models/        # candidate data model
│   │   └── RAG/           # the chat/question-answering part
│   ├── data/             # generated CVs, photos, vector db
│   └── tests/
└── frontend_chat_interface/   # the web UI
```

## What you need

- Python 3.11+
- Node.js and npm
- An Anthropic API key (for generating CV text and answering questions)
- An OpenRouter API key (for generating the candidate photos)

## Setup

Copy `.env.example` to `.env` and put your API keys in it:

```
ANTHROPIC_API_KEY=...
OPENROUTER_API_KEY=...
```

There are a few other settings in there too (model names, folder paths,
chunk size etc) but the defaults are fine to start with.

Install the backend stuff:

```
cd backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Install the frontend stuff:

```
cd frontend_chat_interface
npm install
```

## How to run it

### 1. Generate the fake CVs (optional)

Only needed if you don't already have CVs in `backend/data/resumes`. This calls
the paid APIs so it costs a bit of money.

```
cd backend
.venv\Scripts\python.exe -m app.generation.generate_cvs
```

### 2. Build the search index

This reads the CV PDFs and puts them into the local vector database. It's
free, runs locally.

```
.venv\Scripts\python.exe -m app.ingestion.cv_ingest
```

Run this again whenever you add/change the CV PDFs.

### 3. Ask questions

You can either use the web page or just the terminal.

**Web page** — needs two terminals open at the same time:

```
# terminal 1
cd backend
.venv\Scripts\python.exe -m uvicorn app.api.main:app --reload --port 8000

# terminal 2
cd frontend_chat_interface
npm run dev
```

Then go to http://localhost:5173 in your browser and type a question.

**Terminal only**, no need for the frontend:

```
cd backend
.venv\Scripts\python.exe -m app.RAG.chat
```

(type `exit` to quit)

## Running the tests

```
cd backend
.venv\Scripts\python.exe -m pytest tests\unit -v
```

These are just local tests, no API calls needed.

## If something's not working

- **"Failed to fetch" on the web page** → the backend isn't running. Check
  the uvicorn terminal is still open.
- **"I could not find relevant information..."** → the search index is
  empty, run step 2 again.
- **Port already used** → close whatever is using port 8000 or 5173, or
  change the port and update it in `frontend_chat_interface/src/App.jsx`.
