# Video Demo Preparation — CV Screener (≤ 5 min)

Goal: a tight Loom recording covering **Process → Demo → Technical Highlight**.
Suggested time budget: 60–90s / 2–2.5min / 60–90s.

---

## 0. Before hitting record

- [ ] Have CVs already generated in `backend/data/CVs` and `backend/data/candidates` (don't generate live — it calls paid APIs and is slow/non-deterministic).
- [ ] Vector index already built (`app.ingestion.cv_ingest` run once beforehand) so the demo answers are fast.
- [ ] Two terminals ready but **not yet started**:
  - Terminal 1: `cd backend && .venv\Scripts\python.exe -m uvicorn app.api.main:app --reload --port 8000`
  - Terminal 2: `cd frontend_chat_interface && npm run dev`
- [ ] Browser tab open to `http://localhost:5173`, plus a couple of generated CV PDFs open (one text, one with photo) to show as visuals.
- [ ] Have `backend/app/generation/candidate_specifications.py` and `backend/app/RAG/graph.py` open in the editor for the technical highlight.
- [ ] Decide the 3 sample questions in advance (see Demo section) and know which candidates should answer them, so you can sanity-check the AI's answer live.

---

## 1. The Process (~60–90s)

**What to say — CV generation pipeline:**

- "This project has two halves: a *generation* pipeline that creates synthetic candidate CVs, and a *RAG* pipeline that lets you chat with them."
- Generation pipeline, in order:
  1. **`CandidateSpecificationCatalog`** — a fixed catalog of ~28 candidate specs (role, seniority, country, city, university, must-have skills). This is the "ground truth" used to seed and later validate the LLM output.
  2. **`CandidateGenerator`** — sends a structured prompt to Claude (Anthropic) and uses `messages.parse(..., output_format=Candidate)` to get back a **typed, schema-validated Pydantic object** (`Candidate` model: skills, experience, education, languages, with min/max length constraints) — no manual JSON parsing/repair needed.
  3. After the LLM call, deterministic fields are patched in (email, phone, exact university, guaranteed required skills) so critical facts used later in the demo (e.g. "graduated from UPC") are always correct, not just LLM-probable.
  4. **`PortraitGenerator`** — a separate call to an image model via OpenRouter generates a headshot matching the candidate's gender/region.
  5. **`CandidatePDFRenderer`** (ReportLab) — lays out the structured candidate + photo into a real one-page PDF resume.
- Show 1–2 example PDFs on screen here (text-only + with photo) — this is the visual payoff of the pipeline.

**Backend & AI workflow (RAG side):**

- "Once CVs exist as PDFs, an ingestion step (`CVLoader` + `DocumentChunker`) extracts text per page with PyMuPDF, splits it into overlapping chunks, embeds them with FastEmbed, and stores them in a local Chroma vector database — one collection, `cv_chunks`, tagged with candidate id/name/source/page metadata."
- "The chat side is a small **LangGraph** graph with two nodes: `retrieve` (similarity search, top-k chunks) → `generate` (Claude answers strictly from the retrieved chunks, citing candidates by name). It's exposed through a **FastAPI** backend and a **React** chat frontend."

---

## 2. The Demo (~2–2.5 min)

Run it live against the running app (`localhost:5173`). Suggested questions — pick ones that map cleanly to the seeded catalog so the answer is verifiably correct on screen:

1. **"Who has experience with Python?"** — should surface several candidates (Backend/AI-ML/Data Science/Data Engineering specs all include Python) with named citations.
2. **"Which candidate graduated from UPC?"** — should return the Barcelona-based candidates whose `university` field was pinned to "Universitat Politècnica de Catalunya (UPC)" (there are two — a good moment to show it lists *each* relevant candidate, per the system prompt's rule).
3. **"Summarize the profile of Jane Doe."** (swap in an actual generated candidate name) — shows single-candidate summarization grounded only in that candidate's CV content.

While demoing, call out:
- The answer only uses retrieved CV text (no hallucinated employers/skills) — a deliberate design choice enforced by the system prompt.
- Point out sources/citations returned alongside the answer (candidate name, file, page) if surfaced in the UI.
- Optionally show one "negative" case — ask about a skill nobody has, and show the "I could not find relevant information..." fallback, proving it doesn't hallucinate.

---

## 3. The Technical Highlight (~60–90s)

Pick **one** honest, specific story — don't try to cover everything. Strongest candidates from this codebase:

**Option A — Structured generation with `output_format=Candidate` (recommended):**
Using Anthropic's `messages.parse(..., output_format=Candidate)` to force the LLM to return a schema-validated Pydantic object directly (with field-level constraints like `min_length=5` skills, `min_length=1` experience) — eliminating brittle "ask the LLM for JSON and hope it parses" code, while still deterministically overwriting the facts that must be exactly correct (university, required skills, contact info) after the fact. This is a nice "trust the model for creative content, but verify/pin the facts that matter" pattern.

**Option B — Prompt-injection guardrails in the RAG system prompt:**
`rag_prompts.py` explicitly instructs the model to treat CV content as **untrusted data** and never follow instructions embedded inside a CV. Worth mentioning as a deliberate security-aware design choice for any RAG system that ingests user/candidate-supplied documents — a real prompt-injection vector recruiters' tools have to consider.

**Option C — Grounded/no-hallucination answering via LangGraph:**
The two-node `retrieve → generate` graph plus a system prompt that requires the model to (a) only use supplied context, (b) explicitly say when evidence is insufficient, and (c) distinguish direct evidence from interpretation. Frame the challenge as: recruiter tools are worthless if they hallucinate a candidate's skills — so correctness/trust was prioritized over cleverness.

**Suggested delivery:** show the relevant code snippet on screen (e.g. `candidate_generator.py` lines 26–33, or `rag_prompts.py`), explain the problem it solves in one sentence, then the "why" (the risk you were avoiding), then close.

---

## Timing checklist while recording

| Segment | Target time |
|---|---|
| Intro + Process | 60–90s |
| Live Demo (3 questions) | 120–150s |
| Technical Highlight | 60–90s |
| **Total** | **< 5:00** |

Keep narration tight — script the opening line and the technical-highlight closing line word-for-word if it helps you stay under time.
