# AI Mock Interview Test System

> **Portfolio Project:** AI-assisted interview assessment platform featuring automated question generation against dynamic job descriptions, statistical NLP scoring algorithms (Answer Relevance, Technical Clarity, Keyword Coverage), real-time sentiment/tone profiling, and audio/text stream processing.

---

> [!WARNING]
> **Verification Status Disclaimer:**  
> This project codebase was authored in accordance with resume specifications and software engineering design patterns. **It has not been executed, compiled, tested, or deployed in a live environment within this generation turn.** Pre-flight validation, dependency installation, and local runtime verification must be conducted by the user before running in a production or evaluation setting.

---

## 1. Resume Technology Alignment

| Resume Item | Implementation in AI Mock Interview Test System |
| :--- | :--- |
| **NLP Models for Real-Time Response Generation** | Dynamic question generator engine (`question_generator.py`) parsing raw job description text, extracting technical competencies, and generating structured questions. |
| **Sentiment Analysis & Tone Profiling** | Heuristic & lexicon-based NLP tone analyzer (`sentiment_analyzer.py`) quantifying assertiveness, hesitation markers, and confidence scores (0-100%). |
| **Answer Scoring Algorithms** | Multi-metric evaluation pipeline (`evaluation_engine.py`):<br>1. **Answer Relevance** (lexical/semantic overlap with question intent)<br>2. **Technical Clarity** (sentence length cadence & filler word penalty)<br>3. **Keyword Coverage** (ratio of required technical competencies articulated) |
| **Audio/Text Stream Processing** | Lightweight session stream manager (`stream_handler.py`) supporting real-time token ingestion, silence/pause detection, and live waveform visualization. |
| **Dynamic UI Components** | Modern React 18 cockpit UI with interactive waveform visualizers, dynamic JD inputs, and multi-dimensional evaluation scorecards. |

---

## 2. Accurate AI Behavior Labeling (Prototype & Statistical NLP)

In accordance with transparent engineering principles:
- **Scoring Pipeline:** The current implementation uses **explainable statistical NLP metrics** (token normalization, Jaccard/Dice lexical similarity, heuristic readability indices, and disfluency ratios). It does not require paid external LLM API keys to run out-of-the-box.
- **Sentiment Engine:** Employs a deterministic rule- and lexicon-based profiler measuring assertive vs. hesitant linguistic markers.
- **Pluggable Extension Interface:** The codebase is architected with clean dependency separation, allowing engineers to plug in transformer embeddings (e.g., Sentence-BERT), LLM judge evaluators, or speech-to-text engines (e.g., Whisper) without changing API contracts.

---

## 3. Architecture & Project Layout

```text
AI_Mock_Interview/
├── .env.example                               # Environment configuration template
├── .gitignore                                 # Git ignore rules for Python & Node
├── README.md                                  # Architectural overview & setup instructions
├── backend/
│   ├── evaluation_engine.py                   # Automated scoring algorithms (relevance, clarity, keywords)
│   ├── main.py                                # FastAPI REST API, WebSocket handler, CORS
│   ├── question_generator.py                  # Dynamic JD parsing & question generation engine
│   ├── requirements.txt                       # FastAPI, Uvicorn, Pydantic, WebSockets
│   ├── schemas.py                             # Pydantic data models & request/response contracts
│   ├── sentiment_analyzer.py                  # Lexicon-based sentiment & confidence profiler
│   └── stream_handler.py                      # Real-time audio/text stream processing service
├── data/
│   ├── sample_evaluation_benchmark.json       # Labeled synthetic candidate responses (strong vs weak)
│   └── sample_job_descriptions.json           # Labeled synthetic job descriptions across roles
└── frontend/
    ├── index.html                             # Single-page HTML entry point
    ├── package.json                           # React 18, Vite dependencies & scripts
    ├── vite.config.js                         # Bundler & backend proxy config (port 5174)
    └── src/
        ├── App.jsx                            # Main multi-step session controller
        ├── index.css                          # Dark-mode cockpit stylesheet & waveform styles
        ├── main.jsx                           # React root mount point
        └── components/
            ├── EvaluationScorecard.jsx        # Multi-dimensional score breakdown & coaching tips
            ├── JobDescriptionInput.jsx        # Dynamic JD input & preset benchmark loader
            ├── LiveInterviewRoom.jsx          # Live interview prompt & response workstation
            └── StreamSimulator.jsx            # Live audio waveform & streaming token buffer
```

---

## 4. Synthetic Sample Data & Benchmarks

The project includes pre-built synthetic benchmark datasets in `data/`:
1. **`sample_job_descriptions.json`**:
   - *Full-Stack Software Engineer (React & Python)*
   - *Data Analyst & BI Specialist (SQL & Power BI)*
   - *Machine Learning Engineer (NLP & Computer Vision)*
2. **`sample_evaluation_benchmark.json`**:
   - Benchmark candidate responses comparing an **architecturally detailed answer** (demonstrating ~90% scores) against a **hesitant, filler-dense response** (demonstrating ~40% scores) to validate the scoring algorithms.

---

## 5. Setup & Execution Instructions

### Prerequisites
- **Python 3.9+**
- **Node.js 18+ & npm**

---

### Step 1: Backend Setup (FastAPI)

1. Open a terminal and navigate to `backend/`:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8001
   ```
   - API Root: `http://localhost:8001`
   - Interactive Swagger Docs: `http://localhost:8001/docs`

---

### Step 2: Frontend Setup (React 18 & Vite)

1. Open a second terminal and navigate to `frontend/`:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Launch the Vite development server:
   ```bash
   npm run dev
   ```
   - Application URL: `http://localhost:5174`

---

## 6. Core REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Healthcheck and active AI engine mode status |
| `GET` | `/api/jobs/samples` | Retrieve pre-loaded synthetic job description benchmarks |
| `GET` | `/api/benchmarks/samples` | Retrieve strong/weak candidate benchmark samples |
| `POST` | `/api/questions/generate` | Dynamically generate tailored questions from raw JD text |
| `POST` | `/api/evaluations/score` | Execute automated relevance, clarity, and keyword scoring |
| `POST` | `/api/evaluations/sentiment` | Standalone sentiment and confidence tone evaluation |
| `POST` | `/api/sessions/start` | Initialize live audio/text stream session buffer |
| `POST` | `/api/sessions/chunk` | Append stream token chunk with amplitude telemetry |
| `POST` | `/api/sessions/finalize` | Finalize session and retrieve assembled candidate transcript |
| `WS` | `/api/ws/session/{session_id}` | WebSocket stream for live interactive session testing |
